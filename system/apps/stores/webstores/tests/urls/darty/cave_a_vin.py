def urlgen_cava_de_vino(filtros):

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


filtros = {
    'Marque': 'LA SOMMELIERE',
    'Largeur': '',
    'Volume utile': "",
    'TypePose': "",
    'Systeme de froid': "",
    'Energy': "",
    'Volume utile': '',
    'Hateur': '',
    'Profoundeur': '',
    'Subtype' : '',
    'Stockage' : '',
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_cava_de_vino(filtros))
print("")   

filtros = {
    'Marque': 'CLIMADIFF',
    'Largeur': '',
    'Volume utile': "",
    'TypePose': "",
    'Systeme de froid': "",
    'Energy': "",
    'Volume utile': '',
    'Hateur': '',
    'Profoundeur': '',
    'Subtype' : '',
    'Stockage' : '100-200',
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_cava_de_vino(filtros))
print("")      

filtros = {
    'Marque': 'CLIMADIFF',
    'Largeur': '',
    'Volume utile': "",
    'TypePose': "",
    'Systeme de froid': "",
    'Energy': "",
    'Volume utile': '',
    'Hateur': '',
    'Profoundeur': '',
    'Subtype' : 'Cave à vin multi-températures',
    'Stockage' : 'Moins de 100',
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_cava_de_vino(filtros))
print("")

filtros = {
    'Marque': '',
    'Largeur': '',
    'Volume utile': "",
    'TypePose': "",
    'Systeme de froid': "",
    'Energy': "",
    'Volume utile': '',
    'Hateur': '',
    'Profoundeur': '',
    'Subtype' : 'Cave à vin vieillissement',
    'Stockage' : '',
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_cava_de_vino(filtros))
print("")    

filtros = {
    'Marque': 'CLIMADIFF',
    'Hateur': '100-120',
    'Largeur': '60-70',
    'Profoundeur': '55-60',
    'Volume utile': "",
    'TypePose': "",
    'Systeme de froid': "",
    'Energy': "D",
    'Volume utile': '',
    'Hateur': '',
    'Profoundeur': '',
    'Subtype' : 'Cave à vin multi-températures',
    'Stockage' : 'Plus de 200',
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_cava_de_vino(filtros))
print("")  