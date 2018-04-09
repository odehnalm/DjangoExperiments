from ...constants import ITEM_CATEGORIES
from .helpers import (filter_frigo, filter_mobile, filter_laptop)


def filter(req_post_filter_by_store):

    item_category = req_post_filter_by_store["item_category"]

    list_data_items_by_store = []

    query_products = req_post_filter_by_store["query_products"]
    filtros = req_post_filter_by_store["data"][0]

    if ITEM_CATEGORIES["LAPTOP"] == item_category:

        # Proceder a filtrar
        list_data_items_by_store.extend(filter_laptop(query_products, filtros))

    elif ITEM_CATEGORIES["TELEVISOR"] == item_category:

        raise NotImplementedError

    elif ITEM_CATEGORIES["REFRIGERADOR"] == item_category:

        # Proceder a filtrar
        pass

    elif ITEM_CATEGORIES["REFRIGERADOR_COMBINADO"] == item_category:

        # Proceder a filtrar
        pass

    elif ITEM_CATEGORIES["CONGELADOR"] == item_category:

        # Proceder a filtrar
        pass

    elif ITEM_CATEGORIES["CAVA_DE_VINO"] == item_category:

        # Proceder a filtrar
        pass

    elif ITEM_CATEGORIES["MOVIL"] == item_category:

        # Proceder a filtrar
        list_data_items_by_store.extend(filter_mobile(query_products))

    elif ITEM_CATEGORIES["LAVADORA"] == item_category:

        raise NotImplementedError

    elif ITEM_CATEGORIES["SECADORA"] == item_category:

        raise NotImplementedError
    else:

        raise RuntimeError("POST-FILTROS: error en Categoria de Producto")

    return list_data_items_by_store
