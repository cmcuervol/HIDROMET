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
str_semana = 'Semana: 26 de junio de 2017 hasta 30 de junio de 2017'

#-----------------------------------------------------------------------------------------------
# Parametros necesarios para hacer el reporte
#-----------------------------------------------------------------------------------------------
path_elem = '/home/atlas/informe_hidromet/20170701/'
path_reps = '/home/atlas/informe_hidromet/20170701/informe/'

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
par1 = Paragraph (u'Se comparan los acumulados de la red pluviométrica de EPM desde \
                    el 01 hasta el 30 de junio de 2017 con la mediana de los \
                    acumulados históricos de junio, con la intención de conocer \
                    como es su comportamiento. Hasta esta fecha, los acumualdos \
                    en la mayoría de las estaciones al interior del AMVA estan por \
                    encima de las medianas históricas excepto la estación de San \
                    Antonio de Prado, que es igual a la mediana; Chorrilos Barbosa \
                    y Miguel de Aguinaga que está por encima de la mediana.', style1)
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

par1 = Paragraph (u'A escala regional, los acumulados semanales de precipitación \
                    presentan acumulados altos en oriente oriente y suroeste \
                    antioqueño. Por su parte, a escala local, en el Valle de Aburrá \
                    se registraron acumulados máximos cercanos a 200 mm en el norte \
                    y sur del Valle, estos acumulados se origiraron debido a sistemas \
                    de mesoescala que cubrieron el Valle por completo con intensidades \
                    moderadas, principalmente durante las noches y madrugadas; \
                    dichos sistemas estuvieron fuertemente influenciados por el \
                    paso de algunas ondas del este.', style1)
par1.wrap(390, 890)
par1.drawOn(pdf_rep1, 1260, 585)

# contenido panel 3
data = [['Informe','Inicio','Acumulado','Municipio','Intensidad','Municipio'],
        [1153,'2017-06-26' ,32.10, u'Barbosa',    115.82, u'Medellín'  ],
        [1154,'2017-06-26' ,81.53, 'La Estrella', 109.73, 'La Estrella'],
        [1155,'2017-06-27' ,76.71, 'La Estrella', 91.44,  'La Estrella'],
        [1158,'2017-06-29' ,49.53, u'Medellín',   88.39,  u'Medellín'  ]]

t=Table(data,[1*inch,2*inch,1.5*inch,1.5*inch,1.5*inch,1.5*inch], 5*[0.4*inch])
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

par1 = Paragraph (u'Durante esta semana se registraron ocho eventos de precipitación \
                    que superaron un umbral de 5 mm de acumulado. En la tabla se \
                    muestran los eventos más relevantes, allí se muestra el máximo \
                    acumulado e intensidad máxima con los respectivos municipos \
                    donde fueron registrados. En la gráfica de pastel se resume \
                    el porcentaje de los eventos que se encuentran en varios rangos \
                    de acumulados, es de resaltar que tres eventos sueperaron el \
                    umbral de 45 mm ', style1)
par1.wrap(650, 890)
par1.drawOn(pdf_rep1, 590., 165.)
pdf_rep1.save()



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
pdf_rep5.drawImage(path_elem+'nivel_hidro/108.png', \
                850., 350., 700., 500., mask = 'auto')

style1 = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Avenir', fontSize=20,\
                       leading = 24)
par5 = Paragraph (u'Las figuras corresponden a las estaciones Puente de la 33 y \
                    Santa Rita. En estas se puede observar en la parte superior \
                    izquierda, la distribución de la lluvia acumulada en la cuenca, \
                    calculada a partir de datos del radar meteorológico. En el \
                    recuadro ubicado en la parte superior derecha se ubican las \
                    curvas de duración, estas representan la probabilidad de \
                    excedencia de determinado nivel; la línea roja punteada es \
                    la curva de duración de los últimos 7 días, la línea punteada \
                    azul es la curva de duración del último mes y la curva en \
                    negro sólido es la curva generada apartir de datos históricos. \
                    Los mayores acumulados se registraron en el sur del Valle de \
                    Aburrá, especialmente en la ladera occidental donde en algunos \
                    sectores el acumulado fue mayor a los 80 mm. En la cuenca de \
                    Santa Rita, ubicada en este sector, se puede observar que las \
                    curvas de duración correspondientes al último mes y a los \
                    últimos siete días presentan en general, niveles más altos \
                    que los reportados históricamente. El Puente de la 33 reportó \
                    cinco crecientes que alcanzaron el nivel de alerta 1, mietras \
                    que en la estación Santa Rita alcanzó el nivel de alerta 2 \
                    en dos ocasiones.', style1)
par5.wrap(1620, 300)
par5.drawOn(pdf_rep5, 30., 170.)

pdf_rep5.save()

# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# Se genera reporte pronóstico
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
                    red de monitoreo meteorológico; en general se observa que al \
                    interior de Medellín el modelo sobrestimó la temperatura, se \
                    observa lo contrario y en menor magnitud en los municipios \
                    del norte y en Caldas; las diferencias no exceden 0.5 C; el \
                    máximo se observa en las estaciones ubicadas en la ladera \
                    oriental del valle de Aburrá el mejor pronóstico se observa \
                    en la estación ubicada en Caldas.', style1)


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


par4 = Paragraph (u'Los mapas muestran acumulados de precipitación pronosticada \
                    con el modelo WRF; se observa en general el modelo sub-estimo \
                    la magnitud de los acumulados de precipitación en comparación \
                    con el radar, incluso los acumulados en gran parte del dominio \
                    fueron cercanas a cero. No hubo una adecuada representación \
                    de la distribución espacial de la precipitación; En las series \
                    de tiempo se observa como la magnitud observada con el radar \
                    (negro) es significativamente superior a lo largo de la semana. ', style1)


par4.wrap(770, 350)
par4.drawOn(pdf_rep4, 870., 405)

pdf_rep4.drawImage(path_elem+'pronostico_wrf/rainweek_08.png', \
                870., 595., 340., 320., mask = 'auto')

pdf_rep4.drawImage(path_elem+'pronostico_wrf/rainweek_02.png', \
                1290., 595., 360., 320., mask = 'auto')

pdf_rep4.drawImage(path_elem+'pronostico_wrf/evalmayo_01h_CCA002.png', \
                870., 155., 360., 240., mask = 'auto')

pdf_rep4.drawImage(path_elem+'pronostico_wrf/evalmayo_01h_CCA013.png', \
                1290., 155., 360., 240., mask = 'auto')


pdf_rep4.save()




# ---------------------------------------------------------------------------------------------
# Se hace el merge de los diferentes reportes generados
# ---------------------------------------------------------------------------------------------


#
file1 = file (path_reps+'precipitacion.pdf', 'rb')
file2 = file (path_reps+'niveles.pdf',  'rb')
# file3 = file (path_reps+'sensores_remotos.pdf', 'rb')
file4 = file (path_reps+'pronostico.pdf', 'rb')
#
page1 = PdfFileReader (file1).getPage (0)
page2 = PdfFileReader (file2).getPage (0)
# page3 = PdfFileReader (file3).getPage (0)
page4 = PdfFileReader (file4).getPage (0)
#
output = PdfFileWriter()
output.addPage(page1)
output.addPage(page2)
# output.addPage(page3)
output.addPage(page4)
output.write(file(path_reps+'HIDROMET_2017-07-01.pdf','w'))
