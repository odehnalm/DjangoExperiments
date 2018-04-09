import numpy as np

# ------- GENERADORES DE URL
def urlgen_tv(filtros, should_print):

    fields = {
        'type': [],
        'marque': '',
        'taille': [],
        'resolution': [],
        'feature6' : [],
        'energy' : '',
        'smart' : '',
        '3d' : '',
        'wifi' : '',
        'url' : [],
        'url_sort' : '',
        'url_query_id' : '',
    }

    fields['url'].append("https://www.amazon.fr/s/gp/search/ref=sr_nr_p_89_2?fst=as%3Aoff&rh=n%3A13921051%2Cn%3A%2113910671%2Cn%3A13910681%2Cn%3A14059871")
    #fields['url'].append("https://www.amazon.fr/s/gp/search/ref=sr_nr_p_n_feature_three_br_0?fst=as%3Aoff&rh=n%3A13921051%2Cn%3A%2113910671%2Cn%3A13910681%2Cn%3A14059871")
    fields['url_sort'] = "&bbn=14059871&sort=price-asc-rank&ie=UTF8"
    fields['url_query_id'] = "&qid=152" + str(int(np.random.random() * 1.e7))
    fields['marque'] = filtros['Marque'].replace(' ','+')

    #TYPE
    if filtros['Type'] == 'LCD':
        fields['type'].append('406421031')
        fields['type'].append('667768011')
        fields['type'].append('1611175031')
    if filtros['Type'] == 'LED':
        fields['type'].append('406421031')
        fields['type'].append('1611175031')
    if filtros['Type'] == 'OLED':    
        fields['type'].append('1611175031')    

    #TAILLE
    if filtros['TaillePounce'] and filtros['TaillePounce'].replace(" ", "") != "null":
        if str(filtros['TaillePounce']).isdigit():
            taille_pounces = int(filtros['TaillePounce'])
        
        if taille_pounces <= 29:
            fields['taille'].append('9597715031')
            fields['taille'].append('9597716031')
            fields['taille'].append('9597717031')
            fields['taille'].append('9597718031')
            fields['taille'].append('9597719031')
            fields['taille'].append('9597720031')
        if taille_pounces >= 30 and taille_pounces  <= 39:
            fields['taille'].append('9597716031')
            fields['taille'].append('9597717031')
            fields['taille'].append('9597718031')
            fields['taille'].append('9597719031')
            fields['taille'].append('9597720031')
        if taille_pounces >= 40 and taille_pounces  <= 49:
            fields['taille'].append('9597717031')
            fields['taille'].append('9597718031')
            fields['taille'].append('9597719031')
            fields['taille'].append('9597720031')
        if taille_pounces >= 50 and taille_pounces  <= 59:
            fields['taille'].append('9597718031')
            fields['taille'].append('9597719031')
            fields['taille'].append('9597720031')
        if taille_pounces >= 60 and taille_pounces  <= 69:
            fields['taille'].append('9597719031')
            fields['taille'].append('9597720031')
        if taille_pounces >= 70:
            fields['taille'].append('9597720031')

    # ---- COMPATIBILITE HD
    if filtros['Resolution'] and '' not in filtros['Resolution']:
        if filtros['Resolution'][0] == '720p':
            fields['resolution'].append('667772011')
            fields['resolution'].append('667773011')
            fields['resolution'].append('2752481031')
        if filtros['Resolution'][0] == '1080p':
            fields['resolution'].append('667773011')
            fields['resolution'].append('2752481031')
        if filtros['Resolution'][0].lower() == '4k':
            fields['resolution'].append('2752481031')            

    # DESIGN
    if 'Incurve' in filtros['Design'] or 'incurve' in filtros['Design']:
        fields['feature6'].append('5676178031')

    # 3D
    if filtros['3D'] == 'Oui':
        fields['feature6'].append('507955031')

    # SMARTY/INTERNET
    if filtros['Internet'] == 'Oui' or filtros['Smart'] == 'Oui':
        fields['feature6'].append('507956031')        

    # ---- URL
    # if fields['feature6']:
    #     value = "p_n_feature_six_browse-bin%3A" + "%7C".join(fields['feature6'])
    #     fields['url'].append(value)       
    if fields['type']:
        value = "p_n_feature_three_browse-bin%3A" + "%7C".join(fields['type'])
        fields['url'].append(value)
    if fields['taille']:
        value = "p_n_size_browse-bin%3A" + "%7C".join(fields['taille'])
        fields['url'].append(value)  
    if fields['resolution']:
        value = "p_n_feature_two_browse-bin%3A" + "%7C".join(fields['resolution'])
        fields['url'].append(value)     
    if fields['marque']:
        value = "p_89%3A" + fields["marque"]
        fields['url'].append(value)
    url_amazon = "%2C".join(fields['url']) + fields['url_sort'] + fields['url_query_id']

    return url_amazon


def urlgen_refrigerador(filtros, should_print):

    raise NotImplementedError

def urlgen_refrigerador_combinado(filtros, should_print):

    raise NotImplementedError   

def urlgen_congelador(filtros, should_print):    

    raise NotImplementedError

def urlgen_cava_de_vino(filtros, should_print):

    raise NotImplementedError


def urlgen_mobile(filtros, should_print):

    raise NotImplementedError


def urlgen_laptop(filtros, should_print):

    raise NotImplementedError


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


def filter_laptop(query_products):
    list_products = []
    for p in query_products:
        product = {}
        product["name"] = p.nombre
        product["category_id"] = p.category_id
        product["store_id"] = p.store_id
        list_products.append(product)
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

def filter_tv(query_products):
    list_products = []
    for p in query_products:
        product = {}
        product["name"] = p.nombre
        product["category_id"] = p.category_id
        product["store_id"] = p.store_id
        list_products.append(product)
    return list_products    
