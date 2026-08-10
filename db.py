"""Cliente Supabase para despachos (persistencia al cerrar sesión)."""

from __future__ import annotations

from typing import Any


TABLA = "despachos_papas"


def _secrets_url_key() -> tuple[str | None, str | None]:
    import streamlit as st

    url = key = None
    try:
        url = st.secrets.get("SUPABASE_URL") or st.secrets.get("supabase_url")
        key = st.secrets.get("SUPABASE_KEY") or st.secrets.get("supabase_key")
        if (not url or not key) and "credenciales" in st.secrets:
            c = st.secrets["credenciales"]
            url = url or c.get("SUPABASE_URL") or c.get("supabase_url")
            key = key or c.get("SUPABASE_KEY") or c.get("supabase_key")
        if (not url or not key) and "supabase" in st.secrets:
            s = st.secrets["supabase"]
            url = url or s.get("url") or s.get("URL")
            key = key or s.get("key") or s.get("KEY")
    except Exception:
        pass
    if url:
        url = str(url).strip().rstrip("/")
    if key:
        key = str(key).strip()
    return url or None, key or None


def get_client():
    """Retorna cliente Supabase o None si no hay secrets / paquete."""
    url, key = _secrets_url_key()
    if not url or not key:
        return None
    try:
        from supabase import create_client
    except ImportError:
        return None
    return create_client(url, key)


def supabase_configurado() -> bool:
    return get_client() is not None


def _fila_a_venta(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "semana": row.get("semana") or "",
        "dia": row.get("dia") or "",
        "cliente": row.get("cliente") or "",
        "kilos": float(row.get("kilos") if row.get("kilos") is not None else row.get("sacos") or 0),
        "precio": float(row.get("precio") or 0),
        "estado": row.get("estado") or "Pagado en efectivo",
    }


def listar_despachos(semana: str | None = None) -> list[dict[str, Any]]:
    client = get_client()
    if client is None:
        return []
    q = client.table(TABLA).select("*").order("id", desc=False)
    if semana:
        q = q.eq("semana", semana)
    resp = q.execute()
    rows = resp.data or []
    return [_fila_a_venta(r) for r in rows]


def insertar_despacho(venta: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    if client is None:
        raise RuntimeError("Supabase no configurado")
    payload = {
        "semana": venta["semana"],
        "dia": venta["dia"],
        "cliente": venta["cliente"],
        "kilos": float(venta["kilos"]),
        "precio": float(venta["precio"]),
        "estado": venta["estado"],
    }
    resp = client.table(TABLA).insert(payload).execute()
    if not resp.data:
        raise RuntimeError("Insert vacío en Supabase")
    return _fila_a_venta(resp.data[0])


def actualizar_despacho(id_: int, venta: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    if client is None:
        raise RuntimeError("Supabase no configurado")
    payload = {
        "semana": venta["semana"],
        "dia": venta["dia"],
        "cliente": venta["cliente"],
        "kilos": float(venta["kilos"]),
        "precio": float(venta["precio"]),
        "estado": venta["estado"],
    }
    resp = client.table(TABLA).update(payload).eq("id", id_).execute()
    if not resp.data:
        raise RuntimeError(f"No se actualizó id={id_}")
    return _fila_a_venta(resp.data[0])


def borrar_despacho(id_: int) -> None:
    client = get_client()
    if client is None:
        raise RuntimeError("Supabase no configurado")
    client.table(TABLA).delete().eq("id", id_).execute()
