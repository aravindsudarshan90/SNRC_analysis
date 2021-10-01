import streamlit as st
from PIL import Image
import pandas as pd
import base64,math
import matplotlib.pyplot as plt
from datetime import date
from pymongo import MongoClient
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import requests, json
from lxml import html
import numpy as np

# mongo = MongoClient('mongodb+srv://aravind:aravind@cluster0-9tkxn.mongodb.net/test?retryWrites=true')
# db  = mongo.Lead_Tracking
# leads = db.Leads
@st.cache
def check(lead,conv,month,year):
    if month == '':
        leads = lead.groupby(['added_year','interested_in']).size().to_frame('size').reset_index(level=['added_year','interested_in'])
        leads = leads[leads['added_year'] == year]
        conversions = conv.groupby(['completed_year','enrolled']).size().to_frame('size').reset_index(level=[ 'completed_year','enrolled'])
        conversions = conversions[conversions['completed_year'] == year]
    else:
        leads = lead.groupby(['added_month','added_year','interested_in']).size().to_frame('size').reset_index(level=['added_month','added_year','interested_in'])
        leads = leads[(leads['added_year'] == year) & (leads['added_month'] == month)]
        conversions = conv.groupby(['completed_month','completed_year','enrolled']).size().to_frame('size').reset_index(level=['completed_month','completed_year','enrolled'])
        conversions = conversions[(conversions['completed_year'] == year) & (conversions['completed_month'] == month) ]      
    return leads,conversions

    # if category == 'Leads':
    #     if a['completed'] == '0':
    #         temp = a.groupby(['added_month','added_year','interested_in']).size().to_frame('size').reset_index(level=['added_month', 'added_year','interested_in'])
    #         temp = temp[temp['added_month'] == month]

    # elif category == 'Conversions':
    #     if a['completed'] == '1':
    #         return 1
    #     return 0
@st.cache
def check_month_year(df,month,year):
   
    if month != 'Jan':
        temp = df.groupby(['added_month','added_year','interested_in']).size().to_frame('size').reset_index(level=['added_month', 'added_year','interested_in'])
        temp = temp[temp['added_month'] == month]
        return temp
    elif month == 'Jan':
        temp = df.groupby(['added_year','interested_in']).size().to_frame('size').reset_index(level=['added_year','interested_in'])
        temp = temp[temp['added_year'] == year]
        return temp   
st.title("SNRC Leads")
d = {}
st.sidebar.write("SIDEBAR")
category = st.sidebar.selectbox("Category",['Leads','Conversions'])
year = st.sidebar.selectbox("Year",['2021','2020'])
if year in ['2021','2020']:
    month = st.sidebar.selectbox("Month",['','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
else:
    month = st.sidebar.selectbox("Month",['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
# f = open('data.json', "r")
# print(f.read())
js = {}
f = open('Leads.json', "r")
a = json.loads(f.read())
for x in a:    
    del x['_id']
    del x['Comments']
    add_details = x['added_on'].split('-')
    if x['completed'] == '1':
        comp_details = x['date_of_completion'].split('-')
        x['completed_month'] = comp_details[1]
        x['completed_year'] = comp_details[2].split(' ')[0]
        x['added_month'] = add_details[1]
        x['added_year'] = add_details[2].split(' ')[0]
    if x['completed'] == '0':
        x['completed_month'] = ''
        x['completed_year'] = ''
        x['added_month'] = add_details[1]
        x['added_year'] = add_details[2].split(' ')[0]

new_df = pd.DataFrame()
for x in a:
    new_df = new_df.append(x,ignore_index=True)

# NEW DF READY#

# col1,col2  = st.columns(2)

leads = new_df[new_df['completed'] == '0']
conv = new_df[new_df['completed'] == '1']
lead_df,conv_df = check(leads,conv,month,year)
st.subheader("Leads"+' '+ year+' ' +month)
fig_1 = go.Figure(data=[go.Bar(name='Level',x = lead_df['interested_in'], y = lead_df['size'])])
st.plotly_chart(fig_1)
st.subheader("Conversions"+' '+ year+' ' +month)
fig_2 = go.Figure(data=[go.Bar(name='Level',x = conv_df['enrolled'], y = conv_df['size'])])   
st.plotly_chart(fig_2)
# st.write(recd_df[['size','interested_in']])
# print(recd_df.columns)
# recd_df = recd_df[['size','interested_in']]
# fig = go.Figure(data=[go.Bar(name='Level',x = recd_df['interested_in'], y = recd_df['size'])])
# # st.bar_chart(recd_df[['size','interested_in']])
# with col2:
#     st.plotly_chart(fig)
# # st.write(abc.groupby(['added_month','added_year','interested_in']).size().reset_index())
# new = pd.DataFrame(columns=['levels','count','month','year'])
# new['levels'] = ['N5','N4','N3','N2']

# st.write(new)
# fig = go.Figure(data=[
#         go.Bar(name='N5', x='N5', y=len(new_df[new_df['interested_in'] == 'N5']))])
# st.plotly_chart(fig)
# st.bar_chart(pd.DataFrame({'abc':10,'def':20},index = ['values']))




# ,
#         go.Bar(name='N4', x=df['State'][:5], y=df['Recovered'][:5]),
#         go.Bar(name='N3', x=df['State'][:5], y=df['Active'][:5]),
#         go.Bar(name='N2', x=df['State'][:5], y=df['Recovered'][:5]