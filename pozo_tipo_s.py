import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd



# Definir función principal para construir el pozo tipo S
def construccion():

    # Explicación en markdown sobre la naturaleza simplificada del simulador
    st.markdown(r"""
    # Simulador de Trayectoria de Pozo Tipo S
    
    Si bien la simulación de un pozo tipo S es más que un ejercicio teórico de cálculos y fórmulas, y existen softwares industriales más sofisticados para este propósito, 
    hemos creado un breve simulador en Python que permite ajustar los parámetros principales y obtener una representación gráfica de la trayectoria. 
    Este simulador busca ayudar a visualizar cómo varían las secciones del pozo cuando se modifican las tasas de incremento y disminución de curvatura, 
    así como otros parámetros, pero **no pretende calcular automáticamente todas las variaciones posibles de forma exacta**.
    
    """)

    # Título principal de la app
    st.title('Simulación de la Trayectoria del Pozo Tipo S')

    # Mostrar teoría y fórmulas con LaTeX en la aplicación
    st.header('Teoría y Fórmulas de la Simulación')

    # Explicación de la teoría en Markdown con soporte para LaTeX
    st.markdown(r"""
        ### Trayectoria de un Pozo Tipo S
        La trayectoria de un pozo tipo S se caracteriza por tener diferentes secciones, incluyendo una sección vertical inicial,
        una sección de incremento de inclinación, una sección tangencial, una sección de disminución de inclinación y una sección vertical final.

        #### 1. Fórmulas de Curvatura
        - Tasa de Incremento de Curvatura (BUR): \( BUR \) en grados por cada 100 ft.
        - Tasa de Disminución de Curvatura (DOR): \( DOR \) en grados por cada 100 ft.
        - El radio de curvatura se calcula como:

        $$ 
        r_1 = \frac{180}{\pi \cdot \frac{BUR}{100}} \quad \text{y} \quad r_2 = \frac{180}{\pi \cdot \frac{DOR}{100}} 
        $$

        #### 2. Cálculo del Ángulo de Inclinación (\( \theta \))
        El ángulo de inclinación se calcula de la siguiente manera:

        $$
        \theta = \arctan \left( \frac{D_4 - KOP}{r_1 + r_2 - x_4} \right) - \arccos \left( \frac{r_1 + r_2}{D_4 - KOP} \cdot \sin(\theta) \right)
        $$

        Si \( r_1 + r_2 > x_4 \), usamos una fórmula alternativa para \( \theta \).

        #### 3. Cálculo de la Profundidad y Desplazamiento Horizontal
        - La profundidad medida en la sección de incremento se calcula como:

        $$
        MD_2 = KOP + L_1 \quad \text{donde} \quad L_1 = \theta \cdot r_1
        $$

        - El desplazamiento horizontal al final de la sección de incremento es:

        $$
        x_2 = r_1 \cdot (1 - \cos(\theta))
        $$

        Estas fórmulas permiten modelar la trayectoria del pozo tipo S en función de los parámetros dados.
    """)

    # ----- Inputs en la barra lateral -----
    st.sidebar.header("Parámetros de Entrada")

    # Input: Tasa de Incremento (BUR) en grados por cada 100 pies
    BUR = st.sidebar.number_input(
        'Tasa de Incremento (BUR) en grados por cada 100 ft', 
        min_value=0.1, max_value=10.0, value=3.0, step=0.1
    )

    # Input: Tasa de Disminución (DOR) en grados por cada 100 pies
    DOR = st.sidebar.number_input(
        'Tasa de Disminución (DOR) en grados por cada 100 ft', 
        min_value=0.1, max_value=10.0, value=2.5, step=0.1
    )

    # Input: Profundidad del Kick-Off Point (KOP) en pies
    KOP = st.sidebar.number_input(
        'Profundidad del Kick-Off Point (KOP) en ft', 
        min_value=1, max_value=20000, value=2100, step=100
    )

    # Input: Profundidad vertical al final de la sección tangencial (D3)
    D3 = st.sidebar.number_input(
        'Profundidad vertical verdadera al final de la sección tangencial (D3) en ft', 
        min_value=1, max_value=20000, value=6900, step=100
    )

    # Input: Profundidad vertical al final de la sección de disminución (D4)
    D4 = st.sidebar.number_input(
        'Profundidad vertical verdadera al final de la sección de disminución (D4) en ft', 
        min_value=1, max_value=20000, value=8000, step=100
    )

    # Input: Profundidad total vertical (TVD) en pies
    TVD = st.sidebar.number_input(
        'Profundidad total vertical (TVD) en ft', 
        min_value=1, max_value=20000, value=9300, step=100
    )

    # Input: Desplazamiento horizontal al objetivo (x4) en pies
    x4 = st.sidebar.number_input(
        'Desplazamiento horizontal al objetivo (x4) en ft', 
        min_value=1.0, max_value=5000.0, value=2600.0, step=10.0
    )

    st.sidebar.markdown('Ing. Carlos Carrillo Villavicencio MSc.')
    st.sidebar.markdown('Version App: 3.0')

    # ----- Validaciones -----
    # Asegurarse de que D3 < D4 < TVD
    if D3 >= D4:
        st.error('D3 debe ser menor que D4.')
    elif D4 >= TVD:
        st.error('D4 debe ser menor que TVD.')
    else:
        # Si los inputs son válidos, proceder con los cálculos

        # Constante para convertir grados a radianes (usada en las fórmulas trigonométricas)
        deg_to_rad = np.pi / 180

        # Paso 1: Cálculo de los radios de curvatura
        r1 = 180 / (np.pi * BUR / 100)  # Radio de curvatura en la sección de incremento
        r2 = 180 / (np.pi * DOR / 100)  # Radio de curvatura en la sección de disminución

        # Paso 2: Cálculo del ángulo de inclinación theta (en radianes)
        if r1 + r2 > x4:
            # Cálculo si el radio total de curvatura es mayor que el desplazamiento x4
            term1 = np.arctan((D4 - KOP) / (r1 + r2 - x4))
            term2 = np.arccos((r1 + r2) / (D4 - KOP) * np.sin(term1))
            theta = term1 - term2
        else:
            # Cálculo alternativo si el radio total de curvatura es menor que x4
            term1 = np.arctan((D4 - KOP) / (x4 - (r1 + r2)))
            term2 = np.arccos((r1 + r2) / (D4 - KOP) * np.sin(term1))
            theta = np.pi - term1 - term2  # El ángulo theta en radianes

        # Convertir el ángulo theta a grados para reportar resultados más fácilmente
        theta_deg = np.degrees(theta)

        # ----- Cálculo de profundidades y desplazamientos -----
        D1 = 0  # La profundidad inicial es siempre 0 (superficie)
        D2 = KOP + (r1 * np.sin(theta))  # Profundidad al final de la sección de incremento
        D5 = TVD  # Profundidad total (TVD)

        # Longitud de la curva en la sección de incremento
        L1 = theta * r1

        # Profundidad medida al final de la sección de incremento
        MD2 = KOP + L1

        # Desplazamientos horizontales
        x1 = 0  # No hay desplazamiento horizontal en la superficie
        x2 = r1 * (1 - np.cos(theta))  # Desplazamiento al final de la sección de incremento
        MD3 = MD2 + (D3 - D2) / np.cos(theta)  # Profundidad medida en D3

        # Desplazamiento horizontal al final de la sección tangencial
        x3 = x2 + (D3 - D2) * np.tan(theta)

        # ----- Crear DataFrame con todos los puntos para los gráficos -----
        # Sección de incremento: curva
        theta_values = np.linspace(0, theta, 100)  # Valores de ángulo en la sección de incremento
        x_increment = r1 * (1 - np.cos(theta_values))  # Desplazamientos horizontales en incremento
        y_increment = -KOP - r1 * np.sin(theta_values)  # Profundidades en la sección de incremento

        # Sección tangencial: recta
        x_tangential = np.linspace(x2, x3, 100)  # Desplazamientos horizontales en la sección tangencial
        y_tangential = np.linspace(-D2, -D3, 100)  # Profundidades en la sección tangencial

        # Sección de disminución: curva
        points_drop = 100
        theta_delta = theta / points_drop  # Incremento angular por cada punto
        theta_values_decrease = theta - (theta_delta * (np.arange(points_drop) + 1))  # Ángulos decrecientes en disminución

        # Cálculos de desplazamiento horizontal y vertical en la sección de disminución
        y_checkpoint = -D3
        x_checkpoint = x3
        y_decrease = r2 * (np.sin(theta) - np.sin(theta_values_decrease))  # Desplazamiento vertical
        x_decrease = r2 * (1 - np.cos(theta)) - r2 * (1 - np.cos(theta_values_decrease))  # Desplazamiento horizontal

        # Ajustes de coordenadas
        x_decrease = x_checkpoint + x_decrease
        y_decrease = y_checkpoint - y_decrease

        # Sección final (vertical): No hay desplazamiento horizontal
        x_final = np.full(100, x4)
        y_final = np.linspace(-D4, -TVD, 100)  # La profundidad llega hasta el TVD

        # Concatenar todos los puntos de las diferentes secciones
        x_total = np.concatenate([x_increment, x_tangential, x_decrease, x_final])
        z_total = np.concatenate([y_increment, y_tangential, y_decrease, y_final])

        # Crear columna de colores para identificar secciones en los gráficos
        colors = np.concatenate([np.full(len(x_increment), 'Incremento'),
                                np.full(len(x_tangential), 'Tangencial'),
                                np.full(len(x_decrease), 'Disminución'),
                                np.full(len(x_final), 'Vertical Final')])

        # Crear columna Y para los gráficos 3D
        y_total = np.zeros_like(x_total)

        # Crear DataFrame final con todas las coordenadas calculadas
        data = pd.DataFrame({'x': x_total, 'y': y_total, 'z': z_total, 'Sección': colors})

        # ----- Mostrar los resultados calculados -----
        with st.expander("Resultados calculados"):
            # Mostrar resultados calculados de profundidades y desplazamientos
            st.write(f"Profundidades (D1 a D5): D1 = {D1} ft, D2 = {D2:.2f} ft, D3 = {D3} ft, D4 = {D4} ft, D5 = {D5} ft")
            st.write(f"Desplazamientos horizontales (x1 a x4): x1 = {x1} ft, x2 = {x2:.2f} ft, x3 = {x3:.2f} ft, x4 = {x4} ft")
            st.write(f"Radio de Curvatura en Incremento (r1): {r1:.2f} ft")
            st.write(f"Radio de Curvatura en Disminución (r2): {r2:.2f} ft")
            st.write(f"Ángulo de Inclinación (theta): {theta_deg:.2f} grados")

        # ----- Mostrar los gráficos en dos columnas -----
        col1, col2 = st.columns(2)

        # Gráfico 2D de la trayectoria
        with col1:
            st.subheader('Trayectoria del Pozo en 2D')
            fig_2d = px.line(data, x="x", y="z", color="Sección", title="Trayectoria del Pozo Tipo S en 2D", 
                            labels={"x": "Desplazamiento Horizontal (ft)", "z": "Profundidad Vertical (ft)"})
            st.plotly_chart(fig_2d)

        # Gráfico 3D de la trayectoria
        with col2:
            st.subheader('Trayectoria del Pozo en 3D')
            fig_3d = px.line_3d(data, x="x", y="y", z="z", color="Sección", title="Trayectoria del Pozo Tipo S en 3D", 
                                labels={"x": "Desplazamiento Horizontal (ft)", "y": "Eje Y (ft)", "z": "Profundidad Vertical (ft)"})
            st.plotly_chart(fig_3d)





