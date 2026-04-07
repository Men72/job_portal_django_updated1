from django.core.management.base import BaseCommand
from portal.models import User

class Command(BaseCommand):
    help = 'Create default admin account'

    def handle(self, *args, **kwargs):
        if User.objects.filter(role='admin').exists():
            self.stdout.write(self.style.WARNING(
                'Admin already exists — skipping.'
            ))
            return

        u = User(
            username     = 'admin@gmail.com',
            email        = 'admin@gmail.com',
            first_name   = 'Admin',
            last_name    = 'User',
            role         = 'admin',
            is_staff     = True,
            is_superuser = True,
            avatar       = 'https://cdn-icons-png.flaticon.com/256/6171/6171591.png'
        )
        u.set_password('admin1234')
        u.save()

        self.stdout.write(self.style.SUCCESS(
            'Admin created successfully!\n'
            'Email:    admin@gmail.com\n'
            'Password: admin1234\n'
            'Please change the password after first login!'
        ))
