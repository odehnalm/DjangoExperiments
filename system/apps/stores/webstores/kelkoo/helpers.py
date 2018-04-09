# -*- coding: utf-8 -*-
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


# ------- GENERADORES DE URL
def urlgen_tv(filtros, should_print):

    exist_filter = False
    fields = {
        'x-100311823': '',
        'compatibilite-hd': '',
        'format-d-ecran': '',
        'marque': '',
        'taille-de-la-diagonale': '',
        'type-de-tv': ''
    }

    url_kelkoo = 'http://www.kelkoo.fr/'

    fields['x-100311823'] = 'c-100311823-televiseur'

    # ---- MARQUE
    if filtros['Marque'] != '':
        exist_filter = True

        if filtros['Marque'].lower() == "lg" or\
                filtros['Marque'].lower() == "philips" or\
                filtros['Marque'].lower() == "samsung" or\
                filtros['Marque'].lower() == "sony" or\
                filtros['Marque'].lower() == "panasonic" or\
                filtros['Marque'].lower() == "toshiba":

            fields['x-100311823'] = 'v-100311823-tv-' + filtros['Marque'].lower().replace(' ', '-').replace('&', 'E')
        else:

            fields['marque'] = filtros['Marque'].lower().replace(' ', '-').replace('&', 'E')

    # ---- TYPE DE TV
    # if filtros['3D'] and filtros['3D'] == 'Oui':
    #     exist_filter = True
    #     fields['type-de-tv'] = 'tv-3d'

    # if fields['type-de-tv'] == '' and filtros['Type'] != '':
    if filtros['Type'] != '':
        exist_filter = True

        if filtros['Type'] == 'LED':

            if fields['x-100311823'] == 'c-100311823-televiseur':

                fields['x-100311823'] = 'v-100311823-tv-led'

            elif 'v-100311823-tv-' in fields['x-100311823']:

                if 'samsung' in fields['x-100311823'] or\
                        'sony' in fields['x-100311823']:
                    fields['x-100311823'] = fields['x-100311823'].replace("v-100311823-tv-", 'v-100311823-tv-led-')

                else:
                    fields['type-de-tv'] = "tv-led"

        elif filtros['Type'] == 'LCD':

            fields['type-de-tv'] = 'tv-lcd'

        elif filtros['Type'] == 'OLED':

            fields['type-de-tv'] = 'oled'

    # ---- COMPATIBILITE HD
    if filtros['Resolution'] and '' not in filtros['Resolution']:
        exist_filter = True

        if filtros['Resolution'][0] == '1080p':

            if fields['x-100311823'] == 'c-100311823-televiseur':

                fields['x-100311823'] = 'v-100311823-tv-full-hd'

            elif fields['x-100311823'] == 'v-100311823-tv-led':

                fields['x-100311823'] = 'v-100311823-tv-full-hd'
                fields['type-de-tv'] = "tv-led"

            else:

                fields['compatibilite-hd'] = "full-hd"

        elif filtros['Resolution'][0] == '720p':

            if fields['x-100311823'] == 'c-100311823-televiseur':

                fields['x-100311823'] = 'v-100311823-tv-hd-ready'

            elif fields['x-100311823'] == 'v-100311823-tv-led':

                fields['x-100311823'] = 'v-100311823-tv-hd-ready'
                fields['type-de-tv'] = "tv-led"

            else:

                fields['compatibilite-hd'] = "hd-ready"

        elif filtros['Resolution'][0] == '4k':

            fields['compatibilite-hd'] = "ultra-hd-4k"

    # ---- RATIO
    if filtros['Ratio'] and '' not in filtros['Ratio']:
        exist_filter = True
        if filtros['Ratio'][0] == '4:3':
            fields['format-d-ecran'] = '4-3'
        elif filtros['Ratio'][0] == '16:9':
            fields['format-d-ecran'] = '16-9'

    # ---- PULGADAS
    if filtros['TaillePounce'] and\
            filtros['TaillePounce'].replace(" ", "") != "null":
        if str(filtros['TaillePounce']).isdigit():

            taille_pounces = int(filtros['TaillePounce'])

            if taille_pounces > 0:
                exist_filter = True

            # TAILLE
            if taille_pounces > 0 and taille_pounces < 24:
                fields['taille-de-la-diagonale'] = 'moins-de-24-61cm'
            elif taille_pounces >= 24 and taille_pounces <= 32:
                fields['taille-de-la-diagonale'] = '24-61cm-a-32-82cm'
            elif taille_pounces >= 37 and taille_pounces <= 42:
                fields['taille-de-la-diagonale'] = '37-94cm-a-42-107cm'
            elif taille_pounces >= 46 and taille_pounces <= 50:
                fields['taille-de-la-diagonale'] = '46-116cm-a-50-127cm'
            elif taille_pounces >= 55 and taille_pounces <= 60:
                fields['taille-de-la-diagonale'] = '55-140cm-a-60-152cm'
            elif taille_pounces > 60:
                fields['taille-de-la-diagonale'] = 'plus-de-60-152cm'

    # ---- URL
    counter_fields = 0
    url_kelkoo += fields['x-100311823']
    if fields['compatibilite-hd']:
        counter_fields += 1
        url_kelkoo += '/compatibilite-hd/' + fields['compatibilite-hd']
    if fields['format-d-ecran']:
        counter_fields += 1
        url_kelkoo += '/format-d-ecran/' + fields['format-d-ecran']
    if fields['marque']:
        counter_fields += 1
        url_kelkoo += '/marque/' + fields['marque']
    if fields['taille-de-la-diagonale']:
        counter_fields += 1
        url_kelkoo += '/taille-de-la-diagonale/' + fields['taille-de-la-diagonale']
    if fields['type-de-tv']:
        counter_fields += 1
        url_kelkoo += '/type-de-tv/' + fields['type-de-tv']

    if counter_fields >= 3:
        url_kelkoo = url_kelkoo.replace("www.kelkoo.fr/", "www.kelkoo.fr/nf/")

    if not exist_filter:
        url_kelkoo += '.html'

    # ORDEN DE PRODUCTOS
    url_kelkoo += '?sortby=price_ascending'

    if should_print:
        print('URL de Kelkoo:', '\n', url_kelkoo)

    return url_kelkoo


def urlgen_refrigerador(filtros, should_print):

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

    if should_print:
        print('URL de Kelkoo:', '\n', url_kelkoo)

    return url_kelkoo


def urlgen_refrigerador_combinado(filtros, should_print):

    exist_filter = False
    fields = {
        'x-145801': '',
        'classe-energetique': '',
        'froid-ventile': '',
        'subtype': '',
        'largeur': '',
        'hateur' : '',
        'profoundeur' : '',
        'marque': '',
        'type-de-pose': '',
        'volume-net-en-litres': ''
    }    

    if filtros['Hateur'] == "null":
        filtros['Hateur'] = ""

    if filtros['Largeur'] == "null":
        filtros['Largeur'] = ""

    if filtros['Profoundeur'] == "null":
        filtros['Profoundeur'] = ""

    if filtros['Volume utile'] == "null":
        filtros['Volume utile'] = ""

    try:
        if filtros['Dispenseur'] == "null":
            filtros['Dispenseur'] = ""        
    except:
        filtros['Dispenseur'] = "" 

    try:
        if filtros['Display'] == "null":
            filtros['Display'] = ""        
    except:
        filtros['Display'] = "" 

    url_kelkoo = 'http://www.kelkoo.fr/'

    fields['x-145801'] = 'c-145801-combine-refrigerateur-congelateur'

    #Contamos numero de filtros llenos

    num_filtros_form = 0
    if filtros['Subtype'] != '': exist_filter = True
    if filtros['Marque'] != '': exist_filter = True
    if filtros['Volume utile'] != '': exist_filter = True
    if filtros['TypePose'] != '': exist_filter = True
    if filtros['Energy'] != '': exist_filter = True
    if filtros['Largeur'] != '': exist_filter = True
    if filtros['Type refrigeration'] != '': exist_filter = True

    # SUBTYPE
    if filtros['Subtype'] == 'Réfrigérateur américain':
        fields['subtype'] = 'rofrigorateur-amoricain'
    elif filtros['Subtype'] == 'Réfrigérateur congélateur en haut':
        fields['subtype'] = 'congolateur-au-dessus'
    elif filtros['Subtype'] == 'Réfrigérateur congélateur en bas':
        fields['subtype'] = 'congolateur-en-dessous'

    # MARQUE
    if filtros['Marque'] != "":
        fields['marque'] = filtros['Marque'].lower().replace(' ', '-').replace('&', 'E')

    # VOLUME
    if filtros['Volume net'] == "Moins de 150" or filtros['Volume utile'] == "Moins de 150":
        fields['volume-net-en-litres'] = 'moins-de-150-l'
    elif filtros['Volume net'] == "150-244" or filtros['Volume utile'] == "150-244":
        fields['volume-net-en-litres'] = '150-l-244-l'
    elif filtros['Volume net'] == "245-273" or filtros['Volume utile'] == "245-273":
        fields['volume-net-en-litres'] = '245-l-273-l'
    elif filtros['Volume net'] == "274-316" or filtros['Volume utile'] == "274-316":
        fields['volume-net-en-litres'] = '274-l-316-l'
    elif filtros['Volume net'] == "317-425" or filtros['Volume utile'] == "317-425":
        fields['volume-net-en-litres'] = '317-l-425-l'
    elif filtros['Volume net'] == "Plus de 426" or filtros['Volume utile'] == "Plus de 426":
        fields['volume-net-en-litres'] = 'plus-de-426-l'

    # TYPE DE POSE
    if filtros['TypePose'] == 'Pose libre':
        fields['type-de-pose'] = 'posable'
    elif filtros['TypePose'].lower() == 'integrable':
        fields['x-145801'] = 'v-145801-refrigerateur-congelateur-encastrable'

    # ENERGY
    if filtros['Energy'] == 'G':
        fields['classe-energetique'] = 'g'
    elif filtros['Energy'] == 'E':
        fields['classe-energetique'] = 'e'
    elif filtros['Energy'] == 'D':
        fields['classe-energetique'] = 'd'
    elif filtros['Energy'] == 'C':
        fields['classe-energetique'] = 'c'
    elif filtros['Energy'] == 'B':
        fields['classe-energetique'] = 'b'
    elif filtros['Energy'] == 'A':
        fields['classe-energetique'] = 'a'
    elif filtros['Energy'] == 'A+':
        if filtros['TypePose'].lower() == 'integrable':
            fields['classe-energetique'] = 'ap'
        else:
            fields['x-145801'] = 'v-145801-refrigerateur-congelateur-classe-ap'
    elif filtros['Energy'] == 'A++':
        fields['classe-energetique'] = 'app'
    elif filtros['Energy'] == 'A+++':
        fields['classe-energetique'] = 'appp'

    # TYPE FROID
    if filtros['Type refrigeration'] == 'Ventilé':
        fields['froid-ventile'] = 'avec-froid-ventilo'

    # ---- URL
    counter_fields = 0
    url_kelkoo += fields['x-145801']
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
    if fields['subtype']:
        counter_fields += 1
        url_kelkoo += '/type-de-refrigerateur-congelateur/' + fields['subtype']        
    if fields['volume-net-en-litres']:
        counter_fields += 1
        url_kelkoo += '/volume-total-du-combi/' + fields['volume-net-en-litres']

    if counter_fields >= 3:
        url_kelkoo = url_kelkoo.replace("www.kelkoo.fr/", "www.kelkoo.fr/nf/")

    if not exist_filter:
        url_kelkoo += '.html'

    # ORDEN DE PRODUCTOS
    url_kelkoo += '?sortby=price_ascending'

    return url_kelkoo


def urlgen_congelador(filtros, should_print):

    exist_filter = False
    fields = {
        'x-145701': '',
        'energy': '',
        'subtype': '',
        'marque': '',
        'type-de-pose': ''
    }

    try:
        if filtros['Hauteur'] == "null":
            filtros['Hauteur'] = ""
    except:
        pass
    try:
        if filtros['Largeur'] == "null":
            filtros['Largeur'] = ""
    except:
        pass
    try:
        if filtros['Profoundeur'] == "null":
            filtros['Profoundeur'] = ""
    except:
        pass
    try:
        if filtros['Volume net'] == "null":
            filtros['Volume net'] = ""
    except:
        pass


    url_kelkoo = 'http://www.kelkoo.fr/'

    fields['x-145701'] = "c-145701-congelateur"

    #Contamos numero de filtros llenos

    if filtros['Subtype'] != '': exist_filter = True
    if filtros['Marque'] != '': exist_filter = True
    if filtros['TypePose'] != '': exist_filter = True
    if filtros['Energy'] != '': exist_filter = True

    # SUBTYPE
    if filtros['Subtype'] == 'Congélateur armoire':
        if filtros['TypePose'].lower() == 'integrable':
            fields['subtype'] = 'armoire'
        else:
            fields['x-145701'] = 'v-145701-congelateur-armoire'
    elif filtros['Subtype'] == 'Congélateur coffre':
        if filtros['TypePose'].lower() == 'integrable':
            fields['subtype'] = 'coffre'
        else:
            fields['x-145701'] = 'v-145701-congelateur-coffre'

    # MARQUE
    if filtros['Marque'] != "":
        fields['marque'] = filtros['Marque'].lower().replace(' ', '-')

    # # VOLUME POST FILTER

    # TYPE DE POSE
    if filtros['TypePose'] == 'Pose libre':
        fields['type-de-pose'] += 'pose-libre'
    elif filtros['TypePose'].lower() == 'integrable':
        fields['x-145701'] = 'v-145701-congelateur-encastrable'

    # ENERGY
    if filtros['Energy'] == 'G':
        fields['energy'] = 'g'
    elif filtros['Energy'] == 'E':
        fields['energy'] = 'e'
    elif filtros['Energy'] == 'D':
        fields['energy'] = 'd'
    elif filtros['Energy'] == 'C':
        fields['energy'] = 'c'
    elif filtros['Energy'] == 'B':
        fields['energy'] = 'b'
    elif filtros['Energy'] == 'A':
        fields['energy'] = 'a'
    elif filtros['Energy'] == 'A+':
        fields['energy'] = 'ap'
    elif filtros['Energy'] == 'A++':
        fields['energy'] = 'app'
    elif filtros['Energy'] == 'A+++':
        fields['energy'] = 'appp'

    # ---- URL
    counter_fields = 0
    url_kelkoo += fields['x-145701']
    if fields['energy']:
        url_kelkoo += '/classe-energetique/' + fields['energy']
    if fields['marque']:
        counter_fields += 1
        url_kelkoo += '/marque/' + fields['marque']
    if fields['subtype']:
        counter_fields += 1
        url_kelkoo += '/type-de-congelateur/' + fields['subtype']        
    if fields['type-de-pose']:
        counter_fields += 1
        url_kelkoo += '/type-de-pose/' + fields['type-de-pose']

    if counter_fields >= 3:
        url_kelkoo = url_kelkoo.replace("www.kelkoo.fr/", "www.kelkoo.fr/nf/")
    
    if not exist_filter:
        url_kelkoo += '.html'

    # ORDEN DE PRODUCTOS
    url_kelkoo += '?sortby=price_ascending'

    return url_kelkoo    


def urlgen_cava_de_vino(filtros, should_print):

    exist_filter = False
    
    fields = {
        'x-100014413': '',
        'subtype': '',
        'marque': '',
        'stockage': ''
    } 

    try:
        if filtros['Hateur'] == "null":
            filtros['Hateur'] = ""
    except:
        pass

    try:
        if filtros['Largeur'] == "null":
            filtros['Largeur'] = ""
    except:
        pass

    try:
        if filtros['Profoundeur'] == "null":
            filtros['Profoundeur'] = ""
    except:
        pass

    try:
        if filtros['Volume net'] == "null":
            filtros['Volume net'] = ""
    except:
        pass

    url_kelkoo = 'http://www.kelkoo.fr/'

    fields['x-100014413'] = 'c-100014413-cave-a-vin'

    #Contamos numero de filtros llenos

    if filtros['Subtype'] != '' and filtros['Subtype'] != 'Cave à vin': exist_filter = True
    if filtros['Marque'] != '': exist_filter = True
    if filtros['Stockage'] != '': exist_filter = True
    if filtros['TypePose'] != '': exist_filter = True


    # SUBTYPE
    if filtros['Subtype'] == 'Cave à vin multi-températures':
        fields['subtype'] = 'mise-a-temperature'
    elif filtros['Subtype'] == 'Cave à vin vieillissement':
        fields['subtype'] = 'vieillissement'

    # MARQUE
    if filtros['Marque'] != "":
        fields['marque'] = filtros['Marque'].lower().replace(' ', '-').replace('&', 'E')

    # # VOLUME POST FILTER

    # TYPE DE POSE POST FILTER

    # STOCKAGE
    if filtros['Stockage'] == 'Moins de 100':
        fields['stockage'] = 'moins-de-100'
    elif filtros['Stockage'] == '100-200':
        fields['stockage'] = '100-200'
    elif filtros['Stockage'] == 'Plus de 200':
        fields['stockage'] = '200-300'

    # ---- URL
    counter_fields = 0
    url_kelkoo += fields['x-100014413']         
    if fields['marque']:
        counter_fields += 1
        url_kelkoo += '/marque/' + fields['marque']      
    if fields['stockage']:
        counter_fields += 1
        url_kelkoo += '/nombre-de-bouteilles/' + fields['stockage']
    if fields['subtype']:
        counter_fields += 1
        url_kelkoo += '/type-de-cave-a-vin/' + fields['subtype']

    if counter_fields >= 3:
        url_kelkoo = url_kelkoo.replace("www.kelkoo.fr/", "www.kelkoo.fr/nf/")

    if not exist_filter:
        url_kelkoo += '.html'        

    # ORDEN DE PRODUCTOS
    url_kelkoo += '?sortby=price_ascending'

    return url_kelkoo              


def urlgen_mobile(filtros, should_print):

    exist_filter = False
    fields = {
        'x-100020213': '',
        'marque': '',
        'systeme-d-exploitation': '',
        'resolution-de-l-appareil-photo': ''
    }

    url_kelkoo = 'http://www.kelkoo.fr/'
    fields['x-100020213'] = 'c-100020213-telephone-portable-sans-abonnement'

    if filtros['MegapixelsArriere'] == "null":
        filtros['MegapixelsArriere'] = ""

    # ---- MARQUE
    if filtros['Marque']:
        exist_filter = True

        if filtros['Marque'].lower() == "htc" or\
                filtros['Marque'].lower() == "nokia" or\
                filtros['Marque'].lower() == "samsung":

            fields['x-100020213'] = 'v-100020213-telephone-portable-' + filtros['Marque'].lower().replace(' ', '-').replace('&', 'E')

        elif filtros['Marque'].lower() == "apple":
            fields['x-100020213'] = 'v-100020213-iphone'

        elif filtros['Marque'].lower() == "blackberry":
            fields['x-100020213'] = 'v-100020213-blackberry'

        else:
            fields['marque'] = filtros['Marque'].lower().replace(' ', '-').replace('&', 'E')

    # ---- SYSTEME D EXPLOITATION
    if filtros['Systeme dexploitation']:
        exist_filter = True

        if filtros['Systeme dexploitation'] == 'Android':
            fields['systeme-d-exploitation'] = 'android'
        elif filtros['Systeme dexploitation'] == 'Apple iOS':
            fields['systeme-d-exploitation'] = 'apple-ios'
        elif filtros['Systeme dexploitation'] == 'BlackBerry':
            fields['systeme-d-exploitation'] = 'blackberry-os'
        elif filtros['Systeme dexploitation'] == 'Windows Phone':
            fields['systeme-d-exploitation'] = 'windows-phone'
        elif filtros['Systeme dexploitation'] == 'Windows Phone':
            fields['systeme-d-exploitation'] = 'windows-phone'

    # ---- RESOLUTION DE L APPAREIL PHOTO
    if filtros['MegapixelsArriere'] and isfloat(filtros['MegapixelsArriere']):

        mega_pixels = float(filtros['MegapixelsArriere'])
        exist_filter = True  

        if mega_pixels<1:
            fields['resolution-de-l-appareil-photo'] = 'moins-de-1-megapixel'
        elif mega_pixels>=1 and mega_pixels<=2:
            fields['resolution-de-l-appareil-photo'] = 'entre-1-et-2-megapixels'
        elif mega_pixels>2 and mega_pixels<=3:
            fields['resolution-de-l-appareil-photo'] = 'entre-2-1-et-3-megapixels'
        elif mega_pixels>3 and mega_pixels<=4:
            fields['resolution-de-l-appareil-photo'] = 'entre-3-1-et-4-megapixels'
        elif mega_pixels>4 and mega_pixels<=5:
            fields['resolution-de-l-appareil-photo'] = 'entre-4-1-et-5-megapixels'
        elif mega_pixels>5:
            fields['resolution-de-l-appareil-photo'] = 'plus-de-5-megapixels'

    # ---- URL
    counter_fields = 0
    url_kelkoo += fields['x-100020213']
    if fields['marque']:
        counter_fields += 1
        url_kelkoo += '/marque/' + fields['marque']
    if fields['resolution-de-l-appareil-photo']:
        counter_fields += 1
        url_kelkoo += '/resolution-de-l-appareil-photo/' + fields['resolution-de-l-appareil-photo']
    if fields['systeme-d-exploitation']:
        counter_fields += 1
        url_kelkoo += '/systeme-d-exploitation/' + fields['systeme-d-exploitation']

    if counter_fields >= 3:
        url_kelkoo = url_kelkoo.replace("www.kelkoo.fr/", "www.kelkoo.fr/nf/")

    if not exist_filter:
        url_kelkoo += '.html'

    # ORDEN DE PRODUCTOS
    url_kelkoo += '?sortby=price_ascending'

    # IMPRESION URL
    if should_print:
        print('URL de Kelkoo:', '\n', url_kelkoo)

    return url_kelkoo


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


def filter_frigo(query_products):
    list_products = []
    for p in query_products:
        product = {}
        product["name"] = p.nombre
        product["category_id"] = p.category_id
        product["store_id"] = p.store_id
        list_products.append(product)
    return list_products
