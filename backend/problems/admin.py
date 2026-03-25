from django.contrib import admin
from .models import Pattern, Problem, TemplateProblems

# Register your models here.
admin.site.register(Pattern)

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('leetcode_number', 'title', 'difficulty')
    search_fields = ('leetcode_number', 'title')
    list_filter = ('difficulty',)
    
class TemplateProblemsAdmin(admin.ModelAdmin):
    list_display = ('template', 'problem', 'createdAt')
    search_fields = ('template__name', 'problem__title')
    list_filter = ('createdAt',)
    
admin.site.register(Problem, ProblemAdmin)
admin.site.register(TemplateProblems, TemplateProblemsAdmin)
