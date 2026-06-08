import streamlit as st
import pandas as pd
import math
import plotly.graph_objects as go
import plotly.express as px

# ---------------- CONFIGURACIÓN ----------------

st.set_page_config(
    page_title="Ruta Ahorro",
    page_icon="💰",
    layout="wide"
)
if "calculado" not in st.session_state:
    st.session_state.calculado = False

# ---------------- ESTILOS ----------------

st.markdown("""
<style>

/* Fondo general */
.stApp {
    background-color: var(--background-color);
}

/* Título principal */
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: var(--text-color);
    margin-bottom: 5px;
}

/* Subtítulo */
.subtitle {
    font-size: 20px;
    color: var(--text-color);
    opacity: 0.8;
    margin-bottom: 30px;
}

/* Cards */
.card {
    background-color: var(--secondary-background-color);
    padding: 28px;
    border-radius: 18px;
    border: 1px solid rgba(128,128,128,0.2);
    box-shadow: 0px 4px 12px rgba(0,0,0,0.04);
    min-height: 250px;
}

/* Iconos */
.icon-box {
    width: 58px;
    height: 58px;
    border-radius: 12px;
    background-color: rgba(76,175,80,0.15);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    margin-bottom: 18px;
}

/* Títulos dentro de cards */
.card h3 {
    color: var(--text-color);
    font-size: 22px;
    margin-bottom: 14px;
}

/* Texto dentro de cards */
.card p {
    color: var(--text-color);
    opacity: 0.85;
    font-size: 17px;
    line-height: 1.7;
}

/* Títulos de sección */
.section-title {
    font-size: 28px;
    font-weight: 700;
    color: var(--text-color);
    margin-top: 30px;
    margin-bottom: 15px;
}

/* Métricas */
[data-testid="stMetric"] {
    background-color: var(--secondary-background-color);
    padding: 15px;
    border-radius: 15px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: var(--secondary-background-color);
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border-radius: 12px;
}

/* Plotly */
.js-plotly-plot {
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- FUNCIONES ----------------

def formato_moneda(valor, simbolo):
    valor_formateado = f"{valor:,.2f}"
    valor_formateado = valor_formateado.replace(",", "X")
    valor_formateado = valor_formateado.replace(".", ",")
    valor_formateado = valor_formateado.replace("X", ".")
    return f"{simbolo} {valor_formateado}"

def calcular_monto_invertido(aporte_mensual, tasa_anual, plazo_meses):
    tasa_mensual = (1 + tasa_anual) ** (1 / 12) - 1
    acumulado = 0

    for mes in range(1, plazo_meses + 1):
        acumulado = (acumulado + aporte_mensual) * (1 + tasa_mensual)

    return acumulado

# ---------------- ENCABEZADO ----------------

st.markdown('<div class="main-title">💰 Ruta Ahorro</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Planificá tu objetivo de ahorro con una hoja de ruta financiera simple, visual y personalizada.</div>',
    unsafe_allow_html=True
)

# ---------------- CARDS INICIALES ----------------

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <div class="icon-box">🎯</div>
        <h3>Plan de ahorro personalizado</h3>
        <p>Ingresás tu objetivo, ingresos y gastos. Ruta Ahorro calcula cuánto necesitás ahorrar por mes, si tu meta es realista en el plazo deseado y qué ajustes hacer si no cierra.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="icon-box" style="background-color:#fff0d9;">🗺️</div>
        <h3>Hoja de ruta por etapas</h3>
        <p>No todos parten del mismo lugar. Ruta Ahorro detecta en qué etapa estás —deudas, emergencia, ahorro o inversión— y te guía paso a paso con acciones concretas.</p>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="card">
        <div class="icon-box" style="background-color:#fde4e4;">📊</div>
        <h3>Simulador de escenarios</h3>
        <p>Probá qué pasa si ahorrás más, reducís gastos o invertís tu ahorro. Visualizá el impacto de cada decisión antes de tomarla, sin riesgos.</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
        <div class="icon-box" style="background-color:#e9e6ff;">📈</div>
        <h3>Inversión según perfil</h3>
        <p>La app compara alternativas de inversión según tu perfil y tasas estimadas de mercado para proyectar si podés llegar antes a tu objetivo.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------- FORMULARIO ----------------

st.markdown('<div class="section-title">📝 Cargá tus datos</div>', unsafe_allow_html=True)

objetivo = st.text_input("¿Cuál es tu objetivo de ahorro?")

moneda = st.selectbox(
    "Elegí la moneda",
    ["Pesos argentinos ($)", "Dólares (US$)", "Euros (€)"]
)

if moneda == "Pesos argentinos ($)":
    simbolo = "$"
elif moneda == "Dólares (US$)":
    simbolo = "US$"
else:
    simbolo = "€"

col_a, col_b = st.columns(2)

with col_a:
    monto_objetivo = st.number_input(
        f"¿Cuánto dinero necesitás ahorrar? {simbolo}",
        min_value=0.0,
        step=1000.0,
        format="%.2f"
    )

    ingreso_mensual = st.number_input(
        f"¿Cuál es tu ingreso mensual? {simbolo}",
        min_value=0.0,
        step=1000.0,
        format="%.2f"
    )

with col_b:
    plazo_meses = st.number_input(
        "¿En cuántos meses querés lograrlo?",
        min_value=1,
        step=1
    )

    gastos_mensuales = st.number_input(
        f"¿Cuánto gastás aproximadamente por mes? {simbolo}",
        min_value=0.0,
        step=1000.0,
        format="%.2f"
    )

porcentaje_ahorro_elegido = st.slider(
    "¿Qué porcentaje de tu ingreso querés ahorrar por mes?",
    min_value=1,
    max_value=80,
    value=20,
    step=1
)

perfil = st.selectbox(
    "¿Cuál es tu perfil financiero?",
    ["Conservador", "Moderado", "Arriesgado"]
)

st.divider()

# ---------------- CÁLCULO ----------------

if st.button("Calcular mi plan de ahorro"):
    st.session_state.calculado = True

if st.session_state.calculado:
        
    st.session_state.objetivo = objetivo
    st.session_state.monto_objetivo = monto_objetivo
    st.session_state.plazo_meses = plazo_meses
    st.session_state.ingreso_mensual = ingreso_mensual
    st.session_state.gastos_mensuales = gastos_mensuales
    st.session_state.perfil = perfil
    st.session_state.simbolo = simbolo

if objetivo.strip() == "":
    st.error("Por favor ingresá un objetivo de ahorro.")

elif monto_objetivo <= 0:
    st.error("El monto objetivo debe ser mayor a 0.")

elif ingreso_mensual <= 0:
    st.error("El ingreso mensual debe ser mayor a 0.")

else:

    dinero_disponible = ingreso_mensual - gastos_mensuales
    ahorro_necesario = monto_objetivo / plazo_meses
    ahorro_segun_porcentaje = ingreso_mensual * (porcentaje_ahorro_elegido / 100)

    porcentaje_ahorro_disponible = (dinero_disponible / ingreso_mensual) * 100
    porcentaje_necesario = (ahorro_necesario / ingreso_mensual) * 100

    meses_estimados = monto_objetivo / ahorro_segun_porcentaje

    
# ---------------- RESULTADOS ----------------
    
st.markdown(
        '<div class="section-title">🎯 Plan de ahorro personalizado</div>',
        unsafe_allow_html=True
    )
    
col1, col2, col3, col4 = st.columns(4)
    
col1.metric("Monto objetivo", formato_moneda(monto_objetivo, simbolo))
col2.metric("Ahorro necesario", formato_moneda(ahorro_necesario, simbolo))
col3.metric("Disponible mensual", formato_moneda(dinero_disponible, simbolo))
col4.metric("Ahorro elegido", formato_moneda(ahorro_segun_porcentaje, simbolo))

st.write("**Objetivo:**", objetivo)
st.write("**Porcentaje necesario para cumplir el objetivo:**", round(porcentaje_necesario, 2), "%")
st.write("**Porcentaje disponible actual:**", round(porcentaje_ahorro_disponible, 2), "%")
st.write("**Meses estimados con el porcentaje elegido:**", round(meses_estimados, 1), "meses")

st.divider()
    
# ---------------- DIAGNÓSTICO ----------------

st.markdown('<div class="section-title">✅ Diagnóstico financiero</div>', unsafe_allow_html=True)

if gastos_mensuales > ingreso_mensual:
        st.error("Tus gastos son mayores que tus ingresos. Primero necesitás ordenar tus finanzas.")
elif dinero_disponible <= 0:
        st.error("Actualmente no tenés dinero disponible para ahorrar.")
elif dinero_disponible < ahorro_segun_porcentaje:
        st.warning("El porcentaje de ahorro elegido supera tu dinero disponible mensual.")
        st.write("Reducí el porcentaje de ahorro o revisá tus gastos.")
elif ahorro_segun_porcentaje >= ahorro_necesario:
        st.success("Con el porcentaje de ahorro elegido, tu objetivo es viable.")
else:
        st.error("Con el porcentaje de ahorro elegido, no llegarías al objetivo en el plazo planteado.")
        st.write("Podés aumentar el ahorro, extender el plazo o reducir el monto objetivo.")

if porcentaje_necesario <= 20:
        st.success("El esfuerzo requerido es bajo o moderado.")
elif porcentaje_necesario <= 40:
        st.warning("El esfuerzo requerido es alto.")
else:
        st.error("El esfuerzo requerido es muy alto.")

st.divider()
# ---------------- DIAGNÓSTICO ----------------

st.markdown('<div class="section-title">✅ Diagnóstico financiero</div>', unsafe_allow_html=True)

if gastos_mensuales > ingreso_mensual:
        st.error("Tus gastos son mayores que tus ingresos. Primero necesitás ordenar tus finanzas.")
elif dinero_disponible <= 0:
        st.error("Actualmente no tenés dinero disponible para ahorrar.")
elif dinero_disponible < ahorro_segun_porcentaje:
        st.warning("El porcentaje de ahorro elegido supera tu dinero disponible mensual.")
        st.write("Reducí el porcentaje de ahorro o revisá tus gastos.")
elif ahorro_segun_porcentaje >= ahorro_necesario:
        st.success("Con el porcentaje de ahorro elegido, tu objetivo es viable.")
else:
        st.error("Con el porcentaje de ahorro elegido, no llegarías al objetivo en el plazo planteado.")
        st.write("Podés aumentar el ahorro, extender el plazo o reducir el monto objetivo.")

if porcentaje_necesario <= 20:
        st.success("El esfuerzo requerido es bajo o moderado.")
elif porcentaje_necesario <= 40:
        st.warning("El esfuerzo requerido es alto.")
else:
        st.error("El esfuerzo requerido es muy alto.")

st.divider()

# ---------------- HOJA DE RUTA ----------------

st.markdown('<div class="section-title">🗺️ Hoja de ruta por etapas</div>', unsafe_allow_html=True)

if dinero_disponible <= 0:
        etapa = "Ordenar gastos"
        pasos = [
            "Revisar gastos fijos.",
            "Eliminar consumos innecesarios.",
            "Evitar tomar nueva deuda.",
            "Buscar generar un margen mensual positivo."
        ]
elif dinero_disponible < ahorro_necesario:
        etapa = "Ajustar capacidad de ahorro"
        pasos = [
            "Reducir gastos variables.",
            "Aumentar gradualmente el porcentaje de ahorro.",
            "Extender el plazo del objetivo.",
            "Revisar si el monto objetivo es realista."
        ]
elif perfil == "Conservador":
        etapa = "Ahorrar de forma segura"
        pasos = [
            "Separar el ahorro apenas cobrás.",
            "Crear o mantener un fondo de emergencia.",
            "Usar instrumentos de bajo riesgo.",
            "Revisar el avance mes a mes."
        ]
else:
        etapa = "Ahorrar e invertir"
        pasos = [
            "Separar el ahorro mensual definido.",
            "Mantener un fondo de emergencia.",
            "Invertir según tu perfil.",
            "Comparar rendimiento esperado contra el objetivo."
        ]

st.info(f"**Etapa detectada:** {etapa}")

for i, paso in enumerate(pasos, start=1):
        st.write(f"{i}. {paso}")

st.divider()

# ---------------- SIMULADOR ----------------

st.markdown(
        '<div class="section-title">📊 Simulador de escenarios</div>',
        unsafe_allow_html=True
    )

st.sidebar.header("🎛️ Centro de simulación")

escenario_ahorro_extra = st.sidebar.slider(
    "Aumentar ahorro mensual (%)",
    min_value=0,
    max_value=50,
    value=10,
    step=5
    )

escenario_reduccion_gastos = st.sidebar.slider(
    "Reducir gastos (%)",
    min_value=0,
    max_value=50,
    value=10,
    step=5
    )

ingreso_extra = st.sidebar.slider(
    "Ingreso adicional mensual",
    min_value=0,
    max_value=500000,
    value=0,
    step=10000
    )

nuevo_ingreso = ingreso_mensual + ingreso_extra

ahorro_extra = (
nuevo_ingreso *
(porcentaje_ahorro_elegido / 100)
) * (
1 + escenario_ahorro_extra / 100
)

gastos_reducidos = gastos_mensuales * (
1 - escenario_reduccion_gastos / 100
)

nuevo_disponible = nuevo_ingreso - gastos_reducidos

st.write(
"**Ahorro mensual con aumento simulado:**",
formato_moneda(ahorro_extra, simbolo)
)

st.write(
"**Dinero disponible si reducís gastos:**",
formato_moneda(nuevo_disponible, simbolo)
)

meses = list(range(1, plazo_meses + 1))

datos_proyeccion = pd.DataFrame({
    "Mes": meses,
    "Ahorro actual": [
        ahorro_segun_porcentaje * mes
        for mes in meses
    ],
    "Ahorro con mejora": [
        ahorro_extra * mes
        for mes in meses
    ],
    "Objetivo": [monto_objetivo] * plazo_meses
})

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=datos_proyeccion["Mes"],
        y=datos_proyeccion["Ahorro actual"],
        mode="lines",
        name="Ahorro actual"
    )
)

fig.add_trace(
    go.Scatter(
        x=datos_proyeccion["Mes"],
        y=datos_proyeccion["Ahorro con mejora"],
        mode="lines",
        name="Escenario mejorado"
    )
)

fig.add_trace(
    go.Scatter(
        x=datos_proyeccion["Mes"],
        y=datos_proyeccion["Objetivo"],
        mode="lines",
        name="Objetivo"
    )
)

fig.update_layout(
    paper_bgcolor="#f5f1ea",
    plot_bgcolor="#ffffff",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown(
    '<div class="section-title">🎯 Probabilidad de éxito</div>',
    unsafe_allow_html=True
)

if ahorro_necesario > 0:
    probabilidad = min(
    int((ahorro_extra / ahorro_necesario) * 100),
    100
)
else:
    probabilidad = 0

    st.progress(probabilidad)

    st.write(
        f"Probabilidad estimada de alcanzar el objetivo: {probabilidad}%"
    )

if probabilidad >= 100:
        st.success("Alta probabilidad de éxito.")
elif probabilidad >= 70:
        st.warning("Probabilidad moderada.")
else:
        st.error("Probabilidad baja.")

    st.divider()

# ---------------- COMPARACIÓN ----------------

st.markdown(
        '<div class="section-title">📊 Comparación mensual</div>',
        unsafe_allow_html=True
    )

    datos_comparacion = pd.DataFrame({
        "Concepto": [
            "Ahorro necesario",
            "Ahorro elegido",
            "Dinero disponible",
            "Ahorro con mejora"
        ],
        "Monto": [
            ahorro_necesario,
            ahorro_segun_porcentaje,
            dinero_disponible,
            ahorro_extra
        ]
    })

    fig_bar = go.Figure()

    fig_bar.add_trace(
        go.Bar(
            x=datos_comparacion["Concepto"],
            y=datos_comparacion["Monto"],
            text=[
                formato_moneda(valor, simbolo)
                for valor in datos_comparacion["Monto"]
            ],
            textposition="outside",
            name="Monto"
        )
    )

    fig_bar.update_layout(
        title="Comparación financiera mensual",
        paper_bgcolor="#f5f1ea",
        plot_bgcolor="#ffffff",
        height=500,
        xaxis_title="Concepto",
        yaxis_title=f"Monto ({simbolo})"
    )

st.plotly_chart(
    fig_bar,
    use_container_width=True
    )

st.divider()
# ---------------- INVERSIÓN ----------------

st.markdown(
    '<div class="section-title">📈 Inversión según perfil y mercado</div>',
    unsafe_allow_html=True
    )

    tasas_mercado = {
        "Billetera remunerada": 0.28,
        "Plazo fijo": 0.32,
        "Fondo común conservador": 0.40,
        "Bonos": 0.55,
        "CEDEARs / Acciones": 0.75
    }
if perfil == "Conservador":
        opciones_recomendadas = [
            "Billetera remunerada",
            "Plazo fijo",
            "Fondo común conservador"
        ]
        descripcion_perfil = "Tu perfil prioriza estabilidad y menor riesgo."

elif perfil == "Moderado":
        opciones_recomendadas = [
            "Fondo común conservador",
            "Bonos"
        ]
        descripcion_perfil = "Tu perfil acepta cierto riesgo a cambio de mayor rendimiento."

else:
        opciones_recomendadas = [
            "Bonos",
            "CEDEARs / Acciones"
        ]
        descripcion_perfil = "Tu perfil acepta mayor volatilidad buscando rendimientos superiores."

    st.write(descripcion_perfil)

    resultados_inversion = []
    mejor_opcion = None
    mejor_monto = 0
    mejor_tasa = 0

    for opcion in opciones_recomendadas:
        tasa_anual = tasas_mercado[opcion]
        monto_proyectado = calcular_monto_invertido(
            ahorro_segun_porcentaje,
            tasa_anual,
            plazo_meses
        )

        resultados_inversion.append({
            "Instrumento": opcion,
            "Tasa anual estimada": round(tasa_anual * 100, 2),
            "Monto proyectado": monto_proyectado
        })

        if monto_proyectado > mejor_monto:
            mejor_monto = monto_proyectado
            mejor_opcion = opcion
            mejor_tasa = tasa_anual

    tabla_resultados = pd.DataFrame(resultados_inversion)

    tabla_mostrar = tabla_resultados.copy()
    tabla_mostrar["Tasa anual estimada"] = tabla_mostrar["Tasa anual estimada"].apply(lambda x: f"{x}%")
    tabla_mostrar["Monto proyectado"] = tabla_mostrar["Monto proyectado"].apply(lambda x: formato_moneda(x, simbolo))

    st.dataframe(tabla_mostrar, use_container_width=True)

    st.success(
        f"Según tu perfil y las tasas estimadas de mercado, la alternativa más conveniente sería: **{mejor_opcion}**."
    )

    st.write("**Tasa anual estimada:**", round(mejor_tasa * 100, 2), "%")
    st.write("**Monto proyectado al final del plazo:**", formato_moneda(mejor_monto, simbolo))

    if mejor_monto >= monto_objetivo:
        st.success("Con esta alternativa podrías alcanzar tu objetivo financiero.")
    else:
        st.warning("Incluso con esta alternativa, no alcanzarías el objetivo en el plazo planteado.")

    tasa_mensual_mejor = (1 + mejor_tasa) ** (1 / 12) - 1

    ahorro_sin_invertir = []
    ahorro_con_inversion = []

    acumulado_simple = 0
    acumulado_invertido = 0

    for mes in meses:
        acumulado_simple += ahorro_segun_porcentaje
        acumulado_invertido = (acumulado_invertido + ahorro_segun_porcentaje) * (1 + tasa_mensual_mejor)

        ahorro_sin_invertir.append(acumulado_simple)
        ahorro_con_inversion.append(acumulado_invertido)

    datos_inversion = pd.DataFrame({
        "Mes": meses,
        "Ahorro sin invertir": ahorro_sin_invertir,
        "Ahorro invertido": ahorro_con_inversion,
        "Objetivo": [monto_objetivo] * plazo_meses
    })

    fig_inversion = go.Figure()

    fig_inversion.add_trace(
        go.Scatter(
            x=datos_inversion["Mes"],
            y=datos_inversion["Ahorro sin invertir"],
            mode="lines",
            name="Ahorro sin invertir",
            line=dict(
                color="#6C757D",
                width=3
            )
        )
    )

    fig_inversion.add_trace(
        go.Scatter(
            x=datos_inversion["Mes"],
            y=datos_inversion["Ahorro invertido"],
            mode="lines",
            name="Ahorro invertido",
            line=dict(
                color="#D4A373",
                width=4
            )
        )
    )

    fig_inversion.add_trace(
        go.Scatter(
            x=datos_inversion["Mes"],
            y=datos_inversion["Objetivo"],
            mode="lines",
            name="Objetivo",
            line=dict(
                color="#2E8B57",
                width=3,
                dash="dash"
            )
        )
    )

    fig_inversion.update_layout(
        title="Evolución del ahorro con inversión",
        paper_bgcolor="#f5f1ea",
        plot_bgcolor="#ffffff",
        height=550,
        xaxis_title="Mes",
        yaxis_title=f"Monto ({simbolo})",
        hovermode="x unified"
    )

st.plotly_chart(
        fig_inversion,
        use_container_width=True
    )
st.caption(
        "Las tasas utilizadas son estimativas y sirven para simular escenarios. "
        "No constituyen asesoramiento financiero profesional."
    )

st.success("Gracias por usar Ruta Ahorro 💰")
