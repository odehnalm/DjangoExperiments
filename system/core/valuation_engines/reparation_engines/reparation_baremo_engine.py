from django.conf import settings

import pandas as pd

from repository import Repository


def valuation_start(req_data_engine):

    filtros = req_data_engine["data"][0]

    marque = filtros['Marque'].capitalize()
    modele = filtros['Modele']

    if not marque and not modele:
        return

    # Test request
    dict_test = {
        'item_category': 'TLF-000',
        'data': [{
            'Marque': 'Apple',
            'Modele': 'iPhone 6 Plus',
            'Reparation': ['Ecran', 'Batterie']
        }]
    }

    category = dict_test['item_category']
    if category == 'TLF-000':
        type_item = 'Mobile'

    # marque = dict_test['data'][0]['Marque']

    modele2 = modele + " "
    modeles = [modele, modele2]
    reparations = dict_test['data'][0]['Reparation']

    # Lectura de Fichero excel
    dr_csv = pd.read_csv(settings.PATH_DIC_REPARATION, encoding="ISO-8859-1")
    ca_csv = pd.read_csv(settings.PATH_CAPTAIN, encoding="ISO-8859-1")
    co_csv = pd.read_csv(settings.PATH_CORDON, encoding="ISO-8859-1")
    a_csv = pd.read_csv(settings.PATH_ANGELO, encoding="ISO-8859-1")
    di_csv = pd.read_csv(settings.PATH_DIL, encoding="ISO-8859-1")
    s_csv = pd.read_csv(settings.PATH_SAVE, encoding="ISO-8859-1")

    ca_code_checked = False
    co_code_checked = False
    a_code_checked = False
    di_code_checked = False
    s_code_checked = False

    # Codigos a partir de lista de tipos de reparacion
    codes = dr_csv[(dr_csv['Reparation'].isin(reparations))]['Ref']

    # --------- Captain
    try:
        # Columna de cabecera 'Type'
        type_col = ca_csv['Type']

        # Se reduce la lista a aquellos del tipo indicado
        new_rows = ca_csv[(type_col == type_item)]

        # A partir de la nueva lista, se busca columna de marcas
        marque_col = new_rows['Marque']

        # Se reduce la lista a aquellos con la marca indicada
        new_rows = new_rows[(marque_col == marque)]

    except ValueError:

        raise ValueError("Posible error en marca")

    if not (new_rows.empty or new_rows.isna().all().all()):

        try:
            # A partir de la nueva lista, se busca columna de modelos
            modele_col = new_rows['Modele']

            # Se reduce la lista a aquellos del modelo indicado
            new_rows = new_rows[(modele_col == modele)]

        except ValueError:

            raise ValueError("Posible error en modelo")

        if not (new_rows.empty or new_rows.isna().all().all()):

            try:
                # A partir de la nueva lista, se busca columna de codigos
                code_col = new_rows['CodeReparation']

                # Se reduce la lista a aquellos que coinciden con los codigos
                new_rows = new_rows[(code_col.isin(codes))]

                # Remover duplicados
                new_rows = new_rows.drop_duplicates(subset=["CodeReparation"])

                # Se han procesado los codigos
                ca_code_checked = True

            except ValueError:

                raise ValueError("Posible error en codigos de reparacion")

    if ca_code_checked and\
            not (new_rows.empty or new_rows.isna().all().all()) and\
            len(codes) == len(new_rows):
        reparations_captain = reparations

        tarif_captain = new_rows['Tarifs_TTC'].\
            str.replace(' \x80', '').\
            astype(float).sum()
    else:
        reparations_captain = "Indisponible"
        tarif_captain = 0.0

    # --------- Cordon
    tarif_swap_cordon = ''
    try:
        # Columna de cabecera 'Type'
        type_col = co_csv['Type']

        # Se reduce la lista a aquellos del tipo indicado
        new_rows = co_csv[(type_col == type_item)]

        # A partir de la nueva lista, se busca columna de marcas
        marque_col = new_rows['Marque']

        # Se reduce la lista a aquellos con la marca indicada
        new_rows = new_rows[(marque_col == marque)]

    except ValueError:

        raise ValueError("Posible error en marca")

    if not (new_rows.empty or new_rows.isna().all().all()):

        try:
            # A partir de la nueva lista, se busca columna de modelos
            modele_col = new_rows['Modele']

            # Se reduce la lista a aquellos del modelo indicado
            new_rows = new_rows[(modele_col == modele)]

        except ValueError:

            raise ValueError("Posible error en modelo")

        if not (new_rows.empty or new_rows.isna().all().all()):

            try:
                # A partir de la nueva lista, se busca columna de codigos
                code_col = new_rows['CodeReparation']

                # Tarif swap cordon
                tarif_swap_cordon = new_rows[(code_col == 'D26')]

                # Se reduce la lista a aquellos que coinciden con los codigos
                new_rows = new_rows[(code_col.isin(codes))]

                # Remover duplicados
                new_rows = new_rows.drop_duplicates(subset=["CodeReparation"])

                # Se han procesado los codigos
                co_code_checked = True

            except ValueError:

                raise ValueError("Posible error en codigos de reparacion")

    if co_code_checked and\
            not (new_rows.empty or new_rows.isna().all().all()) and\
            len(codes) == len(new_rows):
        reparations_cordon = reparations

        tarif_cordon = new_rows['Tarif_TTC'].\
            str.replace(' \x80', '').\
            astype(float).sum()

    else:
        reparations_cordon = "Indisponible"
        tarif_cordon = 0.0

    try:

        if not tarif_swap_cordon.empty:

            tarif_swap_cordon = tarif_swap_cordon['Tarif_TTC'].\
                str.replace(' \x80', '').\
                astype(float)

            if (tarif_swap_cordon < tarif_cordon).bool() or tarif_cordon == 0:
                reparations_cordon = ['Swap']
                tarif_cordon = tarif_swap_cordon.values[0]

    except AttributeError:
        print("TARIF SWAP CORDON EXCEPTION ATRIBUTEERROR")
        pass
    except NameError:
        print("TARIF SWAP CORDON EXCEPTION NAMEERROR")
        pass

    # --------- DIL
    tarif_swap_dil = ''
    try:
        # Columna de cabecera 'Type'
        type_col = di_csv['Type']

        # Se reduce la lista a aquellos del tipo indicado
        new_rows = di_csv[(type_col == type_item)]

        # A partir de la nueva lista, se busca columna de marcas
        marque_col = new_rows['Marque']

        # Se reduce la lista a aquellos con la marca indicada
        new_rows = new_rows[(marque_col == marque)]

    except ValueError:

        raise ValueError("Posible error en marca")

    if not (new_rows.empty or new_rows.isna().all().all()):

        try:
            # A partir de la nueva lista, se busca columna de modelos
            modele_col = new_rows['Modele']

            # Se reduce la lista a aquellos del modelo indicado
            new_rows = new_rows[(modele_col == modele)]

        except ValueError:

            raise ValueError("Posible error en modelo")

        if not (new_rows.empty or new_rows.isna().all().all()):

            try:
                # A partir de la nueva lista, se busca columna de codigos
                code_col = new_rows['CodeReparation']

                # Tarif swap dil
                tarif_swap_dil = new_rows[(code_col == 'D26')]

                # Se reduce la lista a aquellos que coinciden con los codigos
                new_rows = new_rows[(code_col.isin(codes))]

                # Remover duplicados
                new_rows = new_rows.drop_duplicates(subset=["CodeReparation"])

                # Se han procesado los codigos
                di_code_checked = True

            except ValueError:

                raise ValueError("Posible error en codigos de reparacion")

    if di_code_checked and\
            not (new_rows.empty or new_rows.isna().all().all()) and\
            len(codes) == len(new_rows):
        reparations_dil = reparations

        tarif_dil = new_rows['Tarif_HT'].\
            str.replace(' Û', '').\
            astype(float).sum() * 1.2

    else:
        reparations_dil = "Indisponible"
        tarif_dil = 0

    try:

        if not tarif_swap_dil.empty:

            tarif_swap_dil = tarif_swap_dil['Tarif_HT'].\
                str.replace(' Û', '').\
                astype(float)

            if (tarif_swap_dil < tarif_dil).bool() or tarif_dil == 0:
                reparations_dil = ['Swap']
                tarif_dil = tarif_swap_dil.values[0]

    except AttributeError:
        print("TARIF SWAP DIL EXCEPTION ATRIBUTEERROR")
        pass
    except NameError:
        print("TARIF SWAP DIL EXCEPTION NAMEERROR")
        pass

    # --------- Angelo
    try:
        # Columna de cabecera 'Type'
        type_col = a_csv['Type']

        # Se reduce la lista a aquellos del tipo indicado
        new_rows = a_csv[(type_col == type_item)]

        # A partir de la nueva lista, se busca columna de marcas
        marque_col = new_rows['Marque']

        # Se reduce la lista a aquellos con la marca indicada
        new_rows = new_rows[(marque_col == marque)]

    except ValueError:

        raise ValueError("Posible error en marca")

    if not (new_rows.empty or new_rows.isna().all().all()):

        try:
            # A partir de la nueva lista, se busca columna de modelos
            modele_col = new_rows['Modele']

            # Se reduce la lista a aquellos del modelo indicado
            new_rows = new_rows[(modele_col == modele)]

        except ValueError:

            raise ValueError("Posible error en modelo")

        if not (new_rows.empty or new_rows.isna().all().all()):

            try:
                # A partir de la nueva lista, se busca columna de codigos
                code_col = new_rows['CodeReparation']

                # Se reduce la lista a aquellos que coinciden con los codigos
                new_rows = new_rows[(code_col.isin(codes))]

                # Remover duplicados
                new_rows = new_rows.drop_duplicates(subset=["CodeReparation"])

                # Se han procesado los codigos
                a_code_checked = True

            except ValueError:

                raise ValueError("Posible error en codigos de reparacion")

    if a_code_checked and\
            not (new_rows.empty or new_rows.isna().all().all()) and\
            len(codes) == len(new_rows):
        reparations_angelo = reparations

        tarif_angelo_site = new_rows['Tarif_HT_Site'].\
            str.replace(' Û', '').\
            astype(float).sum()

        tarif_angelo_collecte = new_rows['Tarif_HT_Collecte'].\
            str.replace(' Û', '').\
            astype(float).sum()

        tarif_angelo_atelier = new_rows['Tarif_HT_Atelier'].\
            str.replace(' Û', '').\
            astype(float).sum()
    else:
        reparations_angelo = "Indisponible"
        tarif_angelo_site = 0.0
        tarif_angelo_collecte = 0.0
        tarif_angelo_atelier = 0.0

    # --------- Save
    try:
        # Columna de cabecera 'Type'
        type_col = s_csv['Type']

        # Se reduce la lista a aquellos del tipo indicado
        new_rows = s_csv[(type_col == type_item)]

        # A partir de la nueva lista, se busca columna de marcas
        marque_col = new_rows['Marque']

        # Se reduce la lista a aquellos con la marca indicada
        new_rows = new_rows[(marque_col == marque)]

    except ValueError:

        raise ValueError("Posible error en marca")

    if not (new_rows.empty or new_rows.isna().all().all()):

        try:
            # A partir de la nueva lista, se busca columna de modelos
            modele_col = new_rows['Modele']

            # Se reduce la lista a aquellos del modelo indicado
            new_rows = new_rows[(modele_col == modele)]

        except ValueError:

            raise ValueError("Posible error en modelo")

        if not (new_rows.empty or new_rows.isna().all().all()):

            try:
                # A partir de la nueva lista, se busca columna de codigos
                code_col = new_rows['CodeReparation']

                # Se reduce la lista a aquellos que coinciden con los codigos
                new_rows = new_rows[(code_col.isin(codes))]

                # Remover duplicados
                new_rows = new_rows.drop_duplicates(subset=["CodeReparation"])

                # Se han procesado los codigos
                s_code_checked = True

            except ValueError:

                raise ValueError("Posible error en codigos de reparacion")

    if s_code_checked and\
            not (new_rows.empty or new_rows.isna().all().all()) and\
            len(codes) == len(new_rows):
        reparations_save = reparations

        tarif_save = new_rows['Tarif_TTC'].\
            str.replace(' Û', '').\
            astype(float).sum()
    else:
        reparations_save = "Indisponible"
        tarif_save = 0.0

    type_repository = Repository.LOCAL_DB

    # Instancia de repositorio
    repository = Repository(type_repository=type_repository)

    repository.set_reparation_baremo_value(
        req_data_engine["job_id"],
        tarif_captain
    )

    print("VALORES")
    print("CAPTAIN:")
    print(tarif_captain)
    print(reparations_captain)
    print("SAVE:")
    print(tarif_save)
    print(reparations_save)
    print("CORDON:")
    print(tarif_cordon)
    print(reparations_cordon)
    print("DIL:")
    print(tarif_dil)
    print(reparations_dil)
    print("ANGELO:")
    print(tarif_angelo_site)
    print(tarif_angelo_collecte)
    print(tarif_angelo_atelier)
    print(reparations_angelo)
