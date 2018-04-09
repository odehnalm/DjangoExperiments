from django.core.management.base import BaseCommand

from apps.scrapy_app.crawler import benchmarks_crawler


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        """
        """
        print("Iniciando creacion de json de cpus y gpus...")
        benchmarks_crawler()
        print("HECHO")
