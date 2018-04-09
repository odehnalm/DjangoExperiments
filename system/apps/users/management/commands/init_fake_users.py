from django.core.management.base import BaseCommand

from ...models import User
from apps.ma_companies.models import MaCompany


class Command(BaseCommand):
    help = "Almacena usuarios de prueba en DB"

    def handle(self, *args, **options):
        """
        Procedimiento que almacena usuarios de prueba en DB
        """
        print("Creando usuarios de prueba...")

        axa = MaCompany.objects.get(name="AXA")
        allianz = MaCompany.objects.get(name="ALLIANZ")

        user_frances1, created = User.objects.get_or_create(
            username='frances_1',
            first_name="fran",
            last_name="ces 1",
            email='frances_1@fakegmail.com'
        )

        if created:
            user_frances1.set_password('passFrances1')
            user_frances1.save()

            user_frances1.emailaddress_set.get_or_create(
                user=user_frances1,
                email=user_frances1.email,
                verified=True,
                primary=True
            )

            user_frances1.profile.company = axa
            user_frances1.profile.save()

        user_frances2, created = User.objects.get_or_create(
            username='frances_2',
            first_name="fran",
            last_name="ces 2",
            email='frances_2@fakegmail.com'
        )

        if created:
            user_frances2.set_password('passFrances2')
            user_frances2.save()

            user_frances2.emailaddress_set.get_or_create(
                user=user_frances2,
                email=user_frances2.email,
                verified=True,
                primary=True
            )

            user_frances2.profile.company = allianz
            user_frances2.profile.save()

        user_espanol1, created = User.objects.get_or_create(
            username='espanol_1',
            first_name="espa",
            last_name="nol 1",
            email='espanol_1@fakegmail.com'
        )

        if created:
            user_espanol1.set_password('passEspanol1')
            user_espanol1.save()

            user_espanol1.emailaddress_set.get_or_create(
                user=user_espanol1,
                email=user_espanol1.email,
                verified=True,
                primary=True
            )

            user_espanol1.profile.language = 'es'
            user_espanol1.profile.company = axa
            user_espanol1.profile.save()

        user_espanol2, created = User.objects.get_or_create(
            username='espanol_2',
            first_name="espa",
            last_name="nol 2",
            email='espanol_2@fakegmail.com'
        )

        if created:
            user_espanol2.set_password('passEspanol2')
            user_espanol2.save()

            user_espanol2.emailaddress_set.get_or_create(
                user=user_espanol2,
                email=user_espanol2.email,
                verified=True,
                primary=True
            )

            user_espanol2.profile.language = 'es'
            user_espanol2.profile.company = allianz
            user_espanol2.profile.save()

        print("HECHO")
