from django.db import models
from problems.models import TemplateProblems,Problem
from users.models import User

# Create your models here.

class UserTemplateProblemProgress(models.Model):
    class Status(models.TextChoices):
        UNSOLVED = 'unsolved','Unsolved'
        SOLVED_ALONE = 'solved_alone','SolvedAlone'
        SOLVED_WITH_HINT = 'solved_with_hint','SolvedWithHint'
        SOLVED_WITH_EDITORIAL = 'solved_with_editorial','SolvedWithEditorial'
        
    class Mistake(models.TextChoices):
        EDGE_CASE = 'edge_case','EgdeCase'
        LOGICAL = 'logical','Logical'
        OPTIMIZATION = 'optimization','Optimization'
        IMPLEMENTATION = 'implementation','Implementation'
        
    status = models.CharField(max_length=22,choices=Status.choices,default=Status.UNSOLVED)
    timeTaken = models.DurationField(blank=True,null=True)
    hintCount = models.PositiveIntegerField(default=0)
    mistakes = models.JSONField(default = list,blank = True) # {"edge_case":true,"logical":false,"optimization":true,"implementation":false}
    solvedAt = models.DateTimeField(blank=True,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    
    templateProblem = models.ForeignKey(
        TemplateProblems,
        on_delete=models.CASCADE,
        related_name='problem_progress'
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_progress'
    )
    
    class Meta:
        unique_together = ('user','templateProblem')
        
    def __str__(self):
        return f"{self.user} - {self.templateProblem}"
    
    
class UserGlobalProblemProgress(models.Model):
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='global_user_progress'
    )
    
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name='global_problem_progress'
    )
    
    score = models.PositiveIntegerField(default=0)
    stability = models.FloatField(default=6.3)
    solvedCount  = models.PositiveIntegerField(default=1)
    revisionDate = models.DateField(null=True,blank=True)
    
    createdAt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user','problem')
        
    def __str__(self):
        return f"{self.user} - {self.problem}"
    
        
class UserAttemptesAndScore(models.Model):
    global_progress = models.ForeignKey(
        UserGlobalProblemProgress,
        on_delete=models.CASCADE,
        related_name='user_attempts_and_score'
    )
    
    attemptCount = models.PositiveIntegerField(default=1)
    timeTaken = models.DurationField(blank=True,null=True)
    hintCount = models.PositiveIntegerField(default=0)
    mistakes = models.JSONField(default = list,blank = True) # {"edge_case":true,"logical":false,"optimization":true,"implementation":false}
    score = models.PositiveIntegerField(default=0)
     
    createdAt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('global_progress','attemptCount')
        
    def __str__(self):
        return f"{self.global_progress.user} - {self.global_progress.problem} - {self.attemptCount} - {self.score}"