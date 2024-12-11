from rest_framework.permissions import BasePermission


class IsTaskOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allows only owners to view or edit the task
        return request.user in obj.owners.all()
