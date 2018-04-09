import importlib
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


from django.conf import settings

from apps.tasks.models import Job


def get_list_cpus(filtros, should_print):

    """
    Retorna lista de cpus a partir de cpu seleccionado por
    cliente
    """

    procesador = filtros["CPUSpec"]
    mejores_series = []

    if procesador:
        # ....................................
        # PREPARANDO TABLA

        # Lectura de JSON
        CPU_bench = pd.read_json(
            settings.BASE_DIR + '/system/data/CPU_Benchmark.json',
            orient='index').transpose()

        # Hacemos numérica la columna del score
        CPU_bench[['item_mark']] = CPU_bench[['item_mark']].apply(pd.to_numeric)

        # Ordenamos por el score de mayor a menor
        CPU_bench = CPU_bench.sort_values(by=['item_mark'], ascending=False)

        # ....................................
        # BUSCANDO MEJORES SERIES
        # Localizamos la posicion que tiene nuestro CPU
        ranking_CPU = np.where(CPU_bench["modelo"] == procesador)[0][0]
        print("Localizacion del CPU: {0}".format(ranking_CPU))

        # Localizamos las series de los procesadores que están por encima
        mejores_series = list(CPU_bench["serie"][0:ranking_CPU].unique())

    if should_print:
        print("Series de CPUs: ", mejores_series)
        print(type(mejores_series))

    return mejores_series


def post_filter(req_post_filter_data):

    job_id = req_post_filter_data["job_id"]

    resp_dict_stores = req_post_filter_data['stores']

    # <<<<<<<<<<<<<
    # EXTRACCION DE DATOS DE DB
    # <<<<<<<<<<<<<
    job = Job.objects.get(_job_id=job_id)
    products = job.substitution_similar_results.all()

    list_data_items = []

    req_post_filter_by_store = {
        "_type": "reqpostfilterbystore",
        "name": "peticion para realizar filtro de datos extraidos"
                " según tipo de bien y pais",
        "country": req_post_filter_data["country"],
        "item_category": req_post_filter_data["item_category"],
        "form_type": req_post_filter_data["form_type"],
        "data": req_post_filter_data["data"]
    }

    # Por cada tienda, se realiza el filtro correspondiente
    for store_id, store_name in resp_dict_stores["stores"].items():

        try:
            WEBSTORES_MODULE = settings.WEBSTORES_MODULE
        except AttributeError:
            raise AttributeError(
                "Debe definir en el archivo "
                "settings la variable WEBSTORES_MODULE")

        try:

            mod_filter = importlib.import_module(
                WEBSTORES_MODULE + "." + store_name + ".filter", __package__)

        except ModuleNotFoundError:
            raise ModuleNotFoundError("La tienda %s no existe" % store_name)

        query_products = products.filter(store_id=store_id)

        req_post_filter_by_store['query_products'] = query_products

        list_data_items.extend(mod_filter.filter(req_post_filter_by_store))

    return list_data_items


def better_bench_cpu(input_benchs):

    #Inicializamos diccionario a retornar
    post_hardware = {
        'CPU' : {
            'modelo' : '',
            'es_valido' : True
        }
    }

    # Nuestra tolerancia, el hardware tiene que ser lo más idéntico posible
    thresh = 90

    #....................................
    # PREPARANDO TABLA

    # Lectura de JSON

    CPU_bench = pd.read_json(
        settings.BASE_DIR + '/system/data/CPU_Benchmark.json',
        orient='index').transpose()

    # Hacemos numérica la columna del score

    CPU_bench[['item_mark']] = CPU_bench[['item_mark']].apply(pd.to_numeric)

    # Ordenamos por el score de mayor a menor

    CPU_bench = CPU_bench.sort_values(by=['item_mark'], ascending=False)


    CPU_list = CPU_bench['modelo'].tolist()

    #....................................
    # BUSCANDO MEJORES SERIES CPU

    candidate_CPU = process.extract(input_benchs['procesador_raw'], CPU_list)[0]

    CPU_search_accuracy = candidate_CPU[1]

    # MEJORES SERIES CPU

    if CPU_search_accuracy < thresh:
        post_hardware['CPU']['modelo'] = input_benchs['procesador_raw']
        post_hardware['CPU']['es_valido'] = True
    else:
        # Localizamos la posicion que tiene nuestro CPU
        try:
            ranking_CPU = np.where(CPU_bench["modelo"] == input_benchs['procesador'])[0][0]  
            ranking_candidate_CPU = np.where(CPU_bench["modelo"] == candidate_CPU[0])[0][0]
            # Verificamos si el ranking del cpu candidato es mejor que el del form
            if ranking_candidate_CPU <= ranking_CPU:
                post_hardware['CPU']['modelo'] = candidate_CPU[0]
                post_hardware['CPU']['es_valido'] = True
            else:
                post_hardware['CPU']['modelo'] = candidate_CPU[0]
                post_hardware['CPU']['es_valido'] = False
        except Exception as xc:
            post_hardware['CPU']['modelo'] = input_benchs['procesador_raw']
            post_hardware['CPU']['es_valido'] = True  

    return post_hardware


def better_bench_gpu(input_benchs):

    #Inicializamos diccionario a retornar
    post_hardware = {
        'GPU' : {
            'modelo' : '',
            'es_valido' : True
        }
    }

    # Nuestra tolerancia, el hardware tiene que ser lo más idéntico posible
    thresh = 90

    #....................................
    # PREPARANDO TABLA

    # Lectura de JSON

    GPU_bench = pd.read_json(
        settings.BASE_DIR + '/system/data/GPU_Benchmark.json',
        orient='index').transpose()

    # Hacemos numérica la columna del score

    GPU_bench[['item_mark']] = GPU_bench[['item_mark']].apply(pd.to_numeric)

    # Ordenamos por el score de mayor a menor

    GPU_bench = GPU_bench.sort_values(by=['item_mark'], ascending=False)


    GPU_list = GPU_bench['modelo'].tolist()

    #....................................
    # BUSCANDO MEJORES SERIES (CPU/GPU)

    candidate_GPU = process.extract(input_benchs['graficos_raw'], GPU_list)[0]

    GPU_search_accuracy = candidate_GPU[1]

    # MEJORES SERIES GPU

    if GPU_search_accuracy < thresh:
        post_hardware['GPU']['modelo'] = input_benchs['graficos_raw']
        post_hardware['GPU']['es_valido'] = True
    else:
        # Localizamos la posicion que tiene nuestro CPU
        try:
            ranking_GPU = np.where(GPU_bench["modelo"] == input_benchs['graficos'])[0][0]  
            ranking_candidate_GPU = np.where(GPU_bench["modelo"] == candidate_GPU[0])[0][0]
            # Verificamos si el ranking del gpu candidato es mejor que el del form
            if ranking_candidate_GPU <= ranking_GPU:
                post_hardware['GPU']['modelo'] = candidate_GPU[0]
                post_hardware['GPU']['es_valido'] = True
            else:
                post_hardware['GPU']['modelo'] = candidate_GPU[0]
                post_hardware['GPU']['es_valido'] = False
        except Exception as xc:
            post_hardware['GPU']['modelo'] = input_benchs['graficos_raw']
            post_hardware['GPU']['es_valido'] = True

    return post_hardware    