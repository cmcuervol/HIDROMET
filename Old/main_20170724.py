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
str_semana = 'Semana: 17 de junlio de 2017 hasta 23 de julio de 2017'

#-----------------------------------------------------------------------------------------------
# Parametros necesarios para hacer el reporte
#-----------------------------------------------------------------------------------------------
path_elem = '/home/atlas/informe_hidromet/20170724/'
path_reps = '/home/atlas/informe_hidromet/20170724/informe/'


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
pdf_rep1 = canvas.Canvas(path_reps+'precipitacion.pdf')
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
pdf_rep1.drawString(25., 955.,'Precipitaciones sobre el Valle de Aburrá')

pdf_rep1.drawImage(path_elem+'ppt_rad/Evento.png', \
                25., 400., 520., 520., mask = 'auto')

style1 = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Avenir', fontSize=20,\
                       leading = 24)

par1 = Paragraph (u'Imagen de reflectividad del radar a las 20:28 del 18 de julio, \
                    correspondiente al evento de precipitación con número de informe \
                    1169, en el cual se observa que durante el evento las precipitaciones \
                    alcanzaron a cubrir completamente el Valle de Aburrá con intensidades \
                    predominantemente bajas y algunos núcleos de altas intensidades \
                    en el occidente. Este evento fue el responsable de los acumulados \
                    en el norte del Valle.', style1)
par1.wrap(515, 890)
par1.drawOn(pdf_rep1, 25., 165)


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

par1 = Paragraph (u'A escala regional, los acumulados semanales de precipitación \
                    presentan acumulados moderados en el oriente antioqueño y bajo \
                    Cauca. Por su parte, a escala local, en el Valle de Aburrá se \
                    registraron acumulados máximos cercanos a 110 mm en el municipio \
                    de Caldas. En promedio en el Valle los acumulados fueron menores \
                    a 50 mm, principalmente debido a los pocos eventos de precipitación \
                    ocurridos durante la semana, aunque dos de estos lograron cubrir \
                    el Valle por completo con intensidades moderadas, principalmente \
                    durante las noches y madrugadas.', style1)
par1.wrap(390, 890)
par1.drawOn(pdf_rep1, 1260, 585)

# contenido panel 3
data = [['Informe','Inicio','Acumulado','Municipio','Intensidad','Municipio'],
        [1169,'2017-07-18' ,27.43, u'Medellín',    67.20, u'Barbosa'  ],
        [1170,'2017-07-19' ,30.99,  'Caldas',      98.28, u'Caldas'   ],
        [1171,'2017-07-19' ,33.74, u'Medellín',    67.06, u'Medellín' ],
        [1172,'2017-07-20' ,15.49, u'Envigado',    82.30, u'Medellín' ]]

t=Table(data,[1*inch,2*inch,1.5*inch,1.5*inch,1.5*inch,1.5*inch], len(data)*[0.4*inch])
pdf_rep1.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
pdf_rep1.rect(565., 150., 1105., 390., fill = False, stroke = True)
pdf_rep1.rect(565., 515., 737., 50., fill = True, stroke = True)
pdf_rep1.setFillColorRGB(1,1,1)
pdf_rep1.setFont("Avenir", 24)
pdf_rep1.drawString(580., 530., 'Resumen eventos de la semana')

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
t.drawOn(pdf_rep1, 590., 350.)

pdf_rep1.drawImage(path_elem+'ppt_est/plot_torta.png', \
                1250, 160., 400., 340., mask = 'auto')

par1 = Paragraph (u'Durante esta semana se registraron cuatro eventos de precipitación \
                    que superaron un umbral de 5 mm de acumulado. En la tabla se \
                    muestran estos eventos, allí se encuentra el máximo acumulado \
                    e intensidad máxima con los respectivos municipos donde fueron \
                    registrados. En la gráfica de pastel se resume el porcentaje \
                    de los eventos que se encuentran en varios rangos de acumulados, \
                    es de resaltar que ningún un evento sueperó el umbral de 45 mm ', style1)
par1.wrap(650, 890)
par1.drawOn(pdf_rep1, 590., 165.)
pdf_rep1.save()

# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# Se genera reporte vientos, Temperatura y descargas eléctricas
#-----------------------------------------------------------------------------------------------
pdf_rep2 = canvas.Canvas(path_reps+'meteorologia.pdf')
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
pdf_rep2.drawImage(path_elem+'descargas_elec/MapaScatter_201707170000.png', \
                760., 595., 380., 360., mask = 'auto')
pdf_rep2.drawImage(path_elem+'descargas_elec/20170723.png', \
                1200., 595., 455., 360., mask = 'auto')
style1 = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Avenir', fontSize=20,\
                       leading = 24)
par1 = Paragraph (u'En resumen, en esta última semana se presentaron en total 147 \
                    descargas eléctricas tipo nube-tierra al interior del Valle \
                    de Aburrá. La mayoría de estas descargas se registraron en \
                    los municipios de Caldas y Barbosa, en donde la cifra ascendió \
                    a 80 y 49 descargas respectivamente. Se presentó una mayor \
                    actividad eléctrica en asociación lluvias de alta intensidad \
                    en el AMVA el día martes, en donde la máxima densidad de las \
                    descargas se localizó en Caldas. El número total de descargas \
                    tipo nube-tierra de este día fue de 90.', style1)
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
                25., 165., 370., 350., mask = 'auto')

pdf_rep2.setFillColorRGB(0,0,0)
par2 = Paragraph (u'En el mapa de la izquierda es posible observar que la dirección \
                    promedio del viento siguió el eje del Valle hasta confluir en el \
                    centro del mismo con velocidades promedio que varian entre los \
                    1 - 4 km/h. Las estaciones ubicadas en las laderas muestran \
                    direcciones también hacia el centro del Valle donde la mayor \
                    velocidad promedio la registró la estación de Santa Elena con \
                    un valor de 20 km/h. Por su parte las temperaturas promedio \
                    registaradas por las estaciones en la base del Valle están \
                    alrededor de los 22ºC y la menor temperatura promedio fue \
                    registrada por la estación Santa Elena (12ºC).', style1)
par2.wrap(400, 890)
par2.drawOn(pdf_rep2, 430., 160)

pdf_rep2.drawImage(path_elem+'vientos_temp/maximo_viento_temperatura.png', \
                850., 165., 370., 350., mask = 'auto')
pdf_rep2.setFillColorRGB(0,0,0)
par3 = Paragraph (u'La dirección de los vientos máximos registrados durante la \
                    semana van de norte a sur siguiendo el eje del Valle, es destacable \
                    la magnitud máxima registrada por la estación UNAL sede Agronomía \
                    (30 km/h). Por su parte, las temperaturas máximas registradas \
                    en la base del Valle estuvieron entre los 28 y 30ºC, mientras \
                    que las laderas variaron entre 24 y 27 ºC. El máximo registrado \
                    por la estación Santa Elena fue de 17ºC ', style1)
par3.wrap(360, 890)
par3.drawOn(pdf_rep2, 1270., 200)

pdf_rep2.save()

#
#

# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# Se genera primer reporte pronóstico
#-----------------------------------------------------------------------------------------------
pdf_rep4 = canvas.Canvas(path_reps+'pronostico.pdf')
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


par4 = Paragraph (u'El mapa representa la diferencia del promedio de temperatura \
                    observada y pronosticada en cada una de las estaciones de la \
                    red de monitoreo meteorológico; en general se observa que las \
                    diferencias son muy cercanas a cero; el modelo WRF subrestimo \
                    la temperatura, siendo muy evidente en Girardota y en el sur \
                    oriente de Medellín, las menores diferencias se observaron en \
                    Barbosa.', style1)

par4.wrap(330, 890)
par4.drawOn(pdf_rep4, 480., 515)

pdf_rep4.drawImage(path_elem+'pronostico_wrf/mapa_temp.png', \
                25., 475., 450., 450., mask = 'auto')

pdf_rep4.drawImage(path_elem+'pronostico_wrf/tmp_mayo_82.png', \
                25., 210., 380., 220., mask = 'auto')

pdf_rep4.drawImage(path_elem+'pronostico_wrf/tmp_mayo_105.png', \
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


par4 = Paragraph (u'Los mapas muestran acumulados de precipitación pronosticada \
                    con el modelo WRF; se observa que el modelo sub estimó la \
                    magnitud de los acumulados de precipitación en comparación \
                    con el radar en el oriente (Valle de San Nicolas) del dominio \
                    en el costado suroccidental los acumulados de precipitación \
                    son muy similares a los observados por el radar, sin embargo \
                    al oriente no se observan acumulados de magnitudes significativas, \
                    esto puede estar relacionado con la omisión de los eventos \
                    ocurridos el 19, 20 y 21 de Julio.', style1)


par4.wrap(770, 350)
par4.drawOn(pdf_rep4, 870., 405)

pdf_rep4.drawImage(path_elem+'pronostico_wrf/rainweek_08.png', \
                870., 595., 340., 320., mask = 'auto')

pdf_rep4.drawImage(path_elem+'pronostico_wrf/rainweek_02.png', \
                1290., 595., 360., 320., mask = 'auto')

pdf_rep4.drawImage(path_elem+'pronostico_wrf/evalmayo_01h_MUN106.png', \
                870., 155., 360., 240., mask = 'auto')

pdf_rep4.drawImage(path_elem+'pronostico_wrf/evalmayo_01h_CCA002.png', \
                1290., 155., 360., 240., mask = 'auto')


pdf_rep4.save()





# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# Se genera reporte niveles
#-----------------------------------------------------------------------------------------------
pdf_rep5 = canvas.Canvas(path_reps+'niveles.pdf')
pdf_rep5.setPageSize((sizex, sizey))

# Dibujamos el rectangulo del encabezado
title_pdf2 = u'INFORME HIDROMETEOROLÓGICO SEMANAL - Niveles hidrológicos'
make_header(pdf_rep5, sizex, sizey, sizex, 180. , color_RGB2, color_RGB3,path_elem,\
           title_pdf2, str_semana)
make_footer(pdf_rep5, 0, 0, sizex, 120. , color_RGB2, path_elem)

# contenido panel 1
pdf_rep5.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
pdf_rep5.rect(10., 150., 1660., 800., fill = False, stroke = True)
pdf_rep5.rect(10., 900., 700., 50., fill = True, stroke = True)
pdf_rep5.setFillColorRGB(1,1,1)
pdf_rep5.setFont("Avenir", 24)
pdf_rep5.drawString(25., 915.,'Análisis información niveles')

pdf_rep5.drawImage(path_elem+'nivel_hidro/93.png', \
                100., 350., 700., 500., mask = 'auto')
pdf_rep5.drawImage(path_elem+'nivel_hidro/ejemplomapa.png', \
                850., 350., 780., 570., mask = 'auto')

style1 = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Avenir', fontSize=20,\
                       leading = 24)
par5 = Paragraph (u'Durante la semana se presentaron tres eventos de precipitación \
                    que acitvaron respuesta hidrológica en las cuencas del Valle \
                    de Aburrá, el primero de ellos el día 17 de julio, en el que \
                    la estación del puente de La 33 registró niveles superiores \
                    al segundo nivel de riesgo; el segundo enveto deprecipitación \
                    se dió el 18 de julio, en el cual la estación del parque lineal \
                    de la presidenta también superó el segundo nivel de alerta; \
                    y durante el evento de precipitación del 20 de julio las estaciones \
                    de La Presidenta y el Encanto superaron el segundo nivel de alerta. \
                    Las figura de la izquierda corresponden a la estacion del Puente \
                    de la 33. En esta se puede observar en la parte superior \
                    izquierda, la distribución de la lluvia acumulada en la cuenca, \
                    calculada a partir de datos del radar meteorológico. En el \
                    recuadro ubicado en la parte superior derecha se ubican las \
                    curvas de duración, estas representan la probabilidad de \
                    excedencia de determinado nivel; la línea roja punteada es \
                    la curva de duración de los últimos 7 días, la línea punteada \
                    azul es la curva de duración del último mes y la curva en \
                    negro sólido es la curva generada apartir de datos históricos. \
                    Los mayores acumulados se registraron en el sur del Valle de \
                    Aburrá donde en algunos sectores el acumulado fue mayor a los \
                    100 mm.', style1)
par5.wrap(1620, 300)
par5.drawOn(pdf_rep5, 30., 160.)

pdf_rep5.save()


# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# Se genera reporte sensores remotos
#-----------------------------------------------------------------------------------------------
pdf_rep3 = canvas.Canvas(path_reps+'sensores_remotos.pdf')
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
pdf_rep3.drawImage(path_elem+'satelital_goes/Imagenes2017.199.194.png', \
                15., 540., 400., 350., mask = 'auto')
pdf_rep3.drawImage(path_elem+'satelital_goes/Imagenes2017.199.211.png', \
                390., 540., 400., 350., mask = 'auto')
pdf_rep3.drawImage(path_elem+'satelital_goes/Imagenes2017.199.221.png', \
                750., 540., 400., 350., mask = 'auto')
pdf_rep3.drawImage(path_elem+'satelital_goes/Imagenes2017.200.001.png', \
                15., 150., 400., 350., mask = 'auto')
pdf_rep3.drawImage(path_elem+'satelital_goes/Imagenes2017.200.021.png', \
                390., 150., 400., 350., mask = 'auto')
pdf_rep3.drawImage(path_elem+'satelital_goes/Imagenes2017.200.041.png', \
                750., 150., 400., 350., mask = 'auto')

style1 = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Avenir', fontSize=20,\
                       leading = 24)
par3 = Paragraph (u'En esta sección se muestra el análisis con información satélital \
                    de los fenómenos meteorológicos ocurridos sobre el Valle de \
                    Aburrá, con el fin de mostrar que muchos de estos fenómenos \
                    se ven originados o influenciados por condiciones regionales \
                    y globales. Específicamente en este informe se muestra cómo \
                    se observa con la información del satélite GOES la evolución \
                    del evento del 19 de julio, el cual fue el evento que más \
                    aportó al acumulado en todo el valle durante esta semana. Al \
                    rededor de las 21:15 UTC ingresa por el sureste de Antioquia \
                    un conjunto de nubes convectivas de gran altura (con temperatura \
                    entre -60°C y -84°C). Conforme se desplazan, las nubes se unifican \
                    formando un núcleo que supera el tamaño del departamento de \
                    Antioquia, el cual a las 2:15 UTC ya albergaba parte importante \
                    del territorio, y entre este el Valle de Aburrá.', style1)
par3.wrap(400, 890)
par3.drawOn(pdf_rep3, 1200., 250)

pdf_rep3.save()

# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# Se genera reporte incendios forestales
#-----------------------------------------------------------------------------------------------
pdf_rep6 = canvas.Canvas(path_reps+'incendios.pdf')
pdf_rep6.setPageSize((sizex, sizey))

# Dibujamos el rectangulo del encabezado
title_pdf6 = u'INFORME HIDROMETEOROLÓGICO SEMANAL - Incendios forestales'
make_header(pdf_rep6, sizex, sizey, sizex, 180. , color_RGB2, color_RGB3,path_elem,\
           title_pdf6, str_semana)
make_footer(pdf_rep6, 0, 0, sizex, 120. , color_RGB2, path_elem)

# contenido panel 1
pdf_rep6.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
pdf_rep6.rect(10., 150., 1660., 800., fill = False, stroke = True)
pdf_rep6.rect(10., 900., 700., 50., fill = True, stroke = True)
pdf_rep6.setFillColorRGB(1,1,1)
pdf_rep6.setFont("Avenir", 24)
pdf_rep6.drawString(25., 915.,'Vulnerabilidad incendios forestales')

pdf_rep6.drawImage(path_elem+'incendios_vul/reporte_semanal_2017-07-18.png', \
                    30., 140., 1250., 700., mask = 'auto')

style1 = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Avenir', fontSize=20,\
                       leading = 24)
par6 = Paragraph (u'Con el fin de mostrar a diario la vulnerabilidad a incendios \
                    forestales que tiene el Valle de Aburrá, diariamente se genera \
                    un mapa de vulnerabilidad que es obtenido a partir de la \
                    información del modelo hidrológico que a su vez es alimentado \
                    por iformación de variables estáticas (no cambian en el timepo) \
                    como el uso del suelo y variables dinámicas como la precipitación \
                    antecendente. Dicho mapa diariamente se le envia a los organismos \
                    de gestión del riesgo, en esta gráfica se observan los mapas \
                    distribuidos y agregado de vulnerabilidad de incendios para \
                    el Valle de Aburrá del día mas crítico de la semana (2017-07-18). \
                    Además se presenta la ubicación de 6 incendios reportados \
                    durante la semana, los cuales se presentaron en su totalidad \
                    en el occidente de Medellín.', style1)
par6.wrap(340, 890)
par6.drawOn(pdf_rep6, 1280., 200)

pdf_rep6.save()


# ---------------------------------------------------------------------------------------------
# Se hace el merge de los diferentes reportes generados
# ---------------------------------------------------------------------------------------------

file1 = file (path_reps+'precipitacion.pdf', 'rb')
file2 = file (path_reps+'meteorologia.pdf',  'rb')
file3 = file (path_reps+'sensores_remotos.pdf', 'rb')
file4 = file (path_reps+'niveles.pdf', 'rb')
file5 = file (path_reps+'pronostico.pdf', 'rb')
file6 = file (path_reps+'incendios.pdf', 'rb')

page1 = PdfFileReader (file1).getPage (0)
page2 = PdfFileReader (file2).getPage (0)
page3 = PdfFileReader (file3).getPage (0)
page4 = PdfFileReader (file4).getPage (0)
page5 = PdfFileReader (file5).getPage (0)
page6 = PdfFileReader (file6).getPage (0)

output = PdfFileWriter()
output.addPage(page1)
output.addPage(page2)
output.addPage(page3)
output.addPage(page4)
output.addPage(page5)
output.addPage(page6)
output.write(file(path_reps+'HIDROMET_2017-07-24.pdf','w'))
