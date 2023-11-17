from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password')

    
    # The serializers.Serializer class is derived from BaseSerializer and 
    # it does not implement the create() method either. 
    # So you have to create a create method to save your model.
    # def create(self, validated_data):
    #     return User.objects.create(**validated_data)
    