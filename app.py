from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="Liseth · Papas y Pollerías",
    page_icon="🥔",
    layout="centered",
)

from cobranza import mostrar_cobranza
from config import ESLOGAN, NOMBRE_NEGOCIO, SECCIONES
from cuaderno import mostrar_cuaderno
from db import listar_despachos, mensaje_nube
from estilo import aplicar_estilo_login_fondo, aplicar_estilo_negocio
from logica import USAR_NUBE, cargar_credenciales, cargar_datos_iniciales
from resumen import mostrar_resumen

aplicar_estilo_negocio()

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario_sesion" not in st.session_state:
    st.session_state.usuario_sesion = ""

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

    creds = cargar_credenciales()
    if not creds:
        st.error("Falta configurar usuario y clave en Streamlit (Settings → Secrets).")
        st.stop()
    usuario_ok, clave_ok = creds

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
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")

    st.stop()

if "base_ventas" not in st.session_state or not isinstance(
    st.session_state.base_ventas, list
):
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
    if st.sidebar.button("Recargar desde la nube", use_container_width=True):
        try:
            with st.spinner("Cargando..."):
                st.session_state.base_ventas = listar_despachos()
            st.session_state.pop("error_supabase", None)
            st.rerun()
        except Exception as e:
            st.sidebar.error(mensaje_nube(e))

if st.session_state.get("error_supabase"):
    st.sidebar.error(f"Supabase: {st.session_state['error_supabase']}")

seccion = st.sidebar.radio("Ir a", SECCIONES)

st.markdown(
    f"""
<div class="lisbet-hero" style="padding:1rem 1rem 0.85rem;margin-bottom:0.75rem;">
  <p class="brand" style="font-size:clamp(1.8rem,6vw,2.6rem);">{NOMBRE_NEGOCIO}</p>
  <p class="tag">Control de papas y pollerías</p>
</div>
    """,
    unsafe_allow_html=True,
)

try:
    if seccion == "Cuaderno Semanal":
        mostrar_cuaderno()
    elif seccion == "Resumen Semanal":
        mostrar_resumen()
    else:
        mostrar_cobranza()
except Exception as e:
    st.error(mensaje_nube(e))
    st.caption("Si sigue igual, recargue la página o toque Recargar desde la nube.")
