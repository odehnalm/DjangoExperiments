from django.core.management.base import BaseCommand

from ... import app
from apps.tasks import app as app_tasks


class Command(BaseCommand):
    help = "Almacena proxies en DB e inicia tarea periodica de actualizacion"

    def handle(self, *args, **options):
        """
        Procedimiento que almacena proxies en DB
        """
        print("Almacenando proxies en DB...")
        app.grabProxies()

        # Iniciar procedimiento periodico para actualizar DB
        print("Iniciando proceso recurrente...")
        app_tasks.cron_job(
            'default',
            app.grabProxies,
            "10 * * * *"
        )
