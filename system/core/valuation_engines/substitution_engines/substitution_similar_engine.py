import importlib
from uuid import uuid4

from django.conf import settings

from scrapyd_api import ScrapydAPI

from apps.scrapy_app.crawler import crawler_process
from repository import Repository

scrapyd = ScrapydAPI('http://localhost:6800')


def valuation_start(req_data_engine):

    resp_dict_stores = req_data_engine['stores']

    # Datos de tiendas a revisar
    dict_data_stores = {}

    # Por cada tienda, se genera la tarea correspondiente
    for store_id, store_name in resp_dict_stores["stores"].items():

        try:
            WEBSTORES_MODULE = settings.WEBSTORES_MODULE
        except AttributeError:
            raise AttributeError(
                "Debe definir en el archivo "
                "settings la variable WEBSTORES_MODULE")

        try:

            mod_app = importlib.import_module(
                WEBSTORES_MODULE + "." + store_name + ".app", __package__)

            mod_scraper = importlib.import_module(
                WEBSTORES_MODULE + "." + store_name + ".scraper", __package__)

            mod_url_gen = importlib.import_module(
                WEBSTORES_MODULE + "." + store_name + ".url_generator",
                __package__)

        except ModuleNotFoundError:
            raise ModuleNotFoundError("La tienda %s no existe" % store_name)

        # TEMPORARY(leonel77.3@gmail.com): aun no defino si sera requerido
        # el parametro "form_type"

        # # Peticion de tipo de form segun el tipo de bien y pais
        # req_form_type = {
        #     "_type": "reqformtype",
        #     "name": "peticion de tipo de formulario a usar "
        #             "para generar url de busqueda",
        #     "country": req_data_engine["country"],
        #     "item_category": req_data_engine["item_category"],
        # }

        # # Conexion a repositorio
        # resp_form_type = repository.get_form_type(
        #     req_form_type
        # )

        req_url_gen_store = {
            "_type": "requrlgeneratorstore",
            "name": "peticion de url generada a partir del item, el pais "
                    "y los datos de formulario",
            "country": req_data_engine["country"],
            "item_category": req_data_engine["item_category"],
            # "form_type": resp_form_type["form_type"],
            "data": req_data_engine["data"]
        }

        # Se pasan los parametros contenidos en
        # req_data_engine.data por la funcion generadora de la url
        url = mod_url_gen.url_generator(req_url_gen_store)
        allowed_domain = mod_app.get_domain()
        robots_OK = mod_app.robots_OK()
        name_scraper = mod_scraper.__name__

        dict_data_stores[name_scraper] = {
            "url": url,
            "allowed_domain": allowed_domain,
            "robots_OK": robots_OK,
            "store_id": store_id
        }

        try:
            if settings.SCRAPY_CRAWLERS_CONTROL_API:
                # Here we schedule a new crawling task from scrapyd.
                # Notice that settings is a special argument name.
                # But we can pass other arguments, though.
                # This returns a ID which belongs and will be belong to
                # this taskWe are goint to use that to check task's status.

                # Crea ID unico de la tarea
                job_id = str(uuid4())

                settings_scrapy = {
                    'job_id': job_id,
                    'USER_AGENT': "Mozilla/5.0 (compatible; Googlebot/2.1;"
                                  " +http://www.google.com/bot.html)"
                }

                task = scrapyd.schedule(
                    'default', 'basic_spider',
                    settings=settings_scrapy, url=url,
                    allowed_domain=allowed_domain,
                    name_scraper=name_scraper)

        except AttributeError:
            raise AttributeError(
                "Debe definir en el archivo "
                "settings la variable SCRAPY_CRAWLERS_CONTROL_API")

    dict_data_stores["job_id"] = req_data_engine["job_id"]

    # Instancia de repositorio
    type_repository = Repository.LOCAL_DB
    repository = Repository(type_repository=type_repository)
    repository.set_urls_generated(dict_data_stores.copy())

    dict_data_stores["item_category"] = req_data_engine["item_category"]
    dict_data_stores["country"] = req_data_engine["country"]

    # ---- Crawler process
    crawler_process(dict_data_stores)
