from django.shortcuts import render
from rest_framework.generics import UpdateAPIView, ListAPIView
from .models import UserTemplateProblemProgress,UserGlobalProblemProgress
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class UserProblemStatViewSet(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddProblemStatSerializer
    
    def put(self, request, *args, **kwargs):
        user = request.user
        template_problem_id = request.data.get('templateProblem')
        try:
            instance = UserTemplateProblemProgress.objects.get(user=user, templateProblem_id=template_problem_id)
        except UserTemplateProblemProgress.DoesNotExist:
            return Response({"detail": "UserTemplateProblemProgress instance not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
class UserTemplateProblemListViewSet(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserTemplateProblemProgressSerializer
    
    def get_queryset(self):
        user = self.request.user
        template_id = self.kwargs.get('template_id')
        return UserTemplateProblemProgress.objects.filter(user=user, templateProblem__template_id=template_id)
    
class UserGlobalProblemProgressListViewSet(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GlobalProblemProgressSerializer
    
    def get_queryset(self):
        user = self.request.user
        return UserGlobalProblemProgress.objects.filter(user=user)
    
class ProblemHistoryViewSet(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAttemptesAndScoreSerializer
    
    def get_queryset(self):
        user = self.request.user
        problem_id = self.kwargs.get('problem_id')
        return UserAttemptesAndScore.objects.filter(global_progress__user=user, global_progress__problem_id=problem_id).order_by('-createdAt')
    


        
