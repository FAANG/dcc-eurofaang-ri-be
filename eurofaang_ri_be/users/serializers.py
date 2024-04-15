from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True, allow_blank=False)
    first_name = serializers.CharField(required=True, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_blank=False)
    email = serializers.CharField(required=True, allow_blank=False)
    phone_number = serializers.CharField(required=True, allow_blank=False)
    organization_name = serializers.CharField(required=True, allow_blank=False)
    organization_address = serializers.CharField(required=True, allow_blank=False)
    role = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'organization_name',
                  'organization_address', 'role')
        read_only_fields = ('username', )
