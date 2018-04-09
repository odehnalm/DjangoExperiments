class Engine(object):
    """ Motor de valoracion de producto

    """

    SUBSTITUTION_SIMILAR = "1"
    REPARATION_BAREMO = "2"
    SUBSTITUTION_SEGUNDA_MANO = "3"
    REPARATION_ML = "4"
    GFK = "5"

    def __init__(self,
                 list_types=[SUBSTITUTION_SIMILAR],
                 list_names=None):

        self.types = list_types
        self.names = list_names
