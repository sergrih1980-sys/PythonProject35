from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser:
            return True
        if not user.is_authenticated:
            return False
        return user.groups.filter(name='moderator').exists()