from django.conf import settings

import rq

from apps.stores.xlsx_generator import app as app_xlsx
from .objects.engine import Engine
from .valuation_engines import app as app_engines
from .valuation_engines.gfk import app as app_gfk
from .valuation_engines.gfk.xlsx_generator import app as app_xlsx_gfk
from repository import Repository


def xlsx_generator(req_xlsx_gen):
    xlsx_templates = []
    engines = req_xlsx_gen["engines"]
    if Engine.GFK in engines:
        results = req_xlsx_gen["results"]
        req_xlsx_gen["results"] = next(
            (result for result in results if "result_gfk" in result),
            None
        )
        xlsx_templates.extend(app_xlsx_gfk.xlsx_generator(req_xlsx_gen))
    if Engine.SUBSTITUTION_SIMILAR in engines:
        xlsx_templates.extend(app_xlsx.xlsx_generator(req_xlsx_gen))

    return xlsx_templates


def init_valuation(data_task):

    job = rq.get_current_job()
    data_task["job_id"] = job.id

    type_repository = Repository.LOCAL_DB
    repository = Repository(type_repository=type_repository)

    # Crea Job para realizar seguimiento
    repository.create_job(job.id)

    if data_task["item_category"][0] == 'c':
        data_task["item_category"] = data_task["item_category"][1:]

    repository.set_type_repository(Repository.FILE_JSON)

    # Peticion de lista de motores segun el tipo de bien y pais
    req_list_engines = {
        "_type": "reqlistengines",
        "name": "peticion de lista de motores segun tipo de bien y pais",
        "country": data_task["country"],
        "item_category": data_task["item_category"]
    }

    # Conexion a repositorio
    resp_list_engines = repository.get_list_engines(
        req_list_engines
    )

    # Preparar peticion de valoraciones
    req_data_engines = {
        "_type": "reqdataengines",
        "name": "peticion de resultados a motores de "
                "valorizacion según tipo de bien y pais",
        "job_id": data_task["job_id"],
        "country": data_task["country"],
        "item_category": data_task["item_category"],
        "form_type": data_task["form_type"],
        "engines": resp_list_engines["engines"],
        "data": data_task["data"],
    }

    # Con lista, hacer peticion para obtener valoracion
    # por cada tipo de motor
    results = app_engines.valuation(req_data_engines)

    req_xlsx_gen = {
        "_type": "reqxlsxgen",
        "name": "peticion para generar xlsx "
                "según tipo de bien y pais",
        "job_id": data_task["job_id"],
        "country": data_task["country"],
        "item_category": data_task["item_category"],
        "results": results,
        "engines": resp_list_engines["engines"],
        "data": data_task["data"],
    }
    # Luego que se pasa por todos los motores, se procede
    # a generar el archivo excel con el contenido acumulado

    xlsx_templates = xlsx_generator(req_xlsx_gen)

    # Eliminar de la base de datos contenido aplicado a la
    # generacion de xlsx
    # repository.set_type_repository(Repository.LOCAL_DB)
    # repository.delete_data_by_field("job_id", data_task["job_id"])

    try:
        EXPORT_DATA_TO_EXTERNAL_HOST = settings.EXPORT_DATA_TO_EXTERNAL_HOST
        API_PRIMARY = settings.API_PRIMARY
    except AttributeError:
        raise AttributeError(
            "Debe definir en el archivo "
            "settings la variable EXPORT_DATA_TO_EXTERNAL_HOST"
            " o API_PRIMARY")

    if EXPORT_DATA_TO_EXTERNAL_HOST:
        if not xlsx_templates:
            raise ValueError("No existen datos para exportar")

        # Actualizo fuente de repositorio
        repository.set_type_repository(Repository.API_EXTERNAL)

        for xlsx_bytes in xlsx_templates:

            if xlsx_bytes is not None:

                req_put_data = {
                    "_type": "reqputdata",
                    "name": "peticion para guardar data "
                            "según tipo de repositorio",
                    "job_id": data_task["job_id"],
                    "data": xlsx_bytes
                }

                repository.save_data(req_put_data, API_PRIMARY)


def ma_temp_models(data_task):

    job = rq.get_current_job()
    data_task["job_id"] = job.id

    type_repository = Repository.LOCAL_DB
    repository = Repository(type_repository=type_repository)

    # Crea Job para realizar seguimiento
    repository.create_job(job.id)

    # Obtenemos modelos desde API de GFK
    models = app_gfk.get_models_by_name(data_task)

    req_put_data = {
        "_type": "reqputdata",
        "name": "peticion para guardar data "
                "según tipo de repositorio",
        "job_id": data_task["job_id"],
        "data": models
    }

    repository.set_temp_models(req_put_data)
