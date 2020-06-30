from rest_framework import serializers
from .models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'is_staff', 'telephone', 'username', 'is_active', 'email')