from rest_framework import serializers
from tna.models import TnaProject
from users.serializers import UserSerializer


class PrincipalInvestigatorField(serializers.RelatedField):
    def to_representation(self, value):
        return f'{value.first_name} {value.last_name}'


class TnaProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = TnaProject
        # fields = "__all__"
        fields = ('id', 'associated_application', 'principal_investigator', 'associated_application_title', 'project_title',
                  'research_installation_1', 'research_installation_2', 'research_installation_3',
                  'context','objective', 'impact', 'state_art', 'scientific_question_hypothesis',
                  'approach', 'strategy', 'created', 'additional_participants')
        extra_kwargs = {
            # 'url': {'lookup_field': 'id'}
        }

    def to_representation(self, instance):
        self.fields['principal_investigator'] = UserSerializer(read_only=True)
        self.fields['additional_participants'] = UserSerializer(read_only=True, many=True)
        return super(TnaProjectSerializer, self).to_representation(instance)
