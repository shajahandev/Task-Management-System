from django.contrib import admin

from .models import Task, TaskAttachment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "assigned_to",
        "created_by",
        "priority",
        "status",
        "due_date",
        "created_at",
    )

    list_filter = (
        "priority",
        "status",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "assigned_to__username",
        "created_by__username",
    )

    autocomplete_fields = (
        "assigned_to",
        "created_by",
    )

@admin.register(TaskAttachment)
class TaskAttachmentAdmin(admin.ModelAdmin):
    list_display = (
        "task",
        "file",
        "uploaded_by",
        "uploaded_at",
    )

    list_filter = (
        "uploaded_at",
    )

    search_fields = (
        "task__title",
        "uploaded_by__username",
    )

    readonly_fields = (
        "uploaded_at",
    )