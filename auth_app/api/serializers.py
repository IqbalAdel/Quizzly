from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model, authenticate
User = get_user_model()
class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.
    Handles validation, creation, and serialization of User data.

    Fields:
        id (int): Read-only. Unique identifier of the user.
        username (str): username of the user.
        email (str): Email address of the user. Must be unique.
        password (str): User's password. Write-only.
        confirmed_password (str): Confirmation of the password. Write-only; must match `password`.
    """
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirmed_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'email': {
                'required': True
            }
        }

    def validate_confirmed_password(self, value):
        password = self.initial_data.get('password')
        if password and value and password != value:
            raise serializers.ValidationError('Passwords do not match')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def save(self):
        pw = self.validated_data['password']

        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(pw)
        account.save()
        return account

class LoginAuthTokenSerializer(serializers.Serializer):
    """
    Serializer for loggin in users.
    Handles validation and serialization of User data.

    Fields:
        username (str): username of the user. Must be unique.
        password (str): User's password. Write-only.
    """

    username = serializers.CharField()
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):    
        password = attrs.get('password')
        username= attrs.get('username')

        user = authenticate(username=username, password=password)
        if not user:
            res = serializers.ValidationError({'detail': 'Invalid username or password.'}) 
            res.status_code = 400
            raise res     
        attrs['user'] = user
        return attrs
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom Serializer for loggin in users.
    Handles validation and serialization of User data.

    Fields:
        email (str): email of the user. Must be unique.
        password (str): User's password. Write-only.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "username" in self.fields:
            self.fields.pop("username")

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('No user with this email found')

        if not user.check_password(password):
            raise serializers.ValidationError('Incorrect password')

        data = super().validate({
            'username': user.username,
            'password': password
        })

        return data