from django.contrib.auth.mixins import LoginRequiredMixin
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

    # def get_context_data(self, **kwargs):
    #     context = super(HomeView, self).get_context_data()
    #     is_logged_in = True
    #     user = self.request.user
    #     logged_user_is_physician = False
    #     logged_user_is_staff = False
    #     if user == 'AnonymousUser':
    #         is_logged_in = False
    #     context['user'] = user
    #     context['is_logged_in'] = is_logged_in
    #     return context


class StaffPatientView(LoginRequiredMixin, views.ListView):
    Model = Profile
    template_name = 'users/staff_view_patient_details.html'
    paginate_by = 10

    def get_queryset(self):
        # new_context = Profile.objects.all().filter(user__is_patient=True)
        new_context = Profile.undeleted_objects.all().filter(user__is_patient=True)

        return new_context