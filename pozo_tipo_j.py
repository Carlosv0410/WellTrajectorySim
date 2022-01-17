import streamlit as st
import pandas as pd
import math 
import plotly.express as px

def construccion(image1):

	#----------------Ingreso de parametros y verifiación------------------------------#
	st.sidebar.header('Ingreso de Parámetros')

	

	BUR = st.sidebar.number_input('Built Up Rate [/100ft]', min_value = 1.0, max_value = 10.0, value = 1.5, step = 1.0)
	TVD = st.sidebar.number_input('Total vertical depth', min_value = 0, max_value = None, value = 9000 )	
	KOP = st.sidebar.number_input('Kickoff Point (KOP)',min_value = 0, max_value = int(TVD), value = 2000 )
	desplazamiento_horizontal = st.sidebar.number_input('Desplazamiento horizontal', min_value = 0, max_value = 10000, value = 3000, step = 100)
	
	st.sidebar.markdown('Ing. Carlos Carrillo Villavicencio MSc.')
	st.sidebar.markdown('Version App: 2.0')

	with st.expander('Variables ingresadas'):
		st.write('Built Up Rate: {}'.format(BUR))
		st.write('Total vertical depth: {}'.format(TVD))
		st.write('Kickoff Point (KOP): {}'.format(KOP))
		st.write('Desplazamiento horizontal: {}'.format(desplazamiento_horizontal))



	#----------------Ingreso de parametros y verifiación------------------------------#

	with st.expander('Diagrama de construcción'):
		st.image(image1, caption='Diagrama de construcción de pozo tipo J',
			          use_column_width=True)

	
	var_bur = BUR
	var_tvd = TVD
	var_kop= KOP
	var_desplazamiento_horizontal =desplazamiento_horizontal

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


	
	with st.expander('Cálculos trigonométricos'):
		st.write('Radio: {}'.format(radio_df))
		st.write('Hipotenusa: {}'.format(hipotenusa_df))
		st.write('Ángulo theta: {}'.format(angulo_teta_df))
		st.write('Ángulo beta: {}'.format(angulo_beta_df))
		st.write('Ángulo alfa: {}'.format(angulo_alfa_df))
		st.write('Inclinación: {}'.format(inclinacion_df))




	x_cuerda= (radio-(radio*math.cos(math.radians(inclinacion))))
	y_cuerda = (radio*math.sin(math.radians(inclinacion)))
	desplazamintox_eob = var_desplazamiento_horizontal-x_cuerda
	desplazamintoy_eob = var_tvd - var_kop - y_cuerda

	x_cuerda_df=str(round(x_cuerda,2)) 
	y_cuerda_df = str(round(y_cuerda,2))
	desplazamintox_eob_df = str(round(desplazamintox_eob,2))
	desplazamintoy_eob_df = str(round(desplazamintoy_eob,2))



	with st.expander('Cálculos en EOP'):
		st.write('Cuerda X: {}'.format(x_cuerda_df))
		st.write('Cuerda Y: {}'.format(y_cuerda_df))
		st.write('EOP Desp. X: {}'.format(desplazamintox_eob_df))
		st.write('EOP Desp. Y: {}'.format(desplazamintoy_eob_df))



	cuerda = (inclinacion*100)/var_bur
	target_section =((hipotenusa**2)-(radio**2))**0.5
	md = var_kop + cuerda + target_section

	cuerda_df = str(round(cuerda,2))
	target_section_df =str(round(target_section , 2))
	md_df = str(round( md ,2 ))


	with st.expander('Cálculos de trayectoria'):
		st.write('Cuerda: {}'.format(cuerda_df))
		st.write('Target section: {}'.format(target_section_df))
		st.write('MD : {}'.format(md_df))
			  

	# parte vertical
	i=int(var_kop)
	ly=list(range(-i ,0))
	ly=reversed(ly)
	lx=[0]*i
	lz=[0]*i

	data_fig1 = {'Eje x':lx,
			     'Eje y':ly,
			     'Eje z':lz}

	df_fig1=pd.DataFrame(data_fig1)
	df_fig1['Sección'] = 'Vertical'
	#st.write(df_fig1)


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
	df_fig2['Sección'] = 'Cuerda'
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
	df_fig3['Sección'] = 'Inclinación'


	df_combinacion = pd.concat([df_fig1,df_fig2,df_fig3],axis= 0)

	fig = px.line_3d(df_combinacion, x="Eje z", y="Eje x", z="Eje y", color='Sección', title = 'Diagrama de construcción')
	st.write(fig)
	with st.expander('Survey'):
		st.write(df_combinacion)