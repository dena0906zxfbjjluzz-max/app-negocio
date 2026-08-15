"""Cliente Supabase para despachos (persistencia al cerrar sesión)."""

from __future__ import annotations

import time
from typing import Any, Callable, TypeVar

TABLA = "despachos_papas"
_COL_CANTIDAD: str | None = None
T = TypeVar("T")


def mensaje_nube(exc: BaseException) -> str:
    t = str(exc).lower()
    if "pgrst204" in t or "could not find" in t:
        return "No se pudo guardar en la nube. Recargue e intente de nuevo."
    if "invalid api key" in t or "jwt" in t or "unauthorized" in t:
        return "La nube no acepta la clave. Avisar a quien instaló la app."
    if "timeout" in t or "timed out" in t or "deadline" in t:
        return "La nube tardó mucho. Espere un momento y vuelva a intentar."
    if "connection" in t or "network" in t or "connect" in t or "ssl" in t:
        return "Sin conexión con la nube. Revise el internet y vuelva a intentar."
    return "No se pudo completar. Espere un momento y vuelva a intentar."


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
        from supabase.client import ClientOptions

        return create_client(
            url,
            key,
            options=ClientOptions(
                postgrest_client_timeout=20,
                storage_client_timeout=20,
            ),
        )
    except Exception:
        try:
            from supabase import create_client

            return create_client(url, key)
        except Exception:
            return None


def supabase_configurado() -> bool:
    return get_client() is not None


def _es_error_columna(exc: BaseException) -> bool:
    txt = str(exc).lower()
    return "pgrst204" in txt or "could not find" in txt


def _es_transitorio(exc: BaseException) -> bool:
    t = str(exc).lower()
    return any(
        p in t
        for p in (
            "timeout",
            "timed out",
            "connection",
            "network",
            "temporarily",
            "503",
            "502",
            "504",
            "ssl",
            "reset",
            "unavailable",
        )
    )


def _con_reintento(fn: Callable[[], T], intentos: int = 3) -> T:
    ultimo: BaseException | None = None
    for i in range(intentos):
        try:
            return fn()
        except Exception as e:
            ultimo = e
            if _es_error_columna(e) or not _es_transitorio(e):
                raise
            if i < intentos - 1:
                time.sleep(0.7 * (i + 1))
    raise RuntimeError(mensaje_nube(ultimo or RuntimeError("error")))


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


def _columnas() -> tuple[str, ...]:
    if _COL_CANTIDAD:
        return (_COL_CANTIDAD,)
    return ("kilos", "sacos")


def _marcar_columna(col: str) -> None:
    global _COL_CANTIDAD
    _COL_CANTIDAD = col


def listar_despachos(semana: str | None = None) -> list[dict[str, Any]]:
    client = get_client()
    if client is None:
        return []

    def _hacer():
        q = client.table(TABLA).select("*").order("id", desc=False)
        if semana:
            q = q.eq("semana", semana)
        resp = q.execute()
        return [_fila_a_venta(r) for r in (resp.data or [])]

    try:
        return _con_reintento(_hacer)
    except Exception as e:
        raise RuntimeError(mensaje_nube(e)) from e


def insertar_despacho(venta: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    if client is None:
        raise RuntimeError("La nube no está configurada.")
    ultimo: BaseException | None = None
    for col in _columnas():
        try:

            def _hacer(c=col):
                resp = client.table(TABLA).insert(_payload(venta, c)).execute()
                if not resp.data:
                    raise RuntimeError("Insert vacío en Supabase")
                return _fila_a_venta(resp.data[0])

            fila = _con_reintento(_hacer)
            _marcar_columna(col)
            return fila
        except Exception as e:
            ultimo = e
            if _es_error_columna(e):
                continue
            raise RuntimeError(mensaje_nube(e)) from e
    raise RuntimeError(mensaje_nube(ultimo or RuntimeError("No se pudo guardar.")))


def actualizar_despacho(id_: int, venta: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    if client is None:
        raise RuntimeError("La nube no está configurada.")
    ultimo: BaseException | None = None
    for col in _columnas():
        try:

            def _hacer(c=col):
                resp = (
                    client.table(TABLA)
                    .update(_payload(venta, c))
                    .eq("id", id_)
                    .execute()
                )
                if not resp.data:
                    raise RuntimeError(f"No se actualizó id={id_}")
                return _fila_a_venta(resp.data[0])

            fila = _con_reintento(_hacer)
            _marcar_columna(col)
            return fila
        except Exception as e:
            ultimo = e
            if _es_error_columna(e):
                continue
            raise RuntimeError(mensaje_nube(e)) from e
    raise RuntimeError(mensaje_nube(ultimo or RuntimeError("No se pudo actualizar.")))


def borrar_despacho(id_: int) -> None:
    client = get_client()
    if client is None:
        raise RuntimeError("La nube no está configurada.")

    def _hacer():
        client.table(TABLA).delete().eq("id", id_).execute()

    try:
        _con_reintento(_hacer)
    except Exception as e:
        raise RuntimeError(mensaje_nube(e)) from e
