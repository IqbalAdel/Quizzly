from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import RegistrationSerializer, LoginAuthTokenSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

class CookieTokenRefreshView(TokenRefreshView):
    """
    API endpoint for refreshing JWT access tokens.

    Accepts a valid refresh token and returns a new access token.
    """
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            return Response({
                "detail": "Refresh token not provided in cookies."
            }, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data={'refresh': refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({
                "detail": "Invalid refresh token."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        access = serializer.validated_data.get('access')
        response = super().post(request, *args, **kwargs)
        response.set_cookie(
            key='access_token',
            value=access,
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        response.data ={
            "detail": "Token refreshed",
            "access": access
            } 
        return response

class CookieTokenObtainPairView(TokenObtainPairView):
    """
    API endpoint for obtaining JWT access and refresh tokens.

    Validates user credentials and returns a token pair for authenticated access.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        else:
            response = super().post(request, *args, **kwargs)
            access = response.data.get('access')
            refresh = response.data.get('refresh')
            user = serializer.validated_data.get('user')
            response.set_cookie(
                key='access_token',
                value=access,
                httponly=True,
                secure=True,
                samesite='Lax'
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh,
                httponly=True,
                secure=True,
                samesite='Lax'
            )
        
            response.data = {
                "detail": "Login successfully.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                    }
                }
            return response

class LogoutView(APIView):
    """
    API endpoint for logging out users.

    Deletes JWT access and refresh tokens from cookies, effectively logging out the user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response(
            {"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."},
            status = status.HTTP_200_OK
        )
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        
        return response

class RegistrationView(APIView):
    """
    API endpoint for registering new users.

    Handles creation of user accounts, including username validation. Returns the created user data.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            data = {
                'username': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.pk
            }
            return Response({
                            "detail": "User created successfully!"
                            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)