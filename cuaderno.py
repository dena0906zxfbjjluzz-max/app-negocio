import pandas as pd
import streamlit as st

from config import DIAS, ESTADOS_PAGO, LISTA_POLLERIAS, TABS_DIAS
from logica import (
    agregar_venta,
    corregir_venta,
    despacho_ya_ingresado,
    eliminar_venta,
    monto_venta,
    semanas_disponibles,
    texto_numero,
)
from db import mensaje_nube


def mostrar_cuaderno() -> None:
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
                    help="Kilos reales del despacho.",
                )
                precio_txt = st.text_input(
                    "Precio por kilo (S/)",
                    placeholder="Escriba el precio, ej: 2.60",
                )
                estado = st.selectbox(
                    "Estado del pago",
                    ESTADOS_PAGO,
                    index=None,
                    placeholder="Elija cómo pagó",
                )
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
                    elif not estado:
                        st.error("Elija el estado del pago.")
                    elif kilos is not None and precio is not None:
                        if kilos <= 0:
                            st.error("Los kilos deben ser mayores que 0.")
                        elif precio < 0:
                            st.error("El precio no puede ser negativo.")
                        else:
                            nueva = {
                                "semana": semana_act,
                                "dia": nombre_dia,
                                "cliente": cliente,
                                "kilos": float(kilos),
                                "precio": float(precio),
                                "estado": estado,
                            }
                            if despacho_ya_ingresado(nueva):
                                st.warning(
                                    "Ese despacho ya está anotado (misma pollería, kilos y precio). "
                                    "No se volvió a guardar."
                                )
                            else:
                                try:
                                    with st.spinner("Guardando..."):
                                        agregar_venta(nueva)
                                    st.success(
                                        f"Anotado: {cliente} · {kilos:g} kg · S/ {kilos * precio:.2f}"
                                    )
                                    st.rerun()
                                except Exception as e:
                                    st.error(mensaje_nube(e))

            indices_dia = [
                i
                for i, v in enumerate(st.session_state.get("base_ventas") or [])
                if v.get("semana") == semana_act and v.get("dia") == nombre_dia
            ]

            if not indices_dia:
                st.info("Hoja vacía. Aún no hay despachos este día.")
                continue

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
            ventas = st.session_state.get("base_ventas") or []
            if idx_edit < 0 or idx_edit >= len(ventas):
                st.warning("Ese despacho ya no está. Recargue la página.")
                continue
            actual = ventas[idx_edit]

            with st.form(f"form_edit_{nombre_dia}_{idx_edit}"):
                st.caption("Al marcar el despacho arriba, aquí se llenan solos. Corrija y guarde, o bórrelo.")
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
                    value=texto_numero(actual["kilos"]),
                    help="Escriba la cantidad de kilos que quiera.",
                )
                e_precio_txt = st.text_input(
                    "Precio por kilo (S/)",
                    value=texto_numero(actual["precio"]),
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
                    if not e_cliente:
                        st.error("Elija la pollería.")
                    elif not e_estado:
                        st.error("Elija el estado del pago.")
                    else:
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
                                corregida = {
                                    "semana": semana_act,
                                    "dia": nombre_dia,
                                    "cliente": e_cliente,
                                    "kilos": float(e_kilos),
                                    "precio": float(e_precio),
                                    "estado": e_estado,
                                }
                                if despacho_ya_ingresado(corregida, excluir_idx=idx_edit):
                                    st.warning(
                                        "Ya hay otro despacho igual (misma pollería, kilos y precio). "
                                        "No se guardó la corrección."
                                    )
                                else:
                                    try:
                                        with st.spinner("Guardando..."):
                                            corregir_venta(idx_edit, corregida)
                                        st.success("Despacho corregido.")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(mensaje_nube(e))
                if btn_borrar:
                    try:
                        with st.spinner("Borrando..."):
                            eliminar_venta(idx_edit)
                        st.success("Despacho borrado.")
                        st.rerun()
                    except Exception as e:
                        st.error(mensaje_nube(e))
