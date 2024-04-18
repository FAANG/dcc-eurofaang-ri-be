from rest_framework import serializers
from .models import User, TnaProject


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


class TnaProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    users = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    another_application = serializers.CharField(required=True, allow_blank=False)
    another_application_link = serializers.CharField(required=False, allow_blank=True)
    title = serializers.CharField(required=True, allow_blank=False)
    research_installation_1 = serializers.CharField(required=True, allow_blank=False)
    research_installation_2 = serializers.CharField(required=True, allow_blank=False)
    research_installation_3 = serializers.CharField(required=True, allow_blank=False)

    context = serializers.CharField(required=True, allow_blank=False)
    objectives = serializers.CharField(required=True, allow_blank=False)
    impact = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = TnaProject
        fields = ('id', 'users', 'another_application', 'another_application_link', 'title', 'research_installation_1',
                  'research_installation_2', 'research_installation_3', 'context', 'objectives', 'impact')
        read_only_fields = ('users', )
