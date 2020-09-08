#Aplicacion Construccion Pozo tipo J

#Librerias a importarse
import streamlit as st
import pandas as pd
import plotly.express as px
import math
#Libreria para importar imagenes
from PIL import Image

#importacion de imagen

image1 = Image.open('Diagrama pozo tipo J.png')

#Títulos
html_temp = """
	<div style="background-color: #0099FF ;padding:16px">
	<h2 style="color:black;text-align:center;">Well trajectory type J App - Python </h2>
	</div>
	"""

st.markdown(html_temp, unsafe_allow_html=True)
st.sidebar.title('Pozo tipo J')

# Parámetros en slidebar
def parametros_perforacion():
	BUR = st.sidebar.slider('Built Up Rate [/100ft]', 1.0, 10.0 , 1.5 , step = 0.1)
	TVD = st.sidebar.slider('Total vertical depth', 3000,15000 , 9000 , step=500)
	KOP = st.sidebar.slider('Kickoff Point (KOP)',1000,10000,2000, step= 100)
	desplazamiento_horizontal = st.sidebar.slider('Desplazamiento horizontal',0,10000,3000, step= 100)

	BUR =round(BUR,2)
	TVD =round(TVD,2)
	KOP =round(KOP,2)
	desplazamiento_horizontal=round(desplazamiento_horizontal,2)

	data_inicial=	{'Built Up Rate':BUR,
					 'Total vertical depth':TVD,
					 'Kick Off Point':KOP,
			 		 'Desp. Horizontal':desplazamiento_horizontal}
		

	parametros_iniciales = pd.DataFrame(data_inicial, index=['-'])
	return parametros_iniciales

df_parametros = parametros_perforacion()
st.subheader('Parámetros de perforación')
st.write(df_parametros)

st.sidebar.markdown('Ing. Carlos Carrillo Villavicencio')
st.sidebar.markdown('Version App: 0.1')

check_diagrama = st.checkbox('Diagrama de construcción', value=False, key=None)
if check_diagrama==True:
	st.image(image1, caption='Diagrama de construcción de pozo tipo J',
		          use_column_width=True)

var_bur =df_parametros.loc['-' ,'Built Up Rate']
var_tvd =df_parametros.loc['-' ,'Total vertical depth']
var_kop=df_parametros.loc['-' ,'Kick Off Point']
var_desplazamiento_horizontal =df_parametros.loc['-' ,'Desp. Horizontal']

radio = (18000/(3.141593 *var_bur))
hipotenusa = (((var_desplazamiento_horizontal-radio)**2)+((var_tvd-var_kop)**2))**0.5
angulo_teta=math.degrees(math.atan((var_desplazamiento_horizontal-radio)/(var_tvd-var_kop)))
angulo_beta = math.degrees(math.acos(radio/hipotenusa))
angulo_alfa = 90-(angulo_beta-angulo_teta)
inclinacion = angulo_alfa


radio_df = str(round(radio, 2))
hipotenusa_df = str(round(hipotenusa, 2))
angulo_teta_df = str(round(angulo_teta,2))
angulo_beta_df =str(round(angulo_beta,2))
angulo_alfa_df =str(round(angulo_alfa,2))
inclinacion_df = str(round(inclinacion,2))

data_calculos = {'Radio':radio_df,
				 'Hipotenusa':hipotenusa_df,
				 'Ángulo theta':angulo_teta_df,
				 'Ángulo beta': angulo_beta_df,
				 'Ángulo alfa': angulo_alfa_df,
				 'Inclinación':inclinacion_df}

calculos_iniciales = pd.DataFrame(data_calculos, index=['-'])

check_calculos_trigonometricos= st.checkbox('Cálculos trigonométricos', value=False, key=None)
if check_calculos_trigonometricos==True:
	st.write(calculos_iniciales)

x_cuerda= (radio-(radio*math.cos(math.radians(inclinacion))))
y_cuerda = (radio*math.sin(math.radians(inclinacion)))
desplazamintox_eob = var_desplazamiento_horizontal-x_cuerda
desplazamintoy_eob = var_tvd - var_kop - y_cuerda

x_cuerda_df=str(round(x_cuerda,2)) 
y_cuerda_df = str(round(y_cuerda,2))
desplazamintox_eob_df = str(round(desplazamintox_eob,2))
desplazamintoy_eob_df = str(round(desplazamintoy_eob,2))

data_calculos2 = {'Cuerda X':x_cuerda_df,
				  'Cuerda Y':y_cuerda_df,
				  'EOP Desp. X': desplazamintox_eob_df,
				  'EOP Desp. Y': desplazamintoy_eob_df}
				  
calculos_iniciales2 = pd.DataFrame(data_calculos2, index=['-'])

check_EOP= st.checkbox('Cálculos en EOP', value=False, key=None)
if check_EOP==True:
	st.write(calculos_iniciales2)

cuerda = (inclinacion*100)/var_bur
target_section =((hipotenusa**2)-(radio**2))**0.5
md = var_kop + cuerda + target_section

cuerda_df = str(round(cuerda,2))
target_section_df =str(round(target_section , 2))
md_df = str(round( md ,2 ))

data_calculos3 = {'Cuerda ':cuerda_df,
				  'Target section':target_section_df,
				  'MD ': md_df}
calculos_iniciales3 = pd.DataFrame(data_calculos3, index=['ft '])

check_trayentoria= st.checkbox('Cálculos de trayectoria', value=False, key=None)
if check_trayentoria==True:
	st.write(calculos_iniciales3)				  

# parte vertical
i=var_kop
ly=list(range(-i ,0))
ly=reversed(ly)
lx=[0]*i
lz=[0]*i

data_fig1 = {'Eje x':lx,
		     'Eje y':ly,
		     'Eje z':lz}

df_fig1=pd.DataFrame(data_fig1)
#st.write(df_fig1)

fig = px.line_3d(df_fig1, x="Eje z", y="Eje x", z="Eje y")
#st.write(fig)

# parte cuerda
var_inclinacion = int(inclinacion)
j = var_inclinacion +180
lista_grados =list(range(180, j))
  
lx_grados = [radio-(-radio*math.cos(math.radians(n))) for n in lista_grados]
ly_grados = [(radio*math.sin(math.radians(n))-var_kop) for n in lista_grados]
lz_grados = [0]*var_inclinacion
data_fig2 = {'Eje x':lx_grados,
			 'Eje y': ly_grados,
			 'Eje z':lz_grados}

df_fig2=pd.DataFrame(data_fig2 )
#st.write(df_fig2)

x1_m = x_cuerda
x2_m = var_desplazamiento_horizontal
y1_m = -(var_tvd - desplazamintoy_eob)
y2_m = -var_tvd

lista_pendientex = [ x1_m , x2_m]
lista_pendientey = [ y1_m , y2_m]
lista_pendientez = [0]*2

data_fig3 = {'Eje x':lista_pendientex,
			 'Eje y':lista_pendientey,
			 'Eje z':lista_pendientez}

df_fig3=pd.DataFrame(data_fig3)


df_combinacion = pd.concat([df_fig1,df_fig2,df_fig3],axis= 0)

fig = px.line_3d(df_combinacion, x="Eje z", y="Eje x", z="Eje y")
st.write(fig)
check_survey = st.checkbox('Survey', value=False, key=None)
if check_survey==True:
	st.write(df_combinacion)
