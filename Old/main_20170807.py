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
str_semana = 'Semana: 31 de julio de 2017 hasta 6 de agosto de 2017'

#-----------------------------------------------------------------------------------------------
# Parametros necesarios para hacer el reporte
#-----------------------------------------------------------------------------------------------
path_elem = '/home/atlas/informe_hidromet/20170807/'
path_reps = '/home/atlas/informe_hidromet/20170807/informe/'

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

par1 = Paragraph (u'Imagen de reflectividad del radar a las 06:44 del 04 de agosto, \
                    correspondiente al evento de precipitación con número de informe \
                    1176, en el cual se observa que durante el evento las precipitaciones \
                    alcanzaron a cubrir por completo el Valle de Aburrá con intensidades \
                    predominantemente bajas y algunos núcleos de intensidades medias \
                    en la ladera occidental de Medellín.', style1)
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
                    presentan acumulados altos en el bajo Cauca, el oriente oriente y suroeste \
                    antioqueño. Por su parte, a escala local, en el Valle de Aburrá \
                    se registraron acumulados máximos cercanos a 100 mm en La Estrella y Caldas, \
                    aunque en promedio en el valle los acumulados fueron menores \
                    a 50 mm, debido a los pocos eventos de precipitación ocurridos \
                    sobre el Valle y a que las mayores intensidades ocurrieron en \
                    el sur del Valle. ', style1)
par1.wrap(390, 890)
par1.drawOn(pdf_rep1, 1260, 585)

# contenido panel 3
data = [['Informe','Inicio','Acumulado','Municipio','Intensidad','Municipio'],
        [1174,'2017-07-31' , 9.14, u'La Estrella',   54.86, u'La Estrella'   ],
        [1175,'2017-08-03' ,11.18, u'Caldas',        76.20, u'Caldas'   ],
        [1176,'2017-08-03' ,26.64, u'Medellín',      40.08, u'Barbosa'  ],
        [1177,'2017-08-04' ,18.29, u'Medellín',      82.30, u'Caldas'   ]]


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




sizes  = [2,2,0]

labels = ['Menor 15mm', 'Entre 15mm y 30mm','Entre 30mm y 45mm']
# labels = ['Menor 15mm', 'Entre 15mm y 30mm', 'Entre 30mm y 45mm']
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

AvenirRoman  = fm.FontProperties(fname=path_reps+'avenir/AvenirLTStd-Roman.ttf', size=14)

explode = (0.05, 0.05, 0.05)
plt.close()
plt.cla()
plt.clf()
fig1 = plt.figure(1)
fig1.set_figheight(8.0)
fig1.set_figwidth(10.0)
# fig1.subplots_adjust(left = 0.0,right = 1.,top = 0.9, bottom = 0.15, hspace = 0.13,\
#                     wspace = -0.8)
# fig1.suptitle('Acumulados de Eventos', fontproperties=AvenirRomanT)
ax1 = fig1.add_subplot(1,1,1)
# ax1.set_title('Este es el subtitulo')
p,t,at = ax1.pie(sizes, explode=explode, labels=labels, autopct=make_autopct(sizes),\
                shadow=False, startangle=45, colors =[ColorInfo1, ColorInfo7, ColorInfo9, ColorInfo10])
plt.setp(at,fontproperties=AvenirRoman)
plt.setp(t,fontproperties=AvenirRoman)
ax1.axis('equal')
plt.savefig(path_elem+'ppt_est/plot_torta.png', format = 'png', dpi = 250)




pdf_rep1.drawImage(path_elem+'ppt_est/plot_torta.png', \
                1250, 160., 400., 340., mask = 'auto')

par1 = Paragraph (u'Durante esta semana se registraron cuatro eventos de precipitación \
                    que superaron un umbral de 5 mm de acumulado. En la tabla se \
                    muestran estos eventos, allí se encuentra el máximo acumulado \
                    e intensidad máxima con los respectivos municipos donde fueron \
                    registrados. En la gráfica de pastel se resume el porcentaje \
                    de los eventos que se encuentran en varios rangos de acumulados, \
                    es de resaltar ningún evento superó el umbral de 30 mm ', style1)
par1.wrap(650, 890)
par1.drawOn(pdf_rep1, 590., 165.)
pdf_rep1.save()


# # ----------------------------------------------------------------------------------------------
# # ----------------------------------------------------------------------------------------------
# # Se genera reporte sensores remotos
# #-----------------------------------------------------------------------------------------------
# pdf_rep3 = canvas.Canvas(path_reps+'sensores_remotos.pdf')
# pdf_rep3.setPageSize((sizex, sizey))
#
# # Dibujamos el rectangulo del encabezado
# title_pdf2 = u'INFORME HIDROMETEOROLÓGICO SEMANAL - Información Satelital'
# make_header(pdf_rep3, sizex, sizey, sizex, 180. , color_RGB2, color_RGB3,path_elem,\
#            title_pdf2, str_semana)
# make_footer(pdf_rep3, 0, 0, sizex, 120. , color_RGB2, path_elem)
#
# # contenido panel 1
# pdf_rep3.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
# pdf_rep3.rect(10., 150., 1660., 800., fill = False, stroke = True)
# pdf_rep3.rect(10., 900., 700., 50., fill = True, stroke = True)
# pdf_rep3.setFillColorRGB(1,1,1)
# pdf_rep3.setFont("Avenir", 24)
# pdf_rep3.drawString(25., 915.,'Análisis información GOES')
# pdf_rep3.drawImage(path_elem+'satelital_goes/Imagenes2017.195.181.png', \
#                 15., 540., 400., 350., mask = 'auto')
# pdf_rep3.drawImage(path_elem+'satelital_goes/Imagenes2017.195.211.png', \
#                 360., 540., 400., 350., mask = 'auto')
# pdf_rep3.drawImage(path_elem+'satelital_goes/Imagenes2017.195.231.png', \
#                 720., 540., 400., 350., mask = 'auto')
# pdf_rep3.drawImage(path_elem+'satelital_goes/Imagenes2017.196.034.png', \
#                 15., 150., 400., 350., mask = 'auto')
# pdf_rep3.drawImage(path_elem+'satelital_goes/Imagenes2017.196.071.png', \
#                 360., 150., 400., 350., mask = 'auto')
# pdf_rep3.drawImage(path_elem+'satelital_goes/Imagenes2017.196.121.png', \
#                 720., 150., 400., 350., mask = 'auto')
#
# style1 = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Avenir', fontSize=20,\
#                        leading = 24)
# par3 = Paragraph (u'El constante movimiento de vapor de agua con dirección este-oeste \
#                     favoreció el desarrollo vertical de nubosidad en el noreste \
#                     del departamento de Antioquia (al rededor de las 18:15 UTC del \
#                     14 de julio), y su posterior desplazamiento. En horas de la \
#                     mañana del 15 de julio (UTC), un núcleo de gran altura se acerco \
#                     al Valle por el norte (con temperatura aproximada de -84°C), \
#                     y comenzó su difusión dejando nubosidad residual sobre la \
#                     zona sur de Antioquia, nubes de menor altura (-40°C aproximadamente), \
#                     que persistieron hasta las 12:15 UTC.', style1)
# par3.wrap(400, 890)
# par3.drawOn(pdf_rep3, 1150., 530)
#
# pdf_rep3.save()

#
# # ----------------------------------------------------------------------------------------------
# # ----------------------------------------------------------------------------------------------
# # Se genera segundo reporte en pdf
# #-----------------------------------------------------------------------------------------------
# pdf_rep2 = canvas.Canvas(path_reps+'meteorologia.pdf')
# pdf_rep2.setPageSize((sizex, sizey))
#
# # Dibujamos el rectangulo del encabezado
# title_pdf2 = u'INFORME HIDROMETEOROLÓGICO SEMANAL - Variables atmosféricas'
# make_header(pdf_rep2, sizex, sizey, sizex, 180. , color_RGB2, color_RGB3,path_elem,\
#            title_pdf2, str_semana)
# make_footer(pdf_rep2, 0, 0, sizex, 120. , color_RGB2, path_elem)
#
# # contenido panel 1
# pdf_rep2.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
# pdf_rep2.rect(10., 580., 1660., 390., fill = False, stroke = True)
# pdf_rep2.rect(10., 940., 700., 50., fill = True, stroke = True)
# pdf_rep2.setFillColorRGB(1,1,1)
# pdf_rep2.setFont("Avenir", 24)
# pdf_rep2.drawString(25., 955., 'Análisis de descargas eléctricas')
# pdf_rep2.drawImage(path_elem+'descargas_elec/MapaScatter_201707100000.png', \
#                 780., 595., 360., 360., mask = 'auto')
# pdf_rep2.drawImage(path_elem+'descargas_elec/20170716.png', \
#                 1200., 595., 455., 360., mask = 'auto')
# style1 = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Avenir', fontSize=20,\
#                        leading = 24)
# par1 = Paragraph (u'En resumen, en esta última semana se presentaron en total 738 \
#                     descargas eléctricas tipo nube-tierra al interior del Valle \
#                     de Aburrá. La mayoría de estas descargas se registraron en \
#                     los municipios de Medellín y Envigado, en donde la cifra ascendió \
#                     a 211 y 110 descargas respectivamente. Se presentó una mayor \
#                     actividad eléctrica en asociación a una tormenta  que tuvo \
#                     lugar desde la tarde del domingo 16, en donde la máxima densidad \
#                     de las descargas se localizó hacia en el límite sur de Medellín \
#                     con los demás municipios del AMVA y en el norte en límites con \
#                     Bello y Copacabana. El número total de descargas tipo nube-tierra \
#                     de este día fue de 633', style1)
# par1.wrap(660., 890.)
# par1.drawOn(pdf_rep2, 40, 700)
#
# # contenido panel 2
# pdf_rep2.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
# pdf_rep2.rect(10., 150., 1660., 395., fill = False, stroke = True)
# pdf_rep2.rect(10., 520., 700., 50., fill = True, stroke = True)
# pdf_rep2.setFillColorRGB(1,1,1)
# pdf_rep2.setFont("Avenir", 24)
# pdf_rep2.drawString(25., 535.,'Análisis de estaciones de vientos y temperatura')
# pdf_rep2.drawImage(path_elem+'vientos_temp/promedio_viento_temperatura.png', \
#                 25., 165., 380., 350., mask = 'auto')
#
# pdf_rep2.setFillColorRGB(0,0,0)
# par2 = Paragraph (u'En el mapa de la izqquierda es posible observar que la dirección promedio \
#                   del viento siguió el eje del Valle hasta confluir en el centro del mismo \
#                   con velocidades promedio \
#                   que varian entre los 1 - 4 km/h. Las estaciones ubicadas en las laderas \
#                   muestran direcciones también hacia el centro del Valle donde la mayor \
#                   velocidad promedio la registró la estación de Santa Elena con un valor de \
#                   10 km/h. Por su parte las temperaturas promedio registaradas por las \
#                   estaciones en la base del Valle están alrededor de los 20ºC y la menor \
#                   temperatura promedio fue registrada por la estación Santa Elena (11ºC).'\
#                   , style1)
# par2.wrap(400, 890)
# par2.drawOn(pdf_rep2, 430., 160)
#
# pdf_rep2.drawImage(path_elem+'vientos_temp/maximo_viento_temperatura.png', \
#                 850., 165., 380., 350., mask = 'auto')
# pdf_rep2.setFillColorRGB(0,0,0)
# par3 = Paragraph (u'La dirección de los vientos máximos registrados durante la semana \
#                   van de norte a sur siguiendo el eje del Valle, \
#                   es destacable la magnitud máxima registrada \
#                   por la estación Santa Helena (35 km/h). Por su parte, las temperaturas \
#                   máximas registradas en la base del Valle estuvieron entre los 26 y \
#                   28ºC, mientras que las laderas variaron entre 16 y 26 ºC. El \
#                   máximo registrado por la estación Santa Elena fue de 16ºC ', style1)
# par3.wrap(360, 890)
# par3.drawOn(pdf_rep2, 1270., 200)
#
# pdf_rep2.save()
#


# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# Se genera reporte niveles
#-----------------------------------------------------------------------------------------------
# pdf_rep5 = canvas.Canvas(path_reps+'niveles.pdf')
# pdf_rep5.setPageSize((sizex, sizey))
#
# # Dibujamos el rectangulo del encabezado
# title_pdf2 = u'INFORME HIDROMETEOROLÓGICO SEMANAL - Niveles hidrológicos'
# make_header(pdf_rep5, sizex, sizey, sizex, 180. , color_RGB2, color_RGB3,path_elem,\
#            title_pdf2, str_semana)
# make_footer(pdf_rep5, 0, 0, sizex, 120. , color_RGB2, path_elem)
#
# # contenido panel 1
# pdf_rep5.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
# pdf_rep5.rect(10., 150., 1660., 800., fill = False, stroke = True)
# pdf_rep5.rect(10., 900., 700., 50., fill = True, stroke = True)
# pdf_rep5.setFillColorRGB(1,1,1)
# pdf_rep5.setFont("Avenir", 24)
# pdf_rep5.drawString(25., 915.,'Análisis información niveles')
#
# pdf_rep5.drawImage(path_elem+'nivel_hidro/94.png', \
#                 100., 350., 700., 500., mask = 'auto')
# pdf_rep5.drawImage(path_elem+'nivel_hidro/20170710to20170716.png', \
#                 850., 350., 730., 500., mask = 'auto')
#
# style1 = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Avenir', fontSize=20,\
#                        leading = 24)
# # par5 = Paragraph (u'Las figuras 1 y 2 corresponden a las estaciones Puente de la 33 y Santa Rita. \
# #                     En estas se puede observar en la parte superior izquierda, la distribución de \
# #                     la lluvia acumulada en la cuenca, calculada a partir de datos del radar meteorológico. \
# #                     En el recuadro ubicado en la parte superior derecha se ubican las curvas de duración, \
# #                     estas representan la probabilidad de excedencia de determinado nivel; la línea roja \
# #                     punteada es la curva de duración de los últimos 7 días, la línea punteada azul es la \
# #                     curva de duración del último mes y la curva en negro sólido es la curva generada apartir \
# #                     de datos históricos. \n Los mayores acumulados se registraron en el sur del Valle de Aburrá, \
# #                     especialmente en la ladera occidental donde en algunos sectores el acumulado fue mayor a los \
# #                     80 mm. En la cuenca de la figura 2, ubicada en este sector, se puede observar que las curvas \
# #                     de duración correspondientes al último mes y a los últimos siete días presentan en general, \
# #                     niveles más altos que los reportados históricamente. El Puente de la 33 reportó cinco \
# #                     crecientes que alcanzaron el nivel de alerta 1, mietras que en la estación Santa Rita \
# #                     alcanzó el nivel de alerta 2 en dos ocasiones.', style1)
#
# par5 = Paragraph (u'Durante la semana se presentaron dos eventos de lluvia de \
#                     especial consideración, el primero de ellos el día 15 de Julio \
#                     a las 00:00 horas, donde estaciones como La Presidenta, La \
#                     Madera y La García reportaron niveles superiores al nivel de \
#                     riesgo 2. El día 16 de Julio se reporta otro evento a las 2 \
#                     de la tarde, las cuencas ubicadas en la ladera occidental del \
#                     Sur del Valle de Aburrá fueron las más afectadas por este; \
#                     las estaciones La Zúñiga, Santa Rita, El Encanto, La Presidenta \
#                     y el puente de la aguacatala ubicadas en este sector reportaron \
#                     niveles por encima del nivel de alerta 2. Sobre la estación \
#                     Puente de La Aguacatala la lluvia promedio acumulada en la \
#                     cuenca alcanza un nivel máximo el día 2017-07-16 14:00:00 con \
#                     una intensidad lluvia de 4.06 mm/h que genera un aumento rápido \
#                     en los niveles alcanzados por el sensor y alcanza hasta 200.33 \
#                     cm, superando el nivel de alerta 2. Según las curvas de duración, \
#                     esta semana la probabilidad de que se presenten eventos que \
#                     superen los niveles de riesgo aumentó levemente.', style1)
# par5.wrap(1620, 300)
# par5.drawOn(pdf_rep5, 30., 170.)
#
# pdf_rep5.save()


# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# Se genera primer reporte en pdf
#-----------------------------------------------------------------------------------------------
# pdf_rep4 = canvas.Canvas(path_reps+'pronostico.pdf')
# pdf_rep4.setPageSize((sizex, sizey))
#
# # Dibujamos el rectangulo del encabezado
# title_pdf4 = u'INFORME HIDROMETEOROLÓGICO SEMANAL - Pronóstico Meteorológico'
# make_header(pdf_rep4, sizex, sizey, sizex, 180. , color_RGB2, color_RGB3,path_elem,\
#            title_pdf4, str_semana)
# make_footer(pdf_rep4, 0, 0, sizex, 120. , color_RGB2, path_elem)
#
# # contenido panel 1
# pdf_rep4.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
# pdf_rep4.rect(10., 150., 820., 805., fill = False, stroke = True)
# pdf_rep4.rect(10., 930., 700., 50., fill = True, stroke = True)
# pdf_rep4.setFillColorRGB(1,1,1)
# pdf_rep4.setFont("Avenir", 24)
# pdf_rep4.drawString(25., 955., 'Pronóstico de Temperatura')
#
# pdf_rep4.setFillColorRGB(0,0,0)
# style1 = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Avenir', fontSize=20,\
#                        leading = 24)
#
#
# par4 = Paragraph (u'El mapa representa la diferencia del promedio de temperatura \
#                     observada y pronosticada en cada una de las estaciones de la \
#                     red de monitoreo meteorológico; en general se observa que en \
#                     los municipios del norte y en Caldas, el  modelo WRF sobrestimo \
#                     la temperatura, siendo muy evidente la madrugada del 13 de \
#                     Julio, por el contrario al interior de Medellín las temperaturas \
#                     pronosticada fue muy cercana a la temperatura observada', style1)
#
#
# par4.wrap(330, 890)
# par4.drawOn(pdf_rep4, 480., 515)
#
# pdf_rep4.drawImage(path_elem+'pronostico_wrf/mapa_temp.png', \
#                 25., 475., 450., 450., mask = 'auto')
#
# pdf_rep4.drawImage(path_elem+'pronostico_wrf/tmp_mayo_82.png', \
#                 25., 210., 380., 220., mask = 'auto')
#
# pdf_rep4.drawImage(path_elem+'pronostico_wrf/tmp_mayo_105.png', \
#                 425., 210., 380., 220., mask = 'auto')
#
#
#
#
# # contenido panel 2
# pdf_rep4.setFillColorRGB(color_RGB1[0]/255., color_RGB1[1]/255., color_RGB1[2]/255.)
# pdf_rep4.rect(840., 150., 820., 805., fill = False, stroke = True)
# pdf_rep4.rect(840., 930., 700., 50., fill = True, stroke = True)
# pdf_rep4.setFillColorRGB(1,1,1)
# pdf_rep4.setFont("Avenir", 24)
# pdf_rep4.drawString(875., 955.,'Pronóstico de Precipitación')
#
# pdf_rep4.setFillColorRGB(0,0,0)
# style1 = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Avenir', fontSize=20,\
#                        leading = 24)
#
#
# par4 = Paragraph (u'Los mapas muestran acumulados de precipitación pronosticada \
#                     con el modelo WRF; se observa que el modelo sub estimó la \
#                     magnitud de los acumulados de precipitación en comparación \
#                     con el radar en el sur oriente del dominio en el costado \
#                     suroccidental los acumulados de precipitación son muy similares \
#                     a los observados por el radar, sin embargo al norte de Medellin \
#                     se observan acumulados de poca magnitud que no fueron observados, \
#                     es lo que se llama falsas alarma.', style1)
#
#
# par4.wrap(770, 350)
# par4.drawOn(pdf_rep4, 870., 405)
#
# pdf_rep4.drawImage(path_elem+'pronostico_wrf/rainweek_08.png', \
#                 870., 595., 340., 320., mask = 'auto')
#
# pdf_rep4.drawImage(path_elem+'pronostico_wrf/rainweek_02.png', \
#                 1290., 595., 360., 320., mask = 'auto')
#
# pdf_rep4.drawImage(path_elem+'pronostico_wrf/evalmayo_01h_MUN106.png', \
#                 870., 155., 360., 240., mask = 'auto')
#
# pdf_rep4.drawImage(path_elem+'pronostico_wrf/evalmayo_01h_MUN043.png', \
#                 1290., 155., 360., 240., mask = 'auto')
#
#
# pdf_rep4.save()
#


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

pdf_rep6.drawImage(path_elem+'incendios_vul/reporte_semanal_2017-08-03.png', \
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
                    el Valle de Aburrá del día mas crítico de la semana (2017-08-03). \
                    Además se presenta la ubicación de 6 incendios reportados \
                    durante la semana, los cuales se presentaron en Itagui, occidente \
                    de Medellín y en Bello. En esta semana predomina alta vulnerabilidad \
                    para los municipios del norte del Valle de Aburrá. la La mancha \
                    urbana se presenta en color gris', style1)

par6.wrap(340, 890)
par6.drawOn(pdf_rep6, 1280., 250)

pdf_rep6.save()




# ---------------------------------------------------------------------------------------------
# Se hace el merge de los diferentes reportes generados
# ---------------------------------------------------------------------------------------------


file1 = file (path_reps+'precipitacion.pdf', 'rb')
# file2 = file (path_reps+'meteorologia.pdf',  'rb')
# file3 = file (path_reps+'sensores_remotos.pdf', 'rb')
# file4 = file (path_reps+'niveles.pdf', 'rb')
# file5 = file (path_reps+'pronostico.pdf', 'rb')
file6 = file (path_reps+'incendios.pdf', 'rb')

page1 = PdfFileReader (file1).getPage (0)
# page2 = PdfFileReader (file2).getPage (0)
# page3 = PdfFileReader (file3).getPage (0)
# page4 = PdfFileReader (file4).getPage (0)
# page5 = PdfFileReader (file5).getPage (0)
page6 = PdfFileReader (file6).getPage (0)

output = PdfFileWriter()
output.addPage(page1)
# output.addPage(page2)
# output.addPage(page3)
# output.addPage(page4)
# output.addPage(page5)
output.addPage(page6)
output.write(file(path_reps+'HIDROMET_2017-08-07.pdf','w'))
