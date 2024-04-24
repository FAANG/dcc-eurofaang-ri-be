from rest_framework import serializers
# from tna.models import WatchList, StreamPlatform, Review
from tna.models import TnaProject
from users.models import User


# from users.serializers import UserSerializer


class PrincipalInvestigatorField(serializers.RelatedField):
    def to_representation(self, value):
        return f'{value.first_name} {value.last_name}'


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    username = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    organization_name = serializers.CharField(required=False, allow_blank=True)
    organization_address = serializers.CharField(required=False, allow_blank=True)
    organization_country = serializers.CharField(required=False, allow_blank=True)
    role = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'organization_name',
                  'organization_address', 'organization_country', 'role')


class TnaProjectSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)
    # additional_participants = UserSerializer(many=True)
    # additional_participants = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='first_name'
    # )

    # additional_participants = serializers.StringRelatedField(many=True)

    # principal_investigator = PrincipalInvestigatorField(read_only=True)

    # principal_investigator = UserSerializer()

    class Meta:
        model = TnaProject
        fields = "__all__"

        # depth = 1
        # exclude = ('password',)
