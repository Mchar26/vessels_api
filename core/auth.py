from ninja.security import HttpBearer
from rest_framework.authtoken.models import Token

class BearerAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            token_obj = Token.objects.get(key=token)
            return token_obj.user
        except Token.DoesNotExist:
            return None