# -*- coding: utf-8 -*-
def urlgen_refrigerador(filtros):

    exist_filter = False
    fields = {
        'x-146401': '',
        'classe-energetique': '',
        'froid-ventile': '',
        'largeur': '',
        'marque': '',
        'type-de-pose': '',
        'volume-net-en-litres': ''
    }

    url_kelkoo = 'http://www.kelkoo.fr/'
    fields['x-146401'] = 'c-146401-refrigerateur'

    if filtros['Hateur'] == "null":
        filtros['Hateur'] = ""

    if filtros['Largeur'] == "null":
        filtros['Largeur'] = ""

    if filtros['Profoundeur'] == "null":
        filtros['Profoundeur'] = ""

    if filtros['Volume net'] == "null":
        filtros['Volume net'] = ""

    if filtros['Volume utile'] == "null":
        filtros['Volume utile'] = ""

    # ---- MARQUE
    if filtros['Marque']:
        exist_filter = True

        if filtros['Marque'].lower() == "beko" or\
                filtros['Marque'].lower() == "bosch" or\
                filtros['Marque'].lower() == "siemens":

            fields['x-146401'] = 'v-146401-refrigerateur-' + filtros['Marque'].lower().replace(' ', '-').replace('&', 'E')
        else:
            fields['marque'] = filtros['Marque'].lower().replace(' ', '-').replace('&', 'E')

    # ---- CLASSE ENERGETIQUE
    if filtros['Energy']:
        exist_filter = True
        if filtros['Energy'] == 'A+':
            if fields['x-146401'] == 'c-146401-refrigerateur':
                fields['x-146401'] = 'v-146401-refrigerateur-classe-ap'
            elif 'v-146401-refrigerateur' in fields['x-146401']:
                fields['classe-energetique'] = 'classe-a-p'
        elif filtros['Energy'] == 'A':
            fields['classe-energetique'] = 'classe-a'
        elif filtros['Energy'] == 'B':
            fields['classe-energetique'] = 'classe-b'
        elif filtros['Energy'] == 'C':
            fields['classe-energetique'] = 'classe-c'
        elif filtros['Energy'] == 'D':
            fields['classe-energetique'] = 'classe-d'
        elif filtros['Energy'] == 'G':
            fields['classe-energetique'] = 'classe-g'

    # ---- FROID VENTILE
    if filtros['Systeme de froid']:
        if filtros['Systeme de froid'] == "Ventilé":
            exist_filter = True
            fields['froid-ventile'] = 'avec-froid-ventilo'

    # ---- LARGEUR
    if filtros['Largeur']:
        exist_filter = True
        if filtros['Largeur'] == '50-60':
            fields['largeur'] = '51-cm-60-cm'
        elif filtros['Largeur'] == '60-70':
            fields['largeur'] = '61-cm-70-cm'
        elif filtros['Largeur'] == '70-80':
            fields['largeur'] = '71-cm-80-cm'
        elif filtros['Largeur'] == '80-90':
            fields['largeur'] = '81-cm-90-cm'
        elif filtros['Largeur'] == '90-105':
            fields['largeur'] = 'plus-de-90-cm'

    # ---- TYPE DE POSE
    if filtros['TypePose'] == 'Pose libre':
        exist_filter = True
        fields['type-de-pose'] = "posable"
    elif filtros['TypePose'] == 'integrable':
        exist_filter = True
        fields['type-de-pose'] = "intograble"

    # ---- VOLUME NET EN LITRES
    if filtros['Volume net']:
        if filtros['Volume net'] == "Moins de 51":
            fields['volume-net-en-litres'] = 'moins-de-51-l'
        elif filtros['Volume net'] == "51-140":
            fields['volume-net-en-litres'] = '51-l-140-l'
        elif filtros['Volume net'] == "141-149":
            fields['volume-net-en-litres'] = '141-l-149-l'
        elif filtros['Volume net'] == "150-179":
            fields['volume-net-en-litres'] = '150-l-179-l'
        elif filtros['Volume net'] == "180-259":
            fields['volume-net-en-litres'] = '180-l-259-l'
        elif filtros['Volume net'] == "Plus de 259":
            fields['volume-net-en-litres'] = 'plus-de-259-l'

    # ---- URL
    counter_fields = 0
    url_kelkoo += fields['x-146401']
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
    if fields['volume-net-en-litres']:
        counter_fields += 1
        url_kelkoo += '/volume-net-en-litres/' + fields['volume-net-en-litres']

    if counter_fields >= 3:
        url_kelkoo = url_kelkoo.replace("www.kelkoo.fr/", "www.kelkoo.fr/nf/")

    if not exist_filter:
        url_kelkoo += '.html'

    # ORDEN DE PRODUCTOS
    url_kelkoo += '?sortby=price_ascending'

    return url_kelkoo


filtros = {
    'Marque': 'BOSCH',
    'Largeur': '50-60',
    'Volume net': "180-259",
    'TypePose': "Pose libre",
    'Systeme de froid': "Ventilé",
    'Energy': "",
    'Volume utile': '',
    'Hateur': '',
    'Profoundeur': ''
}
print("FILTROS")
print(filtros)
print("URL ESPERADA")
print("http://www.kelkoo.fr/nf/v-146401-refrigerateur-bosch/froid-ventile/avec-froid-ventilo/largeur/51-cm-60-cm/type-de-pose/posable/volume-net-en-litres/180-l-259-l?sortby=price_ascending")
print("URL GENERADA")
print(urlgen_refrigerador(filtros))
print("")

filtros = {
    'Marque': 'BOSCH',
    'Largeur': '50-60',
    'Volume net': "180-259",
    'TypePose': "Pose libre",
    'Systeme de froid': "",
    'Energy': "A+",
    'Volume utile': '',
    'Hateur': '',
    'Profoundeur': ''
}
print("FILTROS")
print(filtros)
print("URL ESPERADA")
print("http://www.kelkoo.fr/nf/v-146401-refrigerateur-bosch/classe-energetique/classe-a-p/largeur/51-cm-60-cm/type-de-pose/posable/volume-net-en-litres/180-l-259-l?sortby=price_ascending")
print("URL GENERADA")
print(urlgen_refrigerador(filtros))
print("")

filtros = {
    'Marque': 'BOSCH',
    'Largeur': '50-60',
    'Volume net': "180-259",
    'TypePose': "",
    'Systeme de froid': "",
    'Energy': "",
    'Volume utile': '',
    'Hateur': '',
    'Profoundeur': ''
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
    'Profoundeur': ''
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
    'Profoundeur': ''
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
    'Profoundeur': ''
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
    'Profoundeur': ''
}
print("FILTROS")
print(filtros)
print("URL ESPERADA")
print("http://www.kelkoo.fr/v-146401-refrigerateur-classe-ap?sortby=price_ascending")
print("URL GENERADA")
print(urlgen_refrigerador(filtros))
print("")
