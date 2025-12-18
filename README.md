# app-datos-comparativos
app que compara y grafica datos con graficos de histogramas, box y otras altenativas de analisis de datos 
si se desea mantenar la configuración de fondo
ademas hay que crear una carpeta .stramlit y dentro de ella crear un archivo config.toml

[server]
enableStaticServing = true
[[theme.fontFaces]]
family = "Inter"
url = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap"
[theme]
primaryColor = "#FF8C00"
backgroundColor = "#0D1B2A"
secondaryBackgroundColor = "#1B263B"
textColor = "#FFA500"
linkColor = "#FFA500"
borderColor = "#CCCCCC"
showWidgetBorder = true
baseRadius = "0.5rem"
buttonRadius = "0.5rem"
font = "Inter"
headingFontWeights = [600, 500]
headingFontSizes = ["2.5rem", "1.8rem"]
codeFont = "Courier New"
codeFontSize = "0.75rem"
codeBackgroundColor = "#112B3C"
showSidebarBorder = false
chartCategoricalColors = [
  "#FF8C00",  # Orange oscuro
  "#FFA500",  # Naranja clásico
  "#FFD700",  # Mostaza / dorado
  "#E1C16E",  # Mostaza claro
  "#C8E25D",  # Lima suave
  "#A8D08D",  # Verde pastel
  "#7AC36A",  # Verde hoja
  "#4CAF50",  # Verde medio
  "#40C4FF",  # Celeste vibrante
  "#00B0F0",  # Celeste profesional
  "#3399FF",  # Celeste más oscuro
  "#1E88E5",  # Azul Francia
  "#1976D2",  # Azul fuerte
  "#1565C0",  # Azul oscuro
  "#0D47A1"   # Azul muy profundo
]

chartCategoricalColors1 = [
  "#FF8C00",
  "#FFA500",
  "#FFB347",
  "#FFD580",
  "#FFA07A",
  "#FF7F50",
  "#FF6F00",
  "#CC7000",
  "#FFC107",
  "#FFDD57",
  "#E67E22",
  "#D35400",
  "#F39C12",
  "#E67E22",
  "#F4A261"
]
[theme.sidebar]
backgroundColor = "#1E3A5F"
secondaryBackgroundColor = "#1B263B"
headingFontSizes = ["1.6rem", "1.4rem", "1.2rem"]
dataframeHeaderBackgroundColor = "#1A2A40"
lind de codigo de portal animado de ingreso de la app 
https://codepen.io/matt-cannon/pen/OPPJLNa
link de video base de codigo de modelo de analisis 
https://www.youtube.com/watch?v=JgaYJ0YRJ5I
--------------------------------------------------------------------------------------------------------------------------------------------------------
descripcion de la app 
Data App analítica basada en datos del Banco Mundial y de una empresa tech
Desarrollo de una aplicación interactiva en Python, Streamlit y Plotly que integra y analiza datos oficiales del Banco Mundial sobre actividad agrícola, comercio y PBI, 
orientada a exploración avanzada y análisis comparativo. Y además de ventas de productos de  tecnológico de una tienda. 
La app permite filtrar dinámicamente por año, región y país, comparar indicadores clave mediante gráficos de dispersión con análisis estadístico marginal
y visualizar su evolución histórica con animaciones temporales. Pensada para analistas, BI y perfiles técnicos, 
facilita la detección de patrones macroeconómicos, relaciones entre productividad y comercio, y soporta decisiones basadas en datos confiables y escalables.


video demo 


https://github.com/user-attachments/assets/60f6e70a-1792-46ff-bf94-67f4f96ee910





