from django.core.management.base import BaseCommand
from teams.models import Team

class Command(BaseCommand):
    help = 'Creates initial teams'

    def handle(self, *args, **kwargs):
        initial_teams = [
            ('Kanat Takımı', 'KANAT'),
            ('Gövde Takımı', 'GOVDE'),
            ('Kuyruk Takımı', 'KUYRUK'),
            ('Aviyonik Takımı', 'AVIYONIK'),
            ('Montaj Takımı', 'MONTAJ'),
        ]

        for team_name, responsible_part in initial_teams:
            team, created = Team.objects.get_or_create(
                name=team_name,
                defaults={'responsible_part': responsible_part}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created team "{team_name}"')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Team "{team_name}" already exists')
                )