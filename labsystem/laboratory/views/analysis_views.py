from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import generic as views
from django.urls import reverse_lazy

from labsystem.laboratory.forms.analysis_forms import CreateAnalysisForm, DeleteAnalysisForm, RestoreAnalysisForm
from labsystem.laboratory.models import Analysis
from utils.view_mixins import StaffRequiredMixin


class CreateAnalysisView(LoginRequiredMixin, StaffRequiredMixin, views.CreateView):
    form_class = CreateAnalysisForm
    template_name = 'laboratory/analysis/analysis_create.html'
    success_url = reverse_lazy('all analyses')


class EditAnalysisView(LoginRequiredMixin, StaffRequiredMixin, views.UpdateView):
    model = Analysis
    context_object_name = 'analysis'
    template_name = 'laboratory/analysis/analysis_edit.html'
    fields = (
        'name',
        'description',
        'price',
        'tat',
        'analysis_field',
    )
    success_url = reverse_lazy('all analyses')


def delete_analysis_view(request, pk):
    analysis = Analysis.objects.get(pk=pk)
    if request.method == 'POST':
        form = DeleteAnalysisForm(request.POST, instance=analysis)
        if form.is_valid():
            form.save()
            return redirect('all analyses')
    else:
        form = DeleteAnalysisForm(instance=analysis)

    context = {
        'form': form,
        'analysis': analysis,
    }
    return render(request, 'laboratory/analysis/analysis_delete.html', context)


def restore_analysis_view(request, pk):
    analysis = Analysis.objects.get(pk=pk)
    if request.method == 'POST':
        form = RestoreAnalysisForm(request.POST, instance=analysis)
        if form.is_valid():
            form.save()
            return redirect('all deleted analyses')
    else:
        form = RestoreAnalysisForm(instance=analysis)

    context = {
        'form': form,
        'analysis': analysis
    }
    return render(request, 'laboratory/analysis/analysis_restore.html', context)


class AnalysisListView(views.ListView):
# class AnalysisListView(LoginRequiredMixin, StaffRequiredMixin, views.ListView):
    ITEMS_PER_PAGE = 10
    Model = Analysis
    template_name = 'laboratory/analysis/analysis_nondeleted_list.html'
    context_object_name = 'all_analyses'
    queryset = Analysis.objects.filter(deleted_at=None)
    paginate_by = ITEMS_PER_PAGE

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data()
    #     return context


class DeletedAnalysisListView(LoginRequiredMixin, StaffRequiredMixin, views.ListView):
    ITEMS_PER_PAGE = 10
    Model = Analysis
    template_name = 'laboratory/analysis/analysis_deleted_list.html'
    context_object_name = 'all_analyses'
    queryset = Analysis.objects.exclude(deleted_at=None)
    paginate_by = ITEMS_PER_PAGE


class AnalysisInformationListView(views.ListView):
    ITEMS_PER_PAGE = 10
    Model = Analysis
    template_name = 'laboratory/analysis/analyses_information_list.html'
    context_object_name = 'all_analyses'
    queryset = Analysis.objects.filter(deleted_at=None)
    paginate_by = ITEMS_PER_PAGE