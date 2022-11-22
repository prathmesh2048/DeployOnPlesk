from rest_framework.permissions import IsAuthenticated, BasePermission


# ADMIN PERMISSIONS
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active and request.user.is_authenticated and request.user.is_superuser)
