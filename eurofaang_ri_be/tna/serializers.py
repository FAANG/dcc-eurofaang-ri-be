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

    # principal_investigator = UserSerializer(read_only=True)
    # principal_investigator = serializers.CharField(source='User.id', read_only=True)

    class Meta:
        model = TnaProject
        # fields = "__all__"
        fields = ('associated_application', 'principal_investigator', 'associated_application_title', 'project_title',
                  'research_installation_1', 'research_installation_2', 'research_installation_3',
                  'context','objective', 'impact', 'state_art', 'scientific_question_hypothesis',
                  'approach', 'strategy', 'created', 'additional_participants', 'id'
                  )

    def to_representation(self, instance):
        self.fields['principal_investigator'] = UserSerializer(read_only=True)
        return super(TnaProjectSerializer, self).to_representation(instance)

        # depth = 1
        # exclude = ('password',)

    # def create(self, validated_data):
    #     tracks_data = validated_data.pop('principal_investigator')
    #     album = Album.objects.create(**validated_data)
    #     for track_data in tracks_data:
    #         Track.objects.create(album=album, **track_data)
    #     return album

    # def create(self, validated_data):
    #     principal_investigator = validated_data.pop('principal_investigator')
    #     print(principal_investigator)
    #
    #     # get/(create if not exists) brand
    #     # principal_investigator, _ = User.objects.filter(id=self.kwargs["pk"]).first()
    #     #
    #     # # print(brand_data) # OrderedDict([('name', 'adgg')])
    #     # product = Product.objects.create(brand=principal_investigator, **validated_data)
    #     #
    #     # return product