from rest_framework import serializers
from .models import Template, UserTemplate

class CreateTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ['name', 'visibility']
        reaf_only_fields = ['id', 'createdAt', 'updatedAt']
    
    def create(self, validated_data):
        
        user = self.context['request'].user 
        template,created = Template.objects.get_or_create(
            createdBy=user, 
            **validated_data
        )
        
        if not created:
            raise serializers.ValidationError('Template with this name already exists.')
        
        UserTemplate.objects.create(
            user=user, 
            template=template
        )  # Automatically associate the creator with the template
        return template
    
class AddTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTemplate
        fields = ['id','template','createdAt']
        read_only_fields = ['id', 'createdAt']
        
    def create(self, validated_data):
        user = self.context['request'].user 
        template = validated_data['template']
        obj, created = UserTemplate.objects.get_or_create(  
            user=user, 
            template=template
        )
        
        if not created:
            raise serializers.ValidationError('Template already added to user.')
        
        return obj
