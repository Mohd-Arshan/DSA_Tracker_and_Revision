from rest_framework import serializers
from .models import Pattern, Problem, TemplateProblems
from template.models import Template
from .validators import ProblemSerializer
from .utils import get_leetcode_question_info
from .service import get_problem_by_leetcode_number, save_problem


class AddProblemIntoTemplateSerializer(serializers.ModelSerializer):
    
    leetcode_number = serializers.IntegerField(write_only=True)
    #template = serializers.PrimaryKeyRelatedField(queryset=Template.objects.all()) #to get the template object from the template id passed in the request data.  
    class Meta:
        model = TemplateProblems
        fields = ['id','template','leetcode_number','createdAt', 'updatedAt']  
        read_only_fields = ['id','createdAt', 'updatedAt']
    
    def create(self, validated_data):
        user = self.context['request'].user
        template = validated_data['template']
        leetcode_number = validated_data['leetcode_number']
        
        problem = get_problem_by_leetcode_number(leetcode_number)    
        template_problem, created = TemplateProblems.objects.get_or_create(template=template, problem=problem)
        if not created:
            raise serializers.ValidationError("This problem is already added to the template.")
        return template_problem
        
        
class GetAllProblemsInTemplateSerializer(serializers.ModelSerializer):
    problems = serializers.SerializerMethodField()
    createdBy = serializers.StringRelatedField()  # To display the username instead of the user ID
    class Meta:
        model = Template
        fields = ['id', 'name', 'createdBy', 'problems', 'createdAt','updatedAt']
        
    def get_problems(self, obj):
        template_problems = TemplateProblems.objects.filter(template=obj)
        return ProblemSerializer([tp.problem for tp in template_problems], many=True).data
    