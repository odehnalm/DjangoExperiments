def urlgen_laptop(filtros):    

    fields = {
        'cpu' : [],
        'marque' : '',
        'ram' : '',
        'taille' : '',
        'resolution' : '',
        'tactile' : '',
        'stockage' : '',
        'hdd' : '',
        'ssd' : '',
        'lecteur' : '',
        'os' : '',
    }

    url_pricerunner = 'http://www.pricerunner.fr/cl/27/Ordinateurs-portables'
      
    # MARQUE
    marca_request = ''
    if filtros['Marque'].upper() == 'ACER': marca_request = '?man_id=176'
    elif filtros['Marque'].upper() == 'AEG': marca_request = '?man_id=57'
    elif filtros['Marque'].upper() == 'ALCATEL': marca_request = '?man_id=50'
    elif filtros['Marque'].upper() == 'APPLE': marca_request = '?man_id=162'
    elif filtros['Marque'].upper() == 'ARCHOS': marca_request = '?man_id=484'
    elif filtros['Marque'].upper() == 'ASUS': marca_request = '?man_id=310'
    elif filtros['Marque'].upper() == 'BEA-FON': marca_request = '?man_id=123871'
    elif filtros['Marque'].upper() == 'BEKO': marca_request = '?man_id=157'
    elif filtros['Marque'].upper() == 'BLACKBERRY': marca_request = '?man_id=6145'
    elif filtros['Marque'].upper() == 'BLU': marca_request = '?man_id=63430'
    elif filtros['Marque'].upper() == 'BQ': marca_request = '?man_id=157606'
    elif filtros['Marque'].upper() == 'BOMANN': marca_request = '?man_id=6337'
    elif filtros['Marque'].upper() == 'BOSCH': marca_request = '?man_id=47'
    elif filtros['Marque'].upper() == 'BRANDT': marca_request = '?man_id=975'
    elif filtros['Marque'].upper() == 'BRANDYBEST': marca_request = '?man_id=22656'
    elif filtros['Marque'].upper() == 'BRONDI': marca_request = '?man_id=19346'
    elif filtros['Marque'].upper() == 'CANDY': marca_request = '?man_id=442'
    elif filtros['Marque'].upper() == 'CAT': marca_request = '?man_id=14054'
    elif filtros['Marque'].upper() == 'COOLPAD': marca_request = '?man_id=158416'
    elif filtros['Marque'].upper() == 'CROSSCALL': marca_request = '?man_id=149568'
    elif filtros['Marque'].upper() == 'CYRUS': marca_request = '?man_id=2178'
    elif filtros['Marque'].upper() == 'DAEWOO': marca_request = '?man_id=4'
    elif filtros['Marque'].upper() == 'DANEW': marca_request = '?man_id=18327'
    elif filtros['Marque'].upper() == 'DE DIETRICH': marca_request = '?man_id=974'
    elif filtros['Marque'].upper() == 'DELL': marca_request = '?man_id=571'
    elif filtros['Marque'].upper() == 'DENVER': marca_request = '?man_id=448'
    elif filtros['Marque'].upper() == 'DOMETIC': marca_request = '?man_id=6865'
    elif filtros['Marque'].upper() == 'DOOGEE': marca_request = '?man_id=154504'
    elif filtros['Marque'].upper() == 'DORO': marca_request = '?man_id=69'
    elif filtros['Marque'].upper() == 'DOMO': marca_request = '?man_id=17595'
    elif filtros['Marque'].upper() == 'ELECTROLUX': marca_request = '?man_id=51'
    elif filtros['Marque'].upper() == 'EMPORIA': marca_request = '?man_id=17663'
    elif filtros['Marque'].upper() == 'ENERGIZER': marca_request = '?man_id=159446'
    elif filtros['Marque'].upper() == 'ENERGY SYSTEM': marca_request = '?man_id=12221'
    elif filtros['Marque'].upper() == 'EXQUISIT': marca_request = '?man_id=79684'
    elif filtros['Marque'].upper() == 'FAURE': marca_request = '?man_id=1948'
    elif filtros['Marque'].upper() == 'FRIGELUX': marca_request = '?man_id=18037'
    elif filtros['Marque'].upper() == 'FUJITSU':marca_request = '?man_id=480'
    elif filtros['Marque'].upper() == 'GEEMARC': marca_request = '?man_id=456'
    elif filtros['Marque'].upper() == 'GIGABYTE':marca_request = '?man_id=421'
    elif filtros['Marque'].upper() == 'GIGASET': marca_request = '?man_id=123828'
    elif filtros['Marque'].upper() == 'GOCLEVER': marca_request = '?man_id=146460'
    elif filtros['Marque'].upper() == 'GOOGLE': marca_request = '?man_id=120258'
    elif filtros['Marque'].upper() == 'GORENJE': marca_request = '?man_id=601'
    elif filtros['Marque'].upper() == 'HAIER': marca_request = '?man_id=2692'
    elif filtros['Marque'].upper() == 'HIGH TECH PLACE': marca_request = '?man_id=146025'
    elif filtros['Marque'].upper() == 'HISENSE': marca_request = '?man_id=10176'
    elif filtros['Marque'].upper() == 'HONEYWELL': marca_request = '?man_id=20010'
    elif filtros['Marque'].upper() == 'HOTPOINT': marca_request = '?man_id=963'
    elif filtros['Marque'].upper() == 'HOTPOINT-ARISTON': marca_request = '?man_id=30820'
    elif filtros['Marque'].upper() == 'HP': marca_request = '?man_id=11563'
    elif filtros['Marque'].upper() == 'HTC': marca_request = '?man_id=17987'
    elif filtros['Marque'].upper() == 'HUAWEI': marca_request = '?man_id=17349'
    elif filtros['Marque'].upper() == 'ICE': marca_request = '?man_id=14193'
    elif filtros['Marque'].upper() == 'INDESIT': marca_request = '?man_id=966'
    elif filtros['Marque'].upper() == 'INFINIX': marca_request = '?man_id=155078'
    elif filtros['Marque'].upper() == 'ITTM': marca_request = '?man_id=125489'
    elif filtros['Marque'].upper() == 'KAZAM': marca_request = '?man_id=153992'
    elif filtros['Marque'].upper() == 'KLARSTEIN': marca_request = '?man_id=23200'
    elif filtros['Marque'].upper() == 'KRUGER & MATZ': marca_request = '?man_id=148190'
    elif filtros['Marque'].upper() == 'LENOVO': marca_request = '?man_id=7227'
    elif filtros['Marque'].upper() == 'LG': marca_request = '?man_id=30'
    elif filtros['Marque'].upper() == 'LIEBHERR': marca_request = marca_request = '?man_id=973'
    elif filtros['Marque'].upper() == 'MAXCOM': marca_request = '?man_id=18188'
    elif filtros['Marque'].upper() == 'MEDIACOM': marca_request = '?man_id=109879'
    elif filtros['Marque'].upper() == 'MEDION': marca_request = '?man_id=572'
    elif filtros['Marque'].upper() == 'MEIZU': marca_request = '?man_id=10037'
    elif filtros['Marque'].upper() == 'MICROSOFT': marca_request = '?man_id=745'
    elif filtros['Marque'].upper() == 'MIELE': marca_request = '?man_id=149'
    elif filtros['Marque'].upper() == 'MOBISTEL': marca_request = '?man_id=22819'
    elif filtros['Marque'].upper() == 'MOTO': marca_request = '?man_id=212337'
    elif filtros['Marque'].upper() == 'MOTOROLA': marca_request = '?man_id=49'
    elif filtros['Marque'].upper() == 'MSI': marca_request = '?man_id=7849'
    elif filtros['Marque'].upper() == 'MTT': marca_request = '?man_id=124823'
    elif filtros['Marque'].upper() == 'MYPHONE': marca_request = '?man_id=23230'
    elif filtros['Marque'].upper() == 'MYWIGO': marca_request = '?man_id=160841'
    elif filtros['Marque'].upper() == 'NEFF': marca_request = '?man_id=970'
    elif filtros['Marque'].upper() == 'NOKIA': marca_request = '?man_id=15'
    elif filtros['Marque'].upper() == 'NUBIA': marca_request = '?man_id=165473'
    elif filtros['Marque'].upper() == 'OLYMPIA': marca_request = '?man_id=11328'
    elif filtros['Marque'].upper() == 'PACKARD BELL' : marca_request = '?man_id=551'
    elif filtros['Marque'].upper() == 'PALM': marca_request = '?man_id=2087'
    elif filtros['Marque'].upper() == 'PANASONIC': marca_request = '?man_id=17'
    elif filtros['Marque'].upper() == 'PHICOM': marca_request = '?man_id=148973'
    elif filtros['Marque'].upper() == 'POLAROID': marca_request = '?man_id=1817'
    elif filtros['Marque'].upper() == 'PRESTIGIO': marca_request = '?man_id=7768'
    elif filtros['Marque'].upper() == 'PRIMUX': marca_request = '?man_id=157542'
    elif filtros['Marque'].upper() == 'RUGGEAR': marca_request = '?man_id=154935'
    elif filtros['Marque'].upper() == 'SAMSUNG': marca_request = '?man_id=22'
    elif filtros['Marque'].upper() == 'SEVERIN': marca_request = '?man_id=1925'
    elif filtros['Marque'].upper() == 'SISWOO': marca_request = '?man_id=163238'
    elif filtros['Marque'].upper() == 'SHARP': marca_request = '?man_id=24'
    elif filtros['Marque'].upper() == 'SIEMENS': marca_request = '?man_id=46'
    elif filtros['Marque'].upper() == 'SMEG': marca_request = '?man_id=624'
    elif filtros['Marque'].upper() == 'SONY': marca_request = '?man_id=25'
    elif filtros['Marque'].upper() == 'SWISSTONE': marca_request = '?man_id=124627'
    elif filtros['Marque'].upper() == 'SWITEL': marca_request = '?man_id=17999'
    elif filtros['Marque'].upper() == 'TECMOBILE': marca_request = '?man_id=149612'
    elif filtros['Marque'].upper() == 'TELEFUNKEN': marca_request = '?man_id=27'
    elif filtros['Marque'].upper() == 'TELME': marca_request = '?man_id=167317'
    elif filtros['Marque'].upper() == 'THOMSON': marca_request = '?man_id=28'
    elif filtros['Marque'].upper() == 'TOSHIBA':marca_request = '?man_id=314'
    elif filtros['Marque'].upper() == 'TRISTAR': marca_request = '?man_id=17465'
    elif filtros['Marque'].upper() == 'TINITELL': marca_request = '?man_id=224698'
    elif filtros['Marque'].upper() == 'TIPTEL': marca_request = '?man_id=11802'
    elif filtros['Marque'].upper() == 'TP-LINK': marca_request = '?man_id=17455'
    elif filtros['Marque'].upper() == 'TTFONE': marca_request = '?man_id=147169'
    elif filtros['Marque'].upper() == 'VIEWSONIC': marca_request = '?man_id=192'
    elif filtros['Marque'].upper() == 'WAECO': marca_request = '?man_id=17356'
    elif filtros['Marque'].upper() == 'WHIRLPOOL': marca_request = '?man_id=56'
    elif filtros['Marque'].upper() == 'WIKO': marca_request = '?man_id=125812'
    elif filtros['Marque'].upper() == 'WILEYFOX': marca_request = '?man_id=162199'
    elif filtros['Marque'].upper() == 'WOXTER': marca_request = '?man_id=18921'
    elif filtros['Marque'].upper() == 'XIAOMI': marca_request = '?man_id=156555'
    elif filtros['Marque'].upper() == 'YARVIK': marca_request = '?man_id=125391'
    elif filtros['Marque'].upper() == 'YEZZ': marca_request = '?man_id=157221'    
    elif filtros['Marque'].upper() == 'ZANUSSI': marca_request = '?man_id=58'
    elif filtros['Marque'].upper() == 'ZOPO': marca_request = '?man_id=149039'    
    elif filtros['Marque'].upper() == 'ZTE': marca_request = '?man_id=17971'
    
    fields['marque'] = marca_request

    # CPU
    selected_cpu = False
    if filtros['list_cpus'] != [] and filtros['list_cpus'] != [""] and filtros['list_cpus'] != "":
        selected_cpu = True

    #                    INTEL

        if 'Atom' in filtros['list_cpus']:
            fields['cpu'].append("60382369")
        if 'Celeron' in filtros['list_cpus']:
            fields['cpu'].append("60382370")
        if 'Pentium' in filtros['list_cpus']:
            fields['cpu'].append("60382382")
        if 'Xeon' in filtros['list_cpus']:
            fields['cpu'].append("60382384")
        if 'Core2' in filtros['list_cpus']:
            fields['cpu'].append("60382372")
        if 'Core M' in filtros['list_cpus']:
            fields['cpu'].append("60382378")
        if 'Core i3' in filtros['list_cpus']:
            fields['cpu'].append("60382373")
        if 'Core M3' in filtros['list_cpus']:
            fields['cpu'].append("60382379")
        if 'Core i5' in filtros['list_cpus']:
            fields['cpu'].append("60382374")
        if 'Core M5' in filtros['list_cpus']:
            fields['cpu'].append("60382380")
        if 'Core i7' in filtros['list_cpus']:
            fields['cpu'].append("60382375")
        if 'Core M7' in filtros['list_cpus']:
            fields['cpu'].append("60382381")

        #                     AMD

        if 'E' in filtros['list_cpus'] or 'E1' in filtros['list_cpus'] or 'E2' in filtros['list_cpus']:
            fields['cpu'].append("60382346")
        if 'A4' in filtros["list_cpus"] or 'A6' in filtros["list_cpus"] or 'A6' in filtros["list_cpus"] or 'A8' in filtros["list_cpus"] or 'A9' in filtros["list_cpus"] or 'A10' in filtros["list_cpus"] or 'A12' in filtros["list_cpus"]:
            fields['cpu'].append("60382336")
        if 'A4' in filtros["list_cpus"]:
            fields['cpu'].append("60382339")
        if 'A10' in filtros["list_cpus"]:
            fields['cpu'].append("60382337")
        if 'Fusion' in filtros["list_cpus"]:
            fields['cpu'].append("60382347")

    # RAM
    if filtros['Ram (Go)'] != '':
        if float(filtros['Ram (Go)']) <= 2:
            fields['ram'] = '&attr_60382316=60382323%2C60382326%2C60382329%2C60382332%2C60382333%2C60382325%2C60382322%2C60382321'
        elif filtros['Ram (Go)'] == '3':
            fields['ram'] = '&attr_60382316=60382323%2C60382326%2C60382329%2C60382332%2C60382333%2C60382325%2C60382322'
        elif filtros['Ram (Go)'] == '4':
            fields['ram'] = '&attr_60382316=60382323%2C60382326%2C60382329%2C60382332%2C60382333%2C60382325'
        elif filtros['Ram (Go)'] == '6':
            fields['ram'] = '&attr_60382316=60382326%2C60382329%2C60382332%2C60382333%2C60382325'
        elif filtros['Ram (Go)'] == '8':
            fields['ram'] = '&attr_60382316=60382326%2C60382329%2C60382332%2C60382333'
        elif filtros['Ram (Go)'] in {'12','16'}:
            fields['ram'] = '&attr_60382316=60382329%2C60382332%2C60382333'
        elif filtros['Ram (Go)'] == {'20','24','32'}:
            fields['ram'] = '&attr_60382316=60382332%2C60382333'
        elif filtros['Ram (Go)'] == '64':
            fields['ram'] = '&attr_60382316=60382333'

    # TAILLE
    if filtros['Taille (pounce)'] == "Jusqu'à 8":
        fields['taille'] = '&s_54120131=0_9'
    elif filtros['Taille (pounce)'] == "10":
        fields['taille'] = '&s_54120131=9_11'
    elif filtros['Taille (pounce)'] == "11":
        fields['taille'] = '&s_54120131=10_12'
    elif filtros['Taille (pounce)'] == "12":
        fields['taille'] = '&s_54120131=11_13'
    elif filtros['Taille (pounce)'] == "13":
        fields['taille'] = '&s_54120131=12_14'
    elif filtros['Taille (pounce)'] == "14":
        fields['taille'] = '&s_54120131=13_15'
    elif filtros['Taille (pounce)'] == "15":
        fields['taille'] = '&s_54120131=14_16'
    elif filtros['Taille (pounce)'] == "17":
        fields['taille'] = '&s_54120131=15_18'
    elif filtros['Taille (pounce)'] == "Plus de 18":
        fields['taille'] = '&s_54120131=17_20'

    # RESOLUTION
    if filtros["Resolution"] == 'HD_Ready':
        fields['resolution'] = '&attr_60382392=60382401%2C60382397%2C60382398%2C60382394%2C60382396%2C60382399%2C60382400'
    elif filtros["Resolution"] == 'HD+':
        fields['resolution'] = '&attr_60382392=60382401%2C60382399%2C60382400%2C60382402%2C60382403%2C60382404%2C60382406'
    elif filtros["Resolution"] == 'Full_HD':
        fields['resolution'] = '&attr_60382392=60382401%2C60382402%2C60382403%2C60382404%2C60382406%2C60382409%2C60382412'
    elif filtros["Resolution"] == 'QHD':
        fields['resolution'] = '&attr_60382392=60382412%2C60382415%2C60382413%2C60382409%2C60382406%2C60382404%2C60382402'
    elif filtros["Resolution"] == 'Ultra_HD_(4K)':
        fields['resolution'] = '&attr_60382392=60382401%2C60382402%2C60382403%2C60382404%2C60382406%2C60382409%2C60382412'

    # PROPRIETES
    # IPS evitado por bajos resultados
    if 'Ecran tactile' in filtros['Proprietes']:
        fields['tactile'] = '&attr_60385652=60385653'

    # TYPE DE STOCKAGE
    # if filtros['Type de stockage'] in {'IDE', 'SATA'}:
    #     fields['stockage'] = '&attr_54120148=54120466%2C54120468'
    # if filtros['Type de stockage'] == 'SSD':
    #     fields['stockage'] = '&attr_54120148=54120468'

    # TAILLE HDD
    if filtros['Taille HDD (Go)'] != '':
        if float(filtros['Taille HDD (Go)']) >= 2000:
            fields['hdd'] = '&attr_60382490=60382516'
        elif float(filtros['Taille HDD (Go)']) >= 1000:
            fields['hdd'] = '&attr_60382490=60382516%2C60382513'
        elif float(filtros['Taille HDD (Go)']) >= 750:
            fields['hdd'] = '&attr_60382490=60382516%2C60382512%2C60382513'
        elif float(filtros['Taille HDD (Go)']) >= 640:
            fields['hdd'] = '&attr_60382490=60382516%2C60382512%2C60382511%2C60382513'
        elif float(filtros['Taille HDD (Go)']) >= 500:
            fields['hdd'] = '&attr_60382490=60382516%2C60382512%2C60382511%2C60382513%2C60382510'
        elif float(filtros['Taille HDD (Go)']) >= 320:
            fields['hdd'] = '&attr_60382490=60382516%2C60382512%2C60382511%2C60382507%2C60382513%2C60382510'

    # TAILLE SSD
    if filtros['Taille SSD (Go)'] != '':
        if float(filtros['Taille SSD (Go)']) >= 1500:
            fields['ssd'] = '&attr_60382519=60382548'
        elif float(filtros['Taille SSD (Go)']) >= 1000:
            fields['ssd'] = '&attr_60382519=60382547%2C60382548'
        elif float(filtros['Taille SSD (Go)']) >= 512:
            fields['ssd'] = '&attr_60382519=60382545%2C60382547%2C60382548'
        elif float(filtros['Taille SSD (Go)']) >= 256:
            fields['ssd'] = '&attr_60382519=60382538%2C60382545%2C60382547%2C60382548'
        elif float(filtros['Taille SSD (Go)']) >= 128:
            fields['ssd'] = '&attr_60382519=60382532%2C60382538%2C60382545%2C60382533%2C60382534%2C60382547%2C60382548'
        elif float(filtros['Taille SSD (Go)']) >= 64:
            fields['ssd'] = '&attr_60382519=60382532%2C60382538%2C60382545%2C60382528%2C60382533%2C60382534%2C60382547%2C60382548'
        elif float(filtros['Taille SSD (Go)']) >= 32:
            fields['ssd'] = '&attr_60382519=60382526%2C60382532%2C60382538%2C60382545%2C60382528%2C60382533%2C60382534%2C60382547%2C60382548'

    # LECTEUR/GRAVEUR
    # if filtros['Lecteur/Graveur'] != "":
    #     if filtros['Lecteur/Graveur'] == "Aucun Lecteur":
    #         fields['lecteur'] = '&attr_54120195=54120496'
    #     elif filtros['Lecteur/Graveur'] in {"CD-ROM", "CD-RW/DVD-ROM", "DVD-ROM", "Graveur DVD"}:
    #         fields['lecteur'] = '&attr_54120195=54120495%2C60382334%2C54120646'
    #     elif filtros['Lecteur/Graveur'] == "Lecteur Blur-ray/DVD+-RW Combo":
    #         fields['lecteur'] = '&attr_54120195=54120495%2C54120646'
    #     elif filtros['Lecteur/Graveur'] == "Graveur Blu-ray":
    #         fields['lecteur'] = '&attr_54120195=54120495'

    # SYSTEME DEXPLOITATION
    if 'Windows' in filtros["Systeme dexploitation"]:
        fields['os'] = '&attr_57921602=60384117'
    elif 'Mac' in filtros["Systeme dexploitation"]:
        fields['os'] = '&attr_57921602=57923063'
        
    # ---- URL
    if fields['marque']:
        url_pricerunner +=  fields['marque']
    if selected_cpu:
        url_pricerunner += "&attr_60382335=" + "%2C".join(fields['cpu'])
    if fields['ram']:
        url_pricerunner += fields['ram']
    if fields['taille']:
        url_pricerunner += fields['taille']
    if fields['resolution']:
        url_pricerunner += fields['resolution']
    if fields['tactile']:
        url_pricerunner += fields['tactile']
    if fields['stockage']:
        url_pricerunner += fields['stockage']    
    if fields['hdd']:
        url_pricerunner += fields['hdd']     
    if fields['ssd']:
        url_pricerunner += fields['ssd']     
    if fields['lecteur']:
        url_pricerunner += fields['lecteur']  
    if fields['os']:
        url_pricerunner += fields['os']                             

    #SORT
    url_pricerunner += '&sort=3'

    # Limpieza: el primer filtro va en #
    for i in range(len(url_pricerunner)):
        if url_pricerunner[i] == '&':
            url_pricerunner = url_pricerunner[:i] + '#' + url_pricerunner[i + 1:]
            break


    return url_pricerunner

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