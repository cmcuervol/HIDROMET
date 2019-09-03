# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 10:35:56 2018

@author: GISEL

modified by cmcuervol
"""
import matplotlib as mpl
mpl.use ("Agg")

import pandas as pd
import numpy as np
import datetime as dt
import os
import sys
# from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates
import matplotlib.font_manager as fm
import matplotlib.colors as colors
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from mpl_toolkits.basemap import Basemap
from matplotlib import rcParams
import Pysolar.solar as ps
from dateutil.relativedelta import relativedelta
import collections

import scipy.ndimage
from   pyPdf import PdfFileWriter, PdfFileReader
from   reportlab.pdfgen import canvas
from   StringIO import StringIO
from   reportlab.pdfbase import pdfmetrics
from   reportlab.pdfbase.ttfonts import TTFont
from   reportlab.lib.pagesizes import landscape, A4, LETTER, A0, A1, A2, A3, A5, inch
from   reportlab.lib.styles import ParagraphStyle
from   reportlab.lib.enums import TA_JUSTIFY
from   reportlab.lib.units import cm, mm
from   reportlab.lib import colors as color
from   reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle



##==============================================================================
#Definicion de directorios
# workdir = '/home/gguzmane/Informe_semanal/'
# path_data = workdir + 'data_temp_mensual/'
# path_save = workdir + 'images_mensual/'
# path_historicos = workdir + 'historicos/'
Path_figures = '/home/cmcuervol/Desktop/MapasInforme/'
Path_shapes  = '/home/cmcuervol/Shapes/'
Path_fuentes = '/home/cmcuervol/Fuentes/'

# Types of fonts Avenir
AvenirHeavy = fm.FontProperties(fname=Path_fuentes+'AvenirLTStd-Heavy.otf')
AvenirBook  = fm.FontProperties(fname=Path_fuentes+'AvenirLTStd-Book.otf')
AvenirBlack = fm.FontProperties(fname=Path_fuentes+'AvenirLTStd-Black.otf')
AvenirRoman = fm.FontProperties(fname=Path_fuentes+'AvenirLTStd-Roman.ttf')





# Colors for graphics SIATA style
gris70 = (112/255., 111/255., 111/255.)
gris   = (246/255., 246/255., 246/255.)

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

rcParams['legend.frameon']= False
rcParams['legend.markerscale']=2.
rcParams['legend.fontsize']=14.
rcParams['axes.edgecolor']='0.8'
rcParams['axes.labelcolor']='0.15'
rcParams['axes.linewidth']='0.8'
rcParams['axes.labelsize']=14
rcParams['axes.titlesize']=17
rcParams[u'text.color']= u'.15'
rcParams[u'xtick.direction']= u'in'
rcParams[u'xtick.major.width']= 0.5
rcParams[u'xtick.labelsize']= 13
rcParams[u'ytick.labelsize']= 13
rcParams[u'ytick.color']=u'.15'
rcParams[u'ytick.direction']=u'in'
rcParams[ u'font.sans-serif']=[u'Arial',
                               u'Liberation Sans',
                               u'Bitstream Vera Sans',
                               u'sans-serif']


# Limites del shape en coordenadas geográficas
min_lat = 5.978178; min_lon = -75.719430
max_lat = 6.512488; max_lon = -75.222057

def color_from_custom_cmap(cmap,bounds,value):
    '''El comando de obtener los rgb de un color dentro de una colorbar funciona con la normalizacion de los colores
    del mismo, por lo cual toca tener el rango de 0-255 tal cual como se crearon las colorbar

    value: debe estar en el rango de los bounds sino paila, 0 o 1'''
    scale_factor =  ((255-0.)/(bounds.max() - bounds.min()))

    value_normalice = np.array((value - bounds.min())*scale_factor,dtype = int)
    rgb = cmap(value_normalice)
    return rgb

def cmap_temp_10():
    cmap_temp_10 = colors.LinearSegmentedColormap.from_list('Temp_10',
        [(0,(27/255.,36/255.,122/255.)), (0.1,(49/255.,54/255.,149/255.)), (0.2,(79/255.,129/255.,186/255.)),
         (0.3,(142/255.,194/255.,220/255.)), (0.4,(209/255.,236/255.,244/255.)),(0.5,(254/255.,255/255.,192/255.)),
         (0.6,(254/255.,212/255.,133/255.)),(0.7,(249/255.,142/255.,82/255.)),
         (0.8,(224/255.,77/255.,61/255.)), (1,(181/255.,0,40/255.))], N=256)
    cmap_temp_10.set_over((119/255.,62/255.,82/255.))
#    bounds_temp_10 = np.linspace(5,35,31,endpoint =True)
    bounds_temp_10 = np.linspace(5,35,16,endpoint =True)
    norm_temp_10 = colors.BoundaryNorm(boundaries=bounds_temp_10, ncolors=256)
    return cmap_temp_10,bounds_temp_10,norm_temp_10

cmap_t10 , bounds_t10, norm_t10 = cmap_temp_10()


def MapaLlamados(values,titulo,name,cmap,bounds,colorbar = False):
    # Datos MUN106,Medellin
    # AMVA=['Barbosa', 'Girardota'.....]
    #http://basemaptutorial.readthedocs.io/en/latest/shapefile.html
    rcParams['axes.linewidth']='0' #para desaparecer el cuadro de los mapas
    fig     = plt.figure(figsize=(9,9))
    ax      = fig.add_subplot(111)
    ax.set_title(u'Llamados a entidades de gestión del riesgo durante el mes')
    min_lat = 5.978178; min_lon = -75.719430
    max_lat = 6.512488; max_lon = -75.222057
    m = Basemap(llcrnrlon= min_lon,llcrnrlat= min_lat,
                urcrnrlon= -75.05,urcrnrlat= 6.56,projection='cyl', resolution='i')


    # etiquetas_AMVA() #Etiquetas de los municipios
    #Es muy importante: The elements must have only 2 dimensions y EPSG:4326, or lat/lon coordinates
    m.readshapefile(Path_shapes+'mpios_amva_qnk', 'mpios_amva_qnk', drawbounds = False)
    #-1: nan, -0.5 Misses, 0: False alarmn, 1: Hits
    patches   = [] ; patch_Colors = []
    #https://media.readthedocs.org/pdf/basemaptutorial/latest/basemaptutorial.pdf
    for info, shape in zip(m.mpios_amva_qnk_info, m.mpios_amva_qnk):

        val = values.iloc[info['SHAPENUM']-1].values[0]
        x, y = zip(*shape)
        m.plot(x, y, marker=None,color='m',linewidth=0.)
        patches.append( Polygon(np.array(shape), True) )
        if val != 0:
            patch_Colors.append(color_from_custom_cmap(cmap,bounds,val))
        else:
            patch_Colors.append(gris70)

    ax.add_collection(PatchCollection(patches, facecolor= patch_Colors, edgecolor='w', linewidths=0.5, zorder=2))

    if colorbar == True:
        #___________________  Configuración de la colorbar_____________________________
        # ax1 = fig.add_axes([0.92, 0.2, 0.03, 0.6])
        ax1 = fig.add_axes([0.125, 0.125, 0.78, 0.015])

        # cbar = mpl.colorbar.ColorbarBase(ax1, cmap=cmap, boundaries=bounds,\
        #                                   orientation='vertical')
        # cmap.set_under(gris70)
        cbar = mpl.colorbar.ColorbarBase(ax1, cmap=cmap, boundaries=bounds,\
                                         orientation='horizontal', extend='max')
        cbar.set_label(u'Llamados a entidades de gestión del riesgo', fontsize = 12,fontproperties = AvenirRoman)
        cbar.update_ticks()
        cbar.ax.tick_params(colors=gris70,labelsize = 10)

    if titulo != False:
        plt.text(0.1,0.95,titulo, fontproperties = AvenirRoman,fontsize = 24,transform = ax.transAxes)

    plt.savefig(Path_figures+name,dpi=150,transparent=False,bbox_inches='tight')

# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================

barcode_font = Path_fuentes+'AvenirLTStd-Roman.ttf'
pdfmetrics.registerFont(TTFont("Avenir", barcode_font))
# barcode_font_blk = Path_fuentes+'AvenirLTStd-Black.otf'
# pdfmetrics.registerFont(TTFont("Avenir_blk", barcode_font_blk))

sizey, sizex = A2
JuanMariposo = canvas.Canvas(Path_figures+'JuanMariposo.pdf')
JuanMariposo.setPageSize((sizex, sizey))

JuanMariposo.setFont("Avenir", 24)

# ==============================================================================
# August 2019
barbosa = [['Barbosa',                                             '',            ''             ],
           ['Zona alertada',                                       'Fecha alerta', 'Hora Alerta' ],
          ]

BAR =Table(barbosa,[3.5*inch,1.*inch,0.8*inch], len(barbosa)*[0.25*inch])
BAR.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, gris),\
                        ('BOX',       (0,0), (-1,-1), 0.25, gris),\
                        ('ALIGN',     (0,0),(-1,-1),'CENTER'),\
                        ('ALIGN',     (0,2),(0,-1),'LEFT'),\
                        # ('VALIGN',   (0,0),(-1,-1),'MIDDLE'),\
                        ('VALIGN',    (0,0),(-1,-1),'TOP'),\
                        ('VALIGN',    (0,0),(-1,1),'TOP'),\
                        ('FONTSIZE',  (0,0),(-1, 1), 12),\
                        ('BACKGROUND',(0,0),(-1,1),ColorInfo6),\
                        ('FONTSIZE',  (0,1),(-1,-1), 10),\
                        ('TEXTCOLOR', (0,0),(-1,1),color.white),\
                        ('SPAN',      (0,0), (-1,0)),\
                        # fecha
                        # ('SPAN',   (1,2), (1,3)),\
                        # ('VALIGN', (1,2), (1,3),'MIDDLE'),\
                        ]))

# ==============================================================================
# August 2019
girardota = [['Girardota',                                           '',             ''            ],
             ['Zona alertada',                                       'Fecha alerta', 'Hora Alerta' ],
             [u'Columna de humo en la vía El Barro'                 ,'2019-08-29'  , '13:52'       ],
            ]

GIR =Table(girardota,[3.5*inch,1.*inch,0.8*inch], len(girardota)*[0.25*inch])
GIR.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, gris),\
                        ('BOX',       (0,0), (-1,-1), 0.25, gris),\
                        ('ALIGN',     (0,0),(-1,-1),'CENTER'),\
                        ('ALIGN',     (0,2),(0,-1),'LEFT'),\
                        # ('VALIGN',   (0,0),(-1,-1),'MIDDLE'),\
                        ('VALIGN',    (0,0),(-1,-1),'TOP'),\
                        ('VALIGN',    (0,0),(-1,1),'TOP'),\
                        ('FONTSIZE',  (0,0),(-1, 1), 12),\
                        ('BACKGROUND',(0,0),(-1,1),ColorInfo6),\
                        ('FONTSIZE',  (0,1),(-1,-1), 10),\
                        ('TEXTCOLOR', (0,0),(-1,1),color.white),\
                        ('SPAN',      (0,0), (-1,0)),\
                        ]))

# ==============================================================================

# August 2019
copacabana = [['Copacabana',                                          '',              ''           ],
              ['Zona alertada',                                       'Fecha alerta', 'Hora Alerta' ],
              [u'Columna de humo en Las Salinas'                     ,'2019-08-29'  , '15:59'       ],
              [u'Columna de humo en Autopista Norte'                 ,'2019-09-01'  , '10:50'       ],
              ]

COP =Table(copacabana,[3.5*inch,1.*inch,0.8*inch], len(copacabana)*[0.25*inch])
COP.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, gris),\
                        ('BOX',       (0,0), (-1,-1), 0.25, gris),\
                        ('ALIGN',     (0,0),(-1,-1),'CENTER'),\
                        ('ALIGN',     (0,2),(0,-1),'LEFT'),\
                        # ('VALIGN',   (0,0),(-1,-1),'MIDDLE'),\
                        ('VALIGN',    (0,0),(-1,-1),'TOP'),\
                        ('VALIGN',    (0,0),(-1,1),'TOP'),\
                        ('FONTSIZE',  (0,0),(-1, 1), 12),\
                        ('BACKGROUND',(0,0),(-1,1),ColorInfo6),\
                        ('FONTSIZE',  (0,1),(-1,-1), 10),\
                        ('TEXTCOLOR', (0,0),(-1,1),color.white),\
                        ('SPAN',      (0,0), (-1,0)),\
                        # Zona
                        # ('SPAN',   (0,2), (0,4)),\
                        # ('VALIGN', (0,2), (0,4),'MIDDLE'),\
                        # fecha
                        # ('SPAN',   (1,2), (1,3)),\
                        # ('VALIGN', (1,2), (1,3),'MIDDLE'),\
                        ]))

# ==============================================================================

# August 2019
bello = [['Bello',                                               '',             ],
         ['Zona alertada',                                       'Fecha alerta', 'Hora Alerta'  ],
         [u'Columna de humo en Nueva Jerusalen'                 ,'2019-08-08'  , '13:39'       ],
         [u'Columna de humo en La comuna 9'                     ,'2019-08-19'  , '15:53'       ],
         [u'Columna de humo en el suroccidente de Bello'        ,'2019-08-22'  , '11:34'       ],
         [u'Columna de humo en vereda El Potrerito'             ,'2019-08-24'  , '10:32'       ],
         [u'Columna de humo en El barrio París'                 ,'2019-08-25'  , '13:12'       ],
         [u'Columna de humo en Niquia'                          ,'2019-08-31'  , '14:58'       ],
        ]



BEL =Table(bello,[3.5*inch,1.*inch,0.8*inch], len(bello)*[0.25*inch])
BEL.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, gris),\
                        ('BOX',       (0,0), (-1,-1), 0.25, gris),\
                        ('ALIGN',     (0,0),(-1,-1),'CENTER'),\
                        ('ALIGN',     (0,2),(0,-1),'LEFT'),\
                        # ('VALIGN',   (0,0),(-1,-1),'MIDDLE'),\
                        ('VALIGN',    (0,0),(-1,-1),'TOP'),\
                        ('VALIGN',    (0,0),(-1,1),'TOP'),\
                        ('FONTSIZE',  (0,0),(-1, 1), 12),\
                        ('BACKGROUND',(0,0),(-1,1),ColorInfo6),\
                        ('FONTSIZE',  (0,1),(-1,-1), 10),\
                        ('TEXTCOLOR', (0,0),(-1,1),color.white),\
                        ('SPAN',      (0,0), (-1,0)),\
                        # # Zona
                        # ('SPAN',   (0,3), (0,4)),\
                        # ('VALIGN', (0,3), (0,4),'MIDDLE'),\
                        # ('SPAN',   (0,5), (0,7)),\
                        # ('VALIGN', (0,5), (0,7),'MIDDLE'),\
                        # # # fecha
                        # ('SPAN',   (1,4), (1,5)),\
                        # ('VALIGN', (1,4), (1,5),'MIDDLE'),\
                        # # # Hora
                        # ('SPAN',   (2,4), (2,5)),\
                        # ('VALIGN', (2,4), (2,5),'MIDDLE'),\
                        ]))


# ==============================================================================
# August 2019
medellin = [[u'Medellín',                                           '',                           ],
            ['Zona alertada',                                       'Fecha alerta', 'Hora Alerta' ],
            [u'Columna de humo en San Cristóbal'                   ,'2019-08-01'  , '17:00'       ],
            [u'Columna de humo en San Cristóbal'                   ,'2019-08-15'  , '12:28'       ],
            [u'Columna de humo en San Cristóbal'                   ,'2019-08-15'  , '14:11'       ],
            [u'Columna de humo en San Cristóbal'                   ,'2019-08-13'  , '15:14'       ],
            [u'Columna de humo en San Cristóbal'                   ,'2019-08-22'  , '15:32'       ],
            [u'Columna de humo en San Cristóbal - Pedregal Alto'   ,'2019-08-12'  , '11:30'       ],
            [u'Columna de humo en San Cristóbal - Pedregal Alto'   ,'2019-08-21'  , '09:31'       ],
            [u'Columna de humo en San Cristóbal - Pedregal Alto'   ,'2019-08-21'  , '11:04'       ],
            [u'Columna de humo en San Cristóbal - Pedregal Alto'   ,'2019-08-26'  , '12:13'       ],
            [u'Columna de humo en San Cristóbal - Pedregal Alto'   ,'2019-08-28'  , '14:40'       ],
            [u'Columna de humo en San Cristóbal - Pedregal Alto'   ,'2019-08-29'  , '14:01'       ],
            [u'Columna de humo en San Cristóbal - La Loma'         ,'2019-08-19'  , '11:05'       ],
            [u'Columna de humo en San Cristóbal - El Morro'        ,'2019-08-23'  , '16:55'       ],
            [u'Columna de humo en Belen - Las Violetas'            ,'2019-08-23'  , '08:00'       ],
            [u'Columna de humo en Belén - Las Violetas'            ,'2019-08-27'  , '12:57'       ],
            [u'Columna de humo en Belen - Las Violetas'            ,'2019-08-12'  , '15:52'       ],
            [u'Columna de humo en Calasanz'                        ,'2019-08-12'  , '13:59'       ],
            [u'Columna de humo en Robledo'                         ,'2019-08-12'  , '14:30'       ],
            [u'Columna de humo en San Javier - Antonio Nariño'     ,'2019-08-12'  , '12:59'       ],
            [u'Columna de humo en San Javier'                      ,'2019-08-29'  , '14:01'       ],
            [u'Columna de humo en San Javier - El Salado'          ,'2019-08-30'  , '15:00'       ],
            [u'Columna de humo en San Javier - El Salado'          ,'2019-08-13'  , '10:16'       ],
            [u'Columna de humo en La Asomadera'                    ,'2019-08-13'  , '10:16'       ],
            [u'Columna de humo entre Pedregal y San Cristóbal'     ,'2019-08-13'  , '11:28'       ],
            [u'Columna de humo en Altavista'                       ,'2019-08-13'  , '15:29'       ],
            [u'Columna de humo en Altavista'                       ,'2019-08-16'  , '15:05'       ],
            [u'Columna de humo en Altavista'                       ,'2019-08-18'  , '13:12'       ],
            [u'Columna de humo en Altavista'                       ,'2019-08-14'  , '13:00'       ],
            [u'Columna de humo en Altavista'                       ,'2019-08-22'  , '15:32'       ],
            [u'Columna de humo en Altavista'                       ,'2019-08-22'  , '16:27'       ],
            [u'Columna de humo en Altavista'                       ,'2019-08-22'  , '18:13'       ],
            [u'Columna de humo en Altavista'                       ,'2019-08-23'  , '10:26'       ],
            [u'Columna de humo en Altavista'                       ,'2019-08-31'  , '12:51'       ],
            [u'Columna de humo en Altavista'                       ,'2019-08-28'  , '14:26'       ],
            [u'Columna de humo en Altavista'                       ,'2019-08-28'  , '14:47'       ],
            [u'Columna de humo en Altavista'                       ,'2019-08-29'  , '12:01'       ],
            [u'Columna de humo en Altavista'                       ,'2019-08-29'  , '14:11'       ],
            [u'Columna de humo en San Javier-Nuevos Conquistadores','2019-08-31'  , '12:04'       ],
           ]


MED =Table(medellin,[3.5*inch,1.*inch,0.8*inch], len(medellin)*[0.25*inch])
MED.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, gris),\
                        ('BOX',       (0,0), (-1,-1), 0.25, gris),\
                        ('ALIGN',     (0,0),(-1,-1),'CENTER'),\
                        ('ALIGN',     (0,2),(0,-1),'LEFT'),\
                        # ('VALIGN',   (0,0),(-1,-1),'MIDDLE'),\
                        ('VALIGN',    (0,0),(-1,-1),'TOP'),\
                        ('VALIGN',    (0,0),(-1,1),'TOP'),\
                        ('FONTSIZE',  (0,0),(-1, 1), 12),\
                        ('BACKGROUND',(0,0),(-1,1),ColorInfo6),\
                        ('FONTSIZE',  (0,1),(-1,-1), 10),\
                        ('TEXTCOLOR', (0,0),(-1,1),color.white),\
                        ('SPAN',      (0,0), (-1,0)),\
                        # Zona
                        ('SPAN',   (0,2),  (0,6)),\
                        ('VALIGN', (0,2),  (0,6),'MIDDLE'),\
                        ('SPAN',   (0,7),  (0,12)),\
                        ('VALIGN', (0,7),  (0,12),'MIDDLE'),\
                        ('SPAN',   (0,15), (0,17)),\
                        ('VALIGN', (0,15), (0,17),'MIDDLE'),\
                        ('SPAN',   (0,22), (0,23)),\
                        ('VALIGN', (0,22), (0,23),'MIDDLE'),\
                        ('SPAN',   (0,26), (0,38)),\
                        ('VALIGN', (0,26), (0,38),'MIDDLE'),\
                        # fecha
                        ('SPAN',   (1,3),  (1,4)),\
                        ('VALIGN', (1,3),  (1,4),'MIDDLE'),\
                        ('SPAN',   (1,8),  (1,9)),\
                        ('VALIGN', (1,8),  (1,9),'MIDDLE'),\
                        ('SPAN',   (1,14), (1,15)),\
                        ('VALIGN', (1,14), (1,15),'MIDDLE'),\
                        ('SPAN',   (1,17), (1,20)),\
                        ('VALIGN', (1,17), (1,20),'MIDDLE'),\
                        ('SPAN',   (1,24), (1,26)),\
                        ('VALIGN', (1,24), (1,26),'MIDDLE'),\
                        ('SPAN',   (1,30), (1,32)),\
                        ('VALIGN', (1,30), (1,32),'MIDDLE'),\
                        ('SPAN',   (1,35), (1,36)),\
                        ('VALIGN', (1,35), (1,36),'MIDDLE'),\
                        ('SPAN',   (1,37), (1,38)),\
                        ('VALIGN', (1,37), (1,38),'MIDDLE'),\
                        # Hora
                        # ('SPAN',   (2,5), (2,6)),\
                        # ('VALIGN', (2,5), (2,6),'MIDDLE'),\
                        ]))

# ==============================================================================








# ==============================================================================
# August 2019
medellin1 = [[u'Medellín',                                           '',                           ],
            ['Zona alertada',                                       'Fecha alerta', 'Hora Alerta' ],
            [u'Incendio forestal en San Cristóbal - La Frisolera'  ,'2019-08-09'  , '16:50'       ],
            [u'Columna de humo entre San Javier y San Cristóbal'   ,'2019-08-06'  , '12:00'       ],
            [u'Columna de humo en sector El Corazón'               ,'2019-08-30'  , '16:31'       ],
            [u'Columna de humo en Las Estancias'                   ,'2019-08-02'  , '10:57'       ],
            [u'Columna de humo en Blanquizal'                      ,'2019-08-05'  , '12:05'       ],
            [u'Columna de humo en San Germán'                      ,'2019-08-09'  , '13:30'       ],
            [u'Columna de humo en La Cruz'                         ,'2019-08-12'  , '13:26'       ],
            [u'Columna de humo en La Cruz'                         ,'2019-08-28'  , '16:47'       ],
            [u'Columna de humo en La Cruz'                         ,'2019-08-27'  , '10:50'       ],
            [u'Columna de humo en La Cruz'                         ,'2019-08-29'  , '09:12'       ],
            [u'Columna de humo en Belencito Corazón'               ,'2019-08-31'  , '18:00'       ],
            [u'Columna de humo en Manrique'                        ,'2019-08-14'  , '10:00'       ],
            [u'Columna de humo en el Cerro El Volador'             ,'2019-08-21'  , '09:31'       ],
            [u'Columna de humo en el Cerro El Volador'             ,'2019-08-27'  , '09:12'       ],
            [u'Columna de humo en el Cerro de Las Tres Cruces'     ,'2019-08-21'  , '11:20'       ],
            [u'Columna de humo en el Cerro de Las Tres Cruces'     ,'2019-08-21'  , '13:06'       ],
            [u'Columna de humo en el Cerro de Las Tres Cruces'     ,'2019-08-26'  , '11:30'       ],
            [u'Columna de humo en el Cerro Pan de Azúcar'          ,'2019-08-29'  , '09:12'       ],
            [u'Columna de humo en el Cerro Pan de Azúcar'          ,'2019-08-29'  , '11:35'       ],
            [u'Columna de humo en el Cerro Pan de Azúcar'          ,'2019-08-15'  , '10:45'       ],
            [u'Columna de humo en el Cerro Pan de Azúcar'          ,'2019-08-30'  , '16:05'       ],
            [u'Columna de humo en Santa Margarita'                 ,'2019-08-20'  , '13:28'       ],
            [u'Columna de humo en Santa Elena - Piedras Blancas'   ,'2019-08-20'  , '13:19'       ],
            [u'Columna de humo en Santa Elena - Piedras Blancas'   ,'2019-08-20'  , '20:50'       ],
            [u'Columna de humo en Santa Elena - Piedras Blancas'   ,'2019-08-30'  , '10:00'       ],
            [u'Columna de humo en Santa Elena - Piedras Blancas'   ,'2019-08-28'  , '16:47'       ],
            [u'Columna de humo en Santa Elena'                     ,'2019-08-28'  , '11:30'       ],
            [u'Columna de humo en Santa Elena'                     ,'2019-08-22'  , '06:28'       ],
            [u'Columna de humo en Santa Elena'                     ,'2019-08-22'  , '10:37'       ],
            [u'Columna de humo en La Alpujarra'                    ,'2019-08-23'  , '12:52'       ],
            [u'Columna de humo en El Picacho'                      ,'2019-08-25'  , '12:48'       ],
            [u'Columna de humo en Villa Flora'                     ,'2019-08-26'  , '13:00'       ],
            [u'Columna de humo en San José La Cima Nº2'            ,'2019-08-31'  , '13:00'       ],
            [u'Columna de humo en Pajarito'                        ,'2019-08-30'  , '17:20'       ],
            [u'Columna de humo en Pajarito'                        ,'2019-08-30'  , '11:30'       ],
            [u'Columna de humo en El Socorro'                      ,'2019-08-30'  , '09:50'       ],
            [u'Columna de humo en el barrio Monte Claro'           ,'2019-08-30'  , '14:20'       ],
            [u'Columna de humo en el barrio Monte Claro'           ,'2019-08-29'  , '14:04'       ],
           ]


MED1 =Table(medellin1,[3.5*inch,1.*inch,0.8*inch], len(medellin)*[0.25*inch])
MED1.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, gris),\
                        ('BOX',       (0,0), (-1,-1), 0.25, gris),\
                        ('ALIGN',     (0,0),(-1,-1),'CENTER'),\
                        ('ALIGN',     (0,2),(0,-1),'LEFT'),\
                        # ('VALIGN',   (0,0),(-1,-1),'MIDDLE'),\
                        ('VALIGN',    (0,0),(-1,-1),'TOP'),\
                        ('VALIGN',    (0,0),(-1,1),'TOP'),\
                        ('FONTSIZE',  (0,0),(-1, 1), 12),\
                        ('BACKGROUND',(0,0),(-1,1),ColorInfo6),\
                        ('FONTSIZE',  (0,1),(-1,-1), 10),\
                        ('TEXTCOLOR', (0,0),(-1,1),color.white),\
                        ('SPAN',      (0,0), (-1,0)),\
                        # Zona
                        ('SPAN',   (0,8),  (0,11)),\
                        ('VALIGN', (0,8),  (0,11),'MIDDLE'),\
                        ('SPAN',   (0,14), (0,15)),\
                        ('VALIGN', (0,14), (0,15),'MIDDLE'),\
                        ('SPAN',   (0,16), (0,18)),\
                        ('VALIGN', (0,16), (0,18),'MIDDLE'),\
                        ('SPAN',   (0,19), (0,22)),\
                        ('VALIGN', (0,19), (0,22),'MIDDLE'),\
                        ('SPAN',   (0,24), (0,27)),\
                        ('VALIGN', (0,24), (0,27),'MIDDLE'),\
                        ('SPAN',   (0,28), (0,30)),\
                        ('VALIGN', (0,28), (0,30),'MIDDLE'),\
                        ('SPAN',   (0,24), (0,27)),\
                        ('VALIGN', (0,24), (0,27),'MIDDLE'),\
                        ('SPAN',   (0,35), (0,36)),\
                        ('VALIGN', (0,35), (0,36),'MIDDLE'),\
                        ('SPAN',   (0,38), (0,39)),\
                        ('VALIGN', (0,38), (0,39),'MIDDLE'),\
                        # fecha
                        ('SPAN',   (1,16), (1,17)),\
                        ('VALIGN', (1,16), (1,17),'MIDDLE'),\
                        ('SPAN',   (1,19), (1,20)),\
                        ('VALIGN', (1,19), (1,20),'MIDDLE'),\
                        ('SPAN',   (1,23), (1,25)),\
                        ('VALIGN', (1,23), (1,25),'MIDDLE'),\
                        ('SPAN',   (1,27), (1,28)),\
                        ('VALIGN', (1,27), (1,28),'MIDDLE'),\
                        ('SPAN',   (1,29), (1,30)),\
                        ('VALIGN', (1,29), (1,30),'MIDDLE'),\
                        ('SPAN',   (1,35), (1,38)),\
                        ('VALIGN', (1,35), (1,38),'MIDDLE'),\
                        # Hora
                        ('SPAN',   (2,33), (2,34)),\
                        ('VALIGN', (2,33), (2,34),'MIDDLE'),\
                        ]))

# ==============================================================================
# August 2019
itagui = [[u'Itagüí',                                             '',             ''            ],
          ['Zona alertada',                                       'Fecha alerta', 'Hora Alerta' ],
          [u'Columna de humo en Itagüí'                          ,'2019-08-30'  , '11:00'       ],
          ]


ITA =Table(itagui,[3.5*inch,1.*inch,0.8*inch], len(itagui)*[0.25*inch])
ITA.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, gris),\
                        ('BOX',       (0,0), (-1,-1), 0.25, gris),\
                        ('ALIGN',     (0,0),(-1,-1),'CENTER'),\
                        ('ALIGN',     (0,2),(0,-1),'LEFT'),\
                        # ('VALIGN',   (0,0),(-1,-1),'MIDDLE'),\
                        ('VALIGN',    (0,0),(-1,-1),'TOP'),\
                        ('VALIGN',    (0,0),(-1,1),'TOP'),\
                        ('FONTSIZE',  (0,0),(-1, 1), 12),\
                        ('BACKGROUND',(0,0),(-1,1),ColorInfo6),\
                        ('FONTSIZE',  (0,1),(-1,-1), 10),\
                        ('TEXTCOLOR', (0,0),(-1,1),color.white),\
                        ('SPAN',      (0,0), (-1,0)),\
                        # Zona
                        # ('SPAN',   (0,2), (0,3)),\
                        # ('VALIGN', (0,2), (0,3),'MIDDLE'),\
                        # # fecha
                        # ('SPAN',   (1,2), (1,3)),\
                        # ('VALIGN', (1,2), (1,3),'MIDDLE'),\
                        # Hora
                        # ('SPAN',   (2,3), (2,4)),\
                        # ('VALIGN', (2,3), (2,4),'MIDDLE'),\
                        ]))

# ==============================================================================
# August 2019
envigado = [['Envigado',                                            '',             ''            ],
            ['Zona alertada',                                       'Fecha alerta', 'Hora Alerta' ],
           ]

ENV =Table(envigado,[3.5*inch,1.*inch,0.8*inch], len(envigado)*[0.25*inch])
ENV.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, gris),\
                        ('BOX',       (0,0), (-1,-1), 0.25, gris),\
                        ('ALIGN',     (0,0),(-1,-1),'CENTER'),\
                        ('ALIGN',     (0,2),(0,-1),'LEFT'),\
                        # ('VALIGN',   (0,0),(-1,-1),'MIDDLE'),\
                        ('VALIGN',    (0,0),(-1,-1),'TOP'),\
                        ('VALIGN',    (0,0),(-1,1),'TOP'),\
                        ('FONTSIZE',  (0,0),(-1, 1), 12),\
                        ('BACKGROUND',(0,0),(-1,1),ColorInfo6),\
                        ('FONTSIZE',  (0,1),(-1,-1), 10),\
                        ('TEXTCOLOR', (0,0),(-1,1),color.white),\
                        ('SPAN',      (0,0), (-1,0)),\
                        ]))

# ==============================================================================
# August 2019
laestrella = [['La Esrella',                                          '',             ''            ],
              ['Zona alertada',                                       'Fecha alerta', 'Hora Alerta' ],
              [u'Columna de humo en vereda La Culebra'               ,'2019-08-13'  , '12:55'       ],
             ]


STR =Table(laestrella,[3.5*inch,1.*inch,0.8*inch], len(laestrella)*[0.25*inch])
STR.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, gris),\
                        ('BOX',       (0,0), (-1,-1), 0.25, gris),\
                        ('ALIGN',     (0,0),(-1,-1),'CENTER'),\
                        ('ALIGN',     (0,2),(0,-1),'LEFT'),\
                        # ('VALIGN',   (0,0),(-1,-1),'MIDDLE'),\
                        ('VALIGN',    (0,0),(-1,-1),'TOP'),\
                        ('VALIGN',    (0,0),(-1,1),'TOP'),\
                        ('FONTSIZE',  (0,0),(-1, 1), 12),\
                        ('BACKGROUND',(0,0),(-1,1),ColorInfo6),\
                        ('FONTSIZE',  (0,1),(-1,-1), 10),\
                        ('TEXTCOLOR', (0,0),(-1,1),color.white),\
                        ('SPAN',      (0,0), (-1,0)),\
                        # # Zona
                        # ('SPAN',   (0,2), (0,3)),\
                        # ('VALIGN', (0,2), (0,3),'MIDDLE'),\
                        # fecha
                        # ('SPAN',   (1,2), (1,4)),\
                        # ('VALIGN', (1,2), (1,4),'MIDDLE'),\
                        ]))

# ==============================================================================
# August 2019
sabaneta = [[u'Sabaneta',                                           '',             ''            ],
            ['Zona alertada',                                       'Fecha alerta', 'Hora Alerta' ],
            [u'Columna de humo en sector Mayorca'                  ,'2019-08-25'  , '08:45'       ],
           ]


SAB =Table(sabaneta,[3.5*inch,1.*inch,0.8*inch], len(sabaneta)*[0.25*inch])
SAB.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, gris),\
                        ('BOX',       (0,0), (-1,-1), 0.25, gris),\
                        ('ALIGN',     (0,0),(-1,-1),'CENTER'),\
                        ('ALIGN',     (0,2),(0,-1),'LEFT'),\
                        # ('VALIGN',   (0,0),(-1,-1),'MIDDLE'),\
                        ('VALIGN',    (0,0),(-1,-1),'TOP'),\
                        ('VALIGN',    (0,0),(-1,1),'TOP'),\
                        ('FONTSIZE',  (0,0),(-1, 1), 12),\
                        ('BACKGROUND',(0,0),(-1,1),ColorInfo6),\
                        ('FONTSIZE',  (0,1),(-1,-1), 10),\
                        ('TEXTCOLOR', (0,0),(-1,1),color.white),\
                        ('SPAN',      (0,0), (-1,0)),\
                        # # Zona
                        # ('SPAN',   (0,2), (0,3)),\
                        # ('VALIGN', (0,2), (0,3),'MIDDLE'),\
                        # # fecha
                        # ('SPAN',   (1,2), (1,4)),\
                        # ('VALIGN', (1,2), (1,4),'MIDDLE'),\
                        # Hora
                        # ('SPAN',   (2,3), (2,4)),\
                        # ('VALIGN', (2,3), (2,4),'MIDDLE'),\
                        ]))

# ==============================================================================
# August 2019
caldas = [['Caldas',                                              '',             ''            ],
          ['Zona alertada',                                       'Fecha alerta', 'Hora Alerta' ],
         ]


CAL =Table(caldas,[3.5*inch,1.*inch,0.8*inch], len(caldas)*[0.25*inch])
CAL.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, gris),\
                        ('BOX',       (0,0), (-1,-1), 0.25, gris),\
                        ('ALIGN',     (0,0),(-1,-1),'CENTER'),\
                        ('ALIGN',     (0,2),(0,-1),'LEFT'),\
                        # ('VALIGN',   (0,0),(-1,-1),'MIDDLE'),\
                        ('VALIGN',    (0,0),(-1,-1),'TOP'),\
                        ('VALIGN',    (0,0),(-1,1),'TOP'),\
                        ('FONTSIZE',  (0,0),(-1, 1), 12),\
                        ('BACKGROUND',(0,0),(-1,1),ColorInfo6),\
                        ('FONTSIZE',  (0,1),(-1,-1), 10),\
                        ('TEXTCOLOR', (0,0),(-1,1),color.white),\
                        ('SPAN',      (0,0), (-1,0)),\
                        # # Zona
                        # ('SPAN',   (0,2), (0,3)),\
                        # ('VALIGN', (0,2), (0,3),'MIDDLE'),\
                        # # fecha
                        # ('SPAN',   (1,2), (1,3)),\
                        # ('VALIGN', (1,2), (1,3),'MIDDLE'),\
                        # # Hora
                        # ('SPAN',   (2,3), (2,4)),\
                        # ('VALIGN', (2,3), (2,4),'MIDDLE'),\
                        ]))


Municipios = ['Barbosa',
              'Girardota',
              'Copacabana',
              'Bello',
              'Medellin',
              'Itagui',
              'Envigado',
              'La Estrella',
              'Sabaneta',
              'Caldas']

Llamados = [len(barbosa)-2, len(girardota)-2, len(copacabana)-2, len(bello)-2, \
            len(medellin)-2, len(itagui)-2, len(envigado)-2, len(laestrella)-2, \
            len(sabaneta)-2, len(caldas)-2]

AMVA = pd.DataFrame(Llamados, index=Municipios)
print(AMVA) # see values to write the text
cmap = plt.cm.RdYlGn_r
# Buscar cmap.set_under('gris70')
# bounds = np.arange(1,max(Llamados)+2)
bounds = np.arange(1,32)

MapaLlamados(AMVA,False,'123.png',cmap,bounds,colorbar = True)

JuanMariposo.drawImage(Path_figures+'123.png', \
                      0.25*sizex, 0.1*sizey, width=32*cm, preserveAspectRatio=True)

# BAR.wrapOn(JuanMariposo, 600, 900)
GIR.wrapOn(JuanMariposo, 600, 900)
COP.wrapOn(JuanMariposo, 600, 900)
BEL.wrapOn(JuanMariposo, 600, 900)
MED.wrapOn(JuanMariposo, 600, 900)
MED1.wrapOn(JuanMariposo, 600, 900)
ITA.wrapOn(JuanMariposo, 600, 900)
# ENV.wrapOn(JuanMariposo, 600, 900)
STR.wrapOn(JuanMariposo, 600, 900)
SAB.wrapOn(JuanMariposo, 600, 900)
# CAL.wrapOn(JuanMariposo, 600, 900)

# single 1125; down 300; lef_2P 775;
# MED.drawOn(JuanMariposo,  775.,  500.)
MED.drawOn(JuanMariposo, 1200.,  300.)
MED1.drawOn(JuanMariposo,   10.,  300.)
BEL.drawOn(JuanMariposo,  775.,  600.)
SAB.drawOn(JuanMariposo,  775.,  450.)
# ENV.drawOn(JuanMariposo, 1200.,  790.)
COP.drawOn(JuanMariposo,  775.,  300.)
GIR.drawOn(JuanMariposo,  775.,  525.)
STR.drawOn(JuanMariposo,  775.,  375.)
# BAR.drawOn(JuanMariposo,  775.,  650.)
# CAL.drawOn(JuanMariposo,  775.,  350.)
ITA.drawOn(JuanMariposo,  450, 965.)

JuanMariposo.save()

# lastday = dt.datetime(2019,6,3) #monday
# lastday = dt.datetime.today()+ dt.timedelta(days=1) #monday
# startday = lastday-dt.timedelta(days=7)
# endday   = lastday-dt.timedelta(days=1)
today = dt.datetime.today()
year  = today.year
month = today.month -1 # run in the next month
if month == 0:
    month = 12
    year -= 1

# Path_informe = '/home/atlas/informe_hidromet/'+startday.strftime('%Y%m%d')+'_'+endday.strftime('%Y%m%d')+'/Mensual/'
Path_informe = '/home/atlas/informe_hidromet/'+str(year)+str(month).zfill(2)+'/'

os.system('convert -verbose -density 150 -trim '+Path_figures+'JuanMariposo.pdf -quality 100 -flatten -sharpen 0x1.0 '+Path_figures+'JuanMariposo.png')
os.system('convert -verbose -density 150 -trim -transparent white '+Path_figures+'JuanMariposo.png -quality 100 '+Path_informe+'123.png')
os.system('scp '+Path_figures+'JuanMariposo.* ccuervo@192.168.1.74:/var/www/cmcuervol/')

TextoLlamados = "Durante el mes se realizaron 89 llamados a las líneas de emergencia \
                 municipales; 77 de estos debidos a emergencias en Medellín. \
                 Todos estos llamados se debieron a reportes de columnas de humo, \
                 La mayoría de estos llamados se bebieron a incendios en cobertura \
                 vegetal, adicionalmente debido a las bajas precipitaciones durante \
                 el mes no se registró ninguna alerta hidrometeorológica."


TextoTorta = "La gráfica de torta muestra un resumen de los acumulados máximos de \
              precipitación de todos los eventos que superaron 5 mm de acumulado \
              sobre el valle de Aburrá. Durante agosto se registraron sólo 4 eventos \
              de precipitación, de los cuales sólo uno de ellos tuvo acumulados \
              mayores a 45 mm, los otros tres eventos tuvieron acumulados entre \
              15 y 30 mm. Durante agosto predominaron condiciones de tiempo seco, \
              con total ausencia de precipitaciones en la mayoría del mes, mostrando \
              un comportamiento más seco de lo esperado para esta temporada."

y = []
y.append(unicode(TextoLlamados.replace('                 ',''),'utf-8'))
y.append('<br/>')
y.append(unicode(TextoTorta.replace('              ',''),'utf-8'))

reload(sys)
sys.setdefaultencoding('utf8')
c = open (Path_informe+'Torta_y_alertas.txt', 'w')
# np.savetxt(metaruta+informe+'/Textos.txt', y, fmt='%s')
c.writelines( "%s\n" % str(item) for item in y )
c.close()

print 'Hello world'
