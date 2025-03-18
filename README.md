# BiteBack Dashboard

BiteBack Dashboard es una herramienta de visualización interactiva desarrollada con **Streamlit** para analizar datos clave sobre el uso de la aplicación BiteBack, incluyendo tiempos de carga, restaurantes mejor valorados, filtros más utilizados y categorías de comida más listadas.

---

## **Requisitos Previos**
Antes de ejecutar el dashboard, asegúrate de tener:
- **Python 3.8+**
- **PostgreSQL** con la base de datos `biteback_analytics` ya poblada (proveniente del pipeline de analítica).
- **Credenciales de conexión a PostgreSQL** con el usuario y contraseña adecuados.

---

## **Instalación y Configuración**

### 1. **Clonar el repositorio**
```bash
 git clone https://github.com/tu-usuario/biteback-dashboard.git
 cd biteback-dashboard
```

### 2. **Crear y activar un entorno virtual**
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
# Windows: env\Scripts\activate
```

### 3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

### 4. **Configurar la conexión a la base de datos**
Abre el archivo `config.py` y asegurar que la conexión a PostgreSQL es correcta:
```python
DB_URL = "postgresql://postgres:admin@localhost:5432/biteback_analytics"
```

Si la configuración de la base de datos es diferente, **ajustar el usuario, contraseña y host**.

---

## **Ejecutar el Dashboard**
```bash
streamlit run app.py
```
Esto abrirá el dashboard en `http://localhost:8501`

---

## **Estructura del Proyecto**
```
├── app.py               # Código principal del dashboard
├── config.py            # Configuración de la base de datos
├── requirements.txt     # Lista de dependencias
├── README.md            # Este archivo
```

---

## **Secciones del Dashboard**
- **Inicio:** Vista general del dashboard.
- **Tiempo de Carga:** Análisis del tiempo de carga con **filtro de fechas**.
- **Restaurantes Mejor Valorados:** Ranking con **filtro de año y semana**.
- **Filtros Más Utilizados:** Análisis de la interacción con filtros en la app.
- **Categorías de Comida Más Listadas:** Distribución de los productos más publicados.

---

© 2025 BiteBack - Dashboard de Analítica 🚀

