def urlgen_cava_de_vino(filtros):

    fields = {
        'url_base': '',
        'subtype' : [],
        'brand': '',
        'largeur': [],
        'profondeur': [],
        'hateur': [],
        'stockage': [],
        'energy': [],
        'froid': [],
        'froidcongelateur': [],
        'nofrost': [],
    }

    num_filters = 0

    fields['url_base'] = 'https://www.boulanger.com/c/toutes-les-caves-a-vin'

    # SUBTYPE
    if filtros['Subtype'] == 'Cave à vin service':
        fields['url_base'] = 'https://www.boulanger.com/c/cave-de-service'
    elif filtros['Subtype'] == 'Cave à vin vieillissement':
        fields['url_base'] = 'https://www.boulanger.com/c/cave-de-vieillissement'
    elif filtros['Subtype'] == 'Cave à vin multi-températures':
        fields['url_base'] = 'https://www.boulanger.com/c/cave-polyvalente'        

    # MARQUE
    if filtros["Marque"]:
        fields['brand'] = filtros['Marque'].lower().replace(" ", "20")

    #HATEUR
    if filtros['Hateur'] != "":
        if filtros['Hateur'] in {"30-75","75-100"}:
            fields['hateur'].append('moins20de2070cm')
            fields['hateur'].append('de207020e0208520cm')
            num_filters += 1
        elif filtros['Hateur'] in {"75-100","100-120"}:
            fields['hateur'].append('de207020e0208520cm')
            fields['hateur'].append('de208620e02012020cm')
            num_filters += 1
        elif filtros['Hateur'] in {"120-160"}:
            fields['hateur'].append('de2012120e02016020cm')
            num_filters += 1
        elif filtros['Hateur'] in {"180-195","195-205"}:
            fields['hateur'].append('plus20de2016020cm')
            num_filters += 1

    #LARGEUR
    if filtros['Largeur'] != "":
        if filtros['Largeur'] in {"30-50"}:
            fields['largeur'].append('moins20de205020cm')
            num_filters += 1
        else:
            fields['largeur'].append('de205020e0206520cm')
            fields['largeur'].append('plus20de206520cm')
            num_filters += 1

    #PROFOUNDEUR
    if filtros['Profoundeur'] != "":
        if filtros['Profoundeur'] in {"20-55","55-60"}:
            fields['profondeur'].append('moins20de206020cm')
            num_filters += 1
        else:
            fields['profondeur'].append('plus20de206020cm')
            num_filters += 1

    # STOCKAGE
    if filtros['Stockage'] == "Moins de 100":
        fields['stockage'].append('moins20de20100')
        num_filters += 1
    elif filtros['Stockage'] == "100-200":
        fields['stockage'].append('de2010020e020200')
        num_filters += 1
    elif filtros['Stockage'] == "Plus de 200":
        fields['stockage'].append('plus20de20200')
        num_filters += 1

    #ENERGY
    if filtros['Energy'] == 'D':
        fields['energy'].append('d')
        fields['energy'].append('c')
        fields['energy'].append('b')
        fields['energy'].append('a')
        fields['energy'].append('a2b')
        fields['energy'].append('a2b2b')
        fields['energy'].append('a2b2b2b')
        num_filters += 1    
    if filtros['Energy'] == 'C':
        fields['energy'].append('c')
        fields['energy'].append('b')
        fields['energy'].append('a')
        fields['energy'].append('a2b')
        fields['energy'].append('a2b2b')
        fields['energy'].append('a2b2b2b')
        num_filters += 1
    if filtros['Energy'] == 'B':
        fields['energy'].append('b')
        fields['energy'].append('a')
        fields['energy'].append('a2b')
        fields['energy'].append('a2b2b')
        fields['energy'].append('a2b2b2b')
        num_filters += 1
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
        values = "|".join(['facettes_cave_a_vin_____hauteur_en_cm~'+ e for e in fields['hateur']])
        url_fields.append(values) 
    if fields['largeur']:
        values = "|".join(['facettes_cave_a_vin_____largeur_en_cm~'+ e for e in fields['largeur']])
        url_fields.append(values) 
    if fields['profondeur']:
        values = "|".join(['facettes_cave_a_vin_____profondeur_en_cm~'+ e for e in fields['profondeur']])
        url_fields.append(values)         
    if fields['stockage']:     
        values = "|".join(['facettes_cave_a_vin_____capacite_avec_clayettes~'+ e for e in fields['stockage']])
        url_fields.append(values)    
    if fields['energy']:     
        values = "|".join(['facettes_cave_a_vin_____classe_energetique~'+ e for e in fields['energy']])
        url_fields.append(values)          

    url += "|".join(url_fields)
    url += sorting

    return url

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
    'Stockage' : '100-200',
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_cava_de_vino(filtros))
print("")  