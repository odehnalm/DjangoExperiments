# -*- coding: utf-8 -*-
def urlgen_laptop(filtros):

    fields = {
        'url_base': '',
        'brand': '',
        'ecran': '',
        'taille_de_l_ecran': '',
        'resolution': [],
        'processeur': [],
        'memoire_vive': [],
        'stockage': [],
        'capacite_disque_dur': [],
        'systeme_d_exploitation': []
    }

    num_filters = 0

    fields['url_base'] = "https://www.boulanger.com/c/tous-les-ordinateurs-portables"
    is_apple = False

    # MARQUE
    if filtros["Marque"]:
        num_filters += 1
        if filtros["Marque"].lower() == "apple":
            is_apple = True
            fields['brand'] = 'macbook'
        else:
            fields['brand'] = filtros['Marque'].lower().replace(" ", "20")

    if not is_apple:
        # Si es tactil
        if 'Ecran tactile' in filtros['Proprietes']:
            num_filters += 1
            fields['ecran'] = 'tactile'

    # TAILLE
    if filtros['Taille (pounce)']:
        num_filters += 1
        if filtros['Taille (pounce)'] in {"Jusqu'à 8","10","11"}:
            fields['taille_de_l_ecran'] = 'moins20de201222'
        elif filtros['Taille (pounce)'] in {"12","13","14"}:
            fields['taille_de_l_ecran'] = 'de20122220e020142c922'
        elif filtros['Taille (pounce)'] in {"15","16"}:
            fields['taille_de_l_ecran'] = 'de20152220e020162c922'
        elif filtros['Taille (pounce)'] in {"17","Plus de 18"}:
            fields['taille_de_l_ecran'] = '172220et20plus'

    # RESOLUTION
    if filtros["Resolution"]:
        if is_apple:
            num_filters += 1
            if filtros["Resolution"] in ['HD+', 'Full_HD', 'Ultra_HD_(4K)']:
                fields['resolution'].append('supe9rieure20e020full20hd')
            elif filtros["Resolution"] == "HD_Ready":
                fields['resolution'].append('infe9rieure20e020full20hd')
        else:
            if filtros["Resolution"] == "HD_Ready":
                num_filters += 2
                fields['resolution'].append('infe9rieure20e020full20hd')
                fields['resolution'].append('full20hd')

            elif filtros["Resolution"] == "HD+":
                num_filters += 2
                fields['resolution'].append('supe9rieure20e020full20hd')
                fields['resolution'].append('full20hd')

            elif filtros["Resolution"] == 'Full_HD':
                num_filters += 2
                fields['resolution'].append('supe9rieure20e020full20hd')
                fields['resolution'].append('4k')
            # elif filtros["Resolution"] == 'QHD':
            #     url_boulanger += '&attr_60382392=60382412%2C60382415%2C60382413%2C60382409%2C60382406%2C60382404%2C60382402'
            elif filtros["Resolution"] == 'Ultra_HD_(4K)':
                num_filters += 1
                fields['resolution'].append('4k')

    # CPU
    if 'Atom' in filtros["list_cpus"]:
        fields['processeur'].append('intel20atom')
        num_filters += 1
    if 'Celeron' in filtros["list_cpus"]:
        fields['processeur'].append('intel20celeron')
        num_filters += 1
    if 'Pentium' in filtros["list_cpus"]:
        fields['processeur'].append('intel20pentium')
        num_filters += 1
    if 'Core M' in filtros["list_cpus"]:
        fields['processeur'].append('intel20core20m')
        num_filters += 1
    if 'Core i3' in filtros["list_cpus"]:
        fields['processeur'].append('intel20core20i3')
        num_filters += 1
    if 'Core i5' in filtros["list_cpus"]:
        fields['processeur'].append('intel20core20i5')
        num_filters += 1
    if 'Core i7' in filtros["list_cpus"]:
        fields['processeur'].append('intel20core20i7')
        num_filters += 1
    if 'E' in filtros["list_cpus"] or 'E1' in filtros["list_cpus"] or 'E2' in filtros["list_cpus"]:
        fields['processeur'].append('amd20se9rie20e')
        num_filters += 1
    if 'A4' in filtros["list_cpus"] or 'A6' in filtros["list_cpus"] or 'A6' in filtros["list_cpus"] or 'A8' in filtros["list_cpus"] or 'A9' in filtros["list_cpus"] or 'A10' in filtros["list_cpus"] or 'A12' in filtros["list_cpus"]:
        fields['processeur'].append('amd20a6')
        fields['processeur'].append('amd20a9')
        num_filters += 2
    if 'A4' in filtros["list_cpus"] or 'A6' in filtros["list_cpus"] or 'A6' in filtros["list_cpus"] or 'A8' in filtros["list_cpus"] or 'A9' in filtros["list_cpus"] or 'A10' in filtros["list_cpus"] or 'A12' in filtros["list_cpus"] or 'E' in filtros["list_cpus"] or 'E1' in filtros["list_cpus"] or 'E2' in filtros["list_cpus"] or 'Opteron' in filtros["list_cpus"] or 'PRO' in filtros["list_cpus"] or 'Ryzen' in filtros["list_cpus"] or 'Phenom' in filtros["list_cpus"] or 'Sempron' in filtros["list_cpus"] or 'Turion' in filtros["list_cpus"] or 'Athlon' in filtros["list_cpus"] or 'FX' in filtros["list_cpus"] or 'G' in filtros["list_cpus"] or 'GX' in filtros["list_cpus"] or 'RX' in filtros["list_cpus"] or 'R' in filtros["list_cpus"]:
        fields['processeur'].append('amd')
        num_filters += 1

    # RAM
    if filtros['Ram (Go)']:
        if float(filtros['Ram (Go)']) <= 4:
            fields['memoire_vive'].append('1220go')
            fields['memoire_vive'].append('1620go')
            fields['memoire_vive'].append('420go')
            fields['memoire_vive'].append('620go')
            fields['memoire_vive'].append('820go')
            num_filters += 5
        elif filtros['Ram (Go)'] == '6':
            fields['memoire_vive'].append('1220go')
            fields['memoire_vive'].append('1620go')
            fields['memoire_vive'].append('3220go')
            fields['memoire_vive'].append('620go')
            fields['memoire_vive'].append('820go')
            num_filters += 5
        elif filtros['Ram (Go)'] == '8':
            fields['memoire_vive'].append('1220go')
            fields['memoire_vive'].append('1620go')
            fields['memoire_vive'].append('3220go')
            fields['memoire_vive'].append('820go')
            num_filters += 4
        elif filtros['Ram (Go)'] == '12':
            fields['memoire_vive'].append('1220go')
            fields['memoire_vive'].append('1620go')
            fields['memoire_vive'].append('3220go')
            num_filters += 3
        elif filtros['Ram (Go)'] == '16':
            fields['memoire_vive'].append('1620go')
            fields['memoire_vive'].append('3220go')
            num_filters += 2
        elif float(filtros['Ram (Go)']) > 16:
            fields['memoire_vive'].append('3220go')
            num_filters += 1

    # Capacidad SSD
    if filtros['Taille SSD (Go)']:
        if float(filtros['Taille SSD (Go)']) >= 1000:
            fields['stockage'].append('120to')
            num_filters += 1
        elif float(filtros['Taille SSD (Go)']) >= 512:
            fields['stockage'].append('120to')
            fields['stockage'].append('51220go')
            num_filters += 2
        elif float(filtros['Taille SSD (Go)']) >= 256:
            fields['stockage'].append('120to')
            fields['stockage'].append('25620go')
            fields['stockage'].append('51220go')
            num_filters += 3
        elif float(filtros['Taille SSD (Go)']) >= 128:
            fields['stockage'].append('12820go')
            fields['stockage'].append('25620go')
            fields['stockage'].append('51220go')
            num_filters += 3
        elif float(filtros['Taille SSD (Go)']) >= 64:
            fields['stockage'].append('12820go')
            fields['stockage'].append('25620go')
            fields['stockage'].append('6420go')
            num_filters += 3
        elif float(filtros['Taille SSD (Go)']) >= 32:
            fields['stockage'].append('12820go')
            fields['stockage'].append('3220go')
            fields['stockage'].append('6420go')
            num_filters += 3

    if not is_apple:

        # CAPACIDAD HDD
        if filtros['Taille HDD (Go)']:
            if float(filtros['Taille HDD (Go)']) == 2000:
                fields['capacite_disque_dur'].append('220to')
                num_filters += 1
            elif float(filtros['Taille HDD (Go)']) >= 1000:
                fields['capacite_disque_dur'].append('120to')
                fields['capacite_disque_dur'].append('220to')
                num_filters += 2
            elif float(filtros['Taille HDD (Go)']) >= 750:
                fields['capacite_disque_dur'].append('120to')
                fields['capacite_disque_dur'].append('220to')
                fields['capacite_disque_dur'].append('75020go')
                num_filters += 3

        # OS
        if filtros['Systeme dexploitation']:
            if filtros["Systeme dexploitation"] == "Windows 10":
                fields['systeme_d_exploitation'].append('windows2010')
                fields['systeme_d_exploitation'].append('windows201020pro')
                fields['systeme_d_exploitation'].append('windows2010s')
                num_filters += 3
            elif filtros["Systeme dexploitation"] == "Windows 8":
                fields['systeme_d_exploitation'].append('windows2082e1')
                num_filters += 1

    url = fields['url_base']
    sorting = 'sorting_price=asc'
    url_fields = []

    if num_filters > 1:
        url = 'https://www.boulanger.com/c/nav-filtre/tous-les-ordinateurs-portables'
        sorting = '&' + sorting

    if num_filters == 1:
        url += '/'
        sorting = '?' + sorting
    else:
        url += '?'

    if fields['brand']:
        url_fields.append('brand~'+fields['brand'])
    if fields['ecran']:
        url_fields.append('nouvelles_facettes_ordinateurs_____ecran~'+fields['ecran'])
    if fields['taille_de_l_ecran']:
        url_fields.append('nouvelles_facettes_ordinateurs_____taille_de_l_ecran~'+fields['taille_de_l_ecran'])
    if fields['resolution']:
        values = "|".join(['nouvelles_facettes_ordinateurs_____resolution~' + e for e in fields['resolution']])
        url_fields.append(values)
    if fields['processeur']:
        values = "|".join(['points_comparateurs_____processeur~' + e for e in fields['processeur']])
        url_fields.append(values)
    if fields['memoire_vive']:
        values = "|".join(['nouvelles_facettes_ordinateurs_____memoire_vive~' + e for e in fields['memoire_vive']])
        url_fields.append(values)
    if fields['stockage']:
        values = "|".join(['nouvelles_facettes_ordinateurs_____stockage~' + e for e in fields['stockage']])
        url_fields.append(values)
    if fields['capacite_disque_dur']:
        values = "|".join(['nouvelles_facettes_ordinateurs_____capacite_disque_dur~' + e for e in fields['capacite_disque_dur']])
        url_fields.append(values)
    if fields['systeme_d_exploitation']:
        values = "|".join(['nouvelles_facettes_ordinateurs_____systeme_d_exploitation~' + e for e in fields['systeme_d_exploitation']])
        url_fields.append(values)

    url += "|".join(url_fields)
    url += sorting

    return url    

filtros = {
    'Marque': 'ASUS',
    'Taille (pounce)': '12',
    'CPU': 'Intel Core i3',
    'Type de stockage': 'SATA',
    'Taille SSD (Go)': '128',
    'Taille HDD (Go)': '500',
    "Ram (Go)": '8',
    "Resolution": 'Full_HD',
    "Systeme dexploitation": "Windows 8",
    "Lecteur/Graveur": "Aucun Lecteur",
    'Proprietes': [''],
    'list_cpus' : ['Xeon', 'Core i7', 'Core i5', 'Ryzen', 'FX', 'Core i3', 'RX' ,'A10', 'PRO', 'A12'],    
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_laptop(filtros))
print("")


filtros = {
    'Marque': 'APPLE',
    'Taille (pounce)': '12',
    'CPU': 'Intel Core i3',
    'Type de stockage': 'SSD',
    'Taille SSD (Go)': '256',
    'Taille HDD (Go)': '500',
    "Ram (Go)": '8',
    "Resolution": 'Full_HD',
    "Systeme dexploitation": "Apple iOS",
    "Lecteur/Graveur": "",
    'Proprietes': [''],
    "list_cpus" : []
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_laptop(filtros))
print("")

filtros = {
    'Marque': '',
    'Taille (pounce)': '',
    'CPU': '',
    'Type de stockage': '',
    'Taille SSD (Go)': '',
    'Taille HDD (Go)': '',
    "Ram (Go)": '',
    "Resolution": '',
    "Systeme dexploitation": "",
    "Lecteur/Graveur": "",
    'Proprietes': [''],
    "list_cpus" : ['Xeon', 'Core i7', 'Core i5', 'Ryzen', 'FX', 'Core i3', 'RX' ,'A10', 'PRO', 'A12'],    
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_laptop(filtros))
print("")

filtros = {
    'Marque': 'SAMSUNG',
    'Taille (pounce)': '',
    'CPU': '',
    'Type de stockage': '',
    'Taille SSD (Go)': '',
    'Taille HDD (Go)': '',
    "Ram (Go)": '',
    "Resolution": '',
    "Systeme dexploitation": "",
    "Lecteur/Graveur": "",
    'Proprietes': [''],
    "list_cpus" : []    
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_laptop(filtros))
print("")

filtros = {
    'Marque': 'SAMSUNG',
    'Taille (pounce)': '',
    'CPU': '',
    'Type de stockage': 'SSD',
    'Taille SSD (Go)': '64',
    'Taille HDD (Go)': '',
    "Ram (Go)": '',
    "Resolution": '',
    "Systeme dexploitation": "",
    "Lecteur/Graveur": "",
    'Proprietes': [''],
    "list_cpus" : []    
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_laptop(filtros))
print("")