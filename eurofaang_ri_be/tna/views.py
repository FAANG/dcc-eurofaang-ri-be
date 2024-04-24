from django.shortcuts import render
from .models import TnaProject
from django.http import JsonResponse
from rest_framework.views import APIView

from .serializers import TnaProjectSerializer
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import random
import string


class TnaListAV(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tna_projects = TnaProject.objects.all()
        serializer = TnaProjectSerializer(tna_projects, many=True)
        return Response(serializer.data)

    def generate_username(self, participant):
        username = (participant['firstname'][0] + participant['lastname']
                    .join(random.choices(string.ascii_lowercase +
                                         string.digits, k=3)))
        return username

    def post(self, request):
        print(request.data)
        form_data = request.data

        # map front-end request to DRF model

        participants_list = form_data['participants']['participantFields']

        participants_ids = []

        for participant in participants_list:
            participant_data = {
                "username": self.generate_username(participant),
                "first_name": participant['firstname'],
                "last_name": participant['lastname'],
                "email": participant['email'],
                "phone_number": participant['phone'],
                "organization_name": participant['organisation']['organisationName'],
                "organization_address": participant['organisation']['organisationAddress'],
                "organization_country": participant['organisation']['organisationCountry'],
                "role": "AP"
            }
            user_serializer = UserSerializer(data=participant_data)
            if user_serializer.is_valid():
                user_serializer.save()
                print(user_serializer.data)
                participants_ids.append(user_serializer.data['id'])
            else:
                return Response(user_serializer.errors)

        tna_data = {'additional_participants': participants_ids,
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

        tna_serializer = TnaProjectSerializer(data=tna_data)
        if tna_serializer.is_valid():
            tna_serializer.save()
            return Response(tna_serializer.data)
        else:
            return Response(tna_serializer.errors)


class TnaDetailAV(APIView):

    def get(self, request, pk):
        try:
            movie = TnaProject.objects.get(pk=pk)
        except TnaProject.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TnaProjectSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = TnaProject.objects.get(pk=pk)
        serializer = TnaProjectSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = TnaProject.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
