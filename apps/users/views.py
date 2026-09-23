from django.contrib.auth import get_user_model

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    UserSerializer,
    AdminCreateSerializer,
    StaffCreateSerializer,
)
from .permissions import IsAdmin
User = get_user_model()
class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    permission_classes = [
        IsAuthenticated,
        IsAdmin,
    ]

    def get_serializer_class(self):

        if self.action == "create_admin":
            return AdminCreateSerializer

        if self.action == "create_staff":
            return StaffCreateSerializer

        return UserSerializer

    def create_admin(self, request):

        serializer = AdminCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        return Response(
            {
                "message": "Admin created successfully.",
                "data": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED
        )

    def create_staff(self, request):

        serializer = StaffCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        return Response(
            {
                "message": "Staff created successfully.",
                "data": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED
        )