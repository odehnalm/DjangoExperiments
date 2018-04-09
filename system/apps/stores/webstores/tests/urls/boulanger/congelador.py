def urlgen_congelador(filtros):

    fields = {
        'url_base': '',
        'subtype' : [],
        'brand': '',
        'largeur': [],
        'profondeur': [],
        'hateur': [],
        'volume': [],
        'energy': [],
        'froid': [],
        'froidcongelateur': [],
        'nofrost': [],
    }

    num_filters = 0

    fields['url_base'] = 'https://www.boulanger.com/c/congelateur'

    # SUBTYPE
    if filtros['Subtype'] == 'Congélateur armoire':
        fields['url_base'] = 'https://www.boulanger.com/c/congelateur-armoire'
    elif filtros['Subtype'] == 'Congélateur coffre':
        fields['url_base'] = 'https://www.boulanger.com/c/congelateur-coffre'

    # MARQUE
    if filtros["Marque"]:
        fields['brand'] = filtros['Marque'].lower().replace(" ", "20")

    #HATEUR
    if filtros['Hateur'] in {"30-75","75-100"}:
        fields['hateur'].append('jusqu27e0208520cm')
        num_filters += 1
    elif filtros['Hateur'] in {"75-100","100-120","120-160"}:
        fields['hateur'].append('de208620e02015020cm')
        num_filters += 1
    elif filtros['Hateur'] in {"120-160","160-180"}:
        fields['hateur'].append('de2015120e02017520cm')
        num_filters += 1
    elif filtros['Hateur'] in {"160-180","180-195"}:
        fields['hateur'].append('de2017620e02018620cm')
        num_filters += 1
    elif filtros['Hateur'] in {"180-195","195-205"}:
        fields['hateur'].append('plus20de2017520cm')
        num_filters += 1

    #LARGEUR
    if filtros['Largeur'] in {"50-60"}:
        fields['largeur'].append('de205020e0205520cm')
        fields['largeur'].append('de205620e0206020cm')
        num_filters += 1
    elif filtros['Largeur'] in {"60-70","70-80","80-90"}:
        fields['largeur'].append('de206120e0209020cm')
        num_filters += 1
    elif filtros['Largeur'] == "90-105":
        fields['largeur'].append('3e209020cm')
        num_filters += 1

    # VOLUME UTILE
    if filtros['Volume utile'] == "Moins de 200":
        fields['volume'].append('moins20de2020020l')
        num_filters += 1
    elif filtros['Volume utile'] == "200-299":
        fields['volume'].append('de2020020e02029920l')
        num_filters += 1
    elif filtros['Volume utile'] == "300-400":
        fields['volume'].append('de2030020e02040020l')
        num_filters += 1
    elif filtros['Volume utile'] == "Plus de 400":
        fields['volume'].append('plus20de2040020l')
        num_filters += 1

    #ENERGY
    if filtros['Energy'] == 'A':
        fields['energy'].append('a')
        fields['energy'].append('a2b')
        fields['energy'].append('a2b2b')
        fields['energy'].append('a2b2b2b')
        num_filters += 1
    if filtros['Energy'] == 'A+':
        fields['energy'].append('a2b')
        fields['energy'].append('a2b2b')
        fields['energy'].append('a2b2b2b')
        num_filters += 1
    if filtros['Energy'] == 'A++':
        fields['energy'].append('a2b2b')
        fields['energy'].append('a2b2b2b')
        num_filters += 1
    if filtros['Energy'] == 'A+++':
        fields['energy'].append('a2b2b2b')

    # SYSTEME DE FROID CONGELATEUR
    if filtros['Systeme de froid'] == 'Ventilé':
        fields['froid'].append('froid20statique203a20de9givrage20manuel')
        fields['froid'].append('froid20ventile9203a20de9givrage20automatique')
        num_filters += 1

    url = fields['url_base']
    sorting = 'sorting_price=asc'
    url_fields = []

    if num_filters >= 1:
        url = url.replace('/c/','/c/nav-filtre/')
        sorting = '&' + sorting

    if num_filters == 0:
        url += '/'
        sorting = '?' + sorting
    else:
        url += '?'

    if fields['brand']:
        url_fields.append('brand~'+fields['brand'])       
    if fields['hateur']:
        values = "|".join(['facettes_congelateurs_____Hateur~'+ e for e in fields['hateur']])
        url_fields.append(values) 
    if fields['largeur']:
        values = "|".join(['facettes_congelateurs_____largeur~'+ e for e in fields['largeur']])
        url_fields.append(values) 
    if fields['volume']:     
        values = "|".join(['facettes_congelateurs_____volume~'+ e for e in fields['volume']])
        url_fields.append(values)    
    if fields['energy']:     
        values = "|".join(['facettes_congelateurs_____classe_energetique~'+ e for e in fields['energy']])
        url_fields.append(values)          
    if fields['froid']:     
        values = "|".join(['facettes_congelateurs_____type_de_froid~'+ e for e in fields['froid']])
        url_fields.append(values)                                  

    url += "|".join(url_fields)
    url += sorting

    return url

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