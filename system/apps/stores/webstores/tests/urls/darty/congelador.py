def urlgen_congelador(filtros):

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


filtros = {
    "Hateur": '',
    "Largeur": '',
    "Profoundeur": '',
    "Volume utile": '',
    'Systeme de froid' : 'Ventilé',
    "Subtype": "",
    "Marque": "",
    "TypePose": "",
    "Energy": "",
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_congelador(filtros))
print("")

filtros = {
    "Hateur": '',
    "Largeur": '',
    "Profoundeur": '',
    "Volume utile": '',
    'Systeme de froid' : '',
    "Subtype": "Congélateur coffre",
    "Marque": "",
    "TypePose": "",
    "Energy": "",
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_congelador(filtros))
print("")

filtros = {
    "Hateur": '',
    "Largeur": '',
    "Profoundeur": '',
    "Volume utile": '',
    'Systeme de froid' : '',
    "Subtype": "Congélateur coffre",
    "Marque": "Liebherr",
    "TypePose": "",
    "Energy": "",
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_congelador(filtros))
print("")

filtros = {
    "Hateur": '',
    "Largeur": '',
    "Profoundeur": '',
    "Volume utile": '',
    'Systeme de froid' : '',
    "Subtype": "",
    "Marque": "Bosch",
    "TypePose": "",
    "Energy": "",
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_congelador(filtros))
print("")

filtros = {
    "Hateur": '',
    "Largeur": '',
    "Profoundeur": '',
    "Volume utile": '',
    'Systeme de froid' : '',
    "Subtype": "Congélateur coffre",
    "Marque": "",
    "TypePose": "Integrable",
    "Energy": "",
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_congelador(filtros))
print("")

filtros = {
    "Hateur": '',
    "Largeur": '',
    "Profoundeur": '',
    "Volume utile": '',
'Systeme de froid' : '',
    "Subtype": "Congélateur coffre",
    "Marque": "ELECTROLUX",
    "TypePose": "Integrable",
    "Energy": "",
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_congelador(filtros))
print("")

filtros = {
    "Hateur": '',
    "Largeur": '',
    "Profoundeur": '',
    "Volume utile": '',
'Systeme de froid' : '',
    "Subtype": "Congélateur armoire",
    "Marque": "",
    "TypePose": "Integrable",
    "Energy": "",
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_congelador(filtros))
print("")

filtros = {
    "Hateur": '',
    "Largeur": '',
    "Profoundeur": '',
    "Volume utile": '',
    'Systeme de froid' : 'Ventilé',
    "Subtype": "Congélateur armoire",
    "Marque": "Liebherr",
    "TypePose": "Pose libre",
    "Energy": "",
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_congelador(filtros))
print("")

filtros = {
    "Hateur": '',
    "Largeur": '',
    "Profoundeur": '',
    "Volume utile": '',
'Systeme de froid' : '',
    "Subtype": "Congélateur armoire",
    "Marque": "",
    "TypePose": "Pose libre",
    "Energy": "",
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_congelador(filtros))
print("")

filtros = {
    "Hateur": '195-205',
    "Largeur": '90-105',
    "Profoundeur": '',
    "Volume utile": 'Plus de 400',
    'Systeme de froid' : 'Ventilé',
    "Subtype": "Congélateur armoire",
    "Marque": "Liebherr",
    "TypePose": "Pose libre",
    "Energy": "A",
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_congelador(filtros))
print("")

filtros = {
    "Hateur": '',
    "Largeur": '50-60',
    "Profoundeur": '',
    "Volume utile": 'Plus de 400',
    'Systeme de froid' : 'Ventilé',
    "Subtype": "",
    "Marque": "",
    "TypePose": "Pose libre",
    "Energy": "A+",
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_congelador(filtros))
print("")