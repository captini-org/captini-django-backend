from captini.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = [
            "id",
            "url",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "nationality",
            "location",
            "age",
        ]
