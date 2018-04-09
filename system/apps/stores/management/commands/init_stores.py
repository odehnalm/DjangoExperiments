from django.core.management.base import BaseCommand

from ...models import Store


class Command(BaseCommand):
    help = "Almacena tiendas en DB"

    def handle(self, *args, **options):
        """
        Procedimiento que almacena tiendas en DB
        """
        # FIXME (leonellima@protonmail.com):
        # Crear metodo robusto para almacenar de forma
        # dinamica tiendas, segun su ID y el pais al cual
        # aplican
        print("Iniciando creacion de tiendas...")
        Store.objects.get_or_create(
            store_id="1",
            nombre="darty",
        )
        Store.objects.get_or_create(
            store_id="2",
            nombre="kelkoo",
        )
        Store.objects.get_or_create(
            store_id="3",
            nombre="boulanger",
        )
        Store.objects.get_or_create(
            store_id="4",
            nombre="pricerunner",
        )
        Store.objects.get_or_create(
            store_id="5",
            nombre="rueducommerce",
        )
        Store.objects.get_or_create(
            store_id="6",
            nombre="groupdigital",
        )
        Store.objects.get_or_create(
            store_id="7",
            nombre="amazon",
        )
        Store.objects.get_or_create(
            store_id="8",
            nombre="mediamarkt",
        )
        Store.objects.get_or_create(
            store_id="9",
            nombre="productscompare",
        )
        print("HECHO")
