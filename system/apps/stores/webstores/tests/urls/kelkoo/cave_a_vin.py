def urlgen_cava_de_vino(filtros):

    exist_filter = False
    
    fields = {
        'x-100014413': '',
        'subtype': '',
        'marque': '',
        'stockage': ''
    } 

    try:
        if filtros['Hateur'] == "null":
            filtros['Hateur'] = ""
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

    fields['x-100014413'] = 'c-100014413-cave-a-vin'

    #Contamos numero de filtros llenos

    if filtros['Subtype'] != '': exist_filter = True
    if filtros['Marque'] != '': exist_filter = True
    if filtros['Stockage'] != '': exist_filter = True
    if filtros['TypePose'] != '': exist_filter = True


    # SUBTYPE
    if filtros['Subtype'] == 'Cave à vin multi-températures':
        fields['subtype'] = 'mise-a-temperature'
    elif filtros['Subtype'] == 'Cave à vin vieillissement':
        fields['subtype'] = 'vieillissement'

    # MARQUE
    if filtros['Marque'] != "":
        fields['marque'] = filtros['Marque'].lower().replace(' ', '-').replace('&', 'E')

    # # VOLUME POST FILTER

    # TYPE DE POSE POST FILTER

    # STOCKAGE
    if filtros['Stockage'] == 'Moins de 100':
        fields['stockage'] = 'moins-de-100'
    elif filtros['Stockage'] == '100-200':
        fields['stockage'] = '100-200'
    elif filtros['Stockage'] == 'Plus de 200':
        fields['stockage'] = '200-300'

    # ---- URL
    counter_fields = 0
    url_kelkoo += fields['x-100014413']         
    if fields['marque']:
        counter_fields += 1
        url_kelkoo += '/marque/' + fields['marque']      
    if fields['stockage']:
        counter_fields += 1
        url_kelkoo += '/nombre-de-bouteilles/' + fields['stockage']
    if fields['subtype']:
        counter_fields += 1
        url_kelkoo += '/type-de-cave-a-vin/' + fields['subtype']

    if counter_fields >= 3:
        url_kelkoo = url_kelkoo.replace("www.kelkoo.fr/", "www.kelkoo.fr/nf/")

    if not exist_filter:
        url_kelkoo += '.html'        

    # ORDEN DE PRODUCTOS
    url_kelkoo += '?sortby=price_ascending'

    return url_kelkoo

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