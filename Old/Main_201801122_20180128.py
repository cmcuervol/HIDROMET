#!/usr/bin/env python
# encoding: utf-8

import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from   pyPdf import PdfFileWriter, PdfFileReader
from   reportlab.pdfgen import canvas
from   StringIO import StringIO
import scipy.ndimage
from   reportlab.pdfbase import pdfmetrics
from   reportlab.pdfbase.ttfonts import TTFont
import locale
from   reportlab.lib.pagesizes import landscape, A4, LETTER, A0, A1, A2, A3, A5, inch
from   reportlab.lib.styles import ParagraphStyle
from   reportlab.lib.enums import TA_JUSTIFY
from   reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from   reportlab.lib import colors

def make_header(canva, size_x, size_y, dx, dy, RGB1, RGB2, path_logo, title_pdf, str_week):
    '''
    Esta funcion crea el encabezado con el titulo del reporte con los logos
    '''
    norm_RGB = np.array(RGB1)/255.
    canva.setFillColorRGB(norm_RGB[0], norm_RGB[1], norm_RGB[2])
    canva.rect(size_x - dx, size_y - dy+40., dx, dy, fill = True, stroke = False)


    norm_RGB = np.array(RGB2)/255.
    canva.setFillColorRGB(norm_RGB[0], norm_RGB[1], norm_RGB[2])
    canva.rect(size_x - dx, size_y - dy, dx, dy-140., fill = True, stroke = False)

    canva.setFillColorRGB(1,1,1)
    canva.setFont("Avenir_blk", 34)
    canva.drawString(size_x - dx + 300, size_y - dy + 100., title_pdf)

    canva.setFillColorRGB(1,1,1)
    canva.setFont("Avenir_blk", 22)
    canva.drawString(size_x - 650, size_y - dy+15., str_week)

    canva.drawImage(path_logo+'Informe/logos/Franja_logos_03.png', \
                    size_x - dx, size_y - dy, dy+70., dy, mask = 'auto')

def make_footer(canva, size_x, size_y, dx, dy, RGB, path_logo):
    norm_RGB = np.array(RGB)/255.
    canva.setFillColorRGB(norm_RGB[0], norm_RGB[1], norm_RGB[2])
    canva.rect(size_x, size_y, dx, dy, fill = 1)
    canva.drawImage(path_logo+'Informe/logos/Franja_logos_franja_de_logos.png', \
                    416, 0, 850, 120, mask = 'auto')

#-----------------------------------------------------------------------------------------------
# Se define la fechas para la cual se corre el informe
#-----------------------------------------------------------------------------------------------
str_semana = 'Semana: 22 de enero hasta 28 de enero de 2018'

#-----------------------------------------------------------------------------------------------
# Parametros necesarios para hacer el reporte
#-----------------------------------------------------------------------------------------------
path_elem = '/home/atlas/informe_hidromet/20180122_20180128/'
path_reps = '/home/atlas/informe_hidromet/20180122_20180128/Informe/'

# Se define el tipo de letra con el que se va a trabjar
# en este caso sera Avenir.
barcode_font = path_reps+'avenir/AvenirLTStd-Roman.ttf'
pdfmetrics.registerFont(TTFont("Avenir", barcode_font))
barcode_font_blk = path_reps+'avenir/AvenirLTStd-Black.ttf'
pdfmetrics.registerFont(TTFont("Avenir_blk", barcode_font_blk))
# Se define el RGB de los colores a utilizar
color_RGB1 = [34, 71, 94] # Azul franja principal superior
color_RGB2 = [9, 32, 46] # Azul del banner de los logos y logos siata
color_RGB3 = [31, 115, 116] # Banda pequeña azul claro
color_RGB4 = [55, 123, 148]

gris70 =     (112/255., 111/255., 111/255.)
ColorInfo1 = (82 /255., 183/255.,196/255.)
ColorInfo2 = (55 /255., 123/255.,148/255.)
ColorInfo3 = (43 /255., 72/255.,105/255.)
ColorInfo4 = (32 /255., 34/255., 72/255.)
ColorInfo5 = (34 /255., 71/255., 94/255.)
ColorInfo6 = (31 /255., 115/255.,116/255.)
ColorInfo7 = (39 /255., 165/255.,132/255.)
ColorInfo8 = (139/255., 187/255.,116/255.)
ColorInfo9 = (200/255., 209/255., 93/255.)
ColorInfo10 =(249/255., 230/255., 57/255.)

# ----------------------------------------------------------------------------------------------
# Se establecen las medidas
sizey, sizex = A2
print 'El ancho del canvas', sizex
print 'El alto del canvas', sizey


style1 = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Avenir', \
                        fontSize=20, leading = 24)

# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# Sección precipitación
#-----------------------------------------------------------------------------------------------
pdf_rep_PPT = canvas.Canvas(path_reps+'Precipitacion.pdf')
pdf_rep_PPT.setPageSize((sizex, sizey))
title_pdf_PPT = u'INFORME HIDROMETEOROLÓGICO SEMANAL - Precipitación '
make_header(pdf_rep_PPT, sizex, sizey, sizex, 180. , color_RGB2, color_RGB3, path_elem,\
           title_pdf_PPT, str_semana)
make_footer(pdf_rep_PPT, 0, 0, sizex, 120. , color_RGB2, path_elem)

# contenido panel 1
pdf_rep_PPT.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
pdf_rep_PPT.rect(10., 150., 700., 815., fill = False, stroke = True)
pdf_rep_PPT.rect(10., 940., 500., 50., fill = True, stroke = True)
pdf_rep_PPT.setFillColorRGB(1,1,1)
pdf_rep_PPT.setFont("Avenir", 24)
pdf_rep_PPT.drawString(25., 955.,'Acumulados semanales de precipitación')

pdf_rep_PPT.drawImage(path_elem+'Precipitacion/SemanalCoberta.png', \
                25., 477., 450., 450., mask = 'auto')
pdf_rep_PPT.drawImage(path_elem+'Precipitacion/SemanalAMVA.png', \
                475., 700., 220., 220., mask = 'auto')


pdf_rep_PPT.drawImage(path_elem+'Precipitacion/pluviometros.png', \
                25., 160., 320., 250., mask = 'auto')
# par1 = Paragraph (u'Imagen de reflectividad del radar a las 03:21 del 7 de septiembre, \
#                     correspondiente al evento de precipitación con número de informe \
#                     1203, en el cual se observa que durante el evento las precipitaciones \
#                     alcanzaron a cubrir por completo el Valle de Aburrá con intensidades \
#                     çpredominantemente bajas, que se prolongaron durante la noche \
#                     y madrugada. Este evento de precipitación fue uno de los más \
#                     relevantes de la semana.', style1)
# par1.wrap(515, 890)
# par1.drawOn(pdf_rep_PPT, 25., 165)


# contenido panel 2
pdf_rep_PPT.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
pdf_rep_PPT.rect(720., 150., 950., 815., fill = False, stroke = True)
pdf_rep_PPT.rect(720., 940., 500., 50., fill = True, stroke = True)
pdf_rep_PPT.setFillColorRGB(1,1,1)
pdf_rep_PPT.setFont("Avenir", 24)
pdf_rep_PPT.drawString(835., 955., 'Evento de precipitación 28 enero')


pdf_rep_PPT.drawImage(path_elem+'Precipitacion/Evento.png', \
                730., 620., 300., 300., mask = 'auto')



pdf_rep_PPT.drawImage(path_elem+'Precipitacion/grafica_barras_disdro.png', \
                1050., 380., 600., 300., mask = 'auto')



par1 = Paragraph (u'Histograma de clasificación de lluvia sobre el disdrómetro \
                    ubicado en la I.E. Manuel José Caicedo. Cada barra del gráfico \
                    corresponde a un minuto de medición del disdrómetro y el color \
                    especifica la partícula de mayor tamaño registrada en dicho \
                    minuto, donde llovizna es la partícula de menor tamaño y el \
                    granizo es el de mayor tamaño en la escala de clasificación.', style1)
par1.wrap(250,500 )
par1.drawOn(pdf_rep_PPT, 730, 200)


pdf_rep_PPT.drawImage(path_elem+'Precipitacion/sabias_que_es_un_disdro.png', \
                1050., 160., 600., 200., mask = 'auto')

pdf_rep_PPT.save()
#



# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# Sección Rayos
#-----------------------------------------------------------------------------------------------
pdf_rep_RAYOS = canvas.Canvas(path_reps+'Rayos.pdf')
pdf_rep_RAYOS.setPageSize((sizex, sizey))

# Dibujamos el rectangulo del encabezado
title_pdf_RAYOS = u'INFORME HIDROMETEOROLÓGICO SEMANAL - Descargas eléctricas'
make_header(pdf_rep_RAYOS, sizex, sizey, sizex, 180. , color_RGB2, color_RGB3,path_elem,\
           title_pdf_RAYOS, str_semana)
make_footer(pdf_rep_RAYOS, 0, 0, sizex, 120. , color_RGB2, path_elem)

# contenido panel 1
pdf_rep_RAYOS.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
pdf_rep_RAYOS.rect(10., 580., 1660., 390., fill = False, stroke = True)
pdf_rep_RAYOS.rect(10., 940., 500., 50., fill = True, stroke = True)
pdf_rep_RAYOS.setFillColorRGB(1,1,1)
pdf_rep_RAYOS.setFont("Avenir", 24)
pdf_rep_RAYOS.drawString(25., 955., 'Análisis de descargas eléctricas')


pdf_rep_RAYOS.drawImage(path_elem+'Rayos/HexbinMap_Radar_20180128.png', \
                25., 590., 700., 350., mask = 'auto')

par1 = Paragraph (u'En la figura se muestra el mapa de densidad de rayos tipo nube-tierra \
                    y un zoom del Valle de Aburrá donde se muestra el conteo al \
                    interior de éste. La distribución espacial de la densidad de \
                    los rayos en general muestra un patrón coherente con la localización \
                    de los sistemas de lluvia con mayor intensidad, al interior \
                    del Valle de Aburrá; no se presentó una cantidad considerable \
                    de rayos. La máxima densidad se ubicó entre los corregimientos \
                    de Palmitas y San Cristobal.', style1)
par1.wrap(330., 350.)
par1.drawOn(pdf_rep_RAYOS, 730, 600)

pdf_rep_RAYOS.drawImage(path_elem+'Rayos/20180128_RGB_Paleta.png', \
                1080., 590., 320., 350., mask = 'auto')

par1 = Paragraph (u'En la tabla se muestra el conteo de rayos tipo nube-tierra que \
                    sucedieron en cada día de la semana y en cada uno de \
                    los municipios del Área Metropolitana. En la semana \
                    en total se presentaron 18 rayos al interior del Valle, la mayoría \
                    estuvieron asociados a un evento en las horas de la madrugada \
                    el domingo 28.', style1)
par1.wrap(255., 350.)
par1.drawOn(pdf_rep_RAYOS, 1400, 600)


pdf_rep_RAYOS.drawImage(path_elem+'Rayos/SabiasRayos.png', \
                850., 160., 800., 380., mask = 'auto')



# contenido panel 2
pdf_rep_RAYOS.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
pdf_rep_RAYOS.rect(10., 150., 820., 395., fill = False, stroke = True)
pdf_rep_RAYOS.rect(10., 520., 500., 50., fill = True, stroke = True)
pdf_rep_RAYOS.setFillColorRGB(1,1,1)
pdf_rep_RAYOS.setFont("Avenir", 24)
pdf_rep_RAYOS.drawString(25., 535.,'GLM')


pdf_rep_RAYOS.save()
#
#






# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# Sección Satelital
#-----------------------------------------------------------------------------------------------
pdf_rep_SAT = canvas.Canvas(path_reps+'Satelital.pdf')
pdf_rep_SAT.setPageSize((sizex, sizey))
title_pdf_SAT = u'INFORME HIDROMETEOROLÓGICO SEMANAL - Información satélital'
make_header(pdf_rep_SAT, sizex, sizey, sizex, 180. , color_RGB2, color_RGB3, path_elem,\
           title_pdf_SAT, str_semana)
make_footer(pdf_rep_SAT, 0, 0, sizex, 120. , color_RGB2, path_elem)

# contenido panel 1
pdf_rep_SAT.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
pdf_rep_SAT.rect(10., 150., 830., 815., fill = False, stroke = True)
pdf_rep_SAT.rect(10., 940., 300., 50., fill = True, stroke = True)
pdf_rep_SAT.setFillColorRGB(1,1,1)
pdf_rep_SAT.setFont("Avenir", 24)
pdf_rep_SAT.drawString(25., 955.,'GOES')


pdf_rep_SAT.drawImage(path_elem+'Satelital/CH02.png', \
                90., 625., 300., 300., mask = 'auto')
pdf_rep_SAT.drawImage(path_elem+'Satelital/CH14.png', \
                470., 625., 300., 300., mask = 'auto')
pdf_rep_SAT.drawImage(path_elem+'Satelital/CH09.png', \
                90., 300., 300., 300., mask = 'auto')
pdf_rep_SAT.drawImage(path_elem+'Satelital/CH10.png', \
                470., 300., 300., 300., mask = 'auto')


par1 = Paragraph (u'El alto influjo de humedad proveniente del Pacifico favorecio \
                    la ocurrencia de lluvias en el departamento de antioquia durante \
                    la última semana de mes de enero. Las imágenes de los canales \
                    visible, infrarrojo y vapor de agua, destacan la presencia de \
                    nubes de gran desarrollo vertical sobre el departamento.', style1)
par1.wrap(670., 100.)
par1.drawOn(pdf_rep_SAT, 90, 160)



# contenido panel 2
pdf_rep_SAT.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
pdf_rep_SAT.rect(850., 150., 820., 815., fill = False, stroke = True)
pdf_rep_SAT.rect(850., 940., 300., 50., fill = True, stroke = True)
pdf_rep_SAT.setFillColorRGB(1,1,1)
pdf_rep_SAT.setFont("Avenir", 24)
pdf_rep_SAT.drawString(865., 955., 'GPM')

par1 = Paragraph (u'Sección Carlos Hoyos', style1)
par1.wrap(390, 890)
par1.drawOn(pdf_rep_SAT, 1200, 585)


pdf_rep_SAT.save()
#



# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# Sección vientos
#-----------------------------------------------------------------------------------------------
pdf_rep_WIND = canvas.Canvas(path_reps+'Vientos.pdf')
pdf_rep_WIND.setPageSize((sizex, sizey))

# Dibujamos el rectangulo del encabezado
title_pdf_WIND = u'INFORME HIDROMETEOROLÓGICO SEMANAL - Vientos'
make_header(pdf_rep_WIND, sizex, sizey, sizex, 180. , color_RGB2, color_RGB3,path_elem,\
           title_pdf_WIND, str_semana)
make_footer(pdf_rep_WIND, 0, 0, sizex, 120. , color_RGB2, path_elem)

# contenido panel 1
pdf_rep_WIND.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
pdf_rep_WIND.rect(10., 150., 1660., 800., fill = False, stroke = True)
pdf_rep_WIND.rect(10., 900., 500., 50., fill = True, stroke = True)
pdf_rep_WIND.setFillColorRGB(1,1,1)
pdf_rep_WIND.setFont("Avenir", 24)
pdf_rep_WIND.drawString(25., 915.,'Análisis de vientos')
#

pdf_rep_WIND.drawImage(path_elem+'Viento/RWP_DirunalCycle.png', \
                25., 400., 800., 550., mask = 'auto')

pdf_rep_WIND.drawImage(path_elem+'Viento/maximo_viento_temperatura_2018-01-22_2018-01-28.png', \
                850., 580., 350., 350., mask = 'auto')
pdf_rep_WIND.drawImage(path_elem+'Viento/promedio_viento_temperatura_2018-01-22_2018-01-28.png', \
                1250., 580., 350., 350., mask = 'auto')
pdf_rep_WIND.drawImage(path_elem+'Viento/Estacion_205WR.png', \
                850., 200., 350., 350., mask = 'auto')
pdf_rep_WIND.drawImage(path_elem+'Viento/Estacion_201WR.png', \
                1250., 200., 350., 350., mask = 'auto')


pdf_rep_WIND.save()
#
#

# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# Sección Térmica
#-----------------------------------------------------------------------------------------------
pdf_rep_HEAT = canvas.Canvas(path_reps+'Termico.pdf')
pdf_rep_HEAT.setPageSize((sizex, sizey))
title_pdf_HEAT = u'INFORME HIDROMETEOROLÓGICO SEMANAL - Variables térmicas e incendios forestales'
make_header(pdf_rep_HEAT, sizex, sizey, sizex, 180. , color_RGB2, color_RGB3, path_elem,\
           title_pdf_HEAT, str_semana)
make_footer(pdf_rep_HEAT, 0, 0, sizex, 120. , color_RGB2, path_elem)

# contenido panel 1
pdf_rep_HEAT.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
pdf_rep_HEAT.rect(10., 140., 1000., 825., fill = False, stroke = True)
pdf_rep_HEAT.rect(10., 940., 700., 50., fill = True, stroke = True)
pdf_rep_HEAT.setFillColorRGB(1,1,1)
pdf_rep_HEAT.setFont("Avenir", 24)
pdf_rep_HEAT.drawString(25., 955.,'Condiciones de temperatura, humedad y radiación solar')


pdf_rep_HEAT.drawImage(path_elem+'Incendios/Resumen_T_H_Semanal.png', \
                25., 580., 700., 350., mask = 'auto')



par1 = Paragraph (u'Los mínimos de temperatura y la humedad relativa de todas las \
                    estaciones estuvieron dentro de los valores normales para el \
                    mes de enero. Por su parte, los valores máximos de la semana \
                    fueron ligeramente más altos de los valores de referencia.', style1)
par1.wrap(250, 300)
par1.drawOn(pdf_rep_HEAT, 750., 600)


pdf_rep_HEAT.drawImage(path_elem+'Incendios/Heatmap_Radiacion.png', \
                25., 250., 450., 300., mask = 'auto')


pdf_rep_HEAT.drawImage(path_elem+'Incendios/Horas_alta_radiacion.png', \
                500., 225., 450., 350., mask = 'auto')

par1 = Paragraph (u'Durante la semana, la radiación percibida en superficie tuvo \
                    una alta variación. Se presentaron 15 horas con valores altos, \
                    siendo martes, miércoles y sábado los días con radiación más alta. \
                    El martes la cantidad de energía percibida en superficie en \
                    el piranómetro de Torre SIATA fue de 19.3 MJ/m2, el cual es \
                    un valor que no difiere significativamente de los valores medios \
                    en el lugar.', style1)
par1.wrap(955, 100)
par1.drawOn(pdf_rep_HEAT, 25., 142)




# contenido panel 2
pdf_rep_HEAT.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
pdf_rep_HEAT.rect(1020., 140., 650., 825., fill = False, stroke = True)
pdf_rep_HEAT.rect(1020., 940., 500., 50., fill = True, stroke = True)
pdf_rep_HEAT.setFillColorRGB(1,1,1)
pdf_rep_HEAT.setFont("Avenir", 24)
pdf_rep_HEAT.drawString(1035., 955., 'Susceptibilidad a incendios forestales')

pdf_rep_HEAT.drawImage(path_elem+'Incendios/Mapa_D_2018-01-26.png', \
                1025., 320., 600., 620., mask = 'auto')

par1 = Paragraph (u'El nivel de susceptibilidad se estima a partir de información \
                    estática como la cobertura del suelo y  variables dinámicas \
                    como la temperatura, la humedad en el suelo y la distribución \
                    espacial de la lluvia precedente. La información de este modelo \
                    fue validada con incendios reportados por los cuerpos de bomberos \
                    de los municipios del Valle de Aburrá entre los años 2015 y \
                    2017. En el mapa se indica la ubicación de los incendios reportados.', style1)
par1.wrap(620, 150)
par1.drawOn(pdf_rep_HEAT, 1025., 142)

pdf_rep_HEAT.save()
#



# ---------------------------------------------------------------------------------------------
# Se hace el merge de los diferentes reportes generados
# ---------------------------------------------------------------------------------------------


file1 = file (path_reps+'Precipitacion.pdf', 'rb')
file2 = file (path_reps+'Rayos.pdf',         'rb')
file3 = file (path_reps+'Satelital.pdf',     'rb')
file4 = file (path_reps+'Vientos.pdf',       'rb')
file5 = file (path_reps+'Termico.pdf',       'rb')
# file6 = file (path_reps+'incendios.pdf', 'rb')

page1 = PdfFileReader (file1).getPage (0)
page2 = PdfFileReader (file2).getPage (0)
page3 = PdfFileReader (file3).getPage (0)
page4 = PdfFileReader (file4).getPage (0)
page5 = PdfFileReader (file5).getPage (0)
# page6 = PdfFileReader (file6).getPage (0)

output = PdfFileWriter()
output.addPage(page1)
output.addPage(page2)
output.addPage(page3)
output.addPage(page4)
output.addPage(page5)
# output.addPage(page6)
output.write(file(path_reps+'HIDROMET_20180122_20180128.pdf','w'))
