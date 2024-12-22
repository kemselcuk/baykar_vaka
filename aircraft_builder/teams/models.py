from django.db import models

PART_TYPES = [
    ('KANAT', 'Kanat'),
    ('GÖVDE', 'Gövde'),    # Uses 'GÖVDE' instead of 'GOVDE'
    ('KUYRUK', 'Kuyruk'),
    ('AVİYONİK', 'Aviyonik'),  # Uses 'AVİYONİK' instead of 'AVIYONIK'
]

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    responsible_part = models.CharField(
        max_length=20, 
        choices=PART_TYPES + [('MONTAJ', 'Montaj')],
        null=True, blank=True
    )

    def __str__(self):
        return self.name
