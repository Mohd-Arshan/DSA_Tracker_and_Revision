from rest_framework import serializers
from .models import Problem, Pattern


class ProblemSerializer(serializers.ModelSerializer):
    # WRITE
    patterns = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )

    # READ
    patterns_display = serializers.StringRelatedField(
        many=True,
        read_only=True,
        source='patterns'
    )
    class Meta:
        model = Problem
        fields = ['leetcode_number', 'title', 'difficulty', 'patterns','url','patterns_display','createdAt', 'updatedAt']
        read_only_fields = ['createdAt', 'updatedAt']
        #read_only_fields means 
        
    def create(self, validated_data):
        patterns_data = validated_data.pop('patterns', []) #pop is used to remove the patterns data from validated_data and store it in patterns_data variable. If patterns data is not present in validated_data, it will return an empty list.
        problem = Problem.objects.create(**validated_data)
        for pattern_title in patterns_data:
            pattern, created = Pattern.objects.get_or_create(title=pattern_title)
            problem.patterns.add(pattern)
        return problem