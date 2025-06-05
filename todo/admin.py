from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'priority', 'completed', 'created_date', 'due_date']
    list_filter = ['completed', 'priority', 'created_date']
    search_fields = ['title', 'description']
    list_editable = ['completed']
    date_hierarchy = 'created_date'