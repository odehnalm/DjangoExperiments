# -*- coding: utf-8 -*-
def urlgen_refrigerador_combinado(filtros):

    exist_filter = False
    fields = {
        'x-145801': '',
        'classe-energetique': '',
        'froid-ventile': '',
        'subtype': '',
        'largeur': '',
        'hateur' : '',
        'profoundeur' : '',
        'marque': '',
        'type-de-pose': '',
        'volume-net-en-litres': ''
    }    

    if filtros['Hateur'] == "null":
        filtros['Hateur'] = ""

    if filtros['Largeur'] == "null":
        filtros['Largeur'] = ""

    if filtros['Profoundeur'] == "null":
        filtros['Profoundeur'] = ""

    if filtros['Volume utile'] == "null":
        filtros['Volume utile'] = ""

    try:
        if filtros['Dispenseur'] == "null":
            filtros['Dispenseur'] = ""        
    except:
        filtros['Dispenseur'] = "" 

    try:
        if filtros['Display'] == "null":
            filtros['Display'] = ""        
    except:
        filtros['Display'] = "" 

    url_kelkoo = 'http://www.kelkoo.fr/'

    fields['x-145801'] = 'c-145801-combine-refrigerateur-congelateur'

    #Contamos numero de filtros llenos

    num_filtros_form = 0
    if filtros['Subtype'] != '': exist_filter = True
    if filtros['Marque'] != '': exist_filter = True
    if filtros['Volume utile'] != '': exist_filter = True
    if filtros['TypePose'] != '': exist_filter = True
    if filtros['Energy'] != '': exist_filter = True
    if filtros['Largeur'] != '': exist_filter = True
    if filtros['Systeme de froid'] != '': exist_filter = True

    # SUBTYPE
    if filtros['Subtype'] == 'Réfrigérateur américain':
        fields['subtype'] = 'rofrigorateur-amoricain'
    elif filtros['Subtype'] == 'Réfrigérateur congélateur en haut':
        fields['subtype'] = 'congolateur-au-dessus'
    elif filtros['Subtype'] == 'Réfrigérateur congélateur en bas':
        fields['subtype'] = 'congolateur-en-dessous'

    # MARQUE
    if filtros['Marque'] != "":
        fields['marque'] = filtros['Marque'].lower().replace(' ', '-').replace('&', 'E')

    # VOLUME
    if filtros['Volume net'] == "Moins de 150" or filtros['Volume utile'] == "Moins de 150":
        fields['volume-net-en-litres'] = 'moins-de-150-l'
    elif filtros['Volume net'] == "150-244" or filtros['Volume utile'] == "150-244":
        fields['volume-net-en-litres'] = '150-l-244-l'
    elif filtros['Volume net'] == "245-273" or filtros['Volume utile'] == "245-273":
        fields['volume-net-en-litres'] = '245-l-273-l'
    elif filtros['Volume net'] == "274-316" or filtros['Volume utile'] == "274-316":
        fields['volume-net-en-litres'] = '274-l-316-l'
    elif filtros['Volume net'] == "317-425" or filtros['Volume utile'] == "317-425":
        fields['volume-net-en-litres'] = '317-l-425-l'
    elif filtros['Volume net'] == "Plus de 426" or filtros['Volume utile'] == "Plus de 426":
        fields['volume-net-en-litres'] = 'plus-de-426-l'

    # TYPE DE POSE
    if filtros['TypePose'] == 'Pose libre':
        fields['type-de-pose'] = 'posable'
    elif filtros['TypePose'].lower() == 'integrable':
        fields['x-145801'] = 'v-145801-refrigerateur-congelateur-encastrable'

    # ENERGY
    if filtros['Energy'] == 'G':
        fields['classe-energetique'] = 'g'
    elif filtros['Energy'] == 'E':
        fields['classe-energetique'] = 'e'
    elif filtros['Energy'] == 'D':
        fields['classe-energetique'] = 'd'
    elif filtros['Energy'] == 'C':
        fields['classe-energetique'] = 'c'
    elif filtros['Energy'] == 'B':
        fields['classe-energetique'] = 'b'
    elif filtros['Energy'] == 'A':
        fields['classe-energetique'] = 'a'
    elif filtros['Energy'] == 'A+':
        if filtros['TypePose'].lower() == 'integrable':
            fields['classe-energetique'] = 'ap'
        else:
            fields['x-145801'] = 'v-145801-refrigerateur-congelateur-classe-ap'
    elif filtros['Energy'] == 'A++':
        fields['classe-energetique'] = 'app'
    elif filtros['Energy'] == 'A+++':
        fields['classe-energetique'] = 'appp'

    # TYPE FROID
    if filtros['Systeme de froid'] == 'Ventilé':
        fields['froid-ventile'] = 'avec-froid-ventilo'

    # ---- URL
    counter_fields = 0
    url_kelkoo += fields['x-145801']
    if fields['classe-energetique']:
        counter_fields += 1
        url_kelkoo += '/classe-energetique/' + fields['classe-energetique']
    if fields['froid-ventile']:
        counter_fields += 1
        url_kelkoo += '/froid-ventile/' + fields['froid-ventile']
    if fields['largeur']:
        counter_fields += 1
        url_kelkoo += '/largeur/' + fields['largeur']          
    if fields['marque']:
        counter_fields += 1
        url_kelkoo += '/marque/' + fields['marque']      
    if fields['type-de-pose']:
        counter_fields += 1
        url_kelkoo += '/type-de-pose/' + fields['type-de-pose']
    if fields['subtype']:
        counter_fields += 1
        url_kelkoo += '/type-de-refrigerateur-congelateur/' + fields['subtype']        
    if fields['volume-net-en-litres']:
        counter_fields += 1
        url_kelkoo += '/volume-total-du-combi/' + fields['volume-net-en-litres']

    if counter_fields >= 3:
        url_kelkoo = url_kelkoo.replace("www.kelkoo.fr/", "www.kelkoo.fr/nf/")

    if not exist_filter:
        url_kelkoo += '.html'

    # ORDEN DE PRODUCTOS
    url_kelkoo += '?sortby=price_ascending'

    return url_kelkoo


filtros = {
    'Marque': 'LIEBHERR',
    'Largeur': '',
    'Volume utile': "",
    'TypePose': "",
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
    'TypePose': "",
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
    'TypePose': "",
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
    'TypePose': "",
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
    'TypePose': "integrable",
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
    'TypePose': "",
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
    'Marque': 'LIEBHERR',
    'Largeur': '',
    'TypePose': "Pose libre",
    'Systeme de froid': "Ventilé",
    'Energy': "A+",
    'Volume utile': '274-316',
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