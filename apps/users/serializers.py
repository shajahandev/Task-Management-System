
from rest_framework import serializers
from apps.users.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
            "phone",
            "department",
            "designation",
            "is_active",
        ]

        read_only_fields = [
            "id",
            "role",
        ]


class AdminCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "phone",
            "department",
            "designation",
        ]

        read_only_fields = [
            "id",
        ]

    def create(self, validated_data):

        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            role=User.Role.ADMIN,
            is_staff=True,
            **validated_data
        )

        return user


class StaffCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "phone",
            "department",
            "designation",
        ]

        read_only_fields = [
            "id",
        ]

    def create(self, validated_data):

        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            role=User.Role.STAFF,
            is_staff=False,
            is_superuser=False,
            **validated_data
        )

        return user