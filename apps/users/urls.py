from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet


router = DefaultRouter()

router.register(
    "users",
    UserViewSet,
    basename="users"
)


urlpatterns = [

    path(
        "",
        include(router.urls)
    ),

    path(
        "users/admin/create/",
        UserViewSet.as_view({
            "post": "create_admin"
        }),
        name="create-admin"
    ),

    path(
        "users/staff/create/",
        UserViewSet.as_view({
            "post": "create_staff"
        }),
        name="create-staff"
    ),
]