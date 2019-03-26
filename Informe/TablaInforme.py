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

# # week  February 25th to March 3th
# data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta'],
#         [u'Envigado',     u'Quebrada Ayurá'                                     ,'2019-02-28'  , '18:44'     ],
#         [u'Copacabana',   u'Río Medellín (Puente Machado)'                      ,'2019-02-28'  , '19:55'     ],
#         [u'Copacabana',   u'Río Medellín (Puente Machado)'                      ,'2019-02-26'  , '18:09'     ],
#         [u'Bello',        u'Río Medellín (Puente Machado)'                      ,'2019-02-26'  , '21:15'     ],
#         [u'Medellín',     u'Quebrada La Presidenta'                             ,'2019-02-26'  , '19:24'     ],
#         [u'Medellín',     u'Quebrada Malpaso'                                   ,'2019-02-26'  , '20:54'     ],
#         [u'Medellín',     u'Río Medellín (Puente La 33)'                        ,'2019-03-03'  , '16:23'     ],
#        ]
# # week  February 4th to March 10th
# data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta
#         [u'Medellín',     u'Quebrada La Picacha'                                ,'2019-03-10'  , '18:00'     ],
#         [u'Medellín',     u'Deprimido víal Bulerías'                            ,'2019-03-10'  , '18:10'     ],
#        ]
# # week  March 11th to  17th
# data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta'],
#         [u'Medellín',     u'Quebrada Altavista'                                 ,'2019-03-11'  , '16:00'     ],
#         [u'Medellín',     u'Río Medellín (Puente de la 33)'                     ,'2019-03-11'  , '16:15'     ],
#         [u'Medellín',     u'Quebrada El Chocho'                                 ,'2019-03-12'  , '16:45'     ],
#         [u'Medellín',     u'Quebrada La Guayabala'                              ,'2019-03-12'  , '16:49'     ],
#        ]
# week  March 18th to 24th
data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta'],
        [u'Itagüí',       u'Quebrada Doña María'                                ,'2019-03-19'  , '00:00'     ],
        [u'Medellín',     u'Río Medellín (Puente de la 33)'                     ,'2019-03-19'  , '01:02'     ],
        [u'Medellín',     u'Quebrada La Guayabala'                              ,'2019-03-19'  , '00:30'     ],
        [u'Medellín',     u'Quebrada La Presidenta'                             ,'2019-03-19'  , '01:02'     ],
        [u'Medellín',     u'Quebrada La Presidenta'                             ,'2019-03-24'  , '14:15'     ],
        [u'Medellín',     u'Quebrada La Presidenta'                             ,'2019-03-22'  , '15:02'     ],
        [u'Medellín',     u'Quebrada Altavista'                                 ,'2019-03-22'  , '17:23'     ],
        [u'Medellín',     u'Quebrada El Chocho'                                 ,'2019-03-20'  , '15:35'     ],
        [u'Medellín',     u'Río Medellín (Puente de La 33)'                     ,'2019-03-24'  , '13:59'     ],
        [u'Copacabana',   u'Río Medellín '                                      ,'2019-03-21'  , '16:09'     ],
        [u'Copacabana',   u'Río Medellín (Puente Fundadores)'                   ,'2019-03-21'  , '16:46'     ],
        [u'Copacabana',   u'Río Medellín (Puente Machado)'                      ,'2019-03-22'  , '18:18'     ],
        [u'Copacabana',   u'Río Medellín (Puente Machado)'                      ,'2019-03-19'  , '01:45'     ],
        [u'Bello',        u'Río Medellín (Puente Machado)'                      ,'2019-03-24'  , '15:30'     ],
        [u'Bello',        u'Quebrada Cañada Negra'                              ,'2019-03-24'  , '15:30'     ],
        [u'Bello',        u'Quebrada Cañada Negra'                              ,'2019-03-21'  , '16:02'     ],
        [u'Bello',        u'Quebrada La Madera'                                 ,'2019-03-21'  , '16:24'     ],
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
                       ('SPAN',   (0,2), (0,9)),\
                       ('VALIGN', (0,2), (0,9),'MIDDLE'),\
                       ('SPAN',   (0,10), (0,13)),\
                       ('VALIGN', (0,10), (0,13),'MIDDLE'),\
                       ('SPAN',   (0,14), (0,17)),\
                       ('VALIGN', (0,14), (0,17),'MIDDLE'),\
                       # # # zona
                       ('SPAN',   (1,4), (1,6)),\
                       ('VALIGN', (1,4), (1,6),'MIDDLE'),\
                       ('SPAN',   (1,12), (1,14)),\
                       ('VALIGN', (1,12), (1,14),'MIDDLE'),\
                       ('SPAN',   (1,15), (1,16)),\
                       ('VALIGN', (1,15), (1,16),'MIDDLE'),\
                       # # # # # fecha
                       ('SPAN',   (2,1), (2,4)),\
                       ('VALIGN', (2,1), (2,4),'MIDDLE'),\
                       ('SPAN',   (2,6), (2,7)),\
                       ('VALIGN', (2,6), (2,7),'MIDDLE'),\
                       ('SPAN',   (2,10), (2,11)),\
                       ('VALIGN', (2,10), (2,11),'MIDDLE'),\
                       ('SPAN',   (2,14), (2,15)),\
                       ('VALIGN', (2,14), (2,15),'MIDDLE'),\
                       ('SPAN',   (2,16), (2,17)),\
                       ('VALIGN', (2,16), (2,17),'MIDDLE'),\
                       # # # hora
                       ('SPAN',   (3,14), (3,15)),\
                       ('VALIGN', (3,14), (3,15),'MIDDLE'),\
                        ]))


t.wrapOn(JuanMarica, 600, 890)
t.drawOn(JuanMarica, 50.,50.)

JuanMarica.save()


os.system('scp '+Path+'JuanMarica.pdf ccuervo@192.168.1.74:/var/www/cmcuervol/')


print 'Hello world'
