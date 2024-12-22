from django.test import TestCase, Client
from django.urls import reverse
from employee.models import Employee
from .models import Team
from inventory.models import Part, PartStock

class TeamViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Employee.objects.create_user(username='testuser', password='testpass')  
        self.team = Team.objects.create(name='Test Team', responsible_part='KANAT')
        self.user.team = self.team
        self.user.save()
        self.client.login(username='testuser', password='testpass')

    def test_list_parts(self):
        response = self.client.get(reverse('list_parts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teams/parts_list.html')

    def test_create_part_get(self):
        response = self.client.get(reverse('create_part'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teams/create_part.html')

    def test_create_part_post(self):
        response = self.client.post(reverse('create_part'), {
            'aircraft_type': 'TB2',
            'quantity': 1
        })
        self.assertRedirects(response, reverse('list_parts'))
        self.assertTrue(Part.objects.filter(part_type='KANAT', aircraft_type='TB2').exists())
        self.assertTrue(PartStock.objects.filter(part_type='KANAT', aircraft_type='TB2').exists())

    def test_delete_part(self):
        part = Part.objects.create(part_type='KANAT', aircraft_type='TB2', serial_number='KANAT-123456')
        response = self.client.post(reverse('delete_part', args=[part.id]))
        self.assertRedirects(response, reverse('list_parts'))
        self.assertFalse(Part.objects.filter(id=part.id).exists())

