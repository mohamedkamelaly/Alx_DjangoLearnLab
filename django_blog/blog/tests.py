from django.test import TestCase

# Create your tests here.
#from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserAuthenticationTests(TestCase):

    def test_user_registration(self):
        # Test user registration
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Check if it redirects after successful registration
        self.assertTrue(User.objects.filter(username='testuser').exists())  # Ensure user is created

    def test_user_login(self):
        # Create user first
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        
        # Test login
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)  # Check if login redirects
        self.assertTrue(response.wsgi_request.user.is_authenticated)  # Check if user is authenticated

    def test_user_logout(self):
        # Create and log in user first
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.login(username='testuser', password='password123')

        # Test logout
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Check if logout redirects
        self.assertFalse(response.wsgi_request.user.is_authenticated)  # Ensure user is logged out

    def test_profile_update(self):
        # Create and log in user
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.login(username='testuser', password='password123')

        # Test profile update
        response = self.client.post(reverse('profile'), {
            'username': 'newusername',
            'email': 'newemail@example.com',
        })
        self.assertEqual(response.status_code, 302)  # Check if update redirects
        user.refresh_from_db()
        self.assertEqual(user.username, 'newusername')  # Check if username is updated
        self.assertEqual(user.email, 'newemail@example.com')  # Check if email is updated
