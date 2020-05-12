from django.urls import path
from . import views

app_name='mentors'

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('dashboard/', views.DashBoard.as_view(), name='dashboard'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('dashboard/project/new', views.CreateProject.as_view(), name='create_project'),
]