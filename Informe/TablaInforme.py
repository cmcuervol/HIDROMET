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


# # # week to August 26th to September 1st
# data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta'  ],
#         [u'Medellín',     u'Columna de humo en el Cerro de Las Tres Cruces'     ,'2019-08-26'  , '11:30'       ],
#         [u'Medellín',     u'Columna de humo en Villa Flora'                     ,'2019-08-26'  , '13:00'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal - Pedregal Alto'   ,'2019-08-26'  , '12:13'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal - Pedregal Alto'   ,'2019-08-28'  , '14:40'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal - Pedregal Alto'   ,'2019-08-29'  , '14:01'       ],
#         [u'Medellín',     u'Columna de humo en San Javier'                      ,'2019-08-29'  , '14:01'       ],
#         [u'Medellín',     u'Columna de humo en San Javier - El Salado'          ,'2019-08-30'  , '15:00'       ],
#         [u'Medellín',     u'Columna de humo en sector El Corazón'               ,'2019-08-30'  , '16:31'       ],
#         [u'Medellín',     u'Columna de humo en San Javier-Nuevos Conquistadores','2019-08-31'  , '12:04'       ],
#         [u'Medellín',     u'Columna de humo en San José La Cima Nº2'            ,'2019-08-31'  , '13:00'       ],
#         [u'Medellín',     u'Columna de humo en Belencito Corazón'               ,'2019-08-31'  , '18:00'       ],
#         [u'Medellín',     u'Columna de humo en Altavista'                       ,'2019-08-31'  , '12:51'       ],
#         [u'Medellín',     u'Columna de humo en Altavista'                       ,'2019-08-28'  , '14:26'       ],
#         [u'Medellín',     u'Columna de humo en Altavista'                       ,'2019-08-28'  , '14:47'       ],
#         [u'Medellín',     u'Columna de humo en Altavista'                       ,'2019-08-29'  , '12:01'       ],
#         [u'Medellín',     u'Columna de humo en Altavista'                       ,'2019-08-29'  , '14:11'       ],
#         [u'Medellín',     u'Columna de humo en Belén - Las Violetas'            ,'2019-08-27'  , '12:57'       ],
#         [u'Medellín',     u'Columna de humo en el Cerro El Volador'             ,'2019-08-27'  , '09:12'       ],
#         [u'Medellín',     u'Columna de humo en el Cerro El Volador'             ,'2019-09-01'  , '09:35'       ],
#         [u'Medellín',     u'Columna de humo en Seminario Mayor'                 ,'2019-09-01'  , '16:42'       ],
#         [u'Medellín',     u'Columna de humo en Pajarito'                        ,'2019-08-30'  , '17:20'       ],
#         [u'Medellín',     u'Columna de humo en Pajarito'                        ,'2019-08-30'  , '11:30'       ],
#         [u'Medellín',     u'Columna de humo en Santa Elena - Piedras Blancas'   ,'2019-08-30'  , '10:00'       ],
#         [u'Medellín',     u'Columna de humo en Santa Elena - Piedras Blancas'   ,'2019-08-28'  , '16:47'       ],
#         [u'Medellín',     u'Columna de humo en Santa Elena'                     ,'2019-08-28'  , '11:30'       ],
#         [u'Medellín',     u'Columna de humo en La Cruz'                         ,'2019-08-28'  , '16:47'       ],
#         [u'Medellín',     u'Columna de humo en La Cruz'                         ,'2019-08-27'  , '10:50'       ],
#         [u'Medellín',     u'Columna de humo en La Cruz'                         ,'2019-08-29'  , '09:12'       ],
#         [u'Medellín',     u'Columna de humo en Cerro Pan de Azúcar'             ,'2019-08-29'  , '09:12'       ],
#         [u'Medellín',     u'Columna de humo en Cerro Pan de Azúcar'             ,'2019-08-29'  , '11:35'       ],
#         [u'Medellín',     u'Columna de humo en Cerro Pan de Azúcar'             ,'2019-08-30'  , '16:05'       ],
#         [u'Medellín',     u'Columna de humo en El Socorro'                      ,'2019-08-30'  , '09:50'       ],
#         [u'Medellín',     u'Columna de humo en el barrio Monte Claro'           ,'2019-08-30'  , '14:20'       ],
#         [u'Medellín',     u'Columna de humo en el barrio Monte Claro'           ,'2019-08-29'  , '14:04'       ],
#         [u'Copacabana',   u'Columna de humo en Las Salinas'                     ,'2019-08-29'  , '15:59'       ],
#         [u'Copacabana',   u'Columna de humo en Autopista Norte'                 ,'2019-09-01'  , '10:50'       ],
#         [u'Girardota',    u'Columna de humo en la vía El Barro'                 ,'2019-08-29'  , '13:52'       ],
#         [u'Itagüí',       u'Columna de humo en Itagüí'                          ,'2019-08-30'  , '11:00'       ],
#         [u'Bello',        u'Columna de humo en Niquia'                          ,'2019-08-31'  , '14:58'       ],
#        ]

# # # week to September 2nd to 8th
# data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta'  ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal - La Loma'         ,'2019-09-02'  , '07:09'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal - La Loma'         ,'2019-09-06'  , '14:36'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal - La Loma'         ,'2019-09-06'  , '15:43'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal - La Loma'         ,'2019-09-08'  , '06:05'       ],
#         [u'Medellín',     u'Columna de humo en El Cucaracho'                    ,'2019-09-08'  , '10:34'       ],
#         [u'Medellín',     u'Columna de humo en Pajarito'                        ,'2019-09-08'  , '11:37'       ],
#         [u'Medellín',     u'Columna de humo en Pajarito'                        ,'2019-09-08'  , '15:50'       ],
#         [u'Medellín',     u'Columna de humo en La Cruz'                         ,'2019-09-08'  , '15:53'       ],
#         [u'Medellín',     u'Columna de humo en Altavista - El Corazón'          ,'2019-09-08'  , '15:50'       ],
#         [u'Medellín',     u'Columna de humo en Altavista - vereda Buga'         ,'2019-09-02'  , '14:11'       ],
#         [u'Medellín',     u'Columna de humo en Altavista - vereda San Pablo'    ,'2019-09-02'  , '15:56'       ],
#         [u'Medellín',     u'Columna de humo en Altavista - vereda El Jardín'    ,'2019-09-05'  , '15:22'       ],
#         [u'Medellín',     u'Columna de humo en Altavista - vereda San José'     ,'2019-09-08'  , '11:31'       ],
#         [u'Medellín',     u'Columna de humo en Belén - Los Alpes'               ,'2019-09-08'  , '11:31'       ],
#         [u'Medellín',     u'Columna de humo en San Javier'                      ,'2019-09-08'  , '15:33'       ],
#         [u'Medellín',     u'Columna de humo en San Javier - El Salado'          ,'2019-09-02'  , '15:10'       ],
#         [u'Medellín',     u'Columna de humo en San Javier - El Pesebre'         ,'2019-09-05'  , '16:30'       ],
#         [u'Medellín',     u'Columna de humo en Quinta Linda'                    ,'2019-09-05'  , '14:48'       ],
#         [u'Medellín',     u'Columna de humo en Quinta Linda'                    ,'2019-09-06'  , '14:12'       ],
#         [u'Medellín',     u'Columna de humo en barrio Oriente'                  ,'2019-09-06'  , '15:28'       ],
#         [u'Medellín',     u'Columna de humo en La Sierra'                       ,'2019-09-04'  , '10:49'       ],
#         [u'Medellín',     u'Columna de humo en La Hondonada'                    ,'2019-09-03'  , '10:33'       ],
#         [u'Medellín',     u'Columna de humo en Llanaditas'                      ,'2019-09-03'  , '11:55'       ],
#         [u'Medellín',     u'Columna de humo en Santa Elena - El Mazo'           ,'2019-09-03'  , '12:00'       ],
#         [u'Medellín',     u'Columna de humo en el Cerro de Las Tres Cruces'     ,'2019-09-03'  , '15:53'       ],
#         [u'Medellín',     u'Columna de humo en el Cerro de Las Tres Cruces'     ,'2019-09-08'  , '16:34'       ],
#         [u'Medellín',     u'Columna de humo en el Cerro de Las Tres Cruces'     ,'2019-09-05'  , '21:40'       ],
#         [u'Itagüí',       u'Columna de humo en la vereda Ajizal'                ,'2019-09-05'  , '17:02'       ],
#         [u'Itagüí',       u'Columna de humo en la vereda Los Gómez'             ,'2019-09-03'  , '15:08'       ],
#         [u'Girardota',    u'Columna de humo en la ladera sur'                   ,'2019-09-03'  , '14:12'       ],
#         [u'Bello',        u'Columna de humo en Autopista Medellín Bogotá'       ,'2019-09-03'  , '18:20'       ],
#        ]
# # # week to September 9th to 15th
# data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta'  ],
#         [u'Medellín',     u'Columna de humo en el Cerro Pan de Azúcar'          ,'2019-09-09'  , '07:34'       ],
#         [u'Medellín',     u'Columna de humo en Villa Hermosa'                   ,'2019-09-09'  , '13:50'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal - Boquerón'        ,'2019-09-11'  , '14:00'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal - cerro San Pedro' ,'2019-09-12'  , '15:52'       ],
#         [u'Medellín',     u'Columna de humo en Santa Elena'                     ,'2019-09-12'  , '11:56'       ],
#         [u'Girardota',    u'Columna de humo en Vía San Esteban'                 ,'2019-09-12'  , '12:13'       ],
#         [u'Caldas',       u'Columna de humo en La Valeria'                      ,'2019-09-11'  , '15:27'       ],
#        ]
# # # week to September 16th to 22nd
# data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta'  ],
#         [u'Medellín',     u'Río Medellín Puente de La Aguacatala'               ,'2019-09-18'  , '09:39'       ],
#         [u'Medellín',     u'Río Medellín Puente Aula Ambiental'                 ,'2019-09-18'  , '09:39'       ],
#         [u'Medellín',     u'Río Medellín Puente de La 33'                       ,'2019-09-22'  , '21:00'       ],
#         [u'Medellín',     u'Río Medellín Puente de Machado'                     ,'2019-09-22'  , '21:56'       ],
#        ]
# # # week to September 23rd to 29th
# data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta'  ],
#         [u'Medellín',     u'Quebrada Santa Elena'                               ,'2019-09-25'  , '14:40'       ],
#         [u'Medellín',     u'Columna de humo en Altavista (Patio-bolas)'         ,'2019-09-27'  , '15:08'       ],
#        ]
# # week to September 30th to October 6th
data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta'  ],
        [u'Medellín',     u'Columna de humo en San Cristóbal (La Loma)'         ,'2019-10-01'  , '12:20'       ],
        [u'Medellín',     u'Columna de humo en Altavista'                       ,'2019-10-03'  , '14:16'       ],
        [u'Medellín',     u'Quebrada Santa Elena'                               ,'2019-09-30'  , '15:23'       ],
        [u'Medellín',     u'Columna de humo en San Cristóbal (Pedregal Alto)'   ,'2019-09-30'  , '15:40'       ],
        [u'Medellín',     u'Río Medellín (Puente de La 33)'                     ,'2019-09-30'  , '22:12'       ],
        [u'Bello',        u'Río Medellín (Puente Machado)'                      ,'2019-09-30'  , '22:15'       ],
        [u'Bello',        u'Quebrada El Hato'                                   ,'2019-10-05'  , '20:15'       ],
        [u'Bello',        u'Quebrada La Loca (El Cafetal)'                      ,'2019-10-05'  , '20:15'       ],
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
                       ('SPAN',   (0,1),  (0,5)),\
                       ('VALIGN', (0,1),  (0,5),'MIDDLE'),\
                       ('SPAN',   (0,6),  (0,8)),\
                       ('VALIGN', (0,6),  (0,8),'MIDDLE'),\
                       # # # zona
                       # ('SPAN',   (1,1),  (1,4)),\
                       # ('VALIGN', (1,1),  (1,4),'MIDDLE'),\
                       # # # # fecha
                       ('SPAN',   (2,3), (2,6)),\
                       ('VALIGN', (2,3), (2,6),'MIDDLE'),\
                       ('SPAN',   (2,7), (2,8)),\
                       ('VALIGN', (2,7), (2,8),'MIDDLE'),\
                       # hora
                       ('SPAN',   (3,7),(3,8)),\
                       ('VALIGN', (3,7),(3,8),'MIDDLE'),\
                        ]))


t.wrapOn(JuanMarica, 600, 890)
t.drawOn(JuanMarica, 25.,25.)

JuanMarica.save()


os.system('scp '+Path+'JuanMarica.pdf ccuervo@192.168.1.74:/var/www/cmcuervol/')


print 'Hello world'
