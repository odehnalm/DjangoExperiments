from ..constants import ITEM_CATEGORIES
from .helpers import (
    xlsx_cava_vino, xlsx_congelador, xlsx_laptop,
    xlsx_mobile, xlsx_refrigerador, xlsx_refrigerador_combi,
    xlsx_tv)


def xlsx_generator(req_xlsx_gen):

    xlsx_bytes = []

    # form_type = req_url_gen_store["form_type"]
    item_category = req_xlsx_gen["item_category"]

    if ITEM_CATEGORIES["LAPTOP"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_laptop(req_xlsx_gen))

    elif ITEM_CATEGORIES["TELEVISOR"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_tv(req_xlsx_gen))

    elif ITEM_CATEGORIES["REFRIGERADOR"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_refrigerador(req_xlsx_gen))

    elif ITEM_CATEGORIES["REFRIGERADOR_COMBINADO"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_refrigerador_combi(req_xlsx_gen))

    elif ITEM_CATEGORIES["CONGELADOR"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_congelador(req_xlsx_gen))

    elif ITEM_CATEGORIES["CAVA_DE_VINO"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_cava_vino(req_xlsx_gen))

    elif ITEM_CATEGORIES["MOVIL"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_mobile(req_xlsx_gen))

    elif ITEM_CATEGORIES["LAVADORA"] == item_category:

        # Proceder a generar XLSX
        raise NotImplementedError

    elif ITEM_CATEGORIES["SECADORA"] == item_category:

        # Proceder a generar XLSX
        raise NotImplementedError
    else:
        raise RuntimeError("XLSX-GENERATOR: error en Categoria de Producto")

    return xlsx_bytes
