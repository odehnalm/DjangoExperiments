def urlgen_tv(filtros):

    fields = {
        'type': '',
        'marque': '',
        'taille': '',
        'resolution': '',
        'design' : ''
    }

    url_gd = 'https://www.group-digital.fr/le-catalogue/tv-video-home-cinema/television'

    # # CASO SOLO HAY MARCA
    # if filtros['Type'] == '' and '' in filtros['Resolution'] and filtros['Marque'] != '' and \
    # (filtros['TaillePounce'] == '0' or filtros['TaillePounce'] == 'null') and '' in filtros['Design']:
    #     url_gd += filtros['Marque'].lower() + '.html?dir=asc&order=price'

    #     if should_print:
    #         print('URL de Group Digital:', '\n', url_gd)

    #     return url_gd


    # Type: categoria exclusiva, al no incluirla tenemos ambos productos LED y OLED
    if filtros['Type'] == 'OLED': fields['type'] = 'tv-oled'

    # Resolution
    if '' not in filtros['Resolution']:

        if '720p' in filtros[
            'Resolution']: fields['resolution'] = 'hdtv_hdtv-1080p_ultra-hd-4k_3840x2160_ultra-hd-4k-_1920x1080p_4k-uhd_3840x2160p'
        elif '1080p' in filtros[
            'Resolution']: fields['resolution'] = 'hdtv-1080p_ultra-hd-4k_3840x2160_ultra-hd-4k-_1920x1080p_4k-uhd_3840x2160p'
        elif '4K' in filtros['Resolution'][0].upper(): fields['resolution'] = 'ultra-hd-4k_3840x2160_ultra-hd-4k-_4k-uhd_3840x2160p'

    # Marque
    if filtros['Marque'] != '':
        fields['marque'] = filtros['Marque'].lower()

    # Prix
    # precio_gd = "".join(('price=',filtros['Range_prix'][0],'-',filtros['Range_prix'][1]))

    # Taille
    if filtros['TaillePounce'] != '0' and filtros['TaillePounce'] != 'null' and filtros['TaillePounce'] != '':
        if int(filtros['TaillePounce']) < 26: fields['taille'] = '26-a-32-66-a-82cm_26-66cm_33-a-43-83-a-109cm_44-a-50-110-a-127cm_51-a-58-128-a-147cm_59-a-65-148-a-165cm_66-a-79-166-a-201cm'
        if int(filtros['TaillePounce']) <= 32 and int(filtros['TaillePounce']) >= 26: fields['taille'] = '26-a-32-66-a-82cm_33-a-43-83-a-109cm_44-a-50-110-a-127cm_51-a-58-128-a-147cm_59-a-65-148-a-165cm_66-a-79-166-a-201cm'
        if int(filtros['TaillePounce']) <= 43 and int(filtros['TaillePounce']) >= 33: fields['taille'] = '33-a-43-83-a-109cm_44-a-50-110-a-127cm_51-a-58-128-a-147cm_59-a-65-148-a-165cm_66-a-79-166-a-201cm'
        if int(filtros['TaillePounce']) <= 50 and int(filtros['TaillePounce']) >= 44: fields['taille'] = '44-a-50-110-a-127cm_51-a-58-128-a-147cm_59-a-65-148-a-165cm_66-a-79-166-a-201cm'
        if int(filtros['TaillePounce']) <= 58 and int(filtros['TaillePounce']) >= 51: fields['taille'] = '51-a-58-128-a-147cm_59-a-65-148-a-165cm_66-a-79-166-a-201cm'
        if int(filtros['TaillePounce']) <= 65 and int(filtros['TaillePounce']) >= 59: fields['taille'] = '59-a-65-148-a-165cm_66-a-79-166-a-201cm'
        if int(filtros['TaillePounce']) <= 79 and int(filtros['TaillePounce']) >= 66: fields['taille'] = '66-a-79-166-a-201cm'

    # Design
    if 'Incurve' in filtros['Design'] or 'incurve' in filtros['Design']: fields['design'] = 'incurve'

    # ---- URL
    filtros_gd = ''
    if fields['type']:
        filtros_gd += "/" + fields['type']
    if fields['resolution']:
        filtros_gd += "/" + fields['resolution']
        if fields['marque'] != '' or fields['taille'] != '' or fields['design'] != '': filtros_gd += '_' 
    if fields['marque']:
        filtros_gd += "/" + fields['marque']
        if fields['taille'] != '' or fields['design'] != '': filtros_gd += '_' 
    if fields['taille']:
        filtros_gd += "/" + fields['taille']
        if fields['design'] != '': filtros_gd += '_' 
    if fields['design']:
        filtros_gd += "/" + fields['design']

    #Limpienza: esto es para agregar la extensión .html y así ordenar precios
    filtros_gd = filtros_gd.replace("_/","_")

    url_gd += filtros_gd

    url_gd += '.html?dir=asc&order=price'

    return url_gd

filtros = {
    'Marque': '',
    "TaillePounce": '0',
    "Type": '',
    "Resolution": [''],
    "Ratio": [''],
    "3D": "",
    "Design" : ""
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("")    

filtros = {
    'Marque': 'SONY',
    "TaillePounce": '0',
    "Type": '',
    "Resolution": [''],
    "Ratio": [''],
    "3D": "",
    "Design" : ""
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("") 

filtros = {
    'Marque': '',
    "TaillePounce": '30',
    "Type": '',
    "Resolution": [''],
    "Ratio": [''],
    "3D": "",
    "Design" : ""
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("") 

filtros = {
    'Marque': 'samsung',
    "TaillePounce": '50',
    "Type": '',
    "Resolution": [''],
    "Ratio": [''],
    "3D": "",
    "Design" : "incurve"
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("") 

filtros = {
    'Marque': 'samsung',
    "TaillePounce": '50',
    "Type": '',
    "Resolution": ['4k'],
    "Ratio": [''],
    "3D": "",
    "Design" : "incurve"
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("") 

filtros = {
    'Marque': 'samsung',
    "TaillePounce": '50',
    "Type": 'OLED',
    "Resolution": ['4k'],
    "Ratio": [''],
    "3D": "",
    "Design" : "incurve"
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("") 

filtros = {
    'Marque': '',
    "TaillePounce": '50',
    "Type": 'OLED',
    "Resolution": ['4k'],
    "Ratio": [''],
    "3D": "",
    "Design" : ""
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("") 