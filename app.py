import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Control Papas - Pollerías",
    page_icon="🥔",
    layout="centered",
)

# --- Supabase: se activará cuando pongas secretos (fase 2) ---
SUPABASE_LISTO = False
try:
    url = st.secrets.get("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY")
    if not url and "credenciales" in st.secrets:
        url = st.secrets["credenciales"].get("SUPABASE_URL")
        key = st.secrets["credenciales"].get("SUPABASE_KEY")
    if url and key:
        # from supabase import create_client
        # supabase = create_client(url, key)
        SUPABASE_LISTO = True
except Exception:
    pass

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
    """Etiqueta de semana ISO del año (ej. Semana 33)."""
    f = fecha or date.today()
    return f"Semana {f.isocalendar().week}"


def semanas_disponibles() -> list[str]:
    actual = semana_label()
    # Semana actual, anterior y siguiente (ISO simple por número)
    n = date.today().isocalendar().week
    candidatas = []
    for w in (n - 1, n, n + 1):
        if 1 <= w <= 53:
            candidatas.append(f"Semana {w}")
    # Asegurar orden y sin duplicados
    out = list(dict.fromkeys(candidatas))
    if actual not in out:
        out.insert(0, actual)
    return out


def monto_venta(v: dict) -> float:
    return float(v.get("sacos", 0)) * float(v.get("precio", 0))


if "base_ventas" not in st.session_state:
    s = semana_label()
    st.session_state.base_ventas = [
        {
            "semana": s,
            "dia": "Lunes",
            "cliente": "Pollería El Corralito",
            "sacos": 12,
            "precio": 45.0,
            "estado": "Pagado en efectivo",
        },
        {
            "semana": s,
            "dia": "Lunes",
            "cliente": "Pollería Norky's",
            "sacos": 20,
            "precio": 43.5,
            "estado": "Fiado / Debe",
        },
        {
            "semana": s,
            "dia": "Martes",
            "cliente": "Pollería Rokys",
            "sacos": 15,
            "precio": 44.0,
            "estado": "Transferencia",
        },
    ]

st.title("Control de Papas y Pollerías")
st.caption("Del cuaderno a la nube · datos en memoria por ahora")
if SUPABASE_LISTO:
    st.sidebar.success("Supabase: secrets listos")
else:
    st.sidebar.info("Supabase: sin conectar (ok por ahora)")

seccion = st.sidebar.radio(
    "Menú",
    ["Cuaderno Semanal", "Resumen Semanal", "Cuentas por Cobrar"],
)

# =====================================================================
# 1) CUADERNO SEMANAL
# =====================================================================
if seccion == "Cuaderno Semanal":
    st.header("Registro semanal")
    semana_act = st.selectbox("Semana de trabajo", semanas_disponibles(), index=min(1, len(semanas_disponibles()) - 1))
    st.divider()

    hojas = st.tabs(TABS_DIAS)
    for idx, hoja in enumerate(hojas):
        nombre_dia = DIAS[idx]
        with hoja:
            st.subheader(f"Hoja del {nombre_dia}")

            with st.form(f"form_{nombre_dia}", clear_on_submit=True):
                cliente = st.selectbox("Pollería", LISTA_POLLERIAS)
                sacos = st.number_input("Sacos", min_value=1, value=5, step=1)
                precio = st.number_input("Precio por saco (S/)", min_value=0.0, value=45.0, step=0.5)
                estado = st.selectbox("Estado del pago", ESTADOS_PAGO)
                st.write(f"Monto estimado: **S/ {sacos * precio:.2f}**")
                guardar = st.form_submit_button("Guardar despacho")
                if guardar:
                    st.session_state.base_ventas.append(
                        {
                            "semana": semana_act,
                            "dia": nombre_dia,
                            "cliente": cliente,
                            "sacos": int(sacos),
                            "precio": float(precio),
                            "estado": estado,
                        }
                    )
                    st.success(f"Anotado: {cliente} · {nombre_dia}")

            filtrados = [
                v
                for v in st.session_state.base_ventas
                if v["semana"] == semana_act and v["dia"] == nombre_dia
            ]

            if filtrados:
                df_dia = pd.DataFrame(filtrados)
                df_dia["monto"] = df_dia["sacos"] * df_dia["precio"]
                st.dataframe(
                    df_dia[["cliente", "sacos", "precio", "monto", "estado"]],
                    use_container_width=True,
                    hide_index=True,
                )
                c1, c2 = st.columns(2)
                c1.metric("Sacos hoy", f"{int(df_dia['sacos'].sum())}")
                c2.metric("Total hoy", f"S/ {df_dia['monto'].sum():.2f}")
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
        df_sem["monto"] = df_sem["sacos"] * df_sem["precio"]

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
        m1.metric("Sacos de la semana", f"{int(df_sem['sacos'].sum())}")
        m2.metric("Facturación", f"S/ {df_sem['monto'].sum():.2f}")

        st.dataframe(
            df_sem[["dia", "cliente", "sacos", "precio", "monto", "estado"]],
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Descargar reporte")
        csv = (
            df_sem[["dia", "cliente", "sacos", "precio", "monto", "estado"]]
            .to_csv(index=False)
            .encode("utf-8-sig")
        )
        nombre_archivo = f"reporte_{semana_act.replace(' ', '_')}.csv"
        st.download_button(
            "Descargar CSV (abre en Excel)",
            data=csv,
            file_name=nombre_archivo,
            mime="text/csv",
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
                    "sacos": v["sacos"],
                    "monto": m,
                }
            )

        st.warning(f"{len(pendientes_idx)} entrega(s) pendiente(s) · total S/ {total_debe:.2f}")
        st.dataframe(pd.DataFrame(filas), use_container_width=True, hide_index=True)

        st.subheader("Marcar como cobrado")
        opciones = {
            f"[{i}] {st.session_state.base_ventas[i]['cliente']} · "
            f"{st.session_state.base_ventas[i]['dia']} · S/ {monto_venta(st.session_state.base_ventas[i]):.2f}": i
            for i in pendientes_idx
        }
        elegir = st.selectbox("Entrega", list(opciones.keys()))
        modo = st.radio("Cobrado cómo", ["Pagado en efectivo", "Transferencia"], horizontal=True)
        if st.button("Registrar cobro"):
            idx = opciones[elegir]
            st.session_state.base_ventas[idx]["estado"] = modo
            st.success("Cobro registrado.")
            st.rerun()
