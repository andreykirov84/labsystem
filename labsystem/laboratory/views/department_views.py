from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.views import generic as views
from django.urls import reverse_lazy

from labsystem.laboratory.forms.department_forms import DeleteDepartmentForm, RestoreDepartmentForm, \
    CreateDepartmentForm
from labsystem.laboratory.models import Department
from utils.view_mixins import StaffRequiredMixin


class DepartmentCreation(LoginRequiredMixin, StaffRequiredMixin, views.CreateView):
    form_class = CreateDepartmentForm
    template_name = 'laboratory/department_create.html'
    success_url = reverse_lazy('all departments')


class EditDepartment(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, views.UpdateView):
    model = Department
    context_object_name = 'department'
    template_name = 'laboratory/department_edit.html'
    fields = (
        'name',
        'description',
        'telephone_number',
        'email',
    )
    success_message = f'The Department was successfully updated'
    success_url = reverse_lazy('all departments')


def delete_department(request, pk):
    department = Department.objects.get(pk=pk)
    if request.method == 'POST':
        form = DeleteDepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('all departments')
    else:
        form = DeleteDepartmentForm(instance=department)

    context = {
        'form': form,
        'department': department
    }
    return render(request, 'laboratory/department_delete.html', context)


def restore_department(request, pk):
    department = Department.objects.get(pk=pk)
    if request.method == 'POST':
        form = RestoreDepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('all departments')
    else:
        form = RestoreDepartmentForm(instance=department)

    context = {
        'form': form,
        'department': department
    }
    return render(request, 'laboratory/department_restore.html', context)


class DepartmentsListView(LoginRequiredMixin, StaffRequiredMixin, views.ListView):
    FACILITY_PER_PAGE = 10
    Model = Department
    template_name = 'laboratory/department_nondeleted_list.html'
    context_object_name = 'all_departments'
    queryset = Department.objects.filter(deleted_at=None)
    paginate_by = FACILITY_PER_PAGE


class DeletedDepartmentsListView(LoginRequiredMixin, StaffRequiredMixin, views.ListView):
    FACILITY_PER_PAGE = 10
    Model = Department
    template_name = 'laboratory/department_deleted_list.html'
    context_object_name = 'all_deleted_departments'
    queryset = Department.objects.exclude(deleted_at=None)
    paginate_by = FACILITY_PER_PAGE
