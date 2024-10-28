
# Well Trajectory Simulator 🚀

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen)
![PRs](https://img.shields.io/badge/PRs-Welcome-orange)

**Well Trajectory Simulator** es una aplicación interactiva que permite calcular y visualizar trayectorias de pozos verticales en 3D. Utiliza cálculos trigonométricos para generar puntos de trayectoria y ofrece una visualización precisa mediante gráficos generados con Plotly.

---

## 🚀 Introducción

Bienvenido a **Well Trajectory Simulator**, una herramienta diseñada para ayudar a ingenieros en la industria petrolera a visualizar trayectorias de pozos con precisión. Esta herramienta está centrada en la simulación de trayectorias de pozos verticales, permitiendo a los usuarios ajustar parámetros y visualizar los resultados en gráficos interactivos.

<div align="center">
    <img src="Plataforma1.gif" alt="Plataforma 1 GIF" style="width:100%; margin-right:5%;">
    <img src="Plataforma2.gif" alt="Plataforma 2 GIF" style="width:100%;">
</div>

---

## 📈 Descripción del Proyecto

Este proyecto ofrece:

- **Cálculo y visualización de trayectorias de pozos verticales**.
- **Gráficos 3D interactivos** utilizando Plotly para mejorar la comprensión visual.
- **Interfaz intuitiva y sencilla**, desarrollada en Python y desplegada con Streamlit.
- **Posibilidad de ajustar parámetros clave** como la longitud de cada sección del pozo.
  
---

## 🛠️ Requisitos

Para ejecutar la aplicación necesitas tener instalados los siguientes paquetes:

- Python 3.8 o superior
- Plotly
- Pandas
- Streamlit

Puedes instalar todos los requisitos usando el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Uso

### Clonar el repositorio:

```bash
git clone https://github.com/tu_usuario/WellTrajectorySimulator.git
```

### Ejecutar la aplicación:

```bash
streamlit run app.py
```

---

### 🤝 Contribuciones

Si deseas contribuir a este proyecto:

1. Haz un fork del repositorio.
2. Crea una nueva rama para tus cambios (`git checkout -b feature/nueva_funcionalidad`).
3. Haz commit de tus cambios (`git commit -am 'Añadir nueva funcionalidad'`).
4. Haz push de tu rama (`git push origin feature/nueva_funcionalidad`).
5. Crea un Pull Request.

---

## 🗂️ Estructura de Archivos

```bash
WellTrajectorySimulator/
│
├── app.py               # Control principal de la aplicación.
├── pozo_tipo_j.py        # Cálculos y visualización de pozos tipo J.
├── pozo_tipo_s.py        # Cálculos y visualización de pozos tipo S.
├── pozo_vertical.py      # Cálculos y visualización de pozos verticales.
├── Diagramas y gráficos/
│   ├── Diagrama pozo tipo J.png
│   ├── Logo.png
│   ├── Plataforma1.gif
│   ├── Plataforma2.gif
│   ├── Plataforma3.png
├── requirements.txt      # Archivo con las dependencias del proyecto.
├── README.md             # Archivo con la descripción del proyecto.
```

---

## 📝 Licencia

Este proyecto está bajo la licencia MIT. ¡Siéntete libre de usarlo, mejorarlo y compartirlo!
