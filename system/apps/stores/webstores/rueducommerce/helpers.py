from math import log

from ...post_filter.laptop.utils import check_cpu, check_gpu

# ------- GENERADORES DE URL
def urlgen_tv(filtros, should_print):
    raise NotImplementedError


def urlgen_frigo(filtros, should_print):
    raise NotImplementedError


def urlgen_mobile(filtros, should_print):

    if filtros['Memoire'] == "null":
        filtros['Memoire'] = ""

    url_rueducommerce = "https://www.rueducommerce.fr/rayon/telephonie-92/smartphone-classique-6774?sort=prix-croissants&view=list"

    # MARQUE
    if filtros['Marque']:
        url_rueducommerce += '&marque=' + filtros['Marque'].lower().replace(' ', '-')

    # MEMOIRE
    if filtros['Memoire']:
        url_rueducommerce += '&it_memory_rom_integrated_go='
        gbnum = log(int(filtros['Memoire']), 2)
        for k in range(int(gbnum), 9):
            url_rueducommerce += '{0}.'.format(2**k)
        url_rueducommerce += 'n-a'

    # # COULEURS
    # if filtros['Couleur'] == 'Noir':
    #     url_rueducommerce += '&color_group=noir'
    # elif filtros['Couleur'] == 'Violet':
    #     url_rueducommerce += '&violet.mauve'
    # elif filtros['Couleur'] == 'Blanc':
    #     url_rueducommerce += '&color_group=blanc'
    # elif filtros['Couleur'] == 'Bleu':
    #     url_rueducommerce += '&color_group=bleu'
    # elif filtros['Couleur'] == 'Or':
    #     url_rueducommerce += '&color_group=dore'
    # elif filtros['Couleur'] in {'Gris', 'Argent'}:
    #     url_rueducommerce += '&color_group=argente.gris'
    # elif filtros['Couleur'] == 'Jaune':
    #     url_rueducommerce += '&color_group=jaune'
    # elif filtros['Couleur'] == 'Orange':
    #     url_rueducommerce += '&color_group=orange'
    # elif filtros['Couleur'] == 'Rose':
    #     url_rueducommerce += '&color_group=rose'
    # elif filtros['Couleur'] == 'Rouge':
    #     url_rueducommerce += '&color_group=rouge'
    # elif filtros['Couleur'] == 'Vert':
    #     url_rueducommerce += '&color_group=vert'
    # elif filtros['Couleur'] == 'Marron':
    #     url_rueducommerce += '&color_group=marron'

    # RESOLUTION
    if filtros['Resolution']:
        res_min = min([int(x) for x in filtros['Resolution'].split('x')])
        if res_min <= 720:
            url_rueducommerce += '&it_smartphone_resolution=4k-uhd.quad-hd.full-hd.hd'
        elif res_min <= 1080:
            url_rueducommerce += '&it_smartphone_resolution=4k-uhd.quad-hd.full-hd'
        elif res_min <= 1440:
            url_rueducommerce += '&it_smartphone_resolution=4k-uhd.quad-hd'
        elif res_min <= 2160:
            url_rueducommerce += '&it_smartphone_resolution=4k-uhd'

    # RAM
    if filtros['Ram'] and filtros['Ram'].replace(" ", "") != "null":
        if float(filtros['Ram']) <= 1:
            url_rueducommerce += '&it_memory_ram_installed_go=3.2.1-5.1'
        elif float(filtros['Ram']) <= 1.5:
            url_rueducommerce += '&it_memory_ram_installed_go=4.3.2.1.5'
        elif float(filtros['Ram']) <= 2:
            url_rueducommerce += '&it_memory_ram_installed_go=6.4.3.2'
        elif float(filtros['Ram']) <= 4:
            url_rueducommerce += '&it_memory_ram_installed_go=8.6.4'
        elif float(filtros['Ram']) <= 6:
            url_rueducommerce += '&it_memory_ram_installed_go=16.8.6'
        elif float(filtros['Ram']) <= 8:
            url_rueducommerce += '&it_memory_ram_installed_go=16.8'
        elif float(filtros['Ram']) <= 16:
            url_rueducommerce += '&it_memory_ram_installed_go=16'

    # OS
    if filtros['Systeme dexploitation']:
        if filtros['Systeme dexploitation'] == "Android":
            url_rueducommerce += '&it_tablette_os=android'
        elif filtros['Systeme dexploitation'] == "Apple iOS":
            url_rueducommerce += '&it_tablette_os=ios'

    # IMPRESION URL
    if should_print:
        print('URL de Rueducommerce:', '\n', url_rueducommerce)

    return url_rueducommerce


def urlgen_laptop(filtros, should_print):

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
    if filtros["list_cpus"]:
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


# -------- FILTROS POSTERIORES
def filter_mobile(query_products):
    list_products = []
    for p in query_products:
        product = {}
        product["name"] = p.nombre
        product["category_id"] = p.category_id
        product["store_id"] = p.store_id
        list_products.append(product)
    return list_products


def filter_laptop(query_products, filtros):
    list_products = []
    selected_cpu = False
    selected_gpu = False
    producto_guardado = False
    save_item = True

    rules = {
        'required_cpu': True,
        'required_gpu': False,
        'cpu_over_gpu': True
    }

    # Parametros de control
    parametros = {
        'cpu_ok': True,
        'gpu_ok': True
    }

    if filtros['CPUSpec']:
        selected_cpu = True
    if filtros['GPUSpec']:
        selected_gpu = True

    for p in query_products:

        # ------ CPU FILTER
        if selected_cpu:

            procesador = p.ficha_tecnica.get('Modèle du processeur portable', None)

            if procesador is not None:
                cpu_filter =  " ".join(procesador.split("(")[0].split())

                input_benchs = {
                    'procesador' : filtros['CPUSpec'],
                    'procesador_raw' : cpu_filter,
                }

                status_cpu = check_cpu(input_benchs)
                print("STATUS_CPU RUEDUCOMMERCE")
                print(status_cpu)
                parametros['cpu_ok'] = status_cpu['CPU']['es_valido']

            else:
                # Aplica regla acerca de items sin detalle de procesador
                if rules['required_cpu']:
                    parametros['cpu_ok'] = False     


        if selected_gpu:

            gpu_filter = p.ficha_tecnica.get('Chipset graphique', None)

            if gpu_filter is not None:

                input_benchs = {
                    'graficos' : filtros['GPUSpec'],
                    'graficos_raw' : gpu_filter,
                }

                status_gpu = check_gpu(input_benchs)
                parametros['gpu_ok'] = status_gpu['GPU']['es_valido']

            else:
                # Aplica regla acerca de items sin detalle de tarjeta grafica
                if rules['required_gpu']:
                    parametros['gpu_ok'] = False

        if parametros['cpu_ok'] and not parametros['gpu_ok'] and\
                not rules['required_gpu'] and rules['cpu_over_gpu']:

            # Si se halla item que satisface requisito de cpu,
            # y no se cumple requisito de gpu,
            # y no es requerido encontrar campo descriptor de gpu en
            # la ficha tecnica, y las reglas de la compania permiten
            # salvar el item si cumple con cpu...
            parametros['gpu_ok'] = True

        save_item = all(parametros.values()) 

        if save_item:
            product = {}
            product["name"] = p.nombre
            product["category_id"] = p.category_id
            product["store_id"] = p.store_id
            list_products.append(product)
        else:
            print("BORRANDO DE DB a ", p.nombre)
            p.delete()
        
    return list_products


def filter_frigo(query_products):
    list_products = []
    for p in query_products:
        product = {}
        product["name"] = p.nombre
        product["category_id"] = p.category_id
        product["store_id"] = p.store_id
        list_products.append(product)
    return list_products
