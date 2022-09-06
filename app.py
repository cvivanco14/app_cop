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

dir_main = "/app/app_cop/"

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

#Title
titulo="Game's report draft"

#Report sections
sec01="**1. CDF de entrevista**"
sec02="**2. Entrevistas completadas**"
sec03=""


# Usuarios
d = {'user': ["admin","inspector","fleet1","fleet2","fleet3"], 'pass': ["Admin2022","GOT2020","Arya2022","Sansa2021","Daenerys2020"]}
df_users = pd.DataFrame(data=d)

###############################################################################
#1. User   login                                                              #
###############################################################################
# Título
image = Image.open(os.path.join(dir_main+"photo.jpg"))
st.sidebar.image(image, channels="BGR")
    
st.sidebar.title("Login")

user = st.sidebar.text_input("Username", value='', max_chars=None, key=None, type='default')

passw = st.sidebar.text_input("Password", value='', max_chars=None, key=None, type='password')


try:
  log0 =   df_users.loc[df_users['user']==user,['pass']]==passw
  log = log0.iloc[0,0]
except:
  pass

if len(log0)!=1:
  log= False

if log == False and user!="" and passw!="":
  st.sidebar.error('User or password incorrect')
if log == True:
  st.sidebar.success('Hi {u}, you enter succesfully!'.format(u=user))
  
  st.sidebar.markdown('''
              <hr style="border:1.75px solid black"> </hr>
              ''', unsafe_allow_html=True)

  ###############################################################################
  #2. Sección a seleccionar                                                     #
  ###############################################################################
  section= ["Day 1", "Day 2", 'Day 3','Day 4','Day 5','Day 6','Day 7','Day 8','Day 9','Day 10']
  subsection1=["i. Type-in information", "ii. Overall Reports"]

  st.sidebar.title("Section selection")
  st.sidebar.markdown('''Select the day and section you wish to see.''')

  #Selection of daily report 
  pag_input = st.sidebar.selectbox('Select day:', section)
  #Selection of section in the daily report
  subsection_input = st.sidebar.selectbox('Select report:', subsection1)
