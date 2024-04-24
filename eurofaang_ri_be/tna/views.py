from django.shortcuts import render
from .models import TnaProject
from django.http import JsonResponse
from rest_framework.views import APIView

from .serializers import TnaProjectSerializer
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class TnaListAV(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tna_projects = TnaProject.objects.all()
        serializer = TnaProjectSerializer(tna_projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(request.data)
        form_data = request.data

        # map front-end request to DRF model

        pi_data = {
            "username": "milou2221",
            "first_name": form_data['principalInvestigator']['firstname'],
            "last_name": form_data['principalInvestigator']['lastname'],
            "email": form_data['principalInvestigator']['email'],
            "phone_number": form_data['principalInvestigator']['phone'],
            "organization_name": form_data['principalInvestigator']['organisation']['organisationName'],
            "organization_address": form_data['principalInvestigator']['organisation']['organisationAddress'],
            "organization_country": form_data['principalInvestigator']['organisation']['organisationCountry'],
            "role": "PI"
        }

        serializerUser = UserSerializer(data=pi_data)
        if serializerUser.is_valid():
            serializerUser.save()
            print(serializerUser.data)
        else:
            return Response(serializerUser.errors)

        tna_data = {'additional_participants': [1, 2, 3, 4],  # we need an id here
                    'associated_application_title': 3,  # we need an id here
                    'principal_investigator': serializerUser.data['id'],

                    'associated_application': form_data['projectInformation']['applicationConnection'],
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

        serializer = TnaProjectSerializer(data=tna_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


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
