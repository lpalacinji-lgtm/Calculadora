# app.py

import streamlit as st
from datetime import datetime
from calculator import calcular_tabletas, calcular_ampollas

# ======================================
# CONFIGURACIÓN GENERAL
# ======================================
st.set_page_config(
    page_title="Calculadora de Medicamentos 💊",
    layout="wide",
    page_icon="💉"
)

# ======================================
# ESTILO HOSPITALARIO AZUL
# ======================================
st.markdown("""
    <style>
        /* Fondo general */
        body, .stApp {
            background-color: ;
        }

        /* Contenedor principal */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 1300px;
        }

        /* Títulos */
        h1 {
            color: #005b96;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }
        h2, h3 {
            color: #0074cc;
            margin-bottom: 0.4rem;
        }

        /* Campos del formulario */
        div[data-testid="stNumberInput"], div[data-testid="stDateInput"], div[data-testid="stSelectbox"], div[data-testid="stCheckbox"] {
            margin-bottom: 0.6rem;
        }

        /* Botón principal */
        button[kind="primary"] {
            background-color: #0074cc !important;
            color: white !important;
            border-radius: 8px;
            border: none;
            padding: 0.35rem 0.8rem !important;
            font-size: 0.9rem !important;
            font-weight: 600 !important;
        }
        button[kind="primary"]:hover {
            background-color: #000000 !important;
        }

        /* Caja de resultados */
        [data-testid="stMetric"] {
            background-color: #e7f1fb;
            border-radius: 10px;
            padding: 0.4rem;
            border: 1px solid #b6d4f0;
        }
        div[data-testid="stMetricValue"] {
            color: #005b96;
            font-size: 1.3rem;
            font-weight: 700;
        }

        /* Mensajes de éxito e información */
        .stSuccess {
            background-color: #e6f4ea !important;
            border-left: 5px solid #3c9d3c !important;
        }
        .stInfo {
            background-color:  !important;
            border-left: 5px solid #0074cc !important;
        }

        /* Compactación general */
        hr {
            margin: 0.4rem 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# ======================================
# TITULO Y LAYOUT
# ======================================
st.title("💊 Calculadora de Dispensación Médica")


col_form, col_result = st.columns([1.1, 1])

# ======================================
# COLUMNA IZQUIERDA — FORMULARIO
# ======================================
with col_form:
    st.subheader("🧾 Datos del Medicamento")

    tipo = st.selectbox("Tipo:", ["Tableta 💊", "Ampolla 💉"])
    frecuencia = st.number_input("Frecuencia (horas):", min_value=1, max_value=24, value=8)
    duracion = st.number_input("Duración (días):", min_value=1, max_value=120, value=5)
    fecha_orden = st.date_input("Fecha de orden:", datetime.today())
    inicio_mismo_dia = st.checkbox("Inicia el mismo día", value=True)
    st.caption("Si no marcha Check , inicia el otro dia ")

    st.divider()

    if tipo == "Tableta 💊":
        dosis_toma = st.number_input("Dosis por toma (tabletas):", min_value=0.25, step=0.25, value=1.0)
        unidades_presentacion = st.number_input("Unidades por caja:", min_value=1, step=1, value=30)
        calcular = st.button("🧮 Calcular Tabletas", use_container_width=True)

    else:
        dosis_inyeccion = st.number_input("Dosis por inyección (ml):", min_value=0.1, step=0.1, value=1.0)
        volumen_ampolla = st.number_input("Volumen por ampolla (ml):", min_value=0.5, step=0.5, value=2.0)
        esterilidad_horas = st.number_input("Esterilidad (horas):", min_value=6, step=6, value=24)
        calcular = st.button("🧮 Calcular Ampollas", use_container_width=True)

# ======================================
# COLUMNA DERECHA — RESULTADOS
# ======================================
with col_result:
    st.subheader("📊 Resultados")

    if tipo == "Tableta 💊" and 'calcular' in locals() and calcular:
        resultados = calcular_tabletas(frecuencia, duracion, dosis_toma, unidades_presentacion, fecha_orden, inicio_mismo_dia)

        st.success(f"**Tratamiento:** {resultados['Fecha de inicio']} → {resultados['Fecha de finalización']}")

        colA, colB, colC = st.columns(3)
        colA.metric("Tomas", resultados["Total de tomas"])
        colB.metric("Tabletas", resultados["Total de tabletas"])
        colC.metric("Presentaciones", resultados["Presentaciones necesarias"])

        st.caption("📆 Distribución mensual:")
        st.info(f"**Este mes:** {resultados['Tabletas este mes']} tabletas")
        st.info(f"**Próximo mes:** {resultados['Tabletas próximo mes']} tabletas")

    elif tipo == "Ampolla 💉" and 'calcular' in locals() and calcular:
        resultados = calcular_ampollas(frecuencia, duracion, dosis_inyeccion, volumen_ampolla, esterilidad_horas, fecha_orden, inicio_mismo_dia)

        st.success(f"**Tratamiento:** {resultados['Fecha de inicio']} → {resultados['Fecha de finalización']}")

        colA, colB, colC = st.columns(3)
        colA.metric("Inyecciones", resultados["Total de inyecciones"])
        colB.metric("Volumen (ml)", resultados["Volumen total (ml)"])
        colC.metric("Ampollas", resultados["Ampollas necesarias"])

        st.caption("💡 Reaperturas por esterilidad:")
        st.info(f"{resultados['Reaperturas por esterilidad']} veces")

        st.caption("📆 Distribución mensual:")
        st.info(f"**Este mes:** {resultados['Ampollas este mes']} ampollas ({resultados['Volumen este mes (ml)']} ml)")
        st.info(f"**Próximo mes:** {resultados['Ampollas próximo mes']} ampollas ({resultados['Volumen próximo mes (ml)']} ml)")



