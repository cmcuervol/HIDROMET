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

# ]
# Semana del 5 al 11 de noviembre
data = [['Municipio',     'Zona alertada'                         ,'Fecha alerta','Hora Alerta'],
        [u'Caldas',       u'Río Medellín (sector La Clara)'       ,'2018-11-20'  , '03:16'     ],
        [u'Copacabana',   u'Río Medellín (Puente Fundadores)'     ,'2018-11-25'  , '20:08'     ],
        [u'Barbosa',      u'Río Medellín (El Hatillo)'            ,'2018-11-25'  , '20:16'     ],
        [u'Itagüí',       u'Q. El Tablazo'                        ,'2018-11-25'  , '18:03'     ],
        [u'Itagüí',       u'Q. Doña María'                        ,'2018-11-22'  , '16:54'     ],
        [u'Itagüí',       u'Q. Doña María'                        ,'2018-11-25'  , '18:37'     ],
        [u'Medellín',     u'Q. Doña María'                        ,'2018-11-25'  , '17:31'     ],
        [u'Medellín',     u'Q. Doña María'                        ,'2018-11-20'  , '15:20'     ],
        [u'Medellín',     u'Q. Doña María'                        ,'2018-11-24'  , '18:21'     ],
        [u'Medellín',     u'Q. Doña María'                        ,'2018-11-22'  , '16:40'     ],
        [u'Medellín',     u'Q. La Zuñiga'                         ,'2018-11-22'  , '16:05'     ],
        [u'Medellín',     u'Q. La Presidenta'                     ,'2018-11-21'  , '14:32'     ],
        [u'Medellín',     u'Q. La Presidenta'                     ,'2018-11-24'  , '22:54'     ],
        [u'Medellín',     u'Q. La Presidenta'                     ,'2018-11-23'  , '01:30'     ],
        [u'Medellín',     u'Q. La Guayabala'                      ,'2018-11-23'  , '02:00'     ],
        [u'Medellín',     u'Q. La Guayabala'                      ,'2018-11-25'  , '17:55'     ],
        [u'Medellín',     u'Q. El Chocho'                         ,'2018-11-25'  , '18:20'     ],
        [u'Medellín',     u'Q. Malpaso'                           ,'2018-11-25'  , '18:44'     ],
        [u'Medellín',     u'Q. La Picacha'                        ,'2018-11-24'  , '18:31'     ],
        [u'La Estrella',  u'Q. La Raya'                           ,'2018-11-24'  , '16:57'     ],
        [u'Bello',        u'Q. El Hato'                           ,'2018-11-24'  , '20:35'     ],
        [u'Bello',        u'Q. El Hato'                           ,'2018-11-24'  , '21:18'     ],
        [u'Bello',        u'Q. El Hato'                           ,'2018-11-24'  , '21:23'     ],
        [u'Bello',        u'Q. El Hato'                           ,'2018-11-25'  , '15:51'     ],
        [u'Bello',        u'Q. El Hato'                           ,'2018-11-25'  , '18:53'     ],
        [u'Bello',        u'Q. El Hato'                           ,'2018-11-25'  , '19:04'     ],
        [u'Bello',        u'Q. La Loca'                           ,'2018-11-24'  , '22:37'     ],
        [u'Bello',        u'Q. La Loca'                           ,'2018-11-25'  , '18:53'     ],
        [u'Bello',        u'Q. La Loca'                           ,'2018-11-25'  , '18:56'     ],
        [u'Bello',        u'Q. La Madera'                         ,'2018-11-25'  , '18:53'     ],
        [u'Sabaneta',     u'Q. La Doctora'                        ,'2018-11-25'  , '16:12'     ],
        [u'Sabaneta',     u'Q. La Sabanetica'                     ,'2018-11-24'  , '23:05'     ],
]


# t=Table(data,[2*inch,1.7*inch,1.5*inch,3.5*inch,3*inch], len(data)*[0.4*inch])
t=Table(data,[2.0*inch,4.5*inch,1.7*inch,1.5*inch], len(data)*[0.4*inch])

# Muchas y fechas juntas
t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),\
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),\
                       ('ALIGN',(0,0),(-1,-1),'CENTER'),\
                       # ('VALIGN',(0,0),(-1,-1),'MIDDLE'),\
                       ('VALIGN',(0,0),(-1,-1),'TOP'),\
                       ('VALIGN',(0,0),(-1,0),'TOP'),\
                       ('FONTSIZE', (0, 0), (-1, 1), 20),\
                       ('BACKGROUND',(0,0),(-1,0),ColorInfo6),\
                       ('FONTSIZE', (0, 1), (-1, -1), 18),\
                       ('TEXTCOLOR',(0, 0),(-1,0),colors.white),\
                       # # # Municipio
                       ('SPAN',   (0,4), (0,6)),\
                       ('VALIGN', (0,4), (0,6),'MIDDLE'),\
                       ('SPAN',   (0,7), (0,19)),\
                       ('VALIGN', (0,7), (0,19),'MIDDLE'),\
                       ('SPAN',   (0,21), (0,30)),\
                       ('VALIGN', (0,21), (0,30),'MIDDLE'),\
                       ('SPAN',   (0,31), (0,32)),\
                       ('VALIGN', (0,31), (0,32),'MIDDLE'),\
                       # # # zona
                       ('SPAN',   (1,5), (1,10)),\
                       ('VALIGN', (1,5), (1,10),'MIDDLE'),\
                       ('SPAN',   (1,12), (1,14)),\
                       ('VALIGN', (1,12), (1,14),'MIDDLE'),\
                       ('SPAN',   (1,15), (1,16)),\
                       ('VALIGN', (1,15), (1,16),'MIDDLE'),\
                       ('SPAN',   (1,21), (1,26)),\
                       ('VALIGN', (1,21), (1,26),'MIDDLE'),\
                       ('SPAN',   (1,27), (1,29)),\
                       ('VALIGN', (1,27), (1,29),'MIDDLE'),\
                       # # # fecha
                       ('SPAN',   (2,2), (2,4)),\
                       ('VALIGN', (2,2), (2,4),'MIDDLE'),\
                       ('SPAN',   (2,6), (2,7)),\
                       ('VALIGN', (2,6), (2,7),'MIDDLE'),\
                       ('SPAN',   (2,10), (2,11)),\
                       ('VALIGN', (2,10), (2,11),'MIDDLE'),\
                       ('SPAN',   (2,14), (2,15)),\
                       ('VALIGN', (2,14), (2,15),'MIDDLE'),\
                       ('SPAN',   (2,16), (2,18)),\
                       ('VALIGN', (2,16), (2,18),'MIDDLE'),\
                       ('SPAN',   (2,19), (2,23)),\
                       ('VALIGN', (2,19), (2,23),'MIDDLE'),\
                       ('SPAN',   (2,24), (2,26)),\
                       ('VALIGN', (2,24), (2,26),'MIDDLE'),\
                       ('SPAN',   (2,28), (2,31)),\
                       ('VALIGN', (2,28), (2,31),'MIDDLE'),\
                       # # # hora
                       # ('SPAN',   (3,5), (3,6)),\
                       # ('VALIGN', (3,5), (3,6),'MIDDLE'),\
                        ]))


t.wrapOn(JuanMarica, 600, 890)
t.drawOn(JuanMarica, 100., 335.)

JuanMarica.save()


os.system('scp '+Path+'JuanMarica.pdf ccuervo@192.168.1.74:/var/www/cmcuervol/')


print 'Hello world'
