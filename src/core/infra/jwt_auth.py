from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from core.domain.user import User


class SISAJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token[self.user_id_claim]
        except KeyError:
            raise InvalidToken("Token contains no user ID")
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found", "user_not_found")
        return user

    def authenticate(self, request):
        result = super().authenticate(request)
        if result is not None:
            user, token = result
            return user, token
        return None
