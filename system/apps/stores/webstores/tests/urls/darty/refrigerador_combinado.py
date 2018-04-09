def urlgen_refrigerador_combinado(filtros):

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
    if filtros['Systeme de froid'] == 'Brassé':
        fields['froid'] = '1125294-1444895'
    elif filtros['Systeme de froid'] == 'Ventilé':
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


filtros = {
    'Marque': 'LIEBHERR',
    'Largeur': '',
    'Volume utile': "",
    'Type congelation': "",
    'Systeme de froid': "",
    'Energy': "",
    'Volume utile': '',
    'Hateur': '',
    'Profoundeur': '',
    'Subtype' : '',
    'Volume net' : '',
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_refrigerador_combinado(filtros))
print("")

filtros = {
    'Marque': '',
    'Largeur': '',
    'Type congelation': "",
    'Systeme de froid': "",
    'Energy': "A+",
    'Volume utile': '',
    'Hateur': '',
    'Profoundeur': '',
    'Subtype' : '',
    'Volume net' : '',
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_refrigerador_combinado(filtros))
print("")

filtros = {
    'Marque': '',
    'Largeur': '',
    'Type congelation': "",
    'Systeme de froid': "",
    'Energy': "",
    'Volume utile': '',
    'Hateur': '',
    'Profoundeur': '',
    'Subtype' : 'Réfrigérateur américain',
    'Volume net' : '',
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_refrigerador_combinado(filtros))
print("")

filtros = {
    'Marque': '',
    'Largeur': '',
    'Type congelation': "",
    'Systeme de froid': "Ventilé",
    'Energy': "A",
    'Volume utile': '',
    'Hateur': '',
    'Profoundeur': '',
    'Subtype' : 'Réfrigérateur congélateur en bas',
    'Volume net' : '',
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_refrigerador_combinado(filtros))
print("")

filtros = {
    'Marque': 'SAMSUNG',
    'Largeur': '',
    'Type congelation': "integrable",
    'Systeme de froid': "Ventilé",
    'Energy': "A+",
    'Volume utile': '',
    'Hateur': '',
    'Profoundeur': '',
    'Subtype' : 'Réfrigérateur congélateur en bas',
    'Volume net' : '',
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_refrigerador_combinado(filtros))
print("")

filtros = {
    'Marque': 'hotpoint',
    'Largeur': '',
    'Type congelation': "",
    'Systeme de froid': "Ventilé",
    'Energy': "A+",
    'Volume utile': '',
    'Hateur': '',
    'Profoundeur': '',
    'Subtype' : 'Réfrigérateur congélateur en bas',
    'Volume net' : '',
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_refrigerador_combinado(filtros))
print("")

filtros = {
    'Marque': '',
    'Largeur': '80-90',
    'Type congelation': "Ventilé",
    'Systeme de froid': "Ventilé",
    'Energy': "A+",
    'Volume utile': '274-316',
    'Hateur': '',
    'Profoundeur': '',
    'Subtype' : 'Réfrigérateur congélateur en haut',
    'Volume net' : '',
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_refrigerador_combinado(filtros))
print("")