#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gdal
import matplotlib
matplotlib.use('Agg')
# %matplotlib inline

import MySQLdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import basemap
from matplotlib import rc
import matplotlib.colors as colors
# from wmf import wmf
import matplotlib.font_manager as fm
import datetime as dt
import sys
import matplotlib.dates as mdates
import argparse


# parser = argparse.ArgumentParser(description='Recibe las fechas para generar el mapa de acumulados')
#
# parser.add_argument('-fi',help='fecha inicial',required='True',default='1',type=str)
# parser.add_argument('-ff',help='fecha final',required='True',default='1',type=str)
#
# args = parser.parse_args()
#
# fecha1toda=args.fi
# fecha2toda=args.ff

lastday  = dt.datetime.now()
# lastday  = dt.datetime(2019,11,25)
startday = lastday-dt.timedelta(days=7)

endday = lastday-dt.timedelta(days=1)

fecha1toda = startday.strftime('%Y-%m-%d') + ' 00:00:00'
fecha2toda = endday  .strftime('%Y-%m-%d') + ' 23:59:59'

# Path_informe = '/home/torresiata/reporte_eventos/temporal/Figuras/boletin/'
# Path         = '/home/torresiata/reporte_eventos/MapasInforme/'
# Path_fuentes = '/home/torresiata/reporte_eventos/MapasInforme/Fuentes'

Path_informe = '/home/atlas/informe_hidromet/'+startday.strftime('%Y%m%d')+'_'+endday.strftime('%Y%m%d')+'/Precipitacion/'
Path         = '/home/cmcuervol/Desktop/MapasInforme/'
Path_fuentes = '/home/cmcuervol/Fuentes/'

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


# def pluvio(cliente,fi,ff,df2):
#
#     host   = "192.168.1.74"
#     user   = "siata_Oper"
#     passwd = "si@t@64512_operacional"
#     dbname = "siata"
#
#     columnas=['cliente','sum(p1)/1000.','sum(p2)/1000.']
#
#     fecha1toda=fi
#     fecha1=fecha1toda.split(' ')[0]
#     fecha2toda=ff
#     fecha2=fecha2toda.split(' ')[0]
#
#     query = "select cliente,sum(p1)/1000.,sum(p2)/1000. from datos where cliente={} and fecha BETWEEN '{}' and '{}' AND hora BETWEEN '00:00:00' AND '23:59:59' AND concat(fecha, ' ', hora) BETWEEN '{}' AND '{}'".format(cliente,fecha1,fecha2,fecha1toda,fecha2toda)+" and datos.calidad<100;"
#
#
#     conn_db = MySQLdb.connect (host, user, passwd, dbname)
#     db_cursor = conn_db.cursor ()
#     db_cursor.execute (query)
#     data = db_cursor.fetchall ()
#
#     # #Construimos DataFrame
#     df = pd.DataFrame(np.array(data),columns=columnas)
#
#     # #Importante --- SIEMPRE Cerrar
#     conn_db.close ()
#
#     try:
#         return pd.concat([df2,df])
#     except:
#         return df
#
#

class consulta_mysql(object):
    "CLASE para obetner datos en formato pandas de la base de datos"
    def __init__(self, source_info):
        self.source_info = source_info
        # self.user = 'torresiata'
        self.user = 'siata_Consulta'
        # self.host = '192.168.1.100'
        self.host = '192.168.1.74'
        # self.password = 'TlV729phz'
        self.password = 'si@t@64512_C0nsult4'
        if (self.source_info == 'EPM'):
            self.database = 'estacionesDATA'
            self.table = 'epmData'
        if (self.source_info == 'SIATA'):
            self.database = 'siata'
            self.table = 'datos'
        if (self.source_info == 'SIATA_Vaisala'):
            self.database = 'siata'
            self.table = 'vaisala'
        if (self.source_info == 'SIATA_Thiess'):
            self.database = 'siata'
            self.table = 'meteo_thiess'
        if (self.source_info == 'SIATA_Tramas'):
            self.database = 'siata'
            self.table = 'tramas'

        self.cumulative = False

    def make_query(self, fecha_inicial, fecha_final, estacion):
        datos = [self.host, self.user, self.password, self.database]
        if self.cumulative == False:
            if self.source_info == 'EPM':
                query_mysql = "SELECT fecha, P FROM "+self.table+" WHERE idestacion="+estacion+" and P IS NOT NULL and calidad < 100.0 and fecha between '"+fecha_inicial+"' and '"+fecha_final+"'"
            if self.source_info == 'SIATA':
                # query_mysql = "SELECT CONCAT(fecha,' ', hora), p1/1000.0, p2/1000.0,calidad FROM "+self.table+" WHERE cliente="+estacion+" and p1 IS NOT NULL and p2 IS NOT NULL and calidad < 100.0  and STR_TO_DATE( CONCAT( fecha, ' ', hora ) , '%Y-%m-%d %k:%i:%s' ) between '"+fecha_inicial+"' and '"+fecha_final+"'" + "AND hora BETWEEN '00:00:00' AND '23:59:59'"
                query_mysql = "SELECT CONCAT(fecha,' ', hora), p1/1000.0, p2/1000.0,calidad FROM "+self.table+" WHERE cliente="+estacion+" and p1 IS NOT NULL and p2 IS NOT NULL and calidad < 100.0  and fecha BETWEEN '"+fecha_inicial[:10]+"' and '"+fecha_final[:10]+"'" + "AND hora BETWEEN '00:00:00' AND '23:59:59'"
            if self.source_info == 'SIATA_Tramas':
                # query_mysql = "SELECT CONCAT(fecha,' ', hora), P, calidad FROM "+self.table+" WHERE cliente="+estacion+" and P IS NOT NULL and calidad < 100.0 and STR_TO_DATE( CONCAT( fecha, ' ', hora ) , '%Y-%m-%d %k:%i:%s' ) between '"+fecha_inicial+"' and '"+fecha_final+"'" +"AND hora BETWEEN '00:00:00' AND '23:59:59'"
                query_mysql = "SELECT CONCAT(fecha,' ', hora), P, calidad FROM "+self.table+" WHERE cliente="+estacion+" and P IS NOT NULL and calidad < 100.0 and fecha BETWEEN '"+fecha_inicial[:10]+"' and '"+fecha_final[:10]+"'" + "AND hora BETWEEN '00:00:00' AND '23:59:59'"
            if self.source_info == 'SIATA_Vaisala':
                # query_mysql = "SELECT CONCAT(fecha,' ', hora), rc/100.0, calidad FROM "+self.table+" WHERE cliente="+estacion+" and rc IS NOT NULL and calidad < 100.0 and STR_TO_DATE( CONCAT( fecha, ' ', hora ) , '%Y-%m-%d %k:%i:%s' ) between '"+fecha_inicial+"' and '"+fecha_final+"'"+"AND hora BETWEEN '00:00:00' AND '23:59:59'"
                query_mysql = "SELECT CONCAT(fecha,' ', hora), rc/100.0, calidad FROM "+self.table+" WHERE cliente="+estacion+" and rc IS NOT NULL and calidad < 100.0 and fecha BETWEEN '"+fecha_inicial[:10]+"' and '"+fecha_final[:10]+"'" + "AND hora BETWEEN '00:00:00' AND '23:59:59'"
            if self.source_info == 'SIATA_Thiess':
                # query_mysql = "SELECT CONCAT(fecha,' ', hora), p, calidad FROM "+self.table+" WHERE cliente="+estacion+" and p IS NOT NULL and calidad < 100.0 and STR_TO_DATE( CONCAT( fecha, ' ', hora ) , '%Y-%m-%d %k:%i:%s' ) between '"+fecha_inicial+"' and '"+fecha_final+"'"+"AND hora BETWEEN '00:00:00' AND '23:59:59'"
                query_mysql = "SELECT CONCAT(fecha,' ', hora), p, calidad FROM "+self.table+" WHERE cliente="+estacion+" and p IS NOT NULL and calidad < 100.0 aand fecha BETWEEN '"+fecha_inicial[:10]+"' and '"+fecha_final[:10]+"'" + "AND hora BETWEEN '00:00:00' AND '23:59:59'"
            if self.source_info == 'Disdrometro':
                #print 'hago la consulta en disdro'
                query_mysql = "SELECT fecha_hora, var8, var9, var10, var13 FROM "+self.table+" WHERE cliente="+estacion+" and fecha_hora between '"+fecha_inicial+"' and '"+fecha_final+"'"
        else:
            if self.source_info == 'EPM':
                query_mysql = "SELECT fecha, sum(P) FROM "+self.table+" WHERE idestacion="+estacion+" and P IS NOT NULL and calidad < 100.0 and fecha between '"+fecha_inicial+"' and '"+fecha_final+"'"
            if self.source_info == 'SIATA':
                # query_mysql = "SELECT CONCAT(fecha,' ', hora), sum(p1)/1000.0, sum(p2)/1000.0 FROM "+self.table+" WHERE cliente="+estacion+" and p1 IS NOT NULL and p2 IS NOT NULL and calidad < 100.0  and STR_TO_DATE( CONCAT( fecha, ' ', hora ) , '%Y-%m-%d %k:%i:%s' ) between '"+fecha_inicial+"' and '"+fecha_final+"'" + "AND hora BETWEEN '00:00:00' AND '23:59:59'"
                query_mysql = "SELECT CONCAT(fecha,' ', hora), sum(p1)/1000.0, sum(p2)/1000.0 FROM "+self.table+" WHERE cliente="+estacion+" and p1 IS NOT NULL and p2 IS NOT NULL and calidad < 100.0  and fecha BETWEEN '"+fecha_inicial[:10]+"' and '"+fecha_final[:10]+"'" + "AND hora BETWEEN '00:00:00' AND '23:59:59'"
            if self.source_info == 'SIATA_Tramas':
                # query_mysql = "SELECT CONCAT(fecha,' ', hora), sum(P) FROM "+self.table+" WHERE cliente="+estacion+" and P IS NOT NULL and calidad < 100.0 and STR_TO_DATE( CONCAT( fecha, ' ', hora ) , '%Y-%m-%d %k:%i:%s' ) between '"+fecha_inicial+"' and '"+fecha_final+"'" +"AND hora BETWEEN '00:00:00' AND '23:59:59'"
                query_mysql = "SELECT CONCAT(fecha,' ', hora), sum(P) FROM "+self.table+" WHERE cliente="+estacion+" and P IS NOT NULL and calidad < 100.0 and fecha BETWEEN '"+fecha_inicial[:10]+"' and '"+fecha_final[:10]+"'" + "AND hora BETWEEN '00:00:00' AND '23:59:59'"
            if self.source_info == 'SIATA_Vaisala':
                # query_mysql = "SELECT CONCAT(fecha,' ', hora), sum(rc)/100.0 FROM "+self.table+" WHERE cliente="+estacion+" and rc IS NOT NULL and calidad < 100.0 and STR_TO_DATE( CONCAT( fecha, ' ', hora ) , '%Y-%m-%d %k:%i:%s' ) between '"+fecha_inicial+"' and '"+fecha_final+"'"+"AND hora BETWEEN '00:00:00' AND '23:59:59'"
                query_mysql = "SELECT CONCAT(fecha,' ', hora), sum(rc)/100.0 FROM "+self.table+" WHERE cliente="+estacion+" and rc IS NOT NULL and calidad < 100.0 and fecha BETWEEN '"+fecha_inicial[:10]+"' and '"+fecha_final[:10]+"'" + "AND hora BETWEEN '00:00:00' AND '23:59:59'"
            if self.source_info == 'SIATA_Thiess':
                # query_mysql = "SELECT CONCAT(fecha,' ', hora), sum(p) FROM "+self.table+" WHERE cliente="+estacion+" and p IS NOT NULL and calidad < 100.0 and STR_TO_DATE( CONCAT( fecha, ' ', hora ) , '%Y-%m-%d %k:%i:%s' ) between '"+fecha_inicial+"' and '"+fecha_final+"'"+"AND hora BETWEEN '00:00:00' AND '23:59:59'"
                query_mysql = "SELECT CONCAT(fecha,' ', hora), sum(p) FROM "+self.table+" WHERE cliente="+estacion+" and p IS NOT NULL and calidad < 100.0 and fecha BETWEEN '"+fecha_inicial[:10]+"' and '"+fecha_final[:10]+"'" + "AND hora BETWEEN '00:00:00' AND '23:59:59'"
            if self.source_info == 'Disdrometro':
                #print 'hago la consulta en disdro'
                query_mysql = "SELECT fecha_hora, sum(var8), sum(var9), sum(var10), sum(var13) FROM "+self.table+" WHERE cliente="+estacion+" and fecha_hora between '"+fecha_inicial+"' and '"+fecha_final+"'"

        print query_mysql
        connection = MySQLdb.connect(*datos) # Conectar a la base de datos
        cursor = connection.cursor()         # Crear un cursor
        cursor.execute(query_mysql)          # Ejecutar una consulta
        if query_mysql.upper().startswith('SELECT'):
            self.trama = cursor.fetchall()   # Traer los resultados de un select
        else:
            connection.commit()              # Hacer efectiva la escritura de datos
            self.trama = None
        cursor.close()                 # Cerrar el cursor
        connection.close()                   # Cerrar la conexion

        #return self.trama
    def get_variables(self):
        if self.cumulative == False:
            if (self.source_info == 'SIATA'):
                fecha_ppt  = np.array([])
                value_ppt1 = np.array([])
                value_ppt2 = np.array([])
                calidad    = np.array([])

                for element_trama in self.trama:
                    try:
                        aux_fecha  = dt.datetime.strptime(element_trama[0], '%Y-%m-%d %H:%M:%S')
                        fecha_ppt  = np.append(fecha_ppt, aux_fecha)
                        value_ppt1 = np.append(value_ppt1,element_trama[1])
                        value_ppt2 = np.append(value_ppt2,element_trama[2])
                        calidad    = np.append(calidad, element_trama[3])
                    except:
                        pass
                fecha_ppt = np.array(map(lambda x: x.replace(second = 0), fecha_ppt))
                value_ppt1[value_ppt1 >= 1000.0] = np.nan
                value_ppt2[value_ppt2 >= 1000.0] = np.nan
                # Se establece la resolucion para el calculo de la intensidad.
                self.aux_res = np.array(map(lambda x,y : (x - y), fecha_ppt[1:], fecha_ppt[0:-1]))
                self.res_ppt = np.median(np.array(map(lambda y : y.seconds, self.aux_res)))/60.0

                if self.res_ppt == 1.0:
                    self.ppt_rate1 = value_ppt1*60.0
                    self.ppt_rate2 = value_ppt2*60.0
                    fecha_completa = pd.date_range(fecha_ppt[0],fecha_ppt[-1],freq="1min")
                if self.res_ppt == 5.0:
                    self.ppt_rate1 = value_ppt1*12.0
                    self.ppt_rate2 = value_ppt2*12.0
                    fecha_completa = pd.date_range(fecha_ppt[0],fecha_ppt[-1],freq="5min")

                self.df_aux = pd.DataFrame({'ppt_acum1':value_ppt1, 'ppt_acum2':value_ppt2, 'ppt_int1': self.ppt_rate1, 'ppt_int2': self.ppt_rate2, 'calidad':calidad}, index = fecha_ppt)
                grouped = self.df_aux.groupby(level=0)
                self.est_df = grouped.last()
                self.est_df.reindex(index = fecha_completa)

            if (self.source_info == 'SIATA_Vaisala' or self.source_info == 'SIATA_Thiess' ):
                fecha_ppt = np.array([])
                value_ppt = np.array([])
                calidad   = np.array([])
                for element_trama in self.trama:
                    try:
                        aux_fecha = dt.datetime.strptime(element_trama[0], '%Y-%m-%d %H:%M:%S')
                        fecha_ppt = np.append(fecha_ppt, aux_fecha)
                        value_ppt = np.append(value_ppt,element_trama[1])
                        calidad   = np.append(calidad,element_trama[2])
                    except:
                        pass

                fecha_ppt = np.array(map(lambda x: x.replace(second = 0), fecha_ppt))
                value_ppt[value_ppt >= 1000.0] = np.nan
                # Se establece la resolucion para el calculo de la intensidad.
                self.aux_res = np.array(map(lambda x,y : (x - y), fecha_ppt[1:], fecha_ppt[0:-1]))
                self.res_ppt = np.median(np.array(map(lambda y : y.seconds, self.aux_res)))/60.0

                if self.res_ppt == 1.0:
                    self.ppt_rate = value_ppt*60.0
                    fecha_completa = pd.date_range(fecha_ppt[0],fecha_ppt[-1],freq="1min")
                if self.res_ppt == 5.0:
                    self.ppt_rate  = value_ppt*12.0
                    fecha_completa = pd.date_range(fecha_ppt[0],fecha_ppt[-1],freq="5min")

                self.df_aux = pd.DataFrame({'ppt_acum':value_ppt, 'ppt_int': self.ppt_rate, 'calidad': calidad}, index = fecha_ppt)
                grouped = self.df_aux.groupby(level=0)
                self.est_df = grouped.last()
                self.est_df.reindex(index = fecha_completa)

            if (self.source_info == 'SIATA_Tramas'):
                fecha_ppt = np.array([])
                value_ppt = np.array([])
                calidad   = np.array([])
                for element_trama in self.trama:
                    try:
                        aux_fecha = dt.datetime.strptime(element_trama[0], '%Y-%m-%d %H:%M:%S')
                        fecha_ppt = np.append(fecha_ppt, aux_fecha)
                        value_ppt = np.append(value_ppt,element_trama[1])
                        calidad   = np.append(calidad, element_trama[2])
                    except:
                        pass
                fecha_ppt = np.array(map(lambda x: x.replace(second = 0), fecha_ppt))
                value_ppt[value_ppt >= 1000.0] = np.nan
                # Se establece la resolucion para el calculo de la intensidad.
                self.aux_res = np.array(map(lambda x,y : (x - y), fecha_ppt[1:], fecha_ppt[0:-1]))
                self.res_ppt = np.median(np.array(map(lambda y : y.seconds, self.aux_res)))/60.0

                if self.res_ppt == 1.0:
                    self.ppt_rate = value_ppt*60.0
                    fecha_completa = pd.date_range(fecha_ppt[0],fecha_ppt[-1],freq="1min")
                if self.res_ppt == 5.0:
                    self.ppt_rate  = value_ppt*12.0
                    fecha_completa = pd.date_range(fecha_ppt[0],fecha_ppt[-1],freq="5min")

                self.df_aux = pd.DataFrame({'ppt_acum':value_ppt, 'ppt_int': self.ppt_rate,'calidad':calidad}, index = fecha_ppt)
                grouped = self.df_aux.groupby(level=0)
                self.est_df = grouped.last()
                self.est_df.reindex(index = fecha_completa)

            if (self.source_info == 'EPM'):

                fecha_ppt = np.array(map(lambda x: x[0], self.trama))
                fecha_ppt = np.array(map(lambda x: x.replace(second = 0), fecha_ppt))
                value_ppt = np.array(map(lambda x: x[1], self.trama))
                value_ppt[value_ppt >= 1000.0] = np.nan
                self.aux_res = np.array(map(lambda x,y : (x - y), fecha_ppt[1:], fecha_ppt[0:-1]))
                self.res_ppt = np.median(np.array(map(lambda y : y.seconds, self.aux_res)))/60.0
                print self.res_ppt

                if self.res_ppt == 15.0:
                    self.ppt_rate = value_ppt*4.0
                if self.res_ppt == 10.0:
                    self.ppt_rate = value_ppt*6.0
                if self.res_ppt == 5.0:
                    self.ppt_rate = value_ppt*12.0

                self.df_aux = pd.DataFrame({'ppt_acum':value_ppt, 'ppt_int': self.ppt_rate}, index = fecha_ppt)
                grouped = self.df_aux.groupby(level=0)
                self.est_df = grouped.last()

            return self.est_df
        else:
            return self.trama[0][1:]

#consulta de acumulados

host   = "192.168.1.74"
user   = "siata_Oper"
passwd = "si@t@64512_operacional"
dbname = "siata"

columnas=['Cliente','Nombre','Red','Latitude','Longitude']

# fecha1toda='2017-01-29 12:00:00'
fecha1=fecha1toda.split(' ')[0]
# fecha2toda='2018-01-04 12:00:00'
fecha2=fecha1toda.split(' ')[0]

query ="select codigo,nombreestacion, red, latitude,longitude from estaciones where Ciudad in ('Barbosa','Bello','Medellin','Copacabana','Sabaneta','Envigado','Caldas','Girardota','Itagui','La Estrella', 'Guarne', 'Rionegro') and red in ('pluviografica','meteorologica_thiess', 'meteorologica')  and estado='A';"
print query

conn_db = MySQLdb.connect (host, user, passwd, dbname)
db_cursor = conn_db.cursor ()
db_cursor.execute (query)
data = db_cursor.fetchall ()

# #Construimos DataFrame
Estaciones = pd.DataFrame(np.array(data),columns=columnas)

# #Importante --- SIEMPRE Cerrar
conn_db.close ()

Estaciones.Cliente=Estaciones.Cliente.values.astype(int)


Acum =pd.DataFrame(columns=['Cliente', 'Acumulado'])

for i in range(Estaciones.shape[0]):
# for i in range(3):

    if Estaciones.Red[i] == 'pluviografica':
        source_str = 'SIATA'
    if Estaciones.Red[i] == 'meteorologica':
        source_str = 'SIATA_Vaisala'
    if Estaciones.Red[i] == 'meteorologica_thiess':
        source_str = 'SIATA_Thiess'

    mysql_ppt = consulta_mysql(source_str)
    mysql_ppt.cumulative = True
    trama = mysql_ppt.make_query(fecha1toda, fecha2toda, str(Estaciones.Cliente[i]))
    est_data = mysql_ppt.get_variables()

    Acum = Acum.append({'Cliente' :Estaciones.Cliente[i], 'Acumulado' :np.max(est_data)},ignore_index=True)




df=pd.merge(Acum,Estaciones,how='outer',on='Cliente')


#Creacion del mapa
fig=plt.figure()
DataSet = gdal.Open(Path+'DemAM.tif')
GeoTransform = DataSet.GetGeoTransform()
xOrigin = GeoTransform[0]
yOrigin = GeoTransform[3]
pixelWidth = GeoTransform[1]
pixelHeight = GeoTransform[5]
longitudes=np.array([GeoTransform[0]+0.5*GeoTransform[1]+i*GeoTransform[1] for i in range(DataSet.RasterXSize)])
latitudes=np.array([GeoTransform[3]+0.5*GeoTransform[-1]+i*GeoTransform[-1] for i in range(DataSet.RasterYSize)])
DEM=DataSet.ReadAsArray()
DEM=DEM.astype(float)
DEM[DEM==65535]= np.nan
m=basemap.Basemap(llcrnrlat=np.min(latitudes),llcrnrlon=np.min(longitudes),urcrnrlat=np.max(latitudes),urcrnrlon=np.max(longitudes),resolution='l')
r=m.readshapefile(shapefile=Path+'AMVA/AreaMetropolitana',name='AMVA',color='k')
X,Y= np.meshgrid(longitudes,latitudes)
Xm,Ym= m(X,Y)
cs=m.contourf(Xm,Ym,DEM,levels=np.linspace(1300,3401,101),cmap='Greys')

m.drawcoastlines()
# draw parallels
parallels = np.arange(np.min(latitudes).round(1),np.max(latitudes).round(1)+.15,.15)
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10,linewidth=0.1,fontproperties=AvenirBook)
# draw meridians
meridians = np.arange(np.min(longitudes).round(1)+360,np.max(longitudes).round(1)+360+.15,.15)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10,linewidth=0.1,fontproperties=AvenirBook)



bar_colors=[(255, 255, 255),(0, 255, 255), (0, 0, 255),(70, 220, 45),(44, 141, 29),\
               (255,255,75),(255,142,0),(255,0,0),(128,0,128),(102,0,102),\
                (255, 153, 255)]

lev = np.array([0.,1.,5.,10.,20.,30.,45.,60., 80., 100., 150.])


scale_factor =  ((255-0.)/(lev.max() - lev.min()))
new_Limits = list(np.array(np.round((lev-lev.min())*\
                            scale_factor/255.,3),dtype = float))

Custom_Color = map(lambda x: tuple(ti/255. for ti in x) , bar_colors)

nueva_tupla = [((new_Limits[i]),Custom_Color[i],) for i in range(len(Custom_Color))]
cmap_radar =colors.LinearSegmentedColormap.from_list('RADAR',nueva_tupla)


levels_nuevos = np.linspace(np.min(lev),np.max(lev),255)
norm_new_radar = colors.BoundaryNorm(boundaries=levels_nuevos, ncolors=256)


# precip_colormap = matplotlib.colors.ListedColormap(nws_precip_colors)


lon,lat=m(df.Longitude,df.Latitude)
lon = lon.values.astype(float)
lat = lat.values.astype(float)

ax = fig.add_subplot(111)
#ax.yaxis.set_label_position("right")
ax.yaxis.set_label_coords(1.2,.5)

# plt.ylabel('Acumulado [mm]',fontproperties=AvenirBook)
# levs=[0]
# levs.extend(list(np.linspace(.1,np.max(df.pmax),11,endpoint=True)))
# norm=plt.cm.colors.BoundaryNorm(levs,precip_colormap.N)

# m.scatter(lon,lat,s=13,c=df.pmax,cmap=precip_colormap,norm=norm)
m.scatter(lon,lat,s=13,c=df.Acumulado,cmap=cmap_radar,norm=norm_new_radar, linewidth=0.2)
# cbar= m.colorbar(ticks=np.array(levs).round(1))
cbar= m.colorbar(ticks=np.delete(lev,1))
# cbar.ax.set_yticklabels(np.delete(lev,1).astype(int).astype(str))
cbar.set_label('Acumulado [mm]',fontproperties=AvenirBook)

plt.title(u'Acumulado semanal de la red pluviométrica', fontproperties=AvenirBook)
plt.savefig(Path_informe+'Pluviometros.png',dpi=300,bbox_inches='tight')
print "Hello world"
