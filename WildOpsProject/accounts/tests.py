from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group

class AccountsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')

    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_login_user(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('index'))

    def test_groups_created(self):
        groups = ['Admin', 'Safety Officer', 'Field Member', 'Visitor']
        for group in groups:
            self.assertTrue(Group.objects.filter(name=group).exists(), f"Group {group} does not exist")