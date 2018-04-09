def urlgen_tv(filtros):

    fields = {
        'type': '',
        'marque': '',
        'taille': '',
        'resolution': '',
        'design' : ''
    }

    url_darty = 'https://www.darty.com/nav/extra/list?s=prix_asc'

    #MARCA
    if filtros['Marque'].upper() == 'PHILIPS':
        fields['marque'] = 'MP_philips_tv-PHILI'
    elif filtros['Marque'].upper() == 'MEDIAMARKET':
        fields['marque'] = 'MP_mediamarket'
    elif filtros['Marque'].upper() == 'SMART TECH':
        fields['marque'] = 'MP_smart_tech'
    else:
        try:
            fields['marque'] = filtros['Marque'].upper()[:5]
        except:
            fields['marque'] = filtros['Marque'].upper()

    # Type: categoria exclusiva, al no incluirla tenemos ambos productos LED y OLED
    # si no es OLED, aunque el filtro llegue vacío, así sale por defecto
    if filtros['Type'] == 'OLED':
        fields['type'] = '97056&fa=149552-292059'
    else:
        fields['type'] = '97056'

    # TAMANO DE PANTALLA
    if filtros['TaillePounce'] and str(filtros['TaillePounce'].replace(" ", "")) != "null" and\
            str(filtros['TaillePounce']).replace(" ", "") != "undefined" and filtros['TaillePounce'] != '0':
        # Taille: rango de pulgadas
        fields['taille'] = '-'.join(
            [str(pulgadas) + '0000321600' for pulgadas in range(int(filtros['TaillePounce']), 76)])

    # Resolution
    if '720p' in filtros['Resolution']:
        fields['resolution'] = '885093-mk_54112_11624652-1627160-1531132'
    elif '1080p' in filtros['Resolution']:
        fields['resolution'] = 'mk_54112_11624652-1627160-1531132'
    elif '4K' in filtros['Resolution'][0].upper():
        fields['resolution'] = '1627160-1531132'  # 4K Y 4K UHD

    # Design
    if 'Incurve' in filtros['Design'] or 'incurve' in filtros['Design']: fields['design'] = '367267'

    # ---- URL
    c_filter = '&c='
    if fields['taille']:
        c_filter = "-".join([c_filter,fields['taille']])
    if fields['resolution']:
        c_filter = "-".join([c_filter,fields['resolution']])
    if fields['design']:
        c_filter = "-".join([c_filter,fields['design']])
    url_darty += '&cat=' + fields['type']
    if fields['marque']:
        url_darty += '&m=' + fields['marque']
    if c_filter != '&c=':
        url_darty += c_filter        

    #Limpieza
    url_darty = url_darty.replace('=-','=').replace('--','-')

    url_darty += '&npk=1'

    #Limpieza
    url_darty = url_darty.replace('=-','=').replace('--','-')

    return url_darty

filtros = {
    'Marque': 'SAMSUNG',
    "TaillePounce": '50',
    "Type": 'OLED',
    "Resolution": ['4k'],
    "Ratio": [''],
    "3D": "",
    "Design" : "Incurve"
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("")    

filtros = {
    'Marque': 'PHILIPS',
    "TaillePounce": '',
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
    "TaillePounce": '45',
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
    "TaillePounce": '45',
    "Type": '',
    "Resolution": ['1080p'],
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
    'Marque': 'SAMSUNG',
    "TaillePounce": '',
    "Type": '',
    "Resolution": ['1080p'],
    "Ratio": [''],
    "3D": "",
    "Design" : "Incurve"
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("") 

filtros = {
    'Marque': 'SAMSUNG',
    "TaillePounce": '',
    "Type": '',
    "Resolution": ['4k'],
    "Ratio": [''],
    "3D": "",
    "Design" : "Incurve"
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("") 

filtros = {
    'Marque': 'SAMSUNG',
    "TaillePounce": '45',
    "Type": 'LED',
    "Resolution": ['4k'],
    "Ratio": [''],
    "3D": "",
    "Design" : "Incurve"
}
print("FILTROS")
print(filtros)
print("URL GENERADA")
print(urlgen_tv(filtros))
print("") 

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