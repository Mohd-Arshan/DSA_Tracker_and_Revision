from django.contrib import admin
from .models import UserGlobalProblemProgress,UserTemplateProblemProgress

# Register your models here.

admin.site.register(UserTemplateProblemProgress)
admin.site.register(UserGlobalProblemProgress)
