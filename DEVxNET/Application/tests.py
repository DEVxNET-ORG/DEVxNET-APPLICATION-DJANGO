from django.test import TestCase
from django.urls import reverse
from .models import CustomUser, EmployeeProfile
from .forms import CustomUserForm

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='password123',
            role='employee'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.role, 'employee')

class DashboardViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='adminuser',
            password='password123',
            role='admin'
        )

    def test_dashboard_access(self):
        self.client.login(username='adminuser', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

class EmployeeProfileModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='employee1', password='password', role='employee')
        self.profile = EmployeeProfile.objects.create(user=self.user, tasks_completed=10, progress=75.0)

    def test_employee_profile_str(self):
        self.assertEqual(str(self.profile), f"Profile of {self.user.username}")

class LoginViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password123', role='employee')

    def test_login_page_status_code(self):
        response = self.client.get(reverse('login'), {'username': 'testuser', 'password': 'password123'})
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_login_functionality(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password123'})
        # Update the expected redirect
        self.assertRedirects(response, reverse('dashboard'))  # Change this to match actual behavior

class CustomUserFormTest(TestCase):
    def test_valid_form(self):
        form_data = {'username': 'testuser', 'email': 'test@test.com', 'role': 'employee', 'phone_number': '+1234567890'}
        form = CustomUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {'username': '', 'email': 'notanemail'}
        form = CustomUserForm(data=form_data)
        self.assertFalse(form.is_valid())

