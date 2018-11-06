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


# def nombres():
#     nombres = {'MUN039':'Barbosa','MUN043':'Bello','MUN026': 'Caldas','MUN042':'Copacabana',
#            'MUN029':'Envigado','MUN101':u'Itagüí', 'MUN041':'Girardota','MUN028':'La Estrella',
#            'REG002':u'Med. Zona Urbana','REG004':'Med. Occidente','REG005':'Santa Elena',
#            'MUN106':u'Medellin','MUN027':'Sabaneta','CCA002':u'Guatapé','CCA018':u'La Fé',
#            'CCA015':u'La Herradura','CCA014':'La Vuelta','CCA005':'Miraflores','CCA019':'Piedras Blancas',
#            'CCA003':'Playas','CCA020':'Porce alta','CCA022':'Porce Baja','CCA021':'Porce Media',
#            'CCA006':'Porce III','CCA013':'Rio Grande II','CCA007':'San Francisco','CCA004':'Troneras',
#            'CCA011':u'Guarinó','CCA010':'jaguas','CCA012' :'Manso','CCA009' :'Miel','CCA008':'San Carlos',
#            'CORR001':'Altavista','REG001':'Mpios Sur','CORR002':'Palmitas','CORR003':'San Antonio de Prado',
#            'CORR004':u'San Cristóbal','CORR005':'Santa Elena','59':'ISAGEN','68': 'Jardin Botanico',
#            '73': 'Ciudadela Educativa La Vida','82': 'I.E Manuel Jose Caicedo',
#            '83':  'Centro de salud San Javier la Loma','84': 'Escuela CEDEPRO','105': 'Parque 3 Aguas','122': 'Tasajera',
#            '201': 'Torre SIATA','202': 'AMVA','203': 'UNAL-Sede Agronomia','204': 'Parque de las aguas',
#            '205': 'Santa Elena-Radar','206': 'Colegio Concejo de Itagui',
#            '207': 'Vivero EPM Piedras Blancas','271':'IE Jorge Eliecer Gaitán',
#            '229':'Alcaldía La Estrella','252':'Alcaldía Envigado',}
#     return nombres
#

#nombres_mun = collections.OrderedDict({
#'       Barbosa':'barbosa',
#'         Bello':'bello',
#'        Caldas':'caldas',
#'    Copacabana':'copacabana',
#'      Envigado':'envigado',
#u'        Itagüí':'itagui',
#'     Girardota':'girardota',
#'   La Estrella':'laestrella',
#'Med. Zona Urbana':'medCentro',
#'Med. Occidente':'medOccidente',
#'   Santa Elena':'santaElena',
#'      Sabaneta':'sabaneta'})
#
# nombres_mun = collections.OrderedDict({
# 'Barbosa':'barbosa',
# 'Bello':'bello',
# 'Caldas':'caldas',
# 'Copacabana':'copacabana',
# 'Envigado':'envigado',
# u'Itagüí':'itagui',
# 'Girardota':'girardota',
# 'La Estrella':'laestrella',
# 'Med. Zona Urbana':'medCentro',
# 'Med. Occidente':'medOccidente',
# 'Santa Elena':'santaElena',
# 'Sabaneta':'sabaneta'})
#==============================================================================
##Definicion de directorios
#workdir = 'C:/Users/Asus/Google Drive/Datos_nube/SIATA/Metereologia/Informe_semanal/'
#path_data = workdir + 'version_mensual/data_temp_mensual/'
#path_save = workdir + 'version_mensual/images_mesual/'
#
#path_font = 'C:/Users/Asus/Google Drive/Datos_nube/SIATA/Metereologia/Informe_semanal/avenir/'
#import matplotlib.font_manager as fm
#import matplotlib as mpl
#AvenirRoman  = fm.FontProperties(fname=path_font+'AvenirLTStd-Roman.ttf', size=16)
#path_historicos = workdir + 'historicos/'
#
#path_shapes = workdir+'shapes/'


#==============================================================================
#Fecha de la evaluación
#date_informe  = dt.date.today()
#date_informe  = dt.datetime(2018,1,29).date()
# date_informe  = dt.datetime.now().date()
# date_informe = date_informe +relativedelta(days=1)  #porque las imagenes corren el domingo
#
#
# idx = date_informe -relativedelta(months=1)
# ini_mon = idx.replace(day=1) #primer día
# final_mon = ini_mon + relativedelta(months=1)  - relativedelta(days=1) #ultimo día
#
# mon_informe = final_mon + dt.timedelta(1)
# #date_range = pd.date_range(start=mon,end=sun,freq='D')
# date = str(mon_informe)
#



#__________ Este grafico era el de los mapas de la ubicacion de la estacion con el maximo______
cmap_L = mpl.colors.ListedColormap([ColorInfo7,ColorInfo10,ColorInfo1,ColorInfo2])
bounds=[0.5,1.5,2.5,3.5,4.5]
norm_L = mpl.colors.BoundaryNorm(bounds, cmap_L.N)

# Limites del shape en coordenadas geográficas
min_lat = 5.978178; min_lon = -75.719430
max_lat = 6.512488; max_lon = -75.222057


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

Llamados = [1, 0, 1, 6, 20, 3, 1, 3, 2, 0]


AMVA = pd.DataFrame(Llamados, index=Municipios)

# def etiquetas_AMVA():
#     #Construidas con coordenadas x ini x final, y ini y final
#     #En un futuro se puede poner a que ponga a demás del nombre datos
#     '''Barbosa'''
#     plt.plot([-75.33,-75.45],[6.48,6.48],color='0.20',linewidth = 0.7)
#     plt.text(-75.45-0.065,6.48+0.005,'Barbosa',fontproperties = AvenirRoman)
#     '''Girardota'''
#     plt.plot([-75.45,-75.25],[6.40,6.40],color='0.20',linewidth = 0.7)
#     plt.text(-75.25-0.03,6.40+0.005,'Girardota',fontproperties = AvenirRoman)
#     '''Copacabana'''
#     plt.plot([-75.5,-75.25],[6.37,6.37],color='0.20',linewidth = 0.7)
#     plt.text(-75.25-0.03,6.37+0.005,'Copacabana',fontproperties = AvenirRoman)
#     '''Bello'''
#     plt.plot([-75.58,-75.25],[6.34,6.34],color='0.20',linewidth = 0.7)
#     plt.text(-75.25-0.03,6.34+0.005,'Bello',fontproperties = AvenirRoman)
#     '''Medellín: occidente'''
#     plt.plot([-75.66,-75.25],[6.29,6.29],color='0.20',linewidth = 0.7)
#     plt.text(-75.25-0.03,6.29+0.005,'Med, Occidente',fontproperties = AvenirRoman)
#     '''Medellín: centro'''
#     plt.plot([-75.6,-75.25],[6.26,6.26],color='0.20',linewidth = 0.7)
#     plt.text(-75.25-0.03,6.26+0.005,'Med, Centro',fontproperties = AvenirRoman)
#     '''Medellín: oriente'''
#     plt.plot([-75.53,-75.25],[6.23,6.23],color='0.20',linewidth = 0.7)
#     plt.text(-75.25-0.03,6.23+0.005,'Santa Elena',fontproperties = AvenirRoman)
#     '''Itaguí'''
#     plt.plot([-75.62,-75.25],[6.18,6.18],color='0.20',linewidth = 0.7)
#     plt.text(-75.25+0.01,6.18,u'Itagüí',fontproperties = AvenirRoman)
#     '''Envigado'''
#     plt.plot([-75.55,-75.25],[6.16,6.16],color='0.20',linewidth = 0.7)
#     plt.text(-75.25+0.01,6.16,u'Envigado',fontproperties = AvenirRoman)
#     '''La Estrella'''
#     plt.plot([-75.65,-75.25],[6.14,6.14],color='0.20',linewidth = 0.7)
#     plt.text(-75.25+0.01,6.14,u'La Estrella',fontproperties = AvenirRoman)
#     '''Sabaneta'''
#     plt.plot([-75.63,-75.25],[6.12,6.12],color='0.20',linewidth = 0.7)
#     plt.text(-75.25+0.01,6.12,u'Sabaneta',fontproperties = AvenirRoman)
#     '''Caldas'''
#     plt.plot([-75.63,-75.25],[6.05,6.05],color='0.20',linewidth = 0.7)
#     plt.text(-75.25-0.03,6.05+0.005,'Caldas',fontproperties = AvenirRoman)
#

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

cmap = plt.cm.jet
cmap = plt.cm.RdYlGn_r
# Buscar cmap.set_under('gris70')
bounds = np.arange(1,max(Llamados)+2)

def MapaLlamados(values,titulo,name,cmap,bounds,colorbar = False):
    # Datos MUN106,Medellin
    # AMVA=['Barbosa', 'Girardota'.....]
    #http://basemaptutorial.readthedocs.io/en/latest/shapefile.html
    rcParams['axes.linewidth']='0' #para desaparecer el cuadro de los mapas
    fig     = plt.figure(figsize=(9,9))
    ax      = fig.add_subplot(111)

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
                                         orientation='horizontal')
        cbar.set_label(u'Llamados a entidades de gestión del riesgo', fontsize = 12,fontproperties = AvenirRoman)
        cbar.update_ticks()
        cbar.ax.tick_params(colors=gris70,labelsize = 10)

    if titulo != False:
        plt.text(0.1,0.95,titulo, fontproperties = AvenirRoman,fontsize = 24,transform = ax.transAxes)

    plt.savefig(Path_figures+name,dpi=150,transparent=False,bbox_inches='tight')


MapaLlamados(AMVA,False,'123.png',cmap,bounds,colorbar = True)




barcode_font = Path_fuentes+'AvenirLTStd-Roman.ttf'
pdfmetrics.registerFont(TTFont("Avenir", barcode_font))
# barcode_font_blk = Path_fuentes+'AvenirLTStd-Black.otf'
# pdfmetrics.registerFont(TTFont("Avenir_blk", barcode_font_blk))

sizey, sizex = A2
JuanMariposo = canvas.Canvas(Path_figures+'JuanMariposo.pdf')
JuanMariposo.setPageSize((sizex, sizey))

JuanMariposo.setFont("Avenir", 24)

JuanMariposo.drawImage(Path_figures+'123.png', \
                      0.25*sizex, 0.1*sizey, width=32*cm, preserveAspectRatio=True)
# ==============================================================================
# Septiembre 2018
# barbosa = [['Barbosa',                           '',             ],
#            ['Zona alertada',                     'Fecha alerta','Hora Alerta' ],
#            ['Zona rural',                        '2018-09-29'  ,'17:38'       ],
#            ['Q. Los Chorros, Q. Cinconales',     '2018-09-29'  ,'21:22'       ],
#            ]
# Octubre 2018
barbosa = [['Barbosa',                           '',             ],
           ['Zona alertada',                         'Fecha alerta', 'Hora Alerta' ],
           [u'Q. La López'                          ,'2018-10-08'  , '15:56'       ],
           ]


BAR =Table(barbosa,[2.7*inch,1.*inch,0.8*inch], len(barbosa)*[0.25*inch])
BAR.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, gris),\
                        ('BOX',       (0,0), (-1,-1), 0.25, gris),\
                        ('ALIGN',     (0,0),(-1,-1),'CENTER'),\
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
# Septiembre 2018
# girardota = [['Girardota',                           '',             ],
#            ['Zona alertada',                     'Fecha alerta','Hora Alerta' ],
#            ['Zona rural',                        '2018-09-29'  ,'17:41'       ],
#            ]

#
# GIR =Table(girardota,[2.7*inch,1.*inch,0.8*inch], len(girardota)*[0.25*inch])
# GIR.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, gris),\
#                         ('BOX',       (0,0), (-1,-1), 0.25, gris),\
#                         ('ALIGN',     (0,0),(-1,-1),'CENTER'),\
#                         # ('VALIGN',   (0,0),(-1,-1),'MIDDLE'),\
#                         ('VALIGN',    (0,0),(-1,-1),'TOP'),\
#                         ('VALIGN',    (0,0),(-1,1),'TOP'),\
#                         ('FONTSIZE',  (0,0),(-1, 1), 12),\
#                         ('BACKGROUND',(0,0),(-1,1),ColorInfo6),\
#                         ('FONTSIZE',  (0,1),(-1,-1), 10),\
#                         ('TEXTCOLOR', (0,0),(-1,1),color.white),\
#                         ('SPAN',      (0,0), (-1,0)),\
#                         ]))

# ==============================================================================
# Septiembre 2018
# copacabana = [['Copacabana',                           '',             ],
#            ['Zona alertada',                     'Fecha alerta','Hora Alerta' ],
#            [u'Río Medellín (Puente Fundadores)', '2018-09-27'  ,'18:15'       ],
#            ]
# Ocutbre 2018
copacabana = [['Copacabana',                           '',             ],
           ['Zona alertada',                         'Fecha alerta', 'Hora Alerta' ],
           [u'Río Medellín (Puente Fundadores)'     ,'2018-10-06'  , '06:45'       ],
           ]


COP =Table(copacabana,[2.7*inch,1.*inch,0.8*inch], len(copacabana)*[0.25*inch])
COP.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, gris),\
                        ('BOX',       (0,0), (-1,-1), 0.25, gris),\
                        ('ALIGN',     (0,0),(-1,-1),'CENTER'),\
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
# Septiembre 2018
# bello = [['Bello',                           '',             ],
#            ['Zona alertada',                     'Fecha alerta','Hora Alerta' ],
#            ['Q. La Avelina',                     '2018-09-05'  ,'18:30'       ],
#            ['Q. La Avelina',                     '2018-09-05'  ,'20:26'       ],
#            ['Q. La Avelina',                     '2018-09-15'  ,'20:40'       ],
#            ['Q. La García',                      '2018-09-07'  ,'21:22'       ],
#            ['Q. La García',                      '2018-09-26'  ,'23:06'       ],
#            ['Q. El Hato',                        '2018-09-26'  ,'23:06'       ],
#            ['Q. La Loca',                        '2018-09-26'  ,'23:06'       ],
#            ['Q. La Loca',                        '2018-09-27'  ,'17:10'       ],
#            ['Q. La Madera',                      '2018-09-26'  ,'23:06'       ],
#            ['Q. La Madera',                      '2018-09-27'  ,'18:10'       ],
#            ['Zona urbana',                       '2018-09-27'  ,'16:40'       ],
#            ]
# Octubre 2018
bello = [['Bello',                           '',             ],
           ['Zona alertada',                         'Fecha alerta', 'Hora Alerta' ],
           [u'Q. El Hato'                           ,'2018-10-21'  , '15:20'       ],
           [u'Q. El Hato'                           ,'2018-10-04'  , '20:15'       ],
           [u'Q. La Loca'                           ,'2018-10-04'  , '20:15'       ],
           [u'Q. La Loca'                           ,'2018-10-04'  , '20:20'       ],
           [u'Q. La García'                         ,'2018-10-04'  , '20:15'       ],
           [u'Q. La García'                         ,'2018-10-10'  , '23:05'       ],
           ]



BEL =Table(bello,[2.7*inch,1.*inch,0.8*inch], len(bello)*[0.25*inch])
BEL.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, gris),\
                        ('BOX',       (0,0), (-1,-1), 0.25, gris),\
                        ('ALIGN',     (0,0),(-1,-1),'CENTER'),\
                        # ('VALIGN',   (0,0),(-1,-1),'MIDDLE'),\
                        ('VALIGN',    (0,0),(-1,-1),'TOP'),\
                        ('VALIGN',    (0,0),(-1,1),'TOP'),\
                        ('FONTSIZE',  (0,0),(-1, 1), 12),\
                        ('BACKGROUND',(0,0),(-1,1),ColorInfo6),\
                        ('FONTSIZE',  (0,1),(-1,-1), 10),\
                        ('TEXTCOLOR', (0,0),(-1,1),color.white),\
                        ('SPAN',      (0,0), (-1,0)),\
                        # Zona
                        ('SPAN',   (0,2), (0,3)),\
                        ('VALIGN', (0,2), (0,3),'MIDDLE'),\
                        ('SPAN',   (0,4), (0,5)),\
                        ('VALIGN', (0,4), (0,5),'MIDDLE'),\
                        ('SPAN',   (0,6), (0,7)),\
                        ('VALIGN', (0,6), (0,7),'MIDDLE'),\
                        # fecha
                        ('SPAN',   (1,3), (1,6)),\
                        ('VALIGN', (1,3), (1,6),'MIDDLE'),\
                        # Hora
                        ('SPAN',   (2,3), (2,4)),\
                        ('VALIGN', (2,3), (2,4),'MIDDLE'),\
                        ]))


# ==============================================================================
# Septiembre 2018
# medellin = [[u'Medellín',                           '',             ],
#            ['Zona alertada',                     'Fecha alerta','Hora Alerta' ],
#            [u'Q. Doña María',                    '2018-09-04'  ,'02:35'       ],
#            [u'Deprimido víal Feria de Ganado',   '2018-09-05'  ,'13:50'       ],
#            ['Q. La Presidenta',                  '2018-09-05'  ,'19:30'       ],
#            ['Q. La Yerbabuena',                  '2018-09-05'  ,'19:30'       ],
#            [u'Río Medellín (Puente de la 33)',   '2018-09-05'  ,'19:48'       ],
#            ['Q. Malpaso',                        '2018-09-05'  ,'20:04'       ],
#            ['Q. Malpaso',                        '2018-09-15'  ,'20:55'       ],
#            ['Q. Malpaso',                        '2018-09-26'  ,'22:50'       ],
#            ['Q. Malpaso',                        '2018-09-27'  ,'17:00'       ],
#            ['Villa Guadalupe',                   '2018-09-05'  ,'22:28'       ],
#            ['Q. La Guayabala',                   '2018-09-05'  ,'20:04'       ],
#            ['Q. La Guayabala',                   '2018-09-15'  ,'13:28'       ],
#            ['Q. La Altavista',                   '2018-09-15'  ,'13:40'       ],
#            ['Deprimidos viales urbanos',         '2018-09-27'  ,'16:30'       ],
#            ]
# Octubre 2018
medellin = [[u'Medellín',                           '',             ],
           ['Zona alertada',                     'Fecha alerta','Hora Alerta' ],
           [u'Deprimido víal Feria de Ganado'       ,'2018-10-01'  , '04:15'       ],
           [u'Q. Doña María'                        ,'2018-10-03'  , '15:00'       ],
           [u'Q. Doña María'                        ,'2018-10-03'  , '15:05'       ],
           [u'Q. Doña María'                        ,'2018-10-04'  , '18:20'       ],
           [u'Q. Doña María'                        ,'2018-10-04'  , '19:38'       ],
           [u'Q. La Presidenta'                     ,'2018-10-04'  , '17:25'       ],
           [u'Q. La Presidenta'                     ,'2018-10-06'  , '05:05'       ],
           [u'Q. La Presidenta'                     ,'2018-10-03'  , '14:05'       ],
           [u'Q. La Presidenta'                     ,'2018-10-09'  , '15:14'       ],
           [u'Q. La Presidenta'                     ,'2018-10-20'  , '02:15'       ],
           [u'Q. La Presidenta'                     ,'2018-10-31'  , '16:26'       ],
           [u'Q. La Guayabala'                      ,'2018-10-04'  , '17:75'       ],
           [u'Q. La Guayabala'                      ,'2018-10-03'  , '15:45'       ],
           [u'Q. Cañada Negra'                      ,'2018-10-03'  , '14:50'       ],
           [u'Río Medellín (Puente La Aguacatala)'  ,'2018-10-03'  , '14:20'       ],
           [u'Río Medellín (Puente La Aguacatala)'  ,'2018-10-19'  , '18:30'       ],
           [u'Q. Altavista'                         ,'2018-10-19'  , '18:30'       ],
           [u'Q. Altavista'                         ,'2018-10-19'  , '19:30'       ],
           [u'Q. Altavista'                         ,'2018-10-21'  , '15:15'       ],
           [u'Q. Santa Rita'                        ,'2018-10-17'  , '19:20'       ],
           ]

MED =Table(medellin,[2.7*inch,1.*inch,0.8*inch], len(medellin)*[0.25*inch])
MED.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, gris),\
                        ('BOX',       (0,0), (-1,-1), 0.25, gris),\
                        ('ALIGN',     (0,0),(-1,-1),'CENTER'),\
                        # ('VALIGN',   (0,0),(-1,-1),'MIDDLE'),\
                        ('VALIGN',    (0,0),(-1,-1),'TOP'),\
                        ('VALIGN',    (0,0),(-1,1),'TOP'),\
                        ('FONTSIZE',  (0,0),(-1, 1), 12),\
                        ('BACKGROUND',(0,0),(-1,1),ColorInfo6),\
                        ('FONTSIZE',  (0,1),(-1,-1), 10),\
                        ('TEXTCOLOR', (0,0),(-1,1),color.white),\
                        ('SPAN',      (0,0), (-1,0)),\
                        # Zona
                        ('SPAN',   (0,3), (0,6)),\
                        ('VALIGN', (0,3), (0,6),'MIDDLE'),\
                        ('SPAN',   (0,7), (0,12)),\
                        ('VALIGN', (0,7), (0,12),'MIDDLE'),\
                        ('SPAN',   (0,13), (0,14)),\
                        ('VALIGN', (0,13), (0,14),'MIDDLE'),\
                        ('SPAN',   (0,16), (0,17)),\
                        ('VALIGN', (0,16), (0,17),'MIDDLE'),\
                        ('SPAN',   (0,18), (0,20)),\
                        ('VALIGN', (0,18), (0,20),'MIDDLE'),\
                        # fecha
                        ('SPAN',   (1,3), (1,7)),\
                        ('VALIGN', (1,3), (1,7),'MIDDLE'),\
                        ('SPAN',   (1,5), (1,7)),\
                        ('VALIGN', (1,5), (1,7),'MIDDLE'),\
                        ('SPAN',   (1,14), (1,16)),\
                        ('VALIGN', (1,14), (1,16),'MIDDLE'),\
                        ('SPAN',   (1,17), (1,19)),\
                        ('VALIGN', (1,17), (1,19),'MIDDLE'),\
                        # Hora
                        ('SPAN',   (2,17), (2,18)),\
                        ('VALIGN', (2,17), (2,18),'MIDDLE'),\
                        ]))

# ==============================================================================
# Septiembre 2018
# itagui = [[u'Itagüí',                           '',             ],
#            ['Zona alertada',                     'Fecha alerta','Hora Alerta' ],
#            ['Q. La Tablaza',                     '2018-09-15'  ,'14:00'       ],
#            ]
# Octubre 2018
itagui = [[u'Itagüí',                           '',             ],
           ['Zona alertada',                         'Fecha alerta','Hora Alerta'  ],
           [u'Q. El Tablazo'                        ,'2018-10-03'  , '13:45'       ],
           [u'Q. El Tablazo'                        ,'2018-10-04'  , '17:45'       ],
           [u'Q. Doña María'                        ,'2018-10-04'  , '17:45'       ],
           ]


ITA =Table(itagui,[2.7*inch,1.*inch,0.8*inch], len(itagui)*[0.25*inch])
ITA.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, gris),\
                        ('BOX',       (0,0), (-1,-1), 0.25, gris),\
                        ('ALIGN',     (0,0),(-1,-1),'CENTER'),\
                        # ('VALIGN',   (0,0),(-1,-1),'MIDDLE'),\
                        ('VALIGN',    (0,0),(-1,-1),'TOP'),\
                        ('VALIGN',    (0,0),(-1,1),'TOP'),\
                        ('FONTSIZE',  (0,0),(-1, 1), 12),\
                        ('BACKGROUND',(0,0),(-1,1),ColorInfo6),\
                        ('FONTSIZE',  (0,1),(-1,-1), 10),\
                        ('TEXTCOLOR', (0,0),(-1,1),color.white),\
                        ('SPAN',      (0,0), (-1,0)),\
                        # Zona
                        ('SPAN',   (0,2), (0,3)),\
                        ('VALIGN', (0,2), (0,3),'MIDDLE'),\
                        # fecha
                        ('SPAN',   (1,3), (1,4)),\
                        ('VALIGN', (1,3), (1,4),'MIDDLE'),\
                        # Hora
                        ('SPAN',   (2,3), (2,4)),\
                        ('VALIGN', (2,3), (2,4),'MIDDLE'),\
                        ]))

# ==============================================================================
# Ocutbre 2018
envigado = [['Envigado',                           '',             ],
           [u'Zona alertada',                        'Fecha alerta', 'Hora Alerta' ],
           [u'Q. La Zuñiga'                         ,'2018-10-31'  , '16:35'       ],
           ]


ENV =Table(envigado,[2.7*inch,1.*inch,0.8*inch], len(envigado)*[0.25*inch])
ENV.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, gris),\
                        ('BOX',       (0,0), (-1,-1), 0.25, gris),\
                        ('ALIGN',     (0,0),(-1,-1),'CENTER'),\
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
# Septiembre 2018
# laestrella = [['La Esrella',                           '',             ],
#            ['Zona alertada',                     'Fecha alerta','Hora Alerta' ],
#            ['Q. La Bermejala',                   '2018-09-18'  ,'18:45'       ],
#            ['Q. 3 Aguas',                        '2018-09-28'  ,'15:00'       ],
#            ]
# Octubre 2018
laestrella = [['La Esrella',                           '',             ],
           ['Zona alertada',                         'Fecha alerta', 'Hora Alerta' ],
           [u'Q. La Bermejala'                      ,'2018-10-03'  , '14:25'       ],
           [u'Río Medellín (La Inmaculada)'         ,'2018-10-03'  , '14:30'       ],
           [u'Río Medellín (La Inmaculada)'         ,'2018-10-03'  , '14:35'       ],
           ]


STR =Table(laestrella,[2.7*inch,1.*inch,0.8*inch], len(laestrella)*[0.25*inch])
STR.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, gris),\
                        ('BOX',       (0,0), (-1,-1), 0.25, gris),\
                        ('ALIGN',     (0,0),(-1,-1),'CENTER'),\
                        # ('VALIGN',   (0,0),(-1,-1),'MIDDLE'),\
                        ('VALIGN',    (0,0),(-1,-1),'TOP'),\
                        ('VALIGN',    (0,0),(-1,1),'TOP'),\
                        ('FONTSIZE',  (0,0),(-1, 1), 12),\
                        ('BACKGROUND',(0,0),(-1,1),ColorInfo6),\
                        ('FONTSIZE',  (0,1),(-1,-1), 10),\
                        ('TEXTCOLOR', (0,0),(-1,1),color.white),\
                        ('SPAN',      (0,0), (-1,0)),\
                        # Zona
                        ('SPAN',   (0,3), (0,4)),\
                        ('VALIGN', (0,3), (0,4),'MIDDLE'),\
                        # fecha
                        ('SPAN',   (1,2), (1,4)),\
                        ('VALIGN', (1,2), (1,4),'MIDDLE'),\
                        ]))

# ==============================================================================
# Octubre 2018
sabaneta = [[u'Sabaneta',                           '',             ],
           ['Zona alertada',                         'Fecha alerta','Hora Alerta' ],
           [u'Q. La Sabanetica'                     ,'2018-10-03'  , '14:40'      ],
           [u'Q. La Sabanetica'                     ,'2018-10-14'  , '15:40'      ],
           ]


SAB =Table(sabaneta,[2.7*inch,1.*inch,0.8*inch], len(sabaneta)*[0.25*inch])
SAB.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, gris),\
                        ('BOX',       (0,0), (-1,-1), 0.25, gris),\
                        ('ALIGN',     (0,0),(-1,-1),'CENTER'),\
                        # ('VALIGN',   (0,0),(-1,-1),'MIDDLE'),\
                        ('VALIGN',    (0,0),(-1,-1),'TOP'),\
                        ('VALIGN',    (0,0),(-1,1),'TOP'),\
                        ('FONTSIZE',  (0,0),(-1, 1), 12),\
                        ('BACKGROUND',(0,0),(-1,1),ColorInfo6),\
                        ('FONTSIZE',  (0,1),(-1,-1), 10),\
                        ('TEXTCOLOR', (0,0),(-1,1),color.white),\
                        ('SPAN',      (0,0), (-1,0)),\
                        # Zona
                        ('SPAN',   (0,2), (0,3)),\
                        ('VALIGN', (0,2), (0,3),'MIDDLE'),\
                        ]))

# ==============================================================================
# Septiembre 2018
# caldas = [['Caldas',                           '',             ],
#            ['Zona alertada',                     'Fecha alerta','Hora Alerta' ],
#            ['Q. La Clara',                       '2018-09-16'  ,'00:20'       ],
#            ['Q. 3 Aguas',                        '2018-09-16'  ,'01:07'       ],
#            ['Q. Caldas',                         '2018-09-28'  ,'21:22'       ],
#            ]


# CAL =Table(caldas,[2.7*inch,1.*inch,0.8*inch], len(caldas)*[0.25*inch])
# CAL.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, gris),\
#                         ('BOX',       (0,0), (-1,-1), 0.25, gris),\
#                         ('ALIGN',     (0,0),(-1,-1),'CENTER'),\
#                         # ('VALIGN',   (0,0),(-1,-1),'MIDDLE'),\
#                         ('VALIGN',    (0,0),(-1,-1),'TOP'),\
#                         ('VALIGN',    (0,0),(-1,1),'TOP'),\
#                         ('FONTSIZE',  (0,0),(-1, 1), 12),\
#                         ('BACKGROUND',(0,0),(-1,1),ColorInfo6),\
#                         ('FONTSIZE',  (0,1),(-1,-1), 10),\
#                         ('TEXTCOLOR', (0,0),(-1,1),color.white),\
#                         ('SPAN',      (0,0), (-1,0)),\
#                         # fecha
#                         ('SPAN',   (1,2), (1,3)),\
#                         ('VALIGN', (1,2), (1,3),'MIDDLE'),\
#                         ]))



BAR.wrapOn(JuanMariposo, 600, 900)
# GIR.wrapOn(JuanMariposo, 600, 900)
COP.wrapOn(JuanMariposo, 600, 900)
BEL.wrapOn(JuanMariposo, 600, 900)
MED.wrapOn(JuanMariposo, 600, 900)
ITA.wrapOn(JuanMariposo, 600, 900)
ENV.wrapOn(JuanMariposo, 600, 900)
STR.wrapOn(JuanMariposo, 600, 900)
SAB.wrapOn(JuanMariposo, 600, 900)
# CAL.wrapOn(JuanMariposo, 600, 900)

MED.drawOn(JuanMariposo, 775.,  325.)
BAR.drawOn(JuanMariposo, 450.,  925.)
ENV.drawOn(JuanMariposo, 1125., 840.)
COP.drawOn(JuanMariposo, 1125., 760.)
STR.drawOn(JuanMariposo, 1125., 630.)
SAB.drawOn(JuanMariposo, 1125., 925.)
BEL.drawOn(JuanMariposo, 1125., 450.)
ITA.drawOn(JuanMariposo, 1125,  325.)




JuanMariposo.save()


os.system('scp '+Path_figures+'JuanMariposo.pdf ccuervo@192.168.1.74:/var/www/cmcuervol/')


TextoLlamados = "Durante el mes se realizaron 37 llamados a las líneas de emergencia \
                 municipales. Como se observa en el mapa, Medellín con 20 alertas \
                 presentadas ante las entidades de gestión del riesgo fue ampliamente \
                 el municipo con más alertas, seguido de Bello con 6 alertas. Es \
                 importante resaltar que tanto en Caldas como en Girardota no se \
                 registraro alertas ante las entidades de gestión del riesgo. "

TextoTorta = "La gráfica de torta muestra un resumen de los acumulados máximos de \
              precipitación de todos los eventos que superaron 5 mm de acumulado \
              sobre el valle de Aburrá. Durante octubre se registraron 38 eventos \
              de precipitación, de los cuales sólo 6 de ellos tuvieron acumulados \
              menores a 15 mm y  el 34% de los eventos tuvieron un acumulado superior \
              a 45 mm, indicando que durante el mes predominaron lluvias intensas \
              con duraciones prolongadas que permitieron acumular una lámina de agua \
              considerable por cada evento."

print 'Hello world'
