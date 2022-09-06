# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 17:48:54 2022

@author: camiv
"""

import os
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np
#import streamlit
import streamlit as st
import base64
import pytz
import datetime
from PIL import Image
import openpyxl
from openpyxl import load_workbook
from openpyxl.styles import Alignment
from openpyxl.styles import Font
from openpyxl.styles import PatternFill
from openpyxl.styles.borders import Border, Side
from openpyxl.workbook import Workbook
import string
from openpyxl.styles import Border, Side, PatternFill
import fun

#dir_main = "C:\\Users\\Camila\\Documents\\Ploty\\"
dir_main =  "/root/CMD/AppCami/"
dir_data =  "/root/CMD/ECBS/Reportes/"
dir_data2 =  "/root/CMD/ECBS/data/"



###############################################################################
#0. Inputs                                                                    #
###############################################################################


x_input = ""
y_input = ""
f1_input = ""
f2_input = ""

#Variables relevantes
#variables=['cdf', 'timestamp',"responsable_act","comuna_enc","region"] 
variables=["folio",'cdf', 'timestamp',"responsable","Región", "Comuna",'Zona'] 

#Variables selección base de datos 
input_01=["Responsable", "Región",'Comuna','Zona']  #Reporte 1 
input_02=["Responsable", "Región",'Comuna','Zona']  #Reporte 2


#Input de categorias
old_cat = ["responsable"]
new_cat = ["Responsable"]

#Título pagina 
titulo="Reportes Encuesta Complementaria de Bienestar Social"

#Secciones reporte
sec01="**1. CDF de entrevista**"
sec02="**2. Entrevistas completadas**"
sec03=""


# Usuarios
d = {'user': ["admin","MDSF"], 'pass': ["Microdatos2020","MDSF2021"]}
df_users = pd.DataFrame(data=d)

@st.cache(ttl=60*60, max_entries=20, suppress_st_warning=True,allow_output_mutation=True)
def load_data(dir_data,variables):
    data = pd.read_excel(os.path.join(dir_data+"Seguimiento2.xlsx"))
    data = data.loc[ : ,variables]
    data.loc[data['cdf'].isna(),'cdf']="520"

      #Fecha
    tz = pytz.timezone('Chile/Continental')
    ahora = datetime.datetime.now(tz)

    if ahora.month<10:
     m = "0"+str(ahora.month)
    if ahora.month>=10:
     m = str(ahora.month)
     date = str(ahora.year) + m + str(ahora.day)
    if ahora.day<10:
      date2 = str(ahora.year) + str("-")+m +  str("-0")+str(ahora.day)
    if ahora.day>=10:
      date2 = str(ahora.year) + str("-")+m +  str("-")+str(ahora.day)

  #Formato fecha
    data['Fecha'] = data['timestamp']
    data.loc[data['Fecha'].isna(),'Fecha']=date2
    data['Fecha'] = pd.to_datetime(data['Fecha'])
    data['Fecha'] = data['Fecha'].dt.strftime('%d-%b-%Y')
    data['cdf']=data['cdf'].astype(int)
    data['cdf']=data['cdf'].astype(str)
    data['cdf']=data['cdf']
    del data['timestamp']

    return data

@st.cache(ttl=60*60, max_entries=20, suppress_st_warning=True,allow_output_mutation=True)
def load_bitacora(dir_data):
    data = pd.read_stata(os.path.join(dir_data+"Bitacora/Bitacora.dta"), convert_categoricals=False)
    data=data.loc[data['folio']!='-1',:]
    return data

@st.cache(ttl=60*60, max_entries=20, suppress_st_warning=True,allow_output_mutation=True)
def load_base(dir_data, dir_data2):
    data = pd.read_stata(os.path.join(dir_data2+"Final_ecbs.dta"),convert_categoricals = False)
    df = pd.read_excel(os.path.join(dir_data+"Seguimiento.xlsx"))
    df=df.loc[:,["responsable","folio", 'dir_casen', 'telefono','edad_casen']]
    data['folio'] = data['folio'].astype(int)
    df['folio'] = df['folio'].astype(int)
    data=pd.merge(data,df,on='folio', how='inner')
    return data


##Definir base Seguimiento 
seguimiento = load_data(dir_data,variables)
df=seguimiento
 
#Renombrar variables
df.rename(columns=dict(zip(old_cat, new_cat)), inplace=True)

#Bitacora
bitacora = load_bitacora(dir_data)

#Definir base final (sin cdf, solo 110)
base = load_base(dir_data,dir_data2)



###############################################################################
#1. Ingreso usuario                                                           #
###############################################################################
# Título
image = Image.open(os.path.join(dir_main+"Imagen2.png"))
st.sidebar.image(image, channels="BGR")
    
st.sidebar.title("Login")

user = st.sidebar.text_input("Ingresar usuario", value='', max_chars=None, key=None, type='default')

passw = st.sidebar.text_input("Ingresar password", value='', max_chars=None, key=None, type='password')


try:
  log0 =   df_users.loc[df_users['user']==user,['pass']]==passw
  log = log0.iloc[0,0]
except:
  pass

if len(log0)!=1:
  log= False

if log == False and user!="" and passw!="":
  st.sidebar.error('Usuario o contraseña incorrectos')
if log == True:
  st.sidebar.success('Hola {u}, te logeaste correctamente!'.format(u=user))
  
  st.sidebar.markdown('''
              <hr style="border:1.75px solid black"> </hr>
              ''', unsafe_allow_html=True)

  ###############################################################################
  #2. Sección a seleccionar                                                     #
  ###############################################################################
  seccion= ["Control y Seguimiento", "Calidad de datos", 'Base de datos EBS','Supervisión interna','Tiempos']
  subseccion1=["i. Hoja de ruta", "ii. Reporte de indicadores"]
  subseccion2=["Evaluación expost críticas", "Indicadores de trabajo de campo", "Indicadores de no respuesta al ítem", "Indicadores de registros sistemáticos", "Control de calidad de datos","Indicadores de trabajo de campo", "Indicadores de registros sistemáticos"] 

  st.sidebar.title("Selección de reporte")
  st.sidebar.markdown('''Seleccione la sección y subsección del reporte que desea analizar.''')

  #Selección página
  pag_input = st.sidebar.selectbox('Seleccionar página:', seccion)
  #Selección valor específico
  if pag_input=="Control y Seguimiento": 
   subseccion_input = st.sidebar.selectbox('Seleccionar reporte:', subseccion1)
