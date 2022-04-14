from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


class StaffRequiredMixin(AccessMixin):
    """    View mixin which requires that the authenticated user is a staff member
    (i.e. `is_staff` is True)."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class PhysicianRequiredMixin(AccessMixin):
    """    View mixin which requires that the authenticated user is a staff member
    (i.e. `is_staff` is True)."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_physician:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class SuperUserRequiredMixin(AccessMixin):
    """    View mixin which requires that the authenticated user is a staff member
    (i.e. `is_staff` is True)."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ErrorIfNotPhysicianOrStaff:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_physician or request.user.is_staff:
            raise PermissionDenied('You need to be staff member or Physician to visit this page!')

        return super().dispatch(request, *args, **kwargs)


class LoginAndNotDeletedRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.user.deleted_at:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)