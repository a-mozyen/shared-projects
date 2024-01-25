from rest_framework import serializers
from .models import Blogs

class BlogSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.StringRelatedField()

    class Meta:
        model = Blogs
        fields = '__all__'
