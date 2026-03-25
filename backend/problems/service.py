from template.models import Template
from .models import Problem, Pattern, TemplateProblems
from rest_framework import serializers
from .validators import ProblemSerializer
from .utils import get_leetcode_question_info


def get_problem_by_leetcode_number(leetcode_number):
    try:
        return Problem.objects.get(leetcode_number=leetcode_number)
    except Problem.DoesNotExist:
        problem_info = get_leetcode_question_info(leetcode_number)
        if 'error' in problem_info:
            raise ValueError(problem_info['error'])
        return save_problem(problem_info)
        
        
def save_problem(problem_info):
    problem_serializer = ProblemSerializer(data=problem_info)
    try:
        problem_serializer.is_valid(raise_exception=True)
        return problem_serializer.save()
    except serializers.ValidationError as e:
        raise ValueError("Failed to create problem: " + str(e.detail))