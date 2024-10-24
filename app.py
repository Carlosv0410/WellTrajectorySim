#--------------------------------------------------------------------#
#--------Aplicación Construcción Pozo Vertical, J y S v3.0-----------#
#----Elaborado por Ing. Carlos Carrillo Villavicencio MSc. TIC-------#
#--------------------------------------------------------------------#

#----------------Librerias a importarse------------------------------#
# Importamos la librería Streamlit para crear la interfaz de la aplicación web
import streamlit as st

# Importamos pandas para manipulación y análisis de datos
import pandas as pd

# Importamos Plotly Express para crear gráficos interactivos de manera sencilla
import plotly.express as px

# Importamos math para realizar operaciones matemáticas como funciones trigonométricas
import math

# Importamos la librería PIL (Python Imaging Library) para cargar y manipular imágenes
from PIL import Image

# Importamos base64 para codificar y decodificar datos (útil para manejar imágenes en formato base64)
import base64

#----------------Librerías Internas Módulos -------------------------#
# Importamos el módulo que contiene las funciones para calcular el pozo vertical
import pozo_vertical

# Importamos el módulo que contiene las funciones para calcular el pozo tipo J
import pozo_tipo_j

# Importamos el módulo que contiene las funciones para calcular el pozo tipo S
import pozo_tipo_s

#-------------------Configuraciones de página------------------------#
#st.set_page_config(
#     page_title="Built Well Type J and S App",
#     page_icon="🛢",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )
#----------------Importación Multimedia------------------------------#
# Cargamos la imagen del diagrama del pozo tipo J desde un archivo PNG
image1 = Image.open('Diagrama pozo tipo J.png')

# Cargamos el logo desde un archivo PNG
logo = Image.open('Logo.png')



#------------------Desarrollo de Portada html------------------------#
html_portada = """
	<div style="background-image: linear-gradient(60deg, #0a0a0a, #ffc300, #3a3a3a);padding:10px">
		<h2 style= "color:black; text-align:center; font: bold 25px Poppins, sans-serif  ">Well Trajectory Calculations App - Python </h2>
	</div>
	"""
st.markdown(html_portada, unsafe_allow_html=True)
#------------------------------Logo----------------------------------#
st.sidebar.image(logo, width=300, caption='App Version 3.0')

#--------------------------Gif inicio--------------------------------#
# Utilizamos @st.cache_data para almacenar en caché la codificación base64 del GIF
@st.cache_data
def load_gif(file_path):
    with open(file_path, "rb") as gif_file:
        contents = gif_file.read()
        return base64.b64encode(contents).decode("utf-8")

# Cargamos y codificamos los GIFs animados una sola vez
g1 = load_gif("Plataforma1.png")
g2 = load_gif("Plataforma2.png")
g3 = load_gif("Plataforma3.png")

#-----------------Selección de Módulos ------------------------------#
# Agregamos un encabezado en el sidebar para la selección del tipo de pozo
st.sidebar.header('Selección del tipo de pozo')

# Creamos un selectbox en el sidebar para que el usuario seleccione el tipo de pozo
modulo = st.sidebar.selectbox(
    'Seleccione', 
    options=['Seleccione', 'Pozo Vertical', 'Pozo tipo J', 'Pozo tipo S'], 
    format_func=lambda x: 'Seleccione' if x == '' else x  # Formato para mostrar 'Seleccione' cuando no se elige una opción válida
)

# Verificamos si el usuario no ha seleccionado ningún módulo ('Seleccione')
if modulo == 'Seleccione':

    # Mostramos una descripción centrada de la aplicación
    st.markdown(""" 
    <p style="text-align:center"> 
    Aplicación desarrollada para ejecutar cálculos en la construcción de pozos verticales y direccionales en la industria Oil & Gas
    </p> 
    """, unsafe_allow_html=True)

    # Creamos dos columnas para mostrar los GIFs lado a lado
    col1, col2 ,col3= st.columns(3)

    # Mostramos el primer GIF en la primera columna con alineación centrada
    with col1:
        st.markdown(
            f'<img style="position: relative; display: inline-block; left: 50%; transform: translate(-50%);" src="data:image/gif;base64,{g1}" alt="gif1" width="400" height="250">',
            unsafe_allow_html=True
        )

    # Mostramos el segundo GIF en la segunda columna con alineación centrada
    with col2:
        st.markdown(
            f'<img style="position: relative; display: inline-block; left: 50%; transform: translate(-50%);" src="data:image/gif;base64,{g2}" alt="gif2" width="400" height="250">',
            unsafe_allow_html=True
        )

    # Mostramos el tercer GIF en la tercera columna con alineación centrada
    with col3:
        st.markdown(
            f'<img style="position: relative; display: inline-block; left: 50%; transform: translate(-50%);" src="data:image/gif;base64,{g3}" alt="gif3" width="400" height="250">',
            unsafe_allow_html=True
        )


    # Agregar mensaje centrado de crédito al autor con colores adecuados para modo oscuro
    st.markdown("""
        <div style="text-align:center; font-size:18px; color:lightgray; margin-top:20px;">
            <p><strong>Elaborado por:</strong></p>
            <p><strong>Carlos Carrillo Villavicencio</strong></p>
	    <p>MSc. Tecnologias de la Información</p>
            <p>Ingeniero en Petróleos</p>
            <p>Ingeniero de Transformación Digital</p>
            <p>Data Scientist</p>
            <p>Programador Python</p>
            <p>Instructor Certificado</p>
        </div>
        """, unsafe_allow_html=True)



# Verificamos si el usuario seleccionó el módulo 'Pozo Vertical'
elif modulo == 'Pozo Vertical':
    # Mostramos un mensaje de error temporal indicando que está en construcción
    pozo_vertical.construccion()

# Verificamos si el usuario seleccionó el módulo 'Pozo tipo J'
elif modulo == 'Pozo tipo J':
    # Llamamos a la función 'construccion' del módulo 'pozo_tipo_j', pasándole la imagen del diagrama
    pozo_tipo_j.construccion(image1)

# Verificamos si el usuario seleccionó el módulo 'Pozo tipo S'
elif modulo == 'Pozo tipo S':
    # Mostramos un mensaje de error temporal indicando que está en construcción
    pozo_tipo_s.construccion()
