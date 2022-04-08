from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginAndNotDeletedRequiredMixin
from django.shortcuts import redirect, render
from django.views import generic as views
from django.urls import reverse_lazy
from labsystem.laboratory.forms.analysis_forms import DeleteAnalysisForm, RestoreAnalysisForm, \
    CreateEditAnalysisForm
from labsystem.laboratory.models import Analysis
from utils.validators import validate_only_letters_and_spaces
from utils.view_mixins import StaffRequiredMixin
from django.db.models import Q


class CreateAnalysisView(LoginAndNotDeletedRequiredMixin, StaffRequiredMixin, views.CreateView):
    form_class = CreateEditAnalysisForm
    template_name = 'laboratory/analysis/analysis_create.html'
    success_url = reverse_lazy('all analyses')


class EditAnalysisView(LoginAndNotDeletedRequiredMixin, StaffRequiredMixin, views.UpdateView):
    model = Analysis
    form_class = CreateEditAnalysisForm
    context_object_name = 'analysis'
    template_name = 'laboratory/analysis/analysis_edit.html'
    success_url = reverse_lazy('all analyses')


@staff_member_required
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


@staff_member_required
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
    ITEMS_PER_PAGE = 5
    Model = Analysis
    template_name = 'laboratory/analysis/analysis_nondeleted_list.html'
    context_object_name = 'all_analyses'
    queryset = Analysis.objects.filter(deleted_at=None)
    paginate_by = ITEMS_PER_PAGE


class DeletedAnalysisListView(LoginAndNotDeletedRequiredMixin, StaffRequiredMixin, views.ListView):
    ITEMS_PER_PAGE = 5
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


class SearchAnalysesView(views.ListView):
    ITEMS_PER_PAGE = 10
    Model = Analysis
    template_name = 'laboratory/analysis/analysis_search.html'
    context_object_name = 'all_analyses'
    paginate_by = ITEMS_PER_PAGE

    def get_queryset(self):
        query = self.request.GET.get("search")
        if query == '':
            all_analyses = []
        elif validate_only_letters_and_spaces(query):
            all_analyses = Analysis.objects.filter(
                Q(name__icontains=query) & Q(deleted_at=None))
        else:
            all_analyses = []

        return all_analyses
