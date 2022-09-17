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
#Title
title="Game's report draft"


# Usuarios
d = {'user': ["admin","inspector","fleet1","fleet2","fleet3"], 'pass': ["Admin2022","GOT2020","Arya2022","Sansa2021","Daenerys2020"]}
df_users = pd.DataFrame(data=d)


#Dataframes
#@st.cache(ttl=60*60, max_entries=20, suppress_st_warning=True,allow_output_mutation=True)
#def load_score(dir_main):
#    df = pd.read_csv(os.path.join(dir_main+"score.csv"), sep=";")
#    return df
    
#df = load_score(dir_main)



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
#A. Fleets                                                                    #
###############################################################################

###############################################################################
#2. Section selection                                                         #
###############################################################################
  section= ["Day 1", "Day 2", 'Day 3','Day 4','Day 5','Day 6','Day 7','Day 8','Day 9','Day 10']
  
  st.sidebar.title("Section selection")
  st.sidebar.markdown('''Select the day and section you wish to see.''')
  
  #Selection of daily report 
  pag_input = st.sidebar.selectbox('Select day:', section)



###############################################################################
#2.i Day 1                                                                    #
###############################################################################
  if pag_input=="Day 1": 
    #Selection of section in the daily report
   # Title
   st.title(title)  
   st.markdown('''
              <hr style="border:1.75px solid black"> </hr>
              ''', unsafe_allow_html=True)
   st.header("**Day 1: Type in information**")
   st.markdown('''In this subsection the fleet manager types in the score and the profit for every action (this is already
accumulated)''')

   with st.expander("Vessel scores"):
#    if "df" not in st.session_state or score.columns[0]=="Unnamed: 0":
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=["Vessel 1: Arya", 
                                                    "Vessel 2: Cersei", 
                                                    "Vessel 3: Lyanna", 
                                                    "Vessel 4: Daenerys"])


    st.markdown("Add Record")
    
    num_new_rows = 10
    ncol = st.session_state.df.shape[1]  # col count
    rw = -1
    
    with st.form(key="add form", clear_on_submit= True):
        cols = st.columns(ncol)
        rwdta = []
    
        for i in range(ncol):
            rwdta.append(cols[i].text_input(st.session_state.df.columns[i]))
    
        # you can insert code for a list comprehension here to change the data (rwdta) 
        # values into integer / float, if required
    
        if st.form_submit_button("Add"):
            if st.session_state.df.shape[0] == num_new_rows:
                st.error("Add row limit reached. Cant add any more records..")
            else:
                rw = st.session_state.df.shape[0] + 1
                st.info(f"Row: {rw} / {num_new_rows} added")
                st.session_state.df.loc[rw] = rwdta
    
                if st.session_state.df.shape[0] == num_new_rows:
                    st.error("Add row limit reached...")
    df = st.session_state.df
    df.to_csv("score1.csv",encoding='utf-8',index=False)
    st.text(df)
    
   with st.expander("Vessel profits"):
    if "df2" not in st.session_state:
        st.session_state.df2 = pd.DataFrame(columns=["Vessel 1: Arya", 
                                                    "Vessel 2: Cersei", 
                                                    "Vessel 3: Lyanna", 
                                                    "Vessel 4: Daenerys"])
    
    st.markdown("Add Record")
    
    ncol = st.session_state.df2.shape[1]  # col count
    rw = -1
    
    with st.form(key="add profits form", clear_on_submit= True):
        cols = st.columns(ncol)
        rwdta = []
    
        for i in range(ncol):
            rwdta.append(cols[i].text_input(st.session_state.df2.columns[i]))
    
        # you can insert code for a list comprehension here to change the data (rwdta) 
        # values into integer / float, if required
    
        if st.form_submit_button("Add"):
            if st.session_state.df2.shape[0] == num_new_rows:
                st.error("Add row limit reached. Cant add any more records..")
            else:
                rw = st.session_state.df2.shape[0] + 1
                st.info(f"Row: {rw} / {num_new_rows} added")
                st.session_state.df2.loc[rw] = rwdta
    
                if st.session_state.df2.shape[0] == num_new_rows:
                    st.error("Add row limit reached...")
    


    df2 = st.session_state.df2
    df2.to_csv("profits1.csv",encoding='utf-8',index=False)

    st.text(st.session_state.df2)
 
   with st.expander("Vessel fines"):
    if "df3" not in st.session_state:
        st.session_state.df3 = pd.DataFrame(columns=["Vessel 1: Arya", 
                                                    "Vessel 2: Cersei", 
                                                    "Vessel 3: Lyanna", 
                                                    "Vessel 4: Daenerys"])
    
    st.markdown("Add Record")
    
    ncol = st.session_state.df3.shape[1]  # col count
    rw = -1
    
    with st.form(key="add fines form", clear_on_submit= True):
        cols = st.columns(ncol)
        rwdta = []
    
        for i in range(ncol):
            rwdta.append(cols[i].text_input(st.session_state.df3.columns[i]))
    
        # you can insert code for a list comprehension here to change the data (rwdta) 
        # values into integer / float, if required
    
        if st.form_submit_button("Add"):
            if st.session_state.df3.shape[0] == num_new_rows:
                st.error("Add row limit reached. Cant add any more records..")
            else:
                rw = st.session_state.df3.shape[0] + 1
                st.info(f"Row: {rw} / {num_new_rows} added")
                st.session_state.df3.loc[rw] = rwdta
    
                if st.session_state.df3.shape[0] == num_new_rows:
                    st.error("Add row limit reached...")
    

    df3 = st.session_state.df3
    df3.to_csv("fines1.csv",encoding='utf-8',index=False)

    st.text(st.session_state.df3)

###############################################################################
#2.i Overall reports                                                          #
###############################################################################
   st.markdown('''
              <hr style="border:1.75px solid black"> </hr>
              ''', unsafe_allow_html=True)
   if st.button('Create overall reports'): 
    st.header("**Day 1: Overall reports**")
    st.markdown('''In this subsection the fleet manager can see the current accumulted score and profit of day 1 and the daily fleet scores and profits.''')
    st.markdown('''
              <hr style="border:1.75px solid black"> </hr>
              ''', unsafe_allow_html=True)
    #
    df = pd.read_csv(os.path.join(dir_main,'score1.csv'), sep=',')
    df2 = pd.read_csv(os.path.join(dir_main,'profits1.csv'), sep=',')
    df3 = pd.read_csv(os.path.join(dir_main,'fines1.csv'), sep=',')
    d = {'Vessel': df.columns[0:4] , 'Score':  df.iloc[-1] , 'Accumulated Profit':df2.iloc[-1] ,'Fines':df3.iloc[-1] }
    #d = pd.DataFrame()
    #d['Vessel']= df.columns[0:4]
    #d['CDF'] = df.values[::-1]
    #d['Score'] = df.iloc[-1] 
    #d['Accumulated Profit'] = df2.iloc[-1] 
    #['Fines'] = df3.iloc[-1] 
    outcomes = pd.DataFrame(data=d)
    outcomes=outcomes.reset_index(drop=True)
    st.dataframe(outcomes)
    #st.dataframe(d)
    
    #Plot scores 
    df01 = pd.read_csv(os.path.join(dir_main,'score1.csv'), sep=',')
    #Create the daily average 
    df01['Fleet score']=df01.sum(axis=1)/4
    df01['Action'] = df01.index
    df01 = pd.melt(df01, id_vars='Action', value_vars=["Vessel 1: Arya", 
                                                    "Vessel 2: Cersei", 
                                                    "Vessel 3: Lyanna", 
                                                    "Vessel 4: Daenerys", 
                                                    "Fleet score"])
    st.write(df01)
    st.subheader("*Daily fleet and vessel scores*")
    fig01 = px.line(df01, x='Action', y='value', color='variable', markers=True,range_x=[0,10],width=650,height=650)
    fig01.update_layout(yaxis_type='category')
    fig01.layout.xaxis.fixedrange= True
    fig01.layout.yaxis.fixedrange: True
    fig01.update(layout_showlegend=True)
    st.plotly_chart(fig01)
  
    #Plot profits  
    df02 = pd.read_csv(os.path.join(dir_main,'profits1.csv'), sep=',')
    df02['Fleet profit']=df02.sum(axis=1)
    df02['Action'] = df02.index
    df02['Fleet score'] = df01.loc[df01.variable=="Fleet score",'value']
    st.write(df02)
#    df02['Profit w. score'] = 
    df02 = pd.melt(df02, id_vars='Action', value_vars=["Fleet profit",
                                                       "Fleet score"])
    st.write(df02)
    
  #reset index from 1-10 
  
