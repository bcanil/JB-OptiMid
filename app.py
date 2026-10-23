
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.optimize import linprog
from scipy.optimize import linear_sum_assignment

st.set_page_config(
    page_title="OptiIO | Investigación de Operaciones",
    page_icon="📊",
    layout="wide"
)

st.title("📊 OptiIO")
st.write("Asistente Virtual de Investigación de Operaciones")
st.divider()

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


def resolver_modelo(objetivo, cx, cy, a1, b1, d1, a2, b2, d2):
    coeficientes = [-cx, -cy] if objetivo == "Maximizar" else [cx, cy]

    return linprog(
        c=coeficientes,
        A_ub=[[a1, b1], [a2, b2]],
        b_ub=[d1, d2],
        bounds=[(0, None), (0, None)],
        method="highs"
    )


def mostrar_grafica(cx, cy, a1, b1, d1, a2, b2, d2, x_opt, y_opt):
    # Calcula un rango que permita visualizar la solución
    valores_x = [0.0, x_opt]
    valores_y = [0.0, y_opt]

    for a, b, d in [(a1, b1, d1), (a2, b2, d2)]:
        if a > 0:
            valores_x.append(d / a)
        if b > 0:
            valores_y.append(d / b)

    xmax = max(valores_x) * 1.15 + 1
    ymax = max(valores_y) * 1.15 + 1

    xs = np.linspace(0, xmax, 300)
    ys = np.linspace(0, ymax, 300)
    X, Y = np.meshgrid(xs, ys)

    factible = (
        (a1 * X + b1 * Y <= d1 + 1e-9)
        & (a2 * X + b2 * Y <= d2 + 1e-9)
    )

    fig = go.Figure()

    # Sombrear la región que cumple todas las restricciones
    fig.add_trace(go.Scatter(
        x=X[factible],
        y=Y[factible],
        mode="markers",
        marker=dict(size=3, color="lightgreen", opacity=0.25),
        name="Región factible"
    ))

    # Dibujar las rectas de las restricciones
    for a, b, d, nombre in [
        (a1, b1, d1, "Restricción 1"),
        (a2, b2, d2, "Restricción 2")
    ]:
        if b != 0:
            y_recta = (d - a * xs) / b
            fig.add_trace(go.Scatter(
                x=xs,
                y=y_recta,
                mode="lines",
                name=nombre
            ))
        elif a != 0:
            x_recta = d / a
            fig.add_trace(go.Scatter(
                x=[x_recta, x_recta],
                y=[0, ymax],
                mode="lines",
                name=nombre
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


def calcular_vertices(a1, b1, d1, a2, b2, d2):
    # Candidatos iniciales: intersecciones con los ejes
    candidatos = [(0.0, 0.0)]

    # Intersecciones de cada restricción con los ejes
    for a, b, d in [(a1, b1, d1), (a2, b2, d2)]:
        if a != 0:
            candidatos.append((d / a, 0.0))

        if b != 0:
            candidatos.append((0.0, d / b))

    # Intersección de las dos rectas
    determinante = a1 * b2 - a2 * b1

    if abs(determinante) > 1e-9:
        x = (d1 * b2 - d2 * b1) / determinante
        y = (a1 * d2 - a2 * d1) / determinante
        candidatos.append((x, y))

    # Conservar solamente puntos factibles y evitar duplicados
    vertices = []

    for x, y in candidatos:
        if x < -1e-9 or y < -1e-9:
            continue

        if a1 * x + b1 * y > d1 + 1e-7:
            continue

        if a2 * x + b2 * y > d2 + 1e-7:
            continue

        punto = (max(0.0, x), max(0.0, y))

        if not any(
            abs(punto[0] - vx) < 1e-7
            and abs(punto[1] - vy) < 1e-7
            for vx, vy in vertices
        ):
            vertices.append(punto)

    return sorted(vertices, key=lambda punto: (punto[0], punto[1]))

if modulo == "Inicio":
    st.header("¡Bienvenido a OptiIO!")

    st.write(
        "Aprende, modela y resuelve problemas de Investigación "
        "de Operaciones mediante procedimientos paso a paso."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🧮 **Calcula**\n\nResuelve problemas con tus propios datos.")

    with col2:
        st.info("📈 **Comprende**\n\nConsulta fórmulas y procedimientos.")

    with col3:
        st.info("🎯 **Practica**\n\nPrepárate con ejercicios.")

elif modulo in ["Programación lineal", "Método gráfico"]:
    st.header("🧮 " + modulo)

    st.write(
        "Introduce los coeficientes de tu problema. Esta versión "
        "trabaja con dos variables y dos restricciones de tipo ≤."
    )

    objetivo = st.selectbox(
        "¿Qué deseas hacer?",
        ["Maximizar", "Minimizar"]
    )

    col1, col2 = st.columns(2)

    with col1:
        cx = st.number_input("Coeficiente de x en Z", value=40.0)
    with col2:
        cy = st.number_input("Coeficiente de y en Z", value=30.0)

    st.subheader("Restricciones")

    col1, col2, col3 = st.columns(3)

    with col1:
        a1 = st.number_input("R1: coeficiente de x", value=2.0)
        a2 = st.number_input("R2: coeficiente de x", value=1.0)

    with col2:
        b1 = st.number_input("R1: coeficiente de y", value=1.0)
        b2 = st.number_input("R2: coeficiente de y", value=2.0)

    with col3:
        d1 = st.number_input("R1: límite", value=100.0)
        d2 = st.number_input("R2: límite", value=80.0)

    st.subheader("Modelo matemático")

    palabra = "Maximizar" if objetivo == "Maximizar" else "Minimizar"
    st.latex(rf"\text{{{palabra}}}\quad Z={cx:g}x+{cy:g}y")
    st.latex(rf"{a1:g}x+{b1:g}y\leq {d1:g}")
    st.latex(rf"{a2:g}x+{b2:g}y\leq {d2:g}")
    st.latex(r"x,y\geq0")

    if st.button("Resolver problema", type="primary"):
        datos_validos = (
            all(np.isfinite(v) for v in [cx, cy, a1, b1, d1, a2, b2, d2])
            and (a1 != 0 or b1 != 0)
            and (a2 != 0 or b2 != 0)
            and d1 >= 0
            and d2 >= 0
        )

        if not datos_validos:
            st.error(
                "Revisa los datos: cada restricción debe tener al menos "
                "un coeficiente distinto de cero y límites no negativos."
            )
        else:
            resultado = resolver_modelo(
                objetivo, cx, cy, a1, b1, d1, a2, b2, d2
            )

            if resultado.success:
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
                st.latex(rf"Z={cx:g}({x:.4f})+{cy:g}({y:.4f})={z:.4f}")

                st.write("**2. Verificación de las restricciones**")
                valor1 = a1 * x + b1 * y
                valor2 = a2 * x + b2 * y

                st.latex(
                    rf"{a1:g}({x:.4f})+{b1:g}({y:.4f})"
                    rf"={valor1:.4f}\leq {d1:g}"
                )
                st.latex(
                    rf"{a2:g}({x:.4f})+{b2:g}({y:.4f})"
                    rf"={valor2:.4f}\leq {d2:g}"
                )

                st.success(
                    f"Solución encontrada: x = {x:.4f}, y = {y:.4f}, "
                    f"Z = {z:.4f}."
                )

                st.subheader("Gráfica")
                mostrar_grafica(
                    cx, cy, a1, b1, d1, a2, b2, d2, x, y
                )
		
		
                if modulo == "Método gráfico":
                    st.subheader("Tabla de vértices factibles")

                    vertices = calcular_vertices(
                        a1, b1, d1, a2, b2, d2
                    )

                    filas = []

                    for numero, (vx, vy) in enumerate(vertices, start=1):
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
                        "**Paso 1.** Se determinan las intersecciones "
                        "de las rectas con los ejes y entre sí."
                    )

                    st.write(
                        "**Paso 2.** Se comprueba cuáles puntos cumplen "
                        "todas las restricciones y la no negatividad."
                    )

                    st.write(
                        "**Paso 3.** Se evalúa la función objetivo "
                        "en cada vértice factible."
                    )

                    st.write("**Paso 4. Comparación de resultados**")

                    if vertices:
                        valores_z = [
                            cx * vx + cy * vy
                            for vx, vy in vertices
                        ]

                        if objetivo == "Maximizar":
                            mejor_z = max(valores_z)
                        else:
                            mejor_z = min(valores_z)

                        mejores = [
                            (vx, vy)
                            for (vx, vy), vz in zip(vertices, valores_z)
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
                                f"El vértice óptimo es "
                                f"({vx:.4f}, {vy:.4f}), "
                                f"con Z = {mejor_z:.4f}."
                            )
                        else:
                            st.success(
                                f"Hay múltiples vértices óptimos "
                                f"con el mismo valor Z = {mejor_z:.4f}."
                            )
                    else:
                        st.warning(
                            "No se encontraron vértices factibles."
                        )


            elif resultado.status == 3:
                st.error(
                    "El modelo no tiene un óptimo finito: la función "
                    "objetivo puede mejorar indefinidamente."
                )
            elif resultado.status == 2:
                st.error(
                    "El modelo no tiene solución factible con las "
                    "restricciones ingresadas."
                )
            else:
                st.error("No se pudo resolver el modelo. Revisa los datos.")


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
        if (a1 < 0 or b1 < 0 or a2 < 0 or b2 < 0):
            st.error(
                "Para esta versión, los coeficientes de las "
                "restricciones deben ser no negativos."
            )
        else:
            tabla, base, historial, terminado = resolver_simplex(
                c1, c2, a1, b1, d1, a2, b2, d2
            )

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
                            tabla_paso[i, j], 4
                        )

                    filas_tabla.append(fila)

                fila_z = {"Base": "Z"}

                for j, encabezado in enumerate(encabezados):
                    fila_z[encabezado] = round(
                        tabla_paso[2, j], 4
                    )

                filas_tabla.append(fila_z)

                st.dataframe(
                    filas_tabla,
                    use_container_width=True,
                    hide_index=True
                )

            if terminado:
                solucion = {"x": 0.0, "y": 0.0}

                for i, variable in enumerate(base):
                    if variable in solucion:
                        solucion[variable] = tabla[i, -1]

                x_opt = solucion["x"]
                y_opt = solucion["y"]
                z_opt = c1 * x_opt + c2 * y_opt

                st.subheader("Resultado final")
                r1, r2, r3 = st.columns(3)
                r1.metric("x óptimo", f"{x_opt:.4f}")
                r2.metric("y óptimo", f"{y_opt:.4f}")
                r3.metric("Z máximo", f"{z_opt:.4f}")

                st.success(
                    "El método Simplex alcanzó una solución óptima."
                )
            else:
                st.error(
                    "El modelo es no acotado o no se pudo completar "
                    "el procedimiento. Revisa las restricciones."
                )


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
                    st.dataframe(
                        envios,
                        hide_index=True,
                        column_config={
                            f"column_{j}": st.column_config.NumberColumn(
                                f"Destino {j+1}", format="%.2f"
                            )
                            for j in range(num_destinos)
                        }
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
                    st.write("4. Se resolvió el modelo mediante programación lineal.")
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

else:
    st.header(modulo)
    st.warning(
        "Este módulo está en construcción. Lo desarrollaremos "
        "progresivamente."
    )





st.divider()
st.caption(
    "OptiIO | Proyecto de Investigación de Operaciones | "
    "Universidad Mariano Gálvez de Guatemala"
)
