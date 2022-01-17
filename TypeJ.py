#--------------------------------------------------------------------#
#--------Aplicación Construcción Pozo Vertical, J y S v2.0-----------#
#--------------------------------------------------------------------#
#-----Elaborado por Ing. Carlos Carrillo Villavicencio MSc. TIC------#
#--------------------------------------------------------------------#

#----------------Librerias a importarse------------------------------#
import streamlit as st
import pandas as pd
import plotly.express as px
import math
from PIL import Image
import base64
#----------------Librerias Internas Módulos -------------------------#
import pozo_vertical
import pozo_tipo_j
import pozo_tipo_s
#-------------------Configuraciones de página------------------------#

#----------------Importación Multimedia------------------------------#
image1 = Image.open('Diagrama pozo tipo J.png')
logo = Image.open('Logo.png')


#------------------Desarrollo de Portada html------------------------#
html_portada = """
	<div style="background-image: linear-gradient(60deg, #2ecc71, #2980b9);padding:10px">
		<h2 style= "color:black; text-align:center; font: bold 25px Poppins, sans-serif  ">Well Trajectory Calculations App - Python </h2>
	</div>
	"""
st.markdown(html_portada, unsafe_allow_html=True)
#------------------------------Logo----------------------------------#

st.sidebar.image(logo,width = 100, caption='App Version 2.0')


#--------------------------Gif inicio--------------------------------#
gif1 = open("Plataforma1.gif", "rb")
gif2 = open("Plataforma2.gif", "rb")


contents1 = gif1.read()
g1 = base64.b64encode(contents1).decode("utf-8")
gif1.close()

contents2 = gif2.read()
g2 = base64.b64encode(contents2).decode("utf-8")
gif2.close()

#-----------------Selección de Módulos ------------------------------#
st.sidebar.header('Selección del tipo de pozo')

modulo = st.sidebar.selectbox('Seleccione', options = ['Seleccione', 'Pozo Vertical', 'Pozo tipo J', 'Pozo tipo S'], format_func=lambda x: 'Seleccione' if x == '' else x)

if modulo == 'Seleccione':

	st.markdown(""" <p style="text-align:center"> Aplicación desarrollada para ejecutar cálculos en la construcción de pozos vertiles y direccionales en la indusstria Oil & Gas</p> """,unsafe_allow_html=True)
	col1, col2 = st.beta_columns(2)

	with col1:
		st.markdown(
		    f'<img style="position: relative; display: inline-block; left: 50%; transform: translate(-50%);" src="data:image/gif;base64,{g1}" alt="cat gif" width="400" height="350">',
		    unsafe_allow_html=True)
	with col2:
		st.markdown(
		    f'<img style="position: relative; display: inline-block; left: 50%; transform: translate(-50%);" src="data:image/gif;base64,{g2}" alt="cat gif" width="400" height="350">',
		    unsafe_allow_html=True)

	
	st.markdown(""" <p style="text-align:center"> <b> Elaborado por:</b> Ing. Carlos Carrillo Villavicencio, MSc. en Tecnologias de la Información, Analista de datos y Programador Python</p> """,unsafe_allow_html=True)

elif modulo == 'Pozo Vertical':
	st.error('En construccion')

elif modulo == 'Pozo tipo J':
	pozo_tipo_j.construccion(image1)

elif modulo == 'Pozo tipo S':
	st.error('En construccion')
