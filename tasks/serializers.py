from rest_framework import serializers  
from .models import Task, Category  
from django.contrib.auth.models import User  

class CategorySerializer(serializers.ModelSerializer):  
    """  
    Serializes Category instances.  
    """  
    class Meta:  
        model = Category  
        fields = ['id', 'name']  

class UserSerializer(serializers.ModelSerializer):  
    """  
    Serializes User instances.  
    """  
    class Meta:  
        model = User  
        fields = ['id', 'username', 'email']  

class TaskSerializer(serializers.ModelSerializer):  
    """  
    Serializes Task instances and includes related data.  
    """  
    owners = UserSerializer(many=True, read_only=True)  
    owner_ids = serializers.PrimaryKeyRelatedField(  
        queryset=User.objects.all(), source='owners', many=True, write_only=True  
    )  
    category = CategorySerializer(read_only=True)  
    category_id = serializers.PrimaryKeyRelatedField(  
        queryset=Category.objects.all(), source='category', write_only=True, allow_null=True  
    )  

    class Meta:  
        model = Task  
        fields = [  
            'id', 'title', 'description', 'due_date', 'is_overdue', 'attachment',  
            'owners', 'owner_ids', 'priority', 'category', 'category_id', 'state',  
            'created_at', 'updated_at'  
        ]