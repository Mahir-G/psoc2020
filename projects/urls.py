from django.urls import path
from . import views

app_name='projects'

urlpatterns = [
    path('index/', views.Index.as_view(), name='project_index'),
    path('<int:pk>/', views.ProjectDetail.as_view(), name='detail'),
    path('code_of_conduct/', views.conduct, name='conduct'),
    path('psoc2020/', views.psoc2020, name='psoc2020'),
]
