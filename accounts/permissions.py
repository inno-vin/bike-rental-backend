from rest_framework.permissions import BasePermission


class IsOwnerUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.profile.role in ['owner', 'both']
