from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic as views
from django.urls import reverse_lazy

from labsystem.laboratory.forms.result_form import CreateResultForm
from labsystem.laboratory.models import Profile, Result, Analysis, ResultLine
from utils.view_mixins import StaffRequiredMixin


class CreateResultView(LoginRequiredMixin, StaffRequiredMixin, views.CreateView):
    form_class = CreateResultForm
    template_name = 'laboratory/result/result_create.html'
    success_url = reverse_lazy('index')
    context_object_name = 'result'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = Profile.objects.get(pk=self.kwargs['pk'])
        context['patient'] = patient
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.patient = Profile.objects.get(pk=self.kwargs['pk'])
        self.object.analysis_price = Analysis.objects.get(pk=self.object.analysis.pk).price
        self.object.save()
        return super().form_valid(form)


class EditResultView(LoginRequiredMixin, StaffRequiredMixin, views.UpdateView):
    model = Result
    context_object_name = 'result'
    template_name = 'laboratory/result/result_edit.html'
    success_url = reverse_lazy('')
    fields = (
        'referring_physician',
        'sample_type',
        'sample_collection_time',
        'payment_amount',
        'payment_type',
    )


class PatientSpecificResultListView(LoginRequiredMixin, views.ListView):
    ITEMS_PER_PAGE = 10
    Model = Result
    template_name = 'laboratory/result/patient_specific_result_list.html'
    context_object_name = 'all_results'
    paginate_by = ITEMS_PER_PAGE

    def get_queryset(self):
        return Result.objects.filter(patient=Profile.objects.get(pk=self.kwargs['pk']))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        patient = Profile.objects.get(pk=self.kwargs['pk'])
        is_patient = self.request.user.is_patient
        is_staff = self.request.user.is_staff
        is_physician = self.request.user.is_physician
        context['patient'] = patient
        context['is_patient'] = is_patient
        context['is_staff'] = is_staff
        context['is_physician'] = is_physician
        return context


class ResultDetailsView(views.DetailView):
    model = Result
    template_name = 'laboratory/result/result_details.html'
    context_object_name = 'result_context'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        patient = Profile.objects.get(pk=self.kwargs['patient_pk'])
        result = Result.objects.get(pk=self.kwargs['pk'])
        result_lines = ResultLine.objects.filter(result_id=result.pk)
        context['patient'] = patient
        context['result'] = result
        context['result_lines'] = result_lines
        return context


class EditResultLineView(LoginRequiredMixin, StaffRequiredMixin, views.UpdateView):
    VALUE_IN_RANGE_COMMENT = 'Value in normal range'
    NO_SEX_COMMENT = 'Value in normal range'
    model = ResultLine
    context_object_name = 'result_line'
    template_name = 'laboratory/result/result_line_edit.html'
    success_url = reverse_lazy('result details')
    fields = (
        'value',
    )

    def form_valid(self, form):
        self.object = form.save(commit=False)
        value = self.object.value
        sex = self.object.result.patient.sex.name
        comment = self.VALUE_IN_RANGE_COMMENT
        if sex == 'Male':
            if not self.object.analysis_field.male_min <= value <= self.object.analysis_field.male_max:
                comment = self.object.analysis_field.comment
        elif sex == 'Female':
            if not self.object.analysis_field.female_min <= value <= self.object.analysis_field.female_max:
                comment = self.object.analysis_field.comment
        self.object.comment = comment
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('result details',
                            kwargs={
                                'patient_pk': self.object.result.patient.pk,
                                'pk': self.object.result.pk,
                            })
