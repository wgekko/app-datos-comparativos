import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# --------------------------------------------------
st.set_page_config(page_title="Dashboard de Ventas y Utilidad", layout="wide" , page_icon="icons/monitor-de-computadora.png")


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
    df = pd.read_excel("datos/db-datos.xlsx")
    # Crear columnas útiles para visualizaciones
    df['mes_nombre'] = df['mes'].apply(lambda x: 
        ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
        "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"][x-1]
    )
    df['anio_mes'] = df['anio'].astype(str) + "-" + df['mes'].astype(str).str.zfill(2)
    return df

df = load_data()

st.header(":material/desktop_cloud_stack: Dashboard Interactivo de Ventas, Total y Utilidad" )

# --------------------------------------------------
# SIDEBAR – FILTROS
# --------------------------------------------------
st.sidebar.header("Filtros del Dashboard")

# Años
anios = sorted(df["anio"].unique())
anio_actual = anios[-1]
anio = st.sidebar.selectbox("Año", options=anios, index=len(anios)-1)

# Países
paises = df["pais"].unique().tolist()
paises_seleccionados = st.sidebar.multiselect("Países", options=paises, default=paises)

# Categorías
categorias = df["categoria"].unique().tolist()
categorias_sel = st.sidebar.multiselect("Categorías", options=categorias, default=categorias)

# Productos
productos = df[df["categoria"].isin(categorias_sel)]["producto"].unique()
productos_sel = st.sidebar.multiselect("Productos (opcional)", options=productos)

# --------------------------------------------------
# FILTRADO DE DATOS
# --------------------------------------------------
filtrado = df[df["anio"] == anio]

if paises_seleccionados:
    filtrado = filtrado[filtrado["pais"].isin(paises_seleccionados)]

if categorias_sel:
    filtrado = filtrado[filtrado["categoria"].isin(categorias_sel)]

if productos_sel:
    filtrado = filtrado[filtrado["producto"].isin(productos_sel)]

# --------------------------------------------------
# VARIABLES DISPONIBLES PARA EJE X/Y
# --------------------------------------------------
variables_numericas = ["precio", "Cantidad", "Total", "utilidad", "util_porcent"]

margenes = ["Ninguno", "histogram", "rug", "box", "violin"]

# Selección de ejes
with st.container(horizontal=True):
    var_x = st.selectbox("Variable X", variables_numericas, index=0)
    margen_x = st.selectbox("Margen X", margenes, index=1)
    margen_x = None if margen_x == "Ninguno" else margen_x

with st.container(horizontal=True):
    var_y = st.selectbox("Variable Y", variables_numericas, index=2)
    margen_y = st.selectbox("Margen Y", margenes, index=3)
    margen_y = None if margen_y == "Ninguno" else margen_y

# Selector de color
color = st.selectbox("Color", options=["Ninguno", "pais", "categoria", "producto"], index=1)
color = None if color == "Ninguno" else color

# --------------------------------------------------
# GRÁFICO PRINCIPAL – SCATTER CON MÁRGENES
# --------------------------------------------------
fig1 = px.scatter(
    filtrado,
    x=var_x,
    y=var_y,
    color=color,
    hover_name="producto",
    title=f"{var_x} vs {var_y} – Año {anio}",
    marginal_x=margen_x,
    marginal_y=margen_y,
)

with st.container(border=True):
    st.subheader("Gráfico de Dispersión con Distribuciones")
    st.plotly_chart(fig1, use_container_width=True)

# --------------------------------------------------
# GRÁFICO ANIMADO – EVOLUCIÓN POR MES (AÑO SELECCIONADO)
# --------------------------------------------------
st.subheader("Evolución Animada por Mes")

df_ani = df[df["anio"] == anio]

fig2 = px.scatter(
    df_ani,
    x=var_x,
    y=var_y,
    color=color,
    hover_name="producto",
    animation_frame="mes_nombre",
    animation_group="producto",
    title=f"Evolución Mensual – {var_x} vs {var_y} – Año {anio}",
)

with st.container(border=True):
    st.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------
# RESUMEN DE KPIʼS
# --------------------------------------------------
st.subheader("Indicadores Generales del Filtro Actual")
c1, c2, c3 = st.columns(3)

c1.metric("Ventas Totales (USD)", f"{filtrado['Total'].sum():,.2f}")
c2.metric("Unidades Vendidas", f"{filtrado['Cantidad'].sum():,.0f}")
c3.metric("Utilidad Total (USD)", f"{filtrado['utilidad'].sum():,.2f}")

