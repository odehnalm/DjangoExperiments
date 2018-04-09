def urlgen_tv(filtros):

    fields = {
        'type': '',
        'marque': '',
        'taille': '',
        'resolution': '',
        'design' : '',
        'energy' : '',
        'smart' : '',
        '3d' : '',
        'wifi' : '',
    }

    url_pricerunner = 'http://www.pricerunner.fr/cl/2/Televiseurs'
      
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
    elif filtros['Marque'].upper() == 'CHANGHONG': marca_request = '?man_id=21239'
    elif filtros['Marque'].upper() == 'COOLPAD': marca_request = '?man_id=158416'
    elif filtros['Marque'].upper() == 'CROSSCALL': marca_request = '?man_id=149568'
    elif filtros['Marque'].upper() == 'CYRUS': marca_request = '?man_id=2178'
    elif filtros['Marque'].upper() == 'DAEWOO': marca_request = '?man_id=4'
    elif filtros['Marque'].upper() == 'DANEW': marca_request = '?man_id=18327'
    elif filtros['Marque'].upper() == 'DE DIETRICH': marca_request = '?man_id=974'
    elif filtros['Marque'].upper() == 'DENVER': marca_request = '?man_id=448'
    elif filtros['Marque'].upper() == 'DOMETIC': marca_request = '?man_id=6865'
    elif filtros['Marque'].upper() == 'DOOGEE': marca_request = '?man_id=154504'
    elif filtros['Marque'].upper() == 'DORO': marca_request = '?man_id=69'
    elif filtros['Marque'].upper() == 'DOMO': marca_request = '?man_id=17595'
    elif filtros['Marque'].upper() == 'ELECTROLUX': marca_request = '?man_id=51'
    elif filtros['Marque'].upper() == 'EMPORIA': marca_request = '?man_id=17663'
    elif filtros['Marque'].upper() == 'ENERGIZER': marca_request = '?man_id=159446'
    elif filtros['Marque'].upper() == 'ENERGY SYSTEM': marca_request = '?man_id=12221'
    elif filtros['Marque'].upper() == 'ESSENTIELB': marca_request = '?man_id=21246'
    elif filtros['Marque'].upper() == 'EXQUISIT': marca_request = '?man_id=79684'
    elif filtros['Marque'].upper() == 'FAURE': marca_request = '?man_id=1948'
    elif filtros['Marque'].upper() == 'FRIGELUX': marca_request = '?man_id=18037'
    elif filtros['Marque'].upper() == 'FINLUX': marca_request = '?man_id=5'
    elif filtros['Marque'].upper() == 'GEEMARC': marca_request = '?man_id=456'
    elif filtros['Marque'].upper() == 'GIGASET': marca_request = '?man_id=123828'
    elif filtros['Marque'].upper() == 'GOCLEVER': marca_request = '?man_id=146460'
    elif filtros['Marque'].upper() == 'GOOGLE': marca_request = '?man_id=120258'
    elif filtros['Marque'].upper() == 'GORENJE': marca_request = '?man_id=601'
    elif filtros['Marque'].upper() == 'GRUNDIG': marca_request = '?man_id=8'
    elif filtros['Marque'].upper() == 'HAIER': marca_request = '?man_id=2692'
    elif filtros['Marque'].upper() == 'HIGH TECH PLACE': marca_request = '?man_id=146025'
    elif filtros['Marque'].upper() == 'HISENSE': marca_request = '?man_id=10176'
    elif filtros['Marque'].upper() == 'HITACHI': marca_request = '?man_id=9'
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
    elif filtros['Marque'].upper() == 'LIEBHERR': marca_request = '?man_id=973'
    elif filtros['Marque'].upper() == 'LISTO': marca_request = '?man_id=20245'
    elif filtros['Marque'].upper() == 'LOEWE':marca_request = '?man_id=477'
    elif filtros['Marque'].upper() == 'MAJECTIC':marca_request = '?man_id=9707'
    elif filtros['Marque'].upper() == 'MAXCOM': marca_request = '?man_id=18188'
    elif filtros['Marque'].upper() == 'MEDIACOM': marca_request = '?man_id=109879'
    elif filtros['Marque'].upper() == 'MEDION': marca_request = '?man_id=572'
    elif filtros['Marque'].upper() == 'MEIZU': marca_request = '?man_id=10037'
    elif filtros['Marque'].upper() == 'MICROSOFT': marca_request = '?man_id=745'
    elif filtros['Marque'].upper() == 'MIELE': marca_request = '?man_id=149'
    elif filtros['Marque'].upper() == 'MOBISTEL': marca_request = '?man_id=22819'
    elif filtros['Marque'].upper() == 'MOTO': marca_request = '?man_id=212337'
    elif filtros['Marque'].upper() == 'MOTOROLA': marca_request = '?man_id=49'
    elif filtros['Marque'].upper() == 'MTT': marca_request = '?man_id=124823'
    elif filtros['Marque'].upper() == 'MYPHONE': marca_request = '?man_id=23230'
    elif filtros['Marque'].upper() == 'MYWIGO': marca_request = '?man_id=160841'
    elif filtros['Marque'].upper() == 'NEFF': marca_request = '?man_id=970'
    elif filtros['Marque'].upper() == 'NOKIA': marca_request = '?man_id=15'
    elif filtros['Marque'].upper() == 'NUBIA': marca_request = '?man_id=165473'
    elif filtros['Marque'].upper() == 'OLYMPIA': marca_request = '?man_id=11328'
    elif filtros['Marque'].upper() == 'PALM': marca_request = '?man_id=2087'
    elif filtros['Marque'].upper() == 'PANASONIC': marca_request = '?man_id=17'
    elif filtros['Marque'].upper() == 'PHICOM': marca_request = '?man_id=148973'
    elif filtros['Marque'].upper() == 'PHILIPS': marca_request = '?man_id=18'
    elif filtros['Marque'].upper() == 'POLAROID': marca_request = '?man_id=1817'
    elif filtros['Marque'].upper() == 'PRESTIGIO': marca_request = '?man_id=7768'
    elif filtros['Marque'].upper() == 'PRIMUX': marca_request = '?man_id=157542'
    elif filtros['Marque'].upper() == 'REFLECTION':marca_request = '?man_id=17818'
    elif filtros['Marque'].upper() == 'RUGGEAR': marca_request = '?man_id=154935'
    elif filtros['Marque'].upper() == 'SAMSUNG': marca_request = '?man_id=22'
    elif filtros['Marque'].upper() == 'SEVERIN': marca_request = '?man_id=1925'
    elif filtros['Marque'].upper() == 'SISWOO': marca_request = '?man_id=163238'
    elif filtros['Marque'].upper() == 'SHARP': marca_request = '?man_id=24'
    elif filtros['Marque'].upper() == 'SIEMENS': marca_request = '?man_id=46'
    elif filtros['Marque'].upper() == 'SKYWORTH':marca_request = '?man_id=21273'
    elif filtros['Marque'].upper() == 'SMEG': marca_request = '?man_id=624'
    elif filtros['Marque'].upper() == 'SONY': marca_request = '?man_id=25'
    elif filtros['Marque'].upper() == 'STRONG': marca_request = '?man_id=2214'
    elif filtros['Marque'].upper() == 'SWISSTONE': marca_request = '?man_id=124627'
    elif filtros['Marque'].upper() == 'SWITEL': marca_request = '?man_id=17999'
    elif filtros['Marque'].upper() == 'TCL': marca_request = '?man_id=6991'
    elif filtros['Marque'].upper() == 'TECMOBILE': marca_request = '?man_id=149612'
    elif filtros['Marque'].upper() == 'TELEFUNKEN': marca_request = '?man_id=27'
    elif filtros['Marque'].upper() == 'TELME': marca_request = '?man_id=167317'
    elif filtros['Marque'].upper() == 'THOMSON': marca_request = '?man_id=28'
    elif filtros['Marque'].upper() == 'TRISTAR': marca_request = '?man_id=17465'
    elif filtros['Marque'].upper() == 'TINITELL': marca_request = '?man_id=224698'
    elif filtros['Marque'].upper() == 'TIPTEL': marca_request = '?man_id=11802'
    elif filtros['Marque'].upper() == 'TOSHIBA': marca_request = '?man_id=314'
    elif filtros['Marque'].upper() == 'TP-LINK': marca_request = '?man_id=17455'
    elif filtros['Marque'].upper() == 'TTFONE': marca_request = '?man_id=147169'
    elif filtros['Marque'].upper() == 'VIEWSONIC': marca_request = '?man_id=192'
    elif filtros['Marque'].upper() == 'WAECO': marca_request = '?man_id=17356'
    elif filtros['Marque'].upper() == 'WHIRLPOOL': marca_request = '?man_id=56'
    elif filtros['Marque'].upper() == 'WIKO': marca_request = '?man_id=125812'
    elif filtros['Marque'].upper() == 'WILEYFOX': marca_request = '?man_id=162199'
    elif filtros['Marque'].upper() == 'WOXTER': marca_request = '?man_id=18921'
    elif filtros['Marque'].upper() == 'XIAOMI': marca_request = '?man_id=156555'
    elif filtros['Marque'].upper() == 'XORO': marca_request = '?man_id=6319'
    elif filtros['Marque'].upper() == 'YARVIK': marca_request = '?man_id=125391'
    elif filtros['Marque'].upper() == 'YEZZ': marca_request = '?man_id=157221'    
    elif filtros['Marque'].upper() == 'ZANUSSI': marca_request = '?man_id=58'
    elif filtros['Marque'].upper() == 'ZOPO': marca_request = '?man_id=149039'    
    elif filtros['Marque'].upper() == 'ZTE': marca_request = '?man_id=17971'
    
    fields['marque'] = marca_request
    
    # TAILLE
    if filtros['TaillePounce'] != 'null' and filtros['TaillePounce'] != '0' and filtros['TaillePounce'] != '':
        fields['taille'] = '&s_2000000={0}_100'.format(int(float(filtros['TaillePounce'])))

    # TAILLE ECRAN
    if filtros['Type'] == 'OLED':
        fields['type'] = '&attr_2=40005596'
    
    # RESOLUTION
    if filtros['Resolution'][0] == '720p':
        fields['resolution'] = '&attr_59671628=59671631%2C59671630%2C5967162'
    elif filtros['Resolution'][0] == '1080p':
        fields['resolution'] = '&attr_59671628=59671630%2C59671629'
    elif filtros['Resolution'][0].lower() == '4k':
        fields['resolution'] = '&attr_59671628=59671629'

    #3D
    if filtros['3D'] == 'Oui':
        fields['3d'] = '&attr_47421171=60269395'

    #WIFI
    if filtros['Wifi'] == 'Oui':
        fields['wifi'] = '&attr_60045863=60045864'

    #SMART
    if filtros['Smart'] == 'Oui':
        fields['smart'] = '&attr_49210333=60269397'

    # DESIGN
    if 'Incurve' in filtros['Design'] or 'incurve' in filtros['Design']:
        fields['design'] = '&attr_58191861=60045790'

    # ENERGY
    if filtros['Energy'] == 'B':
        fields['energy'] = '&attr_57477290=57479666%2C57479665%2C57479664%2C57479663'
    elif filtros['Energy'] == 'A':
        fields['energy'] = '&attr_57477290=57479665%2C57479664%2C57479663'
    elif filtros['Energy'] == 'A+':
        fields['energy'] = '&attr_57477290=57479664%2C57479663'
    elif filtros['Energy'] == 'A++':
        fields['energy'] = '&attr_57477290=57479663'

    # ---- URL
    if fields['marque']:
        url_pricerunner +=  fields['marque']
    if fields['taille']:
        url_pricerunner += fields['taille']
    if fields['type']:
        url_pricerunner += fields['type']
    if fields['resolution']:
        url_pricerunner += fields['resolution']
    if fields['3d']:
        url_pricerunner += fields['3d']
    if fields['wifi']:
        url_pricerunner += fields['wifi']
    if fields['smart']:
        url_pricerunner += fields['smart']    
    if fields['design']:
        url_pricerunner += fields['design']     
    if fields['energy']:
        url_pricerunner += fields['energy']                

    #SORT
    url_pricerunner += '&sort=3'

    # Limpieza: el primer filtro va en #
    for i in range(len(url_pricerunner)):
        if url_pricerunner[i] == '&':
            url_pricerunner = url_pricerunner[:i] + '#' + url_pricerunner[i + 1:]
            break

    return url_pricerunner

filtros = {
    'Marque': 'SAMSUNG',
    "TaillePounce": '50',
    "Type": 'OLED',
    "Resolution": ['4k'],
    "Ratio": [''],
    "3D": "",
    "Design" : ["Incurve"],
    "Wifi" : "",
    "Smart" : "",
    "Energy" : "",
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("")    

filtros = {
    'Marque': '',
    "TaillePounce": '',
    "Type": 'OLED',
    "Resolution": [''],
    "Ratio": [''],
    "3D": "",
    "Design" : "",
    "Wifi" : "",
    "Smart" : "",
    "Energy" : "",
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("")  

filtros = {
    'Marque': 'SAMSUNG',
    "TaillePounce": '50',
    "Type": 'LED',
    "Resolution": ['1080p'],
    "Ratio": [''],
    "3D": "Oui",
    "Design" : "",
    "Wifi" : "",
    "Smart" : "",
    "Energy" : "",
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("") 

filtros = {
    'Marque': 'PHILIPS',
    "TaillePounce": '50',
    "Type": 'LED',
    "Resolution": ['1080p'],
    "Ratio": [''],
    "3D": "Oui",
    "Design" : "",
    "Wifi" : "Oui",
    "Smart" : "Oui",
    "Energy" : "A",
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("") 

filtros = {
    'Marque': '',
    "TaillePounce": '',
    "Type": '',
    "Resolution": [''],
    "Ratio": [''],
    "3D": "",
    "Design" : "",
    "Wifi" : "",
    "Smart" : "",
    "Energy" : "",
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("") 