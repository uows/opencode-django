from django.contrib import admin
from .models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'due_date', 'created_by')
    list_filter = ('subject', 'due_date')
