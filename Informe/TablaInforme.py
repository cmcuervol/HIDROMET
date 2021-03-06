#!/usr/bin/env python
# encoding: utf-8
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import letter, inch
# from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table
# from reportlab.lib.styles import getSampleStyleSheet
import os
import numpy as np
import datetime as dt
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
Path_figures = '/home/cmcuervol/Desktop/MapasInforme/HIDROMET/'

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


# # week  December 30th to January 5th
# data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta'  ],
#         [u'Medellín',     u'Columna de humo en San Javier'                      ,'2020-01-03'  , '14:12'       ],
#         [u'Medellín',     u'Columna de humo en Robledo'                         ,'2020-01-04'  , '16:58'       ],
#         [u'Medellín',     u'Columna de humo en Robledo'                         ,'2020-01-05'  , '10:33'       ],
#         [u'Medellín',     u'Columna de humo en Centro'                          ,'2020-01-05'  , '06:00'       ],
#         [u'Medellín',     u'Columna de humo en Manrique'                        ,'2020-01-05'  , '11:05'       ],
#         [u'Medellín',     u'Columna de humo en Cerro El Volador'                ,'2020-01-05'  , '11:25'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal'                   ,'2020-01-05'  , '11:49'       ],
#         [u'Medellín',     u'Columna de humo en Blanzuizal'                      ,'2020-01-05'  , '12:43'       ],
#         [u'Bello',        u'Columna de humo en Cerro Quitasol'                  ,'2020-01-05'  , '12:40'       ],
#         [u'Bello',        u'Columna de humo en el oriente de Bello'             ,'2020-01-05'  , '15:50'       ],
#        ]
# # week  January 6th to 12th
# data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta'  ],
#         [u'Sabaneta',     u'Columna de humo en La Doctora'                      ,'2020-01-08'  , '15:06'       ],
#         [u'La Estrella',  u'Columna de humo en El Pedrero'                      ,'2020-01-08'  , '15:16'       ],
#         [u'Caldas',       u'Columna de humo en La Miel'                         ,'2020-01-09'  , '09:08'       ],
#         [u'Bello',        u'Columna de humo en Granizal'                        ,'2020-01-09'  , '09:54'       ],
#         [u'Bello',        u'Columna de humo en Potrerito'                       ,'2020-01-11'  , '13:10'       ],
#         [u'Bello',        u'Columna de humo en Santa Rita'                      ,'2020-01-10'  , '16:57'       ],
#         [u'Medellín',     u'Columna de humo en Aures2'                          ,'2020-01-10'  , '12:33'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal'                   ,'2020-01-10'  , '15:35'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal'                   ,'2020-01-09'  , '15:50'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal'                   ,'2020-01-12'  , '13:05'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal'                   ,'2020-01-11'  , '13:18'       ],
#         [u'Medellín',     u'Columna de humo en Altavista'                       ,'2020-01-11'  , '10:55'       ],
#         [u'Medellín',     u'Columna de humo en Altavista'                       ,'2020-01-07'  , '15:29'       ],
#        ]
# # week  January 13th to 19th
# data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta'  ],
#         [u'Bello',        u'Columna de humo en Nueva Jerusalén'                 ,'2020-01-14'  , '13:40'       ],
#         [u'Bello',        u'Columna de humo en la vereda Potrerito'             ,'2020-01-15'  , '16:35'       ],
#         [u'Bello',        u'Columna de humo en autopista Medellín - Bogotá'     ,'2020-01-16'  , '14:45'       ],
#         [u'Bello',        u'Columna de humo en la vereda El Hato'               ,'2020-01-13'  , '10:28'       ],
#         [u'Medellín',     u'Columna de humo en Altavista'                       ,'2020-01-13'  , '16:06'       ],
#         [u'Medellín',     u'Columna de humo en Altavista'                       ,'2020-01-18'  , '09:02'       ],
#         [u'Medellín',     u'Columna de humo en Altavista'                       ,'2020-01-18'  , '12:16'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal'                   ,'2020-01-18'  , '14:12'       ],
#         [u'Medellín',     u'Columna de humo en Belén Rincón'                    ,'2020-01-14'  , '13:30'       ],
#         [u'Medellín',     u'Columna de humo en Pajarito'                        ,'2020-01-14'  , '11:50'       ],
#         [u'Medellín',     u'Columna de humo en Picacho'                         ,'2020-01-14'  , '11:50'       ],
#         [u'Medellín',     u'Columna de humo en Aures2'                          ,'2020-01-14'  , '11:50'       ],
#         [u'Medellín',     u'Columna de humo en Aures2'                          ,'2020-01-15'  , '01:25'       ],
#         [u'Medellín',     u'Columna de humo en Santa Rosa de Lima'              ,'2020-01-16'  , '13:05'       ],
#         [u'Medellín',     u'Columna de humo en Cola del Zorro'                  ,'2020-01-19'  , '13:55'       ],
#         [u'Medellín',     u'Columna de humo en Seminario Mayor'                 ,'2020-01-17'  , '06:17'       ],
#         [u'Medellín',     u'Columna de humo en la urbanización Villa Campiña'   ,'2020-01-17'  , '12:33'       ],
#         [u'Itagüí',       u'Columna de humo en la vereda El Porvenir'           ,'2020-01-17'  , '11:10'       ],
#        ]

# # week  January 20th to 26th
# data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta'  ],
#         [u'Bello',        u'Quebrada La Loca'                                   ,'2020-01-21'  , '16:14'       ],
#         [u'Bello',        u'Quebrada El Hato'                                   ,'2020-01-21'  , '16:16'       ],
#         [u'Bello',        u'Río Medellín (La Asunción)'                         ,'2020-01-21'  , '16:19'       ],
#         [u'Bello',        u'Río Medellín (Puente Machado)'                      ,'2020-01-21'  , '16:25'       ],
#         [u'Medellín',     u'Quebrada La Presidenta'                             ,'2020-01-21'  , '15:34'       ],
#         [u'Medellín',     u'Quebrada La Madera'                                 ,'2020-01-21'  , '16:13'       ],
#         [u'Medellín',     u'Columna de humo en San Cristóbal'                   ,'2020-01-22'  , '12:13'       ],
#         [u'Medellín',     u'Columna de humo en la vereda Media Luna'            ,'2020-01-22'  , '12:50'       ],
#         [u'Medellín',     u'Columna de humo en La Castellana'                   ,'2020-01-22'  , '13:11'       ],
#        ]
# week  January 27th to February 2nd
data = [['Municipio',     'Zona alertada'                                       ,'Fecha alerta','Hora Alerta'  ],
        [u'Bello',        u'Quebrada La Loca'                                   ,'2020-01-27'  , '15:58'       ],
        [u'Bello',        u'Quebrada Cañada Negra'                              ,'2020-01-27'  , '15:58'       ],
        [u'Bello',        u'Columna de humo en la vereda Croacia'               ,'2020-01-30'  , '10:20'       ],
        [u'Medellín',     u'Columna de humo Llanaditas'                         ,'2020-01-30'  , '12:06'       ],
        [u'Medellín',     u'Quebrada La Iguaná'                                 ,'2020-01-27'  , '16:12'       ],
        [u'Medellín',     u'Columna de humo en San Cristóbal'                   ,'2020-01-27'  , '12:26'       ],
        [u'Medellín',     u'Columna de humo en San Cristóbal'                   ,'2020-02-01'  , '14:38'       ],
        [u'Medellín',     u'Columna de humo en San Cristóbal'                   ,'2020-02-01'  , '16:11'       ],
        [u'Medellín',     u'Columna de humo en la vereda El Corazón'            ,'2020-01-31'  , '15:00'       ],
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
                       # # Municipio
                       ('SPAN',   (0,1),  (0,3)),\
                       ('VALIGN', (0,1),  (0,3),'MIDDLE'),\
                       ('SPAN',   (0,4),  (0,9)),\
                       ('VALIGN', (0,4),  (0,9),'MIDDLE'),\
                       # # # # zona
                       ('SPAN',   (1,6),  (1,8)),\
                       ('VALIGN', (1,6),  (1,8),'MIDDLE'),\
                       # # # # # # fecha
                       ('SPAN',   (2,1), (2,2)),\
                       ('VALIGN', (2,1), (2,2),'MIDDLE'),\
                       ('SPAN',   (2,3), (2,4)),\
                       ('VALIGN', (2,3), (2,4),'MIDDLE'),\
                       ('SPAN',   (2,5), (2,6)),\
                       ('VALIGN', (2,5), (2,6),'MIDDLE'),\
                       ('SPAN',   (2,7), (2,8)),\
                       ('VALIGN', (2,7), (2,8),'MIDDLE'),\
                       # hora
                       ('SPAN',   (3,1),(3,2)),\
                       ('VALIGN', (3,1),(3,2),'MIDDLE'),\
                        ]))

# sizey, sizex = A2
JuanMarica = canvas.Canvas(Path_figures+'JuanMarica.pdf')
JuanMarica.setPageSize((12*inch, len(data)*0.4*inch+20))

JuanMarica.setFont("Avenir", 24)
t.wrapOn(JuanMarica, 600, 890)
t.drawOn(JuanMarica, 10.,10.)

JuanMarica.save()

# lastday = dt.datetime.today() #run on monday
lastday = dt.datetime.today()+ dt.timedelta(days=1) # run on sunday
startday = lastday-dt.timedelta(days=7)
endday   = lastday-dt.timedelta(days=1)
# Path_informe = '/home/atlas/informe_hidromet/'+str(year)+str(month).zfill(2)+'/'
Path_informe = '/home/atlas/informe_hidromet/'+startday.strftime('%Y%m%d')+'_'+endday.strftime('%Y%m%d')+'/Precipitacion/'

if os.path.exists(Path_informe) == False:
    lastday = dt.datetime.today() #run on monday
    startday = lastday-dt.timedelta(days=7)
    endday   = lastday-dt.timedelta(days=1)
    Path_informe = '/home/atlas/informe_hidromet/'+startday.strftime('%Y%m%d')+'_'+endday.strftime('%Y%m%d')+'/Precipitacion/'

# os.system('convert -verbose -density 150 -trim '+Path_figures+'JuanMariposo.pdf -quality 100 -flatten -sharpen 0x1.0 '+Path_figures+'JuanMariposo.png')
os.system('convert -verbose -density 150 -trim -transparent white '+Path_figures+'JuanMarica.pdf -quality 100 '+Path_informe+'Tabla.png')
# os.system('scp '+Path_figures+'JuanMariposo.* ccuervo@192.168.1.74:/var/www/cmcuervol/')
os.system('scp '+Path_figures+'JuanMarica.pdf ccuervo@192.168.1.74:/var/www/cmcuervol/')


print ('Hello world')
