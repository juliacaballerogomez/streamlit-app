import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")


## 1º Add a text which explain what we are going to do
st.title("Airbnb Analysis")
st.markdown("We are going to analyze a dataset from *Airbnb* in :blue[Madrid]")

## 2º Explore and show the data
df = pd.read_csv("airbnb.csv")
#st.table(df.head())
#st.dataframe(df.head())

## 3º Create a table with the name of the apartment, neighbourhood_group, neighbourhood, price and reviews_per_month
df_sel = df[["name","neighbourhood_group", "neighbourhood", "price", "reviews_per_month"]]
#st.table(df_sel.head())
############## https://docs.streamlit.io/develop/api-reference/data/st.column_config
st.dataframe(
    df_sel.head(),
    column_config={
                    "name":"Airbnb Name",
                    "neighbourhood_group":"Area",
                    "neighbourhood":"Neighbourhood",
                    "price":st.column_config.NumberColumn(
                        label = "Price (€)",
                        width = "medium",
                        format = "€%.1f"),
                    "reviews_per_month": st.column_config.ProgressColumn(
                        label = "Reviews per Month",
                        width = "medium",
                        format = "compact"),
                },
    hide_index=True)

## 4º Represent the top 10 host with more airbnb hostings
#st.dataframe(df.head())
df_host = df.groupby(["host_id","host_name"]).size().reset_index()
df_host["host"] = df_host["host_id"].astype(str) +"---" + df_host["host_name"]
df_host
df_top10_host = df_host.sort_values(by=0, ascending = False).head(10)
st.dataframe(df_top10_host)

## 5º Instead of table, do it in a plotly chart, in the hover include the price
## pip install plotly
import plotly.express as px
fig = px.bar(df_top10_host, x=0, y="host", orientation='h', hover_name = "host_name")
st.subheader("Top 10 Host in Madrid")
st.plotly_chart(fig)


## 6º Instead of Top 10, make it a choice for the user
top = st.radio("How many top host you want to visualize?",[3,5,10,20,50])

df_top_host = df_host.sort_values(by=0, ascending = False).head(top)

fig = px.bar(df_top_host, x=0, y="host", orientation='h', hover_name = "host_name")
st.subheader(f"Top {top} Host in Madrid")
st.plotly_chart(fig, key = f"top {top} host")

## 7º Create a boxplot for the prices for Neighbourhood groups
st.subheader(f"Boxplot per Neighbourhood groups")
#fig2 = px.box(df, x="neighbourhood_group", y="price")
#st.plotly_chart(fig2, key = "Boxplot 1")

## Let create without outliers
fig_boxplot_neighbourhood_group = px.box(df[df["price"]<600], x="neighbourhood_group", y="price")
st.plotly_chart(fig_boxplot_neighbourhood_group, key = "Boxplot 1")

## 8º Create a boxplot for the prices for neighbourhood after selecting one neighbourhood group
st.subheader(f"Boxplot per Neighbourhood")
neighbourhood_group = st.selectbox("Select one neighbourhood",df["neighbourhood_group"].unique())
neighbourhood_group
df_neighbourhood = df[df["neighbourhood_group"]==neighbourhood_group]
fig_boxplot_neighbourhood = px.box(df_neighbourhood[df_neighbourhood["price"]<600], x="neighbourhood", y="price")
st.plotly_chart(fig_boxplot_neighbourhood, key = "Boxplot 2")

## 9º Create a map with all the listings in that neighbourhood
st.subheader(f"Map of listing per neighbourhood")
#df_neighbourhood
st.map(df_neighbourhood.dropna(), latitude="latitude", longitude = "longitude")

st.sidebar.text("HOLA")

## 5º Create a new tab 