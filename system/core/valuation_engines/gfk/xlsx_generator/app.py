from .constants import ITEM_CATEGORIES
from .helpers import (
    xlsx_lave_linge, xlsx_lave_vaisselle, xlsx_lecteur_dvd,
    xlsx_plaques_de_cuisson, xlsx_radio_reveil, xlsx_seche_linge,
    xlsx_projecteurs, xlsx_aspirateurs, xlsx_mini_fours,
    xlsx_kits_oreillette, xlsx_casques, xlsx_tablette,
    xlsx_camescopes, xlsx_moniteurs, xlsx_robots,
    xlsx_consoles_de_jeu, xlsx_hottes
)


def xlsx_generator(req_xlsx_gen):

    xlsx_bytes = []

    # form_type = req_url_gen_store["form_type"]
    item_category = req_xlsx_gen["item_category"]

    if ITEM_CATEGORIES["LAVE_LINGE"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_lave_linge(req_xlsx_gen))

    elif ITEM_CATEGORIES["LECTEUR_DVD"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_lecteur_dvd(req_xlsx_gen))

    elif ITEM_CATEGORIES["DATA/VIDEO_PROJECTEURS"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_projecteurs(req_xlsx_gen))

    elif ITEM_CATEGORIES["ASPIRATEURS"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_aspirateurs(req_xlsx_gen))

    elif ITEM_CATEGORIES["MINI_FOURS"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_mini_fours(req_xlsx_gen))

    elif ITEM_CATEGORIES["TABLETTE"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_tablette(req_xlsx_gen))

    elif ITEM_CATEGORIES["KITS_OREILLETTE"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_kits_oreillette(req_xlsx_gen))

    elif ITEM_CATEGORIES["CASQUES"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_casques(req_xlsx_gen))

    elif ITEM_CATEGORIES["CAMESCOPES"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_camescopes(req_xlsx_gen))

    elif ITEM_CATEGORIES["MONITEURS"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_moniteurs(req_xlsx_gen))

    elif ITEM_CATEGORIES["ROBOTS"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_robots(req_xlsx_gen))

    elif ITEM_CATEGORIES["HOTTES"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_hottes(req_xlsx_gen))

    elif ITEM_CATEGORIES["SECHE_LINGE"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_seche_linge(req_xlsx_gen))

    elif ITEM_CATEGORIES["PLAQUES_DE_CUISSON"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_plaques_de_cuisson(req_xlsx_gen))

    elif ITEM_CATEGORIES["CONSOLES_DE_JEU"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_consoles_de_jeu(req_xlsx_gen))

    elif ITEM_CATEGORIES["LAVE_VAISSELLE"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_lave_vaisselle(req_xlsx_gen))

    elif ITEM_CATEGORIES["RADIO/RADIO_REVEIL"] == item_category:

        # Proceder a generar XLSX
        xlsx_bytes.append(xlsx_radio_reveil(req_xlsx_gen))
    else:
        raise RuntimeError("XLSX-GENERATOR: error en Categoria de Producto")

    return xlsx_bytes
