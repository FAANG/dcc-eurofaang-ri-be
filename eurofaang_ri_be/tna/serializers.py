from rest_framework import serializers
# from tna.models import WatchList, StreamPlatform, Review
from tna.models import TnaProject

from users.serializers import UserSerializer


class PrincipalInvestigatorField(serializers.RelatedField):
    def to_representation(self, value):
        return f'{value.first_name} {value.last_name}'

class TnaProjectSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)
    # additional_participants = UserSerializer(read_only=False, many=True)
    # additional_participants = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='first_name'
    # )

    # additional_participants = serializers.StringRelatedField(many=True)

    # principal_investigator = PrincipalInvestigatorField(read_only=True)



    class Meta:
        model = TnaProject
        fields = "__all__"



