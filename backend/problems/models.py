from django.db import models
from template.models import Template
from django.utils import timezone
# Create your models here.

class Pattern(models.Model):
    title = models.CharField(max_length=15,unique=True)
    description = models.TextField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class Problem(models.Model):
    
    class Difficulty(models.TextChoices):
        EASY = 'Easy', 'Easy'
        MEDIUM = 'Medium', 'Medium'
        HARD = 'Hard', 'Hard'
        
    
    leetcode_number = models.IntegerField(unique=True)
    title = models.TextField(max_length=100)
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices)
    patterns = models.ManyToManyField(Pattern, related_name='problems')
    url = models.URLField(max_length=200, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class TemplateProblems(models.Model):
    
    template = models.ForeignKey(
        Template,
        on_delete=models.CASCADE,
        related_name='template_problems'
    )
    
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name='template_problems'
    )
    
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('template', 'problem')
        
    def __str__(self):
        return f"{self.template} - {self.problem}"
    
