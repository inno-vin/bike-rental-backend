from rest_framework.permissions import BasePermission


class IsBikeOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.bike.owner == request.user
