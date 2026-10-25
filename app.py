
import streamlit as st
import numpy as np
import json

import plotly.graph_objects as go
from scipy.optimize import linprog
from scipy.optimize import linear_sum_assignment


st.set_page_config(
    page_title="JB OptiMid | Investigación de Operaciones",
    page_icon="📊",
    layout="wide"
)





st.markdown("""
<style>
/* ==================================================
   JB OPTIMID — NEON FUTURE
   Azul eléctrico · Cian · Violeta
   ================================================== */

/* Fondo principal */
.stApp,
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse at 8% 0%, rgba(32, 85, 180, 0.20), transparent 38%),
        radial-gradient(ellipse at 92% 12%, rgba(125, 55, 210, 0.17), transparent 34%),
        linear-gradient(145deg, #070b18 0%, #0b1224 52%, #101027 100%);
    color: #edf4ff;
}

/* Cabecera de Streamlit */
[data-testid="stHeader"] {
    background: rgba(7, 11, 24, 0.85);
}

/* Barra lateral */
[data-testid="stSidebar"] {
    background:
        linear-gradient(165deg, #101a35 0%, #10142b 55%, #21123b 100%);
    border-right: 1px solid #344775;
    box-shadow: 5px 0 28px rgba(50, 92, 220, 0.10);
}

[data-testid="stSidebar"] * {
    color: #edf4ff;
}

/* Opciones del menú */
[data-testid="stSidebar"] [role="radiogroup"] label {
    background: rgba(31, 48, 83, 0.78);
    border: 1px solid #30466f;
    border-radius: 11px;
    padding: 9px 12px;
    margin-bottom: 6px;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: linear-gradient(100deg, #193f70, #39245f);
    border-color: #49cfff;
}

/* Texto general */
.stApp p,
.stApp li,
.stApp label,
.stApp [data-testid="stMarkdownContainer"] {
    color: #d6e4fa;
}

.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4 {
    color: #f3f7ff !important;
    letter-spacing: -0.35px;
}

/* Encabezados con acento luminoso */
.stApp h1 {
    text-shadow: 0 0 22px rgba(55, 164, 255, 0.18);
}

.stApp h2 {
    text-shadow: 0 0 15px rgba(71, 123, 255, 0.12);
}

/* Tarjetas y contenedores */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(
        145deg,
        rgba(22, 35, 64, 0.96),
        rgba(18, 22, 46, 0.96)
    );
    border: 1px solid #34466f;
    border-radius: 16px;
    box-shadow: 0 8px 26px rgba(0, 0, 0, 0.18);
}

/* Métricas y resultados numéricos */
[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        rgba(19, 44, 78, 0.98),
        rgba(34, 26, 69, 0.98)
    );
    border: 1px solid #4565a0;
    border-radius: 15px;
    padding: 18px;
    box-shadow:
        0 0 18px rgba(39, 123, 255, 0.09),
        inset 0 1px 0 rgba(255, 255, 255, 0.04);
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] * {
    color: #b8cbed !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] * {
    color: #65dcff !important;
    text-shadow: 0 0 15px rgba(49, 205, 255, 0.22);
}

[data-testid="stMetricDelta"] {
    color: #65e6c1 !important;
}

/* Todos los botones: texto legible siempre */
.stButton > button,
.stFormSubmitButton > button,
[data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-primary"] {
    background: linear-gradient(110deg, #203e6d, #35265f) !important;
    color: #ffffff !important;
    border: 1px solid #5378b6 !important;
    border-radius: 11px !important;
    font-weight: 650 !important;
    min-height: 43px;
    opacity: 1 !important;
    box-shadow: 0 4px 14px rgba(22, 83, 180, 0.14);
    transition: all 0.2s ease;
}

.stButton > button *,
.stFormSubmitButton > button *,
[data-testid="stBaseButton-secondary"] *,
[data-testid="stBaseButton-primary"] * {
    color: #ffffff !important;
    opacity: 1 !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover,
[data-testid="stBaseButton-secondary"]:hover {
    background: linear-gradient(110deg, #176baf, #6236a1) !important;
    border-color: #63e5ff !important;
    box-shadow: 0 0 17px rgba(45, 190, 255, 0.20);
    color: #ffffff !important;
}

/* Botón principal */
.stButton > button[kind="primary"],
[data-testid="stBaseButton-primary"] {
    background: linear-gradient(105deg, #087fca 0%, #414bd5 55%, #783bd0 100%) !important;
    color: #ffffff !important;
    border: 1px solid #62cfff !important;
    box-shadow: 0 0 19px rgba(54, 132, 255, 0.24);
}

.stButton > button[kind="primary"] *,
[data-testid="stBaseButton-primary"] * {
    color: #ffffff !important;
}

.stButton > button[kind="primary"]:hover,
[data-testid="stBaseButton-primary"]:hover {
    background: linear-gradient(105deg, #119ce8, #5949ee 58%, #9149e8) !important;
    box-shadow: 0 0 24px rgba(61, 188, 255, 0.32);
}

/* Campos de texto, números y áreas de texto */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stDateInput"] input {
    background: #111c32 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: 1px solid #40577f !important;
    border-radius: 9px !important;
    caret-color: #5be1ff !important;
}

[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #4ad9ff !important;
    box-shadow: 0 0 0 1px #4ad9ff, 0 0 12px rgba(74, 217, 255, 0.13) !important;
}

input::placeholder,
textarea::placeholder {
    color: #a6b9d5 !important;
    -webkit-text-fill-color: #a6b9d5 !important;
    opacity: 1 !important;
}

/* Botones + y - de campos numéricos */
[data-testid="stNumberInput"] button {
    background: #223655 !important;
    color: #ffffff !important;
    border-color: #40577f !important;
}

[data-testid="stNumberInput"] button * {
    color: #ffffff !important;
}

/* Selectores desplegables */
[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
    background: #111c32 !important;
    color: #ffffff !important;
    border-color: #40577f !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"] *,
[data-testid="stMultiSelect"] [data-baseweb="select"] * {
    color: #ffffff !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"],
[role="listbox"] {
    background: #15213a !important;
    color: #ffffff !important;
    border: 1px solid #40577f !important;
}

[role="option"] {
    background: #15213a !important;
    color: #ffffff !important;
}

[role="option"]:hover,
[role="option"][aria-selected="true"] {
    background: #294774 !important;
    color: #ffffff !important;
}

/* Casillas y opciones */
[data-testid="stCheckbox"] label,
[data-testid="stRadio"] label {
    color: #e8f0ff !important;
}

/* Deslizadores */
[data-testid="stSlider"] {
    color: #55d8ff !important;
}

/* Tablas */
[data-testid="stDataFrame"] {
    border: 1px solid #344b72;
    border-radius: 12px;
    overflow: hidden;
}

/* Mensajes informativos */
[data-testid="stAlert"] {
    background: linear-gradient(115deg, #142a49, #211b43);
    border: 1px solid #3c6090;
    border-radius: 12px;
    color: #eff6ff;
}

/* Separadores */
hr {
    border-color: #304364;
}

/* Pie de página */
.pie-optimid {
    color: #9eb4d3;
    text-align: center;
    font-size: 0.85rem;
    padding: 14px 0;
}


/* Barra de progreso fija para Tutor y prácticas */
.tutor-progreso-flotante {
    position: fixed;
    top: 4.5rem;
    right: 1.5rem;
    z-index: 999999;
    width: 230px;
    padding: 14px;
    border: 1px solid rgba(100, 180, 255, 0.45);
    border-radius: 14px;
    background: rgba(15, 25, 45, 0.96);
    color: #ffffff;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.28);
    backdrop-filter: blur(12px);
}

.tutor-progreso-flotante .titulo {
    font-size: 0.85rem;
    font-weight: 700;
    margin-bottom: 8px;
}

.tutor-progreso-flotante .datos {
    display: flex;
    justify-content: space-between;
    gap: 8px;
    font-size: 0.78rem;
}

.tutor-progreso-flotante .porcentaje {
    font-size: 1.3rem;
    font-weight: 800;
    margin-top: 8px;
}

.tutor-progreso-flotante .barra {
    height: 6px;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.18);
    overflow: hidden;
    margin-top: 8px;
}

.tutor-progreso-flotante .relleno {
    height: 100%;
    background: #35d0a0;
    border-radius: 10px;
}

/* En pantallas pequeñas, ubicarla debajo del encabezado */
@media (max-width: 700px) {
    .tutor-progreso-flotante {
        top: 4rem;
        right: 0.5rem;
        width: 185px;
        padding: 10px;
    }
}

</style>
""", unsafe_allow_html=True)





# Logotipo de JB OptiMid en el menú lateral
import os

ruta_logo = os.path.join("assets", "logo_jb_optimid.png")

if os.path.exists(ruta_logo):
    st.sidebar.image(ruta_logo, use_container_width=True)
    st.sidebar.markdown(
        "<h3 style='text-align:center;'>JB OptiMid</h3>",
        unsafe_allow_html=True
    )

st.sidebar.divider()



modulo = st.sidebar.radio(
    "📚 Menú principal",
    [
        "Inicio",
        "Modelación",
        "Programación lineal",
        "Método gráfico",
        "Método Simplex",
        "Transporte y asignación",
        "Inventarios",
        "Tutor y prácticas"
    ]
)

def resolver_modelo(
    objetivo, cx, cy,
    a1, b1, d1, op1,
    a2, b2, d2, op2
):
    coeficientes = (
        [-cx, -cy]
        if objetivo == "Maximizar"
        else [cx, cy]
    )

    restricciones_ub = []
    limites_ub = []
    restricciones_eq = []
    limites_eq = []

    for a, b, d, operador in [
        (a1, b1, d1, op1),
        (a2, b2, d2, op2)
    ]:
        if operador == "≤":
            restricciones_ub.append([a, b])
            limites_ub.append(d)

        elif operador == "≥":
            restricciones_ub.append([-a, -b])
            limites_ub.append(-d)

        elif operador == "=":
            restricciones_eq.append([a, b])
            limites_eq.append(d)

    return linprog(
        c=coeficientes,
        A_ub=restricciones_ub or None,
        b_ub=limites_ub or None,
        A_eq=restricciones_eq or None,
        b_eq=limites_eq or None,
        bounds=[(0, None), (0, None)],
        method="highs"
    )


def mostrar_grafica(
    cx, cy,
    a1, b1, d1, op1,
    a2, b2, d2, op2,
    x_opt, y_opt
):
    # Crear un rango que incluya el punto óptimo y las rectas
    valores_x = [0.0, x_opt]
    valores_y = [0.0, y_opt]

    restricciones_rango = [(a1, b1, d1)]
    if not (a2 == 0 and b2 == 0):
        restricciones_rango.append((a2, b2, d2))
    for a, b, d in restricciones_rango:
        if a != 0:
            valores_x.append(abs(d / a))
        if b != 0:
            valores_y.append(abs(d / b))

    xmax = max(valores_x) * 1.25 + 5
    ymax = max(valores_y) * 1.25 + 5

    xs = np.linspace(0, xmax, 250)
    ys = np.linspace(0, ymax, 250)
    X, Y = np.meshgrid(xs, ys)

    def cumple(X, Y, a, b, d, operador):
        expresion = a * X + b * Y
        if operador == "≤":
            return expresion <= d + 1e-9
        elif operador == "≥":
            return expresion >= d - 1e-9
        return np.abs(expresion - d) <= 1e-3

    factible = cumple(X, Y, a1, b1, d1, op1) & (X >= 0) & (Y >= 0)
    if not (a2 == 0 and b2 == 0):
        factible &= cumple(X, Y, a2, b2, d2, op2)

    fig = go.Figure()

    # Mostrar los puntos de la región factible
    if np.any(factible):
        fig.add_trace(go.Scatter(
            x=X[factible],
            y=Y[factible],
            mode="markers",
            marker=dict(
                size=4,
                color="lightgreen",
                opacity=0.3
            ),
            name="Región factible"
        ))

    # Dibujar las rectas de las restricciones
    restricciones_grafica = [(a1, b1, d1, op1, "Restricción 1")]
    if not (a2 == 0 and b2 == 0):
        restricciones_grafica.append((a2, b2, d2, op2, "Restricción 2"))
    for a, b, d, operador, nombre in restricciones_grafica:
        if b != 0:
            y_recta = (d - a * xs) / b
            fig.add_trace(go.Scatter(
                x=xs,
                y=y_recta,
                mode="lines",
                name=f"{nombre} ({operador})"
            ))
        elif a != 0:
            x_recta = d / a
            fig.add_trace(go.Scatter(
                x=[x_recta, x_recta],
                y=[0, ymax],
                mode="lines",
                name=f"{nombre} ({operador})"
            ))

    # Marcar la solución óptima
    fig.add_trace(go.Scatter(
        x=[x_opt],
        y=[y_opt],
        mode="markers+text",
        marker=dict(size=13, color="red"),
        text=[f"Óptimo ({x_opt:.2f}, {y_opt:.2f})"],
        textposition="top right",
        name="Solución óptima"
    ))

    fig.update_layout(
        title="Región factible y solución óptima",
        xaxis_title="Variable x",
        yaxis_title="Variable y",
        template="plotly_white",
        height=550
    )

    fig.update_xaxes(range=[0, xmax], zeroline=True)
    fig.update_yaxes(range=[0, ymax], zeroline=True)

    st.plotly_chart(fig, use_container_width=True)



def resolver_simplex(c1, c2, a1, b1, d1, a2, b2, d2):
    # Tabla: x, y, holgura 1, holgura 2, lado derecho
    tabla = np.array([
        [a1, b1, 1, 0, d1],
        [a2, b2, 0, 1, d2],
        [-c1, -c2, 0, 0, 0]
    ], dtype=float)

    nombres = ["s1", "s2"]
    historial = []

    # Guardar la tabla inicial
    historial.append({
        "titulo": "Tabla inicial",
        "tabla": tabla.copy(),
        "base": nombres.copy(),
        "explicacion": (
            "Se agregan variables de holgura para convertir "
            "las restricciones en ecuaciones."
        )
    })

    max_iteraciones = 100

    for iteracion in range(max_iteraciones):
        # Última fila: coeficientes de la función objetivo
        fila_objetivo = tabla[-1, :-1]

        # Si no quedan coeficientes negativos, se alcanzó el óptimo
        if np.all(fila_objetivo >= -1e-9):
            return tabla, nombres, historial, True

        # Variable entrante: coeficiente más negativo
        columna = int(np.argmin(fila_objetivo))

        # Cociente mínimo para elegir variable saliente
        cocientes = []

        for fila in range(len(tabla) - 1):
            if tabla[fila, columna] > 1e-9:
                cocientes.append(
                    (tabla[fila, -1] / tabla[fila, columna], fila)
                )

        if not cocientes:
            return tabla, nombres, historial, False

        _, fila_pivote = min(cocientes)

        nombre_entrante = ["x", "y"][columna]
        nombre_saliente = nombres[fila_pivote]
        pivote = tabla[fila_pivote, columna]

        # Convertir el pivote en 1
        tabla[fila_pivote, :] /= pivote

        # Convertir los demás elementos de esa columna en 0
        for fila in range(len(tabla)):
            if fila != fila_pivote:
                factor = tabla[fila, columna]
                tabla[fila, :] -= factor * tabla[fila_pivote, :]

        nombres[fila_pivote] = nombre_entrante

        historial.append({
            "titulo": f"Iteración {iteracion + 1}",
            "tabla": tabla.copy(),
            "base": nombres.copy(),
            "explicacion": (
                f"Entra {nombre_entrante} porque tiene el coeficiente "
                f"más negativo en la fila objetivo. Sale "
                f"{nombre_saliente}, según el cociente mínimo. "
                f"El elemento pivote fue {pivote:.4f}."
            )
        })

    return tabla, nombres, historial, False


def calcular_vertices(a1, b1, d1, op1, a2, b2, d2, op2):
    candidatos = [(0.0, 0.0)]

    restricciones = [(a1, b1, d1)]
    if not (a2 == 0 and b2 == 0):
        restricciones.append((a2, b2, d2))

    # Intersecciones de cada recta con los ejes
    for a, b, d in restricciones:
        if a != 0:
            candidatos.append((d / a, 0.0))

        if b != 0:
            candidatos.append((0.0, d / b))

    # Intersección entre las dos rectas
    determinante = a1 * b2 - a2 * b1

    if abs(determinante) > 1e-9:
        x = (d1 * b2 - d2 * b1) / determinante
        y = (a1 * d2 - a2 * d1) / determinante
        candidatos.append((x, y))

    def cumple(valor, operador, limite):
        if operador == "≤":
            return valor <= limite + 1e-7
        elif operador == "≥":
            return valor >= limite - 1e-7
        else:
            return abs(valor - limite) <= 1e-7

    vertices = []

    for x, y in candidatos:
        if x < -1e-7 or y < -1e-7:
            continue

        if not cumple(a1 * x + b1 * y, op1, d1):
            continue

        if not (a2 == 0 and b2 == 0) and not cumple(a2 * x + b2 * y, op2, d2):
            continue

        punto = (max(0.0, x), max(0.0, y))

        if not any(
            abs(punto[0] - vx) < 1e-7
            and abs(punto[1] - vy) < 1e-7
            for vx, vy in vertices
        ):
            vertices.append(punto)

    return sorted(vertices)



# ============================================================
# ASISTENTE IA — requiere GEMINI_API_KEY en Streamlit Secrets
# ============================================================
def _cliente_gemini():
    """Crea el cliente Gemini usando únicamente el secreto configurado."""
    try:
        clave = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        clave = ""
    if not clave:
        return None
    try:
        from google import genai
        return genai.Client(api_key=clave)
    except ImportError:
        return None


def _consultar_gemini(instrucciones, mensaje, json_mode=False):
    cliente = _cliente_gemini()
    if cliente is None:
        return None, (
            "El asistente IA no está configurado. Agrega GEMINI_API_KEY "
            "a los Secrets de Streamlit e instala google-genai en requirements.txt."
        )
    try:
        from google.genai import types
        configuracion = types.GenerateContentConfig(
            system_instruction=instrucciones,
            temperature=0.1,
            response_mime_type="application/json" if json_mode else "text/plain"
        )
        respuesta = cliente.models.generate_content(
            model="gemini-3.8-flash",
            contents=mensaje,
            config=configuracion
        )
        if not respuesta.text:
            return None, "Gemini no devolvió texto. Intenta reformular la pregunta."
        return respuesta.text, None
    except Exception as error:
        detalle = str(error)[:200]
        return None, (
            "No se pudo consultar Gemini. Verifica la clave, conexión y límites "
            "gratuitos. Detalle: " + detalle
        )


def mostrar_tutor_ia(modulo_actual):
    """Tutor restringido al contenido académico de JB OptiMid."""
    st.divider()
    st.subheader("🤖 Pregunta al tutor de JB OptiMid")
    st.caption(
        "Haz preguntas sobre Investigación de Operaciones y el módulo actual. "
        "Las respuestas de IA pueden contener errores; verifica los cálculos."
    )
    clave = "tutor_ia_" + modulo_actual.replace(" ", "_").replace("ó", "o").replace("í", "i")
    with st.form("form_" + clave):
        pregunta = st.text_area(
            "¿Qué deseas comprender?",
            placeholder="Ej. ¿Cómo se interpreta la región factible?",
            max_chars=1500,
            key=clave
        )
        enviar = st.form_submit_button("Consultar al tutor", type="primary")
    if enviar:
        if not pregunta.strip():
            st.warning("Escribe una pregunta antes de consultar.")
            return
        instrucciones = (
            "Eres el tutor académico de JB OptiMid, una aplicación universitaria "
            "de Investigación de Operaciones. Responde en español, de forma clara "
            "y didáctica. El módulo actual es: " + modulo_actual + ". Limita la "
            "respuesta a Investigación de Operaciones, matemáticas relacionadas "
            "y al uso educativo del módulo. Si la pregunta es ajena a esos temas, "
            "indica amablemente que no puedes ayudar con ella. No afirmes haber "
            "ejecutado la aplicación. Si faltan datos para calcular, dilo."
        )
        with st.spinner("El tutor está preparando una respuesta..."):
            respuesta, error = _consultar_gemini(instrucciones, pregunta)
        if error:
            st.warning(error)
        elif respuesta:
            st.markdown("**Respuesta del tutor**")
            st.markdown(respuesta)



if modulo == "Inicio":
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <div style="
            color: #1769aa;
            font-weight: 700;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        ">
            TU ESPACIO DE APRENDIZAJE
        </div>
        <h1 style="margin-top: 6px; margin-bottom: 8px;">
            ¡Bienvenido a JB OptiMid!
        </h1>
        <p style="
            color: #526781;
            font-size: 1.08rem;
            max-width: 800px;
        ">
            Convierte problemas en decisiones. Modela, calcula y
            comprende los métodos de Investigación de Operaciones
            paso a paso.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Explora tus herramientas")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("## 🧮")
            st.markdown("### Modela y resuelve")
            st.write(
                "Define funciones objetivo, restricciones y "
                "encuentra soluciones para tus problemas."
            )
            st.caption("Programación lineal · Método gráfico")

    with col2:
        with st.container(border=True):
            st.markdown("## 📊")
            st.markdown("### Analiza resultados")
            st.write(
                "Explora procedimientos, tablas, restricciones "
                "y resultados para comprender cada solución."
            )
            st.caption("Simplex · Transporte · Asignación")

    with col3:
        with st.container(border=True):
            st.markdown("## 🎓")
            st.markdown("### Aprende practicando")
            st.write(
                "Repasa conceptos, resuelve preguntas y recibe "
                "retroalimentación para reforzar lo aprendido."
            )
            st.caption("Inventarios · Tutor y prácticas")

    st.markdown("")

    st.subheader("¿Cómo empezar?")

    st.info(
        "Selecciona un módulo en el menú de la izquierda. "
        "Introduce tus datos, ejecuta el cálculo y revisa "
        "el procedimiento antes de interpretar el resultado."
    )

    st.subheader("✨ Analiza un enunciado con IA")
    st.write(
        "Describe el problema con tus palabras. En esta primera versión, "
        "la preparación automática se habilita para programación lineal de "
        "dos variables; otros tipos se identificarán para su integración posterior."
    )
    with st.form("form_analizador_ia"):
        enunciado = st.text_area(
            "Enunciado del problema",
            placeholder="Ej. Una empresa fabrica dos productos...",
            max_chars=5000,
            key="enunciado_analizador_ia"
        )
        analizar = st.form_submit_button("Analizar enunciado", type="primary")
    if analizar:
        if not enunciado.strip():
            st.warning("Escribe un enunciado antes de analizarlo.")
        else:
            instrucciones = """
Analiza problemas de Investigación de Operaciones y devuelve SOLO JSON válido.
Esquema: tipo (programacion_lineal, transporte, asignacion, inventarios,
simplex, no_identificado), objetivo (Maximizar, Minimizar o cadena vacía),
cx, cy, a1, b1, d1, a2, b2, d2 (números o null), op1, op2 (≤, ≥, = o cadena
vacía), explicacion (cadena), faltantes (lista de cadenas), confianza
(alta, media o baja). Nunca inventes valores. Usa null para datos ausentes.
Interpreta programación lineal de dos variables con una o más restricciones.
Extrae únicamente las restricciones que estén explícitas en el enunciado.
Si solo existe una restricción, deja a2, b2, d2 como null y op2 como cadena vacía;
no inventes una segunda restricción. Si no se especifica ninguna otra condición,
no la marques como dato faltante. Si faltan datos esenciales de una restricción
mencionada, indícalos en faltantes. Si el problema es transporte, asignación o
inventarios, clasifícalo sin forzar los datos al modelo de programación lineal.
Responde en español.
"""
            with st.spinner("Analizando el enunciado..."):
                resultado_ia, error_ia = _consultar_gemini(
                    instrucciones, enunciado, json_mode=True
                )
            if error_ia:
                st.warning(error_ia)
            else:
                try:
                    modelo_ia = json.loads(resultado_ia)
                    # Una segunda restricción ausente no es un dato faltante
                    # cuando el enunciado solo contiene una.
                    if (
                        modelo_ia.get("tipo") == "programacion_lineal"
                        and all(
                            modelo_ia.get(campo) is None
                            for campo in ["a2", "b2", "d2"]
                        )
                        and modelo_ia.get("op2") in [None, ""]
                    ):
                        modelo_ia["faltantes"] = [
                            dato for dato in (modelo_ia.get("faltantes") or [])
                            if "segunda restricción" not in str(dato).lower()
                            and "segunda restriccion" not in str(dato).lower()
                        ]
                    st.session_state["modelo_ia_preparado"] = modelo_ia
                    st.session_state["enunciado_ia_original"] = enunciado
                except (ValueError, TypeError):
                    st.error("La IA no devolvió un modelo válido. Intenta reformular el enunciado.")

    modelo_ia = st.session_state.get("modelo_ia_preparado")
    if modelo_ia:
        st.markdown("#### Resultado del análisis")
        st.info("Tipo detectado: " + str(modelo_ia.get("tipo", "no_identificado")))
        st.write(modelo_ia.get("explicacion", ""))
        # Aplicar también al mostrar el resultado, por si quedó un análisis
        # anterior en la sesión o el modelo incluye variantes del texto.
        if (
            str(modelo_ia.get("tipo", "")).strip().lower() == "programacion_lineal"
            and all(modelo_ia.get(campo) is None for campo in ["a2", "b2", "d2"])
            and modelo_ia.get("op2") in [None, ""]
        ):
            # En programación lineal, la segunda restricción es opcional.
            # No dejar que el texto generado por el modelo IA la convierta
            # en un requisito cuando todos sus campos están vacíos.
            palabras_opcionales = (
                "segunda restricción", "segunda restriccion",
                "restricción adicional", "restriccion adicional",
                "recurso adicional", "condición adicional", "condicion adicional",
            )
            modelo_ia["faltantes"] = [
                dato for dato in (modelo_ia.get("faltantes") or [])
                if not any(
                    frase in str(dato).casefold()
                    for frase in palabras_opcionales
                )
            ]
        faltantes = modelo_ia.get("faltantes") or []
        if faltantes:
            st.warning("Datos faltantes o por confirmar: " + "; ".join(map(str, faltantes)))
        if modelo_ia.get("tipo") == "programacion_lineal":
            campos = ["objetivo", "cx", "cy", "a1", "b1", "op1", "d1", "a2", "b2", "op2", "d2"]
            st.write("**Datos extraídos. Revísalos antes de resolver:**")
            st.json({campo: modelo_ia.get(campo) for campo in campos})
            requeridos = ["cx", "cy", "a1", "b1", "d1"]
            tiene_r2 = all(
                modelo_ia.get(campo) is not None
                for campo in ["a2", "b2", "d2"]
            ) and modelo_ia.get("op2") in ["≤", "≥", "="]
            sin_r2 = (
                all(modelo_ia.get(campo) is None for campo in ["a2", "b2", "d2"])
                and modelo_ia.get("op2") in [None, ""]
            )
            completo = (
                all(modelo_ia.get(campo) is not None for campo in requeridos)
                and modelo_ia.get("objetivo") in ["Maximizar", "Minimizar"]
                and modelo_ia.get("op1") in ["≤", "≥", "="]
                and (tiene_r2 or sin_r2)
            )
            if completo:
                if st.button("Preparar campos de Programación lineal", type="primary"):
                    st.session_state["ia_lp_pendiente"] = modelo_ia
                    st.success("Datos preparados. Abre Programación lineal en el menú para cargarlos y revisarlos.")
            else:
                st.warning("El modelo está incompleto. Completa los campos faltantes manualmente.")
        elif modelo_ia.get("tipo") in ["transporte", "asignacion", "inventarios", "simplex"]:
            st.warning("Se identificó el tipo de problema, pero el llenado automático de este módulo se añadirá en una siguiente etapa. Por ahora, introduce los datos manualmente.")
        else:
            st.warning("No se pudo identificar el problema con suficiente seguridad. Selecciona un módulo y completa los datos manualmente.")

    st.markdown("""
    <div style="
        background: linear-gradient(110deg, #e4f3ff, #e7fbfa);
        border: 1px solid #c9e8f5;
        border-radius: 14px;
        padding: 20px 24px;
        margin-top: 12px;
    ">
        <div style="font-size: 1.05rem; font-weight: 700; color: #143b62;">
            💡 Aprende el procedimiento, no solo la respuesta
        </div>
        <p style="color: #385773; margin-bottom: 0;">
            JB OptiMid te ayuda a relacionar los datos del problema
            con su modelo matemático y a interpretar los resultados.
        </p>
    </div>
    """, unsafe_allow_html=True)


elif modulo in ["Programación lineal", "Método gráfico"]:
    pendiente_ia = st.session_state.get("ia_lp_pendiente")
    if pendiente_ia and modulo == "Programación lineal":
        mapa_campos = {
            "lp_objetivo": pendiente_ia.get("objetivo"),
            "lp_cx": pendiente_ia.get("cx"), "lp_cy": pendiente_ia.get("cy"),
            "lp_a1": pendiente_ia.get("a1"), "lp_b1": pendiente_ia.get("b1"),
            "lp_d1": pendiente_ia.get("d1"), "lp_a2": pendiente_ia.get("a2"),
            "lp_b2": pendiente_ia.get("b2"), "lp_d2": pendiente_ia.get("d2"),
            "lp_op1": pendiente_ia.get("op1"), "lp_op2": pendiente_ia.get("op2"),
            "lp_usar_r2": all(
                pendiente_ia.get(campo) is not None
                for campo in ["a2", "b2", "d2"]
            ) and pendiente_ia.get("op2") in ["≤", "≥", "="]
        }
        for clave, valor in mapa_campos.items():
            if valor is not None:
                st.session_state[clave] = valor
        st.session_state["ia_lp_pendiente"] = None
        st.success("La IA preparó los campos. Revísalos y pulsa Resolver problema cuando estés listo.")
    st.header("🧮 " + modulo)

    st.write(
        "Introduce los coeficientes de la función objetivo y las restricciones "
        "que realmente aparecen en el enunciado. Puedes usar una o dos restricciones."
    )

    objetivo = st.selectbox(
        "¿Qué deseas hacer?",
        ["Maximizar", "Minimizar"],
        key="lp_objetivo"
    )

    col1, col2 = st.columns(2)

    with col1:
        cx = st.number_input("Coeficiente de x en Z", value=40.0, key="lp_cx")
    with col2:
        cy = st.number_input("Coeficiente de y en Z", value=30.0, key="lp_cy")

    st.subheader("Restricciones")
    usar_r2 = st.checkbox(
        "Este problema tiene una segunda restricción",
        key="lp_usar_r2",
        help="Actívala solo si el enunciado incluye otra condición."
    )

    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        a1 = st.number_input("R1: coeficiente de x", value=2.0, key="lp_a1")
    with col2:
        b1 = st.number_input("R1: coeficiente de y", value=1.0, key="lp_b1")
    with col3:
        d1 = st.number_input("R1: límite", value=100.0, key="lp_d1")
    op1 = st.selectbox("Operador R1", ["≤", "≥", "="], key="lp_op1")

    if usar_r2:
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            a2 = st.number_input("R2: coeficiente de x", value=1.0, key="lp_a2")
        with col2:
            b2 = st.number_input("R2: coeficiente de y", value=2.0, key="lp_b2")
        with col3:
            d2 = st.number_input("R2: límite", value=80.0, key="lp_d2")
        op2 = st.selectbox("Operador R2", ["≤", "≥", "="], key="lp_op2")
    else:
        # La restricción inactiva se representa como 0 <= 0 para el cálculo.
        a2, b2, d2, op2 = 0.0, 0.0, 0.0, "≤"

    st.subheader("Modelo matemático")
    palabra = "Maximizar" if objetivo == "Maximizar" else "Minimizar"
    st.latex(rf"\text{{{palabra}}}\quad Z={cx:g}x+{cy:g}y")
    st.latex(rf"{a1:g}x+{b1:g}y\ {op1}\ {d1:g}")
    if usar_r2:
        st.latex(rf"{a2:g}x+{b2:g}y\ {op2}\ {d2:g}")
    st.latex(r"x,y\geq0")

    if st.button("Resolver problema", type="primary"):
        datos = [cx, cy, a1, b1, d1, a2, b2, d2]

        # 1. Validar los datos antes de resolver
        if not all(np.isfinite(v) for v in datos):
            st.error(
                "Los datos contienen valores no válidos. "
                "Introduce solamente números finitos."
            )

        elif (a1 == 0 and b1 == 0) or (usar_r2 and a2 == 0 and b2 == 0):
            st.error(
                "Cada restricción debe tener al menos un "
                "coeficiente distinto de cero."
            )


        else:
            # 2. Ejecutar el solucionador y controlar posibles errores
            try:
                resultado = resolver_modelo(
                    objetivo, cx, cy,
                    a1, b1, d1, op1,
                    a2, b2, d2, op2
                )

            except (ValueError, TypeError, FloatingPointError) as error:
                st.error(
                    "No se pudieron procesar los datos del modelo. "
                    "Revisa los coeficientes e inténtalo de nuevo."
                )
                st.caption(f"Detalle técnico: {error}")

            else:
                # 3. Interpretar el resultado según el estado
                if resultado.status == 0 and resultado.success:
                    x = resultado.x[0]
                    y = resultado.x[1]
                    z = cx * x + cy * y

                    st.subheader("Resultado óptimo")

                    r1, r2, r3 = st.columns(3)
                    r1.metric("Valor de x", f"{x:.4f}")
                    r2.metric("Valor de y", f"{y:.4f}")
                    r3.metric("Valor de Z", f"{z:.4f}")

                    st.subheader("Procedimiento")

                    st.write("**1. Función objetivo evaluada**")
                    st.latex(
                        rf"Z={cx:g}({x:.4f})+{cy:g}({y:.4f})={z:.4f}"
                    )

                    st.write("**2. Verificación de las restricciones**")

                    valor1 = a1 * x + b1 * y
                    valor2 = a2 * x + b2 * y if usar_r2 else None

                    def restriccion_cumplida(valor, operador, limite):
                        if operador == "≤":
                            return valor <= limite + 1e-7
                        elif operador == "≥":
                            return valor >= limite - 1e-7
                        return abs(valor - limite) <= 1e-7

                    st.latex(
                        rf"{a1:g}({x:.4f})+{b1:g}({y:.4f})"
                        rf"={valor1:.4f}\ {op1}\ {d1:g}"
                    )
                    cumple_r1 = restriccion_cumplida(valor1, op1, d1)
                    if usar_r2:
                        st.latex(
                            rf"{a2:g}({x:.4f})+{b2:g}({y:.4f})"
                            rf"={valor2:.4f}\ {op2}\ {d2:g}"
                        )
                        cumple_r2 = restriccion_cumplida(valor2, op2, d2)
                    else:
                        cumple_r2 = True

                    if cumple_r1 and cumple_r2:
                        texto_restricciones = (
                            "La solución cumple ambas restricciones."
                            if usar_r2
                            else "La solución cumple la restricción especificada."
                        )
                        st.success(texto_restricciones)
                    else:
                        st.error("La solución no cumple alguna restricción.")

                    st.success(
                        f"Solución encontrada: x = {x:.4f}, "
                        f"y = {y:.4f}, Z = {z:.4f}."
                    )
                    st.subheader("Gráfica")
                    mostrar_grafica(
                        cx, cy,
                        a1, b1, d1, op1,
                        a2, b2, d2, op2,
                        x, y
                    )
                    if modulo == "Método gráfico":
                        st.subheader("Tabla de vértices factibles")

                        vertices = calcular_vertices(
                            a1, b1, d1, op1,
                            a2, b2, d2, op2
                        )

                        filas = []

                        for numero, (vx, vy) in enumerate(
                            vertices, start=1
                        ):
                            valor_z = cx * vx + cy * vy

                            filas.append({
                                "Vértice": f"V{numero}",
                                "x": round(vx, 4),
                                "y": round(vy, 4),
                                "Valor de Z": round(valor_z, 4)
                            })

                        st.dataframe(
                            filas,
                            use_container_width=True,
                            hide_index=True
                        )

                        st.subheader("Procedimiento del método gráfico")

                        st.write(
                            "**Paso 1.** Se calculan las intersecciones "
                            "de las rectas con los ejes y entre sí."
                        )
                        st.write(
                            "**Paso 2.** Se verifican las restricciones "
                            "y las condiciones de no negatividad."
                        )
                        st.write(
                            "**Paso 3.** Se evalúa la función objetivo "
                            "en cada vértice factible identificado."
                        )
                        st.write(
                            "**Paso 4.** Se comparan los valores de Z."
                        )

                        if vertices:
                            valores_z = [
                                cx * vx + cy * vy
                                for vx, vy in vertices
                            ]

                            mejor_z = (
                                max(valores_z)
                                if objetivo == "Maximizar"
                                else min(valores_z)
                            )

                            mejores = [
                                (vx, vy)
                                for (vx, vy), vz in zip(
                                    vertices, valores_z
                                )
                                if abs(vz - mejor_z) < 1e-7
                            ]

                            for vx, vy in mejores:
                                st.latex(
                                    rf"Z={cx:g}({vx:.4f})"
                                    rf"+{cy:g}({vy:.4f})"
                                    rf"={mejor_z:.4f}"
                                )

                            if len(mejores) == 1:
                                vx, vy = mejores[0]
                                st.success(
                                    f"Mejor vértice identificado: "
                                    f"({vx:.4f}, {vy:.4f}), "
                                    f"con Z = {mejor_z:.4f}."
                                )
                            else:
                                st.success(
                                    f"Se identificaron varios vértices "
                                    f"con el mismo valor de Z = {mejor_z:.4f}."
                                )
                        else:
                            st.warning(
                                "No se identificaron vértices factibles "
                                "para mostrar en la tabla. La solución "
                                "del optimizador debe prevalecer sobre "
                                "esta tabla incompleta."
                            )

                elif resultado.status == 2:
                    st.error(
                        "Modelo infactible: no existe una combinación "
                        "de x e y que cumpla todas las restricciones."
                    )
                    st.info(
                        "Revisa los límites y las restricciones. "
                        "Puede que algunas condiciones sean incompatibles."
                    )

                elif resultado.status == 3:
                    st.error(
                        "Modelo no acotado: la función objetivo puede "
                        "mejorar indefinidamente dentro de la región "
                        "permitida."
                    )
                    st.info(
                        "Revisa si faltan restricciones que limiten "
                        "las variables o la función objetivo."
                    )

                elif resultado.status == 1:
                    st.warning(
                        "El solucionador alcanzó su límite de iteraciones "
                        "antes de confirmar una solución óptima."
                    )
                    st.write(
                        "Esto no demuestra que el modelo sea infactible "
                        "ni que sea no acotado."
                    )

                elif resultado.status == 4:
                    st.error(
                        "El solucionador encontró dificultades numéricas "
                        "y no pudo confirmar el resultado."
                    )
                    st.write(
                        "Comprueba los coeficientes y evita combinar "
                        "valores de escalas extremadamente diferentes."
                    )

                else:
                    st.error(
                        "No se pudo confirmar una solución óptima."
                    )
                    st.caption(
                        f"Estado del solucionador: {resultado.status}. "
                        f"Detalle: {resultado.message}"
                    )


elif modulo == "Método Simplex":
    st.header("📋 Método Simplex")
    st.write(
        "Resuelve problemas de maximización con dos variables y "
        "restricciones de tipo ≤."
    )

    st.latex(r"\text{Maximizar } Z=c_1x+c_2y")

    col1, col2 = st.columns(2)

    with col1:
        c1 = st.number_input(
            "Coeficiente de x en Z", value=40.0, min_value=0.0
        )
        a1 = st.number_input(
            "R1: coeficiente de x", value=2.0
        )
        b1 = st.number_input(
            "R1: coeficiente de y", value=1.0
        )
        d1 = st.number_input(
            "R1: lado derecho", value=100.0, min_value=0.0
        )

    with col2:
        c2 = st.number_input(
            "Coeficiente de y en Z", value=30.0, min_value=0.0
        )
        a2 = st.number_input(
            "R2: coeficiente de x", value=1.0
        )
        b2 = st.number_input(
            "R2: coeficiente de y", value=2.0
        )
        d2 = st.number_input(
            "R2: lado derecho", value=80.0, min_value=0.0
        )

    st.subheader("Modelo matemático")
    st.latex(rf"\text{{Maximizar }} Z={c1:g}x+{c2:g}y")
    st.latex(rf"{a1:g}x+{b1:g}y\leq {d1:g}")
    st.latex(rf"{a2:g}x+{b2:g}y\leq {d2:g}")
    st.latex(r"x,y\geq0")


    if st.button("Ejecutar método Simplex", type="primary"):
        # 1. Detectar restricciones imposibles
        if (
            (a1 == 0 and b1 == 0 and d1 < 0)
            or (a2 == 0 and b2 == 0 and d2 < 0)
        ):
            st.error(
                "Modelo inviable: una restricción exige que "
                "0 sea menor o igual que un número negativo."
            )

        # 2. Validar los coeficientes admitidos por esta versión
        elif a1 < 0 or b1 < 0 or a2 < 0 or b2 < 0:
            st.error(
                "Esta versión de Simplex solo admite coeficientes "
                "no negativos en las restricciones."
            )

        # 3. Detectar si ambas restricciones carecen de variables
        elif (
            a1 == 0 and b1 == 0 and d1 >= 0
            and a2 == 0 and b2 == 0 and d2 >= 0
        ):
            st.error(
                "No hay restricciones que limiten las variables. "
                "Revisa los coeficientes ingresados."
            )

        else:
            try:

                tabla, base, historial, terminado = resolver_simplex(
                    c1, c2, a1, b1, d1, a2, b2, d2
                )

                # Mostrar el procedimiento paso a paso
                for paso in historial:
                    st.subheader(paso["titulo"])
                    st.write(paso["explicacion"])

                    tabla_paso = paso["tabla"]
                    base_paso = paso["base"]

                    encabezados = [
                        "x", "y", "s1", "s2", "Lado derecho"
                    ]

                    filas_tabla = []

                    for i in range(2):
                        fila = {"Base": base_paso[i]}

                        for j, encabezado in enumerate(encabezados):
                            fila[encabezado] = round(
                                float(tabla_paso[i, j]), 4
                            )

                        filas_tabla.append(fila)

                    fila_z = {"Base": "Z"}

                    for j, encabezado in enumerate(encabezados):
                        fila_z[encabezado] = round(
                            float(tabla_paso[2, j]), 4
                        )

                    filas_tabla.append(fila_z)

                    st.dataframe(
                        filas_tabla,
                        use_container_width=True,
                        hide_index=True
                    )

                # Mostrar la solución si Simplex terminó correctamente
                if terminado:
                    solucion = {"x": 0.0, "y": 0.0}

                    for i, variable in enumerate(base):
                        if variable in solucion:
                            solucion[variable] = float(tabla[i, -1])

                    x_opt = solucion["x"]
                    y_opt = solucion["y"]
                    z_opt = c1 * x_opt + c2 * y_opt

                    # Comprobar que la solución cumpla las restricciones
                    cumple_r1 = a1 * x_opt + b1 * y_opt <= d1 + 1e-7
                    cumple_r2 = a2 * x_opt + b2 * y_opt <= d2 + 1e-7

                    if (
                        x_opt < -1e-7
                        or y_opt < -1e-7
                        or not cumple_r1
                        or not cumple_r2
                    ):
                        st.error(
                            "El algoritmo terminó, pero la solución "
                            "obtenida no cumple todas las restricciones. "
                            "Revisa el modelo."
                        )
                    else:
                        st.subheader("Resultado final")
                        r1, r2, r3 = st.columns(3)
                        r1.metric("x óptimo", f"{x_opt:.4f}")
                        r2.metric("y óptimo", f"{y_opt:.4f}")
                        r3.metric("Z máximo", f"{z_opt:.4f}")

                        st.write("**Comprobación de las restricciones**")
                        st.write(
                            f"R1: {a1:g}({x_opt:.4f}) + "
                            f"{b1:g}({y_opt:.4f}) = "
                            f"{a1*x_opt+b1*y_opt:.4f} ≤ {d1:g}"
                        )
                        st.write(
                            f"R2: {a2:g}({x_opt:.4f}) + "
                            f"{b2:g}({y_opt:.4f}) = "
                            f"{a2*x_opt+b2*y_opt:.4f} ≤ {d2:g}"
                        )

                        st.success(
                            "Se obtuvo una solución que cumple "
                            "las restricciones del modelo."
                        )

                else:
                    st.error(
                        "El método Simplex no alcanzó una solución "
                        "óptima. El algoritmo actual no permite "
                        "determinar con certeza si el modelo es "
                        "no acotado o si el procedimiento no pudo "
                        "completarse."
                    )

            except (ValueError, TypeError, IndexError, KeyError) as error:
                st.error(
                    "No fue posible procesar el resultado de Simplex. "
                    "Revisa los datos y la estructura del procedimiento."
                )
                st.caption(f"Detalle técnico: {error}")



elif modulo == "Transporte y asignación":
    st.header("Transporte y asignación")
    tipo_problema = st.radio(
        "Selecciona el tipo de problema:",
        ["Transporte", "Asignación"],
        horizontal=True
    )

    if tipo_problema == "Transporte":
        st.subheader("Problema de transporte")
        st.write(
            "Ingresa los costos por unidad, la oferta de cada origen "
            "y la demanda de cada destino. Para esta primera versión, "
            "la oferta total debe ser igual a la demanda total."
        )

        num_origenes = st.number_input(
            "Número de orígenes", min_value=2, max_value=5,
            value=2, step=1, key="trans_origenes"
        )
        num_destinos = st.number_input(
            "Número de destinos", min_value=2, max_value=5,
            value=2, step=1, key="trans_destinos"
        )

        num_origenes = int(num_origenes)
        num_destinos = int(num_destinos)

        st.markdown("**Costos de transporte por unidad**")
        costos = []
        for i in range(num_origenes):
            columnas = st.columns(num_destinos)
            fila = []
            for j in range(num_destinos):
                valor = columnas[j].number_input(
                    f"Origen {i+1} → Destino {j+1}",
                    min_value=0.0, value=1.0, step=1.0,
                    key=f"trans_costo_{i}_{j}"
                )
                fila.append(valor)
            costos.append(fila)

        st.markdown("**Oferta de cada origen**")
        ofertas = []
        columnas = st.columns(num_origenes)
        for i in range(num_origenes):
            ofertas.append(
                columnas[i].number_input(
                    f"Oferta O{i+1}", min_value=0.0,
                    value=20.0, step=1.0,
                    key=f"trans_oferta_{i}"
                )
            )

        st.markdown("**Demanda de cada destino**")
        demandas = []
        columnas = st.columns(num_destinos)
        for j in range(num_destinos):
            demandas.append(
                columnas[j].number_input(
                    f"Demanda D{j+1}", min_value=0.0,
                    value=20.0, step=1.0,
                    key=f"trans_demanda_{j}"
                )
            )

        if st.button("Resolver transporte", key="resolver_transporte"):
            if abs(sum(ofertas) - sum(demandas)) > 1e-6:
                st.error(
                    f"El problema no está equilibrado. Oferta total: "
                    f"{sum(ofertas):g}; demanda total: "
                    f"{sum(demandas):g}. Ajusta los datos para que "
                    "ambos totales sean iguales."
                )
            else:
                import numpy as np
                from scipy.optimize import linprog

                c = np.array(costos, dtype=float).flatten()
                restricciones = []
                valores = []

                for i in range(num_origenes):
                    fila = np.zeros((num_origenes, num_destinos))
                    fila[i, :] = 1
                    restricciones.append(fila.flatten())
                    valores.append(ofertas[i])

                for j in range(num_destinos):
                    fila = np.zeros((num_origenes, num_destinos))
                    fila[:, j] = 1
                    restricciones.append(fila.flatten())
                    valores.append(demandas[j])

                resultado = linprog(
                    c,
                    A_eq=np.array(restricciones),
                    b_eq=np.array(valores),
                    bounds=(0, None),
                    method="highs"
                )

                
                if resultado.success:
                    envios = resultado.x.reshape(
                        num_origenes, num_destinos
                    )

                    st.success("¡Solución óptima encontrada!")
                    st.subheader("Plan óptimo de envíos")

                    tabla_envios = {
                        "Origen": [
                            f"Origen {i+1}"
                            for i in range(num_origenes)
                        ],
                        **{
                            f"Destino {j+1}": [
                                round(float(envios[i, j]), 2)
                                for i in range(num_origenes)
                            ]
                            for j in range(num_destinos)
                        }
                    }

                    st.dataframe(
                        tabla_envios,
                        hide_index=True,
                        use_container_width=True
                    )

                    st.metric(
                        "Costo mínimo total",
                        f"{resultado.fun:.2f}"
                    )

                    st.markdown("**Procedimiento**")
                    st.write(
                        "1. Se definieron las variables como las "
                        "unidades enviadas desde cada origen a cada destino."
                    )
                    st.write(
                        "2. Se minimizó el costo total: "
                        "Z = suma de (costo por unidad × unidades enviadas)."
                    )
                    st.write(
                        "3. Se impusieron restricciones de oferta, "
                        "demanda y no negatividad."
                    )
                    st.write(
                        "4. Se resolvió el modelo mediante programación lineal."
                    )

                    st.write("**Detalle de los envíos:**")

                    for i in range(num_origenes):
                        for j in range(num_destinos):
                            if envios[i, j] > 1e-6:
                                st.write(
                                    f"- Origen {i+1} → Destino {j+1}: "
                                    f"{envios[i, j]:.2f} unidades × "
                                    f"{costos[i][j]:.2f} por unidad."
                                )
                else:
                    st.error("No fue posible encontrar una solución.")
                    st.write(resultado.message)


    else:
        st.subheader("Problema de asignación")
        st.write(
            "Asigna cada trabajador a una tarea, minimizando el costo. "
            "Esta versión utiliza igual número de trabajadores y tareas."
        )

        cantidad = int(st.number_input(
            "Cantidad de trabajadores y tareas",
            min_value=2, max_value=6, value=3, step=1,
            key="asig_cantidad"
        ))

        st.markdown("**Costo de cada asignación**")
        matriz = []
        for i in range(cantidad):
            columnas = st.columns(cantidad)
            fila = []
            for j in range(cantidad):
                valor = columnas[j].number_input(
                    f"Trabajador {i+1} → Tarea {j+1}",
                    min_value=0.0, value=float(i + j + 1),
                    step=1.0, key=f"asig_costo_{i}_{j}"
                )
                fila.append(valor)
            matriz.append(fila)

        if st.button("Resolver asignación", key="resolver_asignacion"):
            import numpy as np
            from scipy.optimize import linear_sum_assignment

            costos_array = np.array(matriz, dtype=float)
            filas, columnas = linear_sum_assignment(costos_array)
            total = costos_array[filas, columnas].sum()

            st.success("¡Asignación óptima encontrada!")
            st.subheader("Resultado")
            for i, j in zip(filas, columnas):
                st.write(
                    f"- Trabajador {i+1} → Tarea {j+1}: "
                    f"costo {costos_array[i, j]:.2f}"
                )

            st.metric("Costo mínimo total", f"{total:.2f}")
            st.markdown("**Procedimiento**")
            st.write(
                "1. Se construyó una matriz con los costos de cada asignación."
            )
            st.write(
                "2. Se buscó una combinación de asignaciones sin repetir "
                "trabajadores ni tareas."
            )
            st.write(
                "3. Se utilizó el algoritmo húngaro para encontrar "
                "el costo mínimo total."
            )


elif modulo == "Inventarios":
    st.header("📦 Gestión de inventarios")
    st.write(
        "Calcula la cantidad económica de pedido y el punto de "
        "reorden mediante modelos clásicos de Investigación de Operaciones."
    )

    tipo_inventario = st.radio(
        "Selecciona una herramienta:",
        ["Cantidad económica de pedido (EOQ)", "Punto de reorden (ROP)"],
        key="inventario_tipo"
    )

    st.divider()

    if tipo_inventario == "Cantidad económica de pedido (EOQ)":
        st.subheader("Cantidad económica de pedido")

        st.latex(r"Q^* = \sqrt{\frac{2DS}{H}}")

        st.write(
            "El modelo EOQ determina cuántas unidades pedir para "
            "minimizar la suma de los costos anuales de ordenar y mantener "
            "inventario, bajo los supuestos del modelo clásico."
        )

        col1, col2 = st.columns(2)

        with col1:
            demanda_anual = st.number_input(
                "Demanda anual (D), unidades",
                min_value=0.0,
                value=1200.0,
                step=100.0,
                key="eoq_demanda"
            )

            costo_pedido = st.number_input(
                "Costo por pedido (S)",
                min_value=0.01,
                value=50.0,
                step=5.0,
                key="eoq_costo_pedido"
            )

        with col2:
            costo_mantenimiento = st.number_input(
                "Costo anual de mantener una unidad (H)",
                min_value=0.01,
                value=4.0,
                step=0.5,
                key="eoq_mantenimiento"
            )

            costo_unidad = st.number_input(
                "Costo de compra por unidad (opcional)",
                min_value=0.0,
                value=0.0,
                step=1.0,
                help="Ingresa 0 si no deseas calcular el costo anual de compra.",
                key="eoq_costo_unidad"
            )

        if st.button("Calcular EOQ", key="calcular_eoq"):
            import math

            if demanda_anual <= 0:
                st.error("La demanda anual debe ser mayor que cero.")
            elif costo_pedido <= 0 or costo_mantenimiento <= 0:
                st.error(
                    "Los costos de pedido y mantenimiento deben ser mayores que cero."
                )
            else:
                eoq = math.sqrt(
                    (2 * demanda_anual * costo_pedido)
                    / costo_mantenimiento
                )

                pedidos_anuales = demanda_anual / eoq
                tiempo_entre_pedidos = 365 / pedidos_anuales
                costo_ordenar = pedidos_anuales * costo_pedido
                costo_mantener = (eoq / 2) * costo_mantenimiento
                costo_relevante = costo_ordenar + costo_mantener
                costo_compra_anual = demanda_anual * costo_unidad

                st.success("Cálculo EOQ completado.")

                col1, col2, col3 = st.columns(3)
                col1.metric("EOQ", f"{eoq:.2f} unidades")
                col2.metric("Pedidos al año", f"{pedidos_anuales:.2f}")
                col3.metric(
                    "Tiempo entre pedidos",
                    f"{tiempo_entre_pedidos:.1f} días"
                )

                st.subheader("Procedimiento y sustitución")

                st.markdown("**1. Fórmula del modelo:**")
                st.latex(r"Q^* = \sqrt{\frac{2DS}{H}}")

                st.markdown("**2. Sustitución de los datos:**")
                st.latex(
                    rf"Q^* = \sqrt{{\frac{{2({demanda_anual:.2f})"
                    rf"({costo_pedido:.2f})}}{{{costo_mantenimiento:.2f}}}}}"
                )

                st.markdown("**3. Cantidad económica calculada:**")
                st.latex(rf"Q^* = {eoq:.2f}\text{{ unidades}}")

                st.markdown("**4. Costos anuales relevantes:**")
                st.write(
                    f"Costo anual de ordenar: "
                    f"{pedidos_anuales:.2f} × {costo_pedido:.2f} "
                    f"= {costo_ordenar:.2f}"
                )
                st.write(
                    f"Costo anual de mantener: "
                    f"({eoq:.2f} / 2) × {costo_mantenimiento:.2f} "
                    f"= {costo_mantener:.2f}"
                )
                st.metric(
                    "Costo anual relevante mínimo aproximado",
                    f"{costo_relevante:.2f}"
                )

                if costo_unidad > 0:
                    st.write(
                        f"Costo anual de compra: {demanda_anual:.2f} × "
                        f"{costo_unidad:.2f} = {costo_compra_anual:.2f}"
                    )
                    st.metric(
                        "Costo anual total estimado",
                        f"{costo_relevante + costo_compra_anual:.2f}"
                    )

                st.info(
                    f"Interpretación: se recomienda pedir aproximadamente "
                    f"{eoq:.0f} unidades por pedido. Con una demanda anual "
                    f"de {demanda_anual:.0f} unidades, se realizarían "
                    f"alrededor de {pedidos_anuales:.1f} pedidos al año."
                )

                st.caption(
                    "Supuestos: demanda conocida y constante, reposición "
                    "instantánea, sin faltantes ni descuentos por cantidad. "
                    "El tiempo entre pedidos usa un año de 365 días."
                )

    else:
        st.subheader("Punto de reorden (ROP)")

        st.latex(r"ROP = dL + SS")

        st.write(
            "El punto de reorden indica el nivel de inventario en el que "
            "debe emitirse un nuevo pedido para cubrir la demanda durante "
            "el tiempo de entrega. SS representa el inventario de seguridad."
        )

        col1, col2 = st.columns(2)

        with col1:
            demanda_diaria = st.number_input(
                "Demanda diaria (unidades por día)",
                min_value=0.0,
                value=20.0,
                step=1.0,
                key="rop_demanda"
            )

            plazo_entrega = st.number_input(
                "Tiempo de entrega (días)",
                min_value=0.0,
                value=5.0,
                step=1.0,
                key="rop_entrega"
            )

        with col2:
            inventario_seguridad = st.number_input(
                "Inventario de seguridad (unidades)",
                min_value=0.0,
                value=10.0,
                step=1.0,
                key="rop_seguridad"
            )

        if st.button("Calcular punto de reorden", key="calcular_rop"):
            demanda_plazo = demanda_diaria * plazo_entrega
            punto_reorden = demanda_plazo + inventario_seguridad

            st.success("Punto de reorden calculado.")

            col1, col2 = st.columns(2)
            col1.metric(
                "Punto de reorden",
                f"{punto_reorden:.2f} unidades"
            )
            col2.metric(
                "Demanda durante la entrega",
                f"{demanda_plazo:.2f} unidades"
            )

            st.subheader("Procedimiento y sustitución")

            st.markdown("**1. Fórmula:**")
            st.latex(r"ROP = dL + SS")

            st.markdown("**2. Sustitución:**")
            st.latex(
                rf"ROP = ({demanda_diaria:.2f})"
                rf"({plazo_entrega:.2f}) + "
                rf"{inventario_seguridad:.2f}"
            )

            st.markdown("**3. Resultado:**")
            st.latex(rf"ROP = {punto_reorden:.2f}\text{{ unidades}}")

            st.info(
                f"Interpretación: cuando el inventario disponible llegue "
                f"a aproximadamente {punto_reorden:.0f} unidades, debe "
                f"emitirse un nuevo pedido. La demanda estimada durante "
                f"la entrega es de {demanda_plazo:.0f} unidades y se "
                f"reservan {inventario_seguridad:.0f} unidades de seguridad."
            )

            st.caption(
                "Este cálculo supone una demanda diaria promedio constante. "
                "El inventario de seguridad se introduce como dato; el modelo "
                "no calcula automáticamente su valor óptimo."
            )


elif modulo == "Modelación":
    st.header("📝 Modelación matemática")
    st.write(
        "Construye un modelo de programación lineal identificando "
        "sus variables de decisión, función objetivo y restricciones."
    )

    st.info(
        "Esta herramienta formula modelos con dos variables de decisión "
        "y dos restricciones. No resuelve el modelo automáticamente "
        "desde esta sección."
    )

    st.subheader("1. Definir las variables de decisión")

    col1, col2 = st.columns(2)

    with col1:
        nombre_x = st.text_input(
            "Nombre de la primera variable",
            value="x",
            key="mod_nombre_x"
        )
        descripcion_x = st.text_input(
            "¿Qué representa?",
            value="Unidades del producto A",
            key="mod_desc_x"
        )

    with col2:
        nombre_y = st.text_input(
            "Nombre de la segunda variable",
            value="y",
            key="mod_nombre_y"
        )
        descripcion_y = st.text_input(
            "¿Qué representa?",
            value="Unidades del producto B",
            key="mod_desc_y"
        )

    st.subheader("2. Definir la función objetivo")

    objetivo_modelo = st.radio(
        "¿Qué deseas hacer?",
        ["Maximizar", "Minimizar"],
        horizontal=True,
        key="mod_tipo_objetivo"
    )

    col1, col2 = st.columns(2)

    with col1:
        coef_obj_x = st.number_input(
            f"Coeficiente de {nombre_x or 'x'}",
            value=40.0,
            key="mod_obj_x"
        )

    with col2:
        coef_obj_y = st.number_input(
            f"Coeficiente de {nombre_y or 'y'}",
            value=30.0,
            key="mod_obj_y"
        )

    st.subheader("3. Definir las restricciones")

    st.caption(
        "Introduce los coeficientes de cada variable y el límite "
        "disponible del recurso."
    )

    restricciones_modelo = []

    for i in range(2):
        st.markdown(f"**Restricción {i + 1}**")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            coef_x = st.number_input(
                f"Coef. {nombre_x or 'x'}",
                value=2.0 if i == 0 else 1.0,
                key=f"mod_r{i}_x"
            )

        with col2:
            coef_y = st.number_input(
                f"Coef. {nombre_y or 'y'}",
                value=1.0 if i == 0 else 2.0,
                key=f"mod_r{i}_y"
            )

        with col3:
            relacion = st.selectbox(
                "Relación",
                ["≤", "≥", "="],
                key=f"mod_r{i}_rel"
            )

        with col4:
            limite = st.number_input(
                "Límite",
                value=100.0 if i == 0 else 80.0,
                key=f"mod_r{i}_lim"
            )

        restricciones_modelo.append(
            (coef_x, coef_y, relacion, limite)
        )

    st.subheader("4. Generar el modelo matemático")

    if st.button("Generar modelo", key="mod_generar"):
        if not nombre_x.strip() or not nombre_y.strip():
            st.error("Debes escribir un nombre para cada variable.")
        elif nombre_x.strip() == nombre_y.strip():
            st.error("Las dos variables deben tener nombres diferentes.")
        else:
            x = nombre_x.strip()
            y = nombre_y.strip()

            st.success("Modelo matemático generado.")

            st.markdown("### Variables de decisión")

            st.latex(rf"{x} = \text{{cantidad de {descripcion_x.strip() or x}}}")
            st.latex(rf"{y} = \text{{cantidad de {descripcion_y.strip() or y}}}")

            st.markdown("### Función objetivo")

            verbo = (
                r"\text{Maximizar}"
                if objetivo_modelo == "Maximizar"
                else r"\text{Minimizar}"
            )

            st.latex(
                rf"{verbo}\quad Z = "
                rf"{coef_obj_x:g}{x} + {coef_obj_y:g}{y}"
            )

            st.markdown("### Restricciones")

            for coef_x, coef_y, relacion, limite in restricciones_modelo:
                if coef_x == 0 and coef_y == 0:
                    st.warning(
                        "Una restricción tiene ambos coeficientes en cero. "
                        "Revisa si representa una condición útil."
                    )

                signo = {
                    "≤": r"\leq",
                    "≥": r"\geq",
                    "=": "="
                }[relacion]

                st.latex(
                    rf"{coef_x:g}{x} + {coef_y:g}{y} "
                    rf"{signo} {limite:g}"
                )

            st.markdown("### Condiciones de no negatividad")
            st.latex(rf"{x} \geq 0,\quad {y} \geq 0")

            st.markdown("### Interpretación del modelo")

            st.write(
                f"El objetivo es {objetivo_modelo.lower()} el valor de Z, "
                f"calculado a partir de los coeficientes {coef_obj_x:g} "
                f"y {coef_obj_y:g}. Las dos restricciones representan "
                "los límites de los recursos o condiciones del problema."
            )

            st.write(
                "Las condiciones de no negatividad impiden que las "
                "cantidades de decisión sean negativas."
            )

            st.caption(
                "Importante: verifica que las variables, coeficientes, "
                "signos y límites representen correctamente el enunciado "
                "original. Esta herramienta formula el modelo, pero no "
                "interpreta automáticamente texto libre."
            )


elif modulo == "Tutor y prácticas":
    import random

    st.header("🎓 Tutor y prácticas")
    st.write(
        "Repasa conceptos de Investigación de Operaciones, "
        "resuelve ejercicios y comprueba tus respuestas."
    )

    ejercicios = [
        {
            "tema": "Modelación",
            "pregunta": "¿Qué representan las variables de decisión?",
            "opciones": [
                "Las cantidades desconocidas que se deben determinar",
                "Los resultados que siempre son constantes",
                "Los errores de cálculo del modelo",
                "Los datos que no se utilizan"
            ],
            "correcta": 0,
            "explicacion": (
                "Las variables de decisión representan las cantidades "
                "que el modelo debe determinar, como unidades a producir "
                "o productos que se deben transportar."
            )
        },
        {
            "tema": "Modelación",
            "pregunta": "¿Cuál es la función objetivo de un modelo?",
            "opciones": [
                "Una lista de variables sin relación",
                "La expresión que se desea maximizar o minimizar",
                "Una restricción que siempre vale cero",
                "El nombre del algoritmo"
            ],
            "correcta": 1,
            "explicacion": (
                "La función objetivo expresa matemáticamente la meta "
                "del problema, por ejemplo, maximizar ganancias o "
                "minimizar costos."
            )
        },
        {
            "tema": "Programación lineal",
            "pregunta": (
                "Si Z = 40x + 30y, ¿cuánto vale Z cuando x = 2 e y = 3?"
            ),
            "opciones": ["110", "170", "180", "200"],
            "correcta": 1,
            "explicacion": (
                "Sustituyendo: Z = 40(2) + 30(3) = 80 + 90 = 170."
            )
        },
        {
            "tema": "Restricciones",
            "pregunta": "¿Qué significa la restricción 2x + y ≤ 100?",
            "opciones": [
                "El consumo debe ser exactamente 100",
                "El consumo debe ser como mínimo 100",
                "El consumo no puede superar 100",
                "Las variables deben ser negativas"
            ],
            "correcta": 2,
            "explicacion": (
                "El signo ≤ indica que el lado izquierdo debe ser menor "
                "o igual que 100."
            )
        },
        {
            "tema": "Método gráfico",
            "pregunta": "¿Qué representa la región factible?",
            "opciones": [
                "Todas las soluciones que cumplen las restricciones",
                "Únicamente las soluciones negativas",
                "Todas las soluciones sin comprobar restricciones",
                "El valor de la función objetivo solamente"
            ],
            "correcta": 0,
            "explicacion": (
                "La región factible contiene los puntos que satisfacen "
                "simultáneamente todas las restricciones y las condiciones "
                "de no negatividad."
            )
        },
        {
            "tema": "Método Simplex",
            "pregunta": (
                "En un problema de maximización con restricciones ≤, "
                "¿para qué se agregan variables de holgura?"
            ),
            "opciones": [
                "Para eliminar la función objetivo",
                "Para convertir las desigualdades en igualdades",
                "Para hacer negativas las variables",
                "Para cambiar maximización por minimización"
            ],
            "correcta": 1,
            "explicacion": (
                "Las variables de holgura representan recursos no utilizados "
                "y permiten expresar restricciones ≤ como ecuaciones."
            )
        },
        {
            "tema": "Transporte",
            "pregunta": (
                "En un problema de transporte equilibrado, ¿qué relación "
                "existe entre oferta total y demanda total?"
            ),
            "opciones": [
                "La oferta es siempre cero",
                "La demanda debe duplicar la oferta",
                "Ambas deben ser iguales",
                "No existe ninguna relación"
            ],
            "correcta": 2,
            "explicacion": (
                "El problema está equilibrado cuando la suma de las ofertas "
                "es igual a la suma de las demandas."
            )
        },
        {
            "tema": "Asignación",
            "pregunta": "¿Qué busca el algoritmo húngaro en un problema clásico?",
            "opciones": [
                "Maximizar el número de restricciones",
                "Encontrar una asignación de costo mínimo",
                "Calcular inventario de seguridad",
                "Dibujar la región factible"
            ],
            "correcta": 1,
            "explicacion": (
                "El algoritmo húngaro encuentra una asignación óptima "
                "en problemas de asignación, como trabajadores a tareas."
            )
        },
        {
            "tema": "Inventarios EOQ",
            "pregunta": (
                "Si D = 1200, S = 50 y H = 4, ¿cuál es aproximadamente "
                "la cantidad económica de pedido?"
            ),
            "opciones": [
                "100 unidades",
                "150 unidades",
                "173.21 unidades",
                "300 unidades"
            ],
            "correcta": 2,
            "explicacion": (
                "EOQ = √(2DS/H) = √(2 × 1200 × 50 / 4) "
                "= √30000 ≈ 173.21 unidades."
            )
        },
        {
            "tema": "Punto de reorden",
            "pregunta": (
                "Si la demanda es de 20 unidades diarias, el tiempo "
                "de entrega es 5 días y no hay inventario de seguridad, "
                "¿cuál es el punto de reorden?"
            ),
            "opciones": [
                "4 unidades",
                "25 unidades",
                "100 unidades",
                "120 unidades"
            ],
            "correcta": 2,
            "explicacion": (
                "ROP = demanda diaria × tiempo de entrega = 20 × 5 "
                "= 100 unidades."
            )
        }
    ]

    
    # Registrar el progreso del estudiante durante la sesión
    if "tutor_historial" not in st.session_state:
        st.session_state["tutor_historial"] = []

    st.subheader("📚 Banco de ejercicios")
    st.write(
        "Selecciona un ejercicio, responde y recibe una explicación "
        "inmediata para aprender de tus errores."
    )

    nombres_ejercicios = [
        f"{i + 1}. {ej['tema']} — {ej['pregunta']}"
        for i, ej in enumerate(ejercicios)
    ]

    indice = st.selectbox(
        "Selecciona un ejercicio",
        range(len(ejercicios)),
        format_func=lambda i: nombres_ejercicios[i],
        key="tutor_ejercicio"
    )

    ejercicio = ejercicios[indice]

    st.markdown(f"**Tema:** {ejercicio['tema']}")
    st.markdown(f"**Pregunta:** {ejercicio['pregunta']}")

    respuesta = st.radio(
        "Selecciona tu respuesta:",
        range(len(ejercicio["opciones"])),
        format_func=lambda i: ejercicio["opciones"][i],
        key=f"tutor_respuesta_{indice}"
    )


    if st.button("Comprobar respuesta", key="tutor_comprobar"):
        st.session_state["tutor_resultado"] = {
            "indice": indice,
            "respuesta": respuesta
        }

        st.session_state["tutor_historial"].append({
            "correcta": respuesta == ejercicio["correcta"]
        })


    resultado = st.session_state.get("tutor_resultado")

    if resultado is not None and resultado["indice"] == indice:
        if resultado["respuesta"] == ejercicio["correcta"]:
            st.success("¡Correcto! Muy bien.")
        else:
            st.error("Respuesta incorrecta. Revisa la explicación.")

        st.write(
            "**Respuesta correcta:** "
            + ejercicio["opciones"][ejercicio["correcta"]]
        )
        st.info(ejercicio["explicacion"])

    st.divider()
    st.subheader("🎲 Generador de práctica")

    st.write(
        "Genera una pregunta aleatoria del banco y practica "
        "con diferentes ejercicios."
    )

    if st.button("Generar ejercicio aleatorio", key="tutor_generar"):
        st.session_state["tutor_aleatorio"] = random.randrange(
            len(ejercicios)
        )
        st.session_state.pop("tutor_resultado_aleatorio", None)

    if "tutor_aleatorio" in st.session_state:
        indice_aleatorio = st.session_state["tutor_aleatorio"]
        ejercicio_aleatorio = ejercicios[indice_aleatorio]

        st.markdown(f"**Tema:** {ejercicio_aleatorio['tema']}")
        st.markdown(f"**Pregunta:** {ejercicio_aleatorio['pregunta']}")

        respuesta_aleatoria = st.radio(
            "Tu respuesta:",
            range(len(ejercicio_aleatorio["opciones"])),
            format_func=lambda i: ejercicio_aleatorio["opciones"][i],
            key=f"tutor_aleatorio_resp_{indice_aleatorio}"
        )

        if st.button(
            "Evaluar ejercicio generado",
            key="tutor_evaluar_aleatorio"
        ):
            st.session_state["tutor_resultado_aleatorio"] = {
                "indice": indice_aleatorio,
                "respuesta": respuesta_aleatoria
            }

            st.session_state["tutor_historial"].append({
                "correcta": (
                    respuesta_aleatoria
                    == ejercicio_aleatorio["correcta"]
                )
            })

        resultado_aleatorio = st.session_state.get(
            "tutor_resultado_aleatorio"
        )

        if (
            resultado_aleatorio is not None
            and resultado_aleatorio["indice"] == indice_aleatorio
        ):
            if (
                resultado_aleatorio["respuesta"]
                == ejercicio_aleatorio["correcta"]
            ):
                st.success("¡Correcto! Has resuelto el ejercicio.")
            else:
                st.error("No es correcto. Repasa el procedimiento.")

            st.write(
                "**Respuesta correcta:** "
                + ejercicio_aleatorio["opciones"][
                    ejercicio_aleatorio["correcta"]
                ]
            )
            st.info(ejercicio_aleatorio["explicacion"])

    st.caption(
        "Este tutor utiliza ejercicios estructurados y retroalimentación "
        "preparada. El generador selecciona una pregunta aleatoria del "
        "banco; no genera enunciados ilimitados."
    )


    st.divider()
    st.subheader("📊 Mi progreso")

    historial = st.session_state["tutor_historial"]
    total_respuestas = len(historial)
    total_correctas = sum(
        1 for intento in historial if intento["correcta"]
    )
    total_incorrectas = total_respuestas - total_correctas

    porcentaje = (
        total_correctas / total_respuestas * 100
        if total_respuestas > 0
        else 0
    )

    st.markdown(
        f"""
        <div class="tutor-progreso-flotante">
            <div class="titulo">📊 Tu progreso</div>
            <div class="datos">
                <span>Respondidas: {total_respuestas}</span>
                <span>Correctas: {total_correctas}</span>
            </div>
            <div class="porcentaje">{porcentaje:.1f}%</div>
            <div class="barra">
                <div class="relleno" style="width: {porcentaje}%;"></div>
            </div>
            <div style="font-size:0.75rem; margin-top:6px;">
                Incorrectas: {total_incorrectas}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )



    st.divider()
    st.subheader("🧮 Práctica numérica variable")

    st.write(
        "Genera ejercicios nuevos de sustitución en la función "
        "objetivo. Los valores cambian en cada generación."
    )

    if st.button(
        "Crear nuevo ejercicio numérico",
        key="tutor_numerico_generar"
    ):
        coef_x = random.randint(10, 50)
        coef_y = random.randint(10, 40)
        valor_x = random.randint(1, 10)
        valor_y = random.randint(1, 10)

        resultado_correcto = (
            coef_x * valor_x + coef_y * valor_y
        )

        opciones = {
            resultado_correcto,
            resultado_correcto + random.randint(5, 20),
            resultado_correcto - random.randint(5, 20),
            resultado_correcto + random.randint(21, 40)
        }

        while len(opciones) < 4:
            opciones.add(
                resultado_correcto + random.randint(-50, 50)
            )

        opciones = list(opciones)
        random.shuffle(opciones)

        st.session_state["tutor_numerico"] = {
            "coef_x": coef_x,
            "coef_y": coef_y,
            "x": valor_x,
            "y": valor_y,
            "correcta": resultado_correcto,
            "opciones": opciones
        }

        st.session_state.pop("tutor_numerico_resultado", None)
        st.session_state["tutor_numerico_version"] = (
            st.session_state.get("tutor_numerico_version", 0) + 1
        )

    if "tutor_numerico" in st.session_state:
        ejercicio_num = st.session_state["tutor_numerico"]

        st.markdown(
            f"**Problema:** Calcula "
            f"Z = {ejercicio_num['coef_x']}x + "
            f"{ejercicio_num['coef_y']}y cuando "
            f"x = {ejercicio_num['x']} e "
            f"y = {ejercicio_num['y']}."
        )

        st.latex(
            rf"Z={ejercicio_num['coef_x']}({ejercicio_num['x']})"
            rf"+{ejercicio_num['coef_y']}({ejercicio_num['y']})"
        )

        version_num = st.session_state.get(
            "tutor_numerico_version", 0
        )

        respuesta_num = st.radio(
            "Selecciona el resultado:",
            ejercicio_num["opciones"],
            key=f"tutor_numerico_respuesta_{version_num}"
        )

        if st.button(
            "Evaluar respuesta numérica",
            key="tutor_numerico_evaluar"
        ):
            es_correcta = (
                respuesta_num == ejercicio_num["correcta"]
            )

            st.session_state["tutor_numerico_resultado"] = {
                "correcta": es_correcta
            }

            st.session_state["tutor_historial"].append({
                "correcta": es_correcta
            })

        resultado_num = st.session_state.get(
            "tutor_numerico_resultado"
        )

        if resultado_num is not None:
            if resultado_num["correcta"]:
                st.success("¡Correcto! El cálculo es correcto.")
            else:
                st.error("Respuesta incorrecta. Revisa la sustitución.")

            st.write(
                f"**Respuesta correcta:** "
                f"{ejercicio_num['correcta']}"
            )

            st.info(
                f"Procedimiento: Z = "
                f"{ejercicio_num['coef_x']} × {ejercicio_num['x']} "
                f"+ {ejercicio_num['coef_y']} × {ejercicio_num['y']} "
                f"= {ejercicio_num['coef_x'] * ejercicio_num['x']} "
                f"+ {ejercicio_num['coef_y'] * ejercicio_num['y']} "
                f"= {ejercicio_num['correcta']}."
            )


else:
    st.header(modulo)
    st.warning(
        "Este módulo está en construcción. Lo desarrollaremos "
        "progresivamente."
    )






if modulo != "Inicio":
    mostrar_tutor_ia(modulo)

st.divider()
st.caption(
    "JB OptiMid | Proyecto de Investigación de Operaciones | "
    "Universidad Mariano Gálvez de Guatemala"
)
st.caption(
    "Ingeniera en Sistemas y Ciencias de la Computación | Sección: A"
)
st.caption(
    "Bryan Giancarlo Canil Hernández | "
    "John Jairon Antonio Ortega Crúz"
)

