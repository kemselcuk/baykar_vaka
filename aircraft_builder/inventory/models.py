from django.db import models
from django.utils import timezone
from aircraft.models import ProducedAircraft, AIRCRAFT_CHOICES

PART_TYPES = [
    ('KANAT', 'Kanat'),
    ('GOVDE', 'Gövde'),    # Code uses 'GOVDE' but view looks for 'GÖVDE'
    ('KUYRUK', 'Kuyruk'),
    ('AVIYONIK', 'Aviyonik'), # Code uses 'AVIYONIK' but view looks for 'AVİYONİK'
]

class PartStock(models.Model):
    part_type = models.CharField(max_length=20, choices=PART_TYPES)
    aircraft_type = models.CharField(max_length=20, choices=AIRCRAFT_CHOICES)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('part_type', 'aircraft_type')

    def __str__(self):
        return f"{self.aircraft_type} {self.part_type} (Toplam: {self.quantity})"

class Part(models.Model):
    part_type = models.CharField(max_length=20, choices=PART_TYPES)
    aircraft_type = models.CharField(max_length=20, choices=AIRCRAFT_CHOICES)
    serial_number = models.CharField(max_length=50, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.aircraft_type} {self.part_type} SN:{self.serial_number}"

    def use_part(self):
        stock = PartStock.objects.get(part_type=self.part_type, aircraft_type=self.aircraft_type)
        if stock.quantity < 1:
            raise ValueError("Yeterli stok yok.")
        stock.quantity -= 1
        stock.save()

class UsedPart(models.Model):
    produced_aircraft = models.ForeignKey(ProducedAircraft, on_delete=models.CASCADE, related_name='used_parts')
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='used_in_aircrafts')
    used_quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.part.use_part()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produced_aircraft} için kullanılan {self.part.part_type} ({self.used_quantity} adet)"