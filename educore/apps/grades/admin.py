from django.contrib import admin
from .models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'score', 'coefficient', 'date')
    list_filter = ('subject', 'date')
