from io import BytesIO

from django.conf import settings

from xlsxwriter.workbook import Workbook


def xlsx_base(req_xlsx_gen):

    results = req_xlsx_gen["results"]
    if results["result_gfk"] is None:
        return None

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

    print("XLSX")

    results = results["result_gfk"]

    print(results)

    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 0, 50)
    worksheet.set_row(0, 30)

    # icol se usa para pasear por las columnas del excel
    icol = 0

    # <<<<<<<<<<<<<
    # 2) FORMATOS
    # <<<<<<<<<<<<<

    # Datos
    format_regular = workbook.add_format()
    format_regular.set_border(style=1)
    format_regular.set_text_wrap()
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
    # 3) DETERMINAMOS LA ESTRUCTURA DEL ARCHIVO EXCEL
    # <<<<<<<<<<<<<

    # Contamos el numero de caracteristicas
    broken_device = results["BrokenDevice"]
    num_feature = len(broken_device["FeatureData"])

    # Creamos la estructura del archivo excel:
    worksheet.write('A2', "Marque", format_header)
    worksheet.write('A3', "Référence commerciale", format_header)

    for k in range(num_feature):
        worksheet.write(3 + k, 0, broken_device["FeatureData"][k]["FeatureName"], format_header)

    worksheet.write(num_feature,0, "Prix en [EUR] le plus couramment practiqué", format_header)
    worksheet.write(num_feature + 1,0, "Prix moyen des modèles équivalentes", format_header)
    worksheet.write(num_feature + 2,0, "Date de la 1ère vente du produit", format_header)
    worksheet.write(num_feature + 3,0, "Date de la dernière vente enregistrée", format_header)
    worksheet.write(num_feature + 4,0, "Prix historique du modèle sinistré [EUR]", format_header)

    # <<<<<<<<<<<<<
    # 4) PRODUCTO DAÑADO
    # <<<<<<<<<<<<<

    # Creamos la estructura del archivo excel:
    worksheet.write('B1', "Modèle endommagé", format_header)
    try:
        if broken_device["MasterData"]["BrandName"] != None:
            worksheet.write('B2', broken_device["MasterData"]["BrandName"], format_regular)
        else:
            worksheet.write('B2', "", format_NA)
    except:
        worksheet.write('B2', "", format_NA)
    
    try:
        if broken_device["MasterData"]["ProductName"] != None:
            worksheet.write('B3', broken_device["MasterData"]["ProductName"], format_regular)
        else:
            worksheet.write('B3', "", format_NA)    
    except:
        worksheet.write('B3', "", format_NA)

    for k in range(num_feature):
        try:
            if broken_device["FeatureData"][k]["FeatureValue"] != None and broken_device["FeatureData"][k]["FeatureValue"] != "N/A":
                worksheet.write(3 + k, 1, broken_device["FeatureData"][k]["FeatureValue"], format_regular)
            else:
                worksheet.write(3 + k, 1, "", format_NA)            
        except:
            worksheet.write(3 + k, 1, "", format_NA)            

    try:
        if broken_device["MarketData"]["Price"] != None:
            worksheet.write(num_feature,1, broken_device["MarketData"]["Price"], format_regular)
        else:
            worksheet.write(num_feature,1, "", format_NA)       
    except:
        worksheet.write(num_feature,1, "", format_NA)

    worksheet.write(num_feature + 1,1, "", format_NA)

    try: 
        if broken_device["MarketData"]["HistoricalPrice"]["Period"]["Year"] == None:
            worksheet.write(num_feature + 2,1, "", format_NA)
        else:
            if broken_device["MarketData"]["HistoricalPrice"]["Period"]["Month"] == None:
                broken_device["MarketData"]["HistoricalPrice"]["Period"]["Month"] = ""
                fecha_antig = " ".join([broken_device["MarketData"]["HistoricalPrice"]["Period"]["Month"], broken_device["MarketData"]["HistoricalPrice"]["Period"]["Year"]])
                worksheet.write(num_feature + 2,1, fecha_antig, format_regular)
    except:
        worksheet.write(num_feature + 2,1, "", format_NA)  

    worksheet.write(num_feature + 3,1, "", format_NA)

    try:
        if broken_device["MarketData"]["HistoricalPrice"]["Price"] != None:
            worksheet.write(num_feature + 4,1, broken_device["MarketData"]["HistoricalPrice"]["Price"], format_regular)
        else:
            worksheet.write(num_feature + 4,1, "", format_NA) 
    except:
        worksheet.write(num_feature + 4,1, "", format_NA)        

    # <<<<<<<<<<<<<
    # 5) PRODUCTOS DE REEMPLAZO
    # <<<<<<<<<<<<<
    for producto in results["ReplacementDevices"]["WebMethodProduct"]:
        worksheet.write(0,icol+2, "".join(("Modèle de remplacement ",str(icol+1))), format_header)
        try:
            if producto["MasterData"]["BrandName"] != None:
                worksheet.write(1,icol+2, producto["MasterData"]["BrandName"], format_regular)
            else:
                worksheet.write(1,icol+2, "", format_NA)
        except:
            worksheet.write(1,icol+2, "", format_NA)
        
        try:
            if producto["MasterData"]["ProductName"] != None:
                worksheet.write(2,icol+2, producto["MasterData"]["ProductName"], format_regular)
            else:
                worksheet.write(2,icol+2, "", format_NA)    
        except:
            worksheet.write(2,icol+2, "", format_NA)

        for k in range(num_feature):
            try:
                if producto["FeatureData"][k]["FeatureValue"] != None and producto["FeatureData"][k]["FeatureValue"] != "N/A":
                    worksheet.write(3 + k, icol +2, producto["FeatureData"][k]["FeatureValue"], format_regular)
                else:
                    worksheet.write(3 + k, icol +2, "", format_NA)                  
            except:
                worksheet.write(3 + k, icol +2, "", format_NA)                  

        try:
            if producto["MarketData"]["Price"] != None:
                worksheet.write(num_feature,icol +2, producto["MarketData"]["Price"], format_regular)
            else:
                worksheet.write(num_feature,icol +2, "", format_NA)    
        except:
            worksheet.write(num_feature,icol +2, "", format_NA)

        #Precio promedio de modelos equivalentes
        try:
            n_offer = 0
            suma_oferta = 0
            for oferta in producto["MarketData"]["Channels"]["ChannelData"]:
                if oferta["Price"] != None:
                    suma_oferta += float(oferta["Price"])
                    n_offer += 1
            if n_offer != 0:
                worksheet.write(num_feature + 1,icol +2, str(suma_oferta/n_offer), format_regular)
            else:
                worksheet.write(num_feature + 1,icol +2, "", format_NA)
        except:
            worksheet.write(num_feature + 1,icol +2, "", format_NA)

        try: 
            if producto["MarketData"]["HistoricalPrice"]["Period"]["Year"] == None:
                worksheet.write(num_feature + 2,icol +2, "", format_NA)
            else:
                if producto["MarketData"]["HistoricalPrice"]["Period"]["Month"] == None:
                    producto["MarketData"]["HistoricalPrice"]["Period"]["Month"] = ""
                    fecha_antig = " ".join([producto["MarketData"]["HistoricalPrice"]["Period"]["Month"], producto["MarketData"]["HistoricalPrice"]["Period"]["Year"]])
                    worksheet.write(num_feature + 2,icol +2, fecha_antig, format_regular)
        except:
            worksheet.write(num_feature + 2,icol +2, "", format_NA)                

        worksheet.write(num_feature + 3,icol +2, "", format_NA)

        try:
            if producto["MarketData"]["HistoricalPrice"]["Price"] != None:
                worksheet.write(num_feature + 4,icol +2, producto["MarketData"]["HistoricalPrice"]["Price"], format_regular)
            else:
                worksheet.write(num_feature + 4,icol +2, "", format_NA)    
        except:
            worksheet.write(num_feature + 4,icol +2, "", format_NA)      

        icol+=1


    # Ancho de columna (todos los productos)
    worksheet.set_column(1, icol + 2, 25)

    # FIN
    workbook.close()

    if EXPORT_DATA_TO_EXTERNAL_HOST:
        xlsx_bytes = output.getvalue()
        return xlsx_bytes

    return None


def xlsx_lave_linge(req_xlsx_gen):
    xlsx_base(req_xlsx_gen)


def xlsx_lave_vaisselle(req_xlsx_gen):
    xlsx_base(req_xlsx_gen)


def xlsx_projecteurs(req_xlsx_gen):
    xlsx_base(req_xlsx_gen)


def xlsx_aspirateurs(req_xlsx_gen):
    xlsx_base(req_xlsx_gen)


def xlsx_mini_fours(req_xlsx_gen):
    xlsx_base(req_xlsx_gen)


def xlsx_kits_oreillette(req_xlsx_gen):
    xlsx_base(req_xlsx_gen)


def xlsx_casques(req_xlsx_gen):
    xlsx_base(req_xlsx_gen)


def xlsx_hottes(req_xlsx_gen):
    xlsx_base(req_xlsx_gen)


def xlsx_camescopes(req_xlsx_gen):
    xlsx_base(req_xlsx_gen)


def xlsx_moniteurs(req_xlsx_gen):
    xlsx_base(req_xlsx_gen)


def xlsx_consoles_de_jeu(req_xlsx_gen):
    xlsx_base(req_xlsx_gen)


def xlsx_robots(req_xlsx_gen):
    xlsx_base(req_xlsx_gen)


def xlsx_tablette(req_xlsx_gen):
    xlsx_base(req_xlsx_gen)


def xlsx_lecteur_dvd(req_xlsx_gen):
    xlsx_base(req_xlsx_gen)


def xlsx_plaques_de_cuisson(req_xlsx_gen):
    xlsx_base(req_xlsx_gen)


def xlsx_radio_reveil(req_xlsx_gen):
    xlsx_base(req_xlsx_gen)


def xlsx_seche_linge(req_xlsx_gen):
    xlsx_base(req_xlsx_gen)
