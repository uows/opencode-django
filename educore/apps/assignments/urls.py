from django.urls import path
from . import views

urlpatterns = [
    path('', views.assignment_list, name='assignment_list'),
    path('new/', views.assignment_create, name='assignment_create'),
    path('<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('<int:pk>/edit/', views.assignment_edit, name='assignment_edit'),
    path('<int:pk>/delete/', views.assignment_delete, name='assignment_delete'),
]
