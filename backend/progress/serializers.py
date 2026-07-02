from rest_framework import serializers
from .models import UserTemplateProblemProgress,UserGlobalProblemProgress,UserAttemptesAndScore
from problems.models import Problem,TemplateProblems
from datetime import timedelta
from django.utils.timezone import localdate,now
from datetime import datetime
from django.db import transaction
from .algorithm import getScore,getStability,nextRevisionDays

class AddProblemStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTemplateProblemProgress
        fields = ['templateProblem','status','timeTaken','hintCount','mistakes']
        read_only_fields = ['solvedAt','createdAt']
     
    @transaction.atomic   
    def update(self, instance, validated_data):
        instance = UserTemplateProblemProgress.objects.select_for_update().get(pk=instance.pk)
        old_status = instance.status
        new_status = validated_data['status']
        instance.status = new_status 
        
        #duplicate request
        if old_status != UserTemplateProblemProgress.Status.UNSOLVED and (now() - instance.solvedAt) < timedelta(days=1):
            return instance
        problem_id = TemplateProblems.objects.get(pk=instance.templateProblem.pk).problem.pk
        difficulty = Problem.objects.get(pk=problem_id).difficulty
        
        if new_status != UserTemplateProblemProgress.Status.UNSOLVED:
            instance.solvedAt = localdate()
            instance.timeTaken = validated_data.get('timeTaken', instance.timeTaken)
            instance.hintCount = validated_data.get('hintCount', instance.hintCount)
            instance.mistakes = validated_data.get('mistakes', instance.mistakes)
            instance.save()
              
            user = instance.user
            problem = instance.templateProblem.problem
            score = getScore(instance.status,instance.hintCount,instance.mistakes,instance.timeTaken,difficulty)
            
            global_progress, created = UserGlobalProblemProgress.objects.select_for_update().get_or_create(user=user, problem=problem)
            
            # If the user has already solved the problem before, we will update the score and revision date based on the new score and the previous revision date. If not, we will set the score and revision date based on the new score and the current date.
            if not created:
                global_progress.stability = getStability(global_progress.score,score,global_progress.stability)
                
                # The new score is calculated as the average of the previous score and the new score.
                global_progress.score = ((global_progress.solvedCount* global_progress.score) + score) / (global_progress.solvedCount + 1)
                
                global_progress.solvedCount += 1
                global_progress.revisionDate = localdate() + timedelta(days = nextRevisionDays(global_progress.stability))
                print(nextRevisionDays(global_progress.stability))
                global_progress.save()
            else:
                global_progress.score = score
                global_progress.revisionDate = localdate() + timedelta(days = nextRevisionDays(global_progress.stability))
                global_progress.save()
            
            UserAttemptesAndScore.objects.create(global_progress=global_progress, score=score, attemptCount= global_progress.solvedCount)
        return instance 
    
    
class UpdateStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTemplateProblemProgress
        fields = ['templateProblem','status','timeTaken','hintCount','mistakes']
        read_only_fields = ['solvedAt','createdAt']
        
    @transaction.atomic
    def update(self, instance, validated_data):
        instance = UserTemplateProblemProgress.objects.select_for_update().get(pk=instance.pk)
        
        if instance.status == UserTemplateProblemProgress.Status.UNSOLVED:
            return serializers.ValidationError("Cannot update stats for an unsolved problem.")
        
        if (now() - instance.solvedAt) > timedelta(minutes=30):
            return serializers.ValidationError("Cannot update stats for a problem solved more than 30 minutes ago.")
        
        instance.status = validated_data.get('status', instance.status)
        instance.timeTaken = validated_data.get('timeTaken', instance.timeTaken)
        instance.hintCount = validated_data.get('hintCount', instance.hintCount)
        instance.mistakes = validated_data.get('mistakes', instance.mistakes)
        
        if instance.status != UserTemplateProblemProgress.Status.UNSOLVED:
            instance.solvedAt = localdate()
        
        instance.save()
        return instance
    
class TemplateDataSerializer(serializers.ModelSerializer):
    templateName = serializers.CharField(source='template.name', read_only=True)
    templateProblemId = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = TemplateProblems
        fields = ['template','templateName','templateProblemId']
        
class ProblemDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['leetcode_number','title','difficulty']
        

class UserTemplateProblemProgressSerializer(serializers.ModelSerializer):
    templateData = TemplateDataSerializer(source='templateProblem', read_only=True) 
    problemData = ProblemDataSerializer(source='templateProblem.problem', read_only=True)
    score = serializers.SerializerMethodField()
    
    class Meta:
        model = UserTemplateProblemProgress
        fields = ['templateData','problemData','timeTaken','hintCount','score','solvedAt','createdAt']
    
    def get_score(self, obj):
        try:
            global_progress = UserGlobalProblemProgress.objects.get(user=obj.user, problem=obj.templateProblem.problem)
            return global_progress.score
        except UserGlobalProblemProgress.DoesNotExist:
            return 0
        
        
class GlobalProblemProgressSerializer(serializers.ModelSerializer):
    problemData = ProblemDataSerializer(source='problem', read_only=True)
    
    class Meta:
        model = UserGlobalProblemProgress
        fields = ['problemData','score','stability','solvedCount','revisionDate','createdAt']
        
class UserAttemptesAndScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAttemptesAndScore
        fields = ['global_progress','attemptCount','score','timeTaken','hintCount','mistakes','createdAt']
    
