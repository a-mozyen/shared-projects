from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    wallet = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'
