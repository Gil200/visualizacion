import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos
st.title("Nombre del Estudiante")

@st.cache_data
def load_data():
    df = pd.read_csv("/mnt/data/airbnb.csv")
    df = df.rename(columns={"room_type": "listing_type", "neighbourhood": "neighborhood"})
    df.dropna(subset=["price"], inplace=True)  # Eliminar filas sin precio
    return df

df = load_data()

# Sidebar
st.sidebar.header("Filtros")
listing_types = st.sidebar.multiselect("Selecciona tipos de listado", df["listing_type"].unique(), default=df["listing_type"].unique())
neighborhoods = st.sidebar.multiselect("Selecciona barrios", df["neighborhood"].unique(), default=df["neighborhood"].unique())
filtered_df = df[(df["listing_type"].isin(listing_types)) & (df["neighborhood"].isin(neighborhoods))]

# Tabs
tab1, tab2 = st.tabs(["Análisis", "Simulador"])

# Tab de Análisis
with tab1:
    col1, col2 = st.columns(2)
    
    # Gráfico 1: Relación entre tipo de listado y número de personas
    with col1:
        fig1 = px.box(filtered_df, x="listing_type", y="minimum_nights", title="Número de noches mínimas por tipo de listado")
        st.plotly_chart(fig1)
    
    # Gráfico 2: Precio por tipo de listado
    with col2:
        fig2 = px.box(filtered_df, x="listing_type", y="price", title="Precio por tipo de listado")
        st.plotly_chart(fig2)
    
    # Gráfico 3: Apartamentos con más reviews por mes por barrio
    top_reviews = filtered_df.groupby(["neighborhood", "listing_type"]).agg({"reviews_per_month": "sum"}).reset_index()
    fig3 = px.bar(top_reviews, x="neighborhood", y="reviews_per_month", color="listing_type", title="Apartamentos con más reviews por mes por barrio")
    st.plotly_chart(fig3)

# Tab de Simulador
with tab2:
    st.header("Simulador de Precio")
    selected_neighborhood = st.selectbox("Selecciona un barrio", df["neighborhood"].unique())
    selected_type = st.selectbox("Selecciona tipo de listado", df["listing_type"].unique())
    num_nights = st.slider("Número de noches", 1, 30, 2)
    
    # Filtrar datos similares
    similar_listings = df[(df["neighborhood"] == selected_neighborhood) & (df["listing_type"] == selected_type) & (df["minimum_nights"] >= num_nights)]
    price_range = (similar_listings["price"].quantile(0.25), similar_listings["price"].quantile(0.75))
    
    st.write(f"Rango de precio recomendado: ${price_range[0]:.2f} - ${price_range[1]:.2f}")

# Instrucciones finales
st.sidebar.markdown("## Instrucciones")
st.sidebar.info("Sube este código a Streamlit Cloud y entrega el enlace en Moodle.")
