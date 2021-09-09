#!/usr/bin/env python
# coding: utf-8

# # import all required library
# 

# In[1]:


import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import math
import random
from datetime import timedelta
import warnings
warnings.filterwarnings('ignore')
import folium


# # Introducing colour pallet

# In[2]:


cnf='#393e46'
dth='#ff2e63'
rec='#21bf73'
act='#fe9801'


# # Dataset preparation
# 

# In[3]:



import plotly as py
py.offline.init_notebook_mode(connected=True)


# In[4]:


import os


# In[5]:



try:
    os.system("rm -rf Covid-19-preprocessed-Datasheet")
except:
        print('File does not exit')


# In[6]:


get_ipython().system('git clone https://github.com/laxmimerit/Covid-19-Preprocessed-Dataset.git')


# In[7]:


df=pd.read_csv('Covid-19-Preprocessed-Dataset/preprocessed/covid_19_data_cleaned.csv',parse_dates=['Date'])
df["Province/State"]=""


# In[8]:


df.head()


# In[9]:


country_wise_data=pd.read_csv('Covid-19-Preprocessed-Dataset/preprocessed/countrywise.csv')


# In[10]:


country_wise_data.head()


# In[11]:


daywise_data=pd.read_csv('Covid-19-Preprocessed-Dataset/preprocessed/daywise.csv')


# In[12]:


daywise_data.head()


# In[13]:


country_day_wise_data=pd.read_csv('Covid-19-Preprocessed-Dataset/preprocessed/country_daywise.csv')


# In[14]:


country_day_wise_data.head()


# In[15]:


country_day_wise_data.isnull().sum().sum()


# In[16]:


Noof_confirmed=df.groupby('Date').sum()['Confirmed'].reset_index()
Noof_deaths=df.groupby('Date').sum()['Deaths'].reset_index()
Noof_recovered=df.groupby('Date').sum()['Recovered'].reset_index()
Noof_active=df.groupby('Date').sum()['Active'].reset_index()


# In[17]:


df.query('Country == "usa"')


# # Worldwide total confirmed,deaths,recovered and active cases

# In[18]:


Noof_confirmed.tail()   #Latest noof confirmed cases


# In[19]:


Noof_deaths.tail()    #lateast noof deaths


# In[20]:


fig=go.Figure()
fig.add_trace(go.Scatter(x=Noof_deaths['Date'],y=Noof_deaths['Deaths'],mode='lines+markers',name='Deaths',line=dict(color="Red",width=2)))
fig.add_trace(go.Scatter(x=Noof_active['Date'],y=Noof_active['Active'],mode='lines+markers',name='active cases',line=dict(color="orange",width=2)))
fig.add_trace(go.Scatter(x=Noof_recovered['Date'],y=Noof_recovered['Recovered'],mode='lines+markers',name='Recovered',line=dict(color="Green",width=2)))
fig.update_layout(title='Worldwide covid-19 Data',xaxis_tickfont_size=14, yaxis=dict(title='Number of cases'))
fig.show()    


# # Cases animation on world map

# In[21]:


df.head()


# In[22]:


df['Date']=df['Date'].astype(str)


# In[23]:


df.info()


# In[24]:


df.head()


# In[25]:



fig=px.density_mapbox(df,lat='Lat',lon='Long',hover_name='Country',hover_data=['Confirmed','Recovered','Deaths','Active'],animation_frame='Date',color_continuous_scale='Portland',radius=7,zoom=0,height=700)
fig.update_layout(title='World wide covid-19')
fig.update_layout(mapbox_style='open-street-map',mapbox_center_lon=0)
fig.show()


# # Total cases on ships
# 

# In[26]:


df['Date']=pd.to_datetime(df['Date'])


# In[27]:


ships_rows=df['Country'].str.contains('Grand princes') |df['Country'].str.contains('Diamond princes')|df['Country'].str.contains('MS Zaandam princes')
ship=df[ships_rows]
df=df[~ships_rows]


# In[28]:


ship_latest=ship[ship['Date'] == max(ship['Date'],default=0)]
ship_latest


# In[29]:


ship_latest.style.background_gradient(cmap='Pastell_r')


# # Cases over the time area plot
# 

# In[30]:


temp=df.groupby('Date')['Confirmed','Deaths','Recovered','Active'].sum().reset_index()
temp=temp[temp['Date'] == max(temp['Date'])].reset_index(drop=True)
temp


# In[31]:


temp=df.groupby('Date')['Recovered','Active','Deaths'].sum().reset_index()
temp=temp.melt(id_vars='Date',value_vars=['Recovered','Deaths','Active'],var_name='Case',value_name='Count')
fig=px.area(temp,x='Date', y='Count',color='Case', height=600,title='Cases over time',color_discrete_sequence=[rec,dth,act])
fig.update_layout(xaxis_rangeslider_visible=True)
fig.show()


# # Represent with follium on world map

# In[32]:


temp=df[df['Date']==max(df['Date'])]
m=folium.Map(location=[0,0],tiles='cartodbpositron',min_zoom=1,max_zoom=4,zoom_start=1)
for i in range(0,len(temp)):
    folium.Circle(location=[temp.iloc[i]['Lat'],temp.iloc[i]['Long']],color='crimson',fill='crimson',
                 tooltip='<li>Country:' + str(temp.iloc[i]['Country'])+ '<li>Province:' + str(temp.iloc[i]['Province/State'])+
                  '<li>Confirmed:' + str(temp.iloc[i]['Confirmed'])+ '<li>Active:' + str(temp.iloc[i]['Active'])+

                  '<li>Deaths:' + str(temp.iloc[i]['Deaths']), radius=int(temp.iloc[i]['Confirmed'])**0.7).add_to(m)
    
m


# # Analyze data by country wise
# 

# In[33]:


country_wise_data.head()


# In[34]:


country_wise_data['Confirmed'].head()


# In[35]:


temp=df.groupby('Date')['Confirmed','Deaths','Active'].sum().reset_index


# In[36]:


temp


# In[ ]:




