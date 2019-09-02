#!/usr/bin/env python
# encoding: utf-8
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import letter, inch
# from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table
# from reportlab.lib.styles import getSampleStyleSheet
import os
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

Path_fuentes = '/home/cmcuervol/Fuentes/'
Path = '/home/cmcuervol/Desktop/MapasInforme/'

# Colors for graphics SIATA style
gris70 = (112/255., 111/255., 111/255.)

ColorInfo1 = (82 /255., 183/255.,196/255.)
ColorInfo2 = (55 /255., 123/255.,148/255.)
ColorInfo3 = (43 /255.,  72/255.,105/255.)
ColorInfo4 = (32 /255.,  34/255., 72/255.)
ColorInfo5 = (34 /255.,  71/255., 94/255.)
ColorInfo6 = (31 /255., 115/255.,116/255.)
ColorInfo7 = (39 /255., 165/255.,132/255.)
ColorInfo8 = (139/255., 187/255.,116/255.)
ColorInfo9 = (200/255., 209/255., 93/255.)
ColorInfo10 =(249/255., 230/255., 57/255.)


AzulChimba =( 55/255., 132/255., 251/255.)
AzulChimbita =( 16/255., 108/255., 214/255.)
VerdeChimba =(  9/255., 210/255.,  97/255.)
Azul =( 96/255., 200/255., 247/255.)
Naranja =( 240/255., 108/255.,  34/255.)
RojoChimba =( 240/255., 84/255.,  107/255.)
Verdecillo =( 40/255., 225/255.,  200/255.)
Azulillo =( 55/255., 150/255.,  220/255.)


# Types of fonts Avenir
#
AvenirHeavy = fm.FontProperties(fname=Path_fuentes+'AvenirLTStd-Heavy.otf')
AvenirBook  = fm.FontProperties(fname=Path_fuentes+'AvenirLTStd-Book.otf')
AvenirBlack = fm.FontProperties(fname=Path_fuentes+'AvenirLTStd-Black.otf')
AvenirRoman = fm.FontProperties(fname=Path_fuentes+'AvenirLTStd-Roman.ttf')

barcode_font = Path_fuentes+'AvenirLTStd-Roman.ttf'
pdfmetrics.registerFont(TTFont("Avenir", barcode_font))
# barcode_font_blk = Path_fuentes+'AvenirLTStd-Black.otf'
# pdfmetrics.registerFont(TTFont("Avenir_blk", barcode_font_blk))

sizey, sizex = A2
JuanMarica = canvas.Canvas(Path+'JuanMarica.pdf')
JuanMarica.setPageSize((sizex, sizey))

JuanMarica.setFont("Avenir", 24)


# # # week to July 29th to August 4th
# data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta'  ],
#         [u'Medellín',     u'Columna de humo en San Javier - El Salado'          ,'2019-07-30'  , '13:40'       ],
#         [u'Medellín',     u'Columna de humo en Santa Elena - Las Palmas'        ,'2019-07-31'  , '09:23'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal'                   ,'2019-08-01'  , '17:00'       ],
#         [u'Medellín',     u'Columna de humo en Las Estancias'                   ,'2019-08-02'  , '10:57'       ],
#        ]
# # # week to August 5th to 11th
# data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta'  ],
#         [u'Medellín',     u'Columna de humo en Blanquizal'                      ,'2019-08-05'  , '12:05'       ],
#         [u'Medellín',     u'Columna de humo entre San Javier y San Cristóbal'   ,'2019-08-06'  , '12:00'       ],
#         [u'Medellín',     u'Incendio forestal en San Cristóbal - La Frisolera'  ,'2019-08-09'  , '16:50'       ],
#         [u'Medellín',     u'Columna de humo en San Germán'                      ,'2019-08-09'  , '13:30'       ],
#         [u'Bello',        u'Columna de humo en Nueva Jerusalen'                 ,'2019-08-08'  , '13:39'       ],
#        ]
# # week to August 12th to 18th
# data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta'  ],
#         [u'Medellín',     u'Columna de humo en Pedregal Alto'                   ,'2019-08-12'  , '11:30'       ],
#         [u'Medellín',     u'Columna de humo en La Cruz'                         ,'2019-08-12'  , '13:26'       ],
#         [u'Medellín',     u'Columna de humo en Calasanz'                        ,'2019-08-12'  , '13:59'       ],
#         [u'Medellín',     u'Columna de humo en Robledo'                         ,'2019-08-12'  , '14:30'       ],
#         [u'Medellín',     u'Columna de humo en Belen Las Violetas'              ,'2019-08-12'  , '15:52'       ],
#         [u'Medellín',     u'Columna de humo en San Javier (Antonio Nariño)'     ,'2019-08-12'  , '12:59'       ],
#         [u'Medellín',     u'Columna de humo en San Javier (El Salado)'          ,'2019-08-13'  , '10:16'       ],
#         [u'Medellín',     u'Columna de humo en La Asomadera'                    ,'2019-08-13'  , '10:16'       ],
#         [u'Medellín',     u'Columna de humo entre Pedregal y San Cristóbal'     ,'2019-08-13'  , '11:28'       ],
#         [u'Medellín',     u'Columna de humo en Altavista'                       ,'2019-08-13'  , '15:29'       ],
#         [u'Medellín',     u'Columna de humo en Altavista'                       ,'2019-08-16'  , '15:05'       ],
#         [u'Medellín',     u'Columna de humo en Altavista'                       ,'2019-08-18'  , '13:12'       ],
#         [u'Medellín',     u'Columna de humo en Altavista'                       ,'2019-08-14'  , '13:00'       ],
#         [u'Medellín',     u'Columna de humo en Manrique'                        ,'2019-08-14'  , '10:00'       ],
#         [u'Medellín',     u'Columna de humo en el cerro Pan de Azúcar'          ,'2019-08-15'  , '10:45'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal'                   ,'2019-08-15'  , '12:28'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal'                   ,'2019-08-15'  , '14:11'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal'                   ,'2019-08-13'  , '15:14'       ],
#         [u'La Estrella',  u'Columna de humo en vereda La Culebra'               ,'2019-08-13'  , '12:55'       ],
#        ]
# # # week to August 19th to 25th
# data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta'  ],
#         [u'Sabaneta',     u'Columna de humo en sector Mayorca'                  ,'2019-08-25'  , '08:45'       ],
#         [u'Bello',        u'Columna de humo en El barrio París'                 ,'2019-08-25'  , '13:12'       ],
#         [u'Bello',        u'Columna de humo en el suroccidente de Bello'        ,'2019-08-22'  , '11:34'       ],
#         [u'Bello',        u'Columna de humo en vereda El Potrerito'             ,'2019-08-24'  , '10:32'       ],
#         [u'Bello',        u'Columna de humo en La comuna 9'                     ,'2019-08-19'  , '15:53'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal - La Loma'         ,'2019-08-19'  , '11:05'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal'                   ,'2019-08-22'  , '15:32'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal - El Morro'        ,'2019-08-23'  , '16:55'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal - Pedregal Alto'   ,'2019-08-21'  , '09:31'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal - Pedregal Alto'   ,'2019-08-21'  , '11:04'       ],
#         [u'Medellín',     u'Columna de humo en el Cerro El Volador'             ,'2019-08-21'  , '09:31'       ],
#         [u'Medellín',     u'Columna de humo en el Cerro de Las Tres Cruces'     ,'2019-08-21'  , '11:20'       ],
#         [u'Medellín',     u'Columna de humo en el Cerro de Las Tres Cruces'     ,'2019-08-21'  , '13:06'       ],
#         [u'Medellín',     u'Columna de humo en Santa Margarita'                 ,'2019-08-20'  , '13:28'       ],
#         [u'Medellín',     u'Columna de humo en Santa Elena - Piedras Blancas'   ,'2019-08-20'  , '13:19'       ],
#         [u'Medellín',     u'Columna de humo en Santa Elena - Piedras Blancas'   ,'2019-08-20'  , '20:50'       ],
#         [u'Medellín',     u'Columna de humo en Santa Elena'                     ,'2019-08-22'  , '06:28'       ],
#         [u'Medellín',     u'Columna de humo en Santa Elena'                     ,'2019-08-22'  , '10:37'       ],
#         [u'Medellín',     u'Columna de humo en Altavista'                       ,'2019-08-22'  , '15:32'       ],
#         [u'Medellín',     u'Columna de humo en Altavista'                       ,'2019-08-22'  , '16:27'       ],
#         [u'Medellín',     u'Columna de humo en Altavista'                       ,'2019-08-22'  , '18:13'       ],
#         [u'Medellín',     u'Columna de humo en Altavista'                       ,'2019-08-23'  , '10:26'       ],
#         [u'Medellín',     u'Columna de humo en Belen Las Violetas'              ,'2019-08-23'  , '08:00'       ],
#         [u'Medellín',     u'Columna de humo en La Alpujarra'                    ,'2019-08-23'  , '12:52'       ],
#         [u'Medellín',     u'Columna de humo en El Picacho'                      ,'2019-08-25'  , '12:48'       ],
#        ]
# # week to August 26th to September 1st

data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta'  ],
        [u'Medellín',     u'Columna de humo en el Cerro de Las Tres Cruces'     ,'2019-08-26'  , '11:30'       ],
        [u'Medellín',     u'Columna de humo en Villa Flora'                     ,'2019-08-26'  , '13:00'       ],
        [u'Medellín',     u'Columna de humo en San Cristóbal - Pedregal Alto'   ,'2019-08-26'  , '12:13'       ],
        [u'Medellín',     u'Columna de humo en San Cristóbal - Pedregal Alto'   ,'2019-08-28'  , '14:40'       ],
        [u'Medellín',     u'Columna de humo en San Cristóbal - Pedregal Alto'   ,'2019-08-29'  , '14:01'       ],
        [u'Medellín',     u'Columna de humo en San Javier'                      ,'2019-08-29'  , '14:01'       ],
        [u'Medellín',     u'Columna de humo en San Javier - El Salado'          ,'2019-08-30'  , '15:00'       ],
        [u'Medellín',     u'Columna de humo en sector El Corazón'               ,'2019-08-30'  , '16:31'       ],
        [u'Medellín',     u'Columna de humo en San Javier-Nuevos Conquistadores','2019-08-31'  , '12:04'       ],
        [u'Medellín',     u'Columna de humo en San José La Cima Nº2'            ,'2019-08-31'  , '13:00'       ],
        [u'Medellín',     u'Columna de humo en Belencito Corazón'               ,'2019-08-31'  , '18:00'       ],
        [u'Medellín',     u'Columna de humo en Altavista'                       ,'2019-08-31'  , '12:51'       ],
        [u'Medellín',     u'Columna de humo en Altavista'                       ,'2019-08-28'  , '14:26'       ],
        [u'Medellín',     u'Columna de humo en Altavista'                       ,'2019-08-28'  , '14:47'       ],
        [u'Medellín',     u'Columna de humo en Altavista'                       ,'2019-08-29'  , '12:01'       ],
        [u'Medellín',     u'Columna de humo en Altavista'                       ,'2019-08-29'  , '14:11'       ],
        [u'Medellín',     u'Columna de humo en Belén - Las Violetas'            ,'2019-08-27'  , '12:57'       ],
        [u'Medellín',     u'Columna de humo en el Cerro El Volador'             ,'2019-08-27'  , '09:12'       ],
        [u'Medellín',     u'Columna de humo en el Cerro El Volador'             ,'2019-09-01'  , '09:35'       ],
        [u'Medellín',     u'Columna de humo en Seminario Mayor'                 ,'2019-09-01'  , '16:42'       ],
        [u'Medellín',     u'Columna de humo en Pajarito'                        ,'2019-08-30'  , '17:20'       ],
        [u'Medellín',     u'Columna de humo en Pajarito'                        ,'2019-08-30'  , '11:30'       ],
        [u'Medellín',     u'Columna de humo en Santa Elena - Piedras Blancas'   ,'2019-08-30'  , '10:00'       ],
        [u'Medellín',     u'Columna de humo en Santa Elena - Piedras Blancas'   ,'2019-08-28'  , '16:47'       ],
        [u'Medellín',     u'Columna de humo en Santa Elena'                     ,'2019-08-28'  , '11:30'       ],
        [u'Medellín',     u'Columna de humo en La Cruz'                         ,'2019-08-28'  , '16:47'       ],
        [u'Medellín',     u'Columna de humo en La Cruz'                         ,'2019-08-27'  , '10:50'       ],
        [u'Medellín',     u'Columna de humo en La Cruz'                         ,'2019-08-29'  , '09:12'       ],
        [u'Medellín',     u'Columna de humo en Cerro Pan de Azúcar'             ,'2019-08-29'  , '09:12'       ],
        [u'Medellín',     u'Columna de humo en Cerro Pan de Azúcar'             ,'2019-08-29'  , '11:35'       ],
        [u'Medellín',     u'Columna de humo en Cerro Pan de Azúcar'             ,'2019-08-30'  , '16:05'       ],
        [u'Medellín',     u'Columna de humo en El Socorro'                      ,'2019-08-30'  , '09:50'       ],
        [u'Medellín',     u'Columna de humo en el barrio Monte Claro'           ,'2019-08-30'  , '14:20'       ],
        [u'Medellín',     u'Columna de humo en el barrio Monte Claro'           ,'2019-08-29'  , '14:04'       ],
        [u'Copacabana',   u'Columna de humo en Las Salinas'                     ,'2019-08-29'  , '15:59'       ],
        [u'Copacabana',   u'Columna de humo en Autopista Norte'                 ,'2019-09-01'  , '10:50'       ],
        [u'Girardota',    u'Columna de humo en la vía El Barro'                 ,'2019-08-29'  , '13:52'       ],
        [u'Itagüí',       u'Columna de humo en Itagüí'                          ,'2019-08-30'  , '11:00'       ],
        [u'Bello',        u'Columna de humo en Niquia'                          ,'2019-08-31'  , '14:58'       ],
       ]


# More width to zone column
# t=Table(data,[2*inch,1.7*inch,1.5*inch,3.5*inch,3*inch], len(data)*[0.4*inch])
t=Table(data,[2.0*inch,6.5*inch,1.7*inch,1.5*inch], len(data)*[0.4*inch])

t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),\
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),\
                       ('ALIGN',(0,0),(-1,-1),'CENTER'),\
                       ('ALIGN',(1,1),(1,-1),'LEFT'),\
                       # ('VALIGN',(0,0),(-1,-1),'MIDDLE'),\
                       ('VALIGN',(0,0),(-1,-1),'TOP'),\
                       ('VALIGN',(0,0),(-1,0),'TOP'),\
                       ('FONTSIZE', (0, 0), (-1, 1), 20),\
                       ('BACKGROUND',(0,0),(-1,0),ColorInfo6),\
                       ('FONTSIZE', (0, 1), (-1, -1), 18),\
                       ('TEXTCOLOR',(0, 0),(-1,0),colors.white),\
                       # # # Municipio
                       ('SPAN',   (0,1),  (0,34)),\
                       ('VALIGN', (0,1),  (0,34),'MIDDLE'),\
                       ('SPAN',   (0,35), (0,36)),\
                       ('VALIGN', (0,35), (0,36),'MIDDLE'),\
                       # # # zona
                       ('SPAN',   (1,3),  (1,5)),\
                       ('VALIGN', (1,3),  (1,5),'MIDDLE'),\
                       ('SPAN',   (1,12), (1,16)),\
                       ('VALIGN', (1,12), (1,16),'MIDDLE'),\
                       ('SPAN',   (1,18), (1,19)),\
                       ('VALIGN', (1,18), (1,19),'MIDDLE'),\
                       ('SPAN',   (1,21), (1,22)),\
                       ('VALIGN', (1,21), (1,22),'MIDDLE'),\
                       ('SPAN',   (1,23), (1,24)),\
                       ('VALIGN', (1,23), (1,24),'MIDDLE'),\
                       ('SPAN',   (1,26), (1,28)),\
                       ('VALIGN', (1,26), (1,28),'MIDDLE'),\
                       ('SPAN',   (1,29), (1,31)),\
                       ('VALIGN', (1,29), (1,31),'MIDDLE'),\
                       ('SPAN',   (1,33), (1,34)),\
                       ('VALIGN', (1,33), (1,34),'MIDDLE'),\
                       # # # # # fecha
                       ('SPAN',   (2,1), (2,3)),\
                       ('VALIGN', (2,1), (2,3),'MIDDLE'),\
                       ('SPAN',   (2,5), (2,6)),\
                       ('VALIGN', (2,5), (2,6),'MIDDLE'),\
                       ('SPAN',   (2,7), (2,8)),\
                       ('VALIGN', (2,7), (2,8),'MIDDLE'),\
                       ('SPAN',   (2,9), (2,12)),\
                       ('VALIGN', (2,9), (2,12),'MIDDLE'),\
                       ('SPAN',   (2,13),(2,14)),\
                       ('VALIGN', (2,13),(2,14),'MIDDLE'),\
                       ('SPAN',   (2,15),(2,16)),\
                       ('VALIGN', (2,15),(2,16),'MIDDLE'),\
                       ('SPAN',   (2,17),(2,18)),\
                       ('VALIGN', (2,17),(2,18),'MIDDLE'),\
                       ('SPAN',   (2,19),(2,20)),\
                       ('VALIGN', (2,19),(2,20),'MIDDLE'),\
                       ('SPAN',   (2,21),(2,23)),\
                       ('VALIGN', (2,21),(2,23),'MIDDLE'),\
                       ('SPAN',   (2,28),(2,30)),\
                       ('VALIGN', (2,28),(2,30),'MIDDLE'),\
                       ('SPAN',   (2,31),(2,33)),\
                       ('VALIGN', (2,31),(2,33),'MIDDLE'),\
                       ('SPAN',   (2,34),(2,35)),\
                       ('VALIGN', (2,34),(2,35),'MIDDLE'),\
                       # # hora
                       ('SPAN',   (3,5), (3,6)),\
                       ('VALIGN', (3,5), (3,6),'MIDDLE'),\
                       ('SPAN',   (3,28), (3,29)),\
                       ('VALIGN', (3,28), (3,29),'MIDDLE'),\
                        ]))


t.wrapOn(JuanMarica, 600, 890)
t.drawOn(JuanMarica, 25.,25.)

JuanMarica.save()


os.system('scp '+Path+'JuanMarica.pdf ccuervo@192.168.1.74:/var/www/cmcuervol/')


print 'Hello world'
