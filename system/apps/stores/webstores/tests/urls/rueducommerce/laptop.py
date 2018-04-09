# -*- coding: utf-8 -*-
def urlgen_laptop(filtros):

    fields = {
        'url_base': '',
        'it_display_size_max_pouces': '',
        'marque': '',
        'it_cpu_type': [],
        'it_storage_type': '',
        'it_data_storage_ssd_capacity_go': '',
        'it_memory_ram_installed_go': '',
        'it_computer_os_type': '',
        'it_burner_driver_type_computer': '',
        'it_is_tactile': '',
        'it_panel_type': ''
    }

    is_apple = False

    fields['url_base'] = "https://www.rueducommerce.fr/rayon/ordinateurs-64/pc-portable-5875?sort=prix-croissants&view=list"

    # MARQUE
    if filtros["Marque"] != "":

        marque = filtros["Marque"].lower().replace(" ","-")

        if marque == "apple":
            is_apple = True
            fields['url_base'] = "https://www.rueducommerce.fr/rayon/ordinateurs-64/macbook-8022?sort=prix-croissants&view=list"
        else:
            fields['marque'] = filtros['Marque'].lower().replace(" ","-")

    # TAILLE
    if filtros['Taille (pounce)'] != '':
        if filtros['Taille (pounce)'] == "Jusqu'à 8":
            fields['it_display_size_max_pouces'] = ".".join(['{0}-{1}'.format(str(x)[:-1],str(x)[-1]) for x in range(70,81)])
        if filtros['Taille (pounce)'] == "10":
            fields['it_display_size_max_pouces'] = ".".join(['{0}-{1}'.format(str(x)[:-1],str(x)[-1]) for x in range(90, 101)])
        if filtros['Taille (pounce)'] == "11":
            fields['it_display_size_max_pouces'] = ".".join(['{0}-{1}'.format(str(x)[:-1],str(x)[-1]) for x in range(100, 111)])
        if filtros['Taille (pounce)'] == "12":
            fields['it_display_size_max_pouces'] = ".".join(['{0}-{1}'.format(str(x)[:-1],str(x)[-1]) for x in range(120, 131)])
        if filtros['Taille (pounce)'] == "13":
            fields['it_display_size_max_pouces'] = ".".join(['{0}-{1}'.format(str(x)[:-1],str(x)[-1]) for x in range(130, 141)])
        if filtros['Taille (pounce)'] == "14":
            fields['it_display_size_max_pouces'] = ".".join(['{0}-{1}'.format(str(x)[:-1],str(x)[-1]) for x in range(140, 151)])
        if filtros['Taille (pounce)'] == "15":
            fields['it_display_size_max_pouces'] = ".".join(['{0}-{1}'.format(str(x)[:-1],str(x)[-1]) for x in range(150, 161)])
        if filtros['Taille (pounce)'] == "16":
            fields['it_display_size_max_pouces'] = ".".join(['{0}-{1}'.format(str(x)[:-1],str(x)[-1]) for x in range(160, 171)])
        if filtros['Taille (pounce)'] == "17":
            fields['it_display_size_max_pouces'] = ".".join(['{0}-{1}'.format(str(x)[:-1],str(x)[-1]) for x in range(170, 181)])
        if filtros['Taille (pounce)'] == "Plus de 18":
            fields['it_display_size_max_pouces'] = ".".join(['{0}-{1}'.format(str(x)[:-1],str(x)[-1]) for x in range(180, 121)])

    # CPU
    if 'Atom' in filtros["list_cpus"]:
        fields['it_cpu_type'].append('intel-atom')

    if 'Celeron' in filtros["list_cpus"]:
        fields['it_cpu_type'].append('intel-celeron')
        
    if 'Pentium' in filtros["list_cpus"]:
        fields['it_cpu_type'].append('intel-pentium')

    if 'Core i3' in filtros["list_cpus"]:
        fields['it_cpu_type'].append('intel-core-i3')

    if 'Core i5' in filtros["list_cpus"]:
        fields['it_cpu_type'].append('intel-core-i5')

    if 'Core i7' in filtros["list_cpus"]:
        fields['it_cpu_type'].append('intel-core-i7')

    if 'E1' in filtros["list_cpus"]:
        fields['it_cpu_type'].append('amd-e1')

    if 'E2' in filtros["list_cpus"]:
        fields['it_cpu_type'].append('amd-e2')

    if 'A2' in filtros["list_cpus"]:
        fields['it_cpu_type'].append('amd-a2')
 
    if 'A4' in filtros["list_cpus"]:
        fields['it_cpu_type'].append('amd-a4')
 
    if 'A6' in filtros["list_cpus"]:
        fields['it_cpu_type'].append('amd-a6')
 
    if 'A8' in filtros["list_cpus"]:
        fields['it_cpu_type'].append('amd-a8')
                                 
    if 'A9' in filtros["list_cpus"]:
        fields['it_cpu_type'].append('amd-a9')
 
    if 'A10' in filtros["list_cpus"]:
        fields['it_cpu_type'].append('amd-a10')
    


    # TYPE DE STOCKAGE/ SSD
    if is_apple:
        if filtros['Taille SSD (Go)'] == "512" or\
                filtros['Taille SSD (Go)'] == "256" or\
                filtros['Taille SSD (Go)'] == "128":
            fields['it_data_storage_ssd_capacity_go'] = filtros['Taille SSD (Go)']
    else:
        if filtros['Type de stockage'] in {'SATA', "IDE"}:
            fields['it_storage_type'] = 'disque-dur'
        elif filtros['Type de stockage'] == 'SSD':
            fields['it_storage_type'] = 'ssd'
        elif filtros['Type de stockage'] == 'Hybride':
            fields['it_storage_type'] = 'disque-dur-ssd'

    # RAM
    if filtros["Ram (Go)"] != "":
        if filtros["Ram (Go)"] == '2':
            fields['it_memory_ram_installed_go'] = '2.4.6.8.16.32'
        elif filtros["Ram (Go)"] == '4':
            fields['it_memory_ram_installed_go'] = '4.6.8.16.32'
        elif filtros["Ram (Go)"] == '8':
            fields['it_memory_ram_installed_go'] = '8.16.32'
        elif filtros["Ram (Go)"] == '16':
            fields['it_memory_ram_installed_go'] = '16.32'
        elif filtros["Ram (Go)"] == '32':
            fields['it_memory_ram_installed_go'] = '32'

    if not is_apple:
        # SYSTEME DEXPLOITATION
        if filtros["Systeme dexploitation"] == "":
            fields['it_computer_os_type'] = 'windows.n-a'
        elif filtros["Systeme dexploitation"] in {"Windows 10","Windows 8","Windows 7"}:
            fields['it_computer_os_type'] = 'windows'

        # LECTEUR/GRAVEUR
        if filtros["Lecteur/Graveur"] != "":
            if filtros["Lecteur/Graveur"] == "Aucun Lecteur":
                fields['it_burner_driver_type_computer'] = "pas-de-lecteur-graveur"
            else:
                fields['it_burner_driver_type_computer'] = "lecteur-graveur-dvd"

        # PROPRIETES
        if 'Ecran tactile' in filtros['Proprietes']:
            fields['it_is_tactile'] = 'ecran-tactile'
        if 'Ecran brillant' in filtros['Proprietes'] or 'Ecran IPS' in filtros['Proprietes'] or 'Ecran mat' in filtros['Proprietes']:
            panel_type = []
            if 'Ecran brillant' in filtros['Proprietes']:
                panel_type.append('brillant')
            if 'Ecran IPS' in filtros['Proprietes']:
                panel_type.append('ips')
            if 'Ecran mat' in filtros['Proprietes']:
                panel_type.append('mate')
            fields['it_panel_type'] = ".".join(panel_type)

    url = fields['url_base']

    if fields['it_display_size_max_pouces']:
        url += '&it_display_size_max_pouces=' + fields['it_display_size_max_pouces']
    if fields['marque']:
        url += '&marque=' + fields['marque']
    if fields['it_cpu_type']:
        url += '&it_cpu_type=' + ".".join(fields['it_cpu_type'])
    if fields['it_storage_type']:
        url += '&it_storage_type=' + fields['it_storage_type']
    if fields['it_data_storage_ssd_capacity_go']:
        url += '&it_data_storage_ssd_capacity_go=' + fields['it_data_storage_ssd_capacity_go']
    if fields['it_memory_ram_installed_go']:
        url += '&it_memory_ram_installed_go=' + fields['it_memory_ram_installed_go']
    if fields['it_computer_os_type']:
        url += '&it_computer_os_type=' + fields['it_computer_os_type']
    if fields['it_burner_driver_type_computer']:
        url += '&it_burner_driver_type_computer=' + fields['it_burner_driver_type_computer']
    if fields['it_is_tactile']:
        url += '&it_is_tactile=' + fields['it_is_tactile']
    if fields['it_panel_type']:
        url += '&it_panel_type=' + fields['it_panel_type']

    return url


filtros = {
    'Marque': 'ASUS',
    'Taille (pounce)': '12',
    'CPU': 'Intel Core i3',
    'Type de stockage': 'SATA',
    "Ram (Go)": '8',
    "Systeme dexploitation": "Windows 8",
    "Lecteur/Graveur": "Aucun Lecteur",
    'Proprietes': [''],
    'list_cpus' : [],
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
    "Ram (Go)": '8',
    "Systeme dexploitation": "Apple iOS",
    "Lecteur/Graveur": "",
    'Proprietes': [''],
    'list_cpus' : [],    
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
    "Ram (Go)": '',
    "Systeme dexploitation": "",
    "Lecteur/Graveur": "",
    'Proprietes': [''],
    'list_cpus' : ['Xeon', 'Core i7', 'Core i5', 'Ryzen', 'FX', 'Core i3', 'RX' ,'A10', 'PRO', 'A12'],    
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_laptop(filtros))
print("")
