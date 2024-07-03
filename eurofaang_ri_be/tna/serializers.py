from rest_framework import serializers
from tna.models import TnaProject
from users.serializers import UserSerializer
import random
import string
from rest_framework.response import Response


class PrincipalInvestigatorField(serializers.RelatedField):
    def to_representation(self, value):
        return f'{value.first_name} {value.last_name}'


class AssociatedProjectField(serializers.ModelSerializer):
    class Meta:
        model = TnaProject
        fields = ('id', 'project_title')


class TnaProjectSerializer(serializers.ModelSerializer):
    tna_owner = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = TnaProject
        fields = (
        'id', 'associated_application', 'principal_investigator', 'associated_application_title', 'project_title',
        'research_installation_1', 'research_installation_2', 'research_installation_3',
        'context', 'objective', 'impact', 'state_art', 'scientific_question_hypothesis',
        'approach', 'strategy', 'created', 'additional_participants', 'tna_owner', 'record_status')
        extra_kwargs = {
            # 'url': {'lookup_field': 'id'}
        }

    def to_representation(self, instance):
        self.fields['principal_investigator'] = UserSerializer(read_only=True)
        self.fields['additional_participants'] = UserSerializer(read_only=True, many=True)
        self.fields['associated_application_title'] = AssociatedProjectField(read_only=True)
        return super(TnaProjectSerializer, self).to_representation(instance)

    def to_internal_value(self, data):
        tna_data = generate_tna_drf_format(data)
        return super(TnaProjectSerializer, self).to_internal_value(tna_data)

    def validate(self, data):
        if data['record_status'] == 'submitted':
            for key, value in data.items():
                # "additional_participants": [] can be an empty list
                if key == 'additional_participants':
                    continue
                if key == 'associated_application_title' and data['associated_application'] == 'no':
                    continue
                if not value:
                    raise serializers.ValidationError("The fields in the form cannot be left blank if you are "
                                                      "SUBMITTING the data.")
        return data


def generate_tna_drf_format(form_data):

    participants_ids = []
    if 'participantFields' in form_data['participants']:
        participants_list = form_data['participants']['participantFields']

        if len(participants_list) > 0:
            for participant in participants_list:
                if "id" in participant and participant['id'] is not None:
                    participants_ids.append(participant['id'])
                elif "existingParticipants" in participant and participant['existingParticipants'] is not None:
                    participants_ids.append(participant['existingParticipants'])
                else:
                    participant_data = generate_participant_obj(participant)
                    user_serializer = UserSerializer(data=participant_data)
                    if user_serializer.is_valid():
                        user_serializer.save()
                        participants_ids.append(user_serializer.data['id'])
                    else:
                        return Response(user_serializer.errors)

    tna_data = generate_tna_obj(form_data, participants_ids)
    return tna_data


def generate_tna_obj(form_data, participants_ids):
    tna_obj = {'additional_participants': participants_ids,
               'principal_investigator': form_data['principalInvestigator']['principalInvestigatorId'],
               'associated_application': form_data['projectInformation']['applicationConnection'],
               'associated_application_title': form_data['projectInformation']['associatedProjectTitle'],
               'project_title': form_data['projectInformation']['projectTitle'],
               'research_installation_1': form_data['projectInformation']['preferredResearchInstallation'][
                   'preference1'],
               'research_installation_2': form_data['projectInformation']['preferredResearchInstallation'][
                   'preference2'],
               'research_installation_3': form_data['projectInformation']['preferredResearchInstallation'][
                   'preference3'],
               'context': form_data['projectInformation']['rationale']['context'],
               'objective': form_data['projectInformation']['rationale']['objective'],
               'impact': form_data['projectInformation']['rationale']['impact'],
               'state_art': form_data['projectInformation']['scientificQuality']['stateArt'],
               'approach': form_data['projectInformation']['scientificQuality']['approach'],
               'scientific_question_hypothesis': form_data['projectInformation']['scientificQuality'][
                   'questionHypothesis'],
               'strategy': form_data['projectInformation']['valorizationStrategy']['strategy'],
               'record_status': form_data['recordStatus'],
               }
    return tna_obj


def generate_username(participant):
    username = (participant['firstname'][0] + participant['lastname'] +
                "".join(random.choices(string.ascii_lowercase + string.digits, k=3)))
    return username


def generate_participant_obj(participant):
    participant_obj = {
        "username": generate_username(participant),
        "first_name": participant['firstname'],
        "last_name": participant['lastname'],
        "email": participant['email'],
        "phone_number": participant['phone'],
        "organization_name": participant['organisation']['organisationName'],
        "organization_address": participant['organisation']['organisationAddress'],
        "organization_country": participant['organisation']['organisationCountry'],
        "role": "AP"
    }
    return participant_obj
