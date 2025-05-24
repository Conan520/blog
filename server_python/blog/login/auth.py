from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication, AuthUser

from .models import UserInfo


class CustomJSONWebTokenAuthentication(JWTAuthentication):
    def authenticate(self, request):
        jwt_value = request.META.get("HTTP_TOKEN")
        if not jwt_value:
            raise AuthenticationFailed("Token is missing")
        validated_token = self.get_validated_token(jwt_value)
        user = UserInfo.objects.filter(pk=validated_token['user_id']).first()
        if not user:
            raise AuthenticationFailed("User not found")
        setattr(user, 'is_authenticated', True)
        return user, jwt_value
