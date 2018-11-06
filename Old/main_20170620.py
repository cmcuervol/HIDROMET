#!/usr/bin/env python
# encoding: utf-8

import numpy as np
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

    canva.drawImage(path_logo+'informe/logos/Franja_logos_03.png', \
                    size_x - dx, size_y - dy, dy+70., dy, mask = 'auto')

def make_footer(canva, size_x, size_y, dx, dy, RGB, path_logo):
    norm_RGB = np.array(RGB)/255.
    canva.setFillColorRGB(norm_RGB[0], norm_RGB[1], norm_RGB[2])
    canva.rect(size_x, size_y, dx, dy, fill = 1)
    canva.drawImage(path_logo+'informe/logos/Franja_logos_franja_de_logos.png', \
                    416, 0, 850, 120, mask = 'auto')

#-----------------------------------------------------------------------------------------------
# Se define la fechas para la cual se corre el informe
#-----------------------------------------------------------------------------------------------
str_semana = 'Semana: 12 de Junio de 2017 hasta 18 de Junio de 2017'

#-----------------------------------------------------------------------------------------------
# Parametros necesarios para hacer el reporte
#-----------------------------------------------------------------------------------------------
path_elem = '/home/atlas/informe_hidromet/20170620/'

# Se define el tipo de letra con el que se va a trabjar
# en este caso sera Avenir.
barcode_font = path_elem+'informe/avenir/AvenirLTStd-Roman.ttf'
pdfmetrics.registerFont(TTFont("Avenir", barcode_font))
barcode_font_blk = path_elem+'informe/avenir/AvenirLTStd-Black.ttf'
pdfmetrics.registerFont(TTFont("Avenir_blk", barcode_font_blk))
# Se define el RGB de los colores a utilizar
color_RGB1 = [34, 71, 94] # Azul franja principal superior
color_RGB2 = [9, 32, 46] # Azul del banner de los logos y logos siata
color_RGB3 = [31, 115, 116] # Banda pequeña azul claro
color_RGB4 = [55, 123, 148]
gris70 = (112/255., 111/255., 111/255.)
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
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# Se genera primer reporte en pdf
#-----------------------------------------------------------------------------------------------

pdf_rep1 = canvas.Canvas(path_elem+'informe/precipitacion.pdf')
pdf_rep1.setPageSize((sizex, sizey))
title_pdf1 = u'INFORME HIDROMETEOROLÓGICO SEMANAL - Precipitación '
make_header(pdf_rep1, sizex, sizey, sizex, 180. , color_RGB2, color_RGB3, path_elem,\
           title_pdf1, str_semana)
make_footer(pdf_rep1, 0, 0, sizex, 120. , color_RGB2, path_elem)

# contenido panel 1
pdf_rep1.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
pdf_rep1.rect(10., 150., 545., 815., fill = False, stroke = True)
pdf_rep1.rect(10., 940., 470., 50., fill = True, stroke = True)
pdf_rep1.setFillColorRGB(1,1,1)
pdf_rep1.setFont("Avenir", 24)
pdf_rep1.drawString(25., 955.,'Comparación con acumulados históricos')
pdf_rep1.drawImage(path_elem+'ppt_epm/ComparaPercentil_2017_2701035.png', \
                25.,  700., 240., 200., mask = 'auto')
pdf_rep1.drawImage(path_elem+'ppt_epm/ComparaPercentil_2017_2701057.png', \
                300., 700., 240., 200., mask = 'auto')
pdf_rep1.drawImage(path_elem+'ppt_epm/ComparaPercentil_2017_2701038.png', \
                25.,  450., 240., 200., mask = 'auto')
pdf_rep1.drawImage(path_elem+'ppt_epm/ComparaPercentil_2017_2701517.png', \
                300., 450., 240., 200., mask = 'auto')
pdf_rep1.setFillColorRGB(0,0,0)
style1 = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Avenir', fontSize=20,\
                       leading = 24)
par1 = Paragraph (u'Se comparan los acumulados de la red pluviométrica de EPM desde el 01 hasta \
                  el 19 de Junio de 2017 con la mediana de los acumulados históricos de Junio, \
                  con la intención de conocer como es su comportamiento. Hasta esta fecha, los \
                  acumualdos en la mayoría de las estaciones al interior del AMVA estan por \
                  debajo de las medianas históricas excepto en las estaciones Barbosa, que \
                  es igual a la mediana; Chorrilos y Villahermosa que está por encima \
                  de la mediana.', style1)
par1.wrap(500, 890)
par1.drawOn(pdf_rep1, 20, 180)


# contenido panel 2
pdf_rep1.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
pdf_rep1.rect(565., 575., 1100., 395., fill = False, stroke = True)
pdf_rep1.rect(565., 940., 737., 50., fill = True, stroke = True)
pdf_rep1.setFillColorRGB(1,1,1)
pdf_rep1.setFont("Avenir", 24)
pdf_rep1.drawString(580., 955., 'Mapa acumulado semanal de precipitación radar')
pdf_rep1.drawImage(path_elem+'ppt_rad/SemanalCoberta.png', \
                580., 590., 320., 340., mask = 'auto')
pdf_rep1.drawImage(path_elem+'ppt_rad/SemanalAMVA.png', \
                920., 590., 320., 340., mask = 'auto')
pdf_rep1.setFillColorRGB(0,0,0)
style1 = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Avenir', fontSize=20,\
                       leading = 24)
par1 = Paragraph (u'A escala regional, los acumulados semanales de precipitación presentan \
                  acumulados altos en oriente en la zona de los embalses de EPM e Isagen. \
                  Por su parte, a escala local en esta semana se presentan acumulados altos \
                  en las cuencas aferentes a las quebradas La Miel en el municipip de Caldas; \
                  las quebradas doña María y Alavista al occidente de la ciudad de \
                  Medellín. También es destacable los altos acumulados de precipitación \
                  sobre le municipio de principalmente sobre las cuencas de las quebradas \
                  Ovejas, Llano Chiquito, Santiago y Piedras Gordas.', style1)
par1.wrap(390, 890)
par1.drawOn(pdf_rep1, 1260, 580)

# contenido panel 3
data = [['Informe','Inicio','Acumulado','Municipio','Intensidad','Municipio'],
        [1138,'2017-06-11' ,64.01,u'Medellín',122.52,u'Medellín'],
        [1140,'2017-06-13' ,36.91,'Barbosa',81,'Barbosa'],
        [1141,'2017-06-14' ,58.42,u'Medellín',128.02,u'Medellín'],
        [1142,'2017-06-15' ,31.06,'Barbosa',88.39,'La Estrella'],
        [1144,'2017-06-16' ,95.7,u'Medellín',105.6,u'Medellín']]

t=Table(data,[1*inch,2*inch,1.5*inch,1.5*inch,1.5*inch,1.5*inch], 6*[0.4*inch])
pdf_rep1.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
pdf_rep1.rect(565., 150., 1105., 390., fill = False, stroke = True)
pdf_rep1.rect(565., 515., 737., 50., fill = True, stroke = True)
pdf_rep1.setFillColorRGB(1,1,1)
pdf_rep1.setFont("Avenir", 24)
pdf_rep1.drawString(580., 530., 'Resumen eventos de la semana')
pdf_rep1.drawImage(path_elem+'ppt_est/plot_torta.png', \
                1250, 160., 400., 340., mask = 'auto')
t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),\
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),\
                       ('ALIGN',(0,0),(-1,-1),'CENTER'),\
                       ('VALIGN',(0,0),(-1,-1),'MIDDLE'),\
                       ('FONTSIZE', (0, 0), (-1, 1), 18),\
                       ('BACKGROUND',(0,0),(-1,0),ColorInfo6),\
                       ('FONTSIZE', (0, 1), (-1, -1), 14),\
                       ('TEXTCOLOR',(0, 0),(-1,0),colors.white)\
                        ]))
t.wrapOn(pdf_rep1, 600, 890)
t.drawOn(pdf_rep1, 590., 320.)


par1 = Paragraph (u'Durante esta semana se registraron nueve eventos de precipitación \
                    que superaron 5 mm de acumulado. En la tabla se muestran \
                    los eventos más relevantes. En la gráfica de pastel se resume el porcentaje \
                    de los eventos que se encuentran en varios rangos de acumulados, es de resaltar \
                    que tres de estos eventos sueperaron el umbral de 45 mm ', style1)
par1.wrap(650, 870)
par1.drawOn(pdf_rep1, 590., 200.)
pdf_rep1.save()
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# Se genera segundo reporte en pdf
#-----------------------------------------------------------------------------------------------
pdf_rep2 = canvas.Canvas(path_elem+'informe/meteorologia.pdf')
pdf_rep2.setPageSize((sizex, sizey))

# Dibujamos el rectangulo del encabezado
title_pdf2 = u'INFORME HIDROMETEOROLÓGICO SEMANAL - Variables atmosféricas'
make_header(pdf_rep2, sizex, sizey, sizex, 180. , color_RGB2, color_RGB3,path_elem,\
           title_pdf2, str_semana)
make_footer(pdf_rep2, 0, 0, sizex, 120. , color_RGB2, path_elem)

# contenido panel 1
pdf_rep2.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
pdf_rep2.rect(10., 580., 1660., 390., fill = False, stroke = True)
pdf_rep2.rect(10., 940., 700., 50., fill = True, stroke = True)
pdf_rep2.setFillColorRGB(1,1,1)
pdf_rep2.setFont("Avenir", 24)
pdf_rep2.drawString(25., 955., 'Análisis de descargas eléctricas')
pdf_rep2.drawImage(path_elem+'descargas_elec/MapaScatter_201706120000.png', \
                780., 595., 360., 360., mask = 'auto')
pdf_rep2.drawImage(path_elem+'descargas_elec/BarrasTotal_201706120000.png', \
                1200., 595., 455., 360., mask = 'auto')
style1 = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Avenir', fontSize=20,\
                       leading = 24)
par1 = Paragraph (u'En resumen, en esta última semana se presentaron en total 665 descargas \
                  eléctricas tipo nube-tierra al interior del Valle de Aburrá. Cerca de la \
                  mitad de estas descargas (260) se presentaron en el municipio de Barbosa \
                  (ver figura_ la de totales de barras). A esta cifra le siguen con mayor \
                  número de descargas el municipio de  Medellín, en donde se presentaron en \
                  total 193. En la semana se presentó actividad de descargas eléctricas \
                  significativas el día martes 13, en donde en Barbosa el acumulado ascendió \
                  a 237; y en el evento de los días 16 y 17, en donde en total se presentaron \
                  137 descargas en Medellín. ', style1)
par1.wrap(660., 890.)
par1.drawOn(pdf_rep2, 40, 700)

# contenido panel 2
pdf_rep2.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
pdf_rep2.rect(10., 150., 1660., 395., fill = False, stroke = True)
pdf_rep2.rect(10., 520., 700., 50., fill = True, stroke = True)
pdf_rep2.setFillColorRGB(1,1,1)
pdf_rep2.setFont("Avenir", 24)
pdf_rep2.drawString(25., 535.,'Análisis de estaciones de vientos y temperatura')
pdf_rep2.drawImage(path_elem+'vientos_temp/promedio_viento_temperatura.png', \
                25., 165., 390., 350., mask = 'auto')

pdf_rep2.setFillColorRGB(0,0,0)
par2 = Paragraph (u'En el mapa de la izqquierda es posible observar que la dirección promedio \
                  del viento siguió el eje del Valle hasta confluir en el centro del mismo \
                  con velocidades promedio \
                  que varian entre los 1 - 4 km/h. Las estaciones ubicadas en las laderas \
                  muestran direcciones también hacia el centro del Valle donde la mayor \
                  velocidad promedio la registró la estación de Santa Elena con un valor de \
                  10 km/h. Por su parte las temperaturas promedio registaradas por las \
                  estaciones en la base del Valle están alrededor de los 20ºC y la menor \
                  temperatura promedio fue registrada por la estación Santa Elena (11ºC).'\
                  , style1)
par2.wrap(400, 890)
par2.drawOn(pdf_rep2, 430., 160)

pdf_rep2.drawImage(path_elem+'vientos_temp/maximo_viento_temperatura.png', \
                850., 165., 390., 350., mask = 'auto')
pdf_rep2.setFillColorRGB(0,0,0)
par3 = Paragraph (u'La dirección de los vientos máximos registrados durante la semana \
                  van de norte a sur siguiendo el eje del Valle, \
                  es destacable la magnitud máxima registrada \
                  por la estación Santa Helena (35 km/h). Por su parte, las temperaturas \
                  máximas registradas en la base del Valle estuvieron entre los 26 y \
                  28ºC, mientras que las laderas variaron entre 16 y 26 ºC. El \
                  máximo registrado por la estación Santa Elena fue de 16ºC ', style1)
par3.wrap(360, 890)
par3.drawOn(pdf_rep2, 1270., 200)

pdf_rep2.save()

# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# Se genera tercer reporte en pdf
#-----------------------------------------------------------------------------------------------
pdf_rep3 = canvas.Canvas(path_elem+'informe/sensores_remotos.pdf')
pdf_rep3.setPageSize((sizex, sizey))

# Dibujamos el rectangulo del encabezado
title_pdf2 = u'INFORME HIDROMETEOROLÓGICO SEMANAL - Información Satélital'
make_header(pdf_rep3, sizex, sizey, sizex, 180. , color_RGB2, color_RGB3,path_elem,\
           title_pdf2, str_semana)
make_footer(pdf_rep3, 0, 0, sizex, 120. , color_RGB2, path_elem)

# contenido panel 1
pdf_rep3.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
pdf_rep3.rect(10., 150., 1660., 800., fill = False, stroke = True)
pdf_rep3.rect(10., 900., 700., 50., fill = True, stroke = True)
pdf_rep3.setFillColorRGB(1,1,1)
pdf_rep3.setFont("Avenir", 24)
pdf_rep3.drawString(25., 915.,'Análisis información GOES')
pdf_rep3.drawImage(path_elem+'satelital_goes/2017.168.0115.png', \
                15., 540., 500., 350., mask = 'auto')
pdf_rep3.drawImage(path_elem+'satelital_goes/2017.168.0815.png', \
                500., 540., 500., 350., mask = 'auto')
pdf_rep3.drawImage(path_elem+'satelital_goes/2017.168.1415.png', \
                15., 150., 500., 350., mask = 'auto')
pdf_rep3.drawImage(path_elem+'satelital_goes/2017.167.2015.png', \
                500., 150., 500., 350., mask = 'auto')

style1 = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Avenir', fontSize=20,\
                       leading = 24)
par3 = Paragraph (u'En horas previas al evento ocurrido sobre el Valle de aburra \
                    el día 16 de Junio de 2017, se observan dos sistemas convectivos \
                    de mesoescala asociados a dos zonas de baja presión, una de \
                    ellas sobre centro América y el Caribe, y la otra sobre el \
                    Atlántico occidental, entre los 0 y 5° norte. El primero exhibe \
                    un desplazamiento lento hacia el noreste y el segundo, asociado \
                    a una onda tropical, se propaga hacia el continente con más \
                    celeridad. Ambos sistemas presentan un proceso de expansión \
                    y se observa la constante formación de asociados a circulaciones \
                    locales y a interacciones ortográficas. La mayor extensión de \
                    los cúmulos formados en territorio colombiano se presentó entre \
                    la media noche y horas de la madrugada. La temperatura de brillo \
                    mínima asociada a los desarrollos verticales fue en promedio \
                    -80 °C, y en general se observo, para el dominio que se presenta \
                    en las figuras, y para todo el periodo durante el cual se \
                    presentaron precipitaciones en el Valle de Aburrá, coberturas \
                    nubosos con temperaturas de brillo inferiores a -30 °C.', style1)
par3.wrap(600, 890)
par3.drawOn(pdf_rep3, 1000., 300)

pdf_rep3.save()


# ----------------------------------------------------------------------------------------------
# Se genera reporte pronóstico en pdf
#-----------------------------------------------------------------------------------------------
pdf_rep4 = canvas.Canvas(path_elem+'informe/pronostico.pdf')
pdf_rep4.setPageSize((sizex, sizey))

# Dibujamos el rectangulo del encabezado
title_pdf4 = u'INFORME HIDROMETEOROLÓGICO SEMANAL - Pronóstico Meteorológico'
make_header(pdf_rep4, sizex, sizey, sizex, 180. , color_RGB2, color_RGB3,path_elem,\
           title_pdf4, str_semana)
make_footer(pdf_rep4, 0, 0, sizex, 120. , color_RGB2, path_elem)

# contenido panel 1
pdf_rep4.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
pdf_rep4.rect(10., 150., 820., 805., fill = False, stroke = True)
pdf_rep4.rect(10., 930., 700., 50., fill = True, stroke = True)
pdf_rep4.setFillColorRGB(1,1,1)
pdf_rep4.setFont("Avenir", 24)
pdf_rep4.drawString(25., 955., 'Pronóstico de Temperatura')

pdf_rep4.setFillColorRGB(0,0,0)
style1 = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Avenir', fontSize=20,\
                       leading = 24)
par4 = Paragraph (u'El mapa representa la diferencia del promedio de temperatura observado y \
                    pronosticado en cada una de las estaciones de la red de monitoreo meteorológico, \
                    en general se observa que las diferencias no exceden 0.5 C, las mayores diferencias \
                    se observan en las estaciones ubicadas en las laderas del valle de Aburrá (ver serie derecha), \
                    lo cual es contrastado con los puntos ubicados en la base del valle donde las diferencias \
                    de temperaturas son mínimas (ver serie izquierda). ',style1)

par4.wrap(330, 890)
par4.drawOn(pdf_rep4, 480., 515)

pdf_rep4.drawImage(path_elem+'pronostico_wrf/mapa_temp.png', \
                25., 475., 450., 450., mask = 'auto')

pdf_rep4.drawImage(path_elem+'pronostico_wrf/tmp_mayo_82.png', \
                25., 210., 380., 220., mask = 'auto')

pdf_rep4.drawImage(path_elem+'pronostico_wrf/tmp_mayo_59.png', \
                425., 210., 380., 220., mask = 'auto')




# contenido panel 2
pdf_rep4.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
pdf_rep4.rect(840., 150., 820., 805., fill = False, stroke = True)
pdf_rep4.rect(840., 930., 700., 50., fill = True, stroke = True)
pdf_rep4.setFillColorRGB(1,1,1)
pdf_rep4.setFont("Avenir", 24)
pdf_rep4.drawString(875., 955.,'Pronóstico de Precipitación')

pdf_rep4.setFillColorRGB(0,0,0)
style1 = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Avenir', fontSize=20,\
                       leading = 24)
par4 = Paragraph (u'El mapa muestra el acumulado de precipitación pronosticado con el modelo \
                    WRF para la semana del 12 de Mayo al 18 de Mayo del presente año; se debe resaltar \
                    que los acumulados del sur-occidente, oriente, sur-oriente del dominio y la ladera \
                    occidental del valle de Aburrá (ver serie izquierda)  tienen magnitudes y comportamiento espacial \
                    similar a lo observado con el radar meteorológico; sin embargo en la ladera oriental y centro \
                    del Valle de Aburrá las magnitudes pronosticadas sobrestiman el valor observado (ver serie derecha).', style1)

par4.wrap(330, 890)
par4.drawOn(pdf_rep4, 1300., 530)

pdf_rep4.drawImage(path_elem+'pronostico_wrf/prueba_week.png', \
                845., 475., 450., 450., mask = 'auto')

pdf_rep4.drawImage(path_elem+'pronostico_wrf/evalmayo_01h_CCA014.png', \
                845., 210., 380., 220., mask = 'auto')

pdf_rep4.drawImage(path_elem+'pronostico_wrf/evalmayo_01h_CORR005.png', \
                1245., 210., 380., 220., mask = 'auto')


pdf_rep4.save()




# ---------------------------------------------------------------------------------------------
# Se hace el merge de los diferentes reportes generados
# ---------------------------------------------------------------------------------------------
path_reps = '/home/atlas/informe_hidromet/20170620/informe/'

file1 = file (path_reps+'precipitacion.pdf', 'rb')
file2 = file (path_reps+'meteorologia.pdf',  'rb')
file3 = file (path_reps+'sensores_remotos.pdf', 'rb')
file4 = file (path_reps+'pronostico.pdf', 'rb')

page1 = PdfFileReader (file1).getPage (0)
page2 = PdfFileReader (file2).getPage (0)
page3 = PdfFileReader (file3).getPage (0)
page4 = PdfFileReader (file4).getPage (0)

output = PdfFileWriter()
output.addPage(page1)
output.addPage(page2)
output.addPage(page3)
output.addPage(page4)
output.write(file(path_reps+'HIDROMET_2017-06-20.pdf','w'))
