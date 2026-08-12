import streamlit as st
import pandas as pd
from datetime import date

from reportes import generar_excel_cuaderno, generar_pdf_resumen
from db import (
    supabase_configurado,
    listar_despachos,
    insertar_despacho,
    actualizar_despacho,
    borrar_despacho,
)

st.set_page_config(
    page_title="Lisbet · Papas y Pollerías",
    page_icon="🥔",
    layout="centered",
)

NOMBRE_NEGOCIO = "Lisbet"
ESLOGAN = "Control de papas y pollerías · del cuaderno a la nube"

# Demo local si aún no hay secrets (cámbialo en Streamlit Cloud)
USUARIO_DEMO = "admin"
CLAVE_DEMO = "papas2026"


def aplicar_estilo_negocio() -> None:
    """Paleta Premium Logística + marca Lisbet — no cambia la lógica del negocio."""
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap');

:root {
  --bg: #0B0F19;
  --card: #161B26;
  --accent: #00F5D4;
  --text: #FFFFFF;
}

html, body, [data-testid="stAppViewContainer"] {
  font-family: "Outfit", sans-serif;
}

[data-testid="stAppViewContainer"] {
  background:
    radial-gradient(ellipse 80% 45% at 50% 0%, rgba(0, 245, 212, 0.12), transparent 55%),
    radial-gradient(ellipse 50% 40% at 100% 100%, rgba(0, 245, 212, 0.06), transparent 45%),
    #0B0F19;
  background-attachment: fixed;
}

[data-testid="stHeader"] {
  background: rgba(11, 15, 25, 0.85);
}

[data-testid="stSidebar"] {
  background: #161B26 !important;
}

[data-testid="stSidebar"] > div:first-child {
  background: #161B26;
}

[data-testid="stSidebar"] * {
  color: #FFFFFF !important;
}

.block-container {
  padding-top: 1.1rem;
}

.lisbet-hero {
  text-align: center;
  padding: 1.75rem 1.1rem 1.35rem;
  margin: 0 0 1rem 0;
  border-radius: 20px;
  background:
    linear-gradient(160deg, rgba(22, 27, 38, 0.95), rgba(11, 15, 25, 0.98)),
    url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%2300F5D4' fill-opacity='0.07'%3E%3Cellipse cx='20' cy='22' rx='10' ry='8'/%3E%3Cellipse cx='55' cy='48' rx='12' ry='9'/%3E%3Cellipse cx='30' cy='60' rx='8' ry='6'/%3E%3C/g%3E%3C/svg%3E");
  border: 1px solid rgba(0, 245, 212, 0.35);
  box-shadow:
    0 0 28px rgba(0, 245, 212, 0.12),
    0 16px 40px rgba(0, 0, 0, 0.45);
}

.lisbet-hero .brand {
  font-family: Outfit, sans-serif;
  font-size: clamp(2.5rem, 9vw, 3.5rem);
  font-weight: 700;
  letter-spacing: 0.04em;
  color: #FFFFFF;
  line-height: 1.05;
  margin: 0;
  text-shadow: 0 0 24px rgba(0, 245, 212, 0.35);
}

.lisbet-hero .tag {
  margin: 0.55rem 0 0 0;
  font-size: 1.05rem;
  color: #00F5D4;
  font-weight: 600;
}

.lisbet-hero .sub {
  margin: 0.5rem auto 0;
  max-width: 28rem;
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.82);
}

.lisbet-chip {
  display: inline-block;
  margin-top: 0.9rem;
  padding: 0.32rem 0.85rem;
  border-radius: 999px;
  font-size: 0.75rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #0B0F19;
  background: #00F5D4;
  font-weight: 700;
  box-shadow: 0 0 18px rgba(0, 245, 212, 0.45);
}

.lisbet-potato {
  font-size: 3.2rem;
  line-height: 1;
  margin: 0.35rem 0 0.15rem;
  filter: drop-shadow(0 0 14px rgba(0, 245, 212, 0.55));
}

div[data-testid="stForm"] {
  background: #161B26;
  padding: 1.15rem 1rem 0.7rem;
  border-radius: 16px;
  border: 1px solid rgba(0, 245, 212, 0.28);
  box-shadow: 0 0 20px rgba(0, 245, 212, 0.08);
}

/* Botón primario turquesa */
div[data-testid="stForm"] button[kind="primary"],
button[kind="primary"] {
  background: linear-gradient(90deg, #00F5D4, #00c9b0) !important;
  color: #0B0F19 !important;
  border: none !important;
  font-weight: 700 !important;
  box-shadow: 0 0 18px rgba(0, 245, 212, 0.4);
}

h1, h2, h3 {
  font-family: Outfit, sans-serif !important;
  color: #FFFFFF !important;
}

p, label, .stMarkdown, [data-testid="stCaption"],
[data-testid="stWidgetLabel"] p {
  color: #FFFFFF !important;
}

[data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
  color: #FFFFFF !important;
}

[data-testid="stMetricValue"] {
  color: #00F5D4 !important;
}

/* Inputs */
.stTextInput input, .stNumberInput input, .stSelectbox [data-baseweb="select"] > div {
  background-color: #0B0F19 !important;
  color: #FFFFFF !important;
  border: 1px solid rgba(0, 245, 212, 0.35) !important;
  border-radius: 12px !important;
}

.stTextInput input:focus, .stNumberInput input:focus {
  border-color: #00F5D4 !important;
  box-shadow: 0 0 0 1px #00F5D4 !important;
}

[data-testid="stAlert"] {
  border-radius: 12px;
}
</style>
        """,
        unsafe_allow_html=True,
    )


aplicar_estilo_negocio()


def cargar_credenciales() -> tuple[str, str, bool]:
    """Lee usuario/clave desde st.secrets['credenciales']."""
    try:
        creds = st.secrets.get("credenciales")
        if creds is not None:
            usuario = str(creds.get("usuario", "")).strip()
            clave = str(creds.get("clave", "")).strip()
            if usuario and clave:
                return usuario, clave, False
        usuario = str(st.secrets.get("usuario", "")).strip()
        clave = str(st.secrets.get("clave", "")).strip()
        if usuario and clave:
            return usuario, clave, False
    except Exception:
        pass
    return USUARIO_DEMO, CLAVE_DEMO, True


USAR_NUBE = supabase_configurado()

LISTA_POLLERIAS = [
    "Pollería Damnus",
    "Pollería Reynoso",
    "Pollería Taco tico",
    "Pollería Broster. Tac.",
    "Pollería Broster. Fos.",
    "Pollería Broster. Ent.",
    "Pollería Dorados",
    "Pollería Perez",
    "Pollería Patrón",
    "Pollería Surys",
    "Pollería Elimar",
    "Pollería Huaylacho",
    "Pollería Pollón. Pas.",
    "Pollería Pollón. Ind.",
    "Pollería Milano",
    "Pollería Qui wui",
    "Pollería León",
    "Pollería D'criss",
    "Pollería Vegas",
    "Pollería Estrella",
    "Pollería Lua",
    "Pollería Paisa",
    "Pollería Tacuchi",
    "Pollería Alitas",
    "Pollería Covida",
    "Pollería Jairo",
    "Pollería Orión",
    "Pollería Lopez",
    "Pollería Gisela",
    "Pollería Verónica",
    "Pollería Chike burger",
]

ESTADOS_PAGO = ["Pagado en efectivo", "Transferencia", "Fiado / Debe"]
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
TABS_DIAS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]


def semana_label(fecha: date | None = None) -> str:
    f = fecha or date.today()
    return f"Semana {f.isocalendar().week}"


def semanas_disponibles() -> list[str]:
    actual = semana_label()
    n = date.today().isocalendar().week
    candidatas = []
    for w in (n - 1, n, n + 1):
        if 1 <= w <= 53:
            candidatas.append(f"Semana {w}")
    out = list(dict.fromkeys(candidatas))
    if actual not in out:
        out.insert(0, actual)
    # semanas que ya existen en datos
    for v in st.session_state.get("base_ventas", []):
        s = v.get("semana")
        if s and s not in out:
            out.append(s)
    return out


def monto_venta(v: dict) -> float:
    return float(v.get("kilos", 0)) * float(v.get("precio", 0))


def datos_demo() -> list[dict]:
    s = semana_label()
    return [
        {
            "id": None,
            "semana": s,
            "dia": "Lunes",
            "cliente": "Pollería Damnus",
            "kilos": 50.0,
            "precio": 2.60,
            "estado": "Pagado en efectivo",
        },
        {
            "id": None,
            "semana": s,
            "dia": "Lunes",
            "cliente": "Pollería Reynoso",
            "kilos": 80.0,
            "precio": 2.50,
            "estado": "Fiado / Debe",
        },
        {
            "id": None,
            "semana": s,
            "dia": "Martes",
            "cliente": "Pollería Taco tico",
            "kilos": 60.0,
            "precio": 2.55,
            "estado": "Transferencia",
        },
    ]


def cargar_datos_iniciales() -> list[dict]:
    if USAR_NUBE:
        try:
            return listar_despachos()
        except Exception as e:
            st.session_state["error_supabase"] = str(e)
            return []
    return datos_demo()


def agregar_venta(venta: dict) -> None:
    if USAR_NUBE:
        guardada = insertar_despacho(venta)
        st.session_state.base_ventas.append(guardada)
    else:
        venta = {**venta, "id": None}
        st.session_state.base_ventas.append(venta)


def corregir_venta(idx: int, venta: dict) -> None:
    actual = st.session_state.base_ventas[idx]
    if USAR_NUBE and actual.get("id") is not None:
        guardada = actualizar_despacho(int(actual["id"]), venta)
        st.session_state.base_ventas[idx] = guardada
    else:
        st.session_state.base_ventas[idx] = {**venta, "id": actual.get("id")}


def eliminar_venta(idx: int) -> None:
    actual = st.session_state.base_ventas[idx]
    if USAR_NUBE and actual.get("id") is not None:
        borrar_despacho(int(actual["id"]))
    st.session_state.base_ventas.pop(idx)


if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario_sesion" not in st.session_state:
    st.session_state.usuario_sesion = ""

# ---------- LOGIN ----------
if not st.session_state.autenticado:
    st.markdown(
        f"""
<div class="lisbet-hero">
  <p class="lisbet-potato">🥔</p>
  <p class="brand">{NOMBRE_NEGOCIO}</p>
  <p class="tag">Papas · pollerías · cobranzas</p>
  <p class="sub">{ESLOGAN}</p>
  <span class="lisbet-chip">Negocio de {NOMBRE_NEGOCIO}</span>
</div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("SIGN IN · acceso restringido")

    usuario_ok, clave_ok, es_demo = cargar_credenciales()
    if es_demo:
        st.info(
            "Credenciales demo (sin secrets): "
            f"**{USUARIO_DEMO}** / **{CLAVE_DEMO}**. "
            "En Streamlit Cloud ponga las suyas en Settings → Secrets."
        )

    with st.form("login_form"):
        usuario_in = st.text_input("Usuario")
        clave_in = st.text_input("Contraseña", type="password")
        entrar = st.form_submit_button("Ingresar", type="primary", use_container_width=True)

    if entrar:
        if usuario_in.strip() == usuario_ok and clave_in == clave_ok:
            st.session_state.autenticado = True
            st.session_state.usuario_sesion = usuario_in.strip()
            # Recargar datos de nube al entrar
            if "base_ventas" in st.session_state:
                del st.session_state["base_ventas"]
            st.success("Acceso concedido.")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")

    st.stop()

# ---------- APP (requiere login) ----------
if "base_ventas" not in st.session_state:
    st.session_state.base_ventas = cargar_datos_iniciales()

st.sidebar.title(f"🥔 {NOMBRE_NEGOCIO}")
st.sidebar.caption(f"Sesión: **{st.session_state.usuario_sesion or 'usuario'}**")
if st.sidebar.button("Cerrar sesión", use_container_width=True):
    st.session_state.autenticado = False
    st.session_state.usuario_sesion = ""
    if "base_ventas" in st.session_state:
        del st.session_state["base_ventas"]
    st.rerun()

if USAR_NUBE:
    st.sidebar.success("Datos en la nube (Supabase)")
    if st.sidebar.button("Recargar desde la nube", use_container_width=True):
        try:
            st.session_state.base_ventas = listar_despachos()
            st.sidebar.success("Datos actualizados.")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Error: {e}")
else:
    st.sidebar.warning("Sin nube: se pierden al cerrar")

if st.session_state.get("error_supabase"):
    st.sidebar.error(f"Supabase: {st.session_state['error_supabase']}")

seccion = st.sidebar.radio(
    "Ir a",
    ["Cuaderno Semanal", "Resumen Semanal", "Cuentas por Cobrar"],
)

st.markdown(
    f"""
<div class="lisbet-hero" style="padding:1rem 1rem 0.85rem;margin-bottom:0.75rem;">
  <p class="brand" style="font-size:clamp(1.8rem,6vw,2.6rem);">{NOMBRE_NEGOCIO}</p>
  <p class="tag">Control de papas y pollerías</p>
</div>
    """,
    unsafe_allow_html=True,
)
if USAR_NUBE:
    st.caption("Los despachos se guardan en Supabase (no se pierden al cerrar sesión).")
else:
    st.caption(
        "Modo local (memoria). Para no perder datos: cree la tabla en Supabase "
        "y ponga SUPABASE_URL / SUPABASE_KEY en secrets."
    )

# =====================================================================
# 1) CUADERNO SEMANAL
# =====================================================================
if seccion == "Cuaderno Semanal":
    st.header("Registro semanal")
    semana_act = st.selectbox(
        "Semana de trabajo",
        semanas_disponibles(),
        index=min(1, len(semanas_disponibles()) - 1),
    )
    st.divider()

    hojas = st.tabs(TABS_DIAS)
    for idx, hoja in enumerate(hojas):
        nombre_dia = DIAS[idx]
        with hoja:
            st.subheader(f"Hoja del {nombre_dia}")

            with st.form(f"form_{nombre_dia}", clear_on_submit=True):
                cliente = st.selectbox("Pollería", LISTA_POLLERIAS)
                kilos_txt = st.text_input(
                    "Kilos (kg)",
                    placeholder="Escriba la cantidad que quiera, ej: 12 · 37.5 · 200",
                    help="Libre: los kilos reales del despacho (sin conversión a saco).",
                )
                precio_txt = st.text_input(
                    "Precio por kilo (S/)",
                    value="2.60",
                    placeholder="Ej: 2.60",
                )
                estado = st.selectbox("Estado del pago", ESTADOS_PAGO)
                guardar = st.form_submit_button("Guardar despacho")
                if guardar:
                    try:
                        kilos = float((kilos_txt or "").replace(",", ".").strip())
                        precio = float((precio_txt or "").replace(",", ".").strip())
                    except ValueError:
                        st.error("Escriba números válidos en kilos y precio (ej. 25.5 y 2.60).")
                        kilos = precio = None
                    if kilos is not None and precio is not None:
                        if kilos <= 0:
                            st.error("Los kilos deben ser mayores que 0.")
                        elif precio < 0:
                            st.error("El precio no puede ser negativo.")
                        else:
                            try:
                                agregar_venta(
                                    {
                                        "semana": semana_act,
                                        "dia": nombre_dia,
                                        "cliente": cliente,
                                        "kilos": float(kilos),
                                        "precio": float(precio),
                                        "estado": estado,
                                    }
                                )
                                st.success(
                                    f"Anotado: {cliente} · {kilos:g} kg · S/ {kilos * precio:.2f}"
                                )
                                st.rerun()
                            except Exception as e:
                                st.error(f"No se pudo guardar: {e}")

            indices_dia = [
                i
                for i, v in enumerate(st.session_state.base_ventas)
                if v["semana"] == semana_act and v["dia"] == nombre_dia
            ]

            if indices_dia:
                filas_vista = []
                for i in indices_dia:
                    v = st.session_state.base_ventas[i]
                    filas_vista.append(
                        {
                            "cliente": v["cliente"],
                            "kilos": v["kilos"],
                            "precio": v["precio"],
                            "monto": monto_venta(v),
                            "estado": v["estado"],
                        }
                    )
                df_dia = pd.DataFrame(filas_vista)
                st.dataframe(df_dia, use_container_width=True, hide_index=True)
                c1, c2 = st.columns(2)
                c1.metric("Kilos hoy", f"{df_dia['kilos'].sum():.1f}")
                c2.metric("Total hoy", f"S/ {df_dia['monto'].sum():.2f}")

                st.divider()
                st.subheader("Corregir o borrar (si anotó mal)")
                etiquetas = {
                    f"#{n + 1} · {st.session_state.base_ventas[i]['cliente']} · "
                    f"{st.session_state.base_ventas[i]['kilos']} kg · "
                    f"S/ {monto_venta(st.session_state.base_ventas[i]):.2f} · "
                    f"{st.session_state.base_ventas[i]['estado']}": i
                    for n, i in enumerate(indices_dia)
                }
                elegir_lbl = st.selectbox(
                    "Despacho a corregir",
                    list(etiquetas.keys()),
                    key=f"sel_edit_{nombre_dia}_{semana_act}",
                )
                idx_edit = etiquetas[elegir_lbl]
                actual = st.session_state.base_ventas[idx_edit]

                with st.form(f"form_edit_{nombre_dia}_{idx_edit}"):
                    st.caption("Cambie lo que esté mal y guarde, o bórrelo si no debió ir.")
                    e_cliente = st.selectbox(
                        "Pollería",
                        LISTA_POLLERIAS,
                        index=(
                            LISTA_POLLERIAS.index(actual["cliente"])
                            if actual["cliente"] in LISTA_POLLERIAS
                            else 0
                        ),
                    )
                    e_kilos_txt = st.text_input(
                        "Kilos (kg)",
                        value=str(actual["kilos"]).rstrip("0").rstrip(".")
                        if isinstance(actual["kilos"], float)
                        else str(actual["kilos"]),
                        help="Escriba la cantidad de kilos que quiera.",
                    )
                    e_precio_txt = st.text_input(
                        "Precio por kilo (S/)",
                        value=str(actual["precio"]),
                    )
                    e_estado = st.selectbox(
                        "Estado del pago",
                        ESTADOS_PAGO,
                        index=(
                            ESTADOS_PAGO.index(actual["estado"])
                            if actual["estado"] in ESTADOS_PAGO
                            else 0
                        ),
                    )
                    col_g, col_b = st.columns(2)
                    with col_g:
                        btn_guardar = st.form_submit_button(
                            "Guardar corrección",
                            type="primary",
                            use_container_width=True,
                        )
                    with col_b:
                        btn_borrar = st.form_submit_button(
                            "Borrar despacho",
                            use_container_width=True,
                        )

                    if btn_guardar:
                        try:
                            e_kilos = float((e_kilos_txt or "").replace(",", ".").strip())
                            e_precio = float((e_precio_txt or "").replace(",", ".").strip())
                        except ValueError:
                            st.error("Kilos y precio deben ser números válidos.")
                            e_kilos = e_precio = None
                        if e_kilos is not None and e_precio is not None:
                            if e_kilos <= 0:
                                st.error("Los kilos deben ser mayores que 0.")
                            else:
                                try:
                                    corregir_venta(
                                        idx_edit,
                                        {
                                            "semana": semana_act,
                                            "dia": nombre_dia,
                                            "cliente": e_cliente,
                                            "kilos": float(e_kilos),
                                            "precio": float(e_precio),
                                            "estado": e_estado,
                                        },
                                    )
                                    st.success("Despacho corregido.")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"No se pudo corregir: {e}")
                    if btn_borrar:
                        try:
                            eliminar_venta(idx_edit)
                            st.success("Despacho borrado.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"No se pudo borrar: {e}")
            else:
                st.info("Hoja vacía. Aún no hay despachos este día.")

# =====================================================================
# 2) RESUMEN SEMANAL
# =====================================================================
elif seccion == "Resumen Semanal":
    st.header("Cierre de la semana")
    semana_act = st.selectbox("Ver resumen de", semanas_disponibles())
    ventas_sem = [v for v in st.session_state.base_ventas if v["semana"] == semana_act]

    if not ventas_sem:
        st.info("Aún no hay datos en esta semana.")
    else:
        df_sem = pd.DataFrame(ventas_sem)
        df_sem["monto"] = df_sem["kilos"] * df_sem["precio"]

        st.subheader("Clientes sin pedido esta semana")
        con_pedido = set(df_sem["cliente"].unique())
        faltantes = [c for c in LISTA_POLLERIAS if c not in con_pedido]
        if faltantes:
            st.warning(f"Falta despachar a {len(faltantes)} pollería(s):")
            for c in faltantes:
                st.write(f"- {c}")
        else:
            st.success("Ya hay despacho a todas las pollerías de la lista.")

        st.divider()
        st.subheader("Totales")
        m1, m2 = st.columns(2)
        m1.metric("Kilos de la semana", f"{df_sem['kilos'].sum():.1f}")
        m2.metric("Facturación", f"S/ {df_sem['monto'].sum():.2f}")

        st.dataframe(
            df_sem[["dia", "cliente", "kilos", "precio", "monto", "estado"]],
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Descargar reportes")
        st.caption("Excel estilo cuaderno (varias hojas) y PDF de resumen ejecutivo.")
        slug = semana_act.replace(" ", "_")

        try:
            excel_buf = generar_excel_cuaderno(
                ventas_sem,
                semana_act,
                lista_clientes=LISTA_POLLERIAS,
            )
            pdf_buf = generar_pdf_resumen(
                ventas_sem,
                semana_act,
                lista_clientes=LISTA_POLLERIAS,
            )
        except Exception as e:
            st.error(f"No se pudo generar el reporte: {e}")
            excel_buf = pdf_buf = None

        if excel_buf and pdf_buf:
            c1, c2 = st.columns(2)
            with c1:
                st.download_button(
                    "Descargar Excel del cuaderno",
                    data=excel_buf.getvalue(),
                    file_name=f"Cuaderno_{slug}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )
            with c2:
                st.download_button(
                    "Descargar PDF resumen",
                    data=pdf_buf.getvalue(),
                    file_name=f"Resumen_{slug}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

# =====================================================================
# 3) CUENTAS POR COBRAR
# =====================================================================
elif seccion == "Cuentas por Cobrar":
    st.header("Panel de cobranza")
    pendientes_idx = [
        i
        for i, v in enumerate(st.session_state.base_ventas)
        if v["estado"] == "Fiado / Debe"
    ]

    if not pendientes_idx:
        st.success("Todo cobrado. Ninguna pollería debe.")
    else:
        filas = []
        total_debe = 0.0
        for i in pendientes_idx:
            v = st.session_state.base_ventas[i]
            m = monto_venta(v)
            total_debe += m
            filas.append(
                {
                    "semana": v["semana"],
                    "dia": v["dia"],
                    "cliente": v["cliente"],
                    "kilos": v["kilos"],
                    "monto": m,
                }
            )

        st.warning(
            f"{len(pendientes_idx)} entrega(s) pendiente(s) · total S/ {total_debe:.2f}"
        )
        st.dataframe(pd.DataFrame(filas), use_container_width=True, hide_index=True)

        st.subheader("Marcar como cobrado")
        opciones = {
            f"[{i}] {st.session_state.base_ventas[i]['cliente']} · "
            f"{st.session_state.base_ventas[i]['dia']} · "
            f"S/ {monto_venta(st.session_state.base_ventas[i]):.2f}": i
            for i in pendientes_idx
        }
        elegir = st.selectbox("Entrega", list(opciones.keys()))
        modo = st.radio(
            "Cobrado cómo", ["Pagado en efectivo", "Transferencia"], horizontal=True
        )
        if st.button("Registrar cobro"):
            idx = opciones[elegir]
            v = dict(st.session_state.base_ventas[idx])
            v["estado"] = modo
            try:
                corregir_venta(idx, v)
                st.success("Cobro registrado.")
                st.rerun()
            except Exception as e:
                st.error(f"No se pudo registrar cobro: {e}")
