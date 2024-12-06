from rest_framework import serializers  
from .models import Task, Category  
from django.contrib.auth.models import User  
from django.contrib.auth import authenticate

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
    """Handles user registration."""
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
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['email'],  # Use email as the username
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
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
        except Exception as e:
            raise serializers.ValidationError('Invalid token')
        return attrs