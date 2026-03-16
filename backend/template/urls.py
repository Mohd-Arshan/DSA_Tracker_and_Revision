from django.urls import path
from .views import *

urlpatterns = [
    path('create/', CreateTemplateView.as_view(), name='create-template'),
    path('add/', AddTemplateView.as_view(), name='add-template'),
    path('my-templates/', GetMyTemplatesView.as_view(), name='my-templates'),
    path('remove/<int:template_id>/', RemoveTemplateView.as_view(), name='remove-template'),
]