from .app import get_client


def valuation_start(req_data_engine):

    client = get_client()

    # pg_id = req_data_engine['item_category']
    # brand_id = req_data_engine['data'][0]["Marque"]
    product_id = req_data_engine['data'][0]["Modele"]

    result_gfk = client.service.computeReplacementsOfProduct(
        '?', product_id)

    if result_gfk['ReplacementDevices'] is None:

        # Manual request created
        # manual_request_id = replacements_product['ManualRequestId']

        # TEMPORARY (leonellima@protonmail.com): DEBO MODIFICAR EL FLUJO
        # CUANDO TENGA MAS INFORMACION ACERCA DE QUE HAER CUANDO LA PETICION
        # NO TETORNE DATOS
        result_gfk = None

    return {"result_gfk": result_gfk}
