from math import log

def urlgen_mobile(filtros):

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

    # COULEURS
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

    return url_rueducommerce

filtros = {
    'Marque': 'SAMSUNG',
    'Memoire': '12',
    'Couleur': 'Violet',
    'Resolution': '480x1024',
    'Ram': '6',
    'Systeme dexploitation': 'Android'
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_mobile(filtros))
print("")

filtros = {
    'Marque': 'Apple',
    'Memoire': '4',
    'Couleur': '',
    'Resolution': '480x1024',
    'Ram': '2',
    'Systeme dexploitation': 'Apple iOS'
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_mobile(filtros))
print("")

filtros = {
    'Marque': 'Apple',
    'Memoire': '16',
    'Couleur': '',
    'Resolution': '1080x1920',
    'Ram': '2',
    'Systeme dexploitation': 'Apple iOS'
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_mobile(filtros))
print("")

filtros = {
    'Marque': '',
    'Memoire': '',
    'Couleur': '',
    'Resolution': '',
    'Ram': '6',
    'Systeme dexploitation': ''
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_mobile(filtros))
print("")
