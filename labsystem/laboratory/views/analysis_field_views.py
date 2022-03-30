from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import generic as views
from django.urls import reverse_lazy

from labsystem.laboratory.forms.analysis_field_forms import CreateAnalysisFieldForm, DeleteAnalysisFieldForm, \
    RestoreAnalysisFieldForm
from labsystem.laboratory.models import AnalysisField
from utils.view_mixins import StaffRequiredMixin


class CreateAnalysisFieldView(LoginRequiredMixin, StaffRequiredMixin, views.CreateView):
    form_class = CreateAnalysisFieldForm
    template_name = 'laboratory/analysis_field/analysis_field_create.html'
    success_url = reverse_lazy('all analysis fields')


class EditAnalysisFieldView(LoginRequiredMixin, StaffRequiredMixin, views.UpdateView):
    model = AnalysisField
    context_object_name = 'analysis_field'
    template_name = 'laboratory/analysis_field/analysis_field_edit.html'
    fields = (
        'name',
        'unit',
        'male_min',
        'male_max',
        'female_min',
        'female_max',
        'comment',
    )
    success_url = reverse_lazy('all analysis fields')


def delete_analysis_field_view(request, pk):
    analysis_field = AnalysisField.objects.get(pk=pk)
    if request.method == 'POST':
        form = DeleteAnalysisFieldForm(request.POST, instance=analysis_field)
        if form.is_valid():
            form.save()
            return redirect('all analysis fields')
    else:
        form = DeleteAnalysisFieldForm(instance=analysis_field)

    context = {
        'form': form,
        'analysis_field': analysis_field
    }
    return render(request, 'laboratory/analysis_field/analysis_field_delete.html', context)


def restore_analysis_field_view(request, pk):
    analysis_field = AnalysisField.objects.get(pk=pk)
    if request.method == 'POST':
        form = RestoreAnalysisFieldForm(request.POST, instance=analysis_field)
        if form.is_valid():
            form.save()
            return redirect('all analysis fields')
    else:
        form = RestoreAnalysisFieldForm(instance=analysis_field)

    context = {
        'form': form,
        'analysis_field': analysis_field
    }
    return render(request, 'laboratory/analysis_field/analysis_field_restore.html', context)


class AnalysisFieldsListView(LoginRequiredMixin, StaffRequiredMixin, views.ListView):
    FACILITY_PER_PAGE = 10
    Model = AnalysisField
    template_name = 'laboratory/analysis_field/analysis_field_nondeleted_list.html'
    context_object_name = 'all_analysis_fields'
    queryset = AnalysisField.objects.filter(deleted_at=None)
    paginate_by = FACILITY_PER_PAGE


class DeletedAnalysisFieldsListView(LoginRequiredMixin, StaffRequiredMixin, views.ListView):
    FACILITY_PER_PAGE = 10
    Model = AnalysisField
    template_name = 'laboratory/analysis_field/analysis_field_deleted_list.html'
    context_object_name = 'all_deleted_analysis_fields'
    queryset = AnalysisField.objects.exclude(deleted_at=None)
    paginate_by = FACILITY_PER_PAGE
