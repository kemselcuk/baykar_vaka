from django.test import TestCase, Client
from django.urls import reverse
from employee.models import Employee
from teams.models import Team
from inventory.models import Part, PartStock, UsedPart
from .models import ProducedAircraft

class AircraftViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Employee.objects.create_user(username='testuser', password='testpass')
        self.team = Team.objects.create(name='Montaj Team', responsible_part='MONTAJ')
        self.user.team = self.team
        self.user.save()
        self.client.login(username='testuser', password='testpass')

    def test_assemble_aircraft_get(self):
        response = self.client.get(reverse('assemble_aircraft'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'aircraft/assemble.html')

    def test_assemble_aircraft_post(self):
        PartStock.objects.create(part_type='KANAT', aircraft_type='TB2', quantity=2)
        PartStock.objects.create(part_type='GOVDE', aircraft_type='TB2', quantity=2)
        PartStock.objects.create(part_type='KUYRUK', aircraft_type='TB2', quantity=2)
        PartStock.objects.create(part_type='AVIYONIK', aircraft_type='TB2', quantity=2)
        
        Part.objects.create(part_type='KANAT', aircraft_type='TB2', serial_number='KANAT-123456')
        Part.objects.create(part_type='KANAT', aircraft_type='TB2', serial_number='KANAT-654321')
        Part.objects.create(part_type='GOVDE', aircraft_type='TB2', serial_number='GOVDE-123456')
        Part.objects.create(part_type='GOVDE', aircraft_type='TB2', serial_number='GOVDE-654321')
        Part.objects.create(part_type='KUYRUK', aircraft_type='TB2', serial_number='KUYRUK-123456')
        Part.objects.create(part_type='KUYRUK', aircraft_type='TB2', serial_number='KUYRUK-654321')
        Part.objects.create(part_type='AVIYONIK', aircraft_type='TB2', serial_number='AVIYONIK-123456')
        Part.objects.create(part_type='AVIYONIK', aircraft_type='TB2', serial_number='AVIYONIK-654321')

        response = self.client.post(reverse('assemble_aircraft'), {
            'aircraft_type': 'TB2',
            'kanat_qty': 1,
            'govde_qty': 1,
            'kuyruk_qty': 1,
            'aviyonik_qty': 1
        })
        self.assertRedirects(response, reverse('list_aircraft'))
        self.assertTrue(ProducedAircraft.objects.filter(aircraft_type='TB2').exists())
        self.assertEqual(UsedPart.objects.count(), 4)

    def test_list_aircraft(self):
        ProducedAircraft.objects.create(aircraft_type='TB2')
        response = self.client.get(reverse('list_aircraft'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'aircraft/list.html')
