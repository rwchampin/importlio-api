from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Populates the model tables with initial data"

    def handle(self, *args, **options):
        # Your population logic here
        self.stdout.write("Populating data...")
        # Perform the necessary data population
        self.stdout.write("Data population complete.")
