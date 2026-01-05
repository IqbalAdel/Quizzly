from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User

class CookieTokenAuthentication(BaseAuthentication):
    """
    Custom authentication class that retrieves the JWT token from cookies.
    """

    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        if not token:
            return None

        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            user = User.objects.get(id=user_id)
            return (user, access_token)
        
        except Exception:
            return None