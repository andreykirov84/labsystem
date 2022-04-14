from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import generic as views
from django.urls import reverse_lazy, reverse

from labsystem.auth_app.models import LimsUser
from labsystem.laboratory.forms.patient_forms import CreatePatientUserForm, CreateEditProfilePatientForm, DeletePatientForm, \
    RestorePatientForm
from labsystem.laboratory.models import Profile, Result
from utils.generators import get_secure_random_string
from utils.validators import validate_only_letters_and_spaces
from utils.view_mixins import StaffRequiredMixin, PhysicianRequiredMixin, LoginAndNotDeletedRequiredMixin
from django.db.models import Q


class PatientUserCreateView(LoginAndNotDeletedRequiredMixin, StaffRequiredMixin, views.CreateView):
    form_class = CreatePatientUserForm
    template_name = 'users/patient/patient_user_create.html'
    success_url = reverse_lazy('create patient')
    pk = None

    def get_initial(self):
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
            'username': new_username,
        }

        return INITIAL_DATA

    def get_success_url(self):
        return reverse('create patient', kwargs={'pk': self.object.pk})


class PatientCreateView(LoginAndNotDeletedRequiredMixin, StaffRequiredMixin, views.CreateView):
    form_class = CreateEditProfilePatientForm
    template_name = 'users/patient/patient_create.html'
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


class EditPatientView(LoginAndNotDeletedRequiredMixin, StaffRequiredMixin, views.UpdateView):
    model = Profile
    form_class = CreateEditProfilePatientForm
    template_name = 'users/patient/patient_edit.html'
    success_url = reverse_lazy('all patients')


class PatientsListView(LoginAndNotDeletedRequiredMixin, StaffRequiredMixin, views.ListView):
    PATIENTS_PER_PAGE = 10
    Model = Profile
    template_name = 'users/patient/patients_nondeleted_list.html'
    context_object_name = 'all_patients'
    queryset = Profile.objects.filter(user__is_patient=True, deleted_at=None)
    paginate_by = PATIENTS_PER_PAGE
    ordering = ['-updated_on']

#
# class AllPhysicianPatientsListView(LoginAndNotDeletedRequiredMixin, PhysicianRequiredMixin, views.ListView):
#     PATIENTS_PER_PAGE = 2
#     Model = Profile
#     template_name = 'laboratory/all_patients_referred_by_specific_physician_list.html'
#     context_object_name = 'all_patients'
#
#     # queryset = Profile.objects.filter(user__is_patient=True, deleted_at=None)
#     paginate_by = PATIENTS_PER_PAGE
#     ordering = ['-created_on']
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data()
#         physician = Profile.objects.get(pk=self.kwargs['pk'])
#         results = Result.objects.filter(referring_physician=self.kwargs['pk']).distinct('patient_id').values()
#         patients = None
#         if results:
#             all_patients_pk = [x['patient_id'] for x in results]
#             patients = Profile.objects.filter(pk__in=all_patients_pk)
#         context['patients'] = patients
#         context['physician'] = physician
#         return context


class AllPhysicianPatientsListView(LoginAndNotDeletedRequiredMixin, PhysicianRequiredMixin, views.ListView):
    PATIENTS_PER_PAGE = 10
    Model = Profile
    template_name = 'laboratory/all_patients_referred_by_specific_physician_list.html'
    paginate_by = PATIENTS_PER_PAGE
    ordering = ['-updated_on']

    def get_queryset(self):
        results = Result.objects.filter(referring_physician=self.kwargs['pk']).distinct('patient_id').values()
        patients = None
        if results:
            all_patients_pk = [x['patient_id'] for x in results]
            for p in all_patients_pk:
                patient = Profile.objects.get(pk=p)
                if not patient.user.is_active:
                    all_patients_pk.remove(p)
            patients = Profile.objects.filter(pk__in=all_patients_pk)
        return patients

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        physician = Profile.objects.get(pk=self.kwargs['pk'])
        context['physician'] = physician
        return context


class DeletedPatientsListView(LoginAndNotDeletedRequiredMixin, StaffRequiredMixin, views.ListView):
    ITEMS_PER_PAGE = 10
    Model = Profile
    template_name = 'users/patient/patients_deleted_list.html'
    context_object_name = 'deleted_patients'
    queryset = Profile.objects.filter(user__is_patient=True).exclude(deleted_at=None)
    paginate_by = ITEMS_PER_PAGE
    ordering = ['-updated_on']


class PatientDetailsView(LoginAndNotDeletedRequiredMixin, views.DetailView):
    ITEMS_PER_PAGE = 10
    model = Profile
    template_name = 'users/patient/patient_details.html'
    context_object_name = 'profile'
    paginate_by = ITEMS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        deleted = False
        if self.object.deleted_at is not None:
            deleted = True

        patient_results = Result.objects.filter(patient=self.kwargs['pk'])
        patient = Profile.objects.get(pk=self.kwargs['pk'])
        user = Profile.objects.get(pk=self.request.user.pk)
        if user.is_staff:
            user_is_staff = True
        else:
            user_is_staff = False

        context['deleted'] = deleted
        context['user_is_staff'] = user_is_staff
        context['patient_results'] = patient_results
        context['patient'] = patient

        return context


@staff_member_required
def delete_patient_view(request, pk):
    patient = Profile.objects.get(pk=pk)
    patient_pid = patient.pid_type
    has_middlename = False
    if patient.middle_name:
        has_middlename = True
    if request.method == 'POST':
        form = DeletePatientForm(request.POST, instance=patient)
        form.is_valid()
        form_user_username = form.cleaned_data.get('user')
        user = LimsUser.objects.get(username=form_user_username)
        user.is_active = False
        user.deleted_at = timezone.now()
        user.save()
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
    return render(request, 'users/patient/patient_delete.html', context)


@staff_member_required
def restore_patient_view(request, pk):
    patient = Profile.objects.get(pk=pk)
    patient_pid = patient.pid_type
    has_middlename = False
    if patient.middle_name:
        has_middlename = True
    if request.method == 'POST':
        form = RestorePatientForm(request.POST, instance=patient)
        form.is_valid()
        form_user_username = form.cleaned_data.get('user')
        user = LimsUser.objects.get(username=form_user_username)
        user.is_active = True
        user.deleted_at = None
        user.save()
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

    return render(request, 'users/patient/patient_restore.html', context)


class SearchPatientsView(LoginAndNotDeletedRequiredMixin, views.ListView):
    ITEMS_PER_PAGE = 10
    Model = Profile
    template_name = 'users/patient/patients_search_list.html'
    context_object_name = 'all_patients'
    paginate_by = ITEMS_PER_PAGE

    def get_queryset(self):
        query = self.request.GET.get("search")
        if query == '':
            all_patients = []
        elif validate_only_letters_and_spaces(query):
            if self.request.user.is_staff:
                all_patients = Profile.objects.filter(
                    (Q(first_name__icontains=query) | Q(middle_name__icontains=query) | Q(last_name__icontains=query)) &
                    Q(deleted_at=None) &
                    Q(user__is_patient=True)
                )

            elif self.request.user.is_physician:
                results = Result.objects.filter(referring_physician=self.request.user.pk).values()
                patient_pks = None
                if results:
                    all_patients_pk = [x['patient_id'] for x in results]
                    patients = Profile.objects.filter(pk__in=all_patients_pk).values
                    patient_pks = [x['pk'] for x in patients]

                all_patients = Profile.objects.filter(
                    (Q(first_name__icontains=query) | Q(middle_name__icontains=query) | Q(last_name__icontains=query)) &
                    Q(pk__in=patient_pks) &
                    Q(deleted_at=None) &
                    Q(user__is_patient=True)
                )
            else:
                all_patients = Profile.objects.get(pk=self.request.user.pk)
        else:
            all_patients = []

        return all_patients
