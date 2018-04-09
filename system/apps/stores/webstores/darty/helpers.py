# ------- GENERADORES DE URL
def urlgen_tv(filtros, should_print):

    fields = {
        'type': '',
        'marque': '',
        'taille': '',
        'resolution': '',
        'design' : ''
    }

    url_darty = 'https://www.darty.com/nav/extra/list?s=prix_asc'

    #MARCA
    if filtros['Marque'].upper() == 'PHILIPS':
        fields['marque'] = 'MP_philips_tv-PHILI'
    elif filtros['Marque'].upper() == 'MEDIAMARKET':
        fields['marque'] = 'MP_mediamarket'
    elif filtros['Marque'].upper() == 'SMART TECH':
        fields['marque'] = 'MP_smart_tech'
    else:
        try:
            fields['marque'] = filtros['Marque'].upper()[:5]
        except:
            fields['marque'] = filtros['Marque'].upper()

    # Type: categoria exclusiva, al no incluirla tenemos ambos productos LED y OLED
    # si no es OLED, aunque el filtro llegue vacío, así sale por defecto
    if filtros['Type'] == 'OLED':
        fields['type'] = '97056&fa=149552-292059'
    else:
        fields['type'] = '97056'

    # TAMANO DE PANTALLA
    if filtros['TaillePounce'] and str(filtros['TaillePounce'].replace(" ", "")) != "null" and\
            str(filtros['TaillePounce']).replace(" ", "") != "undefined" and filtros['TaillePounce'] != '0':
        # Taille: rango de pulgadas
        fields['taille'] = '-'.join(
            [str(pulgadas) + '0000321600' for pulgadas in range(int(filtros['TaillePounce']), 76)])

    # Resolution
    if '720p' in filtros['Resolution']:
        fields['resolution'] = '885093-mk_54112_11624652-1627160-1531132'
    elif '1080p' in filtros['Resolution']:
        fields['resolution'] = 'mk_54112_11624652-1627160-1531132'
    elif '4K' in filtros['Resolution'][0].upper():
        fields['resolution'] = '1627160-1531132'  # 4K Y 4K UHD

    # Design
    if 'Incurve' in filtros['Design'] or 'incurve' in filtros['Design']: fields['design'] = '367267'

    # ---- URL
    c_filter = '&c='
    if fields['taille']:
        c_filter = "-".join([c_filter,fields['taille']])
    if fields['resolution']:
        c_filter = "-".join([c_filter,fields['resolution']])
    if fields['design']:
        c_filter = "-".join([c_filter,fields['design']])
    url_darty += '&cat=' + fields['type']
    if fields['marque']:
        url_darty += '&m=' + fields['marque']
    if c_filter != '&c=':
        url_darty += c_filter        

    #Limpieza
    url_darty = url_darty.replace('=-','=').replace('--','-')

    url_darty += '&npk=1'

    #Limpieza
    url_darty = url_darty.replace('=-','=').replace('--','-')

    return url_darty


def urlgen_refrigerador(filtros, should_print):

    fields = {
        'subtype': '',
        'marque': '',
        'energy': '',
        'froid': '',
        'largeur': '',
        'c_filters' : [],
    }

    url_darty = 'https://www.darty.com/nav/extra/list?s=prix_asc'

    if filtros['Hateur'] == "null":
        filtros['Hateur'] = ""

    if filtros['Largeur'] == "null":
        filtros['Largeur'] = ""

    if filtros['Profoundeur'] == "null":
        filtros['Profoundeur'] = ""

    if filtros['Volume utile'] == "null":
        filtros['Volume utile'] = ""

    # MARQUE
    # OBS: EXISTEN ABREVIACIONES DISTINTAS
    if filtros['Marque'].upper() == 'CALIFORNIA': fields['marque'] = 'MP_california'
    elif filtros['Marque'].upper() == 'NODOR': fields['marque'] = 'MP_nodor'
    elif filtros['Marque'].upper() == 'KLARSTEIN': fields['marque'] = 'MP_klarstein'
    elif filtros['Marque'].upper() == 'LA SOMMELIERE': fields['marque'] = 'LASOM'
    elif filtros['Marque'].upper() == 'LE CHAI': fields['marque'] = 'LECHA'
    elif filtros['Marque'].upper() == 'ELECTROLUX': fields['marque'] = 'ELLUX'
    elif filtros['Marque'].upper() == 'DE DIETRICH': fields['marque'] = 'DEDIE'
    elif filtros['Marque'].upper() == 'ICYTECH': fields['marque'] = 'MP_icytech'
    elif filtros['Marque'].upper() == 'TECHNOLEC': fields['marque'] = 'TECNL'
    elif filtros['Marque'].upper() == 'MOULINEX STUDIO': fields['marque'] = 'MOSTU'
    elif filtros['Marque'].upper() == 'SOGELUX': fields['marque'] = 'MP_sogelux'
    else:
        if len(filtros['Marque']) >=5:
            fields['marque'] = filtros['Marque'].upper()[:5]
        else:
            fields['marque'] = filtros['Marque'].upper()
    # SUBTYPE
    if filtros['Subtype'] == 'Réfrigérateur compact':
        fields['subtype'] = '11601'
    else:
        fields['subtype'] = '23561'

    # LARGEUR
    if filtros['Largeur'] and str(filtros['Largeur'].replace(" ", "")) != "null" and\
            str(filtros['Largeur']).replace(" ", "") != "undefined" and filtros['Largeur'] != '0':
        # Taille: rango de pulgadas
        lower_large  = filtros['Largeur'].split("-")[0]
        upper_large  = filtros['Largeur'].split("-")[1]
        a = int(float(lower_large))*10
        b = int(float(upper_large))*10 + 1
        fields['largeur'] = '-'.join(
            [str(centimetros) + '000266616' for centimetros in range(a, b)])

    # SYSTEME DE FROID REFRIGERATEUR (VENTILE > BRASSE > STATIQUE)
    if filtros['Systeme de froid'] == 'Brassé':
        fields['froid'] = '1125294-1444895'
    elif filtros['Systeme de froid'] == 'Ventilé':
        fields['froid'] = '1125294'

    # ENERGY:
    if filtros['Energy'] == 'A+++':
        fields['energy'] = '1287037'
    elif filtros['Energy'] == 'A++':
        fields['energy'] = '1287037-883184'
    elif filtros['Energy'] == 'A+':
        fields['energy'] = '1287037-883184-1007875'
    elif filtros['Energy'] == 'A':
        fields['energy'] = '1287037-883184-1007875-883186'
    elif filtros['Energy'] == 'B':
        fields['energy'] = '883186-1287037-883184-1007875-889028'
    elif filtros['Energy'] == 'C':
        fields['energy'] = '883186-889028-1287037-883184-1007875-902412'
    elif filtros['Energy'] == 'D':
        fields['energy'] = '883186-889028-1287037-883184-1007875-902412-1311230'
    elif filtros['Energy'] == 'E':
        fields['energy'] = '883186-889028-1287037-883184-1007875-902412-1311230-1369604'



    # ---- URL
    c_filter = '&c='
    if fields['energy']:
        fields['c_filters'].append(fields['energy'])
    if fields['froid']:
        fields['c_filters'].append(fields['froid'])
    if fields['largeur']:
        fields['c_filters'].append(fields['largeur'])        
    url_darty += '&cat=' + fields['subtype']
    if fields['marque']:
        url_darty += '&m=' + fields['marque']           
    if fields['c_filters'] != []:
        url_darty += c_filter + "-".join(fields['c_filters'])         

    #Limpieza
    # url_darty = url_darty.replace('=-','=').replace('--','-')

    url_darty += '&npk=1'

    #Limpieza
    url_darty = url_darty.replace('=-','=').replace('--','-')

    return url_darty


def urlgen_refrigerador_combinado(filtros, should_print):
    
    fields = {
        'subtype': '',
        'marque': '',
        'energy': '',
        'froid': '',
        'largeur': '',
        'c_filters' : [],
        'froidcongelation' : ''
    }

    url_darty = 'https://www.darty.com/nav/extra/list?s=prix_asc'

    if filtros['Hateur'] == "null":
        filtros['Hateur'] = ""

    if filtros['Largeur'] == "null":
        filtros['Largeur'] = ""

    if filtros['Profoundeur'] == "null":
        filtros['Profoundeur'] = ""

    if filtros['Volume utile'] == "null":
        filtros['Volume utile'] = ""

    # MARQUE
    # OBS: EXISTEN ABREVIACIONES DISTINTAS
    if filtros['Marque'].upper() == 'CALIFORNIA': fields['marque'] = 'MP_california'
    elif filtros['Marque'].upper() == 'NODOR': fields['marque'] = 'MP_nodor'
    elif filtros['Marque'].upper() == 'KLARSTEIN': fields['marque'] = 'MP_klarstein'
    elif filtros['Marque'].upper() == 'LA SOMMELIERE': fields['marque'] = 'LASOM'
    elif filtros['Marque'].upper() == 'LE CHAI': fields['marque'] = 'LECHA'
    elif filtros['Marque'].upper() == 'ELECTROLUX': fields['marque'] = 'ELLUX'
    elif filtros['Marque'].upper() == 'DE DIETRICH': fields['marque'] = 'DEDIE'
    elif filtros['Marque'].upper() == 'ICYTECH': fields['marque'] = 'MP_icytech'
    elif filtros['Marque'].upper() == 'TECHNOLEC': fields['marque'] = 'TECNL'
    elif filtros['Marque'].upper() == 'MOULINEX STUDIO': fields['marque'] = 'MOSTU'
    elif filtros['Marque'].upper() == 'SOGELUX': fields['marque'] = 'MP_sogelux'
    else:
        if len(filtros['Marque']) >=5:
            fields['marque'] = filtros['Marque'].upper()[:5]
        else:
            fields['marque'] = filtros['Marque'].upper()

    # SUBTYPE
    if filtros['Subtype'] == 'Réfrigérateur américain':
        fields['subtype'] = '515'        
    elif filtros['Subtype'] == 'Réfrigérateur congélateur en bas':
        fields['subtype'] = '17001'
    elif filtros['Subtype'] == 'Réfrigérateur congélateur en haut':
        fields['subtype'] = '514'
    else:
        fields['subtype'] = '12448'

    # LARGEUR
    if filtros['Largeur'] and str(filtros['Largeur'].replace(" ", "")) != "null" and\
            str(filtros['Largeur']).replace(" ", "") != "undefined" and filtros['Largeur'] != '0':
        # Taille: rango de pulgadas
        lower_large  = filtros['Largeur'].split("-")[0]
        upper_large  = filtros['Largeur'].split("-")[1]
        a = int(float(lower_large))*10
        b = int(float(upper_large))*10 + 1
        fields['largeur'] = '-'.join(
            [str(centimetros) + '000266616' for centimetros in range(a, b)])

    # SYSTEME DE FROID REFRIGERATEUR (VENTILE > BRASSE > STATIQUE)
    if filtros['Type refrigeration'] == 'Brassé':
        fields['froid'] = '1125294-1444895'
    elif filtros['Type refrigeration'] == 'Ventilé':
        fields['froid'] = '1125294'

    # SYSTEME DE FROID CONGELATEUR
    if filtros['Type congelation'] == 'Ventilé':
        fields['froidcongelation'] = '1369547'

    # ENERGY:
    if filtros['Energy'] == 'A+++':
        fields['energy'] = '1287037'
    elif filtros['Energy'] == 'A++':
        fields['energy'] = '1287037-883184'
    elif filtros['Energy'] == 'A+':
        fields['energy'] = '1287037-883184-1007875'
    elif filtros['Energy'] == 'A':
        fields['energy'] = '1287037-883184-1007875-883186'
    elif filtros['Energy'] == 'B':
        fields['energy'] = '883186-1287037-883184-1007875-889028'
    elif filtros['Energy'] == 'C':
        fields['energy'] = '883186-889028-1287037-883184-1007875-902412'
    elif filtros['Energy'] == 'D':
        fields['energy'] = '883186-889028-1287037-883184-1007875-902412-1311230'
    elif filtros['Energy'] == 'E':
        fields['energy'] = '883186-889028-1287037-883184-1007875-902412-1311230-1369604'



    # ---- URL
    c_filter = '&c='
    if fields['energy']:
        fields['c_filters'].append(fields['energy'])
    if fields['froid']:
        fields['c_filters'].append(fields['froid'])
    if fields['froidcongelation']:
        fields['c_filters'].append(fields['froidcongelation'])        
    if fields['largeur']:
        fields['c_filters'].append(fields['largeur'])        
    url_darty += '&cat=' + fields['subtype']
    if fields['marque']:
        url_darty += '&m=' + fields['marque']           
    if fields['c_filters'] != []:
        url_darty += c_filter + "-".join(fields['c_filters'])         

    #Limpieza
    # url_darty = url_darty.replace('=-','=').replace('--','-')

    url_darty += '&npk=1'

    #Limpieza
    url_darty = url_darty.replace('=-','=').replace('--','-')

    return url_darty


def urlgen_congelador(filtros, should_print):

    fields = {
        'subtype': '',
        'marque': '',
        'energy': '',
        'froid': '',
        'largeur': '',
        'c_filters' : [],
        'froidcongelation' : ''
    }

    url_darty = 'https://www.darty.com/nav/extra/list?s=prix_asc'

    if filtros['Hateur'] == "null":
        filtros['Hateur'] = ""

    if filtros['Largeur'] == "null":
        filtros['Largeur'] = ""

    if filtros['Profoundeur'] == "null":
        filtros['Profoundeur'] = ""

    if filtros['Volume utile'] == "null":
        filtros['Volume utile'] = ""

    # MARQUE
    # OBS: EXISTEN ABREVIACIONES DISTINTAS
    if filtros['Marque'].upper() == 'CALIFORNIA': fields['marque'] = 'MP_california'
    elif filtros['Marque'].upper() == 'NODOR': fields['marque'] = 'MP_nodor'
    elif filtros['Marque'].upper() == 'KLARSTEIN': fields['marque'] = 'MP_klarstein'
    elif filtros['Marque'].upper() == 'LA SOMMELIERE': fields['marque'] = 'LASOM'
    elif filtros['Marque'].upper() == 'LE CHAI': fields['marque'] = 'LECHA'
    elif filtros['Marque'].upper() == 'ELECTROLUX': fields['marque'] = 'ELLUX'
    elif filtros['Marque'].upper() == 'DE DIETRICH': fields['marque'] = 'DEDIE'
    elif filtros['Marque'].upper() == 'ICYTECH': fields['marque'] = 'MP_icytech'
    elif filtros['Marque'].upper() == 'TECHNOLEC': fields['marque'] = 'TECNL'
    elif filtros['Marque'].upper() == 'MOULINEX STUDIO': fields['marque'] = 'MOSTU'
    elif filtros['Marque'].upper() == 'SOGELUX': fields['marque'] = 'MP_sogelux'
    else:
        if len(filtros['Marque']) >=5:
            fields['marque'] = filtros['Marque'].upper()[:5]
        else:
            fields['marque'] = filtros['Marque'].upper()

    # SUBTYPE
    if filtros['Subtype'] == 'Congélateur coffre':
        fields['subtype'] = '522'        
    elif filtros['Subtype'] == 'Congélateur armoire':
        fields['subtype'] = '524'
    else:
        fields['subtype'] = '23564'

    # LARGEUR
    if filtros['Largeur'] and str(filtros['Largeur'].replace(" ", "")) != "null" and\
            str(filtros['Largeur']).replace(" ", "") != "undefined" and filtros['Largeur'] != '0':
        # Taille: rango de pulgadas
        lower_large  = filtros['Largeur'].split("-")[0]
        upper_large  = filtros['Largeur'].split("-")[1]
        a = int(float(lower_large))*10
        b = int(float(upper_large))*10 + 1
        fields['largeur'] = '-'.join(
            [str(centimetros) + '000266616' for centimetros in range(a, b)])

    # SYSTEME DE FROID CONGELATEUR (VENTILE > BRASSE > STATIQUE)
    if filtros['Systeme de froid'] == 'Ventilé':
        fields['froid'] = '1512745'

    # ENERGY:
    if filtros['Energy'] == 'A+++':
        fields['energy'] = '1512661'
    elif filtros['Energy'] == 'A++':
        fields['energy'] = '1512661-1512660'
    elif filtros['Energy'] == 'A+':
        fields['energy'] = '1512661-1512660-1512659'


    # ---- URL
    c_filter = '&c='
    if fields['energy']:
        fields['c_filters'].append(fields['energy'])
    if fields['froid']:
        fields['c_filters'].append(fields['froid'])      
    if fields['largeur']:
        fields['c_filters'].append(fields['largeur'])        
    url_darty += '&cat=' + fields['subtype']
    if fields['marque']:
        url_darty += '&m=' + fields['marque']           
    if fields['c_filters'] != []:
        url_darty += c_filter + "-".join(fields['c_filters'])         

    #Limpieza
    # url_darty = url_darty.replace('=-','=').replace('--','-')

    url_darty += '&npk=1'

    #Limpieza
    url_darty = url_darty.replace('=-','=').replace('--','-')

    return url_darty



def urlgen_cava_de_vino(filtros, should_print):    

    fields = {
        'subtype': '',
        'marque': '',
        'energy': '',
        'froid': '',
        'largeur': '',
        'c_filters' : [],
        'stockage' : '',
        'froidcongelation' : ''
    }

    url_darty = 'https://www.darty.com/nav/extra/list?s=prix_asc'

    if filtros['Hateur'] == "null":
        filtros['Hateur'] = ""

    if filtros['Largeur'] == "null":
        filtros['Largeur'] = ""

    if filtros['Profoundeur'] == "null":
        filtros['Profoundeur'] = ""

    if filtros['Volume net'] == "null":
        filtros['Volume net'] = ""

    # MARQUE
    # OBS: EXISTEN ABREVIACIONES DISTINTAS
    if filtros['Marque'].upper() == 'CALIFORNIA': fields['marque'] = 'MP_california'
    elif filtros['Marque'].upper() == 'NODOR': fields['marque'] = 'MP_nodor'
    elif filtros['Marque'].upper() == 'KLARSTEIN': fields['marque'] = 'MP_klarstein'
    elif filtros['Marque'].upper() == 'LA SOMMELIERE': fields['marque'] = 'LASOM'
    elif filtros['Marque'].upper() == 'LE CHAI': fields['marque'] = 'LECHA'
    elif filtros['Marque'].upper() == 'ELECTROLUX': fields['marque'] = 'ELLUX'
    elif filtros['Marque'].upper() == 'DE DIETRICH': fields['marque'] = 'DEDIE'
    elif filtros['Marque'].upper() == 'ICYTECH': fields['marque'] = 'MP_icytech'
    elif filtros['Marque'].upper() == 'TECHNOLEC': fields['marque'] = 'TECNL'
    elif filtros['Marque'].upper() == 'MOULINEX STUDIO': fields['marque'] = 'MOSTU'
    elif filtros['Marque'].upper() == 'SOGELUX': fields['marque'] = 'MP_sogelux'
    else:
        if len(filtros['Marque']) >=5:
            fields['marque'] = filtros['Marque'].upper()[:5]
        else:
            fields['marque'] = filtros['Marque'].upper()

    # SUBTYPE
    if filtros['Subtype'] == 'Cave à vin service':
        fields['subtype'] = '24567'        
    elif filtros['Subtype'] == 'Cave à vin vieillissement':
        fields['subtype'] = '513'
    elif filtros['Subtype'] == 'Cave à vin multi-températures':
        fields['subtype'] = '24570'        
    else:
        fields['subtype'] = '12410'

    # SYSTEME DE FROID (VENTILE > BRASSE > STATIQUE)
    if filtros['Systeme de froid'] == 'Ventilé':
        fields['froid'] = '1512745'

    # STOCKAGE
    if filtros['Stockage'] == "100-200":
        fields['stockage'] = '1490000355592-1180000355592-1420000355592-1200000355592-1280000355592-1050000355592-1020000355592-1400000355592-1500000355592-1220000355592-1380000355592-1150000355592-1300000355592-1370000355592-1070000355592-1010000355592-1100000355592-1210000355592-1440000355592-1190000355592-1640000355592-1870000355592-1720000355592-1800000355592-1780000355592-1650000355592-1940000355592-1960000355592-1700000355592-1930000355592-1660000355592-1600000355592-1990000355592-1730000355592-1680000355592-1980000355592-2000000355592-1970000355592-1590000355592-1510000355592-1770000355592-1620000355592-1740000355592-1820000355592-1950000355592-1920000355592-1540000355592'
    elif filtros['Stockage'] == "Plus de 200":
        fields['stockage'] = '2110000355592-2180000355592-2340000355592-2100000355592-2040000355592-2050000355592-2020000355592-2400000355592-2480000355592-2300000355592-2370000355592-2360000355592-2010000355592-2470000355592-2090000355592-2440000355592-2030000355592-2060000355592-2640000355592-2940000355592-2650000355592-3120000355592-2760000355592-3250000355592-3150000355592-2530000355592-3000000355592-4740000355592-2670000355592'

    # ENERGY:
    if filtros['Energy'] == 'A++':
        fields['energy'] = '1512661'
    elif filtros['Energy'] == 'A+':
        fields['energy'] = '1512161-1512162'
    elif filtros['Energy'] == 'A':
        fields['energy'] = '1512162-1512161-1512163'
    elif filtros['Energy'] == 'B':
        fields['energy'] = '1512162-1512163-1512161-1512210'
    elif filtros['Energy'] == 'C':
        fields['energy'] = '1512210-1512162-1512163-1512161-1512164'
    elif filtros['Energy'] == 'D':
        fields['energy'] = '1512210-1512162-1512163-1512164-1512161-1512211'                        


    # ---- URL
    c_filter = '&c='
    if fields['energy']:
        fields['c_filters'].append(fields['energy'])
    if fields['froid']:
        fields['c_filters'].append(fields['froid'])      
    if fields['stockage']:
        fields['c_filters'].append(fields['stockage'])              
    if fields['largeur']:
        fields['c_filters'].append(fields['largeur'])        
    url_darty += '&cat=' + fields['subtype']
    if fields['marque']:
        url_darty += '&m=' + fields['marque']           
    if fields['c_filters'] != []:
        url_darty += c_filter + "-".join(fields['c_filters'])         

    #Limpieza
    # url_darty = url_darty.replace('=-','=').replace('--','-')

    url_darty += '&npk=1'

    #Limpieza
    url_darty = url_darty.replace('=-','=').replace('--','-')

    return url_darty


def urlgen_mobile(filtros, should_print):
    raise NotImplementedError


# -------- FILTROS POSTERIORES
def filter_tv(query_products):
    list_products = []
    for p in query_products:
        product = {}
        product["name"] = p.nombre
        product["category_id"] = p.category_id
        product["store_id"] = p.store_id
        list_products.append(product)
    return list_products


def filter_frigo(query_products):
    list_products = []
    for p in query_products:
        product = {}
        product["name"] = p.nombre
        product["category_id"] = p.category_id
        product["store_id"] = p.store_id
        list_products.append(product)
    return list_products
