#-----------------Módulo de Pozo Vertical ----------------------------#
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Función principal para la construcción del pozo vertical
def construccion():
    """
    Función principal para construir el pozo vertical, que gestiona los inputs
    del usuario y la estructura de la interfaz. Organiza las columnas y llama
    a la función para construir el survey.
    """
    # Título de la aplicación
    st.title("Simulación de la Trayectoria del Pozo Tipo Vertical")

    # Pedimos al usuario que ingrese el número de secciones del pozo
    num_secciones = st.sidebar.number_input(
        'Número de secciones del pozo', min_value=1, max_value=10, value=1
    )

    # Pedimos al usuario que ingrese cada cuántos pies se tomará el survey
    intervalo_survey = st.sidebar.number_input(
        'Intervalo de survey (ft)', min_value=1, max_value=1000, value=100
    )

    st.sidebar.markdown('Ing. Carlos Carrillo Villavicencio MSc.')
    st.sidebar.markdown('Version App: 3.0')   
    
    # Crear cuatro columnas para organizar la interfaz
    col1, col2, col3, col4 = st.columns(4)

    # Parámetros del pozo vertical en la primera columna, sin expander
    with col1:
        st.write("Parámetros del Pozo Vertical")
        
        # Creamos un dataframe vacío para almacenar las secciones y longitudes
        secciones = pd.DataFrame(columns=['Sección', 'Longitud (ft)'])

        # Iteramos según el número de secciones para que el usuario ingrese la longitud de cada una en pies
        for i in range(num_secciones):
            longitud = st.number_input(
                f'Longitud para la sección {i+1} (ft)', 
                min_value=0, max_value=30000, value=0
            )
            secciones = secciones.append(
                {'Sección': f'Sección {i+1}', 'Longitud (ft)': longitud}, 
                ignore_index=True
            )

    # Mostramos el dataframe con las longitudes ingresadas en la segunda columna
    with col2:
        st.write("Longitudes ingresadas (en pies):")
        st.write(secciones)

    # Si el usuario ya ingresó todas las longitudes y hace clic en "Construir Survey"
    if st.button('Construir Survey'):
        construir_survey(secciones, intervalo_survey, col3, col4)


# Función para construir el survey del pozo con puntos intermedios y visualizarlo en 3D
def construir_survey(secciones, intervalo_survey, col3, col4):
    """
    Función para construir el survey del pozo basado en las longitudes de cada
    sección, generar puntos intermedios y visualizar el pozo en 3D. También 
    se muestra el survey completo en una tabla expandible.
    
    Args:
    secciones (pd.DataFrame): DataFrame con las secciones y longitudes en ft.
    intervalo_survey (int): Intervalo en pies para la toma de puntos del survey.
    col3 (st.columns): Columna para mostrar el gráfico 3D.
    col4 (st.columns): Columna para mostrar el survey completo.
    """
    # Informamos al usuario que estamos construyendo el survey
    st.write("Construyendo el Survey del pozo...")

    # Asignamos los ejes ficticios para un pozo vertical
    secciones['Eje x'] = 0  # No hay desplazamiento en el eje x
    secciones['Eje y'] = 0  # No hay desplazamiento en el eje y

    # Calculamos la longitud acumulada (MD = measured depth) en pies y multiplicamos por -1 para el eje Z
    secciones['Eje z'] = -1 * secciones['Longitud (ft)'].cumsum()

    # Generamos puntos intermedios cada 'intervalo_survey' pies
    puntos_survey = []
    for i in range(len(secciones)):
        inicio = 0 if i == 0 else secciones['Eje z'].iloc[i-1]
        fin = secciones['Eje z'].iloc[i]
        # Creamos los puntos entre el inicio y el fin de cada sección
        puntos_intermedios = np.arange(inicio, fin, -intervalo_survey)
        for punto in puntos_intermedios:
            puntos_survey.append({
                'Sección': secciones['Sección'].iloc[i], 
                'Eje x': 0, 
                'Eje y': 0, 
                'Eje z': punto
            })

    # Convertimos los puntos intermedios en un dataframe para graficar
    df_puntos_survey = pd.DataFrame(puntos_survey)
    
    # Plotear el survey en 3D con Plotly Express en la tercera columna
    with col3:
        fig = px.line_3d(
            df_puntos_survey, x="Eje x", y="Eje y", z="Eje z", 
            color='Sección', title='Diagrama de construcción del Pozo Vertical'
        )
        st.write(fig)

    # Mostrar el survey completo en una cuarta columna, dentro de un expander
    with col4:
        with st.expander('Survey Completo'):
            st.write(df_puntos_survey)
