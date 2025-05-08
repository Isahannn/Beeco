from rest_framework import serializers
from .models.user import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'nickname', 'date_of_birth', 'location', 'avatar', 'date_joined']
