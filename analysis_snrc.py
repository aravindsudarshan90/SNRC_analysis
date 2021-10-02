import streamlit as st
import pandas as pd
import base64,math
import matplotlib.pyplot as plt
from datetime import date
from pymongo import MongoClient
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import  json

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

st.title("SNRC Leads")
st.sidebar.write("SIDEBAR")
category = st.sidebar.selectbox("Category",['Leads','Conversions'])
year = st.sidebar.selectbox("Year",['2021','2020'])
if year in ['2021','2020']:
    month = st.sidebar.selectbox("Month",['','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
else:
    month = st.sidebar.selectbox("Month",['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
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

leads = new_df[new_df['completed'] == '0']
conv = new_df[new_df['completed'] == '1']
lead_df,conv_df = check(leads,conv,month,year)
st.subheader("Leads"+' '+ year+' ' +month)
fig_1 = go.Figure(data=[go.Bar(name='Level',x = lead_df['interested_in'], y = lead_df['size'])])
st.plotly_chart(fig_1)
st.subheader("Conversions"+' '+ year+' ' +month)
fig_2 = go.Figure(data=[go.Bar(name='Level',x = conv_df['enrolled'], y = conv_df['size'])])   
st.plotly_chart(fig_2)