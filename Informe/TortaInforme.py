#!/usr/bin/env python
# encoding: utf-8


import matplotlib
matplotlib.use ("template")
import os
import sys
import argparse
import numpy as np
import glob as gb
import pandas as pd
import datetime as dt
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


# Path_RWP = '/home/cmcuervol/Desktop/RWP/'
Path_fuentes = '/home/cmcuervol/Fuentes/'
Path_metadatos = '/home/cmcuervol/Desktop/MapasInforme/Informes/'

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--sizes",default='', help="sizes of the pie chart: 'Menor 15 mm', 'Entre 15 y 30 mm', 'Entre 30 y 45 mm', 'Mayor a 45 mm' ")
parser.add_argument("-f", "--fecha",default='', help="date of the next day in format %Y-%m-%d")
args = parser.parse_args()




os.system('rsync -avz ccuervo@192.168.1.74:/home/torresiata/reporte_eventos/Metadatos/ '+Path_metadatos)

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

# Types of fonts Avenir
AvenirHeavy = fm.FontProperties(fname=Path_fuentes+'AvenirLTStd-Heavy.otf')
AvenirBook  = fm.FontProperties(fname=Path_fuentes+'AvenirLTStd-Book.otf')
AvenirBlack = fm.FontProperties(fname=Path_fuentes+'AvenirLTStd-Black.otf')
AvenirRoman = fm.FontProperties(fname=Path_fuentes+'AvenirLTStd-Roman.ttf')


def listador(directorio, inicio, final):
    lf = []
    lista = os.listdir(directorio)
    for i in lista:
        if i.startswith(inicio) and i.endswith(final):
            lf.append(i)
    return lf

try:
    # lastday = dt.datetime.strptime(sys.argv[1], '%Y-%m-%d')
    lastday = dt.datetime.strptime(args.fecha, '%Y-%m-%d')
except:
    # lastday = dt.datetime.now()
    lastday = dt.datetime(dt.date.today().year, dt.date.today().month, dt.date.today().day)

# lastday = dt.datetime(2018,7,2)
startday = lastday-dt.timedelta(days=7)
endday   = lastday-dt.timedelta(days=1)

Path_informe = '/home/atlas/informe_hidromet/'+startday.strftime('%Y%m%d')+'_'+endday.strftime('%Y%m%d')+'/Precipitacion/'


evento     =[]
fecha      =[]
intensidad =[]
mint       =[]
acumulado  =[]
macum      =[]
duracion   =[]

for i in sorted(gb.glob(Path_metadatos+'*')):
    # print i
    numero = int(i.split('/')[-1])
    print numero
    a = np.genfromtxt(i + '/maximos.txt', delimiter=',', dtype=str)
    evento    .append(numero)
    # fecha     .append(pd.to_datetime(a[0]))
    intensidad.append(float(a[2]))
    try:
        float(a[6])
        a = np.insert(a,6,'')
        mint.append(a[5])
    except:
        mint.append(a[5]+' - '+a[6])

    acumulado .append(float(a[7]))

    if len(a)==11:
        macum.append(a[10])
    else:
        macum.append(a[10]+' - '+a[11])

    b = pd.read_csv(i+'/textforlatex.txt',header=None,nrows=2,usecols=[0,1])
    diff=(pd.to_datetime(' '.join(list(b.iloc[1].values)))-pd.to_datetime(' '.join(list(b.iloc[0].values))))
    days, seconds = diff.days, diff.seconds
    hours   = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    duracion.append(str(hours).zfill(2)+':'+str(minutes).zfill(2)+':'+str(seconds).zfill(2))
    fecha   .append(pd.to_datetime(b[0][0]))

evento     = np.array(evento)
fecha      = np.array(fecha)
intensidad = np.array(intensidad)
mint       = np.array(mint)
acumulado  = np.array(acumulado)
macum      = np.array(macum)
duracion   = np.array(duracion)


# idx = np.where((fecha>=dt.datetime(year, month, 1))&(fecha<dt.datetime(year, month+1, 1)))[0]
idx = np.where((fecha>=startday)&(fecha<=endday))[0]

faltantes = 1+ evento[idx][-1]- evento[idx][0] - len(evento[idx])

if faltantes != 0 :
    print "******************************"
    print "WARNING, faltan %s eventos" %str(faltantes)
    print "******************************"

# Intensidad = intensidad[idx]
Acumulado  = acumulado [idx]


Total      = Acumulado.shape[0]
Menor15    = Total - np.where(Acumulado>15)[0].shape[0]
Entre15_30 = np.where((Acumulado>=15)&(Acumulado<30))[0].shape[0]
Entre30_45 = np.where((Acumulado>=30)&(Acumulado<45))[0].shape[0]
Mayor45    = np.where( Acumulado>=45)[0].shape[0]


# if len(sys.argv) == 1:
#     sizes  = [Menor15, Entre15_30, Entre30_45, Mayor45]
# else:
#     sizes = list(np.array(sys.argv[2].split(',')).astype(float))

try:
    sizes = list(np.array(args.sizes.split(',')).astype(float))
    event = list(np.array(args.sizes.split(',')).astype(float))
except:
    sizes  = [Menor15, Entre15_30, Entre30_45, Mayor45]
    event  = [Menor15, Entre15_30, Entre30_45, Mayor45]

labels = ['Menor 15 mm', 'Entre 15 y 30 mm', 'Entre 30 y 45 mm', 'Mayor a 45 mm']

colores = [ColorInfo1, ColorInfo7, ColorInfo9, ColorInfo10]
explode = (0.05, 0.05, 0.05, 0.05)

Acumula = np.array([0, 15, 30, 45, 60])
Acumula = 0.5*(Acumula[:-1]+Acumula[1:])

try:
    pos = np.where(np.array(sizes)==0)[0][0]
except:
    pos = None

if pos != None:
        del colores[pos]
        del sizes[pos]
        explode = tuple(np.delete(explode, pos))
        # Acumula = np.delete(Acumula, pos)


my_cmap_barra = mpl.colors.ListedColormap([ColorInfo1, ColorInfo7, ColorInfo9, ColorInfo10])
color_vals_barra = range(len(colores))
my_norm_barra = mpl.colors.Normalize(color_vals_barra[0], color_vals_barra[-1])


my_cmap_f = mpl.colors.ListedColormap(colores)
color_vals = range(len(colores))
my_norm_f = mpl.colors.Normalize(color_vals[0], color_vals[-1])


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct


plt.rc(    'font',
    size = 12,
    family = fm.FontProperties(
        fname = '{}AvenirLTStd-Book.otf'.format(Path_fuentes)
        ).get_name()
)

typColor = '#%02x%02x%02x' % (115,115,115)
plt.rc('axes',labelcolor=typColor, edgecolor=typColor,)#facecolor=typColor)
plt.rc('axes.spines',right=False, top=False, )#left=False, bottom=False)
plt.rc('text',color= typColor)
plt.rc('xtick',color=typColor)
plt.rc('ytick',color=typColor)
plt.close()
plt.cla()
plt.clf()

fig = plt.figure()
fig.set_figheight(4.0)
fig.set_figwidth(6.0)
ax = fig.add_axes([0,0,0.75,0.9])
ax.text(0.4, 1.1, u'Acumulados máximos de los eventos de precipitación \n entre '+startday.strftime('%Y-%m-%d')+\
            ' y '+endday.strftime('%Y-%m-%d'),fontproperties=AvenirRoman, color=gris70, fontsize=12,horizontalalignment='center')
patches, texts, autotexts = ax.pie(sizes, explode=explode, labels=None,autopct=make_autopct(sizes),\
                                    shadow=False, startangle=45, colors=my_cmap_f(my_norm_f(color_vals)))
# patches, texts, autotexts = ax.pie(sizes, explode=explode, labels=None, autopct=make_autopct(sizes),\
#                                     shadow=False, startangle=45, colors=colores)

plt.setp(autotexts,fontproperties=AvenirRoman, fontsize= 10)
plt.setp(texts,    fontproperties=AvenirRoman,fontsize= 10)
ax.axis('equal')
ax_cb = fig.add_axes([.70,.25,.03,.50])

if pos != None:
    colorbar = mpl.colorbar.ColorbarBase(ax=ax_cb, cmap=my_cmap_barra, norm=my_norm_barra, ticks=[0.25,0.75,1.25,1.75])
else:
    colorbar = mpl.colorbar.ColorbarBase(ax=ax_cb, cmap=my_cmap_barra, norm=my_norm_barra, ticks=[0.4,1.1,1.9,2.6])

colorbar.set_ticklabels(labels)
colorbar.ax.tick_params(colors=gris70,labelsize=10)

# plt.tight_layout()
plt.savefig(Path_informe+'Torta.png', format = 'png', dpi = 250, bbox_inches='tight', transparent=True)

# Bar plot
bar_width = 7.5
fig = plt.figure()
fig.set_figheight(4.0)
fig.set_figwidth(6.0)
ax = fig.add_subplot(1,1,1)
ax.set_title(u'Acumulados máximos de los eventos de precipitación \n entre '+startday.strftime('%Y-%m-%d')+\
            ' y '+endday.strftime('%Y-%m-%d'),fontproperties=AvenirRoman, color=gris70, fontsize=12,horizontalalignment='center')
ax.bar(Acumula, event, color=[ColorInfo1, ColorInfo7, ColorInfo9, ColorInfo10], width=bar_width)
Percent = event/(np.sum(event).astype(float))*100
map(lambda i: ax.text(Acumula[i]-0.5*bar_width, event[i],'%.1f' %(Percent[i])+'%') , range(len(event)))
ax.set_ylabel('Cantidad de eventos')
ax.set_xlabel(u'Acumulado máximo de precipitación ')
plt.xticks(Acumula, labels, fontsize =8)
from matplotlib.ticker import MaxNLocator
ax.yaxis.set_major_locator(MaxNLocator(integer=True))

plt.savefig(Path_informe+'Barras.png', format = 'png', dpi = 250, bbox_inches='tight', transparent=True)

os.system('scp '+ Path_informe+'Torta.png '+Path_informe+'Barras.png ccuervo@192.168.1.74:/var/www/cmcuervol/')

print "Hello world"
