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
    Serializes User instances. Includes task count.  
    """  
    task_count = serializers.SerializerMethodField()  

    class Meta:  
        model = User  
        fields = ['id', 'username', 'email', 'task_count']  

    def get_task_count(self, obj):  
        """  
        Returns the count of tasks assigned to the user.  
        """  
        return obj.tasks.count()  

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

# Serializer for user registration  
class RegisterSerializer(serializers.ModelSerializer):
    """Handles user registration."""  
    password = serializers.CharField(write_only=True)  

    class Meta:  
        model = User  
        fields = ['email', 'password']  

    def validate_password(self, value):  
        """Validates the password (e.g., minimum length)."""  
        if len(value) < 8:  
            raise serializers.ValidationError('Password must be at least 8 characters long.')  
        return value  

    def create(self, validated_data):  
        # Create a new user with the provided email and password  
        user = User.objects.create_user(  
            username=validated_data['email'],  # Use email as the username  
            email=validated_data['email'],  
            password=validated_data['password']  
        )  
        return user
