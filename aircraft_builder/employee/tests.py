from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Employee
from .forms import EmployeeSignUpForm
from teams.models import Team

class EmployeeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.team = Team.objects.create(name='Test Team')
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass', team=self.team)
        self.user.save()

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/login.html')

    def test_login_view_post_valid(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertRedirects(response, reverse('home'))

    def test_login_view_post_invalid(self):
        response = self.client.post(reverse('login'), {'username': 'wronguser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/login.html')
        self.assertContains(response, "Geçersiz kullanıcı adı veya şifre.")

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_home_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/home.html')

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/register.html')

    def test_register_view_post_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'team': self.team.id
        }
        response = self.client.post(reverse('register'), form_data)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(Employee.objects.filter(username='newuser').exists())

    def test_register_view_post_invalid(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'wrongpassword',
            'team': self.team.id
        }
        response = self.client.post(reverse('register'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/register.html')
        self.assertContains(response, "Kayıt olurken bir hata oluştu. Lütfen bilgileri kontrol edin.")
