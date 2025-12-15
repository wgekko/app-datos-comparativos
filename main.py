from datetime import time
import streamlit as st
from pathlib import Path
import streamlit as st
import base64
from streamlit.components.v1 import html
import streamlit.components.v1 as components


#st.set_page_config(page_title="Portal Animado", layout="wide")
st.set_page_config(page_title="Portal Animado", page_icon=":material/analytics:"  ,initial_sidebar_state="collapsed" ,layout="centered")

hide_sidebar_style = """
    <style>
        /* Oculta la barra lateral completa */
        [data-testid="stSidebar"] {
            display: none;
        }
        /* Ajusta el área principal para usar todo el ancho */
        [data-testid="stAppViewContainer"] {
            margin-left: 0px;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            .stDeployButton {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

bg_image = get_base64_image("img/alex-knight.jpg")

page_bg_css = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpg;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}

[data-testid="stApp"] {{
    background: transparent;
}}
</style>
"""

st.markdown(page_bg_css, unsafe_allow_html=True)



# ---------- Helper: leer archivos (si existen) ----------
def safe_read(path):
    p = Path(path)
    if p.exists():
        return p.read_text(encoding="utf-8")
    return ""

# Rutas esperadas (creá /assets y pon index.html, style.css, script.js dentro)
html_raw = safe_read("assets/index.html")
css_raw  = safe_read("assets/style.css")
js_raw   = safe_read("assets/script.js")
css_style =  safe_read("assets/styles.css")

# Si no tenés index.html en assets, construimos un HTML mínimo (fallback)
if not html_raw:
    html_raw = """
<div id="portalCard">
  <div class="gooey-effect">
    <div class="gooey-blob"></div>
    <div class="gooey-blob"></div>
    <div class="gooey-blob"></div>
    <div class="gooey-blob"></div>
  </div>

  <div id="portalContent">
    <h1>ENTER<br>THE PORTAL</h1>
    <button id="portalButton">GO</button>
  </div>

  <canvas class="card-bg" id="cardBgEffect"></canvas>
</div>

<div id="tunnelContainer" style="display:none">
  <canvas id="tunnelCanvas"></canvas>
</div>
"""

# Si no tenés style.css te recomiendo pegar tu CSS real en assets/style.css
if not css_raw:
    css_raw = "/* Inserta tu style.css en assets/style.css */\nbody{background:#000;color:#fff;}"

# Si no tenés script.js te recomiendo pegar tu JS real en assets/script.js
if not js_raw:
    js_raw = "// Inserta tu script.js en assets/script.js\nconsole.log('script.js no encontrado.');"

# ---------- Construir HTML final (concat sin f-strings con llaves) ----------
# NOTA: concatenamos para evitar problemas con llaves dentro del JS/CSS.
full_html = (
    "<!doctype html>\n"
    "<html>\n"
    "<head>\n"
    "  <meta charset='utf-8'>\n"
    "  <meta name='viewport' content='width=device-width, initial-scale=1'>\n"
    "  <style>\n" + css_raw + "\n  </style>\n"
    "</head>\n"
    "<body>\n"
    + html_raw + "\n"
    # incluimos Three.js desde CDN por si tu script.js lo usa y no lo incluye internamente
    "  <script src='https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js'></script>\n"
    "  <script>\n" + js_raw + "\n  </script>\n"
    # Hook adicional: asegurar que el botón GO active la función del túnel
    "  <script>\n"
    "    (function(){\n"
    "      function tryAttach(){\n"
    "        const btn = document.getElementById('portalButton');\n"
    "        const portalCard = document.getElementById('portalCard');\n"
    "        const tunnelContainer = document.getElementById('tunnelContainer');\n"
    "        if(!btn) return;\n"
    "        // evitar múltiples attach\n"
    "        if(btn.__attached) return; btn.__attached = true;\n"
    "        btn.addEventListener('click', function(evt){\n"
    "          console.log('GO clicked (bridge)');\n"
    "          try{ \n"
    "            // priorizar startPortal si existe (tu script lo usa)\n"
    "            if(typeof startPortal === 'function'){ startPortal(); }\n"
    "            else if(typeof initTunnel === 'function'){ initTunnel(); }\n"
    "            else if(typeof startTunnel === 'function'){ startTunnel(); }\n"
    "            else if(typeof render === 'function'){ /* render loop exist */ }\n"
    "            else { console.warn('No se encontró función para iniciar el túnel.'); }\n"
    "          } catch(e){ console.error('Error al invocar función del túnel:', e); }\n"
    "          // forzar mostrar/ocultar contenedores si tu script no lo hace\n"
    "          try{ if(portalCard) portalCard.style.display='none'; }catch(e){}\n"
    "          try{ if(tunnelContainer) tunnelContainer.style.display='block'; }catch(e){}\n"
    "        });\n"
    "      }\n"
    "      // retry attach: muchas librerías crean elementos después de load\n"
    "      document.addEventListener('DOMContentLoaded', tryAttach);\n"
    "      // intentar cada 300ms por 3s (por si el script crea elementos de forma asíncrona)\n"
    "      let retries=0; const i=setInterval(function(){ tryAttach(); retries++; if(retries>10) clearInterval(i); }, 300);\n"
    "    })();\n"
    "  </script>\n"
    "</body>\n"
    "</html>\n"
)

# ---------- Render en Streamlit ----------
# height: ajustar según quieras (900 es un buen inicio)
st.components.v1.html(full_html, height=700, scrolling=False)

# Inyectar CSS externo
if css_raw:
    st.markdown(f"<style>{css_raw}</style>", unsafe_allow_html=True)

with st.container(border=True):
    #{css_style}
    col1 , col2, col3, col4 = st.columns(4)

    with col1 :
        if st.button("Tienda Tech", key="acceso", use_container_width=True):
            st.switch_page("pages/1-TiendaTech.py")
    with col2:
        if st.button("Agricultura Global", key="acceso1", use_container_width=True):
            st.switch_page("pages/2-Agricultura Global.py")
    with col3:
        if st.button("Comercio Global", key="acceso2", use_container_width=True):
            st.switch_page("pages/3-Comercio Global.py")
    with col4:
        if st.button("PBI Global", key="acceso3", use_container_width=True):    
            st.switch_page("pages/4-PBI Global.py")    