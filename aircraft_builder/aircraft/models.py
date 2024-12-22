from django.db import models

AIRCRAFT_CHOICES = [
    ('TB2', 'TB2'),
    ('TB3', 'TB3'),
    ('AKINCI', 'AKINCI'),
    ('KIZILELMA', 'KIZILELMA'),
]

class ProducedAircraft(models.Model):
    aircraft_type = models.CharField(max_length=20, choices=AIRCRAFT_CHOICES)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.aircraft_type} - {self.pk}"
