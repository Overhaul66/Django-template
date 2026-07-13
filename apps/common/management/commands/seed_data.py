from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates a small starter seed state for a reusable Django template."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Template seed command completed."))
        self.stdout.write("Add your own seed logic for the domain you are building.")
