# -*- coding: utf-8 -*-
def urlgen_refrigerador(filtros):

    fields = {
        'url_base': '',
        'brand': '',
        'largeur': [],
        'profondeur': [],
        'hateur': [],
        'volume': [],
        'energy': [],
        'froid': [],
    }

    num_filters = 0

    if filtros['Subtype'] == 'Réfrigérateur compact':
        fields['url_base'] = "https://www.boulanger.com/c/petit-refrigerateur"
    else:
        fields['url_base'] = "https://www.boulanger.com/c/refrigerateur-1-porte"

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

    url += "|".join(url_fields)
    url += sorting

    return url  

filtros = {
    'Marque': 'LIEBHERR',
    'Largeur': '50-60',
    'Volume utile': "Moins de 150",
    'TypePose': "Pose libre",
    'Systeme de froid': "Ventilé",
    'Energy': "",
    'Hateur': '',
    'Profoundeur': '',
    'Subtype' : 'Réfrigérateur compact',
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_refrigerador(filtros))
print("")

filtros = {
    'Marque': 'LIEBHERR',
    'Largeur': '',
    'Volume net': "180-259",
    'TypePose': "Pose libre",
    'Systeme de froid': "",
    'Energy': "A+",
    'Volume utile': '',
    'Hateur': '',
    'Profoundeur': '',
    'Subtype' : '',
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_refrigerador(filtros))
print("")

filtros = {
    'Marque': '',
    'Largeur': '',
    'Volume net': "180-259",
    'TypePose': "",
    'Systeme de froid': "",
    'Energy': "",
    'Volume utile': '',
    'Hateur': '180-195',
    'Profoundeur': '',
    'Subtype' : '',
}
print("FILTROS")
print(filtros)
print("URL ESPERADA")
print("http://www.kelkoo.fr/v-146401-refrigerateur-bosch/largeur/51-cm-60-cm/volume-net-en-litres/180-l-259-l?sortby=price_ascending")
print("URL GENERADA")
print(urlgen_refrigerador(filtros))
print("")

filtros = {
    'Marque': '',
    'Largeur': '50-60',
    'Volume net': "180-259",
    'TypePose': "",
    'Systeme de froid': "",
    'Energy': "",
    'Volume utile': '',
    'Hateur': '',
    'Profoundeur': '',
    'Subtype' : '',
}
print("FILTROS")
print(filtros)
print("URL ESPERADA")
print("http://www.kelkoo.fr/c-146401-refrigerateur/largeur/51-cm-60-cm/volume-net-en-litres/180-l-259-l?sortby=price_ascending")
print("URL GENERADA")
print(urlgen_refrigerador(filtros))
print("")

filtros = {
    'Marque': 'LIEBHERR',
    'Largeur': '50-60',
    'Volume net': "180-259",
    'TypePose': "",
    'Systeme de froid': "",
    'Energy': "",
    'Volume utile': '',
    'Hateur': '',
    'Profoundeur': '',
    'Subtype' : '',
}
print("FILTROS")
print(filtros)
print("URL ESPERADA")
print("http://www.kelkoo.fr/nf/c-146401-refrigerateur/largeur/51-cm-60-cm/marque/liebherr/volume-net-en-litres/180-l-259-l?sortby=price_ascending")
print("URL GENERADA")
print(urlgen_refrigerador(filtros))
print("")

filtros = {
    'Marque': '',
    'Largeur': '',
    'Volume net': '',
    'TypePose': "",
    'Systeme de froid': "",
    'Energy': "",
    'Volume utile': '',
    'Hateur': '',
    'Profoundeur': '',
    'Subtype' : '',
}
print("FILTROS")
print(filtros)
print("URL ESPERADA")
print("http://www.kelkoo.fr/c-146401-refrigerateur.html?sortby=price_ascending")
print("URL GENERADA")
print(urlgen_refrigerador(filtros))
print("")

filtros = {
    'Marque': '',
    'Largeur': '',
    'Volume net': '',
    'TypePose': "",
    'Systeme de froid': "",
    'Energy': "A+",
    'Volume utile': '',
    'Hateur': '',
    'Profoundeur': '',
    'Subtype' : '',
}
print("FILTROS")
print(filtros)
print("URL ESPERADA")
print("http://www.kelkoo.fr/v-146401-refrigerateur-classe-ap?sortby=price_ascending")
print("URL GENERADA")
print(urlgen_refrigerador(filtros))
print("")
