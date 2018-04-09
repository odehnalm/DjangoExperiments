# import the logging library
import logging

from apps.stores import adapter
from .gfk import engine as gfk_engine
from ..objects.engine import Engine
from .reparation_engines import (
    reparation_baremo_engine,
    reparation_ml_engine)
from repository import Repository
from .substitution_engines import (
    substitution_similar_engine,
    substitution_second_hand_engine)

# Get an instance of a logger
logger = logging.getLogger(__name__)


def valuation(req_data_engines):

    results_valuation = []

    engines = req_data_engines["engines"]

    req_data_engine = {
        "_type": "reqdataengine",
        "name": "peticion de resultados a motor de valorizacion"
                " en especifico, según tipo de bien y pais",
        "job_id": req_data_engines["job_id"],
        "country": req_data_engines["country"],
        "item_category": req_data_engines["item_category"],
        "form_type": req_data_engines["form_type"],
        "data": req_data_engines["data"],
    }

    if Engine.SUBSTITUTION_SIMILAR in engines:

        # Actualizado tipo de calculadora
        req_data_engine["engine"] = Engine.SUBSTITUTION_SIMILAR

        # Instancia de repositorio
        type_repository = Repository.FILE_JSON
        repository = Repository(type_repository=type_repository)

        # Peticion de lista de tiendas segun el tipo de bien y pais
        req_list_stores = {
            "_type": "reqliststores",
            "name": "peticion de lista de tiendas a usar para busqueda, "
                    "segun tipo de bien y pais",
            "country": req_data_engine["country"],
            "item_category": req_data_engine["item_category"],
            "engine": req_data_engine["engine"]
        }

        # Conexion a repositorio
        resp_dict_stores = repository.get_dict_stores(
            req_list_stores
        )

        if resp_dict_stores["stores"]:

            req_data_engine['stores'] = resp_dict_stores

            # Procedimiento para valoracion de items similares
            substitution_similar_engine.valuation_start(req_data_engine)

            # Post procesamiento de datos extraidos
            req_post_filter_data = {
                "_type": "reqdatapostfilter",
                "name": "peticion para realizar filtro de datos extraidos"
                        " según tipo de bien y pais",
                "job_id": req_data_engines["job_id"],
                "country": req_data_engines["country"],
                "item_category": req_data_engines["item_category"],
                "form_type": req_data_engines["form_type"],
                "stores": resp_dict_stores,
                "data": req_data_engines["data"],
            }

            list_data_items = adapter.post_filter(req_post_filter_data)

            repository.set_type_repository(Repository.LOCAL_DB)
            repository.save_items(list_data_items)

    if Engine.REPARATION_BAREMO in engines:
        req_data_engine["engine"] = Engine.REPARATION_BAREMO
        reparation_baremo_engine.valuation_start(req_data_engine)

    if Engine.SUBSTITUTION_SEGUNDA_MANO in engines:
        req_data_engine["engine"] = Engine.SUBSTITUTION_SEGUNDA_MANO
        substitution_second_hand_engine.valuation_start(req_data_engine)

    if Engine.REPARATION_ML in engines:
        req_data_engine["engine"] = Engine.REPARATION_ML
        reparation_ml_engine.valuation_start(req_data_engine)

    if Engine.GFK in engines:
        req_data_engine["engine"] = Engine.GFK
        results_valuation.append(gfk_engine.valuation_start(req_data_engine))

    return results_valuation
