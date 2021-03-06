from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginAndNotDeletedRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.views import generic as views
from django.urls import reverse_lazy
from labsystem.laboratory.forms.health_facility_forms import DeleteHealthFacilityForm, RestoreHealthFacilityForm, \
    CreateEditHealthFacilityForm
from labsystem.laboratory.models import HealthFacility
from utils.view_mixins import StaffRequiredMixin


class HealthFacilityCreation(LoginAndNotDeletedRequiredMixin, StaffRequiredMixin, views.CreateView):
    model = HealthFacility
    form_class = CreateEditHealthFacilityForm
    template_name = 'laboratory/health_facility/health_facility_create.html'
    success_url = reverse_lazy('all health facilities')


class EditHealthFacility(LoginAndNotDeletedRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, views.UpdateView):
    model = HealthFacility
    form_class = CreateEditHealthFacilityForm
    context_object_name = 'facility'
    template_name = 'laboratory/health_facility/health_facility_edit.html'
    success_url = reverse_lazy('all health facilities')


@staff_member_required
def delete_health_facility(request, pk):
    facility = HealthFacility.objects.get(pk=pk)
    if request.method == 'POST':
        form = DeleteHealthFacilityForm(request.POST, instance=facility)
        if form.is_valid():
            form.save()
            return redirect('all health facilities')
    else:
        form = DeleteHealthFacilityForm(instance=facility)

    context = {
        'form': form,
        'facility': facility
    }
    return render(request, 'laboratory/health_facility/health_facility_delete.html', context)


@staff_member_required
def restore_health_facility(request, pk):
    facility = HealthFacility.objects.get(pk=pk)
    if request.method == 'POST':
        form = RestoreHealthFacilityForm(request.POST, instance=facility)
        if form.is_valid():
            form.save()
            return redirect('all analysis')
    else:
        form = RestoreHealthFacilityForm(instance=facility)

    context = {
        'form': form,
        'facility': facility
    }
    return render(request, 'laboratory/health_facility/health_facility_restore.html', context)


class HealthFacilityListView(LoginAndNotDeletedRequiredMixin, StaffRequiredMixin, views.ListView):
    ITEMS_PER_PAGE = 10
    Model = HealthFacility
    template_name = 'laboratory/health_facility/health_facilities_nondeleted_list.html'
    context_object_name = 'all_facilities'
    queryset = HealthFacility.objects.filter(deleted_at=None)
    paginate_by = ITEMS_PER_PAGE


class DeletedHealthFacilityListView(LoginAndNotDeletedRequiredMixin, StaffRequiredMixin, views.ListView):
    ITEMS_PER_PAGE = 10
    Model = HealthFacility
    template_name = 'laboratory/health_facility/health_facilities_deleted_list.html'
    context_object_name = 'all_deleted_facilities'
    queryset = HealthFacility.objects.exclude(deleted_at=None)
    paginate_by = ITEMS_PER_PAGE
