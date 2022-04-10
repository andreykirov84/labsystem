from django.contrib.auth import views as auth_views


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'users/password_change.html'