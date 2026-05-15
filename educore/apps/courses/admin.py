from django.contrib import admin
from .models import Course, Subject, Enrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'year', 'teacher')
    list_filter = ('year', 'grade')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')
