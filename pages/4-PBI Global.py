import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página de la aplicación
st.set_page_config(page_title="Gráficos de dispersión mejorados", layout="wide")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            .stDeployButton {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --------------------------------------------------
# CARGA DEL ARCHIVO EXCEL LOCAL
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("datos/crecimiento % PBI- PerCapita-Deflactor-Sector Privado.xlsx")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.header(":material/browse_activity: Análisis de PBI a Nivel Global")
st.write("---")

st.header("Gráficos de Dispersión mejorados con gráficos de Margen y animaciones")

# --- SECCIÓN: BARRA LATERAL (SIDEBAR) Y FILTROS ---
st.sidebar.header("Filtros")

# 1. Obtener lista de años únicos y ordenarlos
anos = sorted(df['Anio'].unique())
#ano_actual = datetime.now().year
ano_actual = int(df["Anio"].max())

# Selector de año (Slider)
# Nota: Si el año actual es mayor al máximo del dataset, el slider se ajustará al valor más cercano permitido.
ano = st.sidebar.select_slider("Anio", options=anos, value=ano_actual)

# 2. Obtener lista de continentes únicos
continentes = df['Continente'].unique().tolist()
# Multiselector para continentes
continentes_seleccionados = st.sidebar.multiselect("Continente", options=continentes, default=continentes)

# 3. Filtrado dinámico de países basado en los continentes seleccionados
# Pandas: df[condición] filtra las filas. .unique() obtiene valores únicos.
paises = df[df['Continente'].isin(continentes_seleccionados)]['Pais'].unique().tolist()
paises_seleccionados = st.sidebar.multiselect("Paises (opcional)", options=paises, default=[])

# --- SECCIÓN: TRANSFORMACIÓN DE DATOS (FILTRADO) ---

# Filtrar por año seleccionado
filtrado = df[df['Anio'] == ano]

# Filtrar por continentes si hay selección
if continentes_seleccionados:
    # Pandas: .isin() verifica si el valor de la columna está en la lista dada
    filtrado = filtrado[filtrado['Continente'].isin(continentes_seleccionados)]

# Filtrar por países si el usuario seleccionó alguno específicamente
if paises_seleccionados:
    filtrado = filtrado[filtrado['Pais'].isin(paises_seleccionados)]

# Definición de variables numéricas disponibles para los ejes
#variables = ['Crecimiento PBI % Anual',	'Crecimiento PBI PerCapita % Anual', 'Inflacion Deflactor % PBI', 'Crecimiento Interno Sector Privado % PBI']
# Ahora esto funcionará porque el nombre en el DF ya no tiene el espacio oculto
variables = [
    'Crecimiento PBI % Anual', 
    'Crecimiento PBI PerCapita % Anual', 
    'Inflacion Deflactor % PBI', 
    'Crecimiento Interno Sector Privado % PBI'
]



# Tipos de gráficos marginales disponibles en Plotly
margen_grafico = ["Ninguno","histogram", "rug", "box", "violin"]

# --- SECCIÓN: CONFIGURACIÓN DE EJES Y GRÁFICOS ---

# Selectores para el Eje X
with st.container(horizontal=True): # Disposición horizontal
    var_x = st.selectbox("Variable X", options=variables, index=0)
    margen_x = st.selectbox("Margen X", options=margen_grafico, index=1)
    if margen_x == "Ninguno":
        margen_x = None

# Selectores para el Eje Y
with st.container(horizontal=True):
    var_y = st.selectbox("Variable Y", options=variables, index=1)
    margen_y = st.selectbox("Margen Y", options=margen_grafico, index=3)
    if margen_y == "Ninguno":
        margen_y = None

# Selector de color (variable categórica para agrupar)
color = st.selectbox("Color", options=['Ninguno', 'Continente', 'Pais'], index=0)
if color == 'Ninguno':
    color = None

# --- GRÁFICO 1: SCATTER PLOT ESTÁTICO CON MÁRGENES ---
# px.scatter crea un gráfico de dispersión.
# marginal_x/y añade un gráfico secundario en los márgenes para ver la distribución de esa variable.
fig = px.scatter(filtrado, x=var_x, y=var_y, 
                color=color, hover_name="Pais",
                title=f"{var_x} vs {var_y} Año: {ano}",
                marginal_x=margen_x, marginal_y=margen_y,
                )

# Mostrar el gráfico en Streamlit dentro de un contenedor con borde
with st.container(border=True):
    st.plotly_chart(fig, use_container_width=True)

# --- GRÁFICO 2: ANIMACIÓN TEMPORAL ---

# Slider para seleccionar un rango de años
parRangoAnos = st.slider("Rango de Años", min_value=min(anos), max_value=max(anos), value=(ano_actual-25, ano_actual), step=1)

# Pandas: Filtrado complejo con múltiples condiciones (& significa AND)
# Seleccionamos filas donde el año sea mayor/igual al inicio Y menor/igual al fin del rango
df_rango = df[(df['Anio'] >= parRangoAnos[0]) & (df['Anio'] <= parRangoAnos[1])]

# Crear gráfico animado
# animation_frame: define la variable que cambia en cada frame (el tiempo)
# animation_group: define qué entidad se rastrea a través de los frames (el país)
fig2 = px.scatter(df_rango, x=var_x, y=var_y, 
                color=color, hover_name="Pais",
                title=f"{var_x} vs {var_y} Rango Años: {parRangoAnos[0]} - {parRangoAnos[1]}",
                animation_frame="Anio", animation_group="Pais",
                )

with st.container(border=True):
    st.subheader("Gráfico Animado por Rango de Años")
    st.plotly_chart(fig2, use_container_width=True)