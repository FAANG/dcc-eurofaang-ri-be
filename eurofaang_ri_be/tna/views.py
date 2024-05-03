from .models import TnaProject
from rest_framework.views import APIView
from .serializers import TnaProjectSerializer
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import random
import string
import requests
from rest_framework import viewsets


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
               }
    return tna_obj


def generate_tna_drf_format(form_data):
    participants_ids = []
    if 'participantFields' in form_data['participants']:
        participants_list = form_data['participants']['participantFields']

        if len(participants_list) > 0:
            for participant in participants_list:
                if participant['id'] is not None:
                    participants_ids.append(participant['id'])
                else:
                    participant_data = generate_participant_obj(participant)

                    # url = '/users/'
                    # data = {}  # post data
                    # api_call = requests.post(url, headers={}, data=participant_data)
                    # print(api_call.json())


                    user_serializer = UserSerializer(data=participant_data)
                    if user_serializer.is_valid():
                        user_serializer.save()
                        print(user_serializer.data)
                        participants_ids.append(user_serializer.data['id'])
                    else:
                        print(user_serializer.errors)
                        return Response(user_serializer.errors)

    tna_data = generate_tna_obj(form_data, participants_ids)
    return tna_data


class TnaProjectViewSet(viewsets.ModelViewSet):
    queryset = TnaProject.objects.all()
    serializer_class = TnaProjectSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        form_data = request.data

        # map front-end request to DRF model
        tna_data = generate_tna_drf_format(form_data)

        serializer = self.get_serializer(data=tna_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        # map front-end request to DRF model
        tna_data = generate_tna_drf_format(request.data)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=tna_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    # throttle_classes = [AnonRateThrottle]




