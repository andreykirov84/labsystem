from django.contrib.auth.mixins import LoginAndNotDeletedRequiredMixin
from django.views import generic as views
from django.urls import reverse_lazy
from labsystem.laboratory.forms.job_position_forms import CreateJobPositionForm
from utils.view_mixins import StaffRequiredMixin


class JobPositionCreation(LoginAndNotDeletedRequiredMixin, StaffRequiredMixin, views.CreateView):
    form_class = CreateJobPositionForm
    template_name = 'laboratory/job_position_create.html'
    success_url = reverse_lazy('index')
