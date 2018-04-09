# -*- coding: utf-8 -*-
import json
import pandas as pd

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import MaBrand, MaItemType, MaModel


class Command(BaseCommand):
    help = "Procedimiento que almacena categorias, marcas e identificadores de modelos en DB"

    def handle(self, *args, **options):
        """
        Procedimiento que almacena categorias, marcas e
        identificadores de modelos en DB
        """
        print("ALMACENANDO CATEGORIAS, MARCAS Y MODELOS...")

        # Primero desde sitio web externo
        if settings.EXTERNAL_API_ITEMS == "GFK":

            pass

            # d_csv = pd.read_csv(settings.PATH_DATA_GFK, encoding="utf-8")

            # d_csv = d_csv[( -d_csv["pg_name"].isin(["Réfrigérateur", "Congélateur", "Téléphones", "Téléphones Mobiles / Smartphones", "Télévision", "Ordinateurs Portables"]))]

            # for pg_name, pg_id, brand_name, brand_id in d_csv.values:

            #     item_type, created = MaItemType.objects.get_or_create(
            #         id_item_type="c" + str(pg_id),
            #         name_item_type=pg_name
            #     )

            #     brand, created = MaBrand.objects.get_or_create(
            #         id_brand=brand_id,
            #         name_brand=brand_name
            #     )

            #     item_type.brands.add(brand)
        else:
            raise NotImplementedError

        # Ahora el resto de las categorias manuales
        item_type, created = MaItemType.objects.get_or_create(
            id_item_type="TV_000",
            name_item_type="Television"
        )

        brand, created = MaBrand.objects.get_or_create(
            name_brand="LG"
        )

        item_type.brands.add(brand)

        model, created = MaModel.objects.get_or_create(
            id_model="55EG9A7V",
            brand=brand
        )

        model, created = MaModel.objects.get_or_create(
            id_model="OLED65E7V",
            brand=brand
        )

        model, created = MaModel.objects.get_or_create(
            id_model="OLED55B7V",
            brand=brand
        )

        model, created = MaModel.objects.get_or_create(
            id_model="75UJ675V",
            brand=brand
        )

        model, created = MaModel.objects.get_or_create(
            id_model="24MT49DF",
            brand=brand
        )

        print("HECHO")
