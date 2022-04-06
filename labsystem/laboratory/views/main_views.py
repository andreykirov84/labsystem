from django.contrib.auth.mixins import LoginAndNotDeletedRequiredMixin
from django.views import generic as views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from labsystem.laboratory.models import Profile


class UserLoginView(auth_views.LoginView):
    template_name = 'users/login_page.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class UserLogoutView(auth_views.LogoutView):
    template_name = 'users/logout_page.html'
    success_url = reverse_lazy('index')


class HomeView(views.TemplateView):
    template_name = 'main/home_page.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data()
        user = self.request.user
        context['user'] = user
        return context


class StaffPatientView(LoginAndNotDeletedRequiredMixin, views.ListView):
    Model = Profile
    template_name = 'users/staff_view_patient_details.html'
    paginate_by = 10

    def get_queryset(self):
        new_context = Profile.undeleted_objects.all().filter(user__is_patient=True)

        return new_context
