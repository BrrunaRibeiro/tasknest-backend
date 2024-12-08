from rest_framework import serializers
from .models import Task, Category
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone  # Added for due_date validation

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

class RegisterSerializer(serializers.ModelSerializer):
    """Handles user registration with password confirmation."""
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']

    def validate(self, data):
        """Ensure password and confirm_password match."""
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})
        return data

    def validate_email(self, value):
        """Check if email is already registered."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    def validate_password(self, value):
        """Validate password length."""
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long.')
        return value

    def create(self, validated_data):
        """Remove confirm_password from validated data and create user."""
        validated_data.pop('confirm_password')  # Remove confirm_password before creating user
        user = User.objects.create_user(
            username=validated_data['email'],  # Use email as the username
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=25)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        # Authenticate user using Django's authenticate function
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('Invalid username or password')

        attrs['user'] = user  # Attach user to the validated data
        return attrs

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        from rest_framework_simplejwt.tokens import RefreshToken
        try:
            token = RefreshToken(attrs['refresh'])
            token.blacklist()  # Blacklists the token to invalidate it
        except Exception:
            raise serializers.ValidationError('Invalid token')
        return attrs

class TaskListSerializer(serializers.ModelSerializer):
    """
    A serializer for listing tasks.
    Includes fields necessary for displaying tasks in a list.
    """
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'due_date', 'priority', 'state',
            'is_overdue', 'created_at', 'updated_at'
        ]

class TaskCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new task with validation checks.
    Ensures required fields are present and due_date is in the future.
    """
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'category', 'state', 'attachment']

    def validate_due_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value

    def validate(self, data):
        required_fields = ['title', 'description', 'due_date']
        for field in required_fields:
            if field not in data or not data[field]:
                raise serializers.ValidationError({field: f"{field} is required."})
        return data
