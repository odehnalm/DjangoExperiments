from django.conf import settings
from requests import Session
from zeep import Client
from zeep.transports import Transport


def get_client():
    session = Session()
    session.cert = settings.PATH_CERT
    transport = Transport(session=session)
    client = Client(
        'https://claimmanager.gfk.com/WebService/ClaimManagerServices.asmx?WSDL',
        transport=transport)
    return client


def get_models_by_name(data_task):

    pg_id = data_task['item_category'].split("c")[-1]
    brand_id = data_task['data'][0]["Marque"]
    string_search = data_task['data'][0]["Modele"]

    if not string_search:
        string_search = "?"

    client = get_client()

    product_by_name = client.service.getProductByName(pg_id, brand_id, string_search)

    print(product_by_name)

    if product_by_name["ValueIdPairs"]:

        return product_by_name["ValueIdPairs"]['ValueIdPair']

    return None
