from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import generic as views
from django.urls import reverse_lazy, reverse

from labsystem.auth_app.models import LimsUser
from labsystem.laboratory.forms.patient_forms import CreatePatientUserForm, CreateProfilePatientForm, DeletePatientForm, \
    RestorePatientForm
from labsystem.laboratory.models import Profile
from utils.generators import get_secure_random_string
from utils.view_mixins import StaffRequiredMixin


class PatientUserCreateView(views.CreateView):
    form_class = CreatePatientUserForm
    template_name = 'users/patient_user_create.html'
    success_url = reverse_lazy('create staff')
    pk = None

    def get_initial(self):
        # new_password = None
        while True:
            new_username = get_secure_random_string(
                length=LimsUser.USERNAME_MIN_LENGTH,
            )
            existed_user = LimsUser.objects.filter(username=new_username).first()
            if existed_user:
                continue
            else:
                break

        password1 = get_secure_random_string(length=CreatePatientUserForm.PASSWORD_LENGTH)
        password2 = password1

        INITIAL_DATA = {
            'password1': password1,
            'password2': password2,
            # 'password': new_password,
            'username': new_username,
        }

        return INITIAL_DATA

    def get_success_url(self):
        return reverse('create staff', kwargs={'pk': self.object.pk})


class PatientCreateView(LoginRequiredMixin, StaffRequiredMixin, views.CreateView):
    form_class = CreateProfilePatientForm
    template_name = 'users/patient_create.html'
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
        # context['user_pk'] = self.get_initial['user']
        context['user_pk'] = self.kwargs['pk']
        return context

    def get_success_url(self):
        return reverse_lazy('all patients')


class PatientsListView(LoginRequiredMixin, StaffRequiredMixin, views.ListView):
    PATIENTS_PER_PAGE = 10
    Model = Profile
    template_name = 'users/patients_nondeleted_list.html'
    context_object_name = 'all_patients'
    queryset = Profile.objects.filter(user__is_patient=True, deleted_at=None)
    paginate_by = PATIENTS_PER_PAGE
    ordering = ['-updated_on']


class DeletedPatientsListView(LoginRequiredMixin, StaffRequiredMixin, views.ListView):
    ITEMS_PER_PAGE = 10
    Model = Profile
    template_name = 'users/patients_deleted_list.html'
    context_object_name = 'deleted_patients'
    queryset = Profile.objects.filter(user__is_patient=True).exclude(deleted_at=None)
    paginate_by = ITEMS_PER_PAGE
    ordering = ['-updated_on']


class EditPatientView(LoginRequiredMixin, StaffRequiredMixin, views.UpdateView):
    model = Profile
    template_name = 'users/patient_edit.html'
    fields = (
        'pid',
        'sex',
        'pid_type',
        'first_name',
        'middle_name',
        'last_name',
        'date_of_birth',
        'comments',
    )
    success_url = reverse_lazy('all patients')


class PatientDetailsView(views.DetailView):
    model = Profile
    template_name = 'users/patient_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        deleted = False
        if self.object.deleted_at is not None:
            deleted = True
        context['deleted'] = deleted
        return context


def delete_patient_view(request, pk):
    patient = Profile.objects.get(pk=pk)
    patient_pid = patient.pid_type
    has_middlename = False
    if patient.middle_name:
        has_middlename = True
    if request.method == 'POST':
        form = DeletePatientForm(request.POST, instance=patient)
        # if form.is_valid():
        form.save()
        return redirect('all patients')
    else:
        form = DeletePatientForm(instance=patient)

    context = {
        'form': form,
        'patient': patient,
        'patient_pid': patient_pid,
        'has_middlename': has_middlename
    }
    return render(request, 'users/patient_delete.html', context)


def restore_patient_view(request, pk):
    patient = Profile.objects.get(pk=pk)
    patient_pid = patient.pid_type
    has_middlename = False
    if patient.middle_name:
        has_middlename = True
    if request.method == 'POST':
        form = RestorePatientForm(request.POST, instance=patient)
        form.save()
        return redirect('all patients')
    else:
        form = RestorePatientForm(instance=patient)

    context = {
        'form': form,
        'patient': patient,
        'patient_pid': patient_pid,
        'has_middlename': has_middlename
    }

    return render(request, 'users/patient_restore.html', context)
