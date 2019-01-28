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

# # week  December 31th to January 6th
# data = [['Municipio',     'Zona alertada'                         ,'Fecha alerta','Hora Alerta'],
#         [u'Medellín',     u'Q. La Presidenta'                     ,'2019-01-06'  , '19:00'     ],
#         [u'Medellín',     u'Columna de humo en El Poblado'        ,'2019-01-03'  , '06:40'     ],
#         [u'Medellín',     u'Columna de humo en San Javier'        ,'2019-01-04'  , '15:10'     ],
#         [u'Medellín',     u'Columna de humo en S. Ant. de Prado'  ,'2019-01-01'  , '18:12'     ],
#         [u'Bello',        u'Columna de humo en cerro Quitasol'    ,'2019-01-01'  , '18:30'     ],
#         [u'Bello',        u'Columna de humo en Zamora'            ,'2019-01-01'  , '19:30'     ],
#         [u'Bello',        u'Columna de humo en barrio París'      ,'2019-01-02'  , '06:10'     ],
# ]
# # week  January 7th to 13th
# data = [['Municipio',     'Zona alertada'                         ,'Fecha alerta','Hora Alerta'],
#         [u'Medellín',     u'Q. Cañada Negra'                      ,'2019-01-08'  , '20:50'     ],
#         [u'Copacabana',   u'Río Medellín'                         ,'2019-01-08'  , '21:40'     ],
#         [u'Copacabana',   u'Río Medellín'                         ,'2019-01-08'  , '22:05'     ],
#         [u'Copacabana',   u'Río Medellín'                         ,'2019-01-08'  , '22:09'     ],
#         [u'Copacabana',   u'Río Medellín'                         ,'2019-01-08'  , '23:20'     ],
#        ]
# # week  January 14th to 20th
# data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta'],
#         [u'Medellín',     u'Columna de humo en San Javier'                      ,'2019-01-18'  , '15:50'     ],
#         [u'Medellín',     u'Columnas de humo en San Cristobal'                  ,'2019-01-19'  , '10:55'     ],
#        ]
# week  January 21th to 27th
data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta'],
        [u'Medellín',     u'Columna de humo en San Javier (El Salado)'          ,'2019-01-21'  , '16:30'     ],
        [u'Medellín',     u'Columna de humo en San Javier (El Salado)'          ,'2019-01-22'  , '10:48'     ],
        [u'Medellín',     u'Columna de humo en San Javier (El Socorro)'         ,'2019-01-24'  , '10:04'     ],
        [u'Medellín',     u'Columna de humo en San Javier (El Socorro)'         ,'2019-01-25'  , '11:45'     ],
        [u'Medellín',     u'Columna de humo en San Blas'                        ,'2019-01-23'  , '11:30'     ],
        [u'Medellín',     u'Columna de humo en San Cristobal'                   ,'2019-01-23'  , '13:48'     ],
        [u'Medellín',     u'Columna de humo en Bello Oriente'                   ,'2019-01-23'  , '18:00'     ],
        [u'Bello',        u'Columna de humo en el cerro Quitasol'               ,'2019-01-26'  , '16:15'     ],
       ]

# More width to zone column
# t=Table(data,[2*inch,1.7*inch,1.5*inch,3.5*inch,3*inch], len(data)*[0.4*inch])
t=Table(data,[2.0*inch,6.5*inch,1.7*inch,1.5*inch], len(data)*[0.4*inch])

# Muchas y fechas juntas
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
                       ('SPAN',   (0,1), (0,7)),\
                       ('VALIGN', (0,1), (0,7),'MIDDLE'),\
                       # # # zona
                       ('SPAN',   (1,1), (1,2)),\
                       ('VALIGN', (1,1), (1,2),'MIDDLE'),\
                       ('SPAN',   (1,3), (1,4)),\
                       ('VALIGN', (1,3), (1,4),'MIDDLE'),\
                       # # # # fecha
                       ('SPAN',   (2,5), (2,7)),\
                       ('VALIGN', (2,5), (2,7),'MIDDLE'),\
                       # # # hora
                       # ('SPAN',   (3,1), (3,2)),\
                       # ('VALIGN', (3,1), (3,2),'MIDDLE'),\
                        ]))


t.wrapOn(JuanMarica, 600, 890)
t.drawOn(JuanMarica, 50.,50.)

JuanMarica.save()


os.system('scp '+Path+'JuanMarica.pdf ccuervo@192.168.1.74:/var/www/cmcuervol/')


print 'Hello world'
