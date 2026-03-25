from django.urls import path
from .views import *
urlpatterns = [
    path('add-problem/', AddProblemIntoTemplateView.as_view(), name='add-problem-into-template'),
    path('list-problems/<int:pk>/', ListProblemsInTemplateView.as_view(), name='list-problems-in-template'),
]