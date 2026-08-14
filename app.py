from __future__ import annotations

import base64
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

from reportes import generar_excel_cuaderno, generar_pdf_resumen
from db import (
    supabase_configurado,
    listar_despachos,
    insertar_despacho,
    actualizar_despacho,
    borrar_despacho,
    listar_gastos,
    insertar_gasto,
    actualizar_gasto,
    borrar_gasto,
)

st.set_page_config(
    page_title="Liseth · Papas y Pollerías",
    page_icon="🥔",
    layout="centered",
)

NOMBRE_NEGOCIO = "Liseth"
ESLOGAN = "Control de papas y pollerías · del cuaderno a la nube"
LOGIN_BG = Path(__file__).resolve().parent / "assets" / "login_papas.jpg"
APP_BG = Path(__file__).resolve().parent / "assets" / "app_papas_fritas.jpg"

# Demo local si aún no hay secrets (cámbialo en Streamlit Cloud)
USUARIO_DEMO = "admin"
CLAVE_DEMO = "papas2026"


def _imagen_base64(ruta: Path) -> str | None:
    if not ruta.is_file():
        return None
    return base64.b64encode(ruta.read_bytes()).decode("ascii")


def aplicar_estilo_login_fondo() -> None:
    """Foto de papas de fondo; panel de login a la derecha, mezclado con el fondo."""
    b64 = _imagen_base64(LOGIN_BG)
    if not b64:
        return
    st.markdown(
        f"""
<style>
[data-testid="stAppViewContainer"] {{
  background:
    linear-gradient(90deg,
      rgba(18, 20, 16, 0.25) 0%,
      rgba(18, 20, 16, 0.35) 45%,
      rgba(18, 20, 16, 0.55) 100%),
    url("data:image/jpeg;base64,{b64}") left center / cover no-repeat fixed !important;
}}

[data-testid="stHeader"] {{
  background: transparent !important;
}}

/* Empuja Lisbet + formulario hacia la derecha (hueco de la foto) */
div.block-container {{
  max-width: 26rem !important;
  margin-left: auto !important;
  margin-right: 4vw !important;
  padding-top: 2.2rem !important;
  padding-bottom: 2rem !important;
}}

.lisbet-hero {{
  text-align: left !important;
  background: rgba(18, 20, 16, 0.28) !important;
  border: 1px solid rgba(230, 180, 34, 0.22) !important;
  box-shadow: none !important;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}}

.lisbet-hero .brand {{
  color: #FAFAF7 !important;
  text-shadow: 0 2px 14px rgba(0,0,0,0.55);
}}

.lisbet-hero .tag {{
  color: #E6B422 !important;
}}

.lisbet-hero .sub {{
  margin-left: 0 !important;
  color: #E8EAE3 !important;
}}

div[data-testid="stForm"] {{
  background: rgba(18, 20, 16, 0.32) !important;
  border: 1px solid rgba(230, 180, 34, 0.25) !important;
  box-shadow: none !important;
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
}}

.stTextInput input {{
  background-color: rgba(18, 20, 16, 0.45) !important;
  color: #FAFAF7 !important;
}}

[data-testid="stCaption"],
[data-testid="stWidgetLabel"] p,
label, p, .stMarkdown {{
  color: #FAFAF7 !important;
}}

@media (max-width: 780px) {{
  div.block-container {{
    max-width: 100% !important;
    margin-left: 1rem !important;
    margin-right: 1rem !important;
  }}
  .lisbet-hero {{
    text-align: center !important;
  }}
  .lisbet-hero .sub {{
    margin-left: auto !important;
  }}
  [data-testid="stAppViewContainer"] {{
    background:
      linear-gradient(180deg, rgba(18, 20, 16, 0.4) 0%, rgba(18, 20, 16, 0.65) 100%),
      url("data:image/jpeg;base64,{b64}") left center / cover no-repeat fixed !important;
  }}
}}
</style>
        """,
        unsafe_allow_html=True,
    )


def aplicar_estilo_negocio() -> None:
    """Paleta Papa Mercado + foto de papas fritas suave de fondo."""
    b64 = _imagen_base64(APP_BG)
    fondo = """
  background:
    radial-gradient(ellipse 85% 50% at 50% -5%, rgba(230, 180, 34, 0.16), transparent 55%),
    radial-gradient(ellipse 55% 40% at 0% 80%, rgba(90, 120, 60, 0.12), transparent 50%),
    #121410;
  background-attachment: fixed;
"""
    hero_extra = ""
    if b64:
        fondo = f"""
  background:
    linear-gradient(115deg,
      rgba(18, 20, 16, 0.94) 0%,
      rgba(18, 20, 16, 0.88) 48%,
      rgba(18, 20, 16, 0.62) 100%),
    url("data:image/jpeg;base64,{b64}") right center / cover no-repeat fixed !important;
"""
        hero_extra = f"""
.lisbet-hero {{
  background:
    linear-gradient(165deg, rgba(30, 36, 28, 0.82), rgba(18, 20, 16, 0.78)),
    url("data:image/jpeg;base64,{b64}") center / cover no-repeat !important;
  backdrop-filter: blur(2px);
  -webkit-backdrop-filter: blur(2px);
}}
"""

    st.markdown(
        f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,600;0,9..40,700;1,9..40,400&family=Literata:opsz,wght@7..72,600;7..72,700&display=swap');

:root {{
  --bg: #121410;
  --card: #1E241C;
  --accent: #E6B422;
  --accent-soft: #F0D078;
  --text: #FAFAF7;
  --muted: #C5C9BE;
}}

html, body, [data-testid="stAppViewContainer"] {{
  font-family: "DM Sans", sans-serif;
}}

[data-testid="stAppViewContainer"] {{
{fondo}
}}

[data-testid="stHeader"] {{
  background: rgba(18, 20, 16, 0.85);
}}

[data-testid="stSidebar"] {{
  background: rgba(30, 36, 28, 0.94) !important;
}}

[data-testid="stSidebar"] > div:first-child {{
  background: transparent;
}}

[data-testid="stSidebar"] * {{
  color: #FAFAF7 !important;
}}

.block-container {{
  padding-top: 1.1rem;
}}

.lisbet-hero {{
  text-align: center;
  padding: 1.75rem 1.1rem 1.35rem;
  margin: 0 0 1rem 0;
  border-radius: 20px;
  background:
    linear-gradient(165deg, rgba(30, 36, 28, 0.98), rgba(18, 20, 16, 0.96)),
    url("data:image/svg+xml,%3Csvg width='72' height='72' viewBox='0 0 72 72' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23E6B422' fill-opacity='0.09'%3E%3Cellipse cx='18' cy='20' rx='11' ry='9'/%3E%3Cellipse cx='50' cy='42' rx='13' ry='10'/%3E%3Cellipse cx='28' cy='55' rx='9' ry='7'/%3E%3C/g%3E%3C/svg%3E");
  border: 1px solid rgba(230, 180, 34, 0.4);
  box-shadow: 0 14px 36px rgba(0, 0, 0, 0.35);
}}
{hero_extra}

.lisbet-hero .brand {{
  font-family: Literata, Georgia, serif;
  font-size: clamp(2.5rem, 9vw, 3.5rem);
  font-weight: 700;
  letter-spacing: 0.02em;
  color: #FAFAF7;
  line-height: 1.05;
  margin: 0;
  text-shadow: 0 2px 20px rgba(230, 180, 34, 0.25);
}}

.lisbet-hero .tag {{
  margin: 0.55rem 0 0 0;
  font-size: 1.05rem;
  color: #E6B422;
  font-weight: 600;
}}

.lisbet-hero .sub {{
  margin: 0.5rem auto 0;
  max-width: 28rem;
  font-size: 0.95rem;
  color: #C5C9BE;
}}

.lisbet-chip {{
  display: inline-block;
  margin-top: 0.9rem;
  padding: 0.32rem 0.85rem;
  border-radius: 999px;
  font-size: 0.75rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #121410;
  background: #E6B422;
  font-weight: 700;
}}

.lisbet-potato {{
  font-size: 3.2rem;
  line-height: 1;
  margin: 0.35rem 0 0.15rem;
  filter: drop-shadow(0 4px 12px rgba(230, 180, 34, 0.35));
}}

div[data-testid="stForm"] {{
  background: rgba(30, 36, 28, 0.92);
  padding: 1.15rem 1rem 0.7rem;
  border-radius: 16px;
  border: 1px solid rgba(230, 180, 34, 0.28);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
}}

div[data-testid="stForm"] button[kind="primary"],
button[kind="primary"] {{
  background: linear-gradient(90deg, #E6B422, #C99512) !important;
  color: #121410 !important;
  border: none !important;
  font-weight: 700 !important;
}}

h1, h2, h3 {{
  font-family: Literata, Georgia, serif !important;
  color: #FAFAF7 !important;
}}

p, label, .stMarkdown, [data-testid="stCaption"],
[data-testid="stWidgetLabel"] p {{
  color: #FAFAF7 !important;
}}

[data-testid="stMetricLabel"] {{
  color: #C5C9BE !important;
}}

[data-testid="stMetricValue"] {{
  color: #E6B422 !important;
}}

.stTextInput input, .stNumberInput input, .stSelectbox [data-baseweb="select"] > div {{
  background-color: rgba(18, 20, 16, 0.85) !important;
  color: #FAFAF7 !important;
  border: 1px solid rgba(230, 180, 34, 0.32) !important;
  border-radius: 12px !important;
}}

.stTextInput input:focus, .stNumberInput input:focus {{
  border-color: #E6B422 !important;
  box-shadow: 0 0 0 1px #E6B422 !important;
}}

[data-testid="stAlert"] {{
  border-radius: 12px;
}}

@media (max-width: 780px) {{
  [data-testid="stAppViewContainer"] {{
    background:
      linear-gradient(180deg, rgba(18, 20, 16, 0.9) 0%, rgba(18, 20, 16, 0.78) 100%),
      url("data:image/jpeg;base64,{b64 or ''}") center top / cover no-repeat fixed !important;
  }}
}}
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
    "Pollería Totus",
]

ESTADOS_PAGO = ["Pagado en efectivo", "Transferencia", "Fiado / Debe"]
CATEGORIAS_GASTO = [
    "Compra de papas",
    "Transporte",
    "Personal / jornal",
    "Combustible",
    "Peaje",
    "Empaque",
    "Otro",
]
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
    for g in st.session_state.get("base_gastos", []):
        s = g.get("semana")
        if s and s not in out:
            out.append(s)
    return out


def monto_venta(v: dict) -> float:
    return float(v.get("kilos", 0)) * float(v.get("precio", 0))


def datos_demo() -> list[dict]:
    return []


def datos_demo_gastos() -> list[dict]:
    return []


def cargar_datos_iniciales() -> list[dict]:
    if USAR_NUBE:
        try:
            return listar_despachos()
        except Exception as e:
            st.session_state["error_supabase"] = str(e)
            return []
    return datos_demo()


def cargar_gastos_iniciales() -> list[dict]:
    if USAR_NUBE:
        try:
            return listar_gastos()
        except Exception as e:
            st.session_state["error_gastos"] = str(e)
            return []
    return datos_demo_gastos()


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


def agregar_gasto(gasto: dict) -> None:
    if USAR_NUBE:
        guardado = insertar_gasto(gasto)
        st.session_state.base_gastos.append(guardado)
    else:
        st.session_state.base_gastos.append({**gasto, "id": None})


def corregir_gasto(idx: int, gasto: dict) -> None:
    actual = st.session_state.base_gastos[idx]
    if USAR_NUBE and actual.get("id") is not None:
        guardado = actualizar_gasto(int(actual["id"]), gasto)
        st.session_state.base_gastos[idx] = guardado
    else:
        st.session_state.base_gastos[idx] = {**gasto, "id": actual.get("id")}


def eliminar_gasto(idx: int) -> None:
    actual = st.session_state.base_gastos[idx]
    if USAR_NUBE and actual.get("id") is not None:
        borrar_gasto(int(actual["id"]))
    st.session_state.base_gastos.pop(idx)


if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario_sesion" not in st.session_state:
    st.session_state.usuario_sesion = ""

# ---------- LOGIN ----------
if not st.session_state.autenticado:
    aplicar_estilo_login_fondo()
    st.markdown(
        f"""
<div class="lisbet-hero">
  <p class="lisbet-potato">🥔</p>
  <p class="brand">{NOMBRE_NEGOCIO}</p>
  <p class="tag">Papas · pollerías · cobranzas</p>
  <p class="sub">{ESLOGAN}</p>
</div>
        """,
        unsafe_allow_html=True,
    )

    usuario_ok, clave_ok, _es_demo = cargar_credenciales()

    with st.form("login_form"):
        usuario_in = st.text_input("Usuario")
        clave_in = st.text_input("Contraseña", type="password")
        entrar = st.form_submit_button("Ingresar", type="primary", use_container_width=True)

    if entrar:
        if usuario_in.strip() == usuario_ok and clave_in == clave_ok:
            st.session_state.autenticado = True
            st.session_state.usuario_sesion = usuario_in.strip()
            if "base_ventas" in st.session_state:
                del st.session_state["base_ventas"]
            if "base_gastos" in st.session_state:
                del st.session_state["base_gastos"]
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")

    st.stop()

# ---------- APP (requiere login) ----------
if "base_ventas" not in st.session_state:
    st.session_state.base_ventas = cargar_datos_iniciales()
if "base_gastos" not in st.session_state:
    st.session_state.base_gastos = cargar_gastos_iniciales()

st.sidebar.title(f"🥔 {NOMBRE_NEGOCIO}")
st.sidebar.caption(f"Sesión: **{st.session_state.usuario_sesion or 'usuario'}**")
if st.sidebar.button("Cerrar sesión", use_container_width=True):
    st.session_state.autenticado = False
    st.session_state.usuario_sesion = ""
    if "base_ventas" in st.session_state:
        del st.session_state["base_ventas"]
    if "base_gastos" in st.session_state:
        del st.session_state["base_gastos"]
    st.rerun()

if USAR_NUBE:
    if st.sidebar.button("Recargar desde la nube", use_container_width=True):
        try:
            st.session_state.base_ventas = listar_despachos()
            try:
                st.session_state.base_gastos = listar_gastos()
                st.session_state.pop("error_gastos", None)
            except Exception as eg:
                st.session_state["error_gastos"] = str(eg)
                st.session_state.base_gastos = []
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

if st.session_state.get("error_supabase"):
    st.sidebar.error(f"Supabase: {st.session_state['error_supabase']}")
if st.session_state.get("error_gastos"):
    st.sidebar.warning("Falta crear la tabla de gastos en Supabase.")

seccion = st.sidebar.radio(
    "Ir a",
    ["Cuaderno Semanal", "Gastos", "Resumen Semanal", "Cuentas por Cobrar"],
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
                cliente = st.selectbox(
                    "Pollería",
                    LISTA_POLLERIAS,
                    index=None,
                    placeholder="Elija la pollería",
                )
                kilos_txt = st.text_input(
                    "Kilos (kg)",
                    placeholder="Escriba la cantidad que quiera, ej: 12 · 37.5 · 200",
                    help="Libre: los kilos reales del despacho (sin conversión a saco).",
                )
                precio_txt = st.text_input(
                    "Precio por kilo (S/)",
                    placeholder="Escriba el precio, ej: 2.60",
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
                    if not cliente:
                        st.error("Elija la pollería.")
                    elif kilos is not None and precio is not None:
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
# 1b) GASTOS
# =====================================================================
elif seccion == "Gastos":
    st.header("Gastos del negocio")
    st.caption("Compra de papas, transporte, personal u otros → utilidad neta en el resumen.")
    if USAR_NUBE and st.session_state.get("error_gastos"):
        st.error("No se pudo leer gastos. Ejecute el SQL de gastos en Supabase y recargue.")

    semana_act = st.selectbox(
        "Semana de gastos",
        semanas_disponibles(),
        key="semana_gastos",
    )

    with st.form("form_gasto", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            g_dia = st.selectbox("Día", DIAS)
            g_cat = st.selectbox("Categoría", CATEGORIAS_GASTO)
        with c2:
            g_monto_txt = st.text_input("Monto (S/)", placeholder="Ej: 150.00")
            g_concepto = st.text_input("Concepto / nota", placeholder="Opcional")
        guardar_g = st.form_submit_button("Guardar gasto", type="primary")
        if guardar_g:
            try:
                g_monto = float((g_monto_txt or "").replace(",", ".").strip())
            except ValueError:
                st.error("Escriba un monto válido (ej. 80 o 150.50).")
                g_monto = None
            if g_monto is not None:
                if g_monto <= 0:
                    st.error("El monto debe ser mayor que 0.")
                else:
                    try:
                        agregar_gasto(
                            {
                                "semana": semana_act,
                                "dia": g_dia,
                                "categoria": g_cat,
                                "concepto": (g_concepto or "").strip(),
                                "monto": float(g_monto),
                            }
                        )
                        st.success(f"Gasto anotado: {g_cat} · S/ {g_monto:.2f}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"No se pudo guardar: {e}")

    indices_g = [
        i
        for i, g in enumerate(st.session_state.base_gastos)
        if g["semana"] == semana_act
    ]
    if not indices_g:
        st.info("Sin gastos en esta semana.")
    else:
        filas_g = [
            {
                "día": st.session_state.base_gastos[i]["dia"],
                "categoría": st.session_state.base_gastos[i]["categoria"],
                "concepto": st.session_state.base_gastos[i]["concepto"],
                "monto": st.session_state.base_gastos[i]["monto"],
            }
            for i in indices_g
        ]
        df_g = pd.DataFrame(filas_g)
        st.dataframe(df_g, use_container_width=True, hide_index=True)
        st.metric("Total gastos semana", f"S/ {df_g['monto'].sum():.2f}")

        st.divider()
        st.subheader("Corregir o borrar gasto")
        etiquetas_g = {
            f"#{n + 1} · {st.session_state.base_gastos[i]['dia']} · "
            f"{st.session_state.base_gastos[i]['categoria']} · "
            f"S/ {st.session_state.base_gastos[i]['monto']:.2f}": i
            for n, i in enumerate(indices_g)
        }
        elegir_g = st.selectbox("Gasto", list(etiquetas_g.keys()), key="sel_gasto_edit")
        idx_g = etiquetas_g[elegir_g]
        actual_g = st.session_state.base_gastos[idx_g]

        with st.form("form_edit_gasto"):
            eg_dia = st.selectbox(
                "Día",
                DIAS,
                index=DIAS.index(actual_g["dia"]) if actual_g["dia"] in DIAS else 0,
            )
            eg_cat = st.selectbox(
                "Categoría",
                CATEGORIAS_GASTO,
                index=(
                    CATEGORIAS_GASTO.index(actual_g["categoria"])
                    if actual_g["categoria"] in CATEGORIAS_GASTO
                    else 0
                ),
            )
            eg_monto_txt = st.text_input("Monto (S/)", value=str(actual_g["monto"]))
            eg_concepto = st.text_input("Concepto", value=actual_g.get("concepto") or "")
            col_sg, col_bg = st.columns(2)
            with col_sg:
                btn_sg = st.form_submit_button(
                    "Guardar corrección", type="primary", use_container_width=True
                )
            with col_bg:
                btn_bg = st.form_submit_button("Borrar gasto", use_container_width=True)

            if btn_sg:
                try:
                    eg_monto = float((eg_monto_txt or "").replace(",", ".").strip())
                except ValueError:
                    st.error("Monto inválido.")
                    eg_monto = None
                if eg_monto is not None and eg_monto > 0:
                    try:
                        corregir_gasto(
                            idx_g,
                            {
                                "semana": semana_act,
                                "dia": eg_dia,
                                "categoria": eg_cat,
                                "concepto": (eg_concepto or "").strip(),
                                "monto": float(eg_monto),
                            },
                        )
                        st.success("Gasto corregido.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"No se pudo corregir: {e}")
            if btn_bg:
                try:
                    eliminar_gasto(idx_g)
                    st.success("Gasto borrado.")
                    st.rerun()
                except Exception as e:
                    st.error(f"No se pudo borrar: {e}")

# =====================================================================
# 2) RESUMEN SEMANAL
# =====================================================================
elif seccion == "Resumen Semanal":
    st.header("Cierre de la semana")
    semana_act = st.selectbox("Ver resumen de", semanas_disponibles())
    ventas_sem = [v for v in st.session_state.base_ventas if v["semana"] == semana_act]
    gastos_sem = [g for g in st.session_state.base_gastos if g["semana"] == semana_act]

    if not ventas_sem and not gastos_sem:
        st.info("Aún no hay datos en esta semana.")
    else:
        total_fact = sum(monto_venta(v) for v in ventas_sem)
        total_gast = sum(float(g.get("monto", 0)) for g in gastos_sem)
        utilidad = total_fact - total_gast

        st.subheader("Totales")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(
            "Kilos",
            f"{sum(float(v.get('kilos', 0)) for v in ventas_sem):.1f}",
        )
        m2.metric("Facturación", f"S/ {total_fact:.2f}")
        m3.metric("Gastos", f"S/ {total_gast:.2f}")
        m4.metric("Utilidad neta", f"S/ {utilidad:.2f}")

        if ventas_sem:
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
            st.subheader("Gráficos")
            por_cliente = (
                df_sem.groupby("cliente", as_index=True)[["monto", "kilos"]]
                .sum()
                .sort_values("monto", ascending=False)
            )
            st.caption("Facturación por pollería (S/)")
            st.bar_chart(por_cliente["monto"], use_container_width=True)

            orden_dias = {d: i for i, d in enumerate(DIAS)}
            dias_orden = sorted(set(df_sem["dia"]), key=lambda d: orden_dias.get(d, 99))
            por_dia = df_sem.groupby("dia")["monto"].sum().reindex(dias_orden)
            st.caption("Ventas por día (S/)")
            st.bar_chart(por_dia, use_container_width=True)

            st.dataframe(
                df_sem[["dia", "cliente", "kilos", "precio", "monto", "estado"]],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("Sin despachos esta semana (solo gastos).")

        if gastos_sem:
            df_gs = pd.DataFrame(gastos_sem)
            st.subheader("Gastos de la semana")
            por_cat = (
                df_gs.groupby("categoria", as_index=True)["monto"]
                .sum()
                .sort_values(ascending=False)
            )
            st.caption("Gastos por categoría (S/)")
            st.bar_chart(por_cat, use_container_width=True)
            st.dataframe(
                df_gs[["dia", "categoria", "concepto", "monto"]],
                use_container_width=True,
                hide_index=True,
            )

        # Comparativa entre semanas con datos
        st.divider()
        st.subheader("Comparativa entre semanas")
        filas_comp = []
        semanas_vistas = sorted(
            {
                *(v["semana"] for v in st.session_state.base_ventas),
                *(g["semana"] for g in st.session_state.base_gastos),
            },
            key=lambda s: int("".join(ch for ch in s if ch.isdigit()) or "0"),
        )
        for s in semanas_vistas:
            v_s = [v for v in st.session_state.base_ventas if v["semana"] == s]
            g_s = [g for g in st.session_state.base_gastos if g["semana"] == s]
            fact = sum(monto_venta(v) for v in v_s)
            gast = sum(float(g.get("monto", 0)) for g in g_s)
            filas_comp.append(
                {
                    "semana": s,
                    "Facturación": fact,
                    "Gastos": gast,
                    "Utilidad": fact - gast,
                }
            )
        if len(filas_comp) >= 1:
            df_comp = pd.DataFrame(filas_comp).set_index("semana")
            st.line_chart(df_comp[["Facturación", "Gastos", "Utilidad"]], use_container_width=True)

        if ventas_sem:
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
