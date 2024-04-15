from rest_framework import serializers
from .models import User, Rationale


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
        read_only_fields = ('username', )


class RationaleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    context = serializers.CharField(required=True, allow_blank=False)
    objectives = serializers.CharField(required=True, allow_blank=False)
    impact = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = Rationale
        fields = ('id', 'context', 'objectives', 'impact')
