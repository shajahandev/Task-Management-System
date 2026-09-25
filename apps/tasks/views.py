from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task, TaskAttachment
from .serializers import (
    TaskSerializer,
    TaskStatusSerializer,
    TaskAttachmentSerializer,
    TaskAttachmentCreateSerializer,
)
from .permissions import IsAdmin
from rest_framework import serializers
class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.select_related(
        "assigned_to",
        "created_by"
    ).prefetch_related(
        "attachments"
    )

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        queryset = self.queryset
        # Admin can see all tasks
        if user.is_superuser or user.role == user.Role.ADMIN:
            return queryset

        # Staff can see only assigned tasks
        return queryset.filter(
            assigned_to=user
        )

    def get_permissions(self):

        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
            "assign",
        ]:
            return [
                IsAuthenticated(),
                IsAdmin(),
            ]

        return [
            IsAuthenticated(),
        ]

    def perform_create(self, serializer):

        serializer.save(
            created_by=self.request.user
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="status"
    )
    def update_status(self, request, pk=None):

        task = self.get_object()

        # Only assigned staff or admin can update status
        if not (
            request.user.is_superuser
            or request.user.role == request.user.Role.ADMIN
            or task.assigned_to == request.user
        ):
            return Response(
                {
                    "detail": "You do not have permission to update this task."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TaskStatusSerializer(
            data=request.data,
            context={"task": task}
        )

        serializer.is_valid(raise_exception=True)

        task.status = serializer.validated_data["status"]
        task.save(
            update_fields=[
                "status",
                "updated_at"
            ]
        )

        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_200_OK
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="assign"
    )
    def assign(self, request, pk=None):

        task = self.get_object()

        staff_id = request.data.get("assigned_to")

        if not staff_id:
            return Response(
                {
                    "detail": "assigned_to is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        from django.contrib.auth import get_user_model

        User = get_user_model()

        try:
            staff = User.objects.get(
                id=staff_id,
                role=User.Role.STAFF,
                is_active=True
            )
        except User.DoesNotExist:
            return Response(
                {
                    "detail": "Active Staff user not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        task.assigned_to = staff
        task.save(
            update_fields=[
                "assigned_to",
                "updated_at"
            ]
        )

        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_200_OK
        )

class TaskAttachmentViewSet(viewsets.ModelViewSet):

    queryset = TaskAttachment.objects.select_related(
        "task",
        "uploaded_by"
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        user = self.request.user

        if (
            user.is_superuser
            or user.role == user.Role.ADMIN
        ):
            return self.queryset

        return self.queryset.filter(
            task__assigned_to=user
        )

    def get_serializer_class(self):

        if self.action == "create":
            return TaskAttachmentCreateSerializer

        return TaskAttachmentSerializer

    def perform_create(self, serializer):

        task_id = self.request.data.get("task")

        if not task_id:
            raise serializers.ValidationError(
                {
                    "task": "Task is required."
                }
            )

        try:
            task = Task.objects.get(
                id=task_id
            )
        except Task.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "task": "Task not found."
                }
            )

        user = self.request.user

        if not (
            user.is_superuser
            or user.role == user.Role.ADMIN
            or task.assigned_to == user
        ):
            raise PermissionError(
                "You cannot upload an attachment to this task."
            )

        serializer.save(
            task=task,
            uploaded_by=user,
            original_name=serializer.validated_data[
                "file"
            ].name
        )