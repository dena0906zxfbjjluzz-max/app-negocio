import pandas as pd
import streamlit as st

from config import DIAS, LISTA_POLLERIAS
from logica import monto_venta, semanas_disponibles
from reportes import generar_excel_cuaderno, generar_pdf_resumen


def mostrar_resumen() -> None:
    st.header("Cierre de la semana")
    semana_act = st.selectbox("Ver resumen de", semanas_disponibles())
    ventas_sem = [v for v in st.session_state.base_ventas if v["semana"] == semana_act]

    if not ventas_sem:
        st.info("Aún no hay despachos en esta semana.")
        return

    total_fact = sum(monto_venta(v) for v in ventas_sem)

    st.subheader("Totales")
    m1, m2 = st.columns(2)
    m1.metric(
        "Kilos",
        f"{sum(float(v.get('kilos', 0)) for v in ventas_sem):.1f}",
    )
    m2.metric("Facturación", f"S/ {total_fact:.2f}")

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

    st.divider()
    st.subheader("Comparativa entre semanas")
    filas_comp = []
    semanas_vistas = sorted(
        {v["semana"] for v in st.session_state.base_ventas},
        key=lambda s: int("".join(ch for ch in s if ch.isdigit()) or "0"),
    )
    for s in semanas_vistas:
        v_s = [v for v in st.session_state.base_ventas if v["semana"] == s]
        filas_comp.append(
            {
                "semana": s,
                "Facturación": sum(monto_venta(v) for v in v_s),
            }
        )
    if filas_comp:
        df_comp = pd.DataFrame(filas_comp).set_index("semana")
        st.line_chart(df_comp[["Facturación"]], use_container_width=True)

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
        return

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
