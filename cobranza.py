import pandas as pd
import streamlit as st

from logica import corregir_venta, monto_venta


def mostrar_cobranza() -> None:
    st.header("Panel de cobranza")
    pendientes_idx = [
        i
        for i, v in enumerate(st.session_state.base_ventas)
        if v["estado"] == "Fiado / Debe"
    ]

    if not pendientes_idx:
        st.success("Todo cobrado. Ninguna pollería debe.")
        return

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
