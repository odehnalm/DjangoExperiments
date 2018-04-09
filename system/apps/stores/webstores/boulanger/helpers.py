from ...post_filter.laptop.utils import check_cpu, check_gpu

# ------- GENERADORES DE URL
def urlgen_tv(filtros, should_print):
    raise NotImplementedError


def urlgen_refrigerador(filtros, should_print):

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

def urlgen_refrigerador_combinado(filtros, should_print):

    fields = {
        'url_base': '',
        'subtype' : [],
        'brand': '',
        'largeur': [],
        'profondeur': [],
        'hateur': [],
        'volume': [],
        'energy': [],
        'froid': [],
        'froidcongelateur': [],
        'nofrost': [],
    }

    num_filters = 0

    fields['url_base'] = 'https://www.boulanger.com/c/refrigerateur-avec-congelateur'

    # SUBTYPE
    if filtros['Subtype'] == 'Réfrigérateur américain':
        fields['url_base'] = 'https://www.boulanger.com/c/refrigerateur-americain'
    elif filtros['Subtype'] == 'Réfrigérateur congélateur en bas':
        fields['subtype'].append('conge9lateur20en20bas')
    elif filtros['Subtype'] == 'Réfrigérateur congélateur en haut':
        fields['subtype'].append('conge9lateur20en20haut')

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
    if filtros['Type refrigeration'] == 'Brassé':
        fields['froid'].append('froid20brasse9')
        fields['froid'].append('froid20ventile9')
        num_filters += 1        
    elif filtros['Type refrigeration'] == 'Ventilé':
        fields['froid'].append('froid20ventile9')
        num_filters += 1  

    # SYSTEME DE FROID CONGELATEUR
    if filtros['Type congelation'] == 'Ventilé':
        fields['froidcongelateur'].append('froid20ventile9203a20de9givrage20automatique')
        num_filters += 1

    # TECHNOLOGIE NO FROST
    if filtros['Technologie'] == 'No frost':
        fields['nofrost'].append('supreame20no20frost')
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
    if fields['subtype']:
        values = "|".join(['facetting_tous_les_refs_____configuration~'+ e for e in fields['subtype']])
        url_fields.append(values)         
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
    if fields['froidcongelateur']:     
        values = "|".join(['facetting_tous_les_refs_____type_de_froid_du_congelateur~'+ e for e in fields['froidcongelateur']])
        url_fields.append(values)  
    if fields['nofrost']:     
        values = "|".join(['facetting_tous_les_refs_____technologie~'+ e for e in fields['nofrost']])
        url_fields.append(values)                                  

    url += "|".join(url_fields)
    url += sorting

    return url    

def urlgen_congelador(filtros, should_print):

    fields = {
        'url_base': '',
        'subtype' : [],
        'brand': '',
        'largeur': [],
        'profondeur': [],
        'hateur': [],
        'volume': [],
        'energy': [],
        'froid': [],
        'froidcongelateur': [],
        'nofrost': [],
    }

    num_filters = 0

    fields['url_base'] = 'https://www.boulanger.com/c/congelateur'

    # SUBTYPE
    if filtros['Subtype'] == 'Congélateur armoire':
        fields['url_base'] = 'https://www.boulanger.com/c/congelateur-armoire'
    elif filtros['Subtype'] == 'Congélateur coffre':
        fields['url_base'] = 'https://www.boulanger.com/c/congelateur-coffre'

    # MARQUE
    if filtros["Marque"]:
        fields['brand'] = filtros['Marque'].lower().replace(" ", "20")

    #HATEUR
    if filtros['Hateur'] in {"30-75","75-100"}:
        fields['hateur'].append('jusqu27e0208520cm')
        num_filters += 1
    elif filtros['Hateur'] in {"75-100","100-120","120-160"}:
        fields['hateur'].append('de208620e02015020cm')
        num_filters += 1
    elif filtros['Hateur'] in {"120-160","160-180"}:
        fields['hateur'].append('de2015120e02017520cm')
        num_filters += 1
    elif filtros['Hateur'] in {"160-180","180-195"}:
        fields['hateur'].append('de2017620e02018620cm')
        num_filters += 1
    elif filtros['Hateur'] in {"180-195","195-205"}:
        fields['hateur'].append('plus20de2017520cm')
        num_filters += 1

    #LARGEUR
    if filtros['Largeur'] in {"50-60"}:
        fields['largeur'].append('de205020e0205520cm')
        fields['largeur'].append('de205620e0206020cm')
        num_filters += 1
    elif filtros['Largeur'] in {"60-70","70-80","80-90"}:
        fields['largeur'].append('de206120e0209020cm')
        num_filters += 1
    elif filtros['Largeur'] == "90-105":
        fields['largeur'].append('3e209020cm')
        num_filters += 1

    # VOLUME UTILE
    if filtros['Volume utile'] == "Moins de 200":
        fields['volume'].append('moins20de2020020l')
        num_filters += 1
    elif filtros['Volume utile'] == "200-299":
        fields['volume'].append('de2020020e02029920l')
        num_filters += 1
    elif filtros['Volume utile'] == "300-400":
        fields['volume'].append('de2030020e02040020l')
        num_filters += 1
    elif filtros['Volume utile'] == "Plus de 400":
        fields['volume'].append('plus20de2040020l')
        num_filters += 1

    #ENERGY
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

    # SYSTEME DE FROID CONGELATEUR
    if filtros['Systeme de froid'] == 'Ventilé':
        fields['froid'].append('froid20statique203a20de9givrage20manuel')
        fields['froid'].append('froid20ventile9203a20de9givrage20automatique')
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
        values = "|".join(['facettes_congelateurs_____Hateur~'+ e for e in fields['hateur']])
        url_fields.append(values) 
    if fields['largeur']:
        values = "|".join(['facettes_congelateurs_____largeur~'+ e for e in fields['largeur']])
        url_fields.append(values) 
    if fields['volume']:     
        values = "|".join(['facettes_congelateurs_____volume~'+ e for e in fields['volume']])
        url_fields.append(values)    
    if fields['energy']:     
        values = "|".join(['facettes_congelateurs_____classe_energetique~'+ e for e in fields['energy']])
        url_fields.append(values)          
    if fields['froid']:     
        values = "|".join(['facettes_congelateurs_____type_de_froid~'+ e for e in fields['froid']])
        url_fields.append(values)                                  

    url += "|".join(url_fields)
    url += sorting

    return url 

def urlgen_cava_de_vino(filtros, should_print):

    fields = {
        'url_base': '',
        'subtype' : [],
        'brand': '',
        'largeur': [],
        'profondeur': [],
        'hateur': [],
        'stockage': [],
        'energy': [],
        'froid': [],
        'froidcongelateur': [],
        'nofrost': [],
    }

    num_filters = 0

    fields['url_base'] = 'https://www.boulanger.com/c/toutes-les-caves-a-vin'

    # SUBTYPE
    if filtros['Subtype'] == 'Cave à vin service':
        fields['url_base'] = 'https://www.boulanger.com/c/cave-de-service'
    elif filtros['Subtype'] == 'Cave à vin vieillissement':
        fields['url_base'] = 'https://www.boulanger.com/c/cave-de-vieillissement'
    elif filtros['Subtype'] == 'Cave à vin multi-températures':
        fields['url_base'] = 'https://www.boulanger.com/c/cave-polyvalente'        

    # MARQUE
    if filtros["Marque"]:
        fields['brand'] = filtros['Marque'].lower().replace(" ", "20")

    #HATEUR
    if filtros['Hateur'] != "":
        if filtros['Hateur'] in {"30-75","75-100"}:
            fields['hateur'].append('moins20de2070cm')
            fields['hateur'].append('de207020e0208520cm')
            num_filters += 1
        elif filtros['Hateur'] in {"75-100","100-120"}:
            fields['hateur'].append('de207020e0208520cm')
            fields['hateur'].append('de208620e02012020cm')
            num_filters += 1
        elif filtros['Hateur'] in {"120-160"}:
            fields['hateur'].append('de2012120e02016020cm')
            num_filters += 1
        elif filtros['Hateur'] in {"180-195","195-205"}:
            fields['hateur'].append('plus20de2016020cm')
            num_filters += 1

    #LARGEUR
    if filtros['Largeur'] != "":
        if filtros['Largeur'] in {"30-50"}:
            fields['largeur'].append('moins20de205020cm')
            num_filters += 1
        else:
            fields['largeur'].append('de205020e0206520cm')
            fields['largeur'].append('plus20de206520cm')
            num_filters += 1

    #PROFOUNDEUR
    if filtros['Profoundeur'] != "":
        if filtros['Profoundeur'] in {"20-55","55-60"}:
            fields['profondeur'].append('moins20de206020cm')
            num_filters += 1
        else:
            fields['profondeur'].append('plus20de206020cm')
            num_filters += 1

    # STOCKAGE
    if filtros['Stockage'] == "Moins de 100":
        fields['stockage'].append('moins20de20100')
        num_filters += 1
    elif filtros['Stockage'] == "100-200":
        fields['stockage'].append('de2010020e020200')
        num_filters += 1
    elif filtros['Stockage'] == "Plus de 200":
        fields['stockage'].append('plus20de20200')
        num_filters += 1

    #ENERGY
    if filtros['Energy'] == 'D':
        fields['energy'].append('d')
        fields['energy'].append('c')
        fields['energy'].append('b')
        fields['energy'].append('a')
        fields['energy'].append('a2b')
        fields['energy'].append('a2b2b')
        fields['energy'].append('a2b2b2b')
        num_filters += 1    
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
        values = "|".join(['facettes_cave_a_vin_____hauteur_en_cm~'+ e for e in fields['hateur']])
        url_fields.append(values) 
    if fields['largeur']:
        values = "|".join(['facettes_cave_a_vin_____largeur_en_cm~'+ e for e in fields['largeur']])
        url_fields.append(values) 
    if fields['profondeur']:
        values = "|".join(['facettes_cave_a_vin_____profondeur_en_cm~'+ e for e in fields['profondeur']])
        url_fields.append(values)         
    if fields['stockage']:     
        values = "|".join(['facettes_cave_a_vin_____capacite_avec_clayettes~'+ e for e in fields['stockage']])
        url_fields.append(values)    
    if fields['energy']:     
        values = "|".join(['facettes_cave_a_vin_____classe_energetique~'+ e for e in fields['energy']])
        url_fields.append(values)          

    url += "|".join(url_fields)
    url += sorting

    return url


def urlgen_mobile(filtros, should_print):

    fields = {
        'url_base': '',
        'brand': '',
        'systeme_d_exploitation': '',
        'memoire_interne': '',
        'taille_de_l_ecran': '',
        'memoire_ram': '',
        'coloris': ''
    }

    num_filters = 0

    if filtros['Memoire'].replace(" ", "") == "null":
        filtros['Memoire'] = ""

    if filtros['Taille'].replace(" ", "") == "null":
        filtros['Taille'] = ""

    if filtros['Ram'].replace(" ", "") == "null":
        filtros['Ram'] = ""

    fields['url_base'] = "https://www.boulanger.com/c/smartphone-telephone-portable"

    # Marque
    if filtros["Marque"]:
        num_filters += 1
        fields['brand'] = 'brand~' + filtros['Marque'].lower().replace(" ", "20")


    # OS
    if filtros["Systeme dexploitation"] and not filtros["Marque"]:
        num_filters += 1
        if filtros['Systeme dexploitation'] == 'Android':
            fields['systeme_d_exploitation'] = 'facettes_gsm_____systeme_d_exploitation~android'
        elif filtros['Systeme dexploitation'] == 'Apple iOS':
            fields['systeme_d_exploitation'] = 'facettes_gsm_____systeme_d_exploitation~ios'


    # Memoria
    if filtros['Memoire']:
        num_filters += 1
        if float(filtros['Memoire']) >= 64:
            fields['memoire_interne'] = 'facettes_gsm_____memoire_interne~6420go;12820go;25620go'
        elif float(filtros['Memoire']) >= 32:
            fields['memoire_interne'] = 'facettes_gsm_____memoire_interne~25620go;12820go;6420go;3220go'
        elif float(filtros['Memoire']) >= 16:
            fields['memoire_interne'] = 'facettes_gsm_____memoire_interne~12820go;6420go;3220mo;1620go'
        elif float(filtros['Memoire']) >= 8:
            fields['memoire_interne'] = 'facettes_gsm_____memoire_interne~6420go;3220mo;1620go;820go'
        elif float(filtros['Memoire']) >= 4:
            fields['memoire_interne'] = 'facettes_gsm_____memoire_interne~3220mo;1620go;820go;420mo'
        elif float(filtros['Memoire']) >= 4:
            fields['memoire_interne'] = 'facettes_gsm_____memoire_interne~1620go;820go;420mo;120go'


    if filtros['Taille']:
        num_filters += 1
        if float(filtros['Taille']) < 5.0:
            fields['taille_de_l_ecran'] = 'facettes_gsm_____taille_de_l_ecran~22c42220soit2062c120cm;42c72220soit20112c920cm;22c32220soit2052c820cm;12c772220soit2042c4920cm;42220soit20102c120cm;42c52220soit20112c420cm;42c82220soit20122c220cm;12c72220soit2042c320cm;12c82220soit2042c620cm;42c62220soit20112c720cm;22c82220soit2072c120cm;32c52220soit2082c920cm;22c22220soit2052c620cm;22220soit20520cm;22c62220soit2062c620cm'
        elif float(filtros['Taille']) >= 5.0 and float(filtros['Taille']) <= 5.5:
            fields['taille_de_l_ecran'] = 'facettes_gsm_____taille_de_l_ecran~52c52220soit201420cm;52c22220soit20132c220cm;52c12220soit20122c920cm;52220soit20122c720cm;52c32220soit20132c520cm'
        if float(filtros['Taille']) > 5.5:
            fields['taille_de_l_ecran'] = 'facettes_gsm_____taille_de_l_ecran~52c62220soit20142c220cm|facettes_gsm_____taille_de_l_ecran~52c72220soit20142c520cm;62c22220soit20152c720cm;52c82220soit20142c520cm;62220soit20152c2420cm;52c72220soit20142e2620cm;62c32220soit201620cm;62c42220soit20162c2520cm;52c92220soit20142c520cm'


    if filtros['Ram']:
        num_filters += 1
        if int(filtros['Ram']) >= 4:
            fields['memoire_ram'] = 'memoire_____memoire_ram~820go;620go;420go'
        if int(filtros['Ram']) >= 2:
            fields['memoire_ram'] = 'memoire_____memoire_ram~220go;320go;420go'
        elif int(filtros['Ram']) < 2:
            fields['memoire_ram'] = 'memoire_____memoire_ram~3220mo;6420mo;12c520go;120go;420mo;1620mo;820mo;51220mo;02c2520go'

    # COULEURS
    # if filtros['Couleur']:
    #     num_filters += 1
    #     if filtros['Couleur'] == 'Noir':
    #         fields['coloris'] = 'facettes_communes_____coloris~noir'
    #     elif filtros['Couleur'] == 'Violet':
    #         fields['coloris'] = 'facettes_communes_____coloris~violet'
    #     elif filtros['Couleur'] == 'Beige':
    #         fields['coloris'] = 'facettes_communes_____coloris~beige'
    #     elif filtros['Couleur'] == 'Blanc':
    #         fields['coloris'] = 'facettes_communes_____coloris~blanc'
    #     elif filtros['Couleur'] == 'Bleu':
    #         fields['coloris'] = 'facettes_communes_____coloris~bleu'
    #     elif filtros['Couleur'] == 'Or':
    #         fields['coloris'] = 'facettes_communes_____coloris~dore'
    #     elif filtros['Couleur'] in ['Gris', 'Argent']:
    #         fields['coloris'] = 'facettes_communes_____coloris~gris'
    #     elif filtros['Couleur'] == 'Jaune':
    #         fields['coloris'] = 'facettes_communes_____coloris~dore'
    #     elif filtros['Couleur'] == 'Orange':
    #         fields['coloris'] = 'facettes_communes_____coloris~orange'
    #     elif filtros['Couleur'] == 'Rose':
    #         fields['coloris'] = 'facettes_communes_____coloris~rose'
    #     elif filtros['Couleur'] == 'Rouge':
    #         fields['coloris'] = 'facettes_communes_____coloris~rouge'
    #     elif filtros['Couleur'] == 'Vert':
    #         fields['coloris'] = 'facettes_communes_____coloris~vert'


    url = fields['url_base']
    sorting = 'sorting_price=asc'
    url_fields = []

    if num_filters > 1:
        url = 'https://www.boulanger.com/c/nav-filtre/smartphone-telephone-portable'
        sorting = '&' + sorting

    if num_filters == 1:
        url += '/'
        sorting = '?' + sorting
    else:
        url += '?'

    if fields['brand']:
        url_fields.append(fields['brand'])
    if fields['systeme_d_exploitation']:
        url_fields.append(fields['systeme_d_exploitation'])
    if fields['memoire_interne']:
        url_fields.append(fields['memoire_interne'])
    if fields['taille_de_l_ecran']:
        url_fields.append(fields['taille_de_l_ecran'])
    if fields['memoire_ram']:
        url_fields.append(fields['memoire_ram'])
    if fields['coloris']:
        url_fields.append(fields['coloris'])

    url += "|".join(url_fields)
    url += sorting

    # IMPRESION URL
    if should_print:
        print('URL de Boulanger:', '\n', url)

    return url


def urlgen_laptop(filtros, should_print):

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
    if filtros['list_cpus']:
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

            procesador = p.ficha_tecnica.get("Référence et spécificités", None)

            if procesador is not None:
                cpu_filter =  " ".join(procesador.split(":")[0].split())

                input_benchs = {
                    'procesador' : filtros['CPUSpec'],
                    'procesador_raw' : cpu_filter,
                }

                status_cpu = check_cpu(input_benchs)
                print("STATUS_CPU BOULANGER")
                print(status_cpu)
                parametros['cpu_ok'] = status_cpu['CPU']['es_valido']

            else:
                # Aplica regla acerca de items sin detalle de procesador
                if rules['required_cpu']:
                    parametros['cpu_ok'] = False     


        if selected_gpu:

            gpu_filter = p.ficha_tecnica.get('Contrôleur graphique', None)

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
