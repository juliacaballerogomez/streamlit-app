import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Here we are going to build the dashboard")

df = pd.read_csv("airbnb.csv")

neighbourhood_group = st.sidebar.multiselect("Select one neighbourhood",df["neighbourhood_group"].unique())
neighbourhood = st.sidebar.multiselect("Select one or multi neighbourhood",df["neighbourhood"].unique())
room_type = st.sidebar.multiselect("Select one or multi room_type",df["room_type"].unique())

df_filtered = df[
                (df["neighbourhood_group"].isin(neighbourhood_group))&
                (df["neighbourhood"].isin(neighbourhood))&
                (df["room_type"].isin(room_type))
                ]



#st.table(df_filtered.head())

col1, col2 = st.columns(2)
with col1:
    st.subheader("Map")
    st.map(df_filtered.dropna(), latitude="latitude", longitude = "longitude")

with col2: 
    st.subheader("Boxplot")
    fig_boxplot_neighbourhood = px.box(df_filtered[df_filtered["price"]<600], x="neighbourhood", y="price")
    st.plotly_chart(fig_boxplot_neighbourhood, key = "Boxplot 2")

df_host = df_filtered.groupby(["host_id","host_name"]).size().reset_index()
df_host["host"] = df_host["host_id"].astype(str) +"---" + df_host["host_name"]
df_top10_host = df_host.sort_values(by=0, ascending = False).head(10)
fig = px.bar(df_top10_host, x=0, y="host", orientation='h', hover_name = "host_name")
st.subheader("Top 10 Host")
st.plotly_chart(fig)