python3 -c "
parts = []

parts.append('''import streamlit as st
import pandas as pd
import plotly.graph_objects as go
''')

parts.append('''
# ---- CONFIGURACION ----
st.set_page_config(page_title=\"Ruta Ahorro\", page_icon=\"💰\", layout=\"wide\")
if \"calculado\" not in st.session_state:
    st.session_state.calculado = False
''')

parts.append('''
# ---- ESTILOS ----
st.markdown(\"\"\"
<style>
.stApp { background-color: var(--background-color); }
.main-title { font-size: 42px; font-weight: 800; color: var(--text-color); margin-bottom: 5px; }
.subtitle { font-size: 20px; color: var(--text-color); opacity: 0.8; margin-bottom: 30px; }
.card { background-color: var(--secondary-background-color); padding: 28px; border-radius: 18px;
    border: 1px solid rgba(128,128,128,0.2); box-shadow: 0px 4px 12px rgba(0,0,0,0.04); min-height: 250px; }
.icon-box { width: 58px; height: 58px; border-radius: 12px; background-color: rgba(76,175,80,0.15);
    display: flex; align-items: center; justify-content: center; font-size: 28px; margin-bottom: 18px; }
.card h3 { color: var(--text-color); font-size: 22px; margin-bottom: 14px; }
.card p { color: var(--text-color); opacity: 0.85; font-size: 17px; line-height: 1.7; }
.section-title { font-size: 28px; font-weight: 700; color: var(--text-color); margin-top: 30px; margin-bottom: 8px; }
.section-intro { font-size: 15px; color: var(--text-color); opacity: 0.75; margin-bottom: 18px; line-height: 1.6; }
.moneda-badge { display: inline-block; background: rgba(76,175,80,0.18); color: #2e7d32;
    font-weight: 700; font-size: 13px; padding: 3px 12px; border-radius: 20px; margin-bottom: 18px; }
.instrumento-card { background-color: var(--secondary-background-color); border: 1px solid rgba(128,128,128,0.2);
    border-radius: 14px; padding: 18px 22px; margin-bottom: 14px; }
.instrumento-card h4 { margin: 0 0 6px 0; font-size: 17px; }
.instrumento-card p { margin: 0; font-size: 14px; opacity: 0.8; line-height: 1.5; }
.tasa-badge { display: inline-block; font-size: 13px; font-weight: 700; padding: 2px 10px; border-radius: 12px; margin-top: 8px; }
[data-testid=\"stMetric\"] { background-color: var(--secondary-background-color); padding: 15px; border-radius: 15px; }
section[data-testid=\"stSidebar\"] { background-color: var(--secondary-background-color); }
[data-testid=\"stDataFrame\"] { border-radius: 12px; }
.js-plotly-plot { border-radius: 15px; }
</style>
\"\"\", unsafe_allow_html=True)
''')

code = \"\".join(parts)
with open('/tmp/app_part1.py', 'w') as f:
    f.write(code)
print('part1 ok', len(code))
"
echo "exit $?"
Salida

part1 ok 2345
exit 0
python3 << 'SCRIPT'
part2 = """
# ---- FUNCIONES ----

def formato_moneda(valor, simbolo):
    v = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{simbolo} {v}"

def calcular_monto_invertido(aporte, tasa_anual, plazo):
    tasa_m = (1 + tasa_anual) ** (1/12) - 1
    ac = 0
    for _ in range(1, plazo + 1):
        ac = (ac + aporte) * (1 + tasa_m)
    return ac

# ---- DATOS INSTRUMENTOS ----

INFO_INST = {
    "Billetera remunerada": {
        "desc": ("Cuenta de inversion en billeteras digitales (Mercado Pago, Uala, Naranja X). "
                 "Tu dinero rinde desde el primer dia con liquidez inmediata. "
                 "Ideal para el fondo de emergencia."),
        "link": "https://www.argentina.gob.ar/economia/finanzas/mercado-de-capitales/instrumentos/cuentas-remuneradas",
        "link_lbl": "Como funcionan las cuentas remuneradas",
        "link_t": "https://www.bcra.gob.ar/PublicacionesEstadisticas/Principales_variables.asp",
        "link_t_lbl": "Tasas actuales BCRA",
        "color": "#43A047", "riesgo": "Muy bajo",
    },
    "Plazo fijo": {
        "desc": ("Deposito a termino en un banco durante un plazo acordado (generalmente 30 dias). "
                 "Capital e intereses garantizados por el FGD. "
                 "No podes rescatar antes del vencimiento."),
        "link": "https://www.bcra.gob.ar/SistemasFinancieros/sf_depbancos.asp",
        "link_lbl": "Como funciona el plazo fijo - BCRA",
        "link_t": "https://www.bcra.gob.ar/PublicacionesEstadisticas/Cuadros_estandar.asp",
        "link_t_lbl": "Tasas actuales de plazos fijos",
        "color": "#1E88E5", "riesgo": "Bajo",
    },
    "Fondo comun conservador": {
        "desc": ("Vehiculo de inversion colectiva que invierte en activos de bajo riesgo. "
                 "Rescate en 24-48 hs. Permite diversificacion con montos pequeños "
                 "y suele superar al plazo fijo en rendimiento."),
        "link": "https://www.cafci.org.ar/que-son-los-fci.html",
        "link_lbl": "Que son los Fondos Comunes de Inversion",
        "link_t": "https://www.cafci.org.ar/rendimientos.html",
        "link_t_lbl": "Rendimientos actuales de FCI",
        "color": "#FB8C00", "riesgo": "Bajo-Medio",
    },
    "Bonos": {
        "desc": ("Titulos de deuda del Estado o empresas que pagan un cupon periodico. "
                 "Los bonos CER protegen contra inflacion. Su precio fluctua en mercado secundario. "
                 "Mayor rendimiento que plazo fijo a cambio de mayor volatilidad."),
        "link": "https://www.argentina.gob.ar/economia/finanzas/mercado-de-capitales/instrumentos/bonos",
        "link_lbl": "Como funcionan los bonos - Ministerio de Economia",
        "link_t": "https://www.byma.com.ar/renta-fija/",
        "link_t_lbl": "Bonos con mayor tasa en BYMA",
        "color": "#8E24AA", "riesgo": "Medio-Alto",
    },
    "CEDEARs / Acciones": {
        "desc": ("Los CEDEARs replican acciones extranjeras (Apple, Google, etc.) en pesos "
                 "con cobertura cambiaria implicita respecto al dolar CCL. "
                 "Maximo potencial de rendimiento y maxima volatilidad posible."),
        "link": "https://www.argentina.gob.ar/economia/finanzas/mercado-de-capitales/instrumentos/cedears",
        "link_lbl": "Que son los CEDEARs - Ministerio de Economia",
        "link_t": "https://www.byma.com.ar/cedears/",
        "link_t_lbl": "CEDEARs mas operados en BYMA",
        "color": "#E53935", "riesgo": "Alto",
    },
}

TASAS = {
    "Billetera remunerada":    0.28,
    "Plazo fijo":              0.32,
    "Fondo comun conservador": 0.40,
    "Bonos":                   0.55,
    "CEDEARs / Acciones":      0.75,
}

PERFIL_OPCIONES = {
    "Conservador": ["Billetera remunerada", "Plazo fijo", "Fondo comun conservador"],
    "Moderado":    ["Fondo comun conservador", "Bonos"],
    "Arriesgado":  ["Bonos", "CEDEARs / Acciones"],
}

PERFILES_DESC = {
    "Conservador": ("Priorizas proteger tu capital. Preferes instrumentos seguros aunque rindan menos. "
                    "Ideal si no toleras perder parte de lo ahorrado, incluso temporalmente."),
    "Moderado":    ("Aceptas cierta variabilidad a cambio de mejores rendimientos. "
                    "Combinas instrumentos de bajo y mediano riesgo. Horizonte de mediano plazo."),
    "Arriesgado":  ("Buscas maximizar el rendimiento y aceptas alta volatilidad. "
                    "El valor puede subir o bajar fuerte en el corto plazo. Horizonte de largo plazo."),
}

PERFIL_EMOJI = {"Conservador": "🛡️", "Moderado": "⚖️", "Arriesgado": "🚀"}
"""

with open('/tmp/app_part2.py', 'w') as f:
    f.write(part2)
print("part2 ok", len(part2))
SCRIPT
Salida

part2 ok 4575

python3 << 'SCRIPT'
part3 = """
# ---- ENCABEZADO ----

st.markdown('<div class="main-title">💰 Ruta Ahorro</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Planifica tu objetivo de ahorro con una hoja de ruta financiera simple, visual y personalizada.</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown(\"\"\"<div class="card"><div class="icon-box">🎯</div>
        <h3>Plan de ahorro personalizado</h3>
        <p>Ingresas tu objetivo, ingresos y gastos. Ruta Ahorro calcula cuanto necesitas ahorrar por mes y si tu meta es realista en el plazo deseado.</p>
    </div>\"\"\", unsafe_allow_html=True)
with col2:
    st.markdown(\"\"\"<div class="card"><div class="icon-box" style="background-color:#fff0d9;">🗺️</div>
        <h3>Hoja de ruta por etapas</h3>
        <p>Ruta Ahorro detecta en que etapa estas hoy y te guia paso a paso con acciones concretas y ordenadas.</p>
    </div>\"\"\", unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    st.markdown(\"\"\"<div class="card"><div class="icon-box" style="background-color:#fde4e4;">📊</div>
        <h3>Simulador de escenarios</h3>
        <p>Visualiza el impacto de ahorrar mas, reducir gastos o sumar ingresos antes de tomar la decision.</p>
    </div>\"\"\", unsafe_allow_html=True)
with col4:
    st.markdown(\"\"\"<div class="card"><div class="icon-box" style="background-color:#e9e6ff;">📈</div>
        <h3>Inversion segun perfil</h3>
        <p>Compara alternativas segun tu perfil y proyecta si podes llegar antes al objetivo con interes compuesto.</p>
    </div>\"\"\", unsafe_allow_html=True)

st.divider()
"""

with open('/tmp/app_part3.py', 'w') as f:
    f.write(part3)
print("part3 ok", len(part3))
SCRIPT
Salida

part3 ok 1583

python3 << 'SCRIPT'
part4 = """
# ---- FORMULARIO ----

st.markdown('<div class="section-title">📝 Carga tus datos</div>', unsafe_allow_html=True)
st.markdown('<div class="section-intro">Completa los campos con tu situacion real. Cuanto mas precisos sean los datos, mas util sera el plan que genera Ruta Ahorro para vos.</div>', unsafe_allow_html=True)

objetivo = st.text_input("Cual es tu objetivo de ahorro?", placeholder="Ej: viaje, auto, fondo de emergencia...")

moneda = st.selectbox(
    "Elegi la moneda con la que vas a trabajar",
    ["Pesos argentinos ($)", "Dolares (US$)", "Euros (EUR)"],
    help="Esta moneda se mantiene en TODAS las secciones y calculos de la app."
)

MONEDA_SIM = {"Pesos argentinos ($)": "$", "Dolares (US$)": "US$", "Euros (EUR)": "EUR"}
simbolo = MONEDA_SIM[moneda]
st.session_state.simbolo = simbolo

st.markdown(
    f'<div class="moneda-badge">Moneda activa: {moneda} &mdash; todos los montos en {simbolo}</div>',
    unsafe_allow_html=True
)

col_a, col_b = st.columns(2)
with col_a:
    monto_objetivo = st.number_input(f"Cuanto dinero necesitas ahorrar? ({simbolo})", min_value=0.0, step=1000.0, format="%.2f")
    ingreso_mensual = st.number_input(f"Cual es tu ingreso mensual? ({simbolo})", min_value=0.0, step=1000.0, format="%.2f")
with col_b:
    plazo_meses = st.number_input("En cuantos meses queres lograrlo?", min_value=1, step=1)
    gastos_mensuales = st.number_input(f"Cuanto gastas por mes? ({simbolo})", min_value=0.0, step=1000.0, format="%.2f")
    pct_ahorro = st.slider("Que porcentaje de tu ingreso queres ahorrar?", min_value=1, max_value=80, value=20, step=1)
    perfil = st.selectbox("Cual es tu perfil de inversor?", ["Conservador", "Moderado", "Arriesgado"])

st.info(f"{PERFIL_EMOJI[perfil]} **{perfil}** — {PERFILES_DESC[perfil]}")

st.divider()

if st.button("🚀 Calcular mi plan de ahorro", use_container_width=True):
    st.session_state.calculado = True
"""

with open('/tmp/app_part4.py', 'w') as f:
    f.write(part4)
print("part4 ok", len(part4))
SCRIPT
Salida

part4 ok 1896

python3 << 'SCRIPT'
part5 = """
# ---- BLOQUE PRINCIPAL ----

if st.session_state.calculado:

    if objetivo.strip() == "":
        st.error("Por favor ingresa un objetivo de ahorro.")
        st.stop()
    if monto_objetivo <= 0:
        st.error("El monto objetivo debe ser mayor a 0.")
        st.stop()
    if ingreso_mensual <= 0:
        st.error("El ingreso mensual debe ser mayor a 0.")
        st.stop()

    st.session_state.update({
        "objetivo": objetivo, "monto_objetivo": monto_objetivo, "plazo_meses": plazo_meses,
        "ingreso_mensual": ingreso_mensual, "gastos_mensuales": gastos_mensuales,
        "perfil": perfil, "simbolo": simbolo,
    })

    disp         = ingreso_mensual - gastos_mensuales
    nec          = monto_objetivo / plazo_meses
    eleg         = ingreso_mensual * (pct_ahorro / 100)
    pct_disp     = (disp / ingreso_mensual) * 100
    pct_nec      = (nec / ingreso_mensual) * 100
    meses_est    = (monto_objetivo / eleg if eleg > 0 else float("inf"))
    meses        = list(range(1, plazo_meses + 1))

    st.markdown(f'<div class="moneda-badge">Todos los montos en: {moneda} ({simbolo})</div>', unsafe_allow_html=True)

    # ---- PLAN ----
    st.markdown('<div class="section-title">🎯 Plan de ahorro personalizado</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-intro">Estos cuatro numeros son el corazon de tu plan. '
        'El <b>ahorro necesario</b> es lo que tenes que guardar cada mes para cumplir el plazo. '
        'El <b>ahorro elegido</b> es lo que decidiste destinar segun tu porcentaje. '
        'Si el elegido es igual o mayor al necesario, tu objetivo es viable tal como esta planteado.</div>',
        unsafe_allow_html=True
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Monto objetivo",         formato_moneda(monto_objetivo, simbolo))
    c2.metric("Ahorro necesario / mes", formato_moneda(nec, simbolo))
    c3.metric("Disponible mensual",     formato_moneda(disp, simbolo))
    c4.metric("Ahorro elegido / mes",   formato_moneda(eleg, simbolo))
    st.write("**Objetivo:**", objetivo)
    st.write("**Porcentaje necesario:**",     round(pct_nec, 2), "%")
    st.write("**Porcentaje disponible:**",    round(pct_disp, 2), "%")
    st.write("**Meses estimados:**", round(meses_est, 1) if meses_est != float("inf") else "No calculable (ahorro = 0)")
    st.divider()

    # ---- DIAGNOSTICO ----
    st.markdown('<div class="section-title">✅ Diagnostico financiero</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-intro">El diagnostico evalua si tu situacion actual te permite cumplir el objetivo '
        f'en el plazo definido. Identifica el principal obstaculo para que puedas actuar sobre el antes de comenzar. '
        f'Todos los montos estan en <b>{simbolo}</b>.</div>',
        unsafe_allow_html=True
    )
    if gastos_mensuales > ingreso_mensual:
        st.error("Tus gastos superan tus ingresos. Antes de ahorrar, necesitas cerrar esa brecha.")
    elif disp <= 0:
        st.error("No tenes margen disponible para ahorrar con los datos ingresados.")
    elif disp < eleg:
        st.warning(f"El porcentaje elegido ({pct_ahorro}%) supera tu disponible ({formato_moneda(disp, simbolo)}). Reduce el porcentaje o los gastos.")
    elif eleg >= nec:
        st.success("Con el porcentaje de ahorro elegido, tu objetivo es totalmente viable.")
    else:
        st.error("Con el porcentaje elegido no alcanzarias el objetivo en el plazo planteado.")
        st.write("Podes aumentar el ahorro, extender el plazo o reducir el monto objetivo.")
    if pct_nec <= 20:
        st.success("El esfuerzo requerido es bajo o moderado (hasta 20% del ingreso).")
    elif pct_nec <= 40:
        st.warning("El esfuerzo requerido es alto (entre 20% y 40% del ingreso).")
    else:
        st.error("El esfuerzo requerido es muy alto (mas del 40% del ingreso).")
    st.divider()

    # ---- HOJA DE RUTA ----
    st.markdown('<div class="section-title">🗺️ Hoja de ruta por etapas</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-intro">No todas las personas estan en el mismo punto de partida. '
        'Esta seccion detecta en que etapa financiera estas hoy y te da pasos concretos y ordenados. '
        'Seguir este orden evita el error mas comun: intentar invertir antes de tener las bases solidas.</div>',
        unsafe_allow_html=True
    )
    if disp <= 0:
        etapa = "Ordenar gastos"
        pasos = [
            "Lista todos tus gastos fijos y variables del ultimo mes.",
            "Identifica y elimina consumos no esenciales.",
            "Evita tomar nueva deuda hasta tener margen positivo.",
            "Tu meta inmediata: que ingresos superen gastos cada mes."
        ]
    elif disp < nec:
        etapa = "Ajustar capacidad de ahorro"
        pasos = [
            "Reduce al menos un gasto variable esta semana.",
            "Aumenta el porcentaje de ahorro de a 2% por mes.",
            "Evalua si podes extender el plazo para reducir la presion mensual.",
            "Revisa si el monto objetivo puede ajustarse sin resignar lo esencial."
        ]
    elif perfil == "Conservador":
        etapa = "Ahorrar de forma segura"
        pasos = [
            "Separa el ahorro apenas cobras, antes de gastar.",
            "Construi un fondo de emergencia equivalente a 3 meses de gastos.",
            "Usa instrumentos de bajo riesgo: billetera remunerada o plazo fijo.",
            "Revisa tu avance cada 30 dias y ajusta si cambia tu situacion."
        ]
    else:
        etapa = "Ahorrar e invertir"
        pasos = [
            "Separa el ahorro mensual ni bien cobras.",
            "Asegurate de tener un fondo de emergencia ya constituido.",
            "Invierte el excedente segun los instrumentos recomendados para tu perfil.",
            "Compara mensualmente el rendimiento real contra tu objetivo."
        ]
    st.info(f"**Etapa detectada:** {etapa}")
    for i, paso in enumerate(pasos, start=1):
        st.write(f"{i}. {paso}")
    st.divider()
"""

with open('/tmp/app_part5.py', 'w') as f:
    f.write(part5)
print("part5 ok", len(part5))
SCRIPT
Salida

part5 ok 6070
python3 << 'SCRIPT'
part6 = """
    # ---- SIMULADOR ----
    st.markdown('<div class="section-title">📊 Simulador de escenarios</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-intro">Usa los controles del panel lateral para simular mejoras: '
        f'aumentar el porcentaje de ahorro, reducir gastos o sumar ingresos extra. '
        f'El grafico muestra como esos cambios impactan en la acumulacion mes a mes. '
        f'Moneda activa: <b>{simbolo}</b>.</div>',
        unsafe_allow_html=True
    )

    st.sidebar.header("🎛️ Centro de simulacion")
    st.sidebar.markdown(f"**Moneda: {simbolo}**")
    extra_pct  = st.sidebar.slider("Aumentar ahorro mensual (%)", 0, 50, 10, 5)
    reduc_gast = st.sidebar.slider("Reducir gastos (%)",          0, 50, 10, 5)
    ing_extra  = st.sidebar.slider(f"Ingreso adicional mensual ({simbolo})", 0, 500000, 0, 10000)

    nuevo_ing  = ingreso_mensual + ing_extra
    ahorro_sim = (nuevo_ing * (pct_ahorro / 100)) * (1 + extra_pct / 100)
    gast_red   = gastos_mensuales * (1 - reduc_gast / 100)
    nuevo_disp = nuevo_ing - gast_red

    st.write("**Ahorro mensual simulado:**",            formato_moneda(ahorro_sim, simbolo))
    st.write("**Disponible si reducis gastos:**",       formato_moneda(nuevo_disp, simbolo))

    dp = {
        "Mes":              meses,
        "Ahorro actual":    [eleg * m for m in meses],
        "Ahorro simulado":  [ahorro_sim * m for m in meses],
        "Objetivo":         [monto_objetivo] * plazo_meses,
    }
    import pandas as pd
    df_sim = pd.DataFrame(dp)

    import plotly.graph_objects as go
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_sim["Mes"], y=df_sim["Ahorro actual"],   mode="lines", name="Ahorro actual"))
    fig.add_trace(go.Scatter(x=df_sim["Mes"], y=df_sim["Ahorro simulado"], mode="lines", name="Escenario mejorado"))
    fig.add_trace(go.Scatter(x=df_sim["Mes"], y=df_sim["Objetivo"],        mode="lines", name="Objetivo",
                             line=dict(dash="dash", color="#2E8B57")))
    fig.update_layout(paper_bgcolor="#f5f1ea", plot_bgcolor="#ffffff", height=500,
                      xaxis_title="Mes", yaxis_title=f"Monto ({simbolo})", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    # Probabilidad
    st.markdown('<div class="section-title">🎯 Probabilidad de exito</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-intro">Este indicador estima cuanto del objetivo cubririas con el escenario simulado. '
        'Un 100% significa que el ahorro proyectado cubre o supera el monto necesario. '
        'Es una referencia orientativa basada en los datos que ingresaste.</div>',
        unsafe_allow_html=True
    )
    prob = min(int((ahorro_sim / nec) * 100), 100) if nec > 0 else 0
    st.progress(prob)
    st.write(f"Probabilidad estimada: **{prob}%**")
    if prob >= 100:
        st.success("Alta probabilidad de exito con el escenario simulado.")
    elif prob >= 70:
        st.warning("Probabilidad moderada. Ajusta un poco mas para asegurar el objetivo.")
    else:
        st.error("Probabilidad baja. Revisa los parametros del simulador.")
    st.divider()

    # Comparacion mensual
    st.markdown('<div class="section-title">📊 Comparacion mensual</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-intro">El grafico compara en un mismo vistazo los cuatro montos clave de tu plan '
        f'en <b>{simbolo}</b>: lo que necesitas, lo que elegiste, lo que tenes disponible y el escenario simulado.</div>',
        unsafe_allow_html=True
    )
    df_comp = pd.DataFrame({
        "Concepto": ["Ahorro necesario", "Ahorro elegido", "Disponible mensual", "Ahorro simulado"],
        "Monto":    [nec, eleg, disp, ahorro_sim],
    })
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=df_comp["Concepto"], y=df_comp["Monto"],
        text=[formato_moneda(v, simbolo) for v in df_comp["Monto"]], textposition="outside"
    ))
    fig_bar.update_layout(title="Comparacion financiera mensual", paper_bgcolor="#f5f1ea",
                          plot_bgcolor="#ffffff", height=500, xaxis_title="Concepto",
                          yaxis_title=f"Monto ({simbolo})")
    st.plotly_chart(fig_bar, use_container_width=True)
    st.divider()
"""

with open('/tmp/app_part6.py', 'w') as f:
    f.write(part6)
print("part6 ok", len(part6))
SCRIPT
Salida

part6 ok 4282
python3 << 'SCRIPT'
part7 = """
    # ---- INVERSION ----
    st.markdown('<div class="section-title">📈 Inversion segun perfil y mercado</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-intro">Invertir el ahorro en lugar de guardarlo sin rendir puede acercarte al objetivo '
        f'antes de lo previsto gracias al interes compuesto. Esta seccion proyecta cuanto acumularias '
        f'con cada instrumento recomendado para tu perfil <b>{perfil}</b>, en <b>{simbolo}</b>. '
        f'Las tasas son estimativas; usa los links de cada opcion para ver los valores vigentes en Argentina.</div>',
        unsafe_allow_html=True
    )

    st.markdown(f"**Tu perfil: {PERFIL_EMOJI[perfil]} {perfil}** — {PERFILES_DESC[perfil]}")
    st.markdown("---")

    opciones = PERFIL_OPCIONES[perfil]
    resultados = []
    mejor_op = None
    mejor_m  = 0
    mejor_t  = 0

    for op in opciones:
        tasa   = TASAS[op]
        proy   = calcular_monto_invertido(eleg, tasa, plazo_meses)
        info   = INFO_INST[op]
        resultados.append({"Instrumento": op, "Tasa anual estimada": round(tasa*100,2), "Monto proyectado": proy})
        if proy > mejor_m:
            mejor_m = proy
            mejor_op = op
            mejor_t  = tasa

        alcanza  = proy >= monto_objetivo
        b_color  = "#2e7d32" if alcanza else "#b71c1c"
        b_texto  = "Alcanza el objetivo" if alcanza else "No alcanza el objetivo"

        st.markdown(f\"\"\"
        <div class="instrumento-card">
            <h4 style="color:{info['color']};">{op}</h4>
            <p>{info['desc']}</p>
            <span class="tasa-badge" style="background:{info['color']}22;color:{info['color']};">
                Tasa estimada: {round(tasa*100,1)}% anual &nbsp;|&nbsp; Riesgo: {info['riesgo']}
            </span><br>
            <span class="tasa-badge" style="background:{b_color}22;color:{b_color};margin-top:6px;">
                {b_texto} &mdash; Proyectado: {formato_moneda(proy, simbolo)}
            </span>
            <br><br>
            <a href="{info['link']}" target="_blank">📖 {info['link_lbl']}</a>
            &nbsp;&nbsp;|&nbsp;&nbsp;
            <a href="{info['link_t']}" target="_blank">📊 {info['link_t_lbl']}</a>
        </div>
        \"\"\", unsafe_allow_html=True)

    st.markdown("---")
    import pandas as pd
    tabla = pd.DataFrame(resultados).copy()
    tabla["Tasa anual estimada"] = tabla["Tasa anual estimada"].apply(lambda x: f"{x}%")
    tabla["Monto proyectado"]    = tabla["Monto proyectado"].apply(lambda x: formato_moneda(x, simbolo))
    st.markdown('<div class="section-intro"><b>Resumen comparativo:</b></div>', unsafe_allow_html=True)
    st.dataframe(tabla, use_container_width=True)

    st.success(
        f"La alternativa con mayor proyeccion para tu perfil es: **{mejor_op}** "
        f"| Tasa estimada: {round(mejor_t*100,2)}% anual "
        f"| Proyectado al mes {plazo_meses}: {formato_moneda(mejor_m, simbolo)}"
    )
    if mejor_m >= monto_objetivo:
        st.success("Con esta alternativa podrias alcanzar tu objetivo financiero en el plazo definido.")
    else:
        st.warning(f"Incluso con la mejor opcion, no alcanzarias el objetivo en {plazo_meses} meses. Considera extender el plazo o aumentar el ahorro.")

    # Grafico inversion vs simple
    st.markdown(
        f'<div class="section-intro" style="margin-top:18px;">El grafico compara guardar el dinero sin '
        f'rendir versus invertirlo mes a mes con la mejor opcion de tu perfil. '
        f'La brecha entre curvas es el efecto del interes compuesto acumulado. '
        f'Moneda: <b>{simbolo}</b>.</div>',
        unsafe_allow_html=True
    )

    import plotly.graph_objects as go
    tasa_m   = (1 + mejor_t) ** (1/12) - 1
    sin_inv  = []
    con_inv  = []
    ac_s     = 0
    ac_i     = 0
    for m in meses:
        ac_s  += eleg
        ac_i   = (ac_i + eleg) * (1 + tasa_m)
        sin_inv.append(ac_s)
        con_inv.append(ac_i)

    df_inv = pd.DataFrame({
        "Mes": meses, "Ahorro sin invertir": sin_inv,
        "Ahorro invertido": con_inv, "Objetivo": [monto_objetivo]*plazo_meses
    })

    fig_inv = go.Figure()
    fig_inv.add_trace(go.Scatter(x=df_inv["Mes"], y=df_inv["Ahorro sin invertir"],
        mode="lines", name="Ahorro sin invertir", line=dict(color="#6C757D", width=3)))
    fig_inv.add_trace(go.Scatter(x=df_inv["Mes"], y=df_inv["Ahorro invertido"],
        mode="lines", name=f"Invertido: {mejor_op}", line=dict(color="#D4A373", width=4)))
    fig_inv.add_trace(go.Scatter(x=df_inv["Mes"], y=df_inv["Objetivo"],
        mode="lines", name="Objetivo", line=dict(color="#2E8B57", width=3, dash="dash")))
    fig_inv.update_layout(
        title="Efecto del interes compuesto: ahorro simple vs inversion",
        paper_bgcolor="#f5f1ea", plot_bgcolor="#ffffff", height=550,
        xaxis_title="Mes", yaxis_title=f"Monto ({simbolo})", hovermode="x unified"
    )
    st.plotly_chart(fig_inv, use_container_width=True)

    st.caption(
        "Las tasas son estimativas y de referencia. "
        "No constituyen asesoramiento financiero profesional. "
        "Consulta con un asesor habilitado antes de tomar decisiones de inversion."
    )
    st.success("Gracias por usar Ruta Ahorro 💰 — Tu camino hacia el objetivo empieza hoy!")
"""

with open('/tmp/app_part7.py', 'w') as f:
    f.write(part7)
print("part7 ok", len(part7))
SCRIPT
Salida

part7 ok 5275
