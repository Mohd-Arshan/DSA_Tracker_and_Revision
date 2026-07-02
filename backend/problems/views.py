from django.shortcuts import render
from .models import Problem, Pattern, TemplateProblems
from template.models import Template
from .serializers import AddProblemIntoTemplateSerializer, GetAllProblemsInTemplateSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,RetrieveAPIView, ListAPIView
from .validators import ProblemSerializer
# Create your views here.


#ADD
class AddProblemIntoTemplateView(CreateAPIView):
    serializer_class = AddProblemIntoTemplateSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        
        if not Template.objects.filter(id=request.data.get('template')).exists():
            return Response({"error": "Template does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        template_user = Template.objects.get(id=request.data.get('template')).createdBy
        
        if template_user != request.user:
            return Response({"error": "You do not have permission to add problems to this template."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        template_problem = serializer.save()
        return Response({
            "message": "Problem added to template successfully",
            "template_problem_id": template_problem.id,
            "problem_id": template_problem.problem.leetcode_number    
        }, status=status.HTTP_201_CREATED)
 

       
#READ       
class ListProblemsInTemplateView(RetrieveAPIView):
    serializer_class = GetAllProblemsInTemplateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Template.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        template = self.get_object()
        if not Template.objects.filter(id=kwargs['pk']).exists():
            return Response({"error": "Template does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(template)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

#DELETE    
class RemoveProblemFromTemplateView(APIView):
   permission_classes = [IsAuthenticated]
   method  = 'delete'
   
   def delete(self,request,template_id,leetcode_id):
       user = request.user
       
       if not Template.objects.filter(id = template_id).exists():
           return Response({"error":"Template does not exits."},status=status.HTTP_400_BAD_REQUEST)
       
       template_user = Template.objects.get(id = template_id).createdBy
       
       if template_user != user:
           return Response({"error":"You dont have permission."},status=status.HTTP_403_FORBIDDEN)
       
       if not Problem.objects.filter(leetcode_number = leetcode_id).exists():
           return Response({"error":"Problem does not exits."},status=status.HTTP_400_BAD_REQUEST)
       
       problem = Problem.objects.get(leetcode_number = leetcode_id)
       
       if not TemplateProblems.objects.filter(template = template_id, problem = problem).exists():
           return Response({"error":"Problem does not exits in template."},status=status.HTTP_400_BAD_REQUEST)
       
       template_problem = TemplateProblems.objects.get(template = template_id,problem = problem)
       template_problem.delete()
       
       return Response({"success":"problem removed successfully."},status=status.HTTP_204_NO_CONTENT)
           
     
       