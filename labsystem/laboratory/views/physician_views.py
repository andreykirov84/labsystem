from django.contrib.auth.mixins import LoginAndNotDeletedRequiredMixin
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import generic as views
from django.urls import reverse_lazy, reverse
from labsystem.auth_app.models import LimsUser
from labsystem.laboratory.forms.physician_forms import CreatePhysicianUserForm, CreateProfilePhysicianForm, \
    DeletePhysicianForm, RestorePhysicianForm, EditProfilePhysicianForm
from labsystem.laboratory.models import Profile
from utils.view_mixins import StaffRequiredMixin, SuperUserRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required


class PhysicianUserCreateView(LoginAndNotDeletedRequiredMixin, SuperUserRequiredMixin, views.CreateView):
    form_class = CreatePhysicianUserForm
    template_name = 'users/physician/physician_user_create.html'
    success_url = reverse_lazy('create physician')
    pk = None

    def get_success_url(self):
        return reverse('create physician', kwargs={'pk': self.object.pk})


class PhysicianCreateView(LoginAndNotDeletedRequiredMixin, SuperUserRequiredMixin, views.CreateView):
    form_class = CreateProfilePhysicianForm
    template_name = 'users/physician/physician_create.html'
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


class PhysicianListView(LoginAndNotDeletedRequiredMixin, StaffRequiredMixin, views.ListView):
    ITEMS_PER_PAGE = 10
    Model = Profile
    template_name = 'users/physician/physician_nondeleted_list.html'
    context_object_name = 'all_physicians'
    queryset = Profile.objects.filter(user__is_physician=True, deleted_at=None)
    paginate_by = ITEMS_PER_PAGE
    ordering = ['-updated_on']


class DeletedPhysicianListView(LoginAndNotDeletedRequiredMixin, SuperUserRequiredMixin, views.ListView):
    ITEMS_PER_PAGE = 10
    Model = Profile
    template_name = 'users/physician/physician_deleted_list.html'
    context_object_name = 'all_physicians'
    queryset = Profile.objects.filter(user__is_physician=True).exclude(deleted_at=None)
    paginate_by = ITEMS_PER_PAGE
    ordering = ['-updated_on']


class EditPhysicianView(LoginAndNotDeletedRequiredMixin, StaffRequiredMixin, views.UpdateView):
    model = Profile
    template_name = 'users/physician/physician_edit.html'
    form_class = EditProfilePhysicianForm
    success_url = reverse_lazy('all physicians')


class PhysicianDetailsView(LoginAndNotDeletedRequiredMixin, StaffRequiredMixin, views.DetailView):
    model = Profile
    template_name = 'users/physician/physician_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        deleted = False
        if self.object.deleted_at is not None:
            deleted = True
        context['deleted'] = deleted
        return context


@staff_member_required
def delete_physician_view(request, pk):
    physician = Profile.objects.get(pk=pk)
    physician_pid = physician.pid_type
    physician_health_facility = physician.health_facility
    has_middlename = False
    if physician.middle_name:
        has_middlename = True
    if request.method == 'POST':
        form = DeletePhysicianForm(request.POST, instance=physician)
        form.is_valid()
        form_user_username = form.cleaned_data.get('user')
        user = LimsUser.objects.get(username=form_user_username)
        user.is_active = False
        user.deleted_at = timezone.now()
        user.save()
        form.save()
        return redirect('all deleted physicians')
    else:
        form = DeletePhysicianForm(instance=physician)

    context = {
        'form': form,
        'physician': physician,
        'physician_pid': physician_pid,
        'physician_health_facility': physician_health_facility,
        'has_middlename': has_middlename,
    }
    return render(request, 'users/physician/physician_delete.html', context)


@staff_member_required
def restore_physician_view(request, pk):
    physician = Profile.objects.get(pk=pk)
    physician_pid = physician.pid_type
    physician_health_facility = physician.health_facility
    has_middlename = False
    if physician.middle_name:
        has_middlename = True
    if request.method == 'POST':
        form = RestorePhysicianForm(request.POST, instance=physician)
        form.is_valid()
        form_user_username = form.cleaned_data.get('user')
        user = LimsUser.objects.get(username=form_user_username)
        user.is_active = True
        user.deleted_at = None
        user.save()
        form.save()
        return redirect('all physicians')
    else:
        form = RestorePhysicianForm(instance=physician)

    context = {
        'form': form,
        'physician': physician,
        'physician_pid': physician_pid,
        'physician_health_facility': physician_health_facility,
        'has_middlename': has_middlename,
    }

    return render(request, 'users/physician/physician_restore.html', context)


