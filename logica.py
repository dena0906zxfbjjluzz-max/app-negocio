from __future__ import annotations

from datetime import date

import streamlit as st

from db import (
    actualizar_despacho,
    borrar_despacho,
    insertar_despacho,
    listar_despachos,
    supabase_configurado,
)

USAR_NUBE = supabase_configurado()


def cargar_credenciales() -> tuple[str, str] | None:
    try:
        creds = st.secrets.get("credenciales")
        if creds is not None:
            usuario = str(creds.get("usuario", "")).strip()
            clave = str(creds.get("clave", "")).strip()
            if usuario and clave:
                return usuario, clave
        usuario = str(st.secrets.get("usuario", "")).strip()
        clave = str(st.secrets.get("clave", "")).strip()
        if usuario and clave:
            return usuario, clave
    except Exception:
        pass
    return None


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
    for v in st.session_state.get("base_ventas", []):
        s = v.get("semana")
        if s and s not in out:
            out.append(s)
    return out


def monto_venta(v: dict) -> float:
    return float(v.get("kilos", 0)) * float(v.get("precio", 0))


def texto_numero(valor) -> str:
    if isinstance(valor, float):
        return str(valor).rstrip("0").rstrip(".")
    return str(valor)


def despacho_ya_ingresado(venta: dict, excluir_idx: int | None = None) -> bool:
    cliente = (venta.get("cliente") or "").strip().casefold()
    kilos = round(float(venta.get("kilos") or 0), 4)
    precio = round(float(venta.get("precio") or 0), 4)
    for i, v in enumerate(st.session_state.get("base_ventas", [])):
        if excluir_idx is not None and i == excluir_idx:
            continue
        if (
            v.get("semana") == venta.get("semana")
            and v.get("dia") == venta.get("dia")
            and (v.get("cliente") or "").strip().casefold() == cliente
            and round(float(v.get("kilos") or 0), 4) == kilos
            and round(float(v.get("precio") or 0), 4) == precio
        ):
            return True
    return False


def cargar_datos_iniciales() -> list[dict]:
    if USAR_NUBE:
        try:
            return listar_despachos()
        except Exception as e:
            st.session_state["error_supabase"] = str(e)
            return []
    return []


def agregar_venta(venta: dict) -> None:
    if USAR_NUBE:
        guardada = insertar_despacho(venta)
        st.session_state.base_ventas.append(guardada)
    else:
        st.session_state.base_ventas.append({**venta, "id": None})


def corregir_venta(idx: int, venta: dict) -> None:
    actual = st.session_state.base_ventas[idx]
    if USAR_NUBE and actual.get("id") is not None:
        st.session_state.base_ventas[idx] = actualizar_despacho(int(actual["id"]), venta)
    else:
        st.session_state.base_ventas[idx] = {**venta, "id": actual.get("id")}


def eliminar_venta(idx: int) -> None:
    actual = st.session_state.base_ventas[idx]
    if USAR_NUBE and actual.get("id") is not None:
        borrar_despacho(int(actual["id"]))
    st.session_state.base_ventas.pop(idx)
