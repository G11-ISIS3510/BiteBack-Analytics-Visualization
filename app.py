import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from streamlit_option_menu import option_menu

# Conexión a PostgreSQL
DB_URL = "postgresql://postgres:admin@localhost:5432/biteback_analytics"
engine = create_engine(DB_URL)

# Configurar Streamlit
st.set_page_config(page_title="BiteBack Dashboard", layout="wide")

# Menú lateral
with st.sidebar:
    selected = option_menu(
        menu_title="📊 BiteBack Dashboard",
        options=["Inicio", "Tiempo de Carga", "Restaurantes", "Filtros", "Categorías"],
        icons=["house", "clock", "star", "search", "list"],
        menu_icon="cast",
        default_index=0,
    )

# Función para obtener datos
@st.cache_data
def get_data(query):
    return pd.read_sql(query, engine)

# Sección: Inicio
if selected == "Inicio":
    st.title("📊 BiteBack Analytics")
    st.subheader("📈 Análisis de Datos en Tiempo Real")
    st.markdown("Selecciona una sección en el menú lateral.")

# Sección: Tiempo de carga
elif selected == "Tiempo de Carga":
    st.subheader("⏳ Tiempo de Carga de la App")
    df_load_time = get_data("SELECT * FROM homepage_load_time ORDER BY timestamp DESC LIMIT 100")
    if not df_load_time.empty:
        st.line_chart(df_load_time.set_index("timestamp")["load_time"])
    else:
        st.warning("No hay datos disponibles.")

# Sección: Restaurantes
elif selected == "Restaurantes":
    st.subheader("⭐ Restaurantes Más Valorados")
    df_reviews = get_data("SELECT restaurant_name, review_score FROM restaurant_reviews ORDER BY review_score DESC LIMIT 10")
    if not df_reviews.empty:
        st.bar_chart(df_reviews.set_index("restaurant_name")["review_score"])
    else:
        st.warning("No hay datos disponibles.")

# Sección: Filtros
elif selected == "Filtros":
    st.subheader("🔍 Filtros Más Utilizados")
    df_filters = get_data("SELECT filter_name, count FROM filter_buttons_usage ORDER BY count DESC LIMIT 10")
    if not df_filters.empty:
        st.bar_chart(df_filters.set_index("filter_name")["count"])
    else:
        st.warning("No hay datos disponibles.")

# Sección: Categorías de comida
elif selected == "Categorías":
    st.subheader("🍽️ Categorías de Comida Más Listadas")
    df_food = get_data("SELECT category_name, count FROM food_listing ORDER BY count DESC LIMIT 10")
    if not df_food.empty:
        st.bar_chart(df_food.set_index("category_name")["count"])
    else:
        st.warning("No hay datos disponibles.")

st.markdown("---")
st.caption("📌 BiteBack Dashboard - Creado con Streamlit 🚀")
