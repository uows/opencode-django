from django.urls import path
from . import views

urlpatterns = [
    path('', views.grade_list, name='grade_list'),
    path('new/', views.grade_create, name='grade_create'),
    path('<int:pk>/edit/', views.grade_edit, name='grade_edit'),
    path('<int:pk>/delete/', views.grade_delete, name='grade_delete'),
    path('student/<int:student_id>/', views.student_grades, name='student_grades'),
]
