from django.core.management.base import BaseCommand
from portal.models import Teacher
from portal.utils import hash_password

class Command(BaseCommand):
    help = "Create a teacher user with username and password"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str)
        parser.add_argument("password", type=str)

    def handle(self, *args, **opts):
        username = opts["username"]
        password = opts["password"]

        if Teacher.objects.filter(username=username).exists():
            self.stderr.write(self.style.ERROR("Username already exists"))
            return

        salt_hex, hash_hex = hash_password(password)
        Teacher.objects.create(username=username, salt=salt_hex, password_hash=hash_hex)
        self.stdout.write(self.style.SUCCESS(f"Teacher '{username}' created"))
