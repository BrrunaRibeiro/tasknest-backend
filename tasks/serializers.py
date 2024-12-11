from rest_framework import serializers
from .models import Task, Category
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    Provides fields for ID and name.
    """

    class Meta:
        model = Category
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Includes task count as an additional field.
    """
    task_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'task_count']

    def get_task_count(self, obj):
        """
        Get the count of tasks assigned to the user.
        """
        return obj.tasks.count()


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.
    Includes related data for owners and category.
    """
    owners = UserSerializer(many=True, read_only=True)
    owner_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='owners',
        many=True,
        write_only=True,
    )
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        allow_null=True,
    )

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'due_date', 'is_overdue',
            'attachment', 'owners', 'owner_ids', 'priority', 'category',
            'category_id', 'state', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'state': {'required': False},
        }


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles password confirmation and validation.
    """
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']

    def validate(self, data):
        """
        Ensure password and confirm_password match.
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'Passwords do not match.'
            })
        return data

    def validate_email(self, value):
        """
        Check if the email is already registered.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'A user with this email already exists.'
            )
        return value

    def validate_password(self, value):
        """
        Ensure the password has the minimum length.
        """
        if len(value) < 8:
            raise serializers.ValidationError(
                'Password must be at least 8 characters long.'
            )
        return value

    def create(self, validated_data):
        """
        Create a user after removing confirm_password from data.
        """
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Validates user credentials and returns user instance.
    """
    username = serializers.CharField(max_length=25)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Authenticate the user using provided credentials.
        """
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError(
                'Invalid username or password'
            )

        attrs['user'] = user
        return attrs


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for user logout.
    Blacklists the refresh token to invalidate it.
    """
    refresh = serializers.CharField()

    def validate(self, attrs):
        """
        Blacklist the provided refresh token.
        """
        from rest_framework_simplejwt.tokens import RefreshToken
        try:
            token = RefreshToken(attrs['refresh'])
            token.blacklist()
        except Exception:
            raise serializers.ValidationError('Invalid token')
        return attrs


class TaskListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing tasks.
    Provides fields necessary for displaying tasks in a list.
    """

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'due_date', 'priority', 'state',
            'is_overdue', 'created_at', 'updated_at'
        ]


class TaskCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new task.
    Validates due_date and required fields.
    """

    class Meta:
        model = Task
        fields = [
            'title', 'description', 'due_date', 'priority', 'category',
            'state', 'attachment'
        ]

    def validate_due_date(self, value):
        """
        Ensure the due_date is in the future.
        """
        if value < timezone.now():
            raise serializers.ValidationError(
                "Due date must be in the future."
            )
        return value

    def validate(self, data):
        """
        Check for presence of all required fields.
        """
        required_fields = ['title', 'description', 'due_date']
        for field in required_fields:
            if field not in data or not data[field]:
                raise serializers.ValidationError({
                    field: f"{field} is required."
                })
        return data
