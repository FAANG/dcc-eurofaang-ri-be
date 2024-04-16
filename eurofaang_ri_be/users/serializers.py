from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    organization_name = serializers.CharField(required=False, allow_blank=True)
    organization_address = serializers.CharField(required=False, allow_blank=True)
    organization_country = serializers.CharField(source='get_organization_country_display',
                                                 required=False, allow_blank=True)
    role = serializers.CharField(source='get_role_display', required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'organization_name',
                  'organization_address', 'organization_country', 'role')
        read_only_fields = ('username', )
