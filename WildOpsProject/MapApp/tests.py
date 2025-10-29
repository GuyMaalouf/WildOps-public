# MapApp/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group, Permission

class MapAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin_group = Group.objects.create(name='Admin')
        self.safety_officer_group = Group.objects.create(name='Safety Officer')
        self.field_member_group = Group.objects.create(name='Field Member')
        self.visitor_group = Group.objects.create(name='Visitor')

        # Assign permissions to groups
        self.admin_group.permissions.set(Permission.objects.all())
        self.safety_officer_group.permissions.set(Permission.objects.filter(codename__in=['view_olpejeta', 'view_flightcylinders']))
        self.field_member_group.permissions.set(Permission.objects.filter(codename='view_olpejeta'))
        self.visitor_group.permissions.set(Permission.objects.filter(codename='view_index'))

    def test_home_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'WildOps')

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')

    def test_admin_access(self):
        self.user.groups.add(self.admin_group)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('olpejeta'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('flight_cylinders'))
        self.assertEqual(response.status_code, 200)

    def test_safety_officer_access(self):
        self.user.groups.add(self.safety_officer_group)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('olpejeta'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('flight_cylinders'))
        self.assertEqual(response.status_code, 200)

    def test_field_member_access(self):
        self.user.groups.add(self.field_member_group)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('olpejeta'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('flight_cylinders'))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_visitor_access(self):
        self.user.groups.add(self.visitor_group)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('olpejeta'))
        self.assertEqual(response.status_code, 403)  # Forbidden
        response = self.client.get(reverse('flight_cylinders'))
        self.assertEqual(response.status_code, 403)  # Forbidden