from uuid import uuid4

from django.shortcuts import render

from apps.tasks import app as app_tasks
from apps.scrapy_app import proxies
from core import app
from repository import Repository


def home(request):

    # TEST
    requests_rv = []

    # TELEVISION
    # request_rv = {
    #     "_type": "reqrv",
    #     "name": "Peticion de cliente para valoracion de producto",
    #     "country": "1",
    #     "item_category": 'TV_000',
    #     "form_type": 'TV_000',
    #     "data": [{
    #         "3D": "Non",
    #         "AutresMarques": "Non",
    #         "Couleur": "Noir",
    #         "Design": [
    #            "Plat"
    #         ],
    #         "Energy": "A+",
    #         "Framerate": [
    #            "60"
    #         ],
    #         "HDR": [],
    #         "Indice_refresh": "400",
    #         "Internet": "Oui",
    #         "Marque": "Samsung",
    #         "Modele": "55MU6645",
    #         "PannelType": [
    #           "IPS"
    #         ],
    #         "Ratio": [
    #           "16:9"
    #         ],
    #         "Refresh": "100",
    #         "Resolution": [
    #           "1080p"
    #         ],
    #         "Smart": "Oui",
    #         "TailleCm": "102",
    #         "TaillePounce": "40",
    #         "Type": "LED",
    #         "Wifi": "Oui"
    #     }]
    # }
    request_rv = {'_type': 'datatask', 'name': 'Coleccion de datos para ejecutar tarea', 'country': '1', 'item_category': 'TV-000', 'form_type': 'TV-000', 'data': [{'Marque': 'Samsung', 'Modele': 'UE65K58000', 'TaillePounce': '55', 'TailleCm': '140', 'Type': 'LED', 'Resolution': ['1080p'], 'Refresh': '', 'Indice_refresh': '', '3D': '', 'HDR': [''], 'Internet': 'Oui', 'Wifi': 'oUI', 'Smart': '', 'Ratio': [''], 'Couleur': '', 'PannelType': [''], 'Framerate': [''], 'Design': [''], 'Energy': ''}]}
    requests_rv.append(request_rv.copy())

    # NEVERAS
    # request_rv = {
    #     "_type": "reqrv",
    #     "name": "Peticion de cliente para valoracion de producto",
    #     "country": "1",
    #     "item_category": 'FRIGO_000',
    #     "form_type": 'FRIGO_000',
    #     "data": [{
    #         'Marque': 'La Sommeliere',
    #         'Modele': 'CVD102DZ',
    #         'Type': 'Cave a vin',
    #         'Subtype': 'Multi-temperatures',
    #         'Hateur': '128',
    #         'Largeur': '55',
    #         'Profoundeur': '57',
    #         'Volume': '203',
    #         'TypePose': 'Pose libre',
    #         'Couleur': 'Noir',
    #         'Energy': 'C',
    #     }]
    # }

    request_rv = {'_type': 'datatask', 'name': 'Coleccion de datos para ejecutar tarea', 'country': '1', 'item_category': 'FRIGO-000', 'form_type': 'FRIGO-000', 'data': [{'Marque': 'Haier', 'Modele': '', 'Type': 'Réfrigétateur combiné', 'Subtype': 'Americain', 'Hateur': 'null', 'Largeur': 'null', 'Profoundeur': 'null', 'Volume': 'null', 'TypePose': '', 'Couleur': '', 'Energy': ''}]}
    requests_rv.append(request_rv.copy())

    # TELEFONOS
    # request_rv = {
    #     "_type": "reqrv",
    #     "name": "Peticion de cliente para valoracion de producto",
    #     "country": "1",
    #     "item_category": 'TLF_000',
    #     "form_type": 'TLF_000',
    #     "data": [{
    #         'Type': 'Mobile',
    #         'Marque': 'Asus',
    #         'Modele': 'ZenFone 3',
    #         'Systeme dexploitation': 'Android',
    #         'Taille': '4.7',
    #         'Resolution': '1920 X1080',
    #         'Memoire': '64',
    #         'Ram': '4',
    #         'Coeurs': '8',
    #         'MegapixelsFrontale': '7',
    #         'MegapixelsArriere': '16',
    #         'Couleur': 'Noir',
    #         'CapaciteBatterie': '3000',
    #         'Date achat': '2016-10-06',
    #         'Prix achat': '379'
    #     }]
    # }

    # requests_rv.append(request_rv.copy())

    type_repository = Repository.LOCAL_DB
    repository = Repository(type_repository=type_repository)

    for request_ in requests_rv:

        # Crea Job para realizar seguimiento
        job_id = repository.create_job()

        # Crea estructura para argumento de la tarea
        data_task = {
            "_type": "datatask",
            "name": "Coleccion de datos para ejecutar tarea",
            "job_id": job_id,
            "country": request_["country"],
            "item_category": request_["item_category"],
            "form_type": request_["form_type"],
            "data": request_["data"],
        }

        app_tasks.enqueue_task(
            'default', app.init_valuation, data_task)

    return render(request, 'index.html')
