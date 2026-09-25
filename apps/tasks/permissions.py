from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):

        user = request.user

        return (
            user.is_authenticated
            and (
                user.is_superuser
                or user.role == user.Role.ADMIN
            )
        )


class IsTaskStaff(BasePermission):

    def has_permission(self, request, view):

        user = request.user

        return (
            user.is_authenticated
            and user.role == user.Role.STAFF
        )


class IsTaskAssignee(BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj.assigned_to == request.user