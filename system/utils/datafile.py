import json

from django.conf import settings


def engines_for_item(
        req_list_engines,
        path_file=settings.PATH_ITEMS_BY_ENGINE):

    list_engines = []
    item_category = req_list_engines['item_category']

    with open(path_file) as json_data:
        dict_data = json.load(json_data)

        for engine_key, item_keys in dict_data.items():

            if item_category in item_keys.keys():
                list_engines.append(engine_key)

    return list_engines


def stores_for_item_country(
        req_list_stores,
        path_file=settings.PATH_ITEMS_BY_STORE):

    dict_stores = {}
    item_category = req_list_stores['item_category']
    country_ID = req_list_stores['country']

    with open(path_file) as json_data:
        dict_data = json.load(json_data)

        data_by_country = dict_data.get(country_ID, None)

        if data_by_country is not None:

            for store_id, store_values in data_by_country["stores"].items():

                if item_category in store_values["items"].keys():

                    dict_stores[store_id] = store_values["name"]

    return dict_stores


def form_type_by_item(
        req_form_type,
        path_file=settings.PATH_FORM_TYPE_BY_ITEM):

    form_type = ""
    item_category = req_form_type['item_category']

    with open(path_file) as json_data:
        dict_data = json.load(json_data)

        for _category, body in dict_data.items():

            if _category == item_category:

                form_type = body["form_type"]
                break
    return form_type
