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
    raw = row.get("kilos")
    if raw is None:
        raw = row.get("sacos")
    return {
        "id": row.get("id"),
        "semana": row.get("semana") or "",
        "dia": row.get("dia") or "",
        "cliente": row.get("cliente") or "",
        "kilos": float(raw or 0),
        "precio": float(row.get("precio") or 0),
        "estado": row.get("estado") or "Pagado en efectivo",
    }


def _es_error_columna(exc: BaseException) -> bool:
    txt = str(exc).lower()
    return "pgrst204" in txt or "could not find" in txt


def _payload(venta: dict[str, Any], col_cantidad: str) -> dict[str, Any]:
    qty = float(venta["kilos"])
    cantidad: int | float = int(round(qty)) if col_cantidad == "sacos" else qty
    return {
        "semana": venta["semana"],
        "dia": venta["dia"],
        "cliente": venta["cliente"],
        col_cantidad: cantidad,
        "precio": float(venta["precio"]),
        "estado": venta["estado"],
    }


def listar_despachos(semana: str | None = None) -> list[dict[str, Any]]:
    client = get_client()
    if client is None:
        return []
    q = client.table(TABLA).select("*").order("id", desc=False)
    if semana:
        q = q.eq("semana", semana)
    resp = q.execute()
    return [_fila_a_venta(r) for r in (resp.data or [])]


def insertar_despacho(venta: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    if client is None:
        raise RuntimeError("Supabase no configurado")
    ultimo: BaseException | None = None
    for col in ("kilos", "sacos"):
        try:
            resp = client.table(TABLA).insert(_payload(venta, col)).execute()
            if resp.data:
                return _fila_a_venta(resp.data[0])
        except Exception as e:
            ultimo = e
            if not _es_error_columna(e):
                raise
    raise RuntimeError(ultimo or "Insert vacío en Supabase")


def actualizar_despacho(id_: int, venta: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    if client is None:
        raise RuntimeError("Supabase no configurado")
    ultimo: BaseException | None = None
    for col in ("kilos", "sacos"):
        try:
            resp = (
                client.table(TABLA)
                .update(_payload(venta, col))
                .eq("id", id_)
                .execute()
            )
            if resp.data:
                return _fila_a_venta(resp.data[0])
        except Exception as e:
            ultimo = e
            if not _es_error_columna(e):
                raise
    raise RuntimeError(ultimo or f"No se actualizó id={id_}")


def borrar_despacho(id_: int) -> None:
    client = get_client()
    if client is None:
        raise RuntimeError("Supabase no configurado")
    client.table(TABLA).delete().eq("id", id_).execute()
