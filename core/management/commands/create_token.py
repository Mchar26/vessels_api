from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = "Create token for superuser"

    def handle(self, *args, **kwargs):
        user = User.objects.get(username='tsaritos')
        token, created = Token.objects.get_or_create(user=user)
        self.stdout.write(self.style.SUCCESS(f"Token: {token.key}"))