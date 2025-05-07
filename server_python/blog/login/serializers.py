from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from login.models import UserInfo


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('username', 'password')

    def validate(self, attrs):
        user = self._get_user(attrs)
        refresh = RefreshToken.for_user(user)
        print(f"{refresh = }")
        print(refresh.access_token)
        self.context['refresh'] = str(refresh)
        self.context['access'] = str(refresh.access_token)
        return attrs

    def _get_user(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = UserInfo.objects.filter(username=username, password=password).first()
        if not user:
            raise ValidationError({'user': "user error"})
        return user