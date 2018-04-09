#==================================================================================
# Importacion de librerías
import os
import io
import json
from xlsxwriter.workbook import Workbook
#==================================================================================

def crearExcel(filtros):

    # <<<<<<<<<<<<<
    # 1) CREACION DE ARCHIVO
    # <<<<<<<<<<<<<
    scraped_json = 'result_amazon.json'

    output_file_name = 'amazon_output.xlsx'

    # Creacion del archivo Excel
    workbook = Workbook(output_file_name)
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 0, 25)
    worksheet.set_row(0, 30)

    #icol se usa para pasear por las columnas del excel
    icol=0

    # <<<<<<<<<<<<<
    # 2) FORMATOS
    # <<<<<<<<<<<<<

    # Datos
    format = workbook.add_format()
    format.set_border(style=1)
    format.set_text_wrap()
    # URL
    format_url = workbook.add_format()
    format_url.set_border(style=1)
    format_url.set_font_size(8)
    format_url.set_text_wrap()
    # Not Available
    format_NA = workbook.add_format()
    format_NA.set_bg_color('silver')
    format_NA.set_border(style=1)
    # Encabezados
    format_header = workbook.add_format()
    format_header.set_border(style=1)
    format_header.set_text_wrap()
    format_header.set_bold()

    # <<<<<<<<<<<<<
    # 3) APERTURA DE ARCHIVOS
    # <<<<<<<<<<<<<

    try:
        with io.open(scraped_json, 'r', encoding='utf8') as json_f:
            json_data = json.load(json_f)
    except Exception as error:
        print('JSON no encontrado: ' + repr(error))
        json_data = []

    # <<<<<<<<<<<<<
    # 4) MAXIMO NUMERO DE TIENDAS
    # <<<<<<<<<<<<<
    # Este número determinará el número de filas dedicadas a tiendas que se va a agregar al Excel

    max_tiendas_lcdcmp = 0
    max_tiendas_pricerunner = 0
    max_tiendas_kelkoo = 0
    max_tiendas = 1

    # for i in range(len(json_lcdcmp)):
    #     if len(json_lcdcmp[i]['tiendas']) > max_tiendas_lcdcmp:
    #         max_tiendas_lcdcmp = len(json_lcdcmp[i]['tiendas'])
    # for i in range(len(json_pricerunner)):
    #     if len(json_pricerunner[i]['tiendas']) > max_tiendas_pricerunner:
    #         max_tiendas_pricerunner = len(json_pricerunner[i]['tiendas'])
    # for i in range(len(json_kelkoo)):
    #     if len(json_kelkoo[i]['tiendas']) > max_tiendas_kelkoo:
    #         max_tiendas_kelkoo = len(json_kelkoo[i]['tiendas'])

    # max_tiendas = max([max_tiendas_lcdcmp,
    #                    max_tiendas_pricerunner,
    #                    max_tiendas_kelkoo])

    # <<<<<<<<<<<<<
    # 5) DETERMINAMOS LA ESTRUCTURA DEL ARCHIVO EXCEL
    # <<<<<<<<<<<<<

    #Creamos la estructura del archivo excel:
    worksheet.write('A2', "Marque", format_header)
    worksheet.write('A3', "Modèle", format_header)
    worksheet.write('A4', "Taille de l'ecran en pouces", format_header)
    worksheet.write('A5', "Type d'écran", format_header)
    worksheet.write('A6', "Résolution", format_header)
    worksheet.write('A7', "Taux de rafraichissement", format_header)
    worksheet.write('A8', "3D", format_header)
    worksheet.write('A9', "Internet", format_header)
    worksheet.write('A10', "Wifi intégré", format_header)
    worksheet.write('A11', "Smart", format_header)
    worksheet.write('A12', "Autre", format_header)

    for k in range(max_tiendas):
        worksheet.write(13+4*k,0, "Prix", format_header)
        worksheet.write(14+4*k,0, "Enseigne", format_header)
        worksheet.write(15+4*k,0, "URL", format_header)

    # <<<<<<<<<<<<<
    # 6) COLUMNA DE PRODUCTO A REEMPLAZAR
    # <<<<<<<<<<<<<

    worksheet.write('B1', "Modèle endommagé", format_header)
    worksheet.write('B2', filtros['Marque'].upper(), format)
    worksheet.write('B3', filtros['Modele'], format)
    worksheet.write('B4', filtros['TaillePounce'], format)
    worksheet.write('B5', filtros['Type'], format)
    worksheet.write('B6', filtros['Resolution'][0], format)
    worksheet.write('B7', filtros['Indice_refresh'], format)
    worksheet.write('B8', filtros['3D'], format)
    worksheet.write('B9', filtros['Internet'], format)
    worksheet.write('B10', filtros['Wifi'], format)
    worksheet.write('B11', filtros['Smart'], format)
    worksheet.write('B12', filtros['Design'][0], format)

    for k in range(max_tiendas):
        worksheet.write(13+4*k,1, "", format_NA)
        worksheet.write(14+4*k,1, "", format_NA)
        worksheet.write(15+4*k,1, "", format_NA)

    # <<<<<<<<<<<<<
    # 7) AMAZON
    # <<<<<<<<<<<<<

    for producto in json_data:

        if producto['tiendas'][0]['precio'] == ' EUR': continue

        detalles_string = json.dumps(producto['detalles'])
        ficha_tec_string = json.dumps(producto['ficha_tecnica'])

        worksheet.write(0, icol + 2, "".join(("Produit ", str(icol + 1))), format_header)
        try:
            worksheet.write(1, icol + 2, producto['ficha_tecnica']['Marque'].upper(), format)
        except:
            worksheet.write(1, icol + 2, '', format_NA)
        try:
            worksheet.write(2, icol + 2, producto['ficha_tecnica']["Numéro du modèle de l'article"], format)
        except:
            worksheet.write(2, icol + 2, '', format_NA)
        try:
            if "Ecran" in producto['ficha_tecnica']:
                if 'centimètres' in producto['ficha_tecnica']["Ecran"]:
                    worksheet.write(3, icol + 2, str(round(float(producto['ficha_tecnica']["Ecran"].replace(' centimètres',''))/2.54)) + ' pouces', format)
                else:
                    worksheet.write(3, icol + 2, producto['ficha_tecnica']["Ecran"], format)
            elif "Taille de l'écran" in producto['ficha_tecnica']:
                if 'centimètres' in producto['ficha_tecnica']["Taille de l'écran"]:
                    worksheet.write(3, icol + 2, str(round(float(producto['ficha_tecnica']["Taille de l'écran"].replace(' centimètres',''))/2.54)) + ' pouces', format)
                else:
                    worksheet.write(3, icol + 2, producto['ficha_tecnica']["Taille de l'écran"], format)
            else:
                worksheet.write(3, icol + 2, '', format_NA)
        except:
            worksheet.write(3, icol + 2, '', format_NA)
        try:
            if 'OLED' in detalles_string or 'OLED' in ficha_tec_string or 'OLED' in producto['nombre']:
                worksheet.write(4, icol + 2, 'OLED', format)
            elif 'LED' in detalles_string or 'LED' in ficha_tec_string or 'LED' in producto['nombre']:
                worksheet.write(4, icol + 2, 'LED', format)
            elif 'LCD' in detalles_string or 'LCD' in ficha_tec_string or 'LCD' in producto['nombre']:
                worksheet.write(4, icol + 2, 'LCD', format)
            else:
                worksheet.write(4, icol + 2, '', format_NA)
        except:
            worksheet.write(4, icol + 2, '', format_NA)
        try:
            if '4k' in detalles_string.lower() or '4k' in ficha_tec_string.lower() or '4k' in producto['nombre'].lower() \
            or'4 k' in detalles_string.lower() or '4 k' in ficha_tec_string.lower() or '4 k' in producto['nombre'].lower():
                worksheet.write(5, icol + 2, '4K', format)
            elif '1080' in detalles_string or '1080' in ficha_tec_string or '1080' in producto['nombre']:
                worksheet.write(5, icol + 2, '1080p', format)
            elif '720' in detalles_string or '720' in ficha_tec_string or '720' in producto['nombre']:
                worksheet.write(5, icol + 2, '720', format)
            else:
                worksheet.write(5, icol + 2, '', format_NA)
        except:
            worksheet.write(5, icol + 2, '', format_NA)
        # INDICE DE FLUIDEZ, DIFICIL DE LOCALIZAR
        try:
            worksheet.write(6, icol + 2, '', format_NA)
            # worksheet.write(6, icol + 2, str(producto['detalles']).split('Fluidité  : ')[1].split("', '")[0], format)
        except:
            worksheet.write(6, icol + 2, '', format_NA)
        try:
            if '3d' in detalles_string.lower() or '3d' in ficha_tec_string.lower() or '3d' in producto['nombre'].lower() \
            or'3 d' in detalles_string.lower() or '3 d' in ficha_tec_string.lower() or '3 d' in producto['nombre'].lower():
                worksheet.write(7, icol + 2, 'Oui', format)
            else:
                worksheet.write(7, icol + 2, 'Non', format)
        except:
            worksheet.write(7, icol + 2, '', format_NA)
        try:
            if 'internet' in detalles_string.lower() or 'internet' in ficha_tec_string.lower() or 'internet' in producto['nombre'].lower():
                worksheet.write(8, icol + 2, 'Oui', format)
            else:
                worksheet.write(8, icol + 2, '', format_NA)
        except:
            worksheet.write(8, icol + 2, '', format_NA)
        try:
            if 'wifi' in detalles_string.lower() or 'wifi' in ficha_tec_string.lower() or 'wifi' in producto['nombre'].lower()\
            or 'wi-fi' in detalles_string.lower() or 'wi-fi' in ficha_tec_string.lower() or 'wi-fi' in producto['nombre'].lower()\
            or 'wi fi' in detalles_string.lower() or 'wi fi' in ficha_tec_string.lower() or 'wi fi' in producto['nombre'].lower():
                worksheet.write(9, icol + 2, 'Oui', format)
            else:
                worksheet.write(9, icol + 2, '', format_NA)
        except:
            worksheet.write(9, icol + 2, '', format_NA)
        try:
            if 'smart' in detalles_string.lower() or 'smart' in ficha_tec_string.lower() or 'smart' in producto['nombre'].lower():
                worksheet.write(10, icol + 2, 'Oui', format)
            else:
                worksheet.write(10, icol + 2, '', format_NA)
        except:
            worksheet.write(10, icol + 2, '', format_NA)
        try:
            if 'noir' in detalles_string.lower() or 'noir' in ficha_tec_string.lower() or 'noir' in producto['nombre'].lower():
                worksheet.write(11, icol + 2, 'Noir', format)
            elif 'blanc' in detalles_string.lower() or 'blanc' in ficha_tec_string.lower() or 'blanc' in producto['nombre'].lower():
                worksheet.write(11, icol + 2, 'Blanc', format)     
            elif 'argent' in detalles_string.lower() or 'argent' in ficha_tec_string.lower() or 'argent' in producto['nombre'].lower():
                worksheet.write(11, icol + 2, 'Argent', format)                           
            else:
                worksheet.write(11, icol + 2, '', format_NA)
        except:
            worksheet.write(11, icol + 2, '', format_NA)

        for k in range(max_tiendas):
            if k <= len(producto['tiendas']) - 1:
                worksheet.write(13 + 4 * k, icol + 2, producto['tiendas'][k]['precio'], format)
                worksheet.write(14 + 4 * k, icol + 2, producto['tiendas'][k]['nombre_tienda'], format)
                worksheet.write(15 + 4 * k, icol + 2, producto['tiendas'][k]['url_tienda'], format_url)
            else:
                worksheet.write(13 + 4 * k, icol + 2, "", format_NA)
                worksheet.write(14 + 4 * k, icol + 2, "", format_NA)
                worksheet.write(15 + 4 * k, icol + 2, "", format_NA)

        icol += 1



    # Ancho de columna (todos los productos)
    worksheet.set_column(1, icol + 2, 25)

    # FIN
    workbook.close()

filtros = {
    'Marque': 'SAMSUNG',
    'Modele' : 'UX50JDFKE',
    "TaillePounce": '50',
    'Indice_refresh' : '50',
    "Type": 'LED',
    "Resolution": ['1080p'],
    "Ratio": [''],
    "3D": "Oui",
    "Design" : [""],
    "Wifi" : "",
    "Internet" : "",
    "Smart" : "",
    "Energy" : "",
}

crearExcel(filtros)    