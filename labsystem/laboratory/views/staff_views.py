from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import generic as views
from django.urls import reverse_lazy, reverse
from labsystem.auth_app.models import LimsUser
from labsystem.laboratory.forms.staff_forms import CreateStafftUserForm, CreateProfileStaffForm, DeleteStaffForm, \
    RestoreStaffForm
from labsystem.laboratory.models import Profile
from utils.decorators import superuser_required
from utils.view_mixins import StaffRequiredMixin, SuperUserRequiredMixin


class StaffUserCreateView(LoginRequiredMixin, SuperUserRequiredMixin, views.CreateView):
    form_class = CreateStafftUserForm
    template_name = 'users/staff/staff_user_create.html'
    success_url = reverse_lazy('create staff')
    pk = None

    def get_success_url(self):
        return reverse('create staff', kwargs={'pk': self.object.pk})


class StaffCreateView(LoginRequiredMixin, SuperUserRequiredMixin, views.CreateView):
    form_class = CreateProfileStaffForm
    template_name = 'users/staff/staff_create.html'
    success_url = reverse_lazy('index')

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = LimsUser.objects.get(pk=self.kwargs['pk'])
        print('user')
        print(initial['user'])
        print(initial['user'].username)
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user_pk'] = self.kwargs['pk']
        return context

    def get_success_url(self):
        return reverse_lazy('index')


class StaffListView(LoginRequiredMixin, SuperUserRequiredMixin, views.ListView):
    ITEMS_PER_PAGE = 10
    Model = Profile
    template_name = 'users/staff/staff_nondeleted_list.html'
    context_object_name = 'all_staff'
    queryset = Profile.objects.filter(user__is_staff=True, deleted_at=None)
    paginate_by = ITEMS_PER_PAGE
    ordering = ['-updated_on']


class DeletedStaffListView(LoginRequiredMixin, SuperUserRequiredMixin, views.ListView):
    ITEMS_PER_PAGE = 10
    Model = Profile
    template_name = 'users/staff/staff_deleted_list.html'
    context_object_name = 'all_staff'
    queryset = Profile.objects.filter(user__is_staff=True).exclude(deleted_at=None)
    paginate_by = ITEMS_PER_PAGE
    ordering = ['-updated_on']


class EditStaffView(LoginRequiredMixin, SuperUserRequiredMixin, views.UpdateView):
    model = Profile
    template_name = 'users/staff/staff_edit.html'
    fields = (
        'pid',
        'pid_type',
        'sex',
        'first_name',
        'middle_name',
        'last_name',
        'date_of_birth',
        'telephone_number',
        'email',
        'address',
        'city',
        'specialty',
        'position',
        'department',
        'salary',
        'comments',
    )
    success_url = reverse_lazy('all staffs')


class StaffDetailsView(LoginRequiredMixin, SuperUserRequiredMixin, views.DetailView):
    model = Profile
    template_name = 'users/staff/staff_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        deleted = False
        if self.object.deleted_at is not None:
            deleted = True
        context['deleted'] = deleted
        return context


@superuser_required
def delete_staff_view(request, pk):
    staff = Profile.objects.get(pk=pk)
    staff_pid = staff.pid_type
    staff_department = staff.department
    has_middlename = False
    if staff.middle_name:
        has_middlename = True
    if request.method == 'POST':
        form = DeleteStaffForm(request.POST, instance=staff)
        form.save()
        return redirect('all patients')
    else:
        form = DeleteStaffForm(instance=staff)

    context = {
        'form': form,
        'staff': staff,
        'staff_pid': staff_pid,
        'staff_department': staff_department,
        'has_middlename': has_middlename,
    }
    return render(request, 'users/staff/staff_delete.html', context)


@superuser_required
def restore_staff_view(request, pk):
    staff = Profile.objects.get(pk=pk)
    staff_pid = staff.pid_type
    staff_department = staff.department
    has_middlename = False
    if staff.middle_name:
        has_middlename = True
    if request.method == 'POST':
        form = RestoreStaffForm(request.POST, instance=staff)
        form.save()
        return redirect('all staffs')
    else:
        form = RestoreStaffForm(instance=staff)

    context = {
        'form': form,
        'staff': staff,
        'staff_pid': staff_pid,
        'staff_department': staff_department,
        'has_middlename': has_middlename,
    }

    return render(request, 'users/staff/staff_restore.html', context)


