class Store(object):
    """ Categoria de producto

    """

    DARTY = "1"
    KELKOO = "2"
    BOULANGER = "3"
    PRICERUNNER = "4"
    RUEDUCOMMERCE = "5"
    GROUPDIGITAL = "6"
    AMAZON = "7"
    MEDIAMARKT = "8"
    PRODUCTSCOMPARE = "9"

    def __init__(self,
                 list_stores=[DARTY]):

        self.stores = list_stores
