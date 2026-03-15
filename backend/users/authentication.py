from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get('access_token')
        if raw_token is None:
            return None
        validated_token = self.get_validated_token(raw_token)
        
        token_version = validated_token.get('token_version')
        user = self.get_user(validated_token)
        if user.token_version != token_version:
            raise AuthenticationFailed('Token has been invalidated. Please log in again.')
        return user, validated_token