import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from streamlit_option_menu import option_menu
import plotly.express as px
from config import engine, API_BASE_URL
import requests

# Constants for styling
PRIMARY_COLOR = "#F77F00"  
SECONDARY_COLOR = "#003049"  
TEXT_COLOR = "#303030"
BACKGROUND_COLOR = "#F5F5F5"
CARD_BG_COLOR = "#FCBF49" 

# Streamlit page configuration
st.set_page_config(page_title="BiteBack Dashboard", layout="wide")

# Sidebar setup
def setup_sidebar():
    with st.sidebar:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("assets/BiteBackLogoNaranja.png", width=60)
        with col2:
            st.markdown(f'<h1 style="color: {PRIMARY_COLOR};">BiteBack</h1>', unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title="Dashboard",
            options=["Inicio", "Tiempo de Carga", "Restaurantes", "Filtros", "Categorías","Búsquedas", "Popularidad", "Dispositivos", "Duración Checkout","Duracion en el carrito" ,"Top Productos", "Resumen de compras", "Tiempo de Carga Cart", "Pares de Productos", "Android Versions", "Android SDK"],
            icons=["house", "clock", "star", "search", "list", "search", "bar-chart","phone", "clock","hourglass-split" ,"cart", "clipboard", "clock", "link", "android", "cogs"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"background-color": BACKGROUND_COLOR},
                "icon": {"color": SECONDARY_COLOR, "font-size": "20px"},
                "nav-link": {"color": TEXT_COLOR, "font-size": "16px", "text-align": "left"},
                "nav-link-selected": {"background-color": PRIMARY_COLOR, "color": "white"},
            }
        )
    return selected

def update_database():
    endpoints = [
        "/homepage-load-time",
        "/most-liked-restaurants",
        "/most-used-filters",
        "/categories-frequencies",
        "/search-analytics",
        "/calculate-popularity",
        "/click-interactions",
        "/users-by-device",
        "/checkout-session-analytics",
        "/avg-checkout-time",
        "/checkout-summary",
        "/cartpage-load-time",
        "/most-common-product-pairs",
        "/users-by-android-version",
        "/users-by-android-sdk"
    ]
        
        
    with st.spinner("Actualizando datos..."):
        for endpoint in endpoints:
            response = requests.get(f"{API_BASE_URL}{endpoint}")
            if response.status_code == 200:
                st.success(f"Datos de {endpoint} actualizados correctamente")
            else:
                st.error(f"Error al actualizar {endpoint}: {response.status_code}")
                
    st.cache_data.clear()
                
def clean_database():
    endpoints = [
        "/clean-homepage-load-time",
        "/clean-most-liked-restaurants",
        "/clean-most-used-filters",
        "/clean-categories-frequencies",
        "/clean-search-analytics",
        "/clean-popularity",
        "/clean-click-interactions",
        "/clean-users-by-device",
        "/clean-checkout-session-analytics",
        "/clean-cartpage-load-time",
        "/clean-product-pairs",
        "/clean-user-android-versions",
        "/clean-user-android-sdks"
    
    ]
    with st.spinner("Vaciando base de datos..."):
        for endpoint in endpoints:
            response = requests.get(f"{API_BASE_URL}{endpoint}")
            if response.status_code == 200:
                st.success(f"Datos de {endpoint} limpiados correctamente")
            else:
                st.error(f"Error al actualizar {endpoint}: {response.status_code}")
            
    st.cache_data.clear()

# Data fetching function
@st.cache_data
def get_data(query):
    return pd.read_sql(query, engine)

# Page: Inicio
def show_inicio():
    st.title("BiteBack Analytics")
    st.subheader("Análisis de Datos de la Aplicación")
    st.markdown("Bienvenido al panel de control de BiteBack. Selecciona una opción en el menú lateral para visualizar métricas y análisis.")
    
    if st.button("🔄 Actualizar Información"):
        update_database()
        
    if st.button("🔄 Limpiar Información"):
        clean_database()

# Page: Tiempo de Carga
def show_tiempo_de_carga():
    st.subheader("Tiempo de Carga de la Aplicación")
    df_load_time = get_data("SELECT * FROM homepage_load_time ORDER BY timestamp DESC LIMIT 1000")
    
    if not df_load_time.empty:
        try:
            df_load_time['timestamp'] = pd.to_datetime(df_load_time['timestamp'])
            start_date, end_date = st.date_input("Rango de fechas", [df_load_time['timestamp'].min(), df_load_time['timestamp'].max()])
            df_filtered = df_load_time[(df_load_time['timestamp'] >= pd.to_datetime(start_date)) & (df_load_time['timestamp'] <= pd.to_datetime(end_date))]
            
            if not df_filtered.empty:
                col1, col2 = st.columns(2)
                with col1:
                    fig = px.box(df_filtered, y="load_time", title="Distribución del Tiempo de Carga", color_discrete_sequence=[SECONDARY_COLOR])
                    st.plotly_chart(fig, use_container_width=True)
                with col2:
                    fig_hist = px.histogram(df_filtered, x="load_time", title="Histograma de Tiempo de Carga", color_discrete_sequence=[PRIMARY_COLOR])
                    st.plotly_chart(fig_hist, use_container_width=True)
            else:
                st.warning("No hay datos disponibles en el rango de fechas seleccionado.")
        except Exception as e:
            st.error("Ocurrió un error al filtrar los datos. Por favor, verifica los valores seleccionados.")
    else:
        st.warning("No hay datos disponibles.")

# Page: Restaurantes
def show_restaurantes():
    st.subheader("Restaurantes Mejor Valorados")
    df_reviews = get_data("SELECT * FROM restaurant_reviews ORDER BY review_score DESC LIMIT 500")
    
    if not df_reviews.empty:
        year = st.selectbox("Selecciona el año", sorted(df_reviews["year"].unique(), reverse=True))
        week = st.selectbox("Selecciona la semana", sorted(df_reviews[df_reviews["year"] == year]["week"].unique(), reverse=True))
        df_filtered = df_reviews[(df_reviews["year"] == year) & (df_reviews["week"] == week)]
        
        fig = px.bar(df_filtered, x="restaurant_name", y="review_score", title="Restaurantes Mejor Calificados", color_discrete_sequence=[SECONDARY_COLOR])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos disponibles.")

# Page: Filtros
def show_filtros():
    st.subheader("Filtros Más Utilizados")
    df_filters = get_data("SELECT * FROM filter_buttons_usage ORDER BY count DESC LIMIT 10")
    if not df_filters.empty:
        fig = px.bar(df_filters, x="filter_name", y="count", title="Uso de Filtros en la Aplicación", color_discrete_sequence=[PRIMARY_COLOR])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos disponibles.")

# Page: Categorías
def show_categorias():
    st.subheader("Categorías de Comida Más Listadas")
    df_food = get_data("SELECT * FROM food_listing ORDER BY count DESC LIMIT 10")
    if not df_food.empty:
        fig = px.bar(df_food, x="category_name", y="count", title="Distribución de Categorías de Comida", color_discrete_sequence=[SECONDARY_COLOR])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos disponibles.")

# Page: Búsquedas más populares
def show_busquedas():
    st.subheader("Términos de Búsqueda Más Usados")
    df_searches = get_data("SELECT * FROM searches_analytics ORDER BY count DESC LIMIT 10")
    if not df_searches.empty:
        fig = px.bar(df_searches, x="search_term", y="count", title="Búsquedas Más Frecuentes", color_discrete_sequence=[PRIMARY_COLOR])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos disponibles.")

# Page: Popularidad de Categorías
def show_popularidad():
    st.subheader("Índice de Popularidad de Categorías")
    df_popularity = get_data("SELECT * FROM popularity_index ORDER BY popularity_score DESC LIMIT 10")
    if not df_popularity.empty:
        fig = px.bar(df_popularity, x="category", y="popularity_score", title="Popularidad de Categorías", color_discrete_sequence=[SECONDARY_COLOR])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos disponibles.")
        
def show_dispositivos():
    st.subheader("Distribución de Dispositivos por Modelo")
    df_devices = get_data("SELECT * FROM user_devices ORDER BY user_count DESC")

    if not df_devices.empty:
        fig = px.pie(df_devices, names='device_model', values='user_count', title='Distribución de Usuarios por Dispositivo', color_discrete_sequence=px.colors.sequential.Oranges)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos disponibles sobre dispositivos.")

def show_duracion_checkout():
    st.subheader("🕒 Tiempo promedio de navegación antes de la compra")

    df = get_data("SELECT * FROM checkout_session_stats")

    if not df.empty:
        df['week'] = df['week'].astype(int)
        df['year'] = df['year'].astype(int)

        # Crear fecha a partir del año + semana (lunes como día base)
        df['fecha'] = pd.to_datetime(df['year'].astype(str) + df['week'].astype(str) + '1', format='%G%V%u')

        selected_year = st.selectbox("Selecciona el año", sorted(df['year'].unique(), reverse=True))

        filtered = df[df['year'] == selected_year].sort_values("fecha")

        # Calcular el promedio anual
        promedio_anual = filtered['avg_duration'].mean()

        fig = px.line(
            filtered,
            x="fecha",
            y="avg_duration",
            title=f"Duración Promedio de Navegación - Año {selected_year}",
            labels={
                "fecha": "Semana",
                "avg_duration": "Duración Promedio (ms)"
            },
            markers=True,
            color_discrete_sequence=[PRIMARY_COLOR]
        )

        # Línea horizontal para mostrar el promedio anual
        fig.add_hline(
            y=promedio_anual,
            line_dash="dot",
            line_color="gray",
            annotation_text=f"Promedio anual: {promedio_anual:.0f} ms",
            annotation_position="top left"
        )

        fig.update_layout(
            xaxis_title="Semana del Año",
            yaxis_title="Duración Promedio (milisegundos)",
            hovermode="x unified",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ No hay datos disponibles para mostrar.")



def show_top_productos():
    st.subheader("Top Productos más Comprados por Semana")
    df = get_data("SELECT * FROM top_products_by_week")

    if not df.empty:
        selected_year = st.selectbox("Selecciona el año", sorted(df['year'].unique(), reverse=True))
        selected_week = st.selectbox("Selecciona la semana", sorted(df[df['year'] == selected_year]['week'].unique(), reverse=True))

        filtered = df[(df['year'] == selected_year) & (df['week'] == selected_week)]

        fig = px.bar(
            filtered,
            x="name",  # ← Este era el error
            y="quantity",
            title=f"Top productos semana {selected_week}, {selected_year}",
            color_discrete_sequence=[SECONDARY_COLOR]
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos disponibles para mostrar.")

def show_duracion_purchases():
    st.subheader("Tiempo Promedio para Finalizar Compra")

    df_checkout = get_data("SELECT * FROM checkout_time_analytics ORDER BY timestamp DESC LIMIT 500")

    if not df_checkout.empty:
        df_checkout["timestamp"] = pd.to_datetime(df_checkout["timestamp"])

      
        general_average = df_checkout[(df_checkout["day_of_week"].isna()) & (df_checkout["hour"].isna())]
        avg_all = general_average["average_minutes"].mean()

     
        by_day = df_checkout[df_checkout["hour"].isna() & df_checkout["day_of_week"].notna()]
        avg_day = by_day.groupby("day_of_week")["average_minutes"].mean().reset_index()

       
        by_hour = df_checkout[df_checkout["day_of_week"].isna() & df_checkout["hour"].notna()]
        avg_hour = by_hour.groupby("hour")["average_minutes"].mean().reset_index()

        # Average global metrics
        col1, col2 = st.columns(2)
        with col1:
            avg_today = df_checkout[df_checkout["timestamp"].dt.date == pd.Timestamp.today().date()]["average_minutes"].mean()
            st.metric("Promedio de hoy", f"{avg_today:.2f} min" if pd.notna(avg_today) else "N/A")
        with col2:
            st.metric("Promedio general", f"{avg_all:.2f} min" if pd.notna(avg_all) else "N/A")

        # Line graph
        fig_line = px.line(
            df_checkout.sort_values("timestamp"),
            x="timestamp",
            y="average_minutes",
            title="Evolución del Tiempo Promedio de Checkout",
            color_discrete_sequence=[SECONDARY_COLOR]
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # Pie char per day
        fig_pie = px.pie(
            avg_day,
            names="day_of_week",
            values="average_minutes",
            title="Promedio de tiempo de compra por dia"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        # BarChar by Hour
        fig_bar = px.bar(
            avg_hour.sort_values("hour"),
            x="hour",
            y="average_minutes",
            title="Promedio de tiempo de compra por Hora del Día",
            labels={"hour": "Hora", "average_minutes": "Minutos"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

      
    else:
        st.warning("No hay datos disponibles para mostrar.")

def show_checkout_summary():
    st.subheader("Resumen de Comportamiento de Checkout")

    df_summary = get_data("SELECT * FROM checkout_summary_analytics")

    if not df_summary.empty:
        # Separar los tipos
        df_forgotten = df_summary[df_summary["type"] == "forgotten"]
        df_completed = df_summary[df_summary["type"] == "completed"]

        # Mostrar número de olvidos
        forgotten_count = int(df_forgotten["sales_count"].sum()) if not df_forgotten.empty else 0
        st.metric("Veces que los usuarios olvidaron pagar", forgotten_count)

        # Gráfica de barras por día de la semana
        if not df_completed.empty:
            fig_bar = px.bar(
                df_completed.sort_values("day_of_week"),
                x="day_of_week",
                y="sales_count",
                title="Cantidad de Compras Completadas por Día de la Semana",
                labels={"day_of_week": "Día", "sales_count": "Cantidad"},
                color_discrete_sequence=[PRIMARY_COLOR]
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No hay compras completadas registradas.")

    else:
        st.warning("No hay datos disponibles para mostrar.")
        
        
# Gráfica: Tiempo de carga CartScreen

def show_tiempo_de_carga_cart():
    st.subheader("⏳ Tiempo de Carga - Vista del Carrito")
    df = get_data("SELECT * FROM cartpage_load_time ORDER BY timestamp DESC LIMIT 1000")

    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        start, end = st.date_input("Rango de fechas", [df['timestamp'].min(), df['timestamp'].max()])
        filtered = df[(df['timestamp'] >= pd.to_datetime(start)) & (df['timestamp'] <= pd.to_datetime(end))]

        if not filtered.empty:
            col1, col2 = st.columns(2)
            with col1:
                fig_box = px.box(filtered, y="load_time", title="Distribución del Tiempo de Carga del Carrito", color_discrete_sequence=[SECONDARY_COLOR])
                st.plotly_chart(fig_box, use_container_width=True)
            with col2:
                fig_hist = px.histogram(filtered, x="load_time", title="Histograma de Tiempos de Carga del Carrito", color_discrete_sequence=[PRIMARY_COLOR])
                st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.warning("No hay datos en el rango seleccionado.")
    else:
        st.warning("No hay datos disponibles.")

# Gráfica: Pares de productos más comprados juntos

def show_product_pairs():
    st.subheader("🔗 Productos Comprados Juntos con Mayor Frecuencia")
    df = get_data("SELECT * FROM product_pair_analytics ORDER BY count DESC LIMIT 10")
    if not df.empty:

        df['pair'] = df['name_a'] + " + " + df['name_b']
        fig = px.bar(df.sort_values("count", ascending=False), x="pair", y="count", title="Pares de productos más vendidos")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos disponibles.")

# Gráfica: Usuarios por versión de Android

def show_android_versions():
    st.subheader("📱 Usuarios por Versión de Android")
    df = get_data("SELECT * FROM user_android_versions ORDER BY user_count DESC")

    if not df.empty:
        fig = px.pie(df, names='android_version', values='user_count', title='Distribución de Usuarios por Versión de Android', color_discrete_sequence=px.colors.sequential.Oranges)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos disponibles.")

# Gráfica: Usuarios por SDK

def show_android_sdk():
    st.subheader("🔢 Usuarios por Nivel de SDK (Android)")
    df = get_data("SELECT * FROM user_android_sdks ORDER BY user_count DESC")

    if not df.empty:
        fig = px.bar(df, x="android_sdk", y="user_count", title="Usuarios por Nivel de SDK", color_discrete_sequence=[PRIMARY_COLOR])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos disponibles.")





# Main function to handle page selection
def main():
    selected = setup_sidebar()
    
    if selected == "Inicio":
        show_inicio()
    elif selected == "Tiempo de Carga":
        show_tiempo_de_carga()
    elif selected == "Restaurantes":
        show_restaurantes()
    elif selected == "Filtros":
        show_filtros()
    elif selected == "Categorías":
        show_categorias()
    elif selected == "Búsquedas":
        show_busquedas()
    elif selected == "Popularidad":
        show_popularidad()
    elif selected == "Dispositivos":
        show_dispositivos()
    elif selected == "Duración Checkout":
        show_duracion_checkout()
    elif selected == "Duracion en el carrito":
        show_duracion_purchases()  
    elif selected == "Top Productos":
        show_top_productos()
    elif selected == "Tiempo de Carga Cart":
        show_tiempo_de_carga_cart()
    elif selected == "Pares de Productos":
        show_product_pairs()
    elif selected == "Android Versions":
        show_android_versions()
    elif selected == "Android SDK":
        show_android_sdk()
    elif selected == "Resumen de compras":
        show_checkout_summary()

if __name__ == "__main__":
    main()
