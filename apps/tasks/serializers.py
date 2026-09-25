# from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.users.models import User

from .models import Task, TaskAttachment

# User = get_user_model()


class TaskAttachmentSerializer(serializers.ModelSerializer):

    uploaded_by = serializers.StringRelatedField(read_only=True)
    original_name = serializers.CharField(read_only=True)

    class Meta:
        model = TaskAttachment
        fields = [
            "id",
            "file",
            "original_name",
            "uploaded_by",
            "uploaded_at",
        ]

        read_only_fields = [
            "id",
            "original_name",
            "uploaded_by",
            "uploaded_at",
        ]

class TaskSerializer(serializers.ModelSerializer):

    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(
            role=User.Role.STAFF,
            is_active=True
        ),
        required=False,
        allow_null=True
    )
    created_by = serializers.StringRelatedField(read_only=True)
    attachments = TaskAttachmentSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "assigned_to",
            "created_by",
            "priority",
            "status",
            "due_date",
            "attachments",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_by",
            "status",
            "attachments",
            "created_at",
            "updated_at",
        ]

    def validate_assigned_to(self, user):
        if user.role != User.Role.STAFF:
            raise serializers.ValidationError(
                "Task can only be assigned to a Staff user."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "Cannot assign task to an inactive user."
            )

        return user


class TaskStatusSerializer(serializers.Serializer):

    status = serializers.ChoiceField(
        choices=Task.Status.choices
    )

    def validate_status(self, new_status):

        task = self.context["task"]

        current_status = task.status

        allowed_transitions = {
            Task.Status.TODO: [
                Task.Status.IN_PROGRESS,
                Task.Status.CANCELLED,
            ],

            Task.Status.IN_PROGRESS: [
                Task.Status.COMPLETED,
                Task.Status.CANCELLED,
            ],

            Task.Status.COMPLETED: [],

            Task.Status.CANCELLED: [],
        }

        if new_status not in allowed_transitions[current_status]:
            raise serializers.ValidationError(
                f"Cannot change status from "
                f"{current_status} to {new_status}."
            )

        return new_status


class TaskAttachmentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskAttachment
        fields = [
            "id",
            "file",
            "original_name",
            "uploaded_by",
            "uploaded_at",
        ]

        read_only_fields = [
            "id",
            "original_name",
            "uploaded_by",
            "uploaded_at",
        ]

    def create(self, validated_data):

        request = self.context["request"]

        file = validated_data["file"]

        validated_data["original_name"] = file.name
        validated_data["uploaded_by"] = request.user

        return super().create(validated_data)