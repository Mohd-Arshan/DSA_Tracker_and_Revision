from django.urls import path
from .views import *
urlpatterns = [
    path('addStats/',UserProblemStatViewSet.as_view(),name='user-problem-stat'),
    path('list/<int:template_id>/',UserTemplateProblemListViewSet.as_view(),name='user-template-problem-list'),
    path('globalProgress/',UserGlobalProblemProgressListViewSet.as_view(),name='user-global-problem-progress'),
    path('problemHistory/<int:problem_id>/',ProblemHistoryViewSet.as_view(),name='user-problem-history')
]