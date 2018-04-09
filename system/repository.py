import os.path

from django.conf import settings

from django_rq import get_connection
from rq.job import Job as rq_Job

from apps.aws import app as app_aws
from apps.items.models import Item
from apps.stores.models import Store
from apps.tasks.models import Job
from core.repository_interface import RepositoryInterface
from utils import datafile


class Repository(RepositoryInterface):

    LOCAL_DB = 1
    EXTERNAL_DB = 2
    FILE_CSV = 3
    FILE_JSON = 4
    FILE_PDF = 5
    FILE_TXT = 6
    APP_LOCAL = 7
    API_EXTERNAL = 8

    GET = 1
    POST = 2

    def __init__(self, type_repository=LOCAL_DB, method_api=None):
        self.type = type_repository
        self.method_api = method_api

    def set_type_repository(self, new_type_repository):
        self.type = new_type_repository

    def set_method_api(self, new_method_api):
        self.method_api = new_method_api

    def _get_object_info(self, path, data_request=None, **kwargs):
        """Retorna contenido 'en crudo' de una fuente descrita por path

        Dependiendo de la 'fuente', retorna el contenido solicitado sin
        formateo alguno.

        Args:
            path (str): ruta al 'deposito' de datos
            data_request (:obj:'dict', optional): datos requeridos por la
                peticion. Pueden ser parametros de autenticacion, configuracion
                o datos extra
            **kwargs: argumentos extra, entre ellos:
                - headers (dict)
                - timeout (float)

        Returns:
            'dict' o Query.

            - 'dict': Si la fuente es externa, el formato sera:
                {'data': 'dict', 'status_code': 'int'}

        Raises:

            En caso de conexiones a interfaces externas:

                requests.exceptions.TooManyRedirects:
                requests.exceptions.RequestException:
                ...
                (Ver requests.exceptions para otros posibles eventos,
                excepto Timeout, HTTPError y ConnectionError, los cuales se
                gestionan manualmente)

        """
        pass

    def get_list_engines(self, req_list_engines):
        if self.FILE_JSON == self.type:
            list_engines = datafile.engines_for_item(req_list_engines)
            return {
                "_type": "reslistengines",
                "name": "lista de motores segun tipo de bien y pais",
                "country": req_list_engines["country"],
                "item_category": req_list_engines["item_category"],
                "engines": list_engines
            }
        else:
            # NOTE(leonellima@protonmail.com): queda como pendiente si se
            # llega a necesitar
            raise NotImplementedError

    def get_dict_stores(self, req_list_stores):
        if self.FILE_JSON == self.type:
            dict_stores = datafile.stores_for_item_country(req_list_stores)
            return {
                "_type": "resliststores",
                "name": "lista de tiendas a usar para busqueda "
                        "segun tipo de bien y pais",
                "country": req_list_stores["country"],
                "item_category": req_list_stores["item_category"],
                "engine": req_list_stores["engine"],
                "stores": dict_stores
            }
        else:
            # NOTE(leonellima@protonmail.com): queda como pendiente si se
            # llega a necesitar
            raise NotImplementedError

    def get_form_type(self, req_form_type):
        if self.FILE_JSON == self.type:
            form_type = datafile.form_type_by_item(req_form_type)
            return {
                "_type": "resformtype",
                "name": "tipo de formulario a usar "
                        "para generar url de scraping",
                "country": req_form_type["country"],
                "item_category": req_form_type["item_category"],
                "form_type": form_type
            }
        else:
            # NOTE(leonellima@protonmail.com): queda como pendiente si se
            # llega a necesitar
            raise NotImplementedError

    def get_data_url(self, req_get_url, API_TYPE=None):
        if self.APP_LOCAL == self.type:
            if settings.API_PRIMARY == API_TYPE:
                job_id = req_get_url["job_id"]

                # TODO(leonellima@protonmail.com): Debo integrar logica
                # para pasar la extension del archivo

                filename = "xlsx_" + job_id + ".xlsx"
                return app_aws.get_data_url(filename)

        else:
            # NOTE(leonellima@protonmail.com): queda como pendiente si se
            # llega a necesitar
            raise NotImplementedError

    def get_and_destroy_urls_generated(self, req_urls):
        if self.LOCAL_DB == self.type:
            urls = []
            job = Job.objects.get(pk=req_urls["job_id"])
            if job.urls_generated.exists():
                urls.extend(list(job.urls_generated.values_list(
                    "url", flat=True)))
                job.urls_generated.all().delete()
            return urls
        else:
            # NOTE(leonellima@protonmail.com): queda como pendiente si se
            # llega a necesitar
            raise NotImplementedError

    def get_full_data_job(self, req_full_data):
        if self.LOCAL_DB == self.type:

            job_data = []
            job = Job.objects.get(pk=req_full_data["job_id"])

            if job.substitution_similar_results.exists():

                precios = []
                for r in job.substitution_similar_results.all().values_list(
                        'tiendas', flat=True):
                    if isinstance(r, list):
                        for res_tienda in r:

                            value = res_tienda["precio"].replace("EUR", "")

                            value = value.replace(" ", "")
                            value = value.replace("\xa0", "")

                            print('VALUE FINAL')
                            print(value)

                            precios.append(float(value))
                    else:

                        value = r["precio"].replace("EUR", "")

                        value = value.replace(" ", "")
                        value = value.replace("\xa0", "")

                        precios.append(float(value))

                job_data.append({"precio_minimo": min(precios)})
                job_data.append({"precios": precios})

            if job.reparation_sh_results.exists():

                value = job.reparation_sh_results.get().value

                job_data.append(
                    {"resultado_segunda_mano": float("{0:.2f}".format(value))}
                )

            if job.reparation_ml_results.exists():

                value = job.reparation_ml_results.get().value

                job_data.append(
                    {"resultado_reparation": value}
                )

            if job.reparation_baremo_results.exists():

                value = job.reparation_baremo_results.get().value

                job_data.append(
                    {"resultado_reparation_baremo": value}
                )

            if job.ma_temp_models.exists():

                models = list(job.ma_temp_models.all().values(
                    'id_model', 'name_model'))

                job.ma_temp_models.all().delete()

                job_data.append(
                    {"ma_temp_models": models}
                )

            return job_data

        else:
            # NOTE(leonellima@protonmail.com): queda como pendiente si se
            # llega a necesitar
            raise NotImplementedError

    def check_data(self, req_check_data, API_TYPE=None):
        if self.API_EXTERNAL == self.type:
            if settings.API_PRIMARY == API_TYPE:
                job_id = req_check_data["job_id"]

                # TODO(leonellima@protonmail.com): Debo integrar logica
                # para pasar la extension del archivo

                filename = "xlsx_" + job_id + ".xlsx"
                return app_aws.check_data_on_aws(filename)

        elif self.APP_LOCAL == self.type:
            job_id = req_check_data["job_id"]
            filename = "xlsx_" + job_id + ".xlsx"
            path = settings.TMP_FOLDER + "/" + filename
            return os.path.isfile(path)
        else:
            # NOTE(leonellima@protonmail.com): queda como pendiente si se
            # llega a necesitar
            raise NotImplementedError

    def check_status_job(self, job_id):
        if self.APP_LOCAL == self.type:
            redis_conn = get_connection()
            _job = rq_Job.fetch(job_id, redis_conn)
            return {
                'is_finished': _job.is_finished,
                'is_failed': _job.is_failed,
            }
        else:
            # NOTE(leonellima@protonmail.com): queda como pendiente si se
            # llega a necesitar
            raise NotImplementedError

    def get_and_destroy_temp_models(self, req_temp_models):
        if self.LOCAL_DB == self.type:
            return self.get_full_data_job(req_temp_models)
        else:
            # NOTE(leonellima@protonmail.com): queda como pendiente si se
            # llega a necesitar
            raise NotImplementedError

    def save_data(self, req_put_data, API_TYPE=None):
        if self.API_EXTERNAL == self.type:
            if settings.API_PRIMARY == API_TYPE:
                job_id = req_put_data["job_id"]

                # TODO(leonellima@protonmail.com): Debo integrar logica para
                # detectar que tipo de archivo es y asignar extension

                filename = "xlsx_" + job_id + ".xlsx"
                app_aws.put_data_to_aws(filename, req_put_data["data"])
        else:
            # NOTE(leonellima@protonmail.com): queda como pendiente si se
            # llega a necesitar
            raise NotImplementedError

    def save_items(self, list_data_items):
        if self.LOCAL_DB == self.type:
            for item in list_data_items:
                store = Store.objects.get(store_id=item["store_id"])
                Item.objects.create(
                    store=store,
                    category_id=item["category_id"],
                    nombre=item["name"]
                )
        else:
            # NOTE(leonellima@protonmail.com): queda como pendiente si se
            # llega a necesitar
            raise NotImplementedError

    def create_job(self, job_id):
        if self.LOCAL_DB == self.type:
            Job.objects.create(_job_id=job_id)
        else:
            # NOTE(leonellima@protonmail.com): queda como pendiente si se
            # llega a necesitar
            raise NotImplementedError

    def set_second_hand_value(self, job_id, value):
        if self.LOCAL_DB == self.type:
            # TODO(leonellima@protonmail.com): buscar la forma de
            # independizar metodo del modelo
            job = Job.objects.get(pk=job_id)
            job.reparation_sh_results.create(value=value)
        else:
            # NOTE(leonellima@protonmail.com): queda como pendiente si se
            # llega a necesitar
            raise NotImplementedError

    def set_reparation_ml_value(self, job_id, value):
        if self.LOCAL_DB == self.type:
            # TODO(leonellima@protonmail.com): buscar la forma de
            # independizar metodo del modelo
            job = Job.objects.get(pk=job_id)
            job.reparation_ml_results.create(value=value)
        else:
            # NOTE(leonellima@protonmail.com): queda como pendiente si se
            # llega a necesitar
            raise NotImplementedError

    def set_urls_generated(self, res_urls):
        if self.LOCAL_DB == self.type:
            job_id = res_urls.pop("job_id")
            job = Job.objects.get(pk=job_id)
            for name, body in res_urls.items():
                job.urls_generated.create(url=body["url"])
        else:
            # NOTE(leonellima@protonmail.com): queda como pendiente si se
            # llega a necesitar
            raise NotImplementedError

    def set_reparation_baremo_value(self, job_id, value):
        if self.LOCAL_DB == self.type:
            # TODO(leonellima@protonmail.com): buscar la forma de
            # independizar metodo del modelo
            job = Job.objects.get(pk=job_id)
            job.reparation_baremo_results.create(value=value)
        else:
            # NOTE(leonellima@protonmail.com): queda como pendiente si se
            # llega a necesitar
            raise NotImplementedError

    def set_temp_models(self, req_put_data):
        if self.LOCAL_DB == self.type:
            job_id = req_put_data["job_id"]
            job = Job.objects.get(pk=job_id)
            models = req_put_data["data"]
            if models:
                for model in models:
                    job.ma_temp_models.create(
                        id_model=model['Id'],
                        name_model=model['Value']
                    )
        else:
            # NOTE(leonellima@protonmail.com): queda como pendiente si se
            # llega a necesitar
            raise NotImplementedError

    def delete_data_by_field(self, field, value):
        if self.LOCAL_DB == self.type:
            # TODO(leonellima@protonmail.com): buscar la forma de
            # independizar metodo del modelo
            Job.objects.get(pk=value).delete()
        else:
            # NOTE(leonellima@protonmail.com): queda como pendiente si se
            # llega a necesitar
            raise NotImplementedError
