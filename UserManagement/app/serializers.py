from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    # Set the password field to write_only (hidden in get() method)
    password = serializers.CharField(write_only=True)
    # Set the id field to read_only (shown to used but can not be modified)
    id = serializers.IntegerField(read_only=True)
    last_login = serializers.DateTimeField(write_only=True)
    last_update = serializers.DateTimeField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"
