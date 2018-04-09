from django.core.management.base import BaseCommand

from ...models import MaCompany


class Command(BaseCommand):
    help = "Almacena companias de prueba en DB"

    def handle(self, *args, **options):
        """
        Procedimiento que almacena companias de prueba en DB
        """
        print("Creando companias de prueba...")

        axa, created = MaCompany.objects.get_or_create(
        	name="AXA",
        	country="fr",
        )

       	allianz, created = MaCompany.objects.get_or_create(
        	name="ALLIANZ",
        	country="es",
        )

        print("HECHO")