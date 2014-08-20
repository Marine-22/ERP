from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Generates a new user, with username 'admin' and password 'admin'."
    requires_model_validation = True
    
    def handle(self, *app_labels, **options):
        call_command("createsuperuser", username='admin', email='admin@example.com', interactive=False)
        admin = User.objects.get(username__exact='admin')
        admin.set_password('admin')
        admin.save()
