#-----------------Módulo de Pozo Tipo J ----------------------------#
import streamlit as st
import pandas as pd
import math
import plotly.express as px

def calcular_limite_kop(bur, tvd, desplazamiento_horizontal):
    """
    Calcula el valor máximo de KOP permitido en función del BUR, TVD y el desplazamiento horizontal.
    """
    # Cálculo del radio (R)
    radio = 18000 / (3.141593 * bur)
    
    # Validar si el desplazamiento es mayor al radio
    if desplazamiento_horizontal <= radio:
        return "El desplazamiento horizontal debe ser mayor al radio para evitar problemas geométricos."
    
    # Cálculo del límite máximo de KOP
    try:
        kop_max = tvd - math.sqrt((desplazamiento_horizontal - radio) ** 2)
        return max(0, round(kop_max, 2))  # El KOP no puede ser negativo
    except ValueError:
        return "No es posible calcular el KOP máximo con los parámetros actuales. Revisa BUR o Desplazamiento."

def calculos_trigonometricos(bur, tvd, kop, desplazamiento_horizontal):
    """
    Realiza los cálculos trigonométricos dependiendo de si el desplazamiento es mayor o menor al radio.
    """
    # Cálculo del radio
    radio = (18000 / (3.141593 * bur))  # Fórmula para radio

    # Determinar si desplazamiento final es mayor o menor que el radio
    if desplazamiento_horizontal > radio:
        # Caso Desplazamiento Horizontal > Radio
        hipotenusa = (((desplazamiento_horizontal - radio) ** 2) + ((tvd - kop) ** 2)) ** 0.5
        angulo_mu = math.degrees(math.atan((desplazamiento_horizontal - radio) / (tvd - kop)))
        angulo_alpha = math.degrees(math.acos(radio / hipotenusa))
        inclinacion = 90 + angulo_mu - angulo_alpha
    else:
        # Caso Desplazamiento Horizontal < Radio
        hipotenusa = (((radio - desplazamiento_horizontal) ** 2) + ((tvd - kop) ** 2)) ** 0.5
        angulo_mu = math.degrees(math.atan((radio - desplazamiento_horizontal) / (tvd - kop)))
        angulo_alpha = math.degrees(math.acos(radio / hipotenusa))
        inclinacion = 90 - angulo_mu - angulo_alpha

    return {
        "radio": round(radio, 2),
        "hipotenusa": round(hipotenusa, 2),
        "angulo_mu": round(angulo_mu, 2),
        "angulo_alpha": round(angulo_alpha, 2),
        "inclinacion": round(inclinacion, 2)
    }

def calculos_eob(inclinacion, radio, kop, tvd, desplazamiento_horizontal):
    """
    Calcula las coordenadas en el End of Build (EOB) y devuelve los valores.
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

    # Título principal de la app
    st.title('Simulación de la Trayectoria del Pozo Tipo J')

    # Ingreso de parámetros
    st.sidebar.header('Ingreso de Parámetros')
    bur = st.sidebar.number_input('Built Up Rate [/100ft]', min_value=1.0, max_value=10.0, value=1.5, step=1.0)
    tvd = st.sidebar.number_input('Total Vertical Depth', min_value=0, value=9000)
    kop = st.sidebar.number_input('Kickoff Point (KOP)', min_value=0, max_value=int(tvd), value=2000)
    desplazamiento_horizontal = st.sidebar.number_input('Desplazamiento horizontal', min_value=0, max_value=10000, value=3000, step=100)

    st.sidebar.markdown('Ing. Carlos Carrillo Villavicencio MSc.')
    st.sidebar.markdown('Version App: 3.0')

    # Calcular límite máximo de KOP
    limite_kop = calcular_limite_kop(bur, tvd, desplazamiento_horizontal)

    # Validar el KOP ingresado y mostrar advertencias si es necesario
    if isinstance(limite_kop, str):
        st.error(limite_kop)
        return
    elif kop > limite_kop:
        st.warning(f"El KOP ingresado ({kop}) excede el límite permitido ({limite_kop}). Ajusta los parámetros.")

    # Mostramos los parámetros ingresados
    with st.expander('Variables ingresadas'):
        st.write(f'Built Up Rate: {bur}')
        st.write(f'Total Vertical Depth: {tvd}')
        st.write(f'Kickoff Point (KOP): {kop}')
        st.write(f'Desplazamiento horizontal: {desplazamiento_horizontal}')
        st.write(f'Límite máximo de KOP permitido: {limite_kop}')

    # Mostramos el diagrama de construcción
    with st.expander('Diagrama de construcción'):
        st.image(image1, caption='Diagrama de construcción de pozo tipo J', use_column_width=True)

    # Cálculos trigonométricos
    resultados_trigonométricos = calculos_trigonometricos(bur, tvd, kop, desplazamiento_horizontal)

    with st.expander('Cálculos trigonométricos'):
        st.write(f"Radio: {resultados_trigonométricos['radio']}")
        st.write(f"Hipotenusa: {resultados_trigonométricos['hipotenusa']}")
        st.write(f"Ángulo Mu: {resultados_trigonométricos['angulo_mu']}")
        st.write(f"Ángulo Alpha: {resultados_trigonométricos['angulo_alpha']}")
        st.write(f"Inclinación: {resultados_trigonométricos['inclinacion']}")

    # Cálculos en EOP
    resultados_eob = calculos_eob(
        resultados_trigonométricos['inclinacion'],
        resultados_trigonométricos['radio'],
        kop,
        tvd,
        desplazamiento_horizontal
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

