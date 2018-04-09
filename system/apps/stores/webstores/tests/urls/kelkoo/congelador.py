def urlgen_congelador(filtros):

    exist_filter = False
    fields = {
        'x-145701': '',
        'energy': '',
        'subtype': '',
        'marque': '',
        'type-de-pose': ''
    }

    try:
        if filtros['Hauteur'] == "null":
            filtros['Hauteur'] = ""
    except:
        pass
    try:
        if filtros['Largeur'] == "null":
            filtros['Largeur'] = ""
    except:
        pass
    try:
        if filtros['Profoundeur'] == "null":
            filtros['Profoundeur'] = ""
    except:
        pass
    try:
        if filtros['Volume net'] == "null":
            filtros['Volume net'] = ""
    except:
        pass


    url_kelkoo = 'http://www.kelkoo.fr/'

    fields['x-145701'] = "c-145701-congelateur"

    #Contamos numero de filtros llenos

    if filtros['Subtype'] != '': exist_filter = True
    if filtros['Marque'] != '': exist_filter = True
    if filtros['TypePose'] != '': exist_filter = True
    if filtros['Energy'] != '': exist_filter = True

    # SUBTYPE
    if filtros['Subtype'] == 'Congélateur armoire':
        if filtros['TypePose'].lower() == 'integrable':
            fields['subtype'] = 'armoire'
        else:
            fields['x-145701'] = 'v-145701-congelateur-armoire'
    elif filtros['Subtype'] == 'Congélateur coffre':
        if filtros['TypePose'].lower() == 'integrable':
            fields['subtype'] = 'coffre'
        else:
            fields['x-145701'] = 'v-145701-congelateur-coffre'

    # MARQUE
    if filtros['Marque'] != "":
        fields['marque'] = filtros['Marque'].lower().replace(' ', '-')

    # # VOLUME POST FILTER

    # TYPE DE POSE
    if filtros['TypePose'] == 'Pose libre':
        fields['type-de-pose'] += 'pose-libre'
    elif filtros['TypePose'].lower() == 'integrable':
        fields['x-145701'] = 'v-145701-congelateur-encastrable'

    # ENERGY
    if filtros['Energy'] == 'G':
        fields['energy'] = 'g'
    elif filtros['Energy'] == 'E':
        fields['energy'] = 'e'
    elif filtros['Energy'] == 'D':
        fields['energy'] = 'd'
    elif filtros['Energy'] == 'C':
        fields['energy'] = 'c'
    elif filtros['Energy'] == 'B':
        fields['energy'] = 'b'
    elif filtros['Energy'] == 'A':
        fields['energy'] = 'a'
    elif filtros['Energy'] == 'A+':
        fields['energy'] = 'ap'
    elif filtros['Energy'] == 'A++':
        fields['energy'] = 'app'
    elif filtros['Energy'] == 'A+++':
        fields['energy'] = 'appp'

    # ---- URL
    counter_fields = 0
    url_kelkoo += fields['x-145701']
    if fields['energy']:
        url_kelkoo += '/classe-energetique/' + fields['energy']
    if fields['marque']:
        counter_fields += 1
        url_kelkoo += '/marque/' + fields['marque']
    if fields['subtype']:
        counter_fields += 1
        url_kelkoo += '/type-de-congelateur/' + fields['subtype']        
    if fields['type-de-pose']:
        counter_fields += 1
        url_kelkoo += '/type-de-pose/' + fields['type-de-pose']

    if counter_fields >= 3:
        url_kelkoo = url_kelkoo.replace("www.kelkoo.fr/", "www.kelkoo.fr/nf/")
    
    if not exist_filter:
        url_kelkoo += '.html'

    # ORDEN DE PRODUCTOS
    url_kelkoo += '?sortby=price_ascending'

    return url_kelkoo        

filtros = {
    "Hauteur": '',
    "Largeur": '',
    "Profoundeur": '',
    "Volume net": '',

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
    "Hauteur": '',
    "Largeur": '',
    "Profoundeur": '',
    "Volume net": '',

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
    "Hauteur": '',
    "Largeur": '',
    "Profoundeur": '',
    "Volume net": '',

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
    "Hauteur": '',
    "Largeur": '',
    "Profoundeur": '',
    "Volume net": '',

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
    "Hauteur": '',
    "Largeur": '',
    "Profoundeur": '',
    "Volume net": '',

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
    "Hauteur": '',
    "Largeur": '',
    "Profoundeur": '',
    "Volume net": '',

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
    "Hauteur": '',
    "Largeur": '',
    "Profoundeur": '',
    "Volume net": '',

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
    "Hauteur": '',
    "Largeur": '',
    "Profoundeur": '',
    "Volume net": '',

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
    "Hauteur": '',
    "Largeur": '',
    "Profoundeur": '',
    "Volume net": '',

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
    "Hauteur": '',
    "Largeur": '',
    "Profoundeur": '',
    "Volume net": '',

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