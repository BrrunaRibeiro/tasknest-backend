from django.contrib import admin
from .models import Task, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Category model.
    """
    list_display = ('id', 'name')  # Display category ID and name
    search_fields = ('name',)  # Add a search bar for category names


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Task model.
    """
    list_display = (
        'id', 'title', 'priority', 'state', 'due_date',
        'is_overdue', 'category'
    )  # Fields to display in the task list
    list_filter = (
        'priority', 'state', 'category', 'is_overdue'
    )  # Add filters for priority, state, and category
    search_fields = ('title', 'description')  # Add a search bar for tasks
    filter_horizontal = ('owners',)  # Add a horizontal filter for owners
