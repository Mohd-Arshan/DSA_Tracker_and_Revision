from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView


class CreateTemplateView(CreateAPIView):
    serializer_class = CreateTemplateSerializer
    permission_classes = [IsAuthenticated]
    
    
    
class AddTemplateView(CreateAPIView):
    serializer_class = AddTemplateSerializer
    permission_classes = [IsAuthenticated]
    
    
    
class GetMyTemplatesView(ListAPIView):
    
    """
     View to retrieve templates associated with the authenticated user.
     
     working 
       - check user is authenticated
       - get queryset of UserTemplate objects for the user
       - serialize the queryset and return the response
    
    serializer_class = AddTemplateSerializer  # Reuse the AddTemplateSerializer for listing templates
    serilaizer covterd Python object to json response
    """
    serializer_class = AddTemplateSerializer 
    permission_classes = [IsAuthenticated]
    
    # Override get_queryset to return templates associated with the authenticated user
    def get_queryset(self):
        user = self.request.user
        return UserTemplate.objects.filter(user=user)
    
    
class RemoveTemplateView(APIView):
    permission_classes = [IsAuthenticated]
    method = 'delete'
    
    def delete(self, request, template_id):
        user = request.user
        try:
            template = Template.objects.get(id=template_id)
            
            # If the user is the creator of the template, delete the template entirely
            if(template.createdBy == user):
                template.delete()
                return Response({'detail': 'Template deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            
            # If the user is not the creator, just remove the association
            user_template = UserTemplate.objects.get(user=user, template=template)
            user_template.delete()
            
            return Response({'detail': 'Template deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)   
        except UserTemplate.DoesNotExist:
            return Response({'detail': 'Template not found for user.'}, status=status.HTTP_404_NOT_FOUND)