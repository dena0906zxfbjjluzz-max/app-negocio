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
    page_title="Control Papas - Pollerías",
    page_icon="🥔",
    layout="centered",
)

# Demo local si aún no hay secrets (cámbialo en Streamlit Cloud)
USUARIO_DEMO = "admin"
CLAVE_DEMO = "papas2026"


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
    "Pollería El Corralito",
    "Pollería Norky's",
    "Pollería Rokys",
    "Pollería Las Canastas",
    "Pollería Pardos",
    "Pollería Granja Azul",
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
            "cliente": "Pollería El Corralito",
            "kilos": 50.0,
            "precio": 2.60,
            "estado": "Pagado en efectivo",
        },
        {
            "id": None,
            "semana": s,
            "dia": "Lunes",
            "cliente": "Pollería Norky's",
            "kilos": 80.0,
            "precio": 2.50,
            "estado": "Fiado / Debe",
        },
        {
            "id": None,
            "semana": s,
            "dia": "Martes",
            "cliente": "Pollería Rokys",
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
    st.title("Control de Papas y Pollerías")
    st.caption("Acceso restringido · introduzca su usuario y contraseña")
    st.divider()

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

st.sidebar.title("Menú")
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

st.title("Control de Papas y Pollerías")
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
                kilos = st.number_input("Kilos", min_value=0.5, value=50.0, step=0.5)
                precio = st.number_input(
                    "Precio por kilo (S/)", min_value=0.0, value=2.60, step=0.1
                )
                estado = st.selectbox("Estado del pago", ESTADOS_PAGO)
                st.write(f"Monto estimado: **S/ {kilos * precio:.2f}**")
                guardar = st.form_submit_button("Guardar despacho")
                if guardar:
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
                        st.success(f"Anotado: {cliente} · {nombre_dia}")
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
                    e_kilos = st.number_input(
                        "Kilos",
                        min_value=0.5,
                        value=float(actual["kilos"]),
                        step=0.5,
                    )
                    e_precio = st.number_input(
                        "Precio por kilo (S/)",
                        min_value=0.0,
                        value=float(actual["precio"]),
                        step=0.1,
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
                    st.write(f"Monto corregido: **S/ {e_kilos * e_precio:.2f}**")
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
