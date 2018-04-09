from io import BytesIO
import json

from django.conf import settings

from xlsxwriter.workbook import Workbook

from apps.scrapy_model.models import Product
from apps.tasks.models import Job


def xlsx_tv(req_xlsx_gen):

    try:
        EXPORT_DATA_TO_EXTERNAL_HOST = settings.EXPORT_DATA_TO_EXTERNAL_HOST
    except AttributeError:
        raise AttributeError(
            "Debe definir en el archivo "
            "settings la variable EXPORT_DATA_TO_EXTERNAL_HOST")

    try:
        TMP_FOLDER = settings.TMP_FOLDER
    except AttributeError:
        raise AttributeError(
            "Debe definir en el archivo "
            "settings la variable TMP_FOLDER")

    job_id = req_xlsx_gen["job_id"]

    if EXPORT_DATA_TO_EXTERNAL_HOST:
        output = BytesIO()
        workbook = Workbook(output)
    else:
        output_file_name = TMP_FOLDER + '/xlsx_' + job_id + '.xlsx'
        workbook = Workbook(output_file_name)

    filtros = req_xlsx_gen["data"][0]

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
    # 3) EXTRACCION DE DATOS DE DB
    # <<<<<<<<<<<<<
    job = Job.objects.get(_job_id=job_id)
    products = job.substitution_similar_results.all()

    list_products_pre = list(products.values_list('pk', 'tiendas'))
    list_products = []
    for i in list_products_pre:
        if i[1] == []:
            continue
        elif i[1][0]['precio'].replace('\xa0',"").replace(" EUR", "").replace(" ", "") != '':
            list_products.append(i)
    # list_products = [i for i in list_products if i[1] != []]
    # list_products = [i for i in list_products if i[1][0]['precio'].replace('\xa0',"").replace(" EUR", "").replace(" ", "") != '']
    list_products = sorted(list_products, key=lambda k: float(k[1][0]['precio'].replace('\xa0',"").replace(" EUR", "").replace(" ", "")))


    # <<<<<<<<<<<<<
    # 4) MAXIMO NUMERO DE TIENDAS
    # <<<<<<<<<<<<<
    max_tiendas = 0

    for product in products:
        if isinstance(product.tiendas, list):
            num_tiendas = len(product.tiendas)
        elif isinstance(product.tiendas, dict):
            num_tiendas = 1
        else:
            raise TypeError("la variable 'tiendas' es un tipo incorrecto")

        if num_tiendas > max_tiendas:
            max_tiendas = num_tiendas

    # FR FR FR FR FR FR FR FR FR FR FR FR FR FR FR FR
    #                FRANCIA
    # FR FR FR FR FR FR FR FR FR FR FR FR FR FR FR FR

    if req_xlsx_gen['country'] == "fr":

        # <<<<<<<<<<<<<
        # 5) DETERMINAMOS LA ESTRUCTURA DEL ARCHIVO EXCEL
        # <<<<<<<<<<<<<

        # Creamos la estructura del archivo excel:
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
            worksheet.write(13 + 4 * k, 0, "Prix", format_header)
            worksheet.write(14 + 4 * k, 0, "Enseigne", format_header)
            worksheet.write(15 + 4 * k, 0, "URL", format_header)

        # <<<<<<<<<<<<<
        # 6) COLUMNA DE PRODUCTO A REEMPLAZAR
        # <<<<<<<<<<<<<
        worksheet.write('B1', "Modèle endommagé", format_header)
        worksheet.write('B2', filtros['Marque'].upper(), format)
        worksheet.write('B3', filtros['Modele'], format)
        worksheet.write('B4', filtros['TaillePounce'], format)
        worksheet.write('B5', filtros['Type'], format)
        worksheet.write('B6', filtros['Resolution'][0], format)
        if filtros['Refresh']:
            filtros['Refresh'] += " Hz"
        worksheet.write('B7', filtros['Refresh'], format)
        worksheet.write('B8', filtros['3D'], format)
        worksheet.write('B9', filtros['Internet'], format)
        worksheet.write('B10', filtros['Wifi'], format)
        worksheet.write('B11', filtros['Smart'], format)
        worksheet.write('B12', filtros['Design'][0], format)

        for k in range(max_tiendas):
            worksheet.write(13 + 4 * k, 1, "", format_NA)
            worksheet.write(14 + 4 * k, 1, "", format_NA)
            worksheet.write(15 + 4 * k, 1, "", format_NA)

        # <<<<<<<<<<<<<
        # 7) ESCRITURA
        # <<<<<<<<<<<<<

        for _product in list_products:
            producto = products.get(pk=_product[0])
        
            # GROUP-DIGITAL <<<<<<<<<<<<<<<<<<<<<<
            if producto.store_id == "6":
                worksheet.write(0,icol+2, "".join(("Produit ",str(icol+1))), format_header)
                try:
                    worksheet.write(1,icol+2, producto.nombre.split(' - ')[0], format)
                except:
                    worksheet.write(1,icol+2,"",format_NA)
                try:
                    worksheet.write(2,icol+2, producto.nombre.split(' - ')[1], format)
                except:
                    worksheet.write(2,icol+2,"",format_NA)
                try:
                    worksheet.write(3,icol+2,str(round(float(producto.ficha_tecnica["Taille de l'écran en cm"])/2.54)),format)
                except:
                    worksheet.write(3,icol+2,"",format_NA)
                try:
                    worksheet.write(4,icol+2,producto.ficha_tecnica["Technologie"],format)
                except:
                    worksheet.write(4,icol+2,"",format_NA)
                try:
                    worksheet.write(5,icol+2,producto.ficha_tecnica["Résolution de l'écran"],format)
                except:
                    worksheet.write(5,icol+2,"",format_NA)
                try:
                    worksheet.write(6,icol+2,producto.ficha_tecnica["Fluidité image en Hz"],format)
                except:
                    worksheet.write(6,icol+2,"",format_NA)
                if str(producto.detalles).find('3D') > 0:
                    worksheet.write(7,icol+2,'Oui',format)
                else:
                    worksheet.write(7,icol+2,'Non',format)
                worksheet.write(8,icol+2,"",format_NA)
                try:
                    worksheet.write(9,icol+2,producto.ficha_tecnica["WiFi"],format)
                except:
                    worksheet.write(9,icol+2,"",format_NA)
                worksheet.write(10,icol+2,"",format_NA)
                try:
                    worksheet.write(11,icol+2,producto.ficha_tecnica["Design"],format)
                except:
                    worksheet.write(11,icol+2,"",format_NA)

                for k in range(max_tiendas):
                    if isinstance(producto.tiendas, list):
                        if k<=len(producto.tiendas)-1:
                            worksheet.write(13+4*k,icol+2, producto.tiendas[k]['precio'], format)
                            worksheet.write(14+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                            worksheet.write(15+4*k,icol+2, producto.tiendas[k]['url_tienda'], format_url)
                        else:
                            worksheet.write(13+4*k,icol+2,"", format_NA)
                            worksheet.write(14+4*k,icol+2, "", format_NA)
                            worksheet.write(15+4*k,icol+2, "", format_NA)
                    else:
                        if len(producto.tiendas) > 0:
                            worksheet.write(13+4*k,icol+2, producto.tiendas['precio'], format)
                            worksheet.write(14+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                            worksheet.write(15+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                        else:
                            worksheet.write(13+4*k,icol+2,"", format_NA)
                            worksheet.write(14+4*k,icol+2, "", format_NA)
                            worksheet.write(15+4*k,icol+2, "", format_NA)

                icol+=1

            # DARTY <<<<<<<<<<<<<<<<<<<<<<
            elif producto.store_id == "1":
                worksheet.write(0,icol+2, "".join(("Produit ",str(icol+1))), format_header)
                try:
                    worksheet.write(1,icol+2, producto.nombre.split()[0].upper(), format)
                except:
                    worksheet.write(1,icol+2,"",format_NA)
                try:    
                    worksheet.write(2,icol+2, producto.nombre.split()[1], format)
                except:
                    worksheet.write(2,icol+2,"",format_NA)
                try:
                    worksheet.write(3,icol+2,producto.ficha_tecnica["Taille d'écran (pouces)"].split()[0],format)
                except:
                    worksheet.write(3,icol+2,"",format_NA)
                try:
                    worksheet.write(4,icol+2,producto.ficha_tecnica['Type de rétroéclairage'],format)
                except:
                    worksheet.write(4,icol+2,"",format_NA)
                try:
                    worksheet.write(5,icol+2,producto.ficha_tecnica['Norme HD'],format)
                except:
                    worksheet.write(5,icol+2,"",format_NA)
               # worksheet.write(6,icol+2,producto.ficha_tecnica["Fluidité de l'image"].split('PQI ')[-1][:-1],format)

                try:
                    worksheet.write(6,icol+2,producto.ficha_tecnica["Fluidité de l'image"],format)
                except KeyError:
                    worksheet.write(6,icol+2,"",format_NA)
                try:
                    worksheet.write(7,icol+2,producto.ficha_tecnica["Compatibilité 3D"],format)
                except KeyError:
                    worksheet.write(7,icol+2,"",format_NA)
                if str(producto.detalles).find('Navigateur internet') > 0:
                    worksheet.write(8 , icol+2, 'Oui',format)
                else:
                    worksheet.write(8, icol+2, 'Non',format)
                if str(producto.detalles).find('Wifi intégré') > 0:
                    worksheet.write(9,icol+2,'Oui',format)
                else:
                    worksheet.write(9,icol+2,'Non',format)
                if str(producto.detalles).find('Smart TV') > 0:
                    worksheet.write(10,icol+2,'Oui',format)
                else:
                    worksheet.write(10,icol+2,'Non',format)
                if str(producto.detalles).find('Design') > 0:
                    worksheet.write(11,icol+2,str(producto.detalles).split('Design ')[1].split()[0][:-2],format)
                else:
                    worksheet.write(11,icol+2,'',format_NA)

                for k in range(max_tiendas):
                    if isinstance(producto.tiendas, list):
                        if k<=len(producto.tiendas)-1:
                            worksheet.write(13+4*k,icol+2, producto.tiendas[k]['precio'], format)
                            worksheet.write(14+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                            worksheet.write(15+4*k,icol+2, producto.tiendas[k]['url_tienda'], format_url)
                        else:
                            worksheet.write(13+4*k,icol+2,"", format_NA)
                            worksheet.write(14+4*k,icol+2, "", format_NA)
                            worksheet.write(15+4*k,icol+2, "", format_NA)
                    else:
                        if len(producto.tiendas) > 0:
                            worksheet.write(13+4*k,icol+2, producto.tiendas['precio'], format)
                            worksheet.write(14+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                            worksheet.write(15+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                        else:
                            worksheet.write(13+4*k,icol+2,"", format_NA)
                            worksheet.write(14+4*k,icol+2, "", format_NA)
                            worksheet.write(15+4*k,icol+2, "", format_NA)

                icol+=1

            # KELKOO <<<<<<<<<<<<<<<<<<<<<<
            elif producto.store_id == "2":
                worksheet.write(0,icol+2, "".join(("Produit ",str(icol+1))), format_header)
                try:
                    worksheet.write(1,icol+2, producto.nombre.split()[0].upper(), format)
                except:
                    worksheet.write(1,icol+2,"",format_NA)
                try:
                    worksheet.write(2,icol+2, producto.nombre[len(producto.nombre.split()[0])+1:], format)
                except:
                    worksheet.write(2,icol+2,"",format_NA)
                try:
                    worksheet.write(3,icol+2, str(round(float(products.filter(store_id="2")[0].detalles[0].split()[-1][:-2].replace(',','.'))/2.54)),format)
                except:
                    worksheet.write(3,icol+2,"",format_NA)
                try:
                    worksheet.write(4,icol+2,producto.ficha_tecnica["Type de TV"].split()[1],format)
                except KeyError:
                    worksheet.write(4,icol+2,"",format_NA)
                try:
                    worksheet.write(5,icol+2,producto.ficha_tecnica["Compatibilité HD"],format)
                except KeyError:
                    worksheet.write(5,icol+2,"",format_NA)
                try:
                    worksheet.write(6,icol+2,producto.ficha_tecnica["Fréquence de rafraîchissement"],format)
                except KeyError:
                    worksheet.write(6,icol+2,"",format_NA)

                if 'Type de TV' in producto.ficha_tecnica:
                    if '3D' in producto.ficha_tecnica['Type de TV']:
                        worksheet.write(7,icol+2,'Oui',format)
                    else:
                        worksheet.write(7,icol+2,'Non',format)
                else:
                    worksheet.write(7,icol+2,'Non',format)

                try:
                    if 'Ethernet' in producto.ficha_tecnica['Connectique'] or 'Internet' in producto.ficha_tecnica['Connectique']:
                        worksheet.write(8, icol + 2, 'Oui', format)
                    else:
                        worksheet.write(8, icol + 2, '', format_NA)
                except:
                    worksheet.write(8,icol+2, '', format_NA)
                try:
                    if 'Wifi' in producto.ficha_tecnica['Connectique']:
                        worksheet.write(9, icol + 2, 'Oui', format)
                    else:
                        worksheet.write(9, icol + 2, '', format_NA)
                except:
                    worksheet.write(9,icol+2, '', format_NA)

                if 'Type de TV' in producto.ficha_tecnica:

                    if 'TV Connect' in producto.ficha_tecnica['Type de TV']:
                        worksheet.write(10,icol+2,'Oui',format)
                    else:
                        worksheet.write(10,icol+2,'',format_NA)
                else:
                    worksheet.write(10,icol+2,'',format_NA)
                worksheet.write(11,icol+2,'',format_NA)

                for k in range(max_tiendas):
                    if isinstance(producto.tiendas, list):
                        if k<=len(producto.tiendas)-1:
                            worksheet.write(13+4*k,icol+2, producto.tiendas[k]['precio'], format)
                            if (producto.tiendas[k]['nombre_tienda']) == '':
                                worksheet.write(14 + 4 * k, icol + 2, '', format_NA)
                            else:
                                worksheet.write(14+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                            worksheet.write(15+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                        else:
                            worksheet.write(13+4*k,icol+2,"", format_NA)
                            worksheet.write(14+4*k,icol+2, "", format_NA)
                            worksheet.write(15+4*k,icol+2, "", format_NA)
                    else:
                        if len(producto.tiendas) > 0:
                            worksheet.write(13+4*k,icol+2, producto.tiendas['precio'], format)
                            worksheet.write(14+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                            worksheet.write(15+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                        else:
                            worksheet.write(13+4*k,icol+2,"", format_NA)
                            worksheet.write(14+4*k,icol+2, "", format_NA)
                            worksheet.write(15+4*k,icol+2, "", format_NA)

                icol+=1

            # PRICERUNNER <<<<<<<<<<<<<<<<<<<<<<
            elif producto.store_id == "4":
                worksheet.write(0,icol+2, "".join(("Produit ",str(icol+1))), format_header)
                try:
                    if "Smart Tech" in producto.nombre:
                        worksheet.write(1,icol+2, "SMART TECH", format)    
                    else:
                        worksheet.write(1,icol+2, producto.nombre.split()[0].upper(), format)
                except:
                    worksheet.write(1,icol+2,"",format_NA)
                try:
                    worksheet.write(2, icol + 2, producto.nombre[len(producto.nombre.split()[0])+1:], format)
                except ValueError:
                    worksheet.write(2, icol + 2, producto.nombre, format)
                except IndexError:
                    worksheet.write(2, icol + 2, producto.nombre.split(filtros['Marque'])[0], format)
                try:
                    worksheet.write(3,icol+2, producto.ficha_tecnica["Taille de l'écran La taille de l'écran est mesurée en centimètres, en diagonale à partir du coin inférieur jusqu'au coin supérieur opposé."],format)
                except:
                    worksheet.write(3,icol+2,"",format_NA)
                try:
                    worksheet.write(4,icol+2, producto.detalles[1],format)
                except:
                    worksheet.write(4,icol+2,"",format_NA)
                try:
                    worksheet.write(5,icol+2, producto.ficha_tecnica["Format vidéo Ceci sert à indiquer combien de lignes, ou de pixels, est capable d’afficher l’écran du téléviseur.Le 4K Ultra HD est le format de l’avenir. Cette norme est 4 fois supérieure au Full HD en nombre de pixels. La résolution est d’au moins 3840x2160 et peut s’étendre jusqu’à 4096x3112. Le 1080p b> et le 720p b> font aussi partie de la norme HDTV. Le nombre indique combien de lignes horizontales l’image contient. Une résolution 1080p est constituée de 1920x1080 pixels, et le 720p de 1280x720 pixels."],
                                format)
                except:
                    worksheet.write(5,icol+2,"",format_NA)    
                try:
                    worksheet.write(6,icol+2,producto.ficha_tecnica["Fréquence de rafraîchissement"],format)
                except:
                    worksheet.write(6,icol+2,"",format_NA)
                try:
                    worksheet.write(7,icol+2,producto.ficha_tecnica['3D'],format)
                except:
                    worksheet.write(7,icol+2,'Non',format)
                try:
                    worksheet.write(8, icol + 2, producto.ficha_tecnica['Internet'], format)
                except:
                    worksheet.write(8,icol+2, '', format_NA)
                try:
                    if 'Wifi' in producto.ficha_tecnica['Wireless & Streaming']:
                        worksheet.write(9, icol + 2, 'Oui', format)
                    else:
                        worksheet.write(9, icol + 2, 'Non', format)
                except:
                    worksheet.write(9,icol+2, '', format_NA)
                try:
                    if 'TV Connect' in producto.ficha_tecnica['Smart TV']:
                        worksheet.write(10,icol+2,'Oui',format)
                    else:
                        worksheet.write(10,icol+2,'Non',format)
                except:
                    worksheet.write(10, icol + 2, '', format_NA)
                try:
                    worksheet.write(11,icol+2,producto.ficha_tecnica["Conception d'écran"],format)
                except:
                    worksheet.write(11,icol+2,'',format_NA)

                for k in range(max_tiendas):
                    if isinstance(producto.tiendas, list):
                        if k<=len(producto.tiendas)-1:
                            worksheet.write(13+4*k,icol+2, producto.tiendas[k]['precio'], format)
                            if (producto.tiendas[k]['nombre_tienda']) == '':
                                worksheet.write(14 + 4 * k, icol + 2, '', format_NA)
                            else:
                                worksheet.write(14+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                            worksheet.write(15+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                        else:
                            worksheet.write(13+4*k,icol+2,"", format_NA)
                            worksheet.write(14+4*k,icol+2, "", format_NA)
                            worksheet.write(15+4*k,icol+2, "", format_NA)
                    else:
                        if len(producto.tiendas) > 0:
                            worksheet.write(13+4*k,icol+2, producto.tiendas['precio'], format)
                            worksheet.write(14+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                            worksheet.write(15+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                        else:
                            worksheet.write(13+4*k,icol+2,"", format_NA)
                            worksheet.write(14+4*k,icol+2, "", format_NA)
                            worksheet.write(15+4*k,icol+2, "", format_NA)
                icol+=1

            # AMAZON <<<<<<<<<<<<<<<<<<<<<<
            elif producto.store_id == "7":

                if producto.tiendas[0]['precio'] == ' EUR': continue

                detalles_string = json.dumps(producto.detalles)
                ficha_tec_string = json.dumps(producto.ficha_tecnica)

                worksheet.write(0, icol + 2, "".join(("Produit ", str(icol + 1))), format_header)
                try:
                    worksheet.write(1, icol + 2, producto.ficha_tecnica['Marque'].upper(), format)
                except:
                    worksheet.write(1, icol + 2, '', format_NA)
                try:
                    worksheet.write(2, icol + 2, producto.ficha_tecnica["Numéro du modèle de l'article"], format)
                except:
                    worksheet.write(2, icol + 2, '', format_NA)
                try:
                    if "Ecran" in producto.ficha_tecnica:
                        if 'centimètres' in producto.ficha_tecnica["Ecran"]:
                            worksheet.write(3, icol + 2, str(round(float(producto.ficha_tecnica["Ecran"].replace(' centimètres',''))/2.54)) + ' pouces', format)
                        else:
                            worksheet.write(3, icol + 2, producto.ficha_tecnica["Ecran"], format)
                    elif "Taille de l'écran" in producto.ficha_tecnica:
                        if 'centimètres' in producto.ficha_tecnica["Taille de l'écran"]:
                            worksheet.write(3, icol + 2, str(round(float(producto.ficha_tecnica["Taille de l'écran"].replace(' centimètres',''))/2.54)) + ' pouces', format)
                        else:
                            worksheet.write(3, icol + 2, producto.ficha_tecnica["Taille de l'écran"], format)
                    else:
                        worksheet.write(3, icol + 2, '', format_NA)
                except:
                    worksheet.write(3, icol + 2, '', format_NA)
                try:
                    if 'OLED' in detalles_string or 'OLED' in ficha_tec_string or 'OLED' in producto.nombre:
                        worksheet.write(4, icol + 2, 'OLED', format)
                    elif 'LED' in detalles_string or 'LED' in ficha_tec_string or 'LED' in producto.nombre:
                        worksheet.write(4, icol + 2, 'LED', format)
                    elif 'LCD' in detalles_string or 'LCD' in ficha_tec_string or 'LCD' in producto.nombre:
                        worksheet.write(4, icol + 2, 'LCD', format)
                    else:
                        worksheet.write(4, icol + 2, '', format_NA)
                except:
                    worksheet.write(4, icol + 2, '', format_NA)
                try:
                    if '4k' in detalles_string.lower() or '4k' in ficha_tec_string.lower() or '4k' in producto.nombre.lower() \
                    or'4 k' in detalles_string.lower() or '4 k' in ficha_tec_string.lower() or '4 k' in producto.nombre.lower():
                        worksheet.write(5, icol + 2, '4K', format)
                    elif '1080' in detalles_string or '1080' in ficha_tec_string or '1080' in producto.nombre:
                        worksheet.write(5, icol + 2, '1080p', format)
                    elif '720' in detalles_string or '720' in ficha_tec_string or '720' in producto.nombre:
                        worksheet.write(5, icol + 2, '720', format)
                    else:
                        worksheet.write(5, icol + 2, '', format_NA)
                except:
                    worksheet.write(5, icol + 2, '', format_NA)
                # INDICE DE FLUIDEZ, DIFICIL DE LOCALIZAR
                try:
                    worksheet.write(6, icol + 2, '', format_NA)
                    # worksheet.write(6, icol + 2, str(producto.detalles).split('Fluidité  : ')[1].split("', '")[0], format)
                except:
                    worksheet.write(6, icol + 2, '', format_NA)
                try:
                    if '3d' in detalles_string.lower() or '3d' in ficha_tec_string.lower() or '3d' in producto.nombre.lower() \
                    or'3 d' in detalles_string.lower() or '3 d' in ficha_tec_string.lower() or '3 d' in producto.nombre.lower():
                        worksheet.write(7, icol + 2, 'Oui', format)
                    else:
                        worksheet.write(7, icol + 2, 'Non', format)
                except:
                    worksheet.write(7, icol + 2, '', format_NA)
                try:
                    if 'internet' in detalles_string.lower() or 'internet' in ficha_tec_string.lower() or 'internet' in producto.nombre.lower():
                        worksheet.write(8, icol + 2, 'Oui', format)
                    else:
                        worksheet.write(8, icol + 2, '', format_NA)
                except:
                    worksheet.write(8, icol + 2, '', format_NA)
                try:
                    if 'wifi' in detalles_string.lower() or 'wifi' in ficha_tec_string.lower() or 'wifi' in producto.nombre.lower()\
                    or 'wi-fi' in detalles_string.lower() or 'wi-fi' in ficha_tec_string.lower() or 'wi-fi' in producto.nombre.lower()\
                    or 'wi fi' in detalles_string.lower() or 'wi fi' in ficha_tec_string.lower() or 'wi fi' in producto.nombre.lower():
                        worksheet.write(9, icol + 2, 'Oui', format)
                    else:
                        worksheet.write(9, icol + 2, '', format_NA)
                except:
                    worksheet.write(9, icol + 2, '', format_NA)
                try:
                    if 'smart' in detalles_string.lower() or 'smart' in ficha_tec_string.lower() or 'smart' in producto.nombre.lower():
                        worksheet.write(10, icol + 2, 'Oui', format)
                    else:
                        worksheet.write(10, icol + 2, '', format_NA)
                except:
                    worksheet.write(10, icol + 2, '', format_NA)
                try:
                    if 'noir' in detalles_string.lower() or 'noir' in ficha_tec_string.lower() or 'noir' in producto.nombre.lower():
                        worksheet.write(11, icol + 2, 'Noir', format)
                    elif 'blanc' in detalles_string.lower() or 'blanc' in ficha_tec_string.lower() or 'blanc' in producto.nombre.lower():
                        worksheet.write(11, icol + 2, 'Blanc', format)     
                    elif 'argent' in detalles_string.lower() or 'argent' in ficha_tec_string.lower() or 'argent' in producto.nombre.lower():
                        worksheet.write(11, icol + 2, 'Argent', format)                           
                    else:
                        worksheet.write(11, icol + 2, '', format_NA)
                except:
                    worksheet.write(11, icol + 2, '', format_NA)

                for k in range(max_tiendas):
                    if isinstance(producto.tiendas, list):
                        if k<=len(producto.tiendas)-1:
                            worksheet.write(13+4*k,icol+2, producto.tiendas[k]['precio'], format)
                            if (producto.tiendas[k]['nombre_tienda']) == '':
                                worksheet.write(14 + 4 * k, icol + 2, '', format_NA)
                            else:
                                worksheet.write(14+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                            worksheet.write(15+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                        else:
                            worksheet.write(13+4*k,icol+2,"", format_NA)
                            worksheet.write(14+4*k,icol+2, "", format_NA)
                            worksheet.write(15+4*k,icol+2, "", format_NA)
                    else:
                        if len(producto.tiendas) > 0:
                            worksheet.write(13+4*k,icol+2, producto.tiendas['precio'], format)
                            worksheet.write(14+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                            worksheet.write(15+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                        else:
                            worksheet.write(13+4*k,icol+2,"", format_NA)
                            worksheet.write(14+4*k,icol+2, "", format_NA)
                            worksheet.write(15+4*k,icol+2, "", format_NA)

                icol += 1

            # LCD-COMPARE <<<<<<<<<<<<<<<<<<<<<<
            elif producto.store_id == "9":

                detalles_string = json.dumps(producto.detalles)
                ficha_tec_string = json.dumps(producto.ficha_tecnica)

                worksheet.write(0, icol + 2, "".join(("Produit ", str(icol + 1))), format_header)
                try:
                    worksheet.write(1, icol + 2, producto.nombre.split()[0], format)
                except:
                    worksheet.write(3, icol + 2, '', format_NA)
                try:
                    worksheet.write(2, icol + 2, producto.nombre.split()[1], format)
                except:
                    worksheet.write(2, icol + 2, '', format_NA)
                try:
                    if 'Surface visible' in producto.ficha_tecnica:
                        worksheet.write(3, icol + 2, producto.ficha_tecnica['Surface visible'].split()[2][1:-2], format)
                    elif ' cm' in ficha_tec_string:
                        worksheet.write(3, icol + 2, str(int(float(ficha_tec_string.split(' cm')[0].split()[-1])/2.54)), format)
                    else:
                        worksheet.write(3, icol + 2, '', format_NA)
                except:
                    worksheet.write(3, icol + 2, '', format_NA)
                try:
                    if 'Rétroéclairage' in producto.ficha_tecnica:
                        worksheet.write(4, icol + 2, producto.ficha_tecnica['Rétroéclairage'].split()[0], format)
                    elif 'OLED' in ficha_tec_string or 'OLED' in ficha_tec_string or 'OLED' in producto.nombre:
                        worksheet.write(4, icol + 2, 'OLED', format)
                    elif 'LED' in ficha_tec_string or 'LED' in ficha_tec_string or 'LED' in producto.nombre:
                        worksheet.write(4, icol + 2, 'LED', format)
                    elif 'LCD' in ficha_tec_string or 'LCD' in ficha_tec_string or 'LCD' in producto.nombre:
                        worksheet.write(4, icol + 2, 'LCD', format)                                             
                    else:
                        worksheet.write(4, icol + 2, producto.detalles[0].split()[1], format)
                except:
                    worksheet.write(4, icol + 2, '', format_NA)
                try:
                    if 'Format / Norme' in producto.ficha_tecnica:
                        worksheet.write(5, icol + 2, producto.ficha_tecnica['Format / Norme'].split(' : ')[0], format)
                    elif '4k' in ficha_tec_string.lower() or '4k' in ficha_tec_string.lower() or '4k' in producto.nombre.lower() \
                    or'4 k' in ficha_tec_string.lower() or '4 k' in ficha_tec_string.lower() or '4 k' in producto.nombre.lower():
                        worksheet.write(5, icol + 2, '4K', format)
                    elif '1080' in ficha_tec_string or '1080' in ficha_tec_string or '1080' in producto.nombre:
                        worksheet.write(5, icol + 2, '1080p', format)
                    elif '720' in ficha_tec_string or '720' in ficha_tec_string or '720' in producto.nombre:
                        worksheet.write(5, icol + 2, '720', format)                                            
                    else:
                        worksheet.write(4, icol + 2, producto.detalles[0].split()[1], format)
                except:
                    worksheet.write(5, icol + 2, '', format_NA)
                try:
                    worksheet.write(6, icol + 2, str(producto.detalles).split('Fluidité')[1].split("', '")[0], format)
                except:
                    worksheet.write(6, icol + 2, '', format_NA)
                try:
                    if 'TV 3D' in detalles_string or 'TV 3D' in ficha_tec_string:
                        worksheet.write(7, icol + 2, 'Oui', format)
                    else:
                        worksheet.write(7, icol + 2, '', format_NA)
                except:
                    worksheet.write(7, icol + 2, '', format_NA)
                try:
                    if "Navigateur Internet" in detalles_string:
                        worksheet.write(8, icol + 2, 'Oui', format)
                    elif 'internet' in ficha_tec_string.lower() or 'internet' in ficha_tec_string.lower() or 'internet' in producto.nombre.lower():
                        worksheet.write(8, icol + 2, 'Oui', format)
                    else:
                        worksheet.write(8, icol + 2, '', format_NA)
                except:
                    worksheet.write(8, icol + 2, '', format_NA)
                try:
                    if "Wi-Fi" in detalles_string:
                        worksheet.write(9, icol + 2, 'Oui', format)
                    elif 'wifi' in ficha_tec_string.lower() or 'wifi' in ficha_tec_string.lower() or 'wifi' in producto.nombre.lower()\
                    or 'wi-fi' in ficha_tec_string.lower() or 'wi-fi' in ficha_tec_string.lower() or 'wi-fi' in producto.nombre.lower()\
                    or 'wi fi' in ficha_tec_string.lower() or 'wi fi' in ficha_tec_string.lower() or 'wi fi' in producto.nombre.lower():
                        worksheet.write(9, icol + 2, 'Oui', format)
                    else:
                        worksheet.write(9, icol + 2, '', format_NA)    
                except:
                    worksheet.write(9, icol + 2, '', format_NA)
                try:
                    if 'Smart TV' in detalles_string:
                        worksheet.write(10, icol + 2, 'Oui', format)
                    elif 'smart' in ficha_tec_string.lower() or 'smart' in ficha_tec_string.lower() or 'smart' in producto.nombre.lower():
                        worksheet.write(10, icol + 2, 'Oui', format)
                    else:
                        worksheet.write(10, icol + 2, '', format_NA)
                except:
                    worksheet.write(10, icol + 2, '', format_NA)
                try:
                    if 'Design' in detalles_string:
                        worksheet.write(11, icol + 2, str(producto.detalles).split('Design')[1][:-2].replace(' :',''), format)
                    elif 'incurvé' in ficha_tec_string or 'curve' in ficha_tec_string:
                        worksheet.write(11, icol + 2, "Incurvé", format)                        
                    elif 'plat' in ficha_tec_string or 'slim' in ficha_tec_string:
                        worksheet.write(11, icol + 2, "Slim", format)
                    else:
                        worksheet.write(11, icol + 2, '', format_NA)
                except:
                    worksheet.write(11, icol + 2, '', format_NA)

                for k in range(max_tiendas):
                    if isinstance(producto.tiendas, list):
                        if k<=len(producto.tiendas)-1:
                            worksheet.write(13+4*k,icol+2, producto.tiendas[k]['precio'], format)
                            if (producto.tiendas[k]['nombre_tienda']) == '':
                                worksheet.write(14 + 4 * k, icol + 2, '', format_NA)
                            else:
                                worksheet.write(14+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                            worksheet.write(15+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                        else:
                            worksheet.write(13+4*k,icol+2,"", format_NA)
                            worksheet.write(14+4*k,icol+2, "", format_NA)
                            worksheet.write(15+4*k,icol+2, "", format_NA)
                    else:
                        if len(producto.tiendas) > 0:
                            worksheet.write(13+4*k,icol+2, producto.tiendas['precio'], format)
                            worksheet.write(14+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                            worksheet.write(15+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                        else:
                            worksheet.write(13+4*k,icol+2,"", format_NA)
                            worksheet.write(14+4*k,icol+2, "", format_NA)
                            worksheet.write(15+4*k,icol+2, "", format_NA)
                icol+=1                


    # ES ES ES ES ES ES ES ES ES ES ES ES ES ES ES ES
    #                ESPANA
    # ES ES ES ES ES ES ES ES ES ES ES ES ES ES ES ES

    elif req_xlsx_gen['country'] == "es":

        # <<<<<<<<<<<<<
        # 5) DETERMINAMOS LA ESTRUCTURA DEL ARCHIVO EXCEL
        # <<<<<<<<<<<<<

        #Creamos la estructura del archivo excel:
        worksheet.write('A2', "Marca", format_header)
        worksheet.write('A3', "Modelo", format_header)
        worksheet.write('A4', "Diagonal (pulgadas)", format_header)
        worksheet.write('A5', "Tipo de pantalla", format_header)
        worksheet.write('A6', "Resolución", format_header)
        worksheet.write('A7', "Frecuencia", format_header)
        worksheet.write('A8', "3D", format_header)
        worksheet.write('A9', "Internet", format_header)
        worksheet.write('A10', "Wifi integrado", format_header)
        worksheet.write('A11', "Smart", format_header)
        worksheet.write('A12', "Otras", format_header)

        for k in range(max_tiendas):
            worksheet.write(13+4*k,0, "Prix", format_header)
            worksheet.write(14+4*k,0, "Enseigne", format_header)
            worksheet.write(15+4*k,0, "URL", format_header)

        # <<<<<<<<<<<<<
        # 6) COLUMNA DE PRODUCTO A REEMPLAZAR
        # <<<<<<<<<<<<<

        worksheet.write('B1', "Modelo dañado", format_header)
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

        for _product in list_products:
            producto = products.get(pk=_product[0])
        
            # MEDIAMARKT <<<<<<<<<<<<<<<<<<<<<<
            if producto.store_id == "8":
                worksheet.write(0, icol + 2, "".join(("Producto ", str(icol + 1))), format_header)
                try:
                    worksheet.write(1, icol + 2, producto.nombre.split(' - ')[1].split()[0].upper(), format)
                except:
                    worksheet.write(1, icol + 2, '', format_NA)
                try:
                    worksheet.write(2, icol + 2, producto.nombre.split(' - ')[1].split()[1], format)
                except:
                    worksheet.write(2, icol + 2, '', format_NA)
                try:
                    worksheet.write(3, icol + 2, producto.ficha_tecnica["Pantalla diagonal (pulgadas)"], format)
                except:
                    worksheet.write(3, icol + 2, '', format_NA)
                try:
                    worksheet.write(4, icol + 2, producto.ficha_tecnica['Tecnología del televisor'], format)
                except:
                    worksheet.write(4, icol + 2, '', format_NA)
                try:
                    worksheet.write(5, icol + 2, producto.ficha_tecnica['Resolución (píxeles)'], format)
                except:
                    worksheet.write(5, icol + 2, '', format_NA)
                try:
                    worksheet.write(6, icol + 2, producto.ficha_tecnica["Frecuencia (Hz)"], format)
                except:
                    worksheet.write(6, icol + 2, '', format_NA)
                try:
                    worksheet.write(7, icol + 2, producto.ficha_tecnica['3D'], format)
                except:
                    worksheet.write(7, icol + 2, '', format_NA)
                try:
                    worksheet.write(8, icol + 2, producto.ficha_tecnica['Internet'], format)
                except:
                    worksheet.write(8, icol + 2, '', format_NA)
                try:
                    worksheet.write(9, icol + 2, producto.ficha_tecnica['WiFi'], format)
                except:
                    worksheet.write(9, icol + 2, '', format_NA)
                try:
                    worksheet.write(10, icol + 2, producto.ficha_tecnica['Smart TV'], format)
                except:
                    worksheet.write(10, icol + 2, '', format_NA)
                try:
                    worksheet.write(11, icol + 2, producto.ficha_tecnica['Diseño pantalla'], format)
                except:
                    worksheet.write(11, icol + 2, '', format_NA)

                for k in range(max_tiendas):
                    if isinstance(producto.tiendas, list):
                        if k<=len(producto.tiendas)-1:
                            worksheet.write(13+4*k,icol+2, producto.tiendas[k]['precio'], format)
                            if (producto.tiendas[k]['nombre_tienda']) == '':
                                worksheet.write(14 + 4 * k, icol + 2, '', format_NA)
                            else:
                                worksheet.write(14+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                            worksheet.write(15+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                        else:
                            worksheet.write(13+4*k,icol+2,"", format_NA)
                            worksheet.write(14+4*k,icol+2, "", format_NA)
                            worksheet.write(15+4*k,icol+2, "", format_NA)
                    else:
                        if len(producto.tiendas) > 0:
                            worksheet.write(13+4*k,icol+2, producto.tiendas['precio'], format)
                            worksheet.write(14+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                            worksheet.write(15+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                        else:
                            worksheet.write(13+4*k,icol+2,"", format_NA)
                            worksheet.write(14+4*k,icol+2, "", format_NA)
                            worksheet.write(15+4*k,icol+2, "", format_NA)

                icol += 1



    # Ancho de columna (todos los productos)
    worksheet.set_column(1, icol + 2, 25)

    # FIN
    workbook.close()

    if EXPORT_DATA_TO_EXTERNAL_HOST:
        xlsx_bytes = output.getvalue()
        return xlsx_bytes

    return None


def xlsx_mobile(req_xlsx_gen):

    try:
        EXPORT_DATA_TO_EXTERNAL_HOST = settings.EXPORT_DATA_TO_EXTERNAL_HOST
    except AttributeError:
        raise AttributeError(
            "Debe definir en el archivo "
            "settings la variable EXPORT_DATA_TO_EXTERNAL_HOST")

    try:
        TMP_FOLDER = settings.TMP_FOLDER
    except AttributeError:
        raise AttributeError(
            "Debe definir en el archivo "
            "settings la variable TMP_FOLDER")

    job_id = req_xlsx_gen["job_id"]

    if EXPORT_DATA_TO_EXTERNAL_HOST:
        output = BytesIO()
        workbook = Workbook(output)
    else:
        output_file_name = TMP_FOLDER + '/xlsx_' + job_id + '.xlsx'
        workbook = Workbook(output_file_name)

    filtros = req_xlsx_gen["data"][0]

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
    # 3) EXTRACCION DE DATOS DE DB
    # <<<<<<<<<<<<<
    job = Job.objects.get(_job_id=job_id)
    products = job.substitution_similar_results.all()

    list_products_pre = list(products.values_list('pk', 'tiendas'))
    list_products = []
    for i in list_products_pre:
        if i[1] == []:
            continue
        elif i[1][0]['precio'].replace('\xa0',"").replace(" EUR", "").replace(" ", "") != '':
            list_products.append(i)
    # list_products = [i for i in list_products if i[1] != []]
    # list_products = [i for i in list_products if i[1][0]['precio'].replace('\xa0',"").replace(" EUR", "").replace(" ", "") != '']
    list_products = sorted(list_products, key=lambda k: float(k[1][0]['precio'].replace('\xa0',"").replace(" EUR", "").replace(" ", "")))


    # <<<<<<<<<<<<<
    # 4) MAXIMO NUMERO DE TIENDAS
    # <<<<<<<<<<<<<
    max_tiendas = 0

    for product in products:
        if isinstance(product.tiendas, list):
            num_tiendas = len(product.tiendas)
        elif isinstance(product.tiendas, dict):
            num_tiendas = 1
        else:
            raise TypeError("la variable 'tiendas' es un tipo incorrecto")

        if num_tiendas > max_tiendas:
            max_tiendas = num_tiendas

    # <<<<<<<<<<<<<
    # 5) DETERMINAMOS LA ESTRUCTURA DEL ARCHIVO EXCEL
    # <<<<<<<<<<<<<

    #Creamos la estructura del archivo excel:
    worksheet.write('A2', "Marque", format_header)
    worksheet.write('A3', "Modèle", format_header)
    worksheet.write('A4', "Système d'exploitation", format_header)
    worksheet.write('A5', "Taille d’écran", format_header)
    worksheet.write('A6', "Résolution d’écran", format_header)
    worksheet.write('A7', "Stockage", format_header)
    worksheet.write('A8', "RAM", format_header)
    worksheet.write('A9', "Caméra frontale mégapixels", format_header)
    worksheet.write('A10', "Caméra arrière mégapixels", format_header)
    worksheet.write('A11', 'Capacité batterie (mAh)', format_header)
    worksheet.write('A12', "Couleur", format_header)

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
    worksheet.write('B4', filtros['Systeme dexploitation'], format)
    worksheet.write('B5', filtros['Taille'], format)
    worksheet.write('B6', filtros['Resolution'], format)
    worksheet.write('B7', filtros['Memoire'], format)
    worksheet.write('B8', filtros['Ram'], format)
    worksheet.write('B9', filtros['MegapixelsFrontale'], format)
    worksheet.write('B10', filtros['MegapixelsArriere'], format)
    worksheet.write('B11', filtros['CapaciteBatterie'], format)
    worksheet.write('B12', filtros['Couleur'], format)

    for k in range(max_tiendas):
        worksheet.write(13+4*k,1, "", format_NA)
        worksheet.write(14+4*k,1, "", format_NA)
        worksheet.write(15+4*k,1, "", format_NA)

    # <<<<<<<<<<<<<
    # 7) ESCRITURA
    # <<<<<<<<<<<<<

    for _product in list_products:
        producto = products.get(pk=_product[0])
    
        # PRICERUNNER <<<<<<<<<<<<<<<<<<<<<<
        if producto.store_id == "4":

            if producto.tiendas==[]: continue

            worksheet.write(0, icol + 2, "".join(("Produit ", str(icol + 1))), format_header)
            try:
                worksheet.write(1, icol + 2, producto.ficha_tecnica['Marque'].upper(), format)
            except:
                worksheet.write(1, icol + 2, '', format_NA)
            try:
                worksheet.write(2, icol + 2, producto.nombre.split(producto.ficha_tecnica['Marque'])[1][1:], format)
            except ValueError:
                worksheet.write(2, icol + 2, producto.nombre, format)
            except IndexError:
                worksheet.write(2, icol + 2, producto.nombre.split(producto.ficha_tecnica['Marque']), format)
            try:
                worksheet.write(3, icol + 2, producto.ficha_tecnica["Système d'Exploitation"], format)
            except:
                worksheet.write(3, icol + 2, '', format_NA)
            try:
                worksheet.write(4, icol + 2, producto.detalles[1], format)
            except:
                worksheet.write(4, icol + 2, '', format_NA)
            try:
                worksheet.write(5, icol + 2, producto.ficha_tecnica["Taille de l'écran"], format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                worksheet.write(6, icol + 2, producto.ficha_tecnica['Mémoire interne'], format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                worksheet.write(7, icol + 2, producto.ficha_tecnica['RAM'], format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                worksheet.write(8, icol + 2, producto.ficha_tecnica["Caméra frontale mégapixels"], format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                worksheet.write(9, icol + 2, producto.ficha_tecnica["Megapixels Indique la résolution en megapixels de l'appareil photo intégré."], format)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                worksheet.write(10, icol + 2, producto.ficha_tecnica["La capacité de la batterie (mAh)"], format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica["Colour"], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(13+4*k,icol+2, producto.tiendas[k]['precio'], format)
                        worksheet.write(14+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(15+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(13+4*k,icol+2,"", format_NA)
                        worksheet.write(14+4*k,icol+2, "", format_NA)
                        worksheet.write(15+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(13+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(14+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(15+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                    else:
                        worksheet.write(13+4*k,icol+2,"", format_NA)
                        worksheet.write(14+4*k,icol+2, "", format_NA)
                        worksheet.write(15+4*k,icol+2, "", format_NA)

            icol += 1

        # BOULANGER <<<<<<<<<<<<<<<<<<<<<<
        if producto.store_id == "3":
            worksheet.write(0,icol+2, "".join(("Produit ",str(icol+1))), format_header)
            worksheet.write(1,icol+2, filtros['Marque'].upper(), format)
            try:
                worksheet.write(2, icol + 2, producto.nombre.split(filtros["Marque"])[1][1:], format)
            except ValueError:
                worksheet.write(2, icol + 2, producto.nombre, format)
            except IndexError:
                worksheet.write(2, icol + 2, producto.nombre.split(filtros["Marque"])[0], format)
            worksheet.write(3, icol + 2, producto.ficha_tecnica["Système d'exploitation"], format)
            try:
                worksheet.write(4,icol+2,producto.ficha_tecnica['Taille'].split()[0],format)
            except:
                worksheet.write(4, icol + 2,'', format_NA)
            try:
                worksheet.write(5, icol + 2, producto.ficha_tecnica["Résolution de l'écran"], format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                worksheet.write(6, icol + 2, producto.ficha_tecnica["Mémoire interne"] + ' GB', format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                worksheet.write(7, icol + 2, producto.ficha_tecnica['Mémoire RAM'], format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                worksheet.write(8, icol + 2, producto.ficha_tecnica["Résolution caméra avant (Selfie)"], format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                worksheet.write(9, icol + 2, producto.ficha_tecnica["Photos"], format)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                worksheet.write(10, icol + 2, producto.ficha_tecnica["Capacité de la batterie (mAh)"], format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica["Couleur"], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(13+4*k,icol+2, producto.tiendas[k]['precio'], format)
                        worksheet.write(14+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(15+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(13+4*k,icol+2,"", format_NA)
                        worksheet.write(14+4*k,icol+2, "", format_NA)
                        worksheet.write(15+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(13+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(14+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(15+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                    else:
                        worksheet.write(13+4*k,icol+2,"", format_NA)
                        worksheet.write(14+4*k,icol+2, "", format_NA)
                        worksheet.write(15+4*k,icol+2, "", format_NA)

            icol += 1

        # KELKOO <<<<<<<<<<<<<<<<<<<<<<
        if producto.store_id == "2":

            if producto.tiendas==[]: continue

            worksheet.write(0,icol+2, "".join(("Produit ",str(icol+1))), format_header)
            marque_kelkoo = producto.ficha_tecnica['Marque']
            find_interr = marque_kelkoo.find('?')
            marque_filtros = filtros['Marque'][:find_interr] + filtros['Marque'][find_interr+1:]
            if marque_filtros == marque_kelkoo.replace('?',''):
                worksheet.write(1,icol+2, filtros['Marque'].upper(), format)
            else:
                worksheet.write(1, icol + 2, producto.ficha_tecnica['Marque'].upper(), format)
            try:
                worksheet.write(2, icol + 2, producto.nombre.split(marque_kelkoo)[1][1:], format)
            except ValueError:
                worksheet.write(2, icol + 2, producto.nombre, format)
            except IndexError:
                worksheet.write(2, icol + 2, producto.nombre.split(marque_kelkoo)[0], format)
            try:
                worksheet.write(3, icol + 2, producto.ficha_tecnica["Système d'exploitation"], format)
            except:
                worksheet.write(3, icol + 2,"", format_NA)
            try:
                worksheet.write(4,icol+2,producto.ficha_tecnica["Taille d'écran"],format)
            except:
                worksheet.write(4, icol + 2,'', format_NA)
            try:
                worksheet.write(5, icol + 2, producto.ficha_tecnica["Résolution de l'écran"], format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                worksheet.write(6, icol + 2, producto.ficha_tecnica["Taille de la mémoire intégrée"], format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                worksheet.write(7, icol + 2, producto.ficha_tecnica['Mémoire RAM'], format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                worksheet.write(8, icol + 2, producto.ficha_tecnica["Résolution caméra avant (Selfie)"], format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                worksheet.write(9, icol + 2, producto.ficha_tecnica["Résolution de l'appareil photo"], format)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                worksheet.write(10, icol + 2, producto.ficha_tecnica["Capacité de la batterie (mAh)"], format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica["Couleur"], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(13+4*k,icol+2, producto.tiendas[k]['precio'], format)
                        worksheet.write(14+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(15+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(13+4*k,icol+2,"", format_NA)
                        worksheet.write(14+4*k,icol+2, "", format_NA)
                        worksheet.write(15+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(13+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(14+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(15+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                    else:
                        worksheet.write(13+4*k,icol+2,"", format_NA)
                        worksheet.write(14+4*k,icol+2, "", format_NA)
                        worksheet.write(15+4*k,icol+2, "", format_NA)

            icol += 1

        # RUE DU COMMERCE <<<<<<<<<<<<<<<<<<<<<<
        if producto.store_id == "5":
            try:
                worksheet.write(0,icol+2, "".join(("Produit ",str(icol+1))), format_header)
            except:
                worksheet.write(0, icol + 2, '', format_NA)
            try:
                worksheet.write(1,icol+2, filtros['Marque'].upper(), format)
            except:
                worksheet.write(1, icol + 2, '', format_NA)
            try:
                worksheet.write(2,icol+2, producto.nombre.split(filtros['Marque'].capitalize())[1][3:], format)
            except:
                worksheet.write(2, icol + 2, '', format_NA)
            try:
                worksheet.write(3,icol+2,producto.ficha_tecnica["Système d'exploitation mobile"],format)
            except:
                worksheet.write(3, icol + 2, '', format_NA)
            try:
                worksheet.write(4,icol+2,producto.ficha_tecnica["Taille d'écran (pouces)"],format)
            except:
                worksheet.write(4, icol + 2, '', format_NA)
            try:
                worksheet.write(5,icol+2,producto.ficha_tecnica["Resolution de l'ecran"],format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                worksheet.write(6, icol + 2, producto.ficha_tecnica["Mémoire intégrée (ROM)"] + ' GB', format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                worksheet.write(7, icol + 2, producto.ficha_tecnica['Mémoire vive installée'], format)
            except:
                try:
                    worksheet.write(7, icol + 2, producto.ficha_tecnica['Mémoire vive installée (Go)'], format)
                except:
                    worksheet.write(7, icol + 2, '', format_NA)
            try:
                worksheet.write(8, icol + 2, producto.ficha_tecnica["Résolution deuxième appareil photo (Mpixels)"], format)
            except:
                try:
                    worksheet.write(8, icol + 2, producto.ficha_tecnica["Résolution deuxième appareil photo"], format)
                except:
                    worksheet.write(8, icol + 2, '', format_NA)
            try:
                worksheet.write(9, icol + 2, producto.ficha_tecnica["Résolution de l'appareil photo (Mpixels)"], format)
            except:
                try:
                    worksheet.write(9, icol + 2, producto.ficha_tecnica["Résolution de l'appareil photo"], format)
                except:
                    worksheet.write(9, icol + 2, '', format_NA)
            try:
                worksheet.write(10, icol + 2, producto.ficha_tecnica["Capacité de la batterie (mAh)"], format)
            except:
                try:
                    worksheet.write(10, icol + 2, producto.ficha_tecnica["Capacité de la batterie"], format)
                except:
                    worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica["Couleur"], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(13+4*k,icol+2, producto.tiendas[k]['precio'], format)
                        worksheet.write(14+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(15+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(13+4*k,icol+2,"", format_NA)
                        worksheet.write(14+4*k,icol+2, "", format_NA)
                        worksheet.write(15+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(13+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(14+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(15+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                    else:
                        worksheet.write(13+4*k,icol+2,"", format_NA)
                        worksheet.write(14+4*k,icol+2, "", format_NA)
                        worksheet.write(15+4*k,icol+2, "", format_NA)


            icol += 1


    # Ancho de columna (todos los productos)
    worksheet.set_column(1, icol + 2, 30)

    # FIN
    workbook.close()

    if EXPORT_DATA_TO_EXTERNAL_HOST:
        xlsx_bytes = output.getvalue()
        return xlsx_bytes

    return None

def xlsx_laptop(req_xlsx_gen):

    try:
        EXPORT_DATA_TO_EXTERNAL_HOST = settings.EXPORT_DATA_TO_EXTERNAL_HOST
    except AttributeError:
        raise AttributeError(
            "Debe definir en el archivo "
            "settings la variable EXPORT_DATA_TO_EXTERNAL_HOST")

    try:
        TMP_FOLDER = settings.TMP_FOLDER
    except AttributeError:
        raise AttributeError(
            "Debe definir en el archivo "
            "settings la variable TMP_FOLDER")

    job_id = req_xlsx_gen["job_id"]

    if EXPORT_DATA_TO_EXTERNAL_HOST:
        output = BytesIO()
        workbook = Workbook(output)
    else:
        output_file_name = TMP_FOLDER + '/xlsx_' + job_id + '.xlsx'
        workbook = Workbook(output_file_name)

    filtros = req_xlsx_gen["data"][0]

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
    # 3) EXTRACCION DE DATOS DE DB
    # <<<<<<<<<<<<<
    job = Job.objects.get(_job_id=job_id)
    products = job.substitution_similar_results.all()

    ##################### codigo

    list_products_pre = list(products.values_list('pk', 'tiendas'))
    list_products = []
    for i in list_products_pre:
        if i[1] == []:
            continue
        elif i[1][0]['precio'].replace('\xa0',"").replace(" EUR", "").replace(" ", "") != '':
            list_products.append(i)
    # list_products = [i for i in list_products if i[1] != []]
    # list_products = [i for i in list_products if i[1][0]['precio'].replace('\xa0',"").replace(" EUR", "").replace(" ", "") != '']
    list_products = sorted(list_products, key=lambda k: float(k[1][0]['precio'].replace('\xa0',"").replace(" EUR", "").replace(" ", "")))

    # for _product in list_products:
    #     producto = products.get(pk=_product[0])
    # 
    #     if producto.store_id == "4":
    #        ... logica para pricerunner
    #     
    #     elif product.store_id == "3":
    #        ... logica para boulanger
    
    #####################

    # <<<<<<<<<<<<<
    # 4) MAXIMO NUMERO DE TIENDAS
    # <<<<<<<<<<<<<
    max_tiendas = 0

    for product in products:
        if isinstance(product.tiendas, list):
            num_tiendas = len(product.tiendas)
        elif isinstance(product.tiendas, dict):
            num_tiendas = 1
        else:
            raise TypeError("la variable 'tiendas' es un tipo incorrecto")

        if num_tiendas > max_tiendas:
            max_tiendas = num_tiendas

    # <<<<<<<<<<<<<
    # 5) DETERMINAMOS LA ESTRUCTURA DEL ARCHIVO EXCEL
    # <<<<<<<<<<<<<

    #Creamos la estructura del archivo excel:
    worksheet.write('A2', "Marque", format_header)
    worksheet.write('A3', "Modèle", format_header)
    worksheet.write('A4', "RAM", format_header)
    worksheet.write('A5', "CPU", format_header)
    worksheet.write('A6', "GPU", format_header)
    worksheet.write('A7', "Taille d'écran (pounces)", format_header)
    worksheet.write('A8', "Résolution", format_header)
    worksheet.write('A9', "Proprietes d'écran", format_header)
    worksheet.write('A10', "Type de stockage", format_header)
    worksheet.write('A11', 'Capacité HDD', format_header)
    worksheet.write('A12', "Capacité SSD", format_header)
    worksheet.write('A13', "Sortie video", format_header)
    worksheet.write('A14', "Lecteur/Graveur", format_header)
    worksheet.write('A15', "Système d'exploitation", format_header)

    for k in range(max_tiendas):
        worksheet.write(16+4*k,0, "Prix", format_header)
        worksheet.write(17+4*k,0, "Enseigne", format_header)
        worksheet.write(18+4*k,0, "URL", format_header)

    # <<<<<<<<<<<<<
    # 6) COLUMNA DE PRODUCTO A REEMPLAZAR
    # <<<<<<<<<<<<<

    worksheet.write('B1', "Modèle endommagé", format_header)
    worksheet.write('B2', filtros['Marque'].upper(), format)
    worksheet.write('B3', filtros['Modele'], format)
    worksheet.write('B4', filtros['Ram (Go)'], format)
    worksheet.write('B5', filtros['CPUSpec'], format)
    worksheet.write('B6', filtros['GPUSpec'], format)
    worksheet.write('B7', filtros['Taille (pounce)'], format)
    worksheet.write('B8', filtros['Resolution'], format)
    worksheet.write('B9', ", ".join(filtros['Proprietes']), format)
    worksheet.write('B10', filtros['Type de stockage'], format)
    worksheet.write('B11', filtros['Taille HDD (Go)'], format)
    worksheet.write('B12', filtros['Taille SSD (Go)'], format)
    worksheet.write('B13',", ".join(filtros['Sortie video']), format)
    worksheet.write('B14', filtros['Lecteur/Graveur'], format)
    worksheet.write('B15', filtros["Systeme dexploitation"], format)

    for k in range(max_tiendas):
        worksheet.write(16+4*k,1, "", format_NA)
        worksheet.write(17+4*k,1, "", format_NA)
        worksheet.write(18+4*k,1, "", format_NA)

    for _product in list_products:
        producto = products.get(pk=_product[0])
    
        # PRICERUNNER <<<<<<<<<<<<<<<<<<<<<<
        if producto.store_id == "4":
            if producto.tiendas==[]: continue

            worksheet.write(0, icol + 2, "".join(("Produit ", str(icol + 1))), format_header)
            try:
                worksheet.write(1, icol + 2, producto.ficha_tecnica['Marque'].upper(), format)
            except:
                worksheet.write(1, icol + 2, '', format_NA)
            try:
                worksheet.write(2, icol + 2, producto.nombre.split(producto.ficha_tecnica['Marque'])[1][1:], format)
            except:
                worksheet.write(2, icol + 2, '', format_NA)
            try:
                worksheet.write(3, icol + 2, producto.ficha_tecnica["RAM"], format)
            except:
                worksheet.write(3, icol + 2, '', format_NA)
            try:
                worksheet.write(4, icol + 2, producto.ficha_tecnica["Série de processeur"], format)
            except:
                worksheet.write(4, icol + 2, '', format_NA)
            try:
                worksheet.write(5, icol + 2, producto.ficha_tecnica["Modèle de carte graphique"], format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                worksheet.write(6, icol + 2, producto.ficha_tecnica["Taille de l'écran"], format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                worksheet.write(7, icol + 2, producto.ficha_tecnica['Résolution'], format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                propts = []
                if "Type d'écran" in producto.ficha_tecnica.keys(): propts.append(producto.ficha_tecnica["Type d'écran"])
                #if "Type d'écran" in producto.ficha_tecnica.keys(): props.append(producto.ficha_tecnica["Type d'écran"])
                # ESTO ES PARA CONCATENAR PROPIEDADES QUE VENGAN POR SEPARADO
                worksheet.write(8, icol + 2, ", ".join(propts), format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                worksheet.write(9, icol + 2, producto.ficha_tecnica[
                    "Disque dur HDD : disque dur classique (à plateaux)SSD : disque dur flash (sans mécanique, à base de mémoire flash). Les disques SSD sont plus petits en termes de taille et de capacité, et aussi plus chers."],
                                format)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                worksheet.write(10, icol + 2, producto.ficha_tecnica["Taille de HDD"], format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica["Taille de SSD Taille de SSD"], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)
            try:
                worksheet.write(12, icol + 2, producto.ficha_tecnica["Connections"], format)
            except:
                worksheet.write(12, icol + 2, '', format_NA)
            try:
                worksheet.write(13, icol + 2, producto.ficha_tecnica["Lecteur optique Indique de quel type de lecteur optique l'ordinateur est équipé : CD-Rom, DVD-Rom, Graveur de CD, Graveur de DVD, Combiné graveur de CD-lecteur de DVD, etc."], format)
            except:
                worksheet.write(13, icol + 2, '', format_NA)
            try:
                if 'Windows' in producto.ficha_tecnica["Système d'exploitation"]:
                    worksheet.write(14, icol + 2, producto.ficha_tecnica["Windows Version"], format)
                elif producto.ficha_tecnica["Système d'exploitation"] == 'macOS':
                    worksheet.write(14, icol + 2, "macOS", format)
            except:
                worksheet.write(14, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(16+4*k,icol+2, producto.tiendas[k]['precio'], format)
                        if (producto.tiendas[k]['nombre_tienda']) == '':
                            worksheet.write(17 + 4 * k, icol + 2, '', format_NA)
                        else:
                            worksheet.write(17+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(16+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(17+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)

            icol += 1

        # BOULANGER <<<<<<<<<<<<<<<<<<<<<<
        elif producto.store_id == "3":
            worksheet.write(0,icol+2, "".join(("Produit ",str(icol+1))), format_header)
            try:
                if 'PORSCHE DESIGN' in producto.nombre.upper():
                    worksheet.write(1, icol + 2, 'PORSCHE DESIGN', format)
                else:
                    worksheet.write(1,icol+2, producto.nombre.split(' ')[2].upper(), format)
            except:
                worksheet.write(1, icol + 2, '', format_NA)
            try:
                if 'PORSCHE DESIGN' in producto.nombre.upper():
                    worksheet.write(2, icol + 2, " ".join(producto.nombre.split(' ')[3:]), format)
                else:
                    worksheet.write(2, icol + 2, " ".join(producto.nombre.split(' ')[2:]), format)
            except:
                worksheet.write(2, icol + 2, '', format_NA)
            try:
                worksheet.write(3,icol+2,producto.ficha_tecnica["Capacité totale"],format)
            except:
                worksheet.write(3, icol + 2, '', format_NA)
            try:
                worksheet.write(4,icol+2,producto.ficha_tecnica["Référence et spécificités"].split(" : ")[0],format)
            except:
                worksheet.write(4, icol + 2, '', format_NA)
            try:
                if "Carte" in producto.ficha_tecnica:
                    worksheet.write(5,icol+2,producto.ficha_tecnica["Carte"],format)            
                elif "Contrôleur graphique" in producto.ficha_tecnica:
                    worksheet.write(5,icol+2,producto.ficha_tecnica["Contrôleur graphique"],format)
                else:
                    worksheet.write(5, icol + 2, '', format_NA)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                worksheet.write(6, icol + 2, producto.ficha_tecnica["Taille de l'écran"], format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                worksheet.write(7, icol + 2, producto.ficha_tecnica["Résolution de l'écran"], format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                if producto.ficha_tecnica['Ecran tactile'] == 'Oui':
                    worksheet.write(8, icol + 2, "Ecran tactile", format)
                else:
                    worksheet.write(8, icol + 2, "Ecran non tactile", format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                if 'Capacité du disque dur' in list(producto.ficha_tecnica.keys()) and 'Capacité du SSD' in list(producto.ficha_tecnica.keys()):
                    worksheet.write(9, icol + 2, 'Hybride', format)
                elif 'Capacité du disque dur' in list(producto.ficha_tecnica.keys()):
                    worksheet.write(9, icol + 2, 'HDD', format)
                elif 'Capacité du SSD' in list(producto.ficha_tecnica.keys()):
                    worksheet.write(9, icol + 2, 'SSD', format)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                worksheet.write(10, icol + 2, producto.ficha_tecnica["Capacité du disque dur"], format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica["Capacité du SSD"], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)
            try:
                connections_rueducommerce = []
                if 'Sortie HDMI' in list(producto.ficha_tecnica.keys()):
                    connections_rueducommerce.append('HDMI')
                if 'Sortie VGA' in list(producto.ficha_tecnica.keys()):
                    connections_rueducommerce.append('VGA')
                if 'Sortie Thunderbolt' in list(producto.ficha_tecnica.keys()):
                    connections_rueducommerce.append('Thunderbolt')
                worksheet.write(12, icol + 2, ", ".join(connections_rueducommerce), format)
            except:
                worksheet.write(12, icol + 2, '', format_NA)
            try:
                worksheet.write(13, icol + 2, producto.ficha_tecnica["Type"], format)
            except:
                worksheet.write(13, icol + 2, '', format_NA)
            try:
                worksheet.write(14, icol + 2, producto.ficha_tecnica["Système d'exploitation"], format)
            except:
                worksheet.write(14, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(16+4*k,icol+2, producto.tiendas[k]['precio'], format)
                        if (producto.tiendas[k]['nombre_tienda']) == '':
                            worksheet.write(17 + 4 * k, icol + 2, '', format_NA)
                        else:
                            worksheet.write(17+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(16+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(17+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)

            icol += 1

        # RUE DU COMMERCE <<<<<<<<<<<<<<<<<<<<<<
        elif producto.store_id == "5":
            worksheet.write(0,icol+2, "".join(("Produit ",str(icol+1))), format_header)
            try:
                worksheet.write(1,icol+2, producto.nombre.upper().split(' - ')[0], format)
            except:
                worksheet.write(1, icol + 2, '', format_NA)
            try:
                worksheet.write(2,icol+2, producto.nombre.split(' - ')[1], format)
            except:
                worksheet.write(2, icol + 2, '', format_NA)
            try:
                worksheet.write(3,icol+2,producto.ficha_tecnica["Mémoire vive installée (Go)"],format)
            except:
                worksheet.write(3, icol + 2, '', format_NA)
            try:
                worksheet.write(4,icol+2,producto.ficha_tecnica["Type de processeur"],format)
            except:
                worksheet.write(4, icol + 2, '', format_NA)
            try:
                worksheet.write(5,icol+2,producto.ficha_tecnica["Chipset graphique"],format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                worksheet.write(6, icol + 2, producto.ficha_tecnica["Taille maximale"], format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                worksheet.write(7, icol + 2, producto.ficha_tecnica['Résolution maximale'], format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                worksheet.write(8, icol + 2, producto.ficha_tecnica["Ecran tactile"], format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                if producto.ficha_tecnica.get("Support d'enregistrement",""):
                    worksheet.write(9, icol + 2, producto.ficha_tecnica["Support d'enregistrement"], format)
                elif producto.ficha_tecnica.get("Type de stockage",""):
                    worksheet.write(9, icol + 2, producto.ficha_tecnica["Type de stockage"], format)
                else:
                    worksheet.write(9, icol + 2, '', format_NA)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                worksheet.write(10, icol + 2, producto.ficha_tecnica["Capacité de stockages"], format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                if producto.ficha_tecnica.get("Capacité SSD (Go) ",""):
                    worksheet.write(11, icol + 2, producto.ficha_tecnica["Capacité SSD (Go) "], format)
                elif producto.ficha_tecnica.get("Capacité SSD",""):
                    worksheet.write(11, icol + 2, producto.ficha_tecnica["Capacité SSD"], format)
                elif producto.ficha_tecnica.get("Capacité SSD (Go)",""):
                    worksheet.write(11, icol + 2, producto.ficha_tecnica["Capacité SSD (Go)"], format)
                else:
                    worksheet.write(11, icol + 2, '', format_NA)
            except:
                worksheet.write(11, icol + 2, '', format_NA)
            try:
                detalles_rueducommerce = "".join(producto.detalles).upper()
                connections_rueducommerce = []
                if 'HDMI' in detalles_rueducommerce:
                    connections_rueducommerce.append('HDMI')
                if 'VGA' in detalles_rueducommerce:
                    connections_rueducommerce.append('VGA')
                if 'THUNDERBOLT' in detalles_rueducommerce:
                    connections_rueducommerce.append('Thunderbolt')
                worksheet.write(12, icol + 2, ", ".join(connections_rueducommerce), format)
            except:
                worksheet.write(12, icol + 2, '', format_NA)
            try:
                worksheet.write(13, icol + 2, producto.ficha_tecnica["Lecteur/Graveurs"], format)
            except:
                worksheet.write(13, icol + 2, '', format_NA)
            try:
                worksheet.write(14, icol + 2, producto.ficha_tecnica["Version de l'OS"], format)
            except:
                worksheet.write(14, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(16+4*k,icol+2, producto.tiendas[k]['precio'], format)
                        if (producto.tiendas[k]['nombre_tienda']) == '':
                            worksheet.write(17 + 4 * k, icol + 2, '', format_NA)
                        else:
                            worksheet.write(17+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(16+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(17+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)

            icol += 1


    # Ancho de columna (todos los productos)
    worksheet.set_column(1, icol + 2, 30)

    # FIN
    workbook.close()

    if EXPORT_DATA_TO_EXTERNAL_HOST:
        xlsx_bytes = output.getvalue()
        return xlsx_bytes

    return None


def xlsx_refrigerador(req_xlsx_gen):

    try:
        EXPORT_DATA_TO_EXTERNAL_HOST = settings.EXPORT_DATA_TO_EXTERNAL_HOST
    except AttributeError:
        raise AttributeError(
            "Debe definir en el archivo "
            "settings la variable EXPORT_DATA_TO_EXTERNAL_HOST")

    try:
        TMP_FOLDER = settings.TMP_FOLDER
    except AttributeError:
        raise AttributeError(
            "Debe definir en el archivo "
            "settings la variable TMP_FOLDER")

    job_id = req_xlsx_gen["job_id"]

    if EXPORT_DATA_TO_EXTERNAL_HOST:
        output = BytesIO()
        workbook = Workbook(output)
    else:
        output_file_name = TMP_FOLDER + '/xlsx_' + job_id + '.xlsx'
        workbook = Workbook(output_file_name)

    filtros = req_xlsx_gen["data"][0]

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
    # 3) EXTRACCION DE DATOS DE DB
    # <<<<<<<<<<<<<
    job = Job.objects.get(_job_id=job_id)
    products = job.substitution_similar_results.all()

    list_products_pre = list(products.values_list('pk', 'tiendas'))
    list_products = []
    for i in list_products_pre:
        if i[1] == []:
            continue
        elif i[1][0]['precio'].replace('\xa0',"").replace(" EUR", "").replace(" ", "") != '':
            list_products.append(i)
    # list_products = [i for i in list_products if i[1] != []]
    # list_products = [i for i in list_products if i[1][0]['precio'].replace('\xa0',"").replace(" EUR", "").replace(" ", "") != '']
    list_products = sorted(list_products, key=lambda k: float(k[1][0]['precio'].replace('\xa0',"").replace(" EUR", "").replace(" ", "")))


    # <<<<<<<<<<<<<
    # 4) MAXIMO NUMERO DE TIENDAS
    # <<<<<<<<<<<<<
    max_tiendas = 0

    for product in products:
        if isinstance(product.tiendas, list):
            num_tiendas = len(product.tiendas)
        elif isinstance(product.tiendas, dict):
            num_tiendas = 1
        else:
            raise TypeError("la variable 'tiendas' es un tipo incorrecto")

        if num_tiendas > max_tiendas:
            max_tiendas = num_tiendas

    # <<<<<<<<<<<<<
    # 5) DETERMINAMOS LA ESTRUCTURA DEL ARCHIVO EXCEL
    # <<<<<<<<<<<<<
    #Creamos la estructura del archivo excel:
    worksheet.write('A2', "Marque", format_header)
    worksheet.write('A3', "Modèle", format_header)
    worksheet.write('A4', "Type d'appareil", format_header)
    worksheet.write('A5', "Subtype", format_header)
    worksheet.write('A6', "Hauteur", format_header)
    worksheet.write('A7', "Largeur", format_header)
    worksheet.write('A8', "Profoundeur", format_header)
    worksheet.write('A9', "Volume utile", format_header)
    worksheet.write('A10', "Volume net", format_header)
    worksheet.write('A11', "Type de pose", format_header)
    worksheet.write('A12', "Energy", format_header)
    worksheet.write('A13', "Consommation (kWh/an)", format_header)
    worksheet.write('A14', "Système de froid", format_header)
    worksheet.write('A15', "Couleur", format_header)
    for k in range(max_tiendas):
        worksheet.write(16+4*k,0, "Prix", format_header)
        worksheet.write(17+4*k,0, "Enseigne", format_header)
        worksheet.write(18+4*k,0, "URL", format_header)

    # <<<<<<<<<<<<<
    # 6) COLUMNA DE PRODUCTO A REEMPLAZAR
    # <<<<<<<<<<<<<

    worksheet.write('B1', "Modèle endommagé", format_header)
    worksheet.write('B2', filtros['Marque'].upper(), format)
    worksheet.write('B3', filtros['Modele'], format)
    worksheet.write('B4', 'Réfrigérateur', format)
    worksheet.write('B5', filtros['Subtype'], format)
    worksheet.write('B6', filtros['Hateur'], format)
    worksheet.write('B7', filtros['Largeur'], format)
    worksheet.write('B8', filtros['Profoundeur'], format)
    worksheet.write('B9', filtros['Volume utile'], format)
    worksheet.write('B10', filtros['Volume net'], format)
    worksheet.write('B11', filtros['TypePose'], format)
    worksheet.write('B12', filtros['Energy'], format)
    worksheet.write('B13', filtros['Consommation'], format)
    worksheet.write('B14', filtros['Systeme de froid'], format)
    worksheet.write('B15', filtros['Couleur'], format)

    for k in range(max_tiendas):
        worksheet.write(16+4*k,1, "", format_NA)
        worksheet.write(17+4*k,1, "", format_NA)
        worksheet.write(18+4*k,1, "", format_NA)

    # <<<<<<<<<<<<<
    # 7) ESCRITURA
    # <<<<<<<<<<<<<

    for _product in list_products:
        producto = products.get(pk=_product[0])
    
        # PRICERUNNER <<<<<<<<<<<<<<<<<<<<<<
        if producto.store_id == "4":

            if producto.tiendas==[]: continue

            worksheet.write(0, icol + 2, "".join(("Produit ", str(icol + 1))), format_header)
            try:
                worksheet.write(1, icol + 2, producto.ficha_tecnica['Marque'].upper(), format)
            except:
                worksheet.write(1, icol + 2, '', format_NA)
            try:
                worksheet.write(2, icol + 2, "".join(producto.nombre.split(producto.ficha_tecnica['Marque'])), format)
            except:
                worksheet.write(2, icol + 2, '', format_NA)
            try:
                worksheet.write(3, icol + 2, 'Réfrigérateur', format)
            except:
                worksheet.write(3, icol + 2, '', format_NA)
            try:
                taille_pr = float("".join(producto.ficha_tecnica['Taille'].split(' cm')))
                if taille_pr <= 90:
                    worksheet.write(4, icol + 2, 'Réfrigérateur compact', format)
                else:
                    worksheet.write(4, icol + 2, 'Réfrigérateur standard', format)
            except:
                worksheet.write(4, icol + 2, '', format_NA)
            try:
                worksheet.write(5, icol + 2, producto.ficha_tecnica['Taille'], format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                worksheet.write(6, icol + 2, producto.ficha_tecnica['Largeur'], format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                worksheet.write(7, icol + 2, producto.ficha_tecnica['Profondeur'], format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                worksheet.write(8, icol + 2, producto.ficha_tecnica["Volume Indique la capacité interne du réfrigérateur en LITRES."], format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                taille_pr = float("".join(producto.ficha_tecnica['Taille'].split(' cm')))
                largeur_pr = float("".join(producto.ficha_tecnica['Largeur'].split(' cm')))
                prof_pr = float("".join(producto.ficha_tecnica['Profondeur'].split(' cm')))
                worksheet.write(9, icol + 2, '{0} L'.format(int((taille_pr*largeur_pr*prof_pr)/1000)), format)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                worksheet.write(10, icol + 2, producto.ficha_tecnica["Type"], format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica["Classe d'énergie A+++ indique la consommation la moins importante et G la plus importante"], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)
            try:
                worksheet.write(12, icol + 2, producto.ficha_tecnica["Consommation"], format)
            except:
                worksheet.write(12, icol + 2, '', format_NA)
            try:
                worksheet.write(13, icol + 2, producto.ficha_tecnica["Systeme Froid"], format)
            except:
                worksheet.write(13, icol + 2, '', format_NA)
            try:
                worksheet.write(14, icol + 2, producto.ficha_tecnica["Colour"], format)
            except:
                worksheet.write(14, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(16+4*k,icol+2, producto.tiendas[k]['precio'], format)
                        if (producto.tiendas[k]['nombre_tienda']) == '':
                            worksheet.write(17 + 4 * k, icol + 2, '', format_NA)
                        else:
                            worksheet.write(17+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(16+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(17+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)

            icol += 1

        # DARTY <<<<<<<<<<<<<<<<<<<<<<
        if producto.store_id == "1":
            worksheet.write(0,icol+2, "".join(("Produit ",str(icol+1))), format_header)
            try:
                worksheet.write(1,icol+2, producto.nombre.split(" ")[0].upper(), format)
            except:
                worksheet.write(1,icol+2,'',format_NA)
            try:
                worksheet.write(2,icol+2, " ".join(producto.nombre.split(" ")[1:]), format)
            except:
                worksheet.write(2,icol+2,'',format_NA)
            try:
                worksheet.write(3,icol+2,'Réfrigérateur',format)
            except:
                worksheet.write(3,icol+2,'',format_NA)
            try:
                taille_dar = float("".join(producto.ficha_tecnica['Hauteur (cm)'].split(' cm')).replace(',',"."))
                if taille_dar > 300:
                    taille_dar = taille_dar/10.0
                if taille_dar <= 90:
                    worksheet.write(4, icol + 2, 'Réfrigérateur compact', format)
                else:
                    worksheet.write(4, icol + 2, 'Réfrigérateur standard', format)
            except:
                worksheet.write(4,icol+2,'',format_NA)
            try:
                taille_dar = float("".join(producto.ficha_tecnica['Hauteur (cm)'].split(' cm')).replace(',',"."))
                if taille_dar > 300:
                    taille_dar = taille_dar/10.0
                worksheet.write(5, icol + 2, "{0} cm".format(taille_dar), format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                largeur_dar = float("".join(producto.ficha_tecnica['Largeur (cm)'].split(' cm')).replace(',',"."))
                if largeur_dar > 250:
                    largeur_dar = largeur_dar/10.0
                worksheet.write(6, icol + 2, "{0} cm".format(largeur_dar), format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                prof_dar = float("".join(producto.ficha_tecnica['Profondeur (cm)'].split(' cm')).replace(',',"."))
                if prof_dar > 250:
            	    prof_dar = prof_dar/10.0
                worksheet.write(7, icol + 2, "{0} cm".format(prof_dar), format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                worksheet.write(8, icol + 2, producto.ficha_tecnica["Volume utile du réfrigérateur"], format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                worksheet.write(9, icol + 2, '{0} L'.format(int((taille_dar*largeur_dar*prof_dar)/1000)), format)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                worksheet.write(10, icol + 2, producto.ficha_tecnica["Type"], format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica["Classe énergétique"], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)
            try:
                worksheet.write(12, icol + 2, producto.ficha_tecnica["Consommation d'énergie (Norme EN 153)"], format)
            except:
                worksheet.write(12, icol + 2, '', format_NA)
            try:
                worksheet.write(13, icol + 2, producto.ficha_tecnica["Type de réfrigération"], format)
            except:
                worksheet.write(13, icol + 2, '', format_NA)
            try:
                worksheet.write(14, icol + 2, producto.ficha_tecnica["Finition"], format)
            except:
                worksheet.write(14, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(16+4*k,icol+2, producto.tiendas[k]['precio'], format)
                        if (producto.tiendas[k]['nombre_tienda']) == '':
                            worksheet.write(17 + 4 * k, icol + 2, '', format_NA)
                        else:
                            worksheet.write(17+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(16+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(17+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas['url_tienda'], format_url)

                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)

            icol += 1

        # BOULANGER <<<<<<<<<<<<<<<<<<<<<<
        if producto.store_id == "3":
            worksheet.write(0,icol+2, "".join(("Produit ",str(icol+1))), format_header)
            try:
                if 'Encastrable' in producto.ficha_tecnica["Type d'installation"]:
                    separador = " ".join([producto.ficha_tecnica["Type d'appareil"],'encastrable '])
                else:
                    separador = producto.ficha_tecnica["Type d'appareil"] + " "
                    marque_boulanger = "".join(producto.nombre.split(separador)).split(" ")[0]
                worksheet.write(1,icol+2, marque_boulanger.upper(), format)
            except:
                worksheet.write(1,icol+2,'',format_NA)
            try:
                worksheet.write(2,icol+2, "".join(producto.nombre.split(marque_boulanger)[1:]), format)
            except:
                worksheet.write(2, icol + 2, '', format_NA)
            try:
                worksheet.write(3, icol + 2, 'Réfrigérateur', format)
            except:
                worksheet.write(3, icol + 2, '', format_NA)
            try:
                taille_bou = float(producto.ficha_tecnica["L x H x P :"].
                                split('x')[1])
                if taille_bou <= 90:
                    worksheet.write(4,icol+2,'Réfrigérateur compact',format)
                else:
                    worksheet.write(4, icol + 2, 'Réfrigérateur standard', format)
            except:
                worksheet.write(4, icol + 2,'', format_NA)
            try:
                taille_bou = float(producto.ficha_tecnica["L x H x P :"].
                                   split('x')[1])
                if taille_bou >=250: taille_bou = taille_bou/10
                worksheet.write(5, icol + 2, "{0} cm".format(taille_bou), format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                largeur_bou = float(producto.ficha_tecnica["L x H x P :"].
                                   split('x')[0])
                if largeur_bou >=250: largeur_bou = largeur_bou/10
                worksheet.write(6, icol + 2, "{0} cm".format(largeur_bou), format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                prof_bou = float(producto.ficha_tecnica["L x H x P :"].
                                   split('x')[2].replace("cm",""))
                if prof_bou >=250: prof_bou = prof_bou/10
                worksheet.write(7, icol + 2, "{0}".format(prof_bou), format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                worksheet.write(8, icol + 2, producto.ficha_tecnica["Volume (l)"] + " L", format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                worksheet.write(9, icol + 2, '{0} L'.format(int((taille_bou*largeur_bou*prof_bou)/1000)), format)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                if 'Encastrable' in producto.ficha_tecnica["Type d'installation"]:
                    worksheet.write(10, icol + 2, "Integrable", format)
                else:
                    worksheet.write(10, icol + 2, "Pose libre", format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica["Classe énergétique"].split(" ")[0], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)
            try:
                worksheet.write(12, icol + 2, producto.ficha_tecnica["Consommation d'énergie annuelle"], format)
            except:
                worksheet.write(12, icol + 2, '', format_NA)
            try:
                worksheet.write(13, icol + 2, producto.ficha_tecnica["Froid du réfrigérateur"], format)
            except:
                worksheet.write(13, icol + 2, '', format_NA)
            try:
                worksheet.write(14, icol + 2, producto.ficha_tecnica["Couleur produit"], format)
            except:
                worksheet.write(14, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(16+4*k,icol+2, producto.tiendas[k]['precio'], format)
                        if (producto.tiendas[k]['nombre_tienda']) == '':
                            worksheet.write(17 + 4 * k, icol + 2, '', format_NA)
                        else:
                            worksheet.write(17+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(16+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(17+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)

            icol += 1

        # KELKOO <<<<<<<<<<<<<<<<<<<<<<
        if producto.store_id == "2":

            if producto.tiendas==[]: continue

            worksheet.write(0,icol+2, "".join(("Produit ",str(icol+1))), format_header)
            try:
                marque_kelkoo = producto.ficha_tecnica['Marque']
                find_interr = marque_kelkoo.find('?')
                marque_filtros = filtros['Marque'][:find_interr] + filtros['Marque'][find_interr+1:]
                if marque_filtros == marque_kelkoo.replace('?',''):
                    worksheet.write(1,icol+2, filtros['Marque'].upper(), format)
                else:
                    worksheet.write(1, icol + 2, producto.ficha_tecnica['Marque'].upper(), format)
            except:
                worksheet.write(1, icol + 2, "", format)
            try:
                worksheet.write(2,icol+2, producto.nombre.split(marque_kelkoo)[1][1:], format)
            except:
                worksheet.write(2, icol + 2, "", format)
            try:
                worksheet.write(3, icol + 2, producto.ficha_tecnica['Catégorie'], format)
            except:
                worksheet.write(3, icol + 2, "", format)
            try:
                taille_kel = float("".join(producto.ficha_tecnica['Hauteur'].split(' cm')))
                if taille_kel <= 90:
                    worksheet.write(4, icol + 2, 'Réfrigérateur compact', format)
                else:
                    worksheet.write(4, icol + 2, 'Réfrigérateur standard', format)
            except:
                worksheet.write(4, icol + 2, '', format_NA)
            try:
                worksheet.write(5, icol + 2, producto.ficha_tecnica["Hauteur"], format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                worksheet.write(6, icol + 2, producto.ficha_tecnica["Largeur"], format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                worksheet.write(7, icol + 2, producto.ficha_tecnica["Profondeur"], format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                worksheet.write(8, icol + 2, producto.ficha_tecnica["Volume (l)"] + " L", format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                worksheet.write(9, icol + 2, producto.ficha_tecnica["Volume net du réfrigérateur"].replace("litres"," L"), format)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                worksheet.write(10, icol + 2, producto.ficha_tecnica["Type de pose"], format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica["Classe énergétique"].split(" ")[0], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)
            try:
                worksheet.write(12, icol + 2, producto.ficha_tecnica["Consommation énergétique annuelle"], format)
            except:
                worksheet.write(12, icol + 2, '', format_NA)
            try:
                if producto.ficha_tecnica["Froid ventilé"] == "Avec froid ventilé":
                    worksheet.write(13, icol + 2, "Froid ventilé", format)
            except:
                worksheet.write(13, icol + 2, '', format_NA)
            try:
                worksheet.write(14, icol + 2, producto.ficha_tecnica["Couleur"], format)
            except:
                worksheet.write(14, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(16+4*k,icol+2, producto.tiendas[k]['precio'], format)
                        if (producto.tiendas[k]['nombre_tienda']) == '':
                            worksheet.write(17 + 4 * k, icol + 2, '', format_NA)
                        else:
                            worksheet.write(17+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(16+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(17+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)

            icol += 1

    # Ancho de columna (todos los productos)
    worksheet.set_column(1, icol + 2, 30)

    # FIN
    workbook.close()

    if EXPORT_DATA_TO_EXTERNAL_HOST:
        xlsx_bytes = output.getvalue()
        return xlsx_bytes

    return None

def xlsx_refrigerador_combi(req_xlsx_gen):

    try:
        EXPORT_DATA_TO_EXTERNAL_HOST = settings.EXPORT_DATA_TO_EXTERNAL_HOST
    except AttributeError:
        raise AttributeError(
            "Debe definir en el archivo "
            "settings la variable EXPORT_DATA_TO_EXTERNAL_HOST")

    try:
        TMP_FOLDER = settings.TMP_FOLDER
    except AttributeError:
        raise AttributeError(
            "Debe definir en el archivo "
            "settings la variable TMP_FOLDER")

    job_id = req_xlsx_gen["job_id"]

    if EXPORT_DATA_TO_EXTERNAL_HOST:
        output = BytesIO()
        workbook = Workbook(output)
    else:
        output_file_name = TMP_FOLDER + '/xlsx_' + job_id + '.xlsx'
        workbook = Workbook(output_file_name)

    filtros = req_xlsx_gen["data"][0]

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
    # 3) EXTRACCION DE DATOS DE DB
    # <<<<<<<<<<<<<
    job = Job.objects.get(_job_id=job_id)
    products = job.substitution_similar_results.all()

    list_products_pre = list(products.values_list('pk', 'tiendas'))
    list_products = []
    for i in list_products_pre:
        if i[1] == []:
            continue
        elif i[1][0]['precio'].replace('\xa0',"").replace(" EUR", "").replace(" ", "") != '':
            list_products.append(i)
    # list_products = [i for i in list_products if i[1] != []]
    # list_products = [i for i in list_products if i[1][0]['precio'].replace('\xa0',"").replace(" EUR", "").replace(" ", "") != '']
    list_products = sorted(list_products, key=lambda k: float(k[1][0]['precio'].replace('\xa0',"").replace(" EUR", "").replace(" ", "")))


    # <<<<<<<<<<<<<
    # 4) MAXIMO NUMERO DE TIENDAS
    # <<<<<<<<<<<<<
    max_tiendas = 0

    for product in products:
        if isinstance(product.tiendas, list):
            num_tiendas = len(product.tiendas)
        elif isinstance(product.tiendas, dict):
            num_tiendas = 1
        else:
            raise TypeError("la variable 'tiendas' es un tipo incorrecto")

        if num_tiendas > max_tiendas:
            max_tiendas = num_tiendas

    # <<<<<<<<<<<<<
    # 5) DETERMINAMOS LA ESTRUCTURA DEL ARCHIVO EXCEL
    # <<<<<<<<<<<<<
    #Creamos la estructura del archivo excel:
    worksheet.write('A2', "Marque", format_header)
    worksheet.write('A3', "Modèle", format_header)
    worksheet.write('A4', "Type d'appareil", format_header)
    worksheet.write('A5', "Subtype", format_header)
    worksheet.write('A6', "Hauteur", format_header)
    worksheet.write('A7', "Largeur", format_header)
    worksheet.write('A8', "Profoundeur", format_header)
    worksheet.write('A9', "Volume utile frigo", format_header)
    worksheet.write('A10', "Volume net frigo", format_header)
    worksheet.write('A11', "Volume utile congélateur", format_header)
    worksheet.write('A12', "Volume net congélateur", format_header)
    worksheet.write('A13', "Volume total utile", format_header)
    worksheet.write('A14', "Volume total net", format_header)
    worksheet.write('A15', "Type de pose", format_header)
    worksheet.write('A16', "Energy", format_header)
    worksheet.write('A17', "Couleur", format_header)
    worksheet.write('A18', "Type de réfrigération", format_header)
    worksheet.write('A19', "Type de congélation", format_header)
    worksheet.write('A20', "Technologie", format_header)
    worksheet.write('A21', "Display", format_header)
    worksheet.write('A22', "Dispenseur", format_header)
    worksheet.write('A23', "Consommation (kWh/an)", format_header)

    for k in range(max_tiendas):
        worksheet.write(24+4*k,0, "Prix", format_header)
        worksheet.write(25+4*k,0, "Enseigne", format_header)
        worksheet.write(26+4*k,0, "URL", format_header)

    # <<<<<<<<<<<<<
    # 6) COLUMNA DE PRODUCTO A REEMPLAZAR
    # <<<<<<<<<<<<<

    worksheet.write('B1', "Modèle endommagé", format_header)
    worksheet.write('B2', filtros['Marque'].upper(), format)
    worksheet.write('B3', filtros['Modele'], format)
    worksheet.write('B4', 'Réfrigérateur combiné', format)
    worksheet.write('B5', filtros['Subtype'], format)
    worksheet.write('B6', filtros['Hateur'], format)
    worksheet.write('B7', filtros['Largeur'], format)
    worksheet.write('B8', filtros['Profoundeur'], format)
    worksheet.write('B9', filtros["Volume utile frigo"], format)
    worksheet.write('B10', filtros["Volume net frigo"], format)
    worksheet.write('B11', filtros["Volume utile congelateur"], format)
    worksheet.write('B12', filtros["Volume net congelateur"], format)
    worksheet.write('B13', filtros["Volume utile"], format)
    worksheet.write('B14', filtros["Volume net"], format)
    worksheet.write('B15', filtros["TypePose"], format)
    worksheet.write('B16', filtros["Energy"], format)
    worksheet.write('B17', filtros["Couleur"], format)
    worksheet.write('B18', filtros["Type refrigeration"], format)
    worksheet.write('B19', filtros["Type congelation"], format)
    worksheet.write('B20', filtros["Technologie"], format)
    worksheet.write('B21', filtros["Display"], format)
    worksheet.write('B22', filtros["Dispenseur"], format)
    worksheet.write('B23', filtros["Consommation"], format)

    for k in range(max_tiendas):
        worksheet.write(24+4*k,1, "", format_NA)
        worksheet.write(25+4*k,1, "", format_NA)
        worksheet.write(26+4*k,1, "", format_NA)

    # <<<<<<<<<<<<<
    # 7) ESCRITURA
    # <<<<<<<<<<<<<

    for _product in list_products:
        producto = products.get(pk=_product[0])
    
        # PRICERUNNER <<<<<<<<<<<<<<<<<<<<<<
        if producto.store_id == "4":

            if producto.tiendas==[]: continue

            worksheet.write(0, icol + 2, "".join(("Produit ", str(icol + 1))), format_header)
            try:
                worksheet.write(1, icol + 2, producto.ficha_tecnica['Marque'].upper(), format)
            except:
                worksheet.write(1, icol + 2, '', format_NA)
            try:
                worksheet.write(2, icol + 2, "".join(producto.nombre.split(producto.ficha_tecnica['Marque'])), format)
            except:
                worksheet.write(2, icol + 2, '', format_NA)
            try:
                worksheet.write(3, icol + 2, 'Réfrigérateur combiné', format)
            except:
                worksheet.write(3, icol + 2, '', format_NA)
            try:
                worksheet.write(4, icol + 2, producto.ficha_tecnica['Composition'], format)
            except:
                worksheet.write(4, icol + 2, '', format_NA)
            try:
                taille_pr = float("".join(producto.ficha_tecnica['Taille'].split(' cm')))
                worksheet.write(5, icol + 2, producto.ficha_tecnica['Taille'], format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                largeur_pr = float("".join(producto.ficha_tecnica['Largeur'].split(' cm')))
                worksheet.write(6, icol + 2, producto.ficha_tecnica['Largeur'], format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                prof_pr = float("".join(producto.ficha_tecnica['Profondeur'].split(' cm')))
                worksheet.write(7, icol + 2, producto.ficha_tecnica['Profondeur'], format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                vol_utile_ref_pr = float(producto.ficha_tecnica["Volume du réfrigérateur Le volume du réfrigérateur correspond à l'espace de rangement disponible et est exprimé en litres."].replace('L',''))
                vol_utile_cong_pr = float(producto.ficha_tecnica["Volume du congélateur Le volume du congélateur est indiqué en litres"].replace('L',''))
                worksheet.write(8, icol + 2, str(vol_utile_ref_pr) + " L", format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                worksheet.write(9, icol + 2, producto.ficha_tecnica['Volume net frigo'], format)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                worksheet.write(10, icol + 2, str(vol_utile_cong_pr) + " L", format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica['Volume net cong'], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)
            try:
                worksheet.write(12, icol + 2, str(vol_utile_ref_pr+vol_utile_cong_pr) + " L", format)
            except:
                worksheet.write(12, icol + 2, '', format_NA)
            try:
                worksheet.write(13, icol + 2, '{0} L'.format(int((taille_pr*largeur_pr*prof_pr)/1000)), format)
            except:
                worksheet.write(13, icol + 2, '', format_NA)
            try:
                worksheet.write(14, icol + 2, producto.ficha_tecnica["Type de pose Les encastrables sont souvent légèrement moins volumineux mais souvent disponibles dans moins de coloris que les appareils en pose libre."], format)
            except:
                worksheet.write(14, icol + 2, '', format_NA)
            try:
                worksheet.write(15, icol + 2, producto.ficha_tecnica["Catégorie d'énergie Les catégories d'énergie sont évaluées sur une échelle de A+++ à D, où A+++ correspond à la plus basse consommation d'énergie et D à la plus haute."].split(" ")[0], format)
            except:
                worksheet.write(15, icol + 2, '', format_NA)
            try:
                worksheet.write(16, icol + 2, producto.ficha_tecnica["Couleur"], format)
            except:
                worksheet.write(16, icol + 2, '', format_NA)
            try:
                worksheet.write(17, icol + 2, producto.ficha_tecnica["Froid du réfrigérateur"], format)
            except:
                worksheet.write(17, icol + 2, '', format_NA)
            try:
                worksheet.write(18, icol + 2, producto.ficha_tecnica["Froid du congélateur"], format)
            except:
                worksheet.write(18, icol + 2, '', format_NA)
            try:
                if "Frost Free" in producto.ficha_tecnica['Caractéristiques']:
                    worksheet.write(19, icol + 2, "NoFrost", format)
                else:
                    worksheet.write(19, icol + 2, '', format_NA)
            except:
                worksheet.write(19, icol + 2, '', format_NA)
            try:
                worksheet.write(20, icol + 2, producto.ficha_tecnica["Display"], format)
            except:
                worksheet.write(20, icol + 2, '', format_NA)
            try:
                if "Distribu" in producto.ficha_tecnica['Caractéristiques']:
                    worksheet.write(21, icol + 2, "Oui", format)
                else:
                    worksheet.write(21, icol + 2, '', format_NA)
            except:
                worksheet.write(21, icol + 2, '', format_NA)
            try:
                worksheet.write(22, icol + 2, producto.ficha_tecnica["Energy Consumption (kWh/year)"], format)
            except:
                worksheet.write(22, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(24+4*k,icol+2, producto.tiendas[k]['precio'].replace("\xa0",""), format)
                        if (producto.tiendas[k]['nombre_tienda']) == '':
                            worksheet.write(25 + 4 * k, icol + 2, '', format_NA)
                        else:
                            worksheet.write(25+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(26+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(24+4*k,icol+2,"", format_NA)
                        worksheet.write(25+4*k,icol+2, "", format_NA)
                        worksheet.write(26+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(24+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(25+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(26+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                    else:
                        worksheet.write(24+4*k,icol+2,"", format_NA)
                        worksheet.write(25+4*k,icol+2, "", format_NA)
                        worksheet.write(26+4*k,icol+2, "", format_NA)


            icol += 1

        # DARTY <<<<<<<<<<<<<<<<<<<<<<
        elif producto.store_id == "1":
            worksheet.write(0,icol+2, "".join(("Produit ",str(icol+1))), format_header)
            try:
                worksheet.write(1,icol+2, producto.nombre.split(" ")[0].upper(), format)
            except:
                worksheet.write(1,icol+2,'',format_NA)
            try:
                worksheet.write(2,icol+2, " ".join(producto.nombre.split(filtros['Marque'])), format)
            except:
                worksheet.write(2,icol+2,'',format_NA)
            try:
                worksheet.write(3,icol+2,'Réfrigérateur combiné',format)
            except:
                worksheet.write(3,icol+2,'',format_NA)
            try:
                if "americain" in producto.tiendas[0]["url_tienda"]:
                    worksheet.write(4, icol + 2, 'Réfrigérateur américain', format)
                elif "congelateur_bas" in producto.tiendas[0]["url_tienda"]:
                    worksheet.write(4, icol + 2, 'Réfrigérateur congélateur en bas', format)
                elif "congelateur_haut" in producto.tiendas[0]["url_tienda"]:
                    worksheet.write(4, icol + 2, 'Réfrigérateur congélateur en haut', format)
            except:
                worksheet.write(4,icol+2,'',format_NA)
            try:
                taille_dar = float("".join(producto.ficha_tecnica['Hauteur (cm)'].split(' cm')).replace(',',"."))
                if taille_dar > 300:
                    taille_dar = taille_dar/10.0
                worksheet.write(5, icol + 2, "{0} cm".format(taille_dar), format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                largeur_dar = float("".join(producto.ficha_tecnica['Largeur (cm)'].split(' cm')).replace(',',"."))
                if largeur_dar > 250:
                    largeur_dar = largeur_dar/10.0
                worksheet.write(6, icol + 2, "{0} cm".format(largeur_dar), format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                prof_dar = float("".join(producto.ficha_tecnica['Profondeur (cm)'].split(' cm')).replace(',',"."))
                if prof_dar > 250:
                    prof_dar = prof_dar/10.0
                worksheet.write(7, icol + 2, "{0} cm".format(prof_dar), format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                vol_utile_ref_dar = float(producto.ficha_tecnica["Volume utile du réfrigérateur"].replace('l',''))
                vol_utile_cong_dar = float(producto.ficha_tecnica["Volume utile du congélateur"].replace('l',''))
                worksheet.write(8, icol + 2, str(vol_utile_ref_dar) + " L", format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                worksheet.write(9, icol + 2, producto.ficha_tecnica['Volume net frigo'], format)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                worksheet.write(10, icol + 2, str(vol_utile_cong_dar) + " L", format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica['Volume net cong'], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)
            try:
                worksheet.write(12, icol + 2, producto.ficha_tecnica['Volume total net'].replace("l","L"), format)
            except:
                worksheet.write(12, icol + 2, '', format_NA)
            try:
                worksheet.write(13, icol + 2, '{0} L'.format(int((taille_dar*largeur_dar*prof_dar)/1000)), format)
            except:
                worksheet.write(13, icol + 2, '', format_NA)
            try:
                if 'encastrable' in producto.tiendas[0]["url_tienda"]:
                    worksheet.write(14, icol + 2, "Encastrable", format)
                else:
                    worksheet.write(14, icol + 2, "Pose libre", format)
            except:
                worksheet.write(14, icol + 2, '', format_NA)
            try:
                worksheet.write(15, icol + 2, producto.ficha_tecnica["Classe énergétique"], format)
            except:
                worksheet.write(15, icol + 2, '', format_NA)
            try:
                worksheet.write(16, icol + 2, producto.ficha_tecnica["Finition"], format)
            except:
                worksheet.write(16, icol + 2, '', format_NA)
            try:
                worksheet.write(17, icol + 2, producto.ficha_tecnica["Type de réfrigération"], format)
            except:
                worksheet.write(17, icol + 2, '', format_NA)
            try:
                worksheet.write(18, icol + 2, producto.ficha_tecnica["Type de congélation"], format)
            except:
                worksheet.write(18, icol + 2, '', format_NA)
            try:
                if "Frost Free" in producto.ficha_tecnica['Caractéristiques, congélation']:
                    worksheet.write(19, icol + 2, "NoFrost", format)
                else:
                    worksheet.write(19, icol + 2, '', format_NA)
            except:
                worksheet.write(19, icol + 2, '', format_NA)
            try:
                worksheet.write(20, icol + 2, producto.ficha_tecnica["Display"], format)
            except:
                worksheet.write(20, icol + 2, '', format_NA)
            try:
                if producto.ficha_tecnica['Distributeur'] != "":
                    worksheet.write(21, icol + 2, "Oui", format)
                else:
                    worksheet.write(21, icol + 2, '', format_NA)
            except:
                worksheet.write(21, icol + 2, '', format_NA)
            try:
                worksheet.write(22, icol + 2, producto.ficha_tecnica["Consommation d'énergie (Norme EN 153)"], format)
            except:
                worksheet.write(22, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(24+4*k,icol+2, producto.tiendas[k]['precio'], format)
                        if (producto.tiendas[k]['nombre_tienda']) == '':
                            worksheet.write(25 + 4 * k, icol + 2, '', format_NA)
                        else:
                            worksheet.write(25+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(26+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(24+4*k,icol+2,"", format_NA)
                        worksheet.write(25+4*k,icol+2, "", format_NA)
                        worksheet.write(26+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(24+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(25+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(26+4*k,icol+2, producto.tiendas['url_tienda'], format_url)

                    else:
                        worksheet.write(24+4*k,icol+2,"", format_NA)
                        worksheet.write(25+4*k,icol+2, "", format_NA)
                        worksheet.write(26+4*k,icol+2, "", format_NA)

            icol += 1


        # BOULANGER <<<<<<<<<<<<<<<<<<<<<<
        elif producto.store_id == "3":
            worksheet.write(0,icol+2, "".join(("Produit ",str(icol+1))), format_header)
            try:
                if 'Encastrable' in producto.ficha_tecnica["Type d'installation"]:
                    separador = " ".join([producto.ficha_tecnica["Type d'appareil"],'encastrable '])
                else:
                    separador = producto.ficha_tecnica["Type d'appareil"] + " "
                    marque_boulanger = "".join(producto.nombre.split(separador)).split(" ")[0]
                worksheet.write(1,icol+2, marque_boulanger.upper(), format)
            except:
                worksheet.write(1,icol+2,'',format_NA)
            try:
                worksheet.write(2,icol+2, "".join(producto.nombre.split(marque_boulanger)[1:]), format)
            except:
                worksheet.write(2, icol + 2, '', format_NA)
            try:
                worksheet.write(3, icol + 2, 'Réfrigérateur combiné', format)
            except:
                worksheet.write(3, icol + 2, '', format_NA)
            try:
                worksheet.write(4,icol+2,producto.ficha_tecnica["Conception de l'appareil"],format)
            except:
                worksheet.write(4, icol + 2,'', format_NA)
            try:
                taille_bou = float(producto.ficha_tecnica["L x H x P :"].
                                   split('x')[1])
                if taille_bou >=250: taille_bou = taille_bou/10
                worksheet.write(5, icol + 2, "{0} cm".format(taille_bou), format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                largeur_bou = float(producto.ficha_tecnica["L x H x P :"].
                                   split('x')[0])
                if largeur_bou >=250: largeur_bou = largeur_bou/10
                worksheet.write(6, icol + 2, "{0} cm".format(largeur_bou), format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                prof_bou = float(producto.ficha_tecnica["L x H x P :"].
                                   split('x')[2].replace("cm",""))
                if prof_bou >=250: prof_bou = prof_bou/10
                worksheet.write(7, icol + 2, "{0}".format(prof_bou), format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                vol_utile_cong_bou = float(producto.ficha_tecnica['Volume utile'].replace('l',''))
                vol_utile_tot_bou = float(producto.ficha_tecnica['Volume utile total'].replace('l',''))
                worksheet.write(8, icol + 2, str(vol_utile_tot_bou - vol_utile_cong_bou) + " L", format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                worksheet.write(9, icol + 2, producto.ficha_tecnica['Volume net frigo'], format)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                worksheet.write(10, icol + 2, str(vol_utile_cong_bou) + " L", format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica['Volume net cong'], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)
            try:
                worksheet.write(12, icol + 2, str(vol_utile_tot_bou) + " L", format)
            except:
                worksheet.write(12, icol + 2, '', format_NA)
            try:
                worksheet.write(13, icol + 2, '{0} L'.format(int((taille_bou*largeur_bou*prof_bou)/1000)), format)
            except:
                worksheet.write(13, icol + 2, '', format_NA)
            try:
                if 'libre' in producto.ficha_tecnica["Type d'installation"]:
                    worksheet.write(14, icol + 2, "Pose libre", format)
                else:
                    worksheet.write(14, icol + 2, "Integrable", format)
            except:
                worksheet.write(14, icol + 2, '', format_NA)
            try:
                worksheet.write(15, icol + 2, producto.ficha_tecnica["Classe énergétique"].split(" ")[0], format)
            except:
                worksheet.write(15, icol + 2, '', format_NA)
            try:
                worksheet.write(16, icol + 2, producto.ficha_tecnica["Couleur produit"], format)
            except:
                worksheet.write(16, icol + 2, '', format_NA)
            try:
                worksheet.write(17, icol + 2, producto.ficha_tecnica["Froid du réfrigérateur"], format)
            except:
                worksheet.write(17, icol + 2, '', format_NA)
            try:
                worksheet.write(18, icol + 2, producto.ficha_tecnica["Froid du congélateur"], format)
            except:
                worksheet.write(18, icol + 2, '', format_NA)
            try:
                if "Froid NoFrost" in producto.ficha_tecnica['Froid du congélateur']:
                    worksheet.write(19, icol + 2, "NoFrost", format)
                else:
                    worksheet.write(19, icol + 2, '', format_NA)
            except:
                worksheet.write(19, icol + 2, '', format_NA)
            try:
                worksheet.write(20, icol + 2, producto.ficha_tecnica["Technologie"], format)
            except:
                worksheet.write(20, icol + 2, '', format_NA)
            try:
                if producto.ficha_tecnica["Distributeur"] != "":
                    worksheet.write(21, icol + 2, "Oui", format)
                else:
                    worksheet.write(21, icol + 2, '', format_NA)
            except:
                worksheet.write(21, icol + 2, '', format_NA)
            try:
                worksheet.write(22, icol + 2, producto.ficha_tecnica["Consommation d'énergie annuelle"], format)
            except:
                worksheet.write(22, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(24+4*k,icol+2, producto.tiendas[k]['precio'].replace("\xa0",""), format)
                        if (producto.tiendas[k]['nombre_tienda']) == '':
                            worksheet.write(25 + 4 * k, icol + 2, '', format_NA)
                        else:
                            worksheet.write(25+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(26+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(24+4*k,icol+2,"", format_NA)
                        worksheet.write(25+4*k,icol+2, "", format_NA)
                        worksheet.write(26+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(24+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(25+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(26+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                    else:
                        worksheet.write(24+4*k,icol+2,"", format_NA)
                        worksheet.write(25+4*k,icol+2, "", format_NA)
                        worksheet.write(26+4*k,icol+2, "", format_NA)

            icol += 1

        # KELKOO <<<<<<<<<<<<<<<<<<<<<<
        elif producto.store_id == "2":

            if producto.tiendas==[]: continue

            worksheet.write(0,icol+2, "".join(("Produit ",str(icol+1))), format_header)
            try:
                marque_kelkoo = producto.ficha_tecnica['Marque']
                find_interr = marque_kelkoo.find('?')
                marque_filtros = filtros['Marque'][:find_interr] + filtros['Marque'][find_interr+1:]
                if marque_filtros == marque_kelkoo.replace('?',''):
                    worksheet.write(1,icol+2, filtros['Marque'].upper(), format)
                else:
                    worksheet.write(1, icol + 2, producto.ficha_tecnica['Marque'].upper(), format)
            except:
                worksheet.write(1, icol + 2, "", format)
            try:
                worksheet.write(2,icol+2, producto.nombre.split(marque_kelkoo)[1][1:], format)
            except:
                worksheet.write(2, icol + 2, "", format)
            try:
                worksheet.write(3, icol + 2, "Réfrigérateur combiné", format)
            except:
                worksheet.write(3, icol + 2, "", format)
            try:
                worksheet.write(4, icol + 2, producto.ficha_tecnica['Type de réfrigérateur/congélateur'], format)
            except:
                worksheet.write(4, icol + 2, '', format_NA)
            try:
                taille_kel = float("".join(producto.ficha_tecnica['Hauteur'].replace(",",".").split(' cm')))
                worksheet.write(5, icol + 2, producto.ficha_tecnica["Hauteur"], format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                largeur_kel = float("".join(producto.ficha_tecnica['Largeur'].replace(",", ".").split(' cm')))
                worksheet.write(6, icol + 2, producto.ficha_tecnica["Largeur"], format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                prof_kel = float("".join(producto.ficha_tecnica['Profondeur'].replace(",", ".").split(' cm')))
                worksheet.write(7, icol + 2, producto.ficha_tecnica["Profondeur"], format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                vol_utile_cong_kel = float(producto.ficha_tecnica['Volume net du congélateur'].replace('litres',''))
                vol_utile_ref_kel = float(producto.ficha_tecnica['Volume net du réfrigérateur'].replace('litres',''))
                worksheet.write(8, icol + 2, str(vol_utile_ref_kel) + " L", format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                worksheet.write(9, icol + 2, producto.ficha_tecnica['Volume net frigo'], format)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                worksheet.write(10, icol + 2, str(vol_utile_cong_kel) + " L", format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica['Volume net cong'], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)
            try:
                worksheet.write(12, icol + 2, str(vol_utile_cong_kel+vol_utile_ref_kel) + " L", format)
            except:
                worksheet.write(12, icol + 2, '', format_NA)
            try:
                worksheet.write(13, icol + 2, '{0} L'.format(int((taille_kel*largeur_kel*prof_kel)/1000)), format)
            except:
                worksheet.write(13, icol + 2, '', format_NA)
            try:
                if 'Posable' in producto.ficha_tecnica["Type de pose"]:
                    worksheet.write(14, icol + 2, "Pose libre", format)
                else:
                    worksheet.write(14, icol + 2, "Integrable", format)
            except:
                worksheet.write(14, icol + 2, '', format_NA)
            try:
                worksheet.write(15, icol + 2, producto.ficha_tecnica["Classe énergétique"], format)
            except:
                worksheet.write(15, icol + 2, '', format_NA)
            try:
                worksheet.write(16, icol + 2, producto.ficha_tecnica["Couleur"], format)
            except:
                worksheet.write(16, icol + 2, '', format_NA)
            try:
                worksheet.write(17, icol + 2, producto.ficha_tecnica["Froid ventilé"], format)
            except:
                worksheet.write(17, icol + 2, '', format_NA)
            try:
                worksheet.write(18, icol + 2, producto.ficha_tecnica["Froid du congélateur"], format)
            except:
                worksheet.write(18, icol + 2, '', format_NA)
            try:
                if "Froid NoFrost" in producto.ficha_tecnica['Froid du congélateur']:
                    worksheet.write(19, icol + 2, "NoFrost", format)
                else:
                    worksheet.write(19, icol + 2, '', format_NA)
            except:
                worksheet.write(19, icol + 2, '', format_NA)
            try:
                worksheet.write(20, icol + 2, producto.ficha_tecnica["Technologie"], format)
            except:
                worksheet.write(20, icol + 2, '', format_NA)
            try:
                if producto.ficha_tecnica["Distributeur de glace"] != "":
                    worksheet.write(21, icol + 2, "Oui", format)
                else:
                    worksheet.write(21, icol + 2, '', format_NA)
            except:
                worksheet.write(21, icol + 2, '', format_NA)
            try:
                worksheet.write(22, icol + 2, producto.ficha_tecnica["Consommation énergétique annuelle"], format)
            except:
                worksheet.write(22, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(24+4*k,icol+2, producto.tiendas[k]['precio'].replace("\xa0",""), format)
                        if (producto.tiendas[k]['nombre_tienda']) == '':
                            worksheet.write(25 + 4 * k, icol + 2, '', format_NA)
                        else:
                            worksheet.write(25+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(26+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(24+4*k,icol+2,"", format_NA)
                        worksheet.write(25+4*k,icol+2, "", format_NA)
                        worksheet.write(26+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(24+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(25+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(26+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                    else:
                        worksheet.write(24+4*k,icol+2,"", format_NA)
                        worksheet.write(25+4*k,icol+2, "", format_NA)
                        worksheet.write(26+4*k,icol+2, "", format_NA)

            icol += 1

    # Ancho de columna (todos los productos)
    worksheet.set_column(1, icol + 2, 30)

    # FIN
    workbook.close()

    if EXPORT_DATA_TO_EXTERNAL_HOST:
        xlsx_bytes = output.getvalue()
        return xlsx_bytes

    return None


def xlsx_congelador(req_xlsx_gen):

    try:
        EXPORT_DATA_TO_EXTERNAL_HOST = settings.EXPORT_DATA_TO_EXTERNAL_HOST
    except AttributeError:
        raise AttributeError(
            "Debe definir en el archivo "
            "settings la variable EXPORT_DATA_TO_EXTERNAL_HOST")

    try:
        TMP_FOLDER = settings.TMP_FOLDER
    except AttributeError:
        raise AttributeError(
            "Debe definir en el archivo "
            "settings la variable TMP_FOLDER")

    job_id = req_xlsx_gen["job_id"]

    if EXPORT_DATA_TO_EXTERNAL_HOST:
        output = BytesIO()
        workbook = Workbook(output)
    else:
        output_file_name = TMP_FOLDER + '/xlsx_' + job_id + '.xlsx'
        workbook = Workbook(output_file_name)

    filtros = req_xlsx_gen["data"][0]

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
    # 3) EXTRACCION DE DATOS DE DB
    # <<<<<<<<<<<<<
    job = Job.objects.get(_job_id=job_id)
    products = job.substitution_similar_results.all()

    list_products_pre = list(products.values_list('pk', 'tiendas'))
    list_products = []
    for i in list_products_pre:
        if i[1] == []:
            continue
        elif i[1][0]['precio'].replace('\xa0',"").replace(" EUR", "").replace(" ", "") != '':
            list_products.append(i)
    # list_products = [i for i in list_products if i[1] != []]
    # list_products = [i for i in list_products if i[1][0]['precio'].replace('\xa0',"").replace(" EUR", "").replace(" ", "") != '']
    list_products = sorted(list_products, key=lambda k: float(k[1][0]['precio'].replace('\xa0',"").replace(" EUR", "").replace(" ", "")))


    # <<<<<<<<<<<<<
    # 4) MAXIMO NUMERO DE TIENDAS
    # <<<<<<<<<<<<<
    max_tiendas = 0

    for product in products:
        if isinstance(product.tiendas, list):
            num_tiendas = len(product.tiendas)
        elif isinstance(product.tiendas, dict):
            num_tiendas = 1
        else:
            raise TypeError("la variable 'tiendas' es un tipo incorrecto")

        if num_tiendas > max_tiendas:
            max_tiendas = num_tiendas

    # <<<<<<<<<<<<<
    # 5) DETERMINAMOS LA ESTRUCTURA DEL ARCHIVO EXCEL
    # <<<<<<<<<<<<<
    #Creamos la estructura del archivo excel:
    worksheet.write('A2', "Marque", format_header)
    worksheet.write('A3', "Modèle", format_header)
    worksheet.write('A4', "Type d'appareil", format_header)
    worksheet.write('A5', "Subtype", format_header)
    worksheet.write('A6', "Hauteur", format_header)
    worksheet.write('A7', "Largeur", format_header)
    worksheet.write('A8', "Profoundeur", format_header)
    worksheet.write('A9', "Volume utile", format_header)
    worksheet.write('A10', "Volume net", format_header)
    worksheet.write('A11', "Type de pose", format_header)
    worksheet.write('A12', "Energy", format_header)
    worksheet.write('A13', "Consommation (kWh/an)", format_header)
    worksheet.write('A14', "Système de froid", format_header)
    worksheet.write('A15', "Couleur", format_header)
    for k in range(max_tiendas):
        worksheet.write(16+4*k,0, "Prix", format_header)
        worksheet.write(17+4*k,0, "Enseigne", format_header)
        worksheet.write(18+4*k,0, "URL", format_header)

    # <<<<<<<<<<<<<
    # 6) COLUMNA DE PRODUCTO A REEMPLAZAR
    # <<<<<<<<<<<<<

    worksheet.write('B1', "Modèle endommagé", format_header)
    worksheet.write('B2', filtros['Marque'].upper(), format)
    worksheet.write('B3', filtros['Modele'], format)
    worksheet.write('B4', 'Congélateur', format)
    worksheet.write('B5', filtros['Subtype'], format)
    worksheet.write('B6', filtros['Hateur'], format)
    worksheet.write('B7', filtros['Largeur'], format)
    worksheet.write('B8', filtros['Profoundeur'], format)
    worksheet.write('B9', filtros['Volume utile'], format)
    worksheet.write('B10', filtros['Volume net'], format)
    worksheet.write('B11', filtros['TypePose'], format)
    worksheet.write('B12', filtros['Energy'], format)
    worksheet.write('B13', filtros['Consommation'], format)
    worksheet.write('B14', filtros['Systeme de froid'], format)
    worksheet.write('B15', filtros['Couleur'], format)

    for k in range(max_tiendas):
        worksheet.write(16+4*k,1, "", format_NA)
        worksheet.write(17+4*k,1, "", format_NA)
        worksheet.write(18+4*k,1, "", format_NA)

    # <<<<<<<<<<<<<
    # 7) ESCRITURA
    # <<<<<<<<<<<<<

    for _product in list_products:
        producto = products.get(pk=_product[0])
    
        # PRICERUNNER <<<<<<<<<<<<<<<<<<<<<<
        if producto.store_id == "4":

            if producto.tiendas==[]: continue

            worksheet.write(0, icol + 2, "".join(("Produit ", str(icol + 1))), format_header)
            try:
                worksheet.write(1, icol + 2, producto.ficha_tecnica['Marque'].upper(), format)
            except:
                worksheet.write(1, icol + 2, '', format_NA)
            try:
                worksheet.write(2, icol + 2, "".join(producto.nombre.split(producto.ficha_tecnica['Marque'])), format)
            except:
                worksheet.write(2, icol + 2, '', format_NA)
            try:
                worksheet.write(3, icol + 2, 'Congélateur', format)
            except:
                worksheet.write(3, icol + 2, '', format_NA)
            try:
                worksheet.write(4, icol + 2, producto.ficha_tecnica["Type"], format)
            except:
                worksheet.write(4, icol + 2, '', format_NA)
            try:
                worksheet.write(5, icol + 2, producto.ficha_tecnica['Taille'], format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                worksheet.write(6, icol + 2, producto.ficha_tecnica['Largeur Montre la largeur du produit. Son montré en centimètre.'], format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                worksheet.write(7, icol + 2, producto.ficha_tecnica['Profondeur Montre la profondeur du produit. On lui montre en centimètre.'], format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                worksheet.write(8, icol + 2, producto.ficha_tecnica["Volume Le volume nous indique la capacité de contenance du congélateur, qui est mesuré en litre. Un congélateur de 185 cm a un volume de 275 litres."], format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                taille_pr = float("".join(producto.ficha_tecnica['Taille'].split(' cm')))
                largeur_pr = float("".join(producto.ficha_tecnica['Largeur Montre la largeur du produit. Son montré en centimètre.'].split(' cm')))
                prof_pr = float("".join(producto.ficha_tecnica['Profondeur Montre la profondeur du produit. On lui montre en centimètre.'].split(' cm')))
                worksheet.write(9, icol + 2, '{0} L'.format(int((taille_pr*largeur_pr*prof_pr)/1000)), format)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                worksheet.write(10, icol + 2, producto.ficha_tecnica["Type de pose"], format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica["Catégories d'énergie Les congélateurs sont habituellement alimentés en continu. Vous économiserez ainsi en coûts de fonctionnement à long terme si vous optez pour un modèle à faible consommation. Les catégories d'énergie sont mesurés sur une échelle entre A+++ et F, A+++ correspondant à la plus basse cadence de consommation et F à la plus haute. La loi européenne déclare que tous les congélateurs doivent indiquer leur consommation en énergie."], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)
            try:
                worksheet.write(12, icol + 2, producto.ficha_tecnica["Energy Consumption (kWh/year)"], format)
            except:
                worksheet.write(12, icol + 2, '', format_NA)
            try:
                worksheet.write(13, icol + 2, producto.ficha_tecnica["Systeme Froid"], format)
            except:
                worksheet.write(13, icol + 2, '', format_NA)
            try:
                worksheet.write(14, icol + 2, producto.ficha_tecnica["Couleur"], format)
            except:
                worksheet.write(14, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(16+4*k,icol+2, producto.tiendas[k]['precio'], format)
                        if (producto.tiendas[k]['nombre_tienda']) == '':
                            worksheet.write(17 + 4 * k, icol + 2, '', format_NA)
                        else:
                            worksheet.write(17+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(16+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(17+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)

            icol += 1

        # DARTY <<<<<<<<<<<<<<<<<<<<<<
        elif producto.store_id == "1":
            worksheet.write(0,icol+2, "".join(("Produit ",str(icol+1))), format_header)
            try:
                worksheet.write(1,icol+2, producto.nombre.split(" ")[0].upper(), format)
            except:
                worksheet.write(1,icol+2,'',format_NA)
            try:
                worksheet.write(2,icol+2, " ".join(producto.nombre.split(" ")[1:]), format)
            except:
                worksheet.write(2,icol+2,'',format_NA)
            try:
                worksheet.write(3,icol+2,'Congélateur',format)
            except:
                worksheet.write(3,icol+2,'',format_NA)
            try:
                if "armoire" in producto.tiendas[0]["url_tienda"]:
                    worksheet.write(4, icol + 2, 'Congélateur armoire', format)
                elif "coffre" in producto.tiendas[0]["url_tienda"]:
                    worksheet.write(4, icol + 2, 'Congélateur coffre', format)
            except:
                worksheet.write(4,icol+2,'',format_NA)
            try:
                worksheet.write(5, icol + 2, producto.ficha_tecnica['Hauteur (cm)'], format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                worksheet.write(6, icol + 2, producto.ficha_tecnica['Largeur (cm)'], format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                worksheet.write(7, icol + 2, producto.ficha_tecnica['Profondeur (cm)'], format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                worksheet.write(8, icol + 2, producto.ficha_tecnica["Volume total net"], format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                taille_dar = float("".join(producto.ficha_tecnica['Hauteur (cm)'].split(' cm')).replace(',',"."))
                largeur_dar = float("".join(producto.ficha_tecnica['Largeur (cm)'].split(' cm')).replace(',',"."))
                prof_dar = float("".join(producto.ficha_tecnica['Profondeur (cm)'].split(' cm')).replace(',',"."))
                worksheet.write(9, icol + 2, '{0} L'.format(int((taille_dar*largeur_dar*prof_dar)/1000)), format)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                worksheet.write(10, icol + 2, producto.ficha_tecnica["TypePose"], format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica["Classe énergétique"], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)
            try:
                worksheet.write(12, icol + 2, producto.ficha_tecnica["Consommation d'énergie (Norme EN 153)"], format)
            except:
                worksheet.write(12, icol + 2, '', format_NA)
            try:
                worksheet.write(13, icol + 2, producto.ficha_tecnica["Type de congélation"], format)
            except:
                worksheet.write(13, icol + 2, '', format_NA)
            try:
                worksheet.write(14, icol + 2, producto.ficha_tecnica["Finition"], format)
            except:
                worksheet.write(14, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(16+4*k,icol+2, producto.tiendas[k]['precio'], format)
                        if (producto.tiendas[k]['nombre_tienda']) == '':
                            worksheet.write(17 + 4 * k, icol + 2, '', format_NA)
                        else:
                            worksheet.write(17+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(16+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(17+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)

            icol += 1

        # BOULANGER <<<<<<<<<<<<<<<<<<<<<<
        elif producto.store_id == "3":
            worksheet.write(0,icol+2, "".join(("Produit ",str(icol+1))), format_header)
            try:
                worksheet.write(1,icol+2, producto.nombre.split(" ")[2].upper(), format)
            except:
                worksheet.write(1,icol+2,'',format_NA)
            try:
                worksheet.write(2,icol+2, "".join(producto.nombre.split(" ")[3:]), format)
            except:
                worksheet.write(2, icol + 2, '', format_NA)
            try:
                worksheet.write(3, icol + 2, 'Congélateur', format)
            except:
                worksheet.write(3, icol + 2, '', format_NA)
            try:
                if "coffre" in producto.ficha_tecnica["Type d'appareil"]:
                    worksheet.write(4,icol+2,'Congélateur coffre',format)
                else:
                    worksheet.write(4, icol + 2, 'Congélateur armoire', format)
            except:
                worksheet.write(4, icol + 2,'', format_NA)
            try:
                taille_bou = float(producto.ficha_tecnica["L x H x P"].
                                   split('x')[1])
                if taille_bou >=250: taille_bou = taille_bou/10
                worksheet.write(5, icol + 2, "{0} cm".format(taille_bou), format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                largeur_bou = float(producto.ficha_tecnica["L x H x P"].
                                   split('x')[0])
                if largeur_bou >=250: largeur_bou = largeur_bou/10
                worksheet.write(6, icol + 2, "{0} cm".format(largeur_bou), format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                prof_bou = float(producto.ficha_tecnica["L x H x P"].
                                   split('x')[2].replace("cm",""))
                if prof_bou >=250: prof_bou = prof_bou/10
                worksheet.write(7, icol + 2, "{0}".format(prof_bou), format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                worksheet.write(8, icol + 2, producto.ficha_tecnica["Volume total"].replace("l","L"), format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                worksheet.write(9, icol + 2, '{0} L'.format(int((taille_bou*largeur_bou*prof_bou)/1000)), format)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                if 'Encastrable' in producto.ficha_tecnica["Type d'installation"]:
                    worksheet.write(10, icol + 2, "Integrable", format)
                else:
                    worksheet.write(10, icol + 2, "Pose libre", format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica["Classe énergétique"].split(" ")[0], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)
            try:
                worksheet.write(12, icol + 2, producto.ficha_tecnica["Consommation annuelle"], format)
            except:
                worksheet.write(12, icol + 2, '', format_NA)
            try:
                if "statique" in "".join(producto.detalles):
                    syst_boul = "Statique"
                elif "brassé" in "".join(producto.detalles):
                    syst_boul = "Brassé"
                elif "ventilé" in "".join(producto.detalles):
                    syst_boul = "Ventilé"
                worksheet.write(13, icol + 2, syst_boul, format)
            except:
                worksheet.write(13, icol + 2, '', format_NA)
            try:
                worksheet.write(14, icol + 2, producto.ficha_tecnica["Couleur produit"], format)
            except:
                worksheet.write(14, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(16+4*k,icol+2, producto.tiendas[k]['precio'], format)
                        if (producto.tiendas[k]['nombre_tienda']) == '':
                            worksheet.write(17 + 4 * k, icol + 2, '', format_NA)
                        else:
                            worksheet.write(17+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(16+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(17+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)

            icol += 1

        # KELKOO <<<<<<<<<<<<<<<<<<<<<<
        elif producto.store_id == "2":

            if producto.tiendas==[]: continue

            worksheet.write(0,icol+2, "".join(("Produit ",str(icol+1))), format_header)
            try:
                marque_kelkoo = producto.ficha_tecnica['Marque']
                find_interr = marque_kelkoo.find('?')
                marque_filtros = filtros['Marque'][:find_interr] + filtros['Marque'][find_interr+1:]
                if marque_filtros == marque_kelkoo.replace('?',''):
                    worksheet.write(1,icol+2, filtros['Marque'].upper(), format)
                else:
                    worksheet.write(1, icol + 2, producto.ficha_tecnica['Marque'].upper(), format)
            except:
                worksheet.write(1, icol + 2, "", format)
            try:
                worksheet.write(2,icol+2, producto.nombre.split(marque_kelkoo)[1][1:], format)
            except:
                worksheet.write(2, icol + 2, "", format)
            try:
                worksheet.write(3, icol + 2, producto.ficha_tecnica['Catégorie'], format)
            except:
                worksheet.write(3, icol + 2, "", format)
            try:
                worksheet.write(4, icol + 2, producto.ficha_tecnica['Type de congélateur'], format)
            except:
                worksheet.write(4, icol + 2, '', format_NA)
            try:
                taille_kel = float(producto.ficha_tecnica["Hauteur"].replace("cm","").replace(",","."))
                worksheet.write(5, icol + 2, producto.ficha_tecnica["Hauteur"], format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                largeur_kel = float(producto.ficha_tecnica["Largeur"].replace("cm", "").replace(",", "."))
                worksheet.write(6, icol + 2, producto.ficha_tecnica["Largeur"], format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                prof_kel = float(producto.ficha_tecnica["Profondeur"].replace("cm", "").replace(",", "."))
                worksheet.write(7, icol + 2, producto.ficha_tecnica["Profondeur"], format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                worksheet.write(8, icol + 2, producto.ficha_tecnica["Volume net"].replace("litres"," L"), format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                worksheet.write(9, icol + 2, '{0} L'.format(int((taille_kel*largeur_kel*prof_kel)/1000)), format)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                worksheet.write(10, icol + 2, producto.ficha_tecnica["Type de pose"], format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica["Classe énergétique"].split(" ")[0], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)
            try:
                worksheet.write(12, icol + 2, producto.ficha_tecnica["Consommation énergétique annuelle moyenne"], format)
            except:
                worksheet.write(12, icol + 2, '', format_NA)
            try:
                if producto.ficha_tecnica["Froid ventilé"] == "Avec froid ventilé":
                    worksheet.write(13, icol + 2, "Froid ventilé", format)
            except:
                worksheet.write(13, icol + 2, '', format_NA)
            try:
                worksheet.write(14, icol + 2, producto.ficha_tecnica["Couleur"], format)
            except:
                worksheet.write(14, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(16+4*k,icol+2, producto.tiendas[k]['precio'], format)
                        if (producto.tiendas[k]['nombre_tienda']) == '':
                            worksheet.write(17 + 4 * k, icol + 2, '', format_NA)
                        else:
                            worksheet.write(17+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(16+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(17+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)

            icol += 1

    # Ancho de columna (todos los productos)
    worksheet.set_column(1, icol + 2, 30)

    # FIN
    workbook.close()

    if EXPORT_DATA_TO_EXTERNAL_HOST:
        xlsx_bytes = output.getvalue()
        return xlsx_bytes

    return None


def xlsx_cava_vino(req_xlsx_gen):

    try:
        EXPORT_DATA_TO_EXTERNAL_HOST = settings.EXPORT_DATA_TO_EXTERNAL_HOST
    except AttributeError:
        raise AttributeError(
            "Debe definir en el archivo "
            "settings la variable EXPORT_DATA_TO_EXTERNAL_HOST")

    try:
        TMP_FOLDER = settings.TMP_FOLDER
    except AttributeError:
        raise AttributeError(
            "Debe definir en el archivo "
            "settings la variable TMP_FOLDER")

    job_id = req_xlsx_gen["job_id"]

    if EXPORT_DATA_TO_EXTERNAL_HOST:
        output = BytesIO()
        workbook = Workbook(output)
    else:
        output_file_name = TMP_FOLDER + '/xlsx_' + job_id + '.xlsx'
        workbook = Workbook(output_file_name)

    filtros = req_xlsx_gen["data"][0]

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
    # 3) EXTRACCION DE DATOS DE DB
    # <<<<<<<<<<<<<
    job = Job.objects.get(_job_id=job_id)
    products = job.substitution_similar_results.all()

    list_products_pre = list(products.values_list('pk', 'tiendas'))
    list_products = []
    for i in list_products_pre:
        if i[1] == []:
            continue
        elif i[1][0]['precio'].replace('\xa0',"").replace(" EUR", "").replace(" ", "") != '':
            list_products.append(i)
    # list_products = [i for i in list_products if i[1] != []]
    # list_products = [i for i in list_products if i[1][0]['precio'].replace('\xa0',"").replace(" EUR", "").replace(" ", "") != '']
    list_products = sorted(list_products, key=lambda k: float(k[1][0]['precio'].replace('\xa0',"").replace(" EUR", "").replace(" ", "")))


    # <<<<<<<<<<<<<
    # 4) MAXIMO NUMERO DE TIENDAS
    # <<<<<<<<<<<<<
    max_tiendas = 0

    for product in products:
        if isinstance(product.tiendas, list):
            num_tiendas = len(product.tiendas)
        elif isinstance(product.tiendas, dict):
            num_tiendas = 1
        else:
            raise TypeError("la variable 'tiendas' es un tipo incorrecto")

        if num_tiendas > max_tiendas:
            max_tiendas = num_tiendas

    # <<<<<<<<<<<<<
    # 5) DETERMINAMOS LA ESTRUCTURA DEL ARCHIVO EXCEL
    # <<<<<<<<<<<<<
    #Creamos la estructura del archivo excel:
    worksheet.write('A2', "Marque", format_header)
    worksheet.write('A3', "Modèle", format_header)
    worksheet.write('A4', "Type d'appareil", format_header)
    worksheet.write('A5', "Subtype", format_header)
    worksheet.write('A6', "Hauteur", format_header)
    worksheet.write('A7', "Largeur", format_header)
    worksheet.write('A8', "Profoundeur", format_header)
    worksheet.write('A9', "Stockage (bouteilles)", format_header)
    worksheet.write('A10', "Volume net", format_header)
    worksheet.write('A11', "Type de pose", format_header)
    worksheet.write('A12', "Energy", format_header)
    worksheet.write('A13', "Consommation (kWh/an)", format_header)
    worksheet.write('A14', "Système de froid", format_header)
    worksheet.write('A15', "Couleur", format_header)
    for k in range(max_tiendas):
        worksheet.write(16+4*k,0, "Prix", format_header)
        worksheet.write(17+4*k,0, "Enseigne", format_header)
        worksheet.write(18+4*k,0, "URL", format_header)

    # <<<<<<<<<<<<<
    # 6) COLUMNA DE PRODUCTO A REEMPLAZAR
    # <<<<<<<<<<<<<

    worksheet.write('B1', "Modèle endommagé", format_header)
    worksheet.write('B2', filtros['Marque'].upper(), format)
    worksheet.write('B3', filtros['Modele'], format)
    worksheet.write('B4', 'Cave à vin', format)
    worksheet.write('B5', filtros['Subtype'], format)
    worksheet.write('B6', filtros['Hateur'], format)
    worksheet.write('B7', filtros['Largeur'], format)
    worksheet.write('B8', filtros['Profoundeur'], format)
    worksheet.write('B9', filtros['Stockage'], format)
    worksheet.write('B10', filtros['Volume net'], format)
    worksheet.write('B11', filtros['TypePose'], format)
    worksheet.write('B12', filtros['Energy'], format)
    worksheet.write('B13', filtros['Consommation'], format)
    worksheet.write('B14', filtros['Systeme de froid'], format)
    worksheet.write('B15', filtros['Couleur'], format)

    for k in range(max_tiendas):
        worksheet.write(16+4*k,1, "", format_NA)
        worksheet.write(17+4*k,1, "", format_NA)
        worksheet.write(18+4*k,1, "", format_NA)

    for _product in list_products:
        producto = products.get(pk=_product[0])
    
        # PRICERUNNER <<<<<<<<<<<<<<<<<<<<<<
        if producto.store_id == "4":

            if producto.tiendas==[]: continue

            worksheet.write(0, icol + 2, "".join(("Produit ", str(icol + 1))), format_header)
            try:
                worksheet.write(1, icol + 2, producto.ficha_tecnica['Marque'].upper(), format)
            except:
                worksheet.write(1, icol + 2, '', format_NA)
            try:
                worksheet.write(2, icol + 2, "".join(producto.nombre.split(producto.ficha_tecnica['Marque'])), format)
            except:
                worksheet.write(2, icol + 2, '', format_NA)
            try:
                worksheet.write(3, icol + 2, 'Cave à vin', format)
            except:
                worksheet.write(3, icol + 2, '', format_NA)
            try:
                worksheet.write(4, icol + 2, producto.ficha_tecnica["Type"], format)
            except:
                worksheet.write(4, icol + 2, '', format_NA)
            try:
                taille_pr = float(producto.ficha_tecnica["Taille"].replace("cm", "").replace(",", "."))
                worksheet.write(5, icol + 2, producto.ficha_tecnica['Taille'], format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                largeur_pr = float(producto.ficha_tecnica["Largeur"].replace("cm", "").replace(",", "."))
                worksheet.write(6, icol + 2, producto.ficha_tecnica['Largeur'], format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                prof_pr = float(producto.ficha_tecnica["Profondeur"].replace("cm", "").replace(",", "."))
                worksheet.write(7, icol + 2, producto.ficha_tecnica['Profondeur'], format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                worksheet.write(8, icol + 2, producto.ficha_tecnica["Nb. de bouteilles Indique le nombre de bouteilles que la cave à vin peut contenir."], format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                worksheet.write(9, icol + 2, '{0} L'.format(int((taille_pr*largeur_pr*prof_pr)/1000)), format)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                worksheet.write(10, icol + 2, producto.ficha_tecnica["Placement"], format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica["Classe d'énergie"], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)
            try:
                worksheet.write(12, icol + 2, producto.ficha_tecnica["Consommation d'énergie Indique la consommation d'énergie annuelle de l'appareil, en Watts."], format)
            except:
                worksheet.write(12, icol + 2, '', format_NA)
            try:
                worksheet.write(13, icol + 2, producto.ficha_tecnica["Systeme Froid"], format)
            except:
                worksheet.write(13, icol + 2, '', format_NA)
            try:
                worksheet.write(14, icol + 2, producto.ficha_tecnica["Couleur / Habillage"], format)
            except:
                worksheet.write(14, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(16+4*k,icol+2, producto.tiendas[k]['precio'], format)
                        if (producto.tiendas[k]['nombre_tienda']) == '':
                            worksheet.write(17 + 4 * k, icol + 2, '', format_NA)
                        else:
                            worksheet.write(17+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(16+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(17+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)

            icol += 1

        # DARTY <<<<<<<<<<<<<<<<<<<<<<
        elif producto.store_id == "1":
            worksheet.write(0,icol+2, "".join(("Produit ",str(icol+1))), format_header)
            try:
                if "La Sommeliere" in producto.nombre:
                    worksheet.write(1, icol + 2, "LA SOMMELIERE", format)
                else:
                    worksheet.write(1,icol+2, producto.nombre.split(" ")[0].upper(), format)
            except:
                worksheet.write(1,icol+2,'',format_NA)
            try:
                if "La Sommeliere" in producto.nombre:
                    worksheet.write(2, icol + 2, " ".join(producto.nombre.split(" ")[2:]), format)
                else:
                    worksheet.write(2,icol+2, " ".join(producto.nombre.split(" ")[1:]), format)
            except:
                worksheet.write(2,icol+2,'',format_NA)
            try:
                worksheet.write(3,icol+2,'Cave à vin',format)
            except:
                worksheet.write(3,icol+2,'',format_NA)
            try:
                if "service" in producto.tiendas[0]["url_tienda"]:
                    worksheet.write(4, icol + 2, 'Cave à vin service', format)
                elif "vieillissement" in producto.tiendas[0]["url_tienda"]:
                    worksheet.write(4, icol + 2, 'Cave à vin vieillissement', format)
                elif "multi-temperatures" in producto.tiendas[0]["url_tienda"]:
                    worksheet.write(4, icol + 2, 'Cave à vin multi-températures', format)
            except:
                worksheet.write(4,icol+2,'',format_NA)
            try:
                taille_dart = float(producto.ficha_tecnica["Hauteur"].replace("cm", "").replace(",", "."))
                worksheet.write(5, icol + 2, producto.ficha_tecnica['Hauteur'], format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                largeur_dart = float(producto.ficha_tecnica["Largeur (cm)"].replace("cm", "").replace(",", "."))
                worksheet.write(6, icol + 2, producto.ficha_tecnica['Largeur (cm)'], format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                prof_dart = float(producto.ficha_tecnica["Profondeur (cm)"].replace("cm", "").replace(",", "."))
                worksheet.write(7, icol + 2, producto.ficha_tecnica['Profondeur (cm)'], format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                worksheet.write(8, icol + 2, producto.ficha_tecnica["Capacité (bouteilles)"], format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                worksheet.write(9, icol + 2, '{0} L'.format(int((taille_dart*largeur_dart*prof_dart)/1000)), format)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                worksheet.write(10, icol + 2, producto.ficha_tecnica["TypePose"], format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica["Classe énergétique"], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)
            try:
                worksheet.write(12, icol + 2, producto.ficha_tecnica["Consommation d'énergie"], format)
            except:
                worksheet.write(12, icol + 2, '', format_NA)
            try:
                worksheet.write(13, icol + 2, producto.ficha_tecnica["Type de congélation"], format)
            except:
                worksheet.write(13, icol + 2, '', format_NA)
            try:
                worksheet.write(14, icol + 2, producto.ficha_tecnica["Finition"], format)
            except:
                worksheet.write(14, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(16+4*k,icol+2, producto.tiendas[k]['precio'], format)
                        if (producto.tiendas[k]['nombre_tienda']) == '':
                            worksheet.write(17 + 4 * k, icol + 2, '', format_NA)
                        else:
                            worksheet.write(17+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(16+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(17+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)

            icol += 1

# BOULANGER <<<<<<<<<<<<<<<<<<<<<<
        elif producto.store_id == "3":
            worksheet.write(0,icol+2, "".join(("Produit ",str(icol+1))), format_header)
            try:
                if 'La Sommeliere' in producto.nombre:
                    worksheet.write(1, icol + 2, "LA SOMMELIERE", format)
                else:
                    if "polyvalente" in producto.nombre:
                        worksheet.write(1, icol + 2, producto.nombre.split(" ")[2].upper(), format)
                    else:
                        worksheet.write(1, icol + 2, producto.nombre.split(" ")[3].upper(), format)
            except:
                worksheet.write(1,icol+2,'',format_NA)
            try:
                if 'La Sommeliere' in producto.nombre:
                    if "polyvalente" in producto.nombre:
                        worksheet.write(2, icol + 2, " ".join(producto.nombre.split(" ")[4:]), format)
                    else:
                        worksheet.write(2, icol + 2, " ".join(producto.nombre.split(" ")[5:]), format)
                else:
                    if "polyvalente" in producto.nombre:
                        worksheet.write(2, icol + 2, " ".join(producto.nombre.split(" ")[3:]), format)
                    else:
                        worksheet.write(2, icol + 2, " ".join(producto.nombre.split(" ")[4:]), format)
            except:
                worksheet.write(2, icol + 2, '', format_NA)
            try:
                worksheet.write(3, icol + 2, 'Cave à vin', format)
            except:
                worksheet.write(3, icol + 2, '', format_NA)
            try:
                if "polyvalente" in producto.ficha_tecnica["Type d'appareil"].lower():
                    worksheet.write(4,icol+2,'Cave à vin multi-températures',format)
                elif "service" in producto.ficha_tecnica["Type d'appareil"].lower():
                    worksheet.write(4,icol+2,'Cave à vin service',format)
                elif "vieillissement" in producto.ficha_tecnica["Type d'appareil"].lower():
                    worksheet.write(4, icol + 2, 'Cave à vin vieillissement', format)
            except:
                worksheet.write(4, icol + 2,'', format_NA)
            try:
                taille_bou = float(producto.ficha_tecnica["L x H x P :"].
                                   split('x')[1])
                if taille_bou >=250: taille_bou = taille_bou/10
                worksheet.write(5, icol + 2, "{0} cm".format(taille_bou), format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                largeur_bou = float(producto.ficha_tecnica["L x H x P :"].
                                   split('x')[0])
                if largeur_bou >=250: largeur_bou = largeur_bou/10
                worksheet.write(6, icol + 2, "{0} cm".format(largeur_bou), format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                prof_bou = float(producto.ficha_tecnica["L x H x P :"].
                                   split('x')[2].replace("cm",""))
                if prof_bou >=250: prof_bou = prof_bou/10
                worksheet.write(7, icol + 2, "{0}".format(prof_bou), format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                worksheet.write(8, icol + 2, producto.ficha_tecnica["Capacité avec clayettes (Type Bordelaises légères)"], format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                worksheet.write(9, icol + 2, '{0} L'.format(int((taille_bou*largeur_bou*prof_bou)/1000)), format)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                if 'Encastrable' in producto.ficha_tecnica["Type d'installation"]:
                    worksheet.write(10, icol + 2, "Integrable", format)
                else:
                    worksheet.write(10, icol + 2, "Pose libre", format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica["Classe énergétique"].split(" ")[0], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)
            try:
                worksheet.write(12, icol + 2, producto.ficha_tecnica["Consommation"], format)
            except:
                worksheet.write(12, icol + 2, '', format_NA)
            try:
                if "statique" in "".join(producto.detalles):
                    syst_boul = "Statique"
                elif "brassé" in "".join(producto.detalles):
                    syst_boul = "Brassé"
                elif "ventilé" in "".join(producto.detalles):
                    syst_boul = "Ventilé"
                worksheet.write(13, icol + 2, syst_boul, format)
            except:
                worksheet.write(13, icol + 2, '', format_NA)
            try:
                worksheet.write(14, icol + 2, producto.ficha_tecnica["Couleur"], format)
            except:
                worksheet.write(14, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(16+4*k,icol+2, producto.tiendas[k]['precio'], format)
                        if (producto.tiendas[k]['nombre_tienda']) == '':
                            worksheet.write(17 + 4 * k, icol + 2, '', format_NA)
                        else:
                            worksheet.write(17+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(16+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(17+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)

            icol += 1

        # KELKOO <<<<<<<<<<<<<<<<<<<<<<
        elif producto.store_id == "2":

            if producto.tiendas==[]: continue

            worksheet.write(0,icol+2, "".join(("Produit ",str(icol+1))), format_header)
            try:
                marque_kelkoo = producto.ficha_tecnica['Marque']
                find_interr = marque_kelkoo.find('?')
                marque_filtros = filtros['Marque'][:find_interr] + filtros['Marque'][find_interr+1:]
                if marque_filtros == marque_kelkoo.replace('?',''):
                    worksheet.write(1,icol+2, filtros['Marque'].upper(), format)
                else:
                    worksheet.write(1, icol + 2, producto.ficha_tecnica['Marque'].upper(), format)
            except:
                worksheet.write(1, icol + 2, "", format)
            try:
                worksheet.write(2,icol+2, producto.nombre.split(marque_kelkoo)[1][1:], format)
            except:
                worksheet.write(2, icol + 2, "", format)
            try:
                worksheet.write(3, icol + 2, producto.ficha_tecnica['Catégorie'], format)
            except:
                worksheet.write(3, icol + 2, "", format)
            try:
                worksheet.write(4, icol + 2, producto.ficha_tecnica['Type de cave à vin'], format)
            except:
                worksheet.write(4, icol + 2, '', format_NA)
            try:
                taille_kel = float(producto.ficha_tecnica["Hauteur"].replace("cm","").replace(",","."))
                worksheet.write(5, icol + 2, producto.ficha_tecnica["Hauteur"], format)
            except:
                worksheet.write(5, icol + 2, '', format_NA)
            try:
                largeur_kel = float(producto.ficha_tecnica["Largeur"].replace("cm", "").replace(",", "."))
                worksheet.write(6, icol + 2, producto.ficha_tecnica["Largeur"], format)
            except:
                worksheet.write(6, icol + 2, '', format_NA)
            try:
                prof_kel = float(producto.ficha_tecnica["Profondeur"].replace("cm", "").replace(",", "."))
                worksheet.write(7, icol + 2, producto.ficha_tecnica["Profondeur"], format)
            except:
                worksheet.write(7, icol + 2, '', format_NA)
            try:
                worksheet.write(8, icol + 2, producto.ficha_tecnica["Nombre de bouteilles"].replace("bouteilles", " bouteilles"), format)
            except:
                worksheet.write(8, icol + 2, '', format_NA)
            try:
                worksheet.write(9, icol + 2, '{0} L'.format(int((taille_kel*largeur_kel*prof_kel)/1000)), format)
            except:
                worksheet.write(9, icol + 2, '', format_NA)
            try:
                worksheet.write(10, icol + 2, producto.ficha_tecnica["Type de design"], format)
            except:
                worksheet.write(10, icol + 2, '', format_NA)
            try:
                worksheet.write(11, icol + 2, producto.ficha_tecnica["Classe énergétique"].split(" ")[0], format)
            except:
                worksheet.write(11, icol + 2, '', format_NA)
            try:
                worksheet.write(12, icol + 2, producto.ficha_tecnica["Consommation énergétique annuelle moyenne"], format)
            except:
                worksheet.write(12, icol + 2, '', format_NA)
            try:
                if producto.ficha_tecnica["Froid ventilé"] == "Avec froid ventilé":
                    worksheet.write(13, icol + 2, "Froid ventilé", format)
            except:
                worksheet.write(13, icol + 2, '', format_NA)
            try:
                worksheet.write(14, icol + 2, producto.ficha_tecnica["Couleur"], format)
            except:
                worksheet.write(14, icol + 2, '', format_NA)

            for k in range(max_tiendas):
                if isinstance(producto.tiendas, list):
                    if k<=len(producto.tiendas)-1:
                        worksheet.write(16+4*k,icol+2, producto.tiendas[k]['precio'], format)
                        if (producto.tiendas[k]['nombre_tienda']) == '':
                            worksheet.write(17 + 4 * k, icol + 2, '', format_NA)
                        else:
                            worksheet.write(17+4*k,icol+2, producto.tiendas[k]['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas[k]['url_tienda'].split('://')[1], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)
                else:
                    if len(producto.tiendas) > 0:
                        worksheet.write(16+4*k,icol+2, producto.tiendas['precio'], format)
                        worksheet.write(17+4*k,icol+2, producto.tiendas['nombre_tienda'], format)
                        worksheet.write(18+4*k,icol+2, producto.tiendas['url_tienda'], format_url)
                    else:
                        worksheet.write(16+4*k,icol+2,"", format_NA)
                        worksheet.write(17+4*k,icol+2, "", format_NA)
                        worksheet.write(18+4*k,icol+2, "", format_NA)

            icol += 1

    # Ancho de columna (todos los productos)
    worksheet.set_column(1, icol + 2, 30)

    # FIN
    workbook.close()

    if EXPORT_DATA_TO_EXTERNAL_HOST:
        xlsx_bytes = output.getvalue()
        return xlsx_bytes

    return None
