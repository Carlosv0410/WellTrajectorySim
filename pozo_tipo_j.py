# -----------------Módulo de Pozo Tipo J ----------------------------#
import streamlit as st
import pandas as pd
import math
import plotly.express as px

def calculos_trigonometricos(bur, tvd, kop, desplazamiento_horizontal):
    """
    Realiza los cálculos trigonométricos necesarios para la construcción de un pozo tipo J, 
    considerando si el desplazamiento horizontal es mayor o menor que el radio de curvatura.

    Incluye manejo de errores cuando los parámetros no son físicamente consistentes.

    Parámetros:
    ----------
    bur : float
        Build-Up Rate (BUR) en grados por cada 100 ft.
    tvd : float
        True Vertical Depth (TVD) en pies.
    kop : float
        Kick-Off Point (KOP) en pies.
    desplazamiento_horizontal : float
        Desplazamiento horizontal del pozo en pies.

    Retorna:
    --------
    dict:
        Un diccionario con los resultados calculados (o None si ocurre un error).
    """
    # Cálculo del radio de curvatura
    radio = (180 * 100) / (3.141593 * bur)

    # Determinar si desplazamiento horizontal es mayor o menor que el radio
    try:
        if desplazamiento_horizontal > radio:
            # Caso Desplazamiento Horizontal > Radio
            hipotenusa = (((desplazamiento_horizontal - radio) ** 2) + ((tvd - kop) ** 2)) ** 0.5
            # Validación previa a acos
            if radio / hipotenusa > 1 or radio / hipotenusa < -1:
                st.error("Parámetros no válidos. Por favor, incremente el BUR o ajuste los valores ingresados.")
                return None
            angulo_teta = math.degrees(math.atan((desplazamiento_horizontal - radio) / (tvd - kop)))
            angulo_beta = math.degrees(math.acos(radio / hipotenusa))
            angulo_alfa = 90 + angulo_teta - angulo_beta
        else:
            # Caso Desplazamiento Horizontal < Radio
            hipotenusa = (((radio - desplazamiento_horizontal) ** 2) + ((tvd - kop) ** 2)) ** 0.5
            # Validación previa a acos
            if radio / hipotenusa > 1 or radio / hipotenusa < -1:
                st.error("Parámetros no válidos. Por favor, incremente el BUR o ajuste los valores ingresados.")
                return None
            angulo_teta = math.degrees(math.atan((radio - desplazamiento_horizontal) / (tvd - kop)))
            angulo_beta = math.degrees(math.acos(radio / hipotenusa))
            angulo_alfa = 90 - angulo_teta - angulo_beta

        # Asignar inclinación basada en el cálculo de angulo alfa
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
        st.error(f"Error en los cálculos: {e}")
        return None

def calculos_eob(inclinacion, radio, kop, tvd, desplazamiento_horizontal):
    """
    Calcula las coordenadas en el End of Build (EOB) y devuelve los valores.

    Parámetros:
    ----------
    inclinacion : float
        Ángulo de inclinación final en grados.
    radio : float
        Radio de curvatura del pozo en pies.
    kop : float
        Kick-Off Point (KOP) en pies.
    tvd : float
        True Vertical Depth (TVD) en pies.
    desplazamiento_horizontal : float
        Desplazamiento horizontal del pozo en pies.

    Cálculos:
    ---------
    - Coordenada X de la cuerda: `radio - (radio * cos(inclinación))`.
    - Coordenada Y de la cuerda: `radio * sin(inclinación)`.
    - Desplazamiento horizontal en EOB.
    - Desplazamiento vertical en EOB.

    Retorna:
    --------
    dict:
        Un diccionario con las coordenadas y desplazamientos calculados:
        - "x_cuerda": float, coordenada X de la cuerda (pies).
        - "y_cuerda": float, coordenada Y de la cuerda (pies).
        - "desplazamiento_x_eob": float, desplazamiento horizontal en el EOB (pies).
        - "desplazamiento_y_eob": float, desplazamiento vertical en el EOB (pies).

    """
    x_cuerda = (radio - (radio * math.cos(math.radians(inclinacion))))
    y_cuerda = (radio * math.sin(math.radians(inclinacion)))
    desplazamiento_x_eob = desplazamiento_horizontal - x_cuerda
    desplazamiento_y_eob = tvd - kop - y_cuerda
    
    return {
        "x_cuerda": round(x_cuerda, 2),
        "y_cuerda": round(y_cuerda, 2),
        "desplazamiento_x_eob": round(desplazamiento_x_eob, 2),
        "desplazamiento_y_eob": round(desplazamiento_y_eob, 2)
    }

def calculos_trayectoria(inclinacion, bur, hipotenusa, radio, kop):
    """
    Realiza los cálculos de trayectoria del pozo y devuelve los resultados.

    Parámetros:
    ----------
    inclinacion : float
        Ángulo de inclinación final en grados.
    bur : float
        Build-Up Rate (BUR) en grados por cada 100 ft.
    hipotenusa : float
        Distancia entre el KOP y el objetivo en pies.
    radio : float
        Radio de curvatura del pozo en pies.
    kop : float
        Kick-Off Point (KOP) en pies.

    Cálculos:
    ---------
    - Longitud de la cuerda: `(inclinación * 100) / BUR`.
    - Longitud de la sección objetivo: `sqrt(hipotenusa² - radio²)`.
    - Longitud medida total (MD): `KOP + cuerda + sección objetivo`.

    Retorna:
    --------
    dict:
        Un diccionario con los resultados de la trayectoria:
        - "cuerda": float, longitud de la cuerda (pies).
        - "target_section": float, longitud de la sección objetivo (pies).
        - "md": float, longitud medida total (MD, en pies).

    """
    cuerda = (inclinacion * 100) / bur
    target_section = ((hipotenusa ** 2) - (radio ** 2)) ** 0.5
    md = kop + cuerda + target_section
    
    return {
        "cuerda": round(cuerda, 2),
        "target_section": round(target_section, 2),
        "md": round(md, 2)
    }

def construccion(image1):
    """
    Simula la construcción de la trayectoria de un pozo tipo J, mostrando resultados,
    gráficos 3D y survey, además de permitir el ingreso de parámetros desde la interfaz.

    Parámetros:
    ----------
    image1 : str
        Ruta de la imagen del diagrama de construcción del pozo tipo J.

    Retorna:
    --------
    None:
        Esta función utiliza la biblioteca Streamlit para mostrar resultados en una aplicación web.
    """
    # Título principal de la app
    st.title('Simulación de la Trayectoria del Pozo Tipo J')

    # Ingreso de parámetros
    st.sidebar.header('Ingreso de Parámetros')
    bur = st.sidebar.number_input('Built Up Rate [/100ft]', min_value=1.0, max_value=10.0, value=1.5, step=1.0)
    tvd = st.sidebar.number_input('Total Vertical Depth', min_value=0, value=9000)
    kop = st.sidebar.number_input('Kickoff Point (KOP)', min_value=0, max_value=int(tvd), value=2000)
    desplazamiento_horizontal = st.sidebar.number_input('Desplazamiento horizontal', min_value=0, max_value=10000, value=3000, step=100)

    st.sidebar.markdown('Ing. Carlos Carrillo Villavicencio MSc.')
    st.sidebar.markdown('Versión App: 3.0')

    # Mostramos los parámetros ingresados
    with st.expander('Variables ingresadas'):
        st.write(f'Built Up Rate: {bur}')
        st.write(f'Total Vertical Depth: {tvd}')
        st.write(f'Kickoff Point (KOP): {kop}')
        st.write(f'Desplazamiento horizontal: {desplazamiento_horizontal}')

    # Mostramos el diagrama de construcción
    with st.expander('Diagrama de construcción'):
        st.image(image1, caption='Diagrama de construcción de pozo tipo J', use_column_width=True)

    # Cálculos trigonométricos
    resultados_trigonométricos = calculos_trigonometricos(bur, tvd, kop, desplazamiento_horizontal)
    
    with st.expander('Cálculos trigonométricos'):
        st.write(f"Radio: {resultados_trigonométricos['radio']}")
        st.write(f"Hipotenusa: {resultados_trigonométricos['hipotenusa']}")
        st.write(f"Ángulo theta: {resultados_trigonométricos['angulo_teta']}")
        st.write(f"Ángulo beta: {resultados_trigonométricos['angulo_beta']}")
        st.write(f"Ángulo alfa: {resultados_trigonométricos['angulo_alfa']}")
        st.write(f"Inclinación: {resultados_trigonométricos['inclinacion']}")

    # Cálculos en EOP
    resultados_eob = calculos_eob(
        resultados_trigonométricos['inclinacion'], 
        resultados_trigonométricos['radio'], 
        kop, tvd, desplazamiento_horizontal
    )
    
    with st.expander('Cálculos en EOP'):
        st.write(f"Cuerda X: {resultados_eob['x_cuerda']}")
        st.write(f"Cuerda Y: {resultados_eob['y_cuerda']}")
        st.write(f"EOP Desp. X: {resultados_eob['desplazamiento_x_eob']}")
        st.write(f"EOP Desp. Y: {resultados_eob['desplazamiento_y_eob']}")

    # Cálculos de trayectoria
    resultados_trayectoria = calculos_trayectoria(
        resultados_trigonométricos['inclinacion'],
        bur,
        resultados_trigonométricos['hipotenusa'],
        resultados_trigonométricos['radio'],
        kop
    )

    with st.expander('Cálculos de trayectoria'):
        st.write(f"Cuerda: {resultados_trayectoria['cuerda']}")
        st.write(f"Target Section: {resultados_trayectoria['target_section']}")
        st.write(f"MD: {resultados_trayectoria['md']}")

    # Gráfico 3D de la trayectoria
    # Parte vertical
    i = int(kop)
    ly = list(reversed(range(-i, 0)))
    lx = [0] * i
    lz = [0] * i
    df_fig1 = pd.DataFrame({'Eje x': lx, 'Eje y': ly, 'Eje z': lz})
    df_fig1['Sección'] = 'Vertical'

    # Parte cuerda
    inclinacion = int(resultados_trigonométricos['inclinacion'])
    j = inclinacion + 180
    lista_grados = list(range(180, j))
    lx_grados = [resultados_trigonométricos['radio'] - (-resultados_trigonométricos['radio'] * math.cos(math.radians(n))) for n in lista_grados]
    ly_grados = [(resultados_trigonométricos['radio'] * math.sin(math.radians(n)) - kop) for n in lista_grados]
    lz_grados = [0] * inclinacion
    df_fig2 = pd.DataFrame({'Eje x': lx_grados, 'Eje y': ly_grados, 'Eje z': lz_grados})
    df_fig2['Sección'] = 'Cuerda'

    # Inclinación
    x1_m = resultados_eob['x_cuerda']
    x2_m = desplazamiento_horizontal
    y1_m = -(tvd - resultados_eob['desplazamiento_y_eob'])
    y2_m = -tvd
    df_fig3 = pd.DataFrame({'Eje x': [x1_m, x2_m], 'Eje y': [y1_m, y2_m], 'Eje z': [0, 0]})
    df_fig3['Sección'] = 'Inclinación'

    # Combinamos todas las partes
    df_combinacion = pd.concat([df_fig1, df_fig2, df_fig3], axis=0)

    # Colocamos el diagrama y el survey en dos columnas
    col1, col2 = st.columns(2)

    # Diagrama en 3D en la primera columna
    with col1:
        fig = px.line_3d(df_combinacion, x="Eje z", y="Eje x", z="Eje y", color='Sección', title='Diagrama de construcción')
        st.write(fig)

    # Survey en la segunda columna
    with col2:
        with st.expander('Survey Completo'):
            st.write(df_combinacion)
