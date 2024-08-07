from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.tna_owner == request.user or request.user in obj.additional_participants.all()


class SubmittedReadOnly(permissions.BasePermission):
    """
    Custom permission to prevent submitted record to be edited.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.record_status != "submitted"
