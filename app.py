import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from streamlit_option_menu import option_menu
import plotly.express as px
from config import engine

PRIMARY_COLOR = "#F77F00"  
SECONDARY_COLOR = "#003049"  
TEXT_COLOR = "#303030"
BACKGROUND_COLOR = "#F5F5F5"
CARD_BG_COLOR = "#FCBF49"  

st.set_page_config(page_title="BiteBack Dashboard", layout="wide")

with st.sidebar:
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("assets/BiteBackLogoNaranja.png", width=60)
    with col2:
        st.markdown(f'<h1 style="color: {PRIMARY_COLOR};">BiteBack</h1>', unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title="Dashboard",
        options=["Inicio", "Tiempo de Carga", "Restaurantes", "Filtros", "Categorías"],
        icons=["house", "clock", "star", "search", "list"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"background-color": BACKGROUND_COLOR},
            "icon": {"color": SECONDARY_COLOR, "font-size": "20px"},
            "nav-link": {"color": TEXT_COLOR, "font-size": "16px", "text-align": "left"},
            "nav-link-selected": {"background-color": PRIMARY_COLOR, "color": "white"},
        }
    )

@st.cache_data
def get_data(query):
    return pd.read_sql(query, engine)

if selected == "Inicio":
    st.title("BiteBack Analytics")
    st.subheader("Análisis de Datos de la Aplicación")
    st.markdown("Bienvenido al panel de control de BiteBack. Selecciona una opción en el menú lateral para visualizar métricas y análisis.")

#Tiempo de carga
elif selected == "Tiempo de Carga":
    st.subheader("Tiempo de Carga de la Aplicación")
    df_load_time = get_data("SELECT * FROM homepage_load_time ORDER BY timestamp DESC LIMIT 100")
    if not df_load_time.empty:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.box(df_load_time, y="load_time", title="Distribución del Tiempo de Carga", color_discrete_sequence=[SECONDARY_COLOR])
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig_hist = px.histogram(df_load_time, x="load_time", title="Histograma de Tiempo de Carga", color_discrete_sequence=[PRIMARY_COLOR])
            st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.warning("No hay datos disponibles.")

#Restaurantes
elif selected == "Restaurantes":
    st.subheader("Restaurantes Mejor Valorados")
    df_reviews = get_data("SELECT restaurant_name, review_score FROM restaurant_reviews ORDER BY review_score DESC LIMIT 10")
    if not df_reviews.empty:
        fig = px.bar(df_reviews, x="restaurant_name", y="review_score", title="Restaurantes Mejor Calificados", color_discrete_sequence=[SECONDARY_COLOR])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos disponibles.")

#Filtros
elif selected == "Filtros":
    st.subheader("Filtros Más Utilizados")
    df_filters = get_data("SELECT filter_name, count FROM filter_buttons_usage ORDER BY count DESC LIMIT 10")
    if not df_filters.empty:
        fig = px.bar(df_filters, x="filter_name", y="count", title="Uso de Filtros en la Aplicación", color_discrete_sequence=[PRIMARY_COLOR])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos disponibles.")

#Categorías
elif selected == "Categorías":
    st.subheader("Categorías de Comida Más Listadas")
    df_food = get_data("SELECT category_name, count FROM food_listing ORDER BY count DESC LIMIT 10")
    if not df_food.empty:
        fig = px.bar(df_food, x="category_name", y="count", title="Distribución de Categorías de Comida", color_discrete_sequence=[SECONDARY_COLOR])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos disponibles.")

