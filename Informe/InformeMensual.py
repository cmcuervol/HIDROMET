# -*- coding: utf-8 -*-

import numpy as np
import matplotlib
matplotlib.use ("template")
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import datetime as dt
import pandas as pd
import os
import sys
import glob

import argparse
from tqdm import tqdm

Path = '/home/ccuervo/InformeMensual/'
path_font = '/home/ccuervo/Fuentes/'
Path_metadatos = '/home/torresiata/reporte_eventos/Metadatos/'

parser = argparse.ArgumentParser()
parser.add_argument("-y", "--year",      default=dt.datetime.now().year, help="Year for te report")
parser.add_argument("-m", "--month",     default=dt.datetime.now().month, help="month of the report")
parser.add_argument("-u", "--user",      default='cmcuervol', help="user to copy the results")
parser.add_argument("-ip","--ip",        default='192.168.2.129', help="ip to copy the results")
parser.add_argument("-d", "--directory", default='/Users/cmcuervol/Desktop/InformeMensual/Figuras/Operacionales/', help="host directory to copy the results")
parser.add_argument("-scp", "--hostcopy",default=True, help="Boolean to allow the results copy")
args = parser.parse_args()


year  = int(args.year)
month = int(args.month)
# year  = 2018
# month = 5


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

AvenirRoman  = fm.FontProperties(fname=path_font+'AvenirLTStd-Roman.ttf', size=12)
AvenirRomanT = fm.FontProperties(fname=path_font+'AvenirLTStd-Roman.ttf', size=12)


def listador(directorio, inicio, final):
    lf = []
    lista = os.listdir(directorio)
    for i in lista:
        if i.startswith(inicio) and i.endswith(final):
            lf.append(i)
    return lf.sort()

evento     =[]
fecha      =[]
intensidad =[]
mint       =[]
acumulado  =[]
macum      =[]
duracion   =[]

pbar = tqdm(total=len(glob.glob(Path_metadatos+'*')), desc='Reading reports: ')
for i in sorted(glob.glob(Path_metadatos+'*')):
    # print i
    numero = int(i.split('/')[-1])
    # print numero
    a = np.genfromtxt(i + '/maximos.txt', delimiter=',', dtype=str)
    evento    .append(numero)
    fecha     .append(pd.to_datetime(a[0]))
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
    pbar.update(1)
pbar.close()


evento     = np.array(evento)
fecha      = np.array(fecha)
intensidad = np.array(intensidad)
mint       = np.array(mint)
acumulado  = np.array(acumulado)
macum      = np.array(macum)
duracion   = np.array(duracion)


idx = np.where((fecha>=dt.datetime(year, month, 1))&(fecha<dt.datetime(year, month+1, 1)))[0]


faltantes = 1+ evento[idx][-1]- evento[idx][0] - len(evento[idx])

if faltantes != 0 :
    print ('***********************************')
    print ("WARNING, faltan %s eventos" %str(faltantes))
    print ('***********************************')
Intensidad = intensidad[idx]
Acumulado  = acumulado [idx]

filew = open(Path+'LaTeX.txt', 'w')
for i in idx:
    filew.write(str(evento[i])+' & ' )
    filew.write(fecha[i].strftime('%Y-%m-%d')+' & ')
    filew.write(str(round(intensidad[i], 2))+' mm/hora & ' )
    filew.write(mint[i]+' & ')
    filew.write(str(round(acumulado[i], 2))+' mm & ' )
    filew.write(macum[i]+' & ')
    filew.write(duracion[i]+' \\rule[-0.3cm]{0cm}{0.8cm} '+'\\'+'\\'+' \\hline \n')

filew.close()

def Histrogramador(Values, label, name, bins = 10):
    # Genera el histograma de valores
    h,b = np.histogram(Values,bins=bins)
    # h = h.astype(float); h = h / h.sum()
    b = (b[1:]+b[:-1])/2.0
    # Obtiene la figura
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.plot(b,h,color=ColorInfo1,lw=2)
    ax.fill_between(b,h,color=ColorInfo1,alpha=0.2)
    ax.set_xlabel(label,size=15)
    ax.set_ylabel('Frecuencia Absoluta',size=15)
    ax.grid(True)
    ax.legend(loc=0)
    ax.set_ylim(bottom=0)
    # ax.set_xlim(-250,0)
    plt.savefig(Path+name+'.png')
    return h

Histrogramador(Intensidad, 'Intensidad (mm/hora)', 'Intensidad')
Histrogramador(Acumulado,  'Acumulado (mm)'      , 'Acumulado')


# Eventos de todo el año archivo "Actualizado"
# Tablazo = np.genfromtxt(Path_font+'Actualizado.csv', delimiter = ',', dtype = str)


# Acumulado  = Tablazo[1:,4].astype(float)
# Intensidad = Tablazo[1:,8].astype(float)

Total = Acumulado.shape[0]
Menor15 = Total - np.where(Acumulado>15)[0].shape[0]
Entre15_30 = np.where((Acumulado>15)&(Acumulado<30))[0].shape[0]
Entre30_45 = np.where((Acumulado>30)&(Acumulado<45))[0].shape[0]
Mayor45    = np.where(Acumulado>45)[0].shape[0]

sizes  = [Menor15, Entre15_30, Entre30_45, Mayor45]
# sizes  = [6,7,3,6]

labels = ['Menor 15mm', 'Entre 15mm y 30mm', 'Entre 30mm y 45mm', 'Mayor a 45mm']
# labels = ['Menor 15mm', 'Entre 15mm y 30mm', 'Entre 30mm y 45mm']



def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct


my_cmap = mpl.colors.ListedColormap([ColorInfo1, ColorInfo7, ColorInfo9, ColorInfo10])
color_vals = range(len(labels))
my_norm = mpl.colors.Normalize(color_vals[0], color_vals[-1])


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

explode = (0.05, 0.05, 0.05, 0.05)
# explode = (0.05, 0.05, 0.05)
plt.close()
plt.cla()
plt.clf()
fig = plt.figure()
fig.set_figheight(4.0)
fig.set_figwidth(6.0)
ax = fig.add_axes([0,0,0.75,0.9])
# ax.text(0.4, 1.1, u'Acumulados máximos de los eventos de precipitación \n entre '+startday.strftime('%Y-%m-%d')+\
#             ' y '+end.strftime('%Y-%m-%d'),fontproperties=AvenirRoman, color=gris70, fontsize=12,horizontalalignment='center', )
patches, texts, autotexts = ax.pie(sizes, explode=explode, labels=None,autopct=make_autopct(sizes),\
                                    shadow=False, startangle=45, colors=my_cmap(my_norm(color_vals)))
plt.setp(autotexts,fontproperties=AvenirRoman, fontsize= 10)
plt.setp(texts,    fontproperties=AvenirRoman,fontsize= 10)
ax.axis('equal')
ax_cb = fig.add_axes([.70,.25,.03,.50])
colorbar = mpl.colorbar.ColorbarBase(ax_cb, cmap=my_cmap, norm=my_norm, ticks=[0.4,1.1,1.9,2.6])
colorbar.set_ticklabels(labels)
colorbar.ax.tick_params(colors=gris70,labelsize=10)

plt.savefig(Path+'Torta.png', format = 'png', dpi = 250)
plt.close()
if args.hostcopy==True:
    os.system ('scp '+Path+'LaTeX.txt '+Path+'*png '+args.user+'@'+args.ip+':'+args.directory)

print 'Hello world'
