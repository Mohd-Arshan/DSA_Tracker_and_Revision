from django.db import models
from users.models import User

# Create your models here.


class Template(models.Model):
    
    class Visibility(models.TextChoices):
        PUBLIC = 'public', 'Public'
        PRIVATE = 'private', 'Private'
        
    name = models.CharField(max_length=255)
    visibility = models.CharField(
        max_length=10,
        choices=Visibility.choices,
        default=Visibility.PRIVATE,
    )
    createdBy = models.ForeignKey(User, 
            on_delete=models.CASCADE,
            related_name='created_templates'
    )
    
    users = models.ManyToManyField(
        User,
        through='UserTemplate',
        related_name='saved_templates'
    )
    
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
   
    

class UserTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'template')  # Ensure a user can only have one association with a template
        
    def __str__(self):
        return f"{self.user.username} - {self.template.name}"
  

    