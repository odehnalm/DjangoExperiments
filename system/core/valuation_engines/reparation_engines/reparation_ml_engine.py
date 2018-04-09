import random

from core.objects.item_category import ItemCategory

from repository import Repository


def valuation_start(req_data_engine):

    type_repository = Repository.LOCAL_DB

    # Instancia de repositorio
    repository = Repository(type_repository=type_repository)

    item_category = req_data_engine["item_category"]

    # NOTE: PLAN B

    std_deviation = random.randrange(100) - 50

    if ItemCategory.LAPTOP == item_category:
        media = 400
    elif ItemCategory.REFRIGERADOR == item_category or\
            ItemCategory.REFRIGERADOR_COMBINADO == item_category or\
            ItemCategory.CONGELADOR == item_category or\
            ItemCategory.CAVA_DE_VINO == item_category:
        media = 361
    elif ItemCategory.TELEVISOR == item_category:
        media = 396
    else:
        raise TypeError("El tipo de categoria es incorrecto")

    repository.set_reparation_ml_value(
        req_data_engine["job_id"],
        media + std_deviation
    )
