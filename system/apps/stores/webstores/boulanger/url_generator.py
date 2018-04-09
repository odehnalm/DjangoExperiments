from django.conf import settings

from ...adapter import get_list_cpus
from ...constants import ITEM_CATEGORIES, FORM_TYPES
from .helpers import (
    urlgen_cava_de_vino, urlgen_congelador, urlgen_laptop,
    urlgen_mobile, urlgen_refrigerador, urlgen_refrigerador_combinado)


def url_generator(req_url_gen_store):

    # form_type = req_url_gen_store["form_type"]
    item_category = req_url_gen_store["item_category"]

    try:
        should_print = settings.SHOULD_PRINT_DEBUG
    except AttributeError:
        raise AttributeError(
            "Debe definir en el archivo "
            "settings la variable SHOULD_PRINT_DEBUG")

    filtros = req_url_gen_store["data"][0]

    url = ""

    if ITEM_CATEGORIES["LAPTOP"] == item_category:

        # Proceder a generar url
        filtros["list_cpus"] = get_list_cpus(filtros, should_print)
        url = urlgen_laptop(filtros, should_print)

    elif ITEM_CATEGORIES["TELEVISOR"] == item_category:

        # Proceder a generar url
        raise NotImplementedError

    elif ITEM_CATEGORIES["REFRIGERADOR"] == item_category:

        # Proceder a generar url
        url = urlgen_refrigerador(filtros, should_print)

    elif ITEM_CATEGORIES["REFRIGERADOR_COMBINADO"] == item_category:

        # Proceder a generar url
        url = urlgen_refrigerador_combinado(filtros, should_print)

    elif ITEM_CATEGORIES["CONGELADOR"] == item_category:

        # Proceder a generar url
        url = urlgen_congelador(filtros, should_print)

    elif ITEM_CATEGORIES["CAVA_DE_VINO"] == item_category:

        # Proceder a generar url
        url = urlgen_cava_de_vino(filtros, should_print)

    elif ITEM_CATEGORIES["MOVIL"] == item_category:

        # Proceder a generar url
        url = urlgen_mobile(filtros, should_print)

    elif ITEM_CATEGORIES["LAVADORA"] == item_category:

        # Proceder a generar url
        raise NotImplementedError

    elif ITEM_CATEGORIES["SECADORA"] == item_category:

        # Proceder a generar url
        raise NotImplementedError
    else:

        raise RuntimeError("URL-GENERATOR: error en Categoria de Producto")

    return url
