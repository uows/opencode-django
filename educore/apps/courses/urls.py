from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('new/', views.course_create, name='course_create'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('<int:pk>/delete/', views.course_delete, name='course_delete'),
    path('<int:course_pk>/subjects/new/', views.subject_create, name='subject_create'),
    path('subjects/<int:pk>/edit/', views.subject_edit, name='subject_edit'),
    path('subjects/<int:pk>/delete/', views.subject_delete, name='subject_delete'),
    path('<int:course_pk>/enroll/', views.enroll_student, name='enroll_student'),
]
