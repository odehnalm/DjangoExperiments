def urlgen_refrigerador_combinado(filtros):

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

    fields['url_base'] = 'https://www.boulanger.com/c/refrigerateur-avec-congelateur'

    # SUBTYPE
    if filtros['Subtype'] == 'Réfrigérateur américain':
        fields['url_base'] = 'https://www.boulanger.com/c/refrigerateur-americain'
    elif filtros['Subtype'] == 'Réfrigérateur congélateur en bas':
        fields['subtype'].append('conge9lateur20en20bas')
    elif filtros['Subtype'] == 'Réfrigérateur congélateur en haut':
        fields['subtype'].append('conge9lateur20en20haut')

    # MARQUE
    if filtros["Marque"]:
        fields['brand'] = filtros['Marque'].lower().replace(" ", "20")

    #HATEUR
    if filtros['Hateur'] in {"30-75","75-100"}:
        fields['hateur'].append('3c209020cm')
        num_filters += 1
    elif filtros['Hateur'] in {"75-100","100-120","120-160"}:
        fields['hateur'].append('de209020e02015020cm')
        num_filters += 1
    elif filtros['Hateur'] in {"120-160","160-180"}:
        fields['hateur'].append('de2017620e02018620cm')
        num_filters += 1
    elif filtros['Hateur'] in {"160-180","180-195"}:
        fields['hateur'].append('de2017620e02018620cm')
        num_filters += 1
    elif filtros['Hateur'] in {"180-195","195-205"}:
        fields['hateur'].append('de2018720e02019220cm')
        num_filters += 1

    #LARGEUR
    if filtros['Largeur'] in {"50-60"}:
        fields['largeur'].append('de205020e0205520cm')
        fields['largeur'].append('de205620e0206020cm')
        num_filters += 1
    elif filtros['Largeur'] in {"60-70","70-80"}:
        fields['largeur'].append('de206120e0208020cm')
        num_filters += 1
    elif filtros['Largeur'] in {"80-90"}:
        fields['largeur'].append('de208120e0209020cm')
        num_filters += 1
    elif filtros['Largeur'] == "90-105":
        fields['largeur'].append('3e9020cm')
        num_filters += 1

    #PROFOUNDEUR
    if filtros['Profoundeur'] == "20-55":
        fields['profondeur'].append('moins20de205520cm')
        num_filters += 1
    elif filtros['Profoundeur'] == "55-60":
        fields['profondeur'].append('de205520e0206020cm')
        num_filters += 1
    elif filtros['Profoundeur'] == "61-65":
        fields['profondeur'].append('de206120e0206520cm')
        num_filters += 1
    elif filtros['Profoundeur'] == "66-75":
        fields['profondeur'].append('de206620e0207520cm')
        num_filters += 1
    elif filtros['Profoundeur'] == "Plus de 75":
        fields['profondeur'].append('plus20de207520cm')
        num_filters += 1

    # VOLUME TOTAL UTILE
    if filtros['Volume utile'] in {"Moins de 150","150-244"}:
        fields['volume'].append('3c2020020litres')
        num_filters += 1
    elif filtros['Volume utile'] in {"150-244","245-273","247-316","317-425"}:
        fields['volume'].append('de2020020e02035020litres')
        num_filters += 1
    elif filtros['Volume utile'] in {"317-425","Plus de 426"}:
        fields['volume'].append('3e2055020litres')
        fields['volume'].append('de2035120e02055020litres')
        num_filters += 1

    #ENERGY
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

    # SYSTEME DE FROID REFRIGERATEUR (VENTILE > BRASSE > STATIQUE)
    if filtros['Systeme de froid'] == 'Brassé':
        fields['froid'].append('froid20brasse9')
        fields['froid'].append('froid20ventile9')
        num_filters += 1        
    elif filtros['Systeme de froid'] == 'Ventilé':
        fields['froid'].append('froid20ventile9')
        num_filters += 1  

    # SYSTEME DE FROID CONGELATEUR
    if filtros['Type congelation'] == 'Ventilé':
        fields['froidcongelateur'].append('froid20ventile9203a20de9givrage20automatique')
        num_filters += 1

    # TECHNOLOGIE NO FROST
    if filtros['Technologie'] == 'No frost':
        fields['nofrost'].append('supreame20no20frost')
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
    if fields['subtype']:
        values = "|".join(['facetting_tous_les_refs_____configuration~'+ e for e in fields['subtype']])
        url_fields.append(values)         
    if fields['hateur']:
        values = "|".join(['facetting_tous_les_refs_____hauteur_du_refrigerateur~'+ e for e in fields['hateur']])
        url_fields.append(values) 
    if fields['largeur']:
        values = "|".join(['facetting_tous_les_refs_____largeur~'+ e for e in fields['largeur']])
        url_fields.append(values) 
    if fields['profondeur']:        
        values = "|".join(['facetting_tous_les_refs_____profondeur_du_refrigerateur~'+ e for e in fields['hateur']])
        url_fields.append(values) 
    if fields['volume']:     
        values = "|".join(['facetting_tous_les_refs_____volume~'+ e for e in fields['volume']])
        url_fields.append(values)    
    if fields['energy']:     
        values = "|".join(['facetting_tous_les_refs_____classe_energetique~'+ e for e in fields['energy']])
        url_fields.append(values)          
    if fields['froid']:     
        values = "|".join(['facetting_tous_les_refs_____type_de_froid~'+ e for e in fields['froid']])
        url_fields.append(values)              
    if fields['froidcongelateur']:     
        values = "|".join(['facetting_tous_les_refs_____type_de_froid_du_congelateur~'+ e for e in fields['froidcongelateur']])
        url_fields.append(values)  
    if fields['nofrost']:     
        values = "|".join(['facetting_tous_les_refs_____technologie~'+ e for e in fields['nofrost']])
        url_fields.append(values)                                  

    url += "|".join(url_fields)
    url += sorting

    return url  

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
    'Type congelation' : '',
    'Technologie' : '',
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
    'Type congelation' : '',
    'Technologie' : '',
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
    'Type congelation' : '',
    'Technologie' : '',
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
    'Energy': "",
    'Volume utile': '',
    'Hateur': '',
    'Profoundeur': '',
    'Subtype' : 'Réfrigérateur américain',
    'Volume net' : '',
    'Type congelation' : 'Ventilé',
    'Technologie' : 'No frost',
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
    'Type congelation' : '',
    'Technologie' : '',
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
    'Type congelation' : '',
    'Technologie' : '',
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
    'Type congelation' : '',
    'Technologie' : '',
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
    'Type congelation' : '',
    'Technologie' : '',
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_refrigerador_combinado(filtros))
print("")    

filtros = {
    'Marque': 'LIEBHERR',
    'Largeur': '90-105',
    'TypePose': "Pose libre",
    'Systeme de froid': "Ventilé",
    'Energy': "A+",
    'Volume utile': '274-316',
    'Hateur': '195-205',
    'Profoundeur': 'Plus de 75',
    'Subtype' : 'Réfrigérateur congélateur en bas',
    'Volume net' : '',
    'Type congelation' : 'Ventilé',
    'Technologie' : 'No frost',
}

print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_refrigerador_combinado(filtros))
print("")    