from uuid import uuid4

from django.conf import settings
from django.utils import translation
from django.utils.translation import ugettext as _
from django.utils.translation.trans_real import DjangoTranslation
from django.views.i18n import JSONCatalog

import django_rq
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from apps.tasks import app as app_tasks
from core import app
from repository import Repository


class ResultsValuation(APIView):

    renderer_classes = (JSONRenderer,)

    def get(self, request, job_id, format=None):

        type_repository = Repository.APP_LOCAL

        # Instancia de repositorio
        repository = Repository(type_repository=type_repository)

        req_check_data = {
            "_type": "reqcheckdata",
            "name": "peticion para existencia de datos "
                    "a partir de identificador",
            "job_id": job_id
        }

        job_status = repository.check_status_job(job_id)

        if job_status["is_failed"]:
            return Response(
                {'status': 'failed'}
            )

        if job_status["is_finished"]:

            if settings.EXPORT_DATA_TO_EXTERNAL_HOST:

                repository.set_type_repository(Repository.API_EXTERNAL)

                try:
                    API_PRIMARY = settings.API_PRIMARY
                except AttributeError:
                    raise AttributeError(
                        "Debe definir en el archivo "
                        "settings la variable API_PRIMARY")

                file_exist = repository.check_data(req_check_data, API_PRIMARY)

                if file_exist:

                    req_get_url = req_check_data.copy()
                    repository.set_type_repository(Repository.APP_LOCAL)
                    presigned_url = repository.get_data_url(
                        req_get_url, API_PRIMARY)

                    repository.set_type_repository(Repository.LOCAL_DB)
                    job_data = repository.get_full_data_job(req_get_url)
                    repository.delete_data_by_field("job_id", job_id)

                    return Response(
                        {'existe_excel': True,
                         'status': 'completed',
                         'url': presigned_url,
                         'job_data': job_data})
            else:

                # repository.set_type_repository(Repository.APP_LOCAL)

                file_exist = repository.check_data(req_check_data)

                if file_exist:

                    req_get_url = req_check_data.copy()
                    repository.set_type_repository(Repository.LOCAL_DB)
                    job_data = repository.get_full_data_job(req_get_url)
                    repository.delete_data_by_field("job_id", job_id)

                    return Response(
                        {'existe_excel': True,
                         'status': 'completed',
                         'url': '#',
                         'job_data': job_data})

            return Response({'existe_excel': False, 'status': 'completed'})

        else:
            return Response({'existe_excel': False, 'status': 'in_progress'})

    def post(self, request, format=None):

        print("REQUEST USER")
        print(request.session['prueba'])

        user = request.user

        # Crea estructura para argumento de la tarea
        data_task = {
            "_type": "datatask",
            "name": "Coleccion de datos para ejecutar tarea",
            "job_id": "",
            "country": user.profile.company.country,
            "language": user.profile.language,
            "item_category": request.data["item_category"],
            "form_type": request.data["form_type"],
            "data": request.data["data"],
        }

        job_id = app_tasks.enqueue_task(
            'default', app.init_valuation, data_task)

        return Response(
            {'job_id': job_id, 'status': 'OK'}
        )


results_valuation = ResultsValuation.as_view()


class UrlsGenerated(APIView):

    renderer_classes = (JSONRenderer,)

    def get(self, request, job_id, format=None):

        type_repository = Repository.LOCAL_DB

        # Instancia de repositorio
        repository = Repository(type_repository=type_repository)

        req_urls = {
            "_type": "requrls",
            "name": "peticion para existencia de urls "
                    "a partir de identificador",
            "job_id": job_id
        }

        urls = repository.get_and_destroy_urls_generated(req_urls)

        if urls:
            return Response(
                {'existe_urls': True,
                 'urls': urls})
        else:
            return Response(
                {'existe_urls': False})


urls_generated = UrlsGenerated.as_view()


class ModelsByBrand(APIView):

    renderer_classes = (JSONRenderer,)

    def post(self, request, format=None):

        # Crea estructura para argumento de la tarea
        data_task = {
            "_type": "datatask",
            "name": "Coleccion de datos para ejecutar tarea",
            "job_id": "",
            "country": request.data["country"],
            "item_category": request.data["item_category"],
            "form_type": request.data["form_type"],
            "data": request.data["data"],
        }

        job_id = app_tasks.enqueue_task(
            'default', app.ma_temp_models, data_task)

        return Response(
            {'job_id': job_id, 'status': 'OK'}
        )

    def get(self, request, job_id, format=None):

        type_repository = Repository.APP_LOCAL
        repository = Repository(type_repository=type_repository)

        job_status = repository.check_status_job(job_id)

        if job_status["is_failed"]:
            return Response(
                {'status': 'failed'}
            )

        if job_status["is_finished"]:

            repository.set_type_repository(Repository.LOCAL_DB)

            req_ma_temp_models = {
                "_type": "reqmatempmodels",
                "name": "peticion de modelos temporales "
                        "a partir de identificador de job",
                "job_id": job_id
            }

            models = repository.get_and_destroy_temp_models(req_ma_temp_models)

            if models:
                return Response(
                    {'exist_models': True,
                     'models': models,
                     'status': 'completed'}
                )

            else:
                return Response(
                    {'exist_models': False, 'status': 'completed'}
                )

        else:
            return Response(
                {'exist_models': False, 'status': 'in_progress'}
            )


models_by_brand = ModelsByBrand.as_view()


class JSONTranslate(APIView):

    renderer_classes = (JSONRenderer,)

    def get(self, request, lang, format=None):

        translation.activate(lang)

        translates = {
            'prueba1': _("modelos de Producto GFK")
        }

        return Response(
            {'translates': translates}
        )


json_translate = JSONTranslate.as_view()
# class CustomJSONCatalog(JSONCatalog):
#     def get(self, request, lang, *args, **kwargs):
#         translation.activate(lang)
#         locale = translation.get_language()
#         domain = kwargs.get('domain', self.domain)
#         # If packages are not provided, default to all installed packages, as
#         # DjangoTranslation without localedirs harvests them all.
#         packages = kwargs.get('packages', '')
#         packages = packages.split('+') if packages else self.packages
#         paths = self.get_paths(packages) if packages else None
#         self.translation = DjangoTranslation(
#             locale, domain=domain, localedirs=paths)
#         context = self.get_context_data(**kwargs)
#         return self.render_to_response(context)


# json_catalog = CustomJSONCatalog.as_view(domain="djangojs")
