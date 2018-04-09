from django.conf import settings
from django.core.management.base import BaseCommand

from fake_useragent import UserAgent


class Command(BaseCommand):
    help = "Almacena UserAgents en json"

    def handle(self, *args, **options):
        print("ALMACENANDO LISTA DE CABECERAS PARA 'USER AGENT'...")
        UserAgent(path=settings.PATH_FAKE_USER_AGENT)
        print("HECHO")
