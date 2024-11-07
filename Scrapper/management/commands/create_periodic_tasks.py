# yourapp/management/commands/create_periodic_tasks.py
from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

class Command(BaseCommand):
    help = 'Sets up periodic tasks for scraping Amazon products'

    def handle(self, *args, **kwargs):
        schedule, _ = IntervalSchedule.objects.get_or_create(every=6, period=IntervalSchedule.HOURS)

        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Scrape Amazon Products for All Brands',
            task='Scrapper.tasks.scrape_products_for_all_brands',
            args=json.dumps([]),
        )
        self.stdout.write(self.style.SUCCESS('Periodic task created or already exists'))
