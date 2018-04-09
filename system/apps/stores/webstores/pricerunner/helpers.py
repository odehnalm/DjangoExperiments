from ...post_filter.laptop.utils import check_cpu, check_gpu

# ------- GENERADORES DE URL
def urlgen_tv(filtros, should_print):

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


def urlgen_refrigerador(filtros, should_print):

    url_pricerunner = 'http://www.pricerunner.fr/cl/18/Frigo'

    # MARQUE
    marca_request = ''
    if filtros['Marque'].upper() == 'AEG': marca_request = '?man_id=57'
    elif filtros['Marque'].upper() == 'BEKO': marca_request = '?man_id=157'
    elif filtros['Marque'].upper() == 'BOMANN': marca_request = '?man_id=6337'
    elif filtros['Marque'].upper() == 'BOSCH': marca_request = '?man_id=47'
    elif filtros['Marque'].upper() == 'BRANDT': marca_request = '?man_id=975'
    elif filtros['Marque'].upper() == 'BRANDYBEST': marca_request = '?man_id=22656'
    elif filtros['Marque'].upper() == 'CANDY': marca_request = '?man_id=442'
    elif filtros['Marque'].upper() == 'DAEWOO': marca_request = '?man_id=4'
    elif filtros['Marque'].upper() == 'DE DIETRICH': marca_request = '?man_id=974'
    elif filtros['Marque'].upper() == 'DOMETIC': marca_request = '?man_id=6865'
    elif filtros['Marque'].upper() == 'DOMO': marca_request = '?man_id=17595'
    elif filtros['Marque'].upper() == 'ELECTROLUX': marca_request = '?man_id=51'
    elif filtros['Marque'].upper() == 'EXQUISIT': marca_request = '?man_id=79684'
    elif filtros['Marque'].upper() == 'FAURE': marca_request = '?man_id=1948'
    elif filtros['Marque'].upper() == 'FRIGELUX': marca_request = '?man_id=18037'
    elif filtros['Marque'].upper() == 'GORENJE': marca_request = '?man_id=601'
    elif filtros['Marque'].upper() == 'HAIER': marca_request = '?man_id=2692'
    elif filtros['Marque'].upper() == 'HOTPOINT': marca_request = '?man_id=963'
    elif filtros['Marque'].upper() == 'HOTPOINT-ARISTON': marca_request = '?man_id=30820'
    elif filtros['Marque'].upper() == 'INDESIT': marca_request = '?man_id=966'
    elif filtros['Marque'].upper() == 'KLARSTEIN': marca_request = '?man_id=23200'
    elif filtros['Marque'].upper() == 'LG': marca_request = '?man_id=30'
    elif filtros['Marque'].upper() == 'LIEBHERR': marca_request = marca_request = '?man_id=973'
    elif filtros['Marque'].upper() == 'MIELE': marca_request = '?man_id=149'
    elif filtros['Marque'].upper() == 'NEFF': marca_request = '?man_id=970'
    elif filtros['Marque'].upper() == 'PANASONIC': marca_request = '?man_id=17'
    elif filtros['Marque'].upper() == 'SAMSUNG': marca_request = '?man_id=22'
    elif filtros['Marque'].upper() == 'SEVERIN': marca_request = '?man_id=1925'
    elif filtros['Marque'].upper() == 'SHARP': marca_request = '?man_id=24'
    elif filtros['Marque'].upper() == 'SIEMENS': marca_request = '?man_id=46'
    elif filtros['Marque'].upper() == 'SMEG': marca_request = '?man_id=624'
    elif filtros['Marque'].upper() == 'TRISTAR': marca_request = '?man_id=17465'
    elif filtros['Marque'].upper() == 'WAECO': marca_request = '?man_id=17356'
    elif filtros['Marque'].upper() == 'WHIRLPOOL': marca_request = '?man_id=56'
    elif filtros['Marque'].upper() == 'ZANUSSI': marca_request = '?man_id=58'
    url_pricerunner += marca_request

    # SUBTYPE
    if filtros['Subtype'] == 'Réfrigérateur compact':
        url_pricerunner += '&attr_59711098=59711101'


    # TYPE DE POSE
    if filtros['Subtype'] != 'Réfrigérateur compact':
        if filtros['TypePose'] == 'Posable' or filtros['TypePose'] == 'Pose libre':
            url_pricerunner += '?attr_59711098=59711099'
        elif filtros['TypePose'] == 'Integrable':
            url_pricerunner += '?attr_59711098=59711100'

    # ENERGY
    if filtros['Energy'] != "":
        if filtros['Energy'] == 'A+': url_pricerunner += '?attr_2000070=52062131%2C2003149%2C2003142'
        elif filtros['Energy'] == 'A++': url_pricerunner += '?attr_2000070=52062131%2C2003149'
        elif filtros['Energy'] == 'A+++': url_pricerunner += '?attr_2000070=52062131'
        else: url_pricerunner += '&attr_2000070=2003136%2C2003142%2C2003149%2C52062131'

    # COULEUR
    if filtros['Couleur'] != "":
        if filtros['Couleur'] == 'Noir': url_pricerunner += '&attr_59711106=59711122'
        elif filtros['Couleur'] == 'Gris' or filtros['Couleur'] == 'Argent': url_pricerunner += '&attr_59711106=59711120%2C59711107%2C59711123%2C59711113'
        elif filtros['Couleur'] == 'Bleu': url_pricerunner += '&attr_59711106=59711108'
        elif filtros['Couleur'] == 'Blanc': url_pricerunner += '&attr_59711106=59711124%2C59711115%2C59711111'
        elif filtros['Couleur'] == 'Rouge': url_pricerunner += '&attr_59711106=59711121'
        elif filtros['Couleur'] == 'Vert': url_pricerunner += '&attr_59711106=59711114'
        elif filtros['Couleur'] == 'Creme': url_pricerunner += '&attr_59711106=59711110'
        elif filtros['Couleur'] == 'Marron' or filtros['Couleur']=='Brun': url_pricerunner += '&attr_59711106=59711109'
        elif filtros['Couleur'] == 'Orange': url_pricerunner += '&attr_59711106=59711116'
        elif filtros['Couleur'] == 'Or': url_pricerunner += '&attr_59711106=59711112'
        elif filtros['Couleur'] == 'Rose': url_pricerunner += '&attr_59711106=59711119'
        elif filtros['Couleur'] == 'Retro': url_pricerunner += '&attr_59711106=59711118'

    # HATEUR
    if filtros['Hateur'] != '':
        url_pricerunner += '&s_54589398=' + filtros['Hateur'].split('-')[0] + '_' + filtros['Hateur'].split('-')[1]

    # LARGEUR
    if filtros['Largeur'] != '':
        url_pricerunner += '&s_54589397=' + filtros['Largeur'].split('-')[0] + '_' + filtros['Largeur'].split('-')[1]

    # PROFOUNDEUR
    if filtros['Profoundeur'] != '':
        if filtros['Profoundeur'] == 'Plus de 75':
            url_pricerunner += '&s_54589399=' + '75_90'
        else:
            url_pricerunner += '&s_54589399=' + filtros['Profoundeur'].split('-')[0] + '_' + filtros['Profoundeur'].split('-')[1]

    # VOLUME FRIGO
    if filtros['Volume utile'] != '':
        if filtros['Volume utile'] == 'Plus de 259':
            url_pricerunner += '&s_86=259_450'
        else:
            url_pricerunner += '&s_86=' + filtros['Volume utile'].split('-')[0] + '_' + filtros['Volume utile'].split('-')[1]

    # CONSOMNATION
    if filtros['Consommation'] != "":
        if filtros['Consommation'] == 'Plus de 360':
            url_pricerunner += '&s_59588110=' + '360_450'
        else:
            url_pricerunner += '&s_59588110=' + filtros['Consommation'].split('-')[0] + '_' + filtros['Consommation'].split('-')[1]

    #Para casos de un solo filtro
    for i in range(len(url_pricerunner)):
        if url_pricerunner[i] == '&':
            url_pricerunner = url_pricerunner[:i] + '#' + url_pricerunner[i + 1:]
            break

    # ORDEN ASCENDENTE DE PRECIO
    url_pricerunner += '&sort=3'

    # IMPRESION URL
    if should_print:
        print('URL de Pricerunner:', '\n', url_pricerunner)

    return url_pricerunner


def urlgen_refrigerador_combinado(filtros, should_print):

    url_pricerunner = 'http://www.pricerunner.fr/cl/16/Refrigerateurs-Congelateurs'

    # MARQUE
    if filtros['Marque'] != '':
        marca_request = ''
        if filtros['Marque'].upper() == 'AEG': marca_request = '?man_id=57'
        elif filtros['Marque'].upper() == 'BEKO': marca_request = '?man_id=157'
        elif filtros['Marque'].upper() == 'BOMANN': marca_request = '?man_id=6337'
        elif filtros['Marque'].upper() == 'BOSCH': marca_request = '?man_id=47'
        elif filtros['Marque'].upper() == 'BRANDT': marca_request = '?man_id=975'
        elif filtros['Marque'].upper() == 'BRANDYBEST': marca_request = '?man_id=22656'
        elif filtros['Marque'].upper() == 'CANDY': marca_request = '?man_id=442'
        elif filtros['Marque'].upper() == 'DAEWOO': marca_request = '?man_id=4'
        elif filtros['Marque'].upper() == 'DE DIETRICH': marca_request = '?man_id=974'
        elif filtros['Marque'].upper() == 'DOMETIC': marca_request = '?man_id=6865'
        elif filtros['Marque'].upper() == 'DOMO': marca_request = '?man_id=17595'
        elif filtros['Marque'].upper() == 'ELECTROLUX': marca_request = '?man_id=51'
        elif filtros['Marque'].upper() == 'EXQUISIT': marca_request = '?man_id=79684'
        elif filtros['Marque'].upper() == 'FAURE': marca_request = '?man_id=1948'
        elif filtros['Marque'].upper() == 'FRIGELUX': marca_request = '?man_id=18037'
        elif filtros['Marque'].upper() == 'GORENJE': marca_request = '?man_id=601'
        elif filtros['Marque'].upper() == 'HAIER': marca_request = '?man_id=2692'
        elif filtros['Marque'].upper() == 'HOTPOINT': marca_request = '?man_id=963'
        elif filtros['Marque'].upper() == 'HOTPOINT-ARISTON': marca_request = '?man_id=30820'
        elif filtros['Marque'].upper() == 'INDESIT': marca_request = '?man_id=966'
        elif filtros['Marque'].upper() == 'KLARSTEIN': marca_request = '?man_id=23200'
        elif filtros['Marque'].upper() == 'LG': marca_request = '?man_id=30'
        elif filtros['Marque'].upper() == 'LIEBHERR': marca_request = marca_request = '?man_id=973'
        elif filtros['Marque'].upper() == 'MIELE': marca_request = '?man_id=149'
        elif filtros['Marque'].upper() == 'NEFF': marca_request = '?man_id=970'
        elif filtros['Marque'].upper() == 'PANASONIC': marca_request = '?man_id=17'
        elif filtros['Marque'].upper() == 'SAMSUNG': marca_request = '?man_id=22'
        elif filtros['Marque'].upper() == 'SEVERIN': marca_request = '?man_id=1925'
        elif filtros['Marque'].upper() == 'SHARP': marca_request = '?man_id=24'
        elif filtros['Marque'].upper() == 'SIEMENS': marca_request = '?man_id=46'
        elif filtros['Marque'].upper() == 'SMEG': marca_request = '?man_id=624'
        elif filtros['Marque'].upper() == 'TRISTAR': marca_request = '?man_id=17465'
        elif filtros['Marque'].upper() == 'WAECO': marca_request = '?man_id=17356'
        elif filtros['Marque'].upper() == 'WHIRLPOOL': marca_request = '?man_id=56'
        elif filtros['Marque'].upper() == 'ZANUSSI': marca_request = '?man_id=58'
        url_pricerunner += marca_request

    # SUBTYPE
    if filtros['Subtype'] != '':
        if filtros['Subtype'] == 'Réfrigérateur américain':
            url_pricerunner += '&attr_59709490=59908286'
        if filtros['Subtype'] == 'Réfrigérateur congélateur en haut':
            url_pricerunner += '&attr_59709490=59709491'
        if filtros['Subtype'] == 'Réfrigérateur congélateur en bas':
            url_pricerunner += '&attr_59709490=59709492'

    # HATEUR
    if filtros['Hateur'] != '':
        url_pricerunner += '&s_986=' + filtros['Hateur'].split('-')[0] + '_' + filtros['Hateur'].split('-')[1]

    # LARGEUR
    if filtros['Largeur'] != '':
        url_pricerunner += '&s_2000880=' + filtros['Largeur'].split('-')[0] + '_' + filtros['Largeur'].split('-')[1]

    # PROFOUNDEUR
    if filtros['Profoundeur'] != '':
        if filtros['Profoundeur'] == 'Plus de 75':
            url_pricerunner += '&s_59575666=' + '75_90'
        else:
            url_pricerunner += '&s_59575666=' + filtros['Profoundeur'].split('-')[0] + '_' + filtros['Profoundeur'].split('-')[1]

    # VOLUME FRIGO
    if filtros['Volume utile frigo'] != '':
        url_pricerunner += '&s_59704479=' + filtros['Volume utile frigo'].split('-')[0] + '_' + filtros['Volume utile frigo'].split('-')[1]

    # VOLUME CONGELATEUR
    if filtros['Volume utile congelateur'] != '':
        url_pricerunner += '&s_68=' + filtros['Volume utile congelateur'].split('-')[0] + '_' + \
                           filtros['Volume utile congelateur'].split('-')[1]

    # TYPE DE POSE
    if filtros['TypePose'] == 'Posable' or filtros['TypePose'] == 'Pose libre':
        url_pricerunner += '&attr_59709495=59709496'
    elif filtros['TypePose'] == 'Integrable':
        url_pricerunner += '&attr_59709495=59709497'
    #elif filtros['TypePose'] == 'Pose libre':
    #    url_pricerunner += '&attr_59709495=59709496'

    # ENERGY
    if filtros['Energy'] != "":
        if filtros['Energy'] == 'A': url_pricerunner += '&attr_59711070=59711073%2C59711072%2C59711071'
        elif filtros['Energy'] == 'A+': url_pricerunner += '&attr_59711070=59711073%2C59711072%2C59711071'
        elif filtros['Energy'] == 'A++': url_pricerunner += '&attr_59711070=59711072%2C59711071'
        elif filtros['Energy'] == 'A+++': url_pricerunner += '&attr_59711070=59711071'
        else: url_pricerunner += '&attr_59711070=59711074%2C59711073%2C59711072%2C59711071'

    # COULEUR
    if filtros['Couleur'] == 'Noir': url_pricerunner += '&attr_59711172=59711204%2C59711174%2C59711206'
    elif filtros['Couleur'] == 'Gris' or filtros['Couleur'] == 'Argent': url_pricerunner += '&attr_59711172=59711183%2C59711173%2C59711205%2C59711188%2C59711208%2C59711206'
    elif filtros['Couleur'] == 'Bleu': url_pricerunner += '&attr_59711172=59711176'
    elif filtros['Couleur'] == 'Blanc': url_pricerunner += '&attr_59711172=59711208%2C59711190'
    elif filtros['Couleur'] == 'Rouge': url_pricerunner += '&attr_59711172=59711202'
    elif filtros['Couleur'] == 'Vert': url_pricerunner += '&attr_59711172=59711189'
    elif filtros['Couleur'] == 'Creme': url_pricerunner += '&attr_59711172=59711182'
    elif filtros['Couleur'] == 'Marron': url_pricerunner += '&attr_59711172=59711177'
    elif filtros['Couleur'] == 'Orange': url_pricerunner += '&attr_59711172=59711200'
    elif filtros['Couleur'] == 'Rose': url_pricerunner += '&attr_59711172=59711201'

    # CONSOMNATION
    if filtros['Consommation'] != "":
        if filtros['Consommation'] == 'Plus de 360':
            url_pricerunner += '&s_59588110=' + '360_450'
        else:
            url_pricerunner += '&s_59588110=' + filtros['Consommation'].split('-')[0] + '_' + filtros['Consommation'].split('-')[1]

    # Para casos de un solo filtro
    for i in range(len(url_pricerunner)):
        if url_pricerunner[i] == '&':
            url_pricerunner = url_pricerunner[:i] + '#' + url_pricerunner[i + 1:]
            break

    # ORDEN ASCENDENTE DE PRECIO
    url_pricerunner += '&sort=3'

    # IMPRESION URL
    if should_print:
        print('URL de Pricerunner:', '\n', url_pricerunner)

    return url_pricerunner


def urlgen_congelador(filtros, should_print):    

    url_pricerunner = 'http://www.pricerunner.fr/cl/15/Congelateurs'

    # MARQUE
    if filtros['Marque'] != '':
        marca_request = ''
        if filtros['Marque'].upper() == 'AEG': marca_request = '?man_id=57'
        elif filtros['Marque'].upper() == 'BEKO': marca_request = '?man_id=157'
        elif filtros['Marque'].upper() == 'BOMANN': marca_request = '?man_id=6337'
        elif filtros['Marque'].upper() == 'BOSCH': marca_request = '?man_id=47'
        elif filtros['Marque'].upper() == 'BRANDT': marca_request = '?man_id=975'
        elif filtros['Marque'].upper() == 'BRANDYBEST': marca_request = '?man_id=22656'
        elif filtros['Marque'].upper() == 'CANDY': marca_request = '?man_id=442'
        elif filtros['Marque'].upper() == 'DAEWOO': marca_request = '?man_id=4'
        elif filtros['Marque'].upper() == 'DE DIETRICH': marca_request = '?man_id=974'
        elif filtros['Marque'].upper() == 'DOMETIC': marca_request = '?man_id=6865'
        elif filtros['Marque'].upper() == 'DOMO': marca_request = '?man_id=17595'
        elif filtros['Marque'].upper() == 'ELECTROLUX': marca_request = '?man_id=51'
        elif filtros['Marque'].upper() == 'EXQUISIT': marca_request = '?man_id=79684'
        elif filtros['Marque'].upper() == 'EVERGLADES': marca_request = '?man_id=11479'
        elif filtros['Marque'].upper() == 'FAURE': marca_request = '?man_id=1948'
        elif filtros['Marque'].upper() == 'FRIGELUX': marca_request = '?man_id=18037'
        elif filtros['Marque'].upper() == 'GGV EXQUISIT': marca_request = '?man_id=19676'
        elif filtros['Marque'].upper() == 'GORENJE': marca_request = '?man_id=601'
        elif filtros['Marque'].upper() == 'HAIER': marca_request = '?man_id=2692'
        elif filtros['Marque'].upper() == 'HOTPOINT': marca_request = '?man_id=963'
        elif filtros['Marque'].upper() == 'HOTPOINT-ARISTON': marca_request = '?man_id=30820'
        elif filtros['Marque'].upper() == 'INDESIT': marca_request = '?man_id=966'
        elif filtros['Marque'].upper() == 'KLARSTEIN': marca_request = '?man_id=23200'
        elif filtros['Marque'].upper() == 'LG': marca_request = '?man_id=30'
        elif filtros['Marque'].upper() == 'LIEBHERR': marca_request = marca_request = '?man_id=973'
        elif filtros['Marque'].upper() == 'MIELE': marca_request = '?man_id=149'
        elif filtros['Marque'].upper() == 'NEFF': marca_request = '?man_id=970'
        elif filtros['Marque'].upper() == 'PANASONIC': marca_request = '?man_id=17'
        elif filtros['Marque'].upper() == 'SAMSUNG': marca_request = '?man_id=22'
        elif filtros['Marque'].upper() == 'SEVERIN': marca_request = '?man_id=1925'
        elif filtros['Marque'].upper() == 'SHARP': marca_request = '?man_id=24'
        elif filtros['Marque'].upper() == 'SIEMENS': marca_request = '?man_id=46'
        elif filtros['Marque'].upper() == 'SMEG': marca_request = '?man_id=624'
        elif filtros['Marque'].upper() == 'TRISTAR': marca_request = '?man_id=17465'
        elif filtros['Marque'].upper() == 'WAECO': marca_request = '?man_id=17356'
        elif filtros['Marque'].upper() == 'WHIRLPOOL': marca_request = '?man_id=56'
        elif filtros['Marque'].upper() == 'ZANUSSI': marca_request = '?man_id=58'
        url_pricerunner += marca_request

    # SUBTYPE
    if filtros['Subtype'] != '':
        if filtros['Subtype'] == 'Congélateur armoire':
            url_pricerunner += '&attr_59711150=59711154'
        elif filtros['Subtype'] == 'Congélateur coffre':
            url_pricerunner += '&attr_59711150=59711152'

    # HATEUR
    if filtros['Hateur'] != '':
        url_pricerunner += '&s_2000061=' + filtros['Hateur'].split('-')[0] + '_' + filtros['Hateur'].split('-')[1]

    # LARGEUR
    if filtros['Largeur'] != '':
        url_pricerunner += '&s_2000863=' + filtros['Largeur'].split('-')[0] + '_' + filtros['Largeur'].split('-')[1]

    # PROFOUNDEUR
    if filtros['Profoundeur'] != '':
        if filtros['Profoundeur'] == 'Plus de 75':
            url_pricerunner += '&s_59575454=' + '75_90'
        else:
            url_pricerunner += '&s_59575454=' + filtros['Profoundeur'].split('-')[0] + '_' + filtros['Profoundeur'].split('-')[1]

    # VOLUME CONGELATEUR
    if filtros['Volume utile'] != '':
        if filtros['Volume utile'] == 'Moins de 200':
            url_pricerunner += '&s_71=' + '50_200'
        elif filtros['Volume utile'] == 'Plus de 400':
            url_pricerunner += '&s_71=' + '400_500'
        else:
            url_pricerunner += '&s_71=' + filtros['Volume utile'].split('-')[0] + '_' + \
                           filtros['Volume utile'].split('-')[1]


    # TYPE DE POSE: Post filter

    # ENERGY
    if filtros['Energy'] != "":
        if filtros['Energy'] == 'A': url_pricerunner += '&attr_59710022=59710023%2C59710024%2C59710025%2C59710026'
        elif filtros['Energy'] == 'A+': url_pricerunner += '&attr_59710022=59710023%2C59710024%2C59710025'
        elif filtros['Energy'] == 'A++': url_pricerunner += '&attr_59710022=59710023%2C59710024'
        elif filtros['Energy'] == 'A+++': url_pricerunner += '&attr_59710022=59710023'
        else: url_pricerunner += '&attr_59710022=59710024%2C59710023%2C59710025%2C59710026'

    # COULEUR
    if filtros['Couleur'] == 'Noir': url_pricerunner += '&attr_59711155=59711169'
    elif filtros['Couleur'] == 'Gris' or filtros['Couleur'] == 'Argent':
        url_pricerunner += '&attr_59711155=59711170%2C59711161'
    elif filtros['Couleur'] == 'Blanc':
        url_pricerunner += '&attr_59711155=59711165%2C59711171'
    elif filtros['Couleur'] == 'Rouge':
        url_pricerunner += '&attr_59711155=59711167'
    elif filtros['Couleur'] == 'Creme':
        url_pricerunner += 'attr_59711155=59711159'

    # CONSOMNATION
    if filtros['Consommation'] != "":
        if filtros['Consommation'] == 'Plus de 360':
            url_pricerunner += '&s_59587256=' + '360_450'
        else:
            url_pricerunner += '&s_59587256=' + filtros['Consommation'].split('-')[0] + '_' + filtros['Consommation'].split('-')[1]

    # Para casos de un solo filtro
    for i in range(len(url_pricerunner)):
        if url_pricerunner[i] == '&':
            url_pricerunner = url_pricerunner[:i] + '#' + url_pricerunner[i + 1:]
            break

    # ORDEN ASCENDENTE DE PRECIO
    url_pricerunner += '&sort=3'

    # IMPRESION URL
    if should_print:
        print('URL de Pricerunner:', '\n', url_pricerunner)

    return url_pricerunner


def urlgen_cava_de_vino(filtros, should_print):

    url_pricerunner = 'http://www.pricerunner.fr/cl/480/Caves-a-vin'

    # MARQUE
    if filtros['Marque'] != '':
        marca_request = ''
        if filtros['Marque'].upper() == 'AEG': marca_request = '?man_id=57'
        elif filtros['Marque'].upper() == 'ARTEVINO': marca_request = '?man_id=14334'
        elif filtros['Marque'].upper() == 'BEKO': marca_request = '?man_id=157'
        elif filtros['Marque'].upper() == 'BOMANN': marca_request = '?man_id=6337'
        elif filtros['Marque'].upper() == 'BOSCH': marca_request = '?man_id=47'
        elif filtros['Marque'].upper() == 'BRANDT': marca_request = '?man_id=975'
        elif filtros['Marque'].upper() == 'BRANDYBEST': marca_request = '?man_id=22656'
        elif filtros['Marque'].upper() == 'CANDY': marca_request = '?man_id=442'
        elif filtros['Marque'].upper() == 'CASO': marca_request = '?man_id=19608'
        elif filtros['Marque'].upper() == 'CLIMADIFF': marca_request = '?man_id=11482'
        elif filtros['Marque'].upper() == 'DAEWOO': marca_request = '?man_id=4'
        elif filtros['Marque'].upper() == 'DE DIETRICH': marca_request = '?man_id=974'
        elif filtros['Marque'].upper() == 'DOMETIC': marca_request = '?man_id=6865'
        elif filtros['Marque'].upper() == 'DOMO': marca_request = '?man_id=17595'
        elif filtros['Marque'].upper() == 'ELECTROLUX': marca_request = '?man_id=51'
        elif filtros['Marque'].upper() == 'EXQUISIT': marca_request = '?man_id=79684'
        elif filtros['Marque'].upper() == 'FAURE': marca_request = '?man_id=1948'
        elif filtros['Marque'].upper() == 'FRIGELUX': marca_request = '?man_id=18037'
        elif filtros['Marque'].upper() == 'GORENJE': marca_request = '?man_id=601'
        elif filtros['Marque'].upper() == 'HAIER': marca_request = '?man_id=2692'
        elif filtros['Marque'].upper() == 'HOOVER': marca_request = '?man_id=443'
        elif filtros['Marque'].upper() == 'HOTPOINT': marca_request = '?man_id=963'
        elif filtros['Marque'].upper() == 'HOTPOINT-ARISTON': marca_request = '?man_id=30820'
        elif filtros['Marque'].upper() == 'HYUNDAI': marca_request = '?man_id=1710'
        elif filtros['Marque'].upper() == 'INDESIT': marca_request = '?man_id=966'
        elif filtros['Marque'].upper() == 'KLARSTEIN': marca_request = '?man_id=23200'
        elif filtros['Marque'].upper() == 'LA SOMMELIERE': marca_request = '?man_id=14333'
        elif filtros['Marque'].upper() == 'LG': marca_request = '?man_id=30'
        elif filtros['Marque'].upper() == 'LIEBHERR': marca_request = marca_request = '?man_id=973'
        elif filtros['Marque'].upper() == 'MIELE': marca_request = '?man_id=149'
        elif filtros['Marque'].upper() == 'NEFF': marca_request = '?man_id=970'
        elif filtros['Marque'].upper() == 'PANASONIC': marca_request = '?man_id=17'
        elif filtros['Marque'].upper() == 'SAMSUNG': marca_request = '?man_id=22'
        elif filtros['Marque'].upper() == 'SEVERIN': marca_request = '?man_id=1925'
        elif filtros['Marque'].upper() == 'SHARP': marca_request = '?man_id=24'
        elif filtros['Marque'].upper() == 'SIEMENS': marca_request = '?man_id=46'
        elif filtros['Marque'].upper() == 'SMEG': marca_request = '?man_id=624'
        elif filtros['Marque'].upper() == 'TEMPTECH': marca_request = '?man_id=23530'
        elif filtros['Marque'].upper() == 'TRISTAR': marca_request = '?man_id=17465'
        elif filtros['Marque'].upper() == 'WAECO': marca_request = '?man_id=17356'
        elif filtros['Marque'].upper() == 'VINOSPHERE': marca_request = '?man_id=116516'
        elif filtros['Marque'].upper() == 'WHIRLPOOL': marca_request = '?man_id=56'
        elif filtros['Marque'].upper() == 'ZANUSSI': marca_request = '?man_id=58'

        url_pricerunner += marca_request

    # SUBTYPE
    if filtros['Subtype'] != '':
        if filtros['Subtype'] == 'Cave à vin multi-températures':
            url_pricerunner += '&attr_2001265=2007266%2C2007279'
        elif filtros['Subtype'] == 'Cave à vin vieillissement':
            url_pricerunner += '&attr_2001265=2007266%2C2007267'

    # HATEUR
    if filtros['Hateur'] != '':
        url_pricerunner += '&s_59726863=' + filtros['Hateur'].split('-')[0] + '_' + filtros['Hateur'].split('-')[1]

    # LARGEUR
    if filtros['Largeur'] != '':
        url_pricerunner += '&s_59588681=' + filtros['Largeur'].split('-')[0] + '_' + filtros['Largeur'].split('-')[1]

    # PROFOUNDEUR
    if filtros['Profoundeur'] != '':
        if filtros['Profoundeur'] == 'Plus de 75':
            url_pricerunner += '&s_59588680=' + '75_90'
        else:
            url_pricerunner += '&s_59588680=' + filtros['Profoundeur'].split('-')[0] + '_' + filtros['Profoundeur'].split('-')[1]

    # VOLUME NET
    if filtros['Volume net'] != '':
        if filtros['Volume net'] == 'Moins de 200':
            url_pricerunner += '&s_59588677=' + '50_200'
        elif filtros['Volume net'] == 'Plus de 400':
            url_pricerunner += '&s_59588677=' + '400_500'
        else:
            url_pricerunner += '&s_59588677=' + filtros['Volume net'].split('-')[0] + '_' + \
                           filtros['Volume net'].split('-')[1]

    # TYPE DE POSE: Post filter

    # ENERGY
    if filtros['Energy'] != "":
        if filtros['Energy'] == 'E': url_pricerunner += '&attr_58437711=58437713%2C58437712%2C58437715%2C58437716%2C58437718%2C58437717'
        elif filtros['Energy'] == 'D': url_pricerunner += '&attr_58437711=58437713%2C58437712%2C58437715%2C58437716%2C58437717'
        elif filtros['Energy'] == 'C': url_pricerunner += '&attr_58437711=58437713%2C58437712%2C58437715%2C58437716'
        elif filtros['Energy'] == 'B': url_pricerunner += '&attr_58437711=58437713%2C58437712%2C58437715'
        elif filtros['Energy'] == 'A': url_pricerunner += '&attr_58437711=58437713%2C58437712'
        elif filtros['Energy'] == 'A+': url_pricerunner += '&attr_58437711=58437713'

    # COULEUR
    # if filtros['Couleur'] == 'Noir': url_pricerunner += '&attr_59711155=59711169'
    # elif filtros['Couleur'] == 'Gris' or filtros['Couleur'] == 'Argent':
    #     url_pricerunner += '&attr_59711155=59711170%2C59711161'
    # elif filtros['Couleur'] == 'Blanc':
    #     url_pricerunner += '&attr_59711155=59711165%2C59711171'
    # elif filtros['Couleur'] == 'Rouge':
    #     url_pricerunner += '&attr_59711155=59711167'
    # elif filtros['Couleur'] == 'Creme':
    #     url_pricerunner += 'attr_59711155=59711159'

    # CONSOMNATION
    if filtros['Consommation'] != "":
        if filtros['Consommation'] == 'Plus de 360':
            url_pricerunner += '&s_59588682=' + '360_450'
        else:
            url_pricerunner += '&s_59588682=' + filtros['Consommation'].split('-')[0] + '_' + filtros['Consommation'].split('-')[1]

    # Para casos de un solo filtro
    for i in range(len(url_pricerunner)):
        if url_pricerunner[i] == '&':
            url_pricerunner = url_pricerunner[:i] + '#' + url_pricerunner[i + 1:]
            break

    # ORDEN ASCENDENTE DE PRECIO
    url_pricerunner += '&sort=3'

    # IMPRESION URL
    if should_print:
        print('URL de Pricerunner:', '\n', url_pricerunner)

    return url_pricerunner


def urlgen_mobile(filtros, should_print):

    url_pricerunner = 'http://www.pricerunner.fr/cl/1/Telephones-portables'
      
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
    elif filtros['Marque'].upper() == 'GEEMARC': marca_request = '?man_id=456'
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
    
    url_pricerunner += marca_request
    
    # SYSTEME DEXPLOITATION
    if filtros['Systeme dexploitation'] == 'Android': 
        url_pricerunner += '#attr_57315469=57316458'
    elif filtros['Systeme dexploitation'] == 'Windows Phone': 
        url_pricerunner += '#attr_57315469=57316459'   
    elif filtros['Systeme dexploitation'] == 'Apple iOS': 
        url_pricerunner += '#attr_57315469=57316460'
    elif filtros['Systeme dexploitation'] == 'BlackBerry': 
        url_pricerunner += '#attr_57315469=57316461'        
    elif filtros['Systeme dexploitation'] == 'Autre': 
        url_pricerunner += '#attr_57315469=57316462%2C60154776'

    if filtros['Taille'] and filtros['Taille'].replace(" ", "") != "null" and\
            filtros['Taille'].replace(" ", "") != "undefined":
        # TAILLE ECRAN
        url_pricerunner += '&s_53157755={0}_7'.format(int(float(filtros['Taille'])))
    
    # RESOLUTION ECRAN
    if filtros['Resolution'] and filtros['Resolution'].replace(" ", "") != "null" and\
            filtros['Resolution'].replace(" ", "") != "undefined":
        res_min = min([int(x) for x in filtros['Resolution'].lower().split('x')])
        if res_min <= 240: 
            url_pricerunner += '&attr_60162810=60162816%2C60162814%2C60162813%2C60162824%2C60330180%2C60310960%2C60367046%2C60180187%2C60162823%2C60162815%2C60162821%2C60162822%2C60162820%2C60162818%2C60162817'
        elif res_min <= 480:
            url_pricerunner += '&attr_60162810=60162814%2C60162813%2C60162824%2C60330180%2C60310960%2C60367046%2C60180187%2C60162823%2C60162815%2C60162821%2C60162822%2C60162820%2C60162818%2C60162817'
        elif res_min <= 640:
            url_pricerunner += '&attr_60162810=60162814%2C60162813%2C60162824%2C60330180%2C60310960%2C60367046%2C60180187%2C60162823%2C60162815%2C60162821%2C60162822%2C60162820'
        elif res_min <= 720:
            url_pricerunner += '&attr_60162810=60162814%2C60162813%2C60162824%2C60330180%2C60310960%2C60367046%2C60180187%2C60162815%2C60162821%2C60162822%2C60162823'        
        elif res_min <= 750:
            url_pricerunner += '&attr_60162810=60162814%2C60162813%2C60162824%2C60310960%2C60180187%2C60162815%2C60162823'
        elif res_min <= 1080:
            url_pricerunner += '&attr_60162810=60162814%2C60162813%2C60162824%2C60310960%2C60180187%2C60162815'
        elif res_min <= 1440:
            url_pricerunner += '&attr_60162810=60162814%2C60162813%2C60310960%2C60180187%2C60162815'
        elif res_min <= 2160:
            url_pricerunner += '&attr_60162810=60310960%2C60162815'
    
    if filtros['Memoire'] and filtros['Memoire'].replace(" ", "") != "null" and\
            filtros['Memoire'].replace(" ", "") != "undefined":
        # MEMOIRE INTERNE
        if int(filtros['Memoire']) <= 1:
            url_pricerunner += '&attr_57315476=57316464%2C57316467%2C57316468%2C57316469%2C59817412%2C57316465%2C57316470%2C58330664%2C57316466'
        elif int(filtros['Memoire']) <= 2:
            url_pricerunner += '&attr_57315476=57316467%2C57316468%2C57316469%2C59817412%2C57316465%2C57316470%2C58330664%2C57316466'
        elif int(filtros['Memoire']) <= 4:
            url_pricerunner += '&attr_57315476=57316467%2C57316468%2C57316469%2C59817412%2C57316470%2C58330664%2C57316466' 
        elif int(filtros['Memoire']) <= 8:
            url_pricerunner += '&attr_57315476=57316467%2C57316468%2C57316469%2C59817412%2C57316470%2C58330664'    
        elif int(filtros['Memoire']) <= 16:
            url_pricerunner += '&attr_57315476=57316468%2C57316469%2C59817412%2C57316470%2C58330664'
        elif int(filtros['Memoire']) <= 32:
            url_pricerunner += '&attr_57315476=57316469%2C59817412%2C57316470%2C58330664'
        elif int(filtros['Memoire']) <= 64:
            url_pricerunner += '&attr_57315476=59817412%2C57316470%2C58330664'
        elif int(filtros['Memoire']) <= 128:
            url_pricerunner += '&attr_57315476=59817412%2C58330664'
        elif int(filtros['Memoire']) <= 256:
            url_pricerunner += '&attr_57315476=59817412'    
    
    if filtros['Ram'] and filtros['Ram'].replace(" ", "") != "null" and\
            filtros['Ram'].replace(" ", "") != "undefined":
        # RAM
        if float(filtros['Ram'])<= 1.0:
            url_pricerunner += '&attr_57315484=57316021%2C57316022%2C57316023%2C57316024%2C59905543%2C59905542%2C59689103'
        elif float(filtros['Ram'])<= 1.5:
            url_pricerunner += '&attr_57315484=57316022%2C57316023%2C57316024%2C59905543%2C59905542%2C59689103'
        elif float(filtros['Ram'])<= 2.0:
            url_pricerunner += '&attr_57315484=57316023%2C57316024%2C59905543%2C59905542%2C59689103'        
        elif float(filtros['Ram'])<= 3.0:
            url_pricerunner += '&attr_57315484=57316024%2C59905543%2C59905542%2C59689103'
        elif float(filtros['Ram'])<= 4.0:
            url_pricerunner += '&attr_57315484=59905543%2C59905542%2C59689103'
        elif float(filtros['Ram'])<= 6.0:
            url_pricerunner += '&attr_57315484=59905543%2C59905542'
        elif float(filtros['Ram'])<= 8.0:
            url_pricerunner += '&attr_57315484=59905542'
    
    if filtros['Coeurs'] and filtros['Coeurs'].replace(" ", "") != "null" and\
            filtros['Coeurs'].replace(" ", "") != "undefined":
        # COEURS CPU
        if int(filtros['Coeurs']) == 1:
            url_pricerunner += '&attr_59512111=59512137%2C59512138%2C59512139%2C59512141%2C59512140'
        elif int(filtros['Coeurs']) == 2:
            url_pricerunner += '&attr_59512111=59512138%2C59512139%2C59512141%2C59512140'
        elif int(filtros['Coeurs']) == 4:
            url_pricerunner += '&attr_59512111=59512139%2C59512141%2C59512140'
        elif int(filtros['Coeurs']) == 6:
            url_pricerunner += '&attr_59512111=59512141%2C59512140'        
        elif int(filtros['Coeurs']) == 8:
            url_pricerunner += '&attr_59512111=59512141'
        
    if filtros['MegapixelsFrontale'] and filtros['MegapixelsFrontale'].replace(" ", "") != "null" and\
            filtros['MegapixelsFrontale'].replace(" ", "") != "undefined":
        # MEGAPIXELS FRONT
        url_pricerunner += '&s_59738040={0}_100'.format(int(filtros['MegapixelsFrontale']))

    if filtros['MegapixelsArriere'] and filtros['MegapixelsArriere'].replace(" ", "") != "null" and\
            filtros['MegapixelsArriere'].replace(" ", "") != "undefined":
        # MEGAPIXELS BACK
        url_pricerunner += '&s_1374={0}_100'.format(int(filtros['MegapixelsArriere']))
    
    if filtros['CapaciteBatterie'] and filtros['CapaciteBatterie'].replace(" ", "") != "null" and\
            filtros['CapaciteBatterie'].replace(" ", "") != "undefined":
        # BATERIE
        url_pricerunner += '&s_59586294={0}_20000'.format(int(filtros['CapaciteBatterie']))
    
    # COULEUR
    if filtros['Couleur'] == 'Noir':
        url_pricerunner += '&attr_60162858=60162860'
    elif filtros['Couleur'] == 'Blanc':
        url_pricerunner += '&attr_60162858=60162872'
    elif filtros['Couleur'] == 'Bleu' or filtros['Couleur'] == 'Turquoise':
        url_pricerunner += '&attr_60162858=60162861%2C60162871'
    elif filtros['Couleur'] == 'Or':
        url_pricerunner += '&attr_60162858=60162863'
    elif filtros['Couleur'] == 'Marron':
        url_pricerunner += '&attr_60162858=60162862'
    elif filtros['Couleur'] == 'Gris' or filtros['Couleur'] == 'Argent':
        url_pricerunner += '&attr_60162858=60162865%2C60162870'
    elif filtros['Couleur'] == 'Vert':
        url_pricerunner += '&attr_60162858=60162864'
    elif filtros['Couleur'] == 'Jaune':
        url_pricerunner += '&attr_60162858=60162873'
    elif filtros['Couleur'] == 'Violet':
        url_pricerunner += '&attr_60162858=60162868'
    elif filtros['Couleur'] == 'Orange':
        url_pricerunner += '&attr_60162858=60162866'
    elif filtros['Couleur'] == 'Rose':
        url_pricerunner += '&attr_60162858=60162867'
    elif filtros['Couleur'] == 'Rouge':
        url_pricerunner += '&attr_60162858=60162869'    
    elif filtros['Couleur'] == 'Beige':
        url_pricerunner += '&attr_60162858=60162859'           
        
        
    url_pricerunner += '&sort=3'


    # IMPRESION URL
    if should_print:
        print('URL de Pricerunner:', '\n', url_pricerunner)

    return url_pricerunner

def urlgen_laptop(filtros, should_print):    

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


# -------- FILTROS POSTERIORES
def filter_tv(query_products):
    list_products = []
    for p in query_products:
        product = {}
        product["name"] = p.nombre
        product["category_id"] = p.category_id
        product["store_id"] = p.store_id
        list_products.append(product)
    return list_products


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

            procesador = p.ficha_tecnica.get("Série de processeur", None)
            modelo_procesador = p.ficha_tecnica.get("Modèle de processeur", None)

            if procesador is not None and modelo_procesador is not None:
                cpu_filter = procesador + ' ' + modelo_procesador

                input_benchs = {
                    'procesador' : filtros['CPUSpec'],
                    'procesador_raw' : cpu_filter,
                }

                status_cpu = check_cpu(input_benchs)
                print("STATUS_CPU PRICE RUNNER")
                print(status_cpu)
                parametros['cpu_ok'] = status_cpu['CPU']['es_valido']

            else:
                # Aplica regla acerca de items sin detalle de procesador
                if rules['required_cpu']:
                    parametros['cpu_ok'] = False     


        if selected_gpu:

            gpu_filter = p.ficha_tecnica.get("Modèle de carte graphique", None)

            if gpu_filter is not None:

                gpu = gpu_filter.split(',')
                for i in range(len(gpu)):
                    if 'Intel Iris' in gpu_filter[i]:
                        continue
                    elif 'Intel' in gpu_filter[i]:
                        gpu_filter[i] = ""
                gpu_filter = "".join(gpu_filter)

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
