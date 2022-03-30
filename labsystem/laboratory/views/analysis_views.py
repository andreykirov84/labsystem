# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.messages.views import SuccessMessageMixin
# from django.shortcuts import redirect, render
# from django.views import generic as views
# from django.urls import reverse_lazy
#
#
# from labsystem.laboratory.forms.analysis_forms import CreateAnalysisForm, DeleteAnalysisForm, RestoreAnalysisForm
#
# from labsystem.laboratory.models import Analysis
# from utils.view_mixins import StaffRequiredMixin
#
#
# class AnalysisCreation(LoginRequiredMixin, StaffRequiredMixin, views.CreateView):
#     form_class = CreateAnalysisForm
#     template_name = 'laboratory/analysis_create.html'
#     success_url = reverse_lazy('all analysis')
#
#
# class AnalysisView(LoginRequiredMixin, StaffRequiredMixin, views.ListView):
#     ANALYSIS_PER_PAGE = 10
#     Model = Analysis
#     template_name = 'laboratory/analysis_nondeleted_list.html'
#     context_object_name = 'all_analysis'
#     queryset = Analysis.objects.filter(deleted_at=None)
#     paginate_by = ANALYSIS_PER_PAGE
#     ordering = ['-created_on', 'name']
#
#
# class DeletedAnalysisView(LoginRequiredMixin, StaffRequiredMixin, views.ListView):
#     ANALYSIS_PER_PAGE = 10
#     Model = Analysis
#     template_name = 'laboratory/analysis_deleted_list.html'
#     context_object_name = 'all_analysis'
#     queryset = Analysis.objects.exclude(deleted_at=None)
#     paginate_by = ANALYSIS_PER_PAGE
#     ordering = ['-created_on', 'name']
#
#
# class EditAnalysis(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, views.UpdateView):
#     model = Analysis
#     template_name = 'laboratory/analysis_edit.html'
#     fields = (
#         'code',
#         'name',
#         'description',
#         'price',
#         'tat',
#     )
#     success_message = f'The analysis was successfully updated'
#     success_url = reverse_lazy('all analysis')
#
#
# def delete_analysis(request, pk):
#     analysis = Analysis.objects.get(pk=pk)
#     if request.method == 'POST':
#         form = DeleteAnalysisForm(request.POST, instance=analysis)
#         if form.is_valid():
#             form.save()
#             return redirect('all analysis')
#     else:
#         form = DeleteAnalysisForm(instance=analysis)
#
#     context = {
#         'form': form,
#         'analysis': analysis
#     }
#     return render(request, 'laboratory/analysis_delete.html', context)
#
#
# def restore_analysis(request, pk):
#     analysis = Analysis.objects.get(pk=pk)
#     if request.method == 'POST':
#         form = RestoreAnalysisForm(request.POST, instance=analysis)
#         if form.is_valid():
#             form.save()
#             return redirect('all deleted analysis')
#     else:
#         form = RestoreAnalysisForm(instance=analysis)
#
#     context = {
#         'form': form,
#         'analysis': analysis
#     }
#     return render(request, 'laboratory/analysis_restore.html', context)
