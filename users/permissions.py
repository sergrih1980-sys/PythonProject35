from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """Разрешает доступ только пользователям из группы 'moderator'."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='moderator').exists()

    def has_object_permission(self, request, view, obj):
        # Для действий с объектом (retrieve, update, partial_update, destroy)
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='moderator').exists()