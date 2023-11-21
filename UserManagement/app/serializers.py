from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    # Define the password field with write_only set to True
    password = serializers.CharField(write_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = "__all__"
