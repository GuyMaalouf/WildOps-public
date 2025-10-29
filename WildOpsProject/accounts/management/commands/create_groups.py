from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **kwargs):
        # Define permissions
        custom_permissions = [
            {"codename": "view_olpejeta", "name": "Can view Ol Pejeta"},
            {"codename": "view_flightcylinders", "name": "Can view flight cylinders"},
            {"codename": "view_index", "name": "Can view the index page"},
        ]

        # Ensure the permissions exist in the database
        content_type = ContentType.objects.get_for_model(User)  # Use a generic content type
        for perm in custom_permissions:
            permission, created = Permission.objects.get_or_create(
                codename=perm["codename"],
                name=perm["name"],
                content_type=content_type,
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Permission '{perm['codename']}' created."))
            else:
                self.stdout.write(self.style.WARNING(f"Permission '{perm['codename']}' already exists."))

        # Create groups
        admin_group, created = Group.objects.get_or_create(name='Admin')
        self.stdout.write(self.style.SUCCESS(f"Admin group created: {created}"))
        safety_officer_group, created = Group.objects.get_or_create(name='Safety Officer')
        self.stdout.write(self.style.SUCCESS(f"Safety Officer group created: {created}"))
        field_member_group, created = Group.objects.get_or_create(name='Field Member')
        self.stdout.write(self.style.SUCCESS(f"Field Member group created: {created}"))
        visitor_group, created = Group.objects.get_or_create(name='Visitor')
        self.stdout.write(self.style.SUCCESS(f"Visitor group created: {created}"))

        # Assign permissions to groups
        # Admin: access to everything
        admin_permissions = Permission.objects.all()
        admin_group.permissions.set(admin_permissions)

        # Safety Officer: access to Ol Pejeta & Flight Cylinders
        safety_officer_permissions = Permission.objects.filter(codename__in=['view_olpejeta', 'view_flightcylinders'])
        safety_officer_group.permissions.set(safety_officer_permissions)

        # Field Member: access to Ol Pejeta
        field_member_permissions = Permission.objects.filter(codename='view_olpejeta')
        field_member_group.permissions.set(field_member_permissions)

        # Visitor: access to index
        visitor_permissions = Permission.objects.filter(codename='view_index')
        visitor_group.permissions.set(visitor_permissions)

        self.stdout.write(self.style.SUCCESS('User groups and permissions have been created successfully.'))
