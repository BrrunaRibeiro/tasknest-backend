from django.contrib import admin  
from .models import Task, Category  

# Customize the Category admin  
@admin.register(Category)  
class CategoryAdmin(admin.ModelAdmin):  
    list_display = ('id', 'name')  # Display category ID and name  
    search_fields = ('name',)  # Add a search bar for category names  

# Customize the Task admin  
@admin.register(Task)  
class TaskAdmin(admin.ModelAdmin):  
    list_display = ('id', 'title', 'priority', 'state', 'due_date', 'is_overdue', 'category')  # Fields to display in the task list  
    list_filter = ('priority', 'state', 'category', 'is_overdue')  # Add filters for priority, state, and category  
    search_fields = ('title', 'description')  # Add a search bar for tasks  
    filter_horizontal = ('owners',)  # Add a horizontal filter for the ManyToManyField (owners)  