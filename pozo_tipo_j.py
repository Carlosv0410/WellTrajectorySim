#-----------------Módulo de Pozo Tipo J ----------------------------#
import streamlit as st
import pandas as pd
import math
import plotly.express as px

def calculos_trigonometricos(bur, tvd, kop, desplazamiento_horizontal):
    """
    Realiza los cálculos trigonométricos necesarios para la construcción
    del pozo tipo J y maneja los dos escenarios posibles.
    """
    try:
        # Condicionante: KOP no puede ser mayor que el TVD
        if kop >= tvd:
            raise ValueError("El Kickoff Point (KOP) no puede ser mayor o igual al Total Vertical Depth (TVD).")

        # Radio de curvatura
        radio = (18000 / (3.141593 * bur))

        # Determinar la hipotenusa considerando los dos escenarios
        if desplazamiento_horizontal > radio:
            desplazamiento_ajustado = desplazamiento_horizontal - radio
        else:
            desplazamiento_ajustado = radio - desplazamiento_horizontal

        # Línea de profundidad vertical desde el KOP al TVD
        profundidad_vertical = tvd - kop

        # Calcular el ángulo theta (triángulo formado por desplazamiento y profundidad)
        angulo_teta = math.degrees(math.atan(desplazamiento_ajustado / profundidad_vertical))

        # Longitud de la hipotenusa
        hipotenusa = (desplazamiento_ajustado**2 + profundidad_vertical**2) ** 0.5

        # Validación del rango para el coseno en math.acos
        cos_value = radio / hipotenusa
        cos_value = max(-1, min(1, cos_value))  # Asegurar que esté entre -1 y 1

        # Calcular el ángulo beta
        angulo_beta = math.degrees(math.acos(cos_value))

        # Calcular el ángulo alfa
        angulo_alfa = 90 - (angulo_beta - angulo_teta)

        # Máxima inclinación
        inclinacion = angulo_alfa

        return {
            "radio": round(radio, 2),
            "hipotenusa": round(hipotenusa, 2),
            "angulo_teta": round(angulo_teta, 2),
            "angulo_beta": round(angulo_beta, 2),
            "angulo_alfa": round(angulo_alfa, 2),
            "inclinacion": round(inclinacion, 2)
        }
    except Exception as e:
        # Mostrar advertencia y retornar valores predeterminados
        st.warning(f"Error en los cálculos: {str(e)}. Mostrando construcción con valores predeterminados.")
        return {
            "radio": 1000,
            "hipotenusa": 1200,
            "angulo_teta": 45,
            "angulo_beta": 45,
            "angulo_alfa": 45,
            "inclinacion": 45
        }

def construccion(image1):
    # Título principal de la app
    st.title('Simulación de la Trayectoria del Pozo Tipo J')

    # Mensaje informativo sobre BUR y KOP
    st.write("""
        **Información Importante**:
        - El Kickoff Point (KOP) no puede ser mayor o igual al Total Vertical Depth (TVD).
        - Si desea que el Kickoff Point (KOP) esté más cerca del TVD, incremente el Built Up Rate (BUR).
        - Un BUR más alto permite que el pozo se desvíe más rápidamente, reduciendo la distancia
          entre el KOP y el TVD. Sin embargo, también puede aumentar los esfuerzos en la sarta de perforación
          y los riesgos operativos.
    """)

    # Ingreso de parámetros
    st.sidebar.header('Ingreso de Parámetros')
    bur = st.sidebar.number_input('Built Up Rate [/100ft]', min_value=1.0, max_value=10.0, value=1.5, step=1.0)
    tvd = st.sidebar.number_input('Total Vertical Depth', min_value=0, value=9000)
    kop = st.sidebar.number_input('Kickoff Point (KOP)', min_value=0, max_value=int(tvd), value=2000)
    desplazamiento_horizontal = st.sidebar.number_input('Desplazamiento horizontal', min_value=0, max_value=10000, value=3000, step=100)
    
    st.sidebar.markdown('Ing. Carlos Carrillo Villavicencio MSc.')
    st.sidebar.markdown('Version App: 3.0')

    # Mostramos los parámetros ingresados
    with st.expander('Variables ingresadas'):
        st.write(f'Built Up Rate: {bur}')
        st.write(f'Total Vertical Depth: {tvd}')
        st.write(f'Kickoff Point (KOP): {kop}')
        st.write(f'Desplazamiento horizontal: {desplazamiento_horizontal}')

    # Realizamos cálculos trigonométricos
    resultados_trigonométricos = calculos_trigonometricos(bur, tvd, kop, desplazamiento_horizontal)

    # Generamos gráfica básica
    radio = resultados_trigonométricos['radio']
    inclinacion = resultados_trigonométricos['inclinacion']

    # Construcción vertical
    vertical_depth = list(range(-int(kop), 0))
    df_vertical = pd.DataFrame({
        'Eje x': [0] * len(vertical_depth),
        'Eje y': vertical_depth,
        'Eje z': [0] * len(vertical_depth),
        'Sección': ['Vertical'] * len(vertical_depth)
    })

    # Curva
    df_curva = pd.DataFrame({
        'Eje x': [math.sin(math.radians(angle)) * radio for angle in range(0, int(inclinacion))],
        'Eje y': [math.cos(math.radians(angle)) * radio for angle in range(0, int(inclinacion))],
        'Eje z': [0] * int(inclinacion),
        'Sección': ['Curva'] * int(inclinacion)
    })

    # Combinar datos
    df_combinacion = pd.concat([df_vertical, df_curva])

    # Gráfico 3D
    fig = px.line_3d(df_combinacion, x='Eje z', y='Eje x', z='Eje y', color='Sección')
    st.write(fig)

# Ejecuta la construcción del pozo tipo J
construccion(None)

