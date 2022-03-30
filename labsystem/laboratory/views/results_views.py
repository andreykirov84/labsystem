from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic as views
from django.urls import reverse_lazy
from labsystem.auth_app.models import LimsUser
from labsystem.laboratory.forms.patient_forms import CreateProfilePatientForm
from utils.view_mixins import StaffRequiredMixin


class ResultCreateView(LoginRequiredMixin, StaffRequiredMixin, views.CreateView):
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