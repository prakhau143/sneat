from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates the default Super Admin user'

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').exists():
            self.stdout.write(
                self.style.WARNING('Super Admin user already exists!')
            )
            return

        user = User.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='admin',
            first_name='Super',
            last_name='Admin'
        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created Super Admin user: {user.username}')
        )
        self.stdout.write(
            self.style.SUCCESS('Username: admin, Password: admin')
        )
