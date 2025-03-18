import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

DB_URL = "postgresql://postgres:admin@localhost:5432/biteback_analytics"
engine = create_engine(DB_URL)

st.set_page_config(page_title="BiteBack Dashboard", layout="wide")

st.title("📊 BiteBack Analytics Dashboard")
st.subheader("📈 Análisis de Datos de la Aplicación")

@st.cache_data
def get_data(query):
    return pd.read_sql(query, engine)

st.markdown("### ⏳ Tiempo de Carga de la App")
query_1 = "SELECT * FROM homepage_load_time ORDER BY timestamp DESC LIMIT 100"
df_load_time = get_data(query_1)

if not df_load_time.empty:
    st.line_chart(df_load_time.set_index("timestamp")["load_time"])
else:
    st.warning("No hay datos disponibles para el tiempo de carga.")

st.markdown("### ⭐ Restaurantes Mejor Calificados")
query_2 = "SELECT restaurant_name, review_score FROM restaurant_reviews ORDER BY review_score DESC LIMIT 10"
df_reviews = get_data(query_2)

if not df_reviews.empty:
    st.bar_chart(df_reviews.set_index("restaurant_name")["review_score"])
else:
    st.warning("No hay datos de restaurantes disponibles.")

st.markdown("### 🔍 Filtros Más Utilizados")
query_3 = "SELECT filter_name, count FROM filter_buttons_usage ORDER BY count DESC LIMIT 10"
df_filters = get_data(query_3)

if not df_filters.empty:
    st.bar_chart(df_filters.set_index("filter_name")["count"])
else:
    st.warning("No hay datos de filtros disponibles.")

st.markdown("### 🍽️ Categorías de Comida Más Listadas")
query_4 = "SELECT category_name, count FROM food_listing ORDER BY count DESC LIMIT 10"
df_food = get_data(query_4)

if not df_food.empty:
    st.bar_chart(df_food.set_index("category_name")["count"])
else:
    st.warning("No hay datos de categorías de comida.")

st.markdown("---")
st.caption("📌 BiteBack Dashboard - Creado con Streamlit 🚀")
