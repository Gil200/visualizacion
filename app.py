import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
## 1º Add a text which explain what we are going to do

## 2º Explore and show the data
df = pd.read_csv("C:/Users/pgila/Downloads/airbnb.csv")


## 3º Create a table with the name of the apartment, neighbourhood_group, neighbourhood, price and reviews_per_month
df_select = df[["name", "neighbourhood_group", "price", "reviews_per_month"]]
st.dataframe(df_select.head(), 
         column_config={
             "name": "Apartment Name", 
             "price": st.column_config.NumberColumn(
                 label="Price ($)", 
                 format="$%.2f"
             ),
             "reviews_per_month": st.column_config.ProgressColumn(
                 label="Notas por mes", 
                 format = "compact"
             )
         })

## 4º Represent the top 10 host with more airbnb hostings
neighbourhood = st.multiselect("Please, select one neighbourhood", 
                               df_select["neighbourhood_group"].unique()
                               )
df_select = df_select[df_select["price"]<1000]
import plotly.express as px
fig = px.box(df_select , x= "neighbourhood_group", y="price")
st.plotly_chart(fig)


