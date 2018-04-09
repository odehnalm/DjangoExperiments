class ItemCategory(object):
    """ Categoria de producto

    """

    LAPTOP = "COMPU_000"
    TELEVISOR = "TV_000"
    MOVIL = "TLF_000"
    LAVADORA = "5"
    SECADORA = "6"
    REFRIGERADOR = "FRIGO_000"
    REFRIGERADOR_COMBINADO = "FRIGO_001"
    CONGELADOR = "FRIGO_002"
    CAVA_DE_VINO = "FRIGO_003"

    def __init__(self,
                 list_categories=[LAPTOP]):

        self.categories = list_categories
