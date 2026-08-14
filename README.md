# Liseth · Papas y Pollerías

App Streamlit para despachos a pollerías, cobranza, gráficos y reportes Excel/PDF.

**Manual de uso:** [MANUAL.md](MANUAL.md)

## Local

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud

1. Deploy desde este repo (`app.py`).
2. **Settings → Secrets**:

```toml
[credenciales]
usuario = "liseth"
clave = "tu_clave"

SUPABASE_URL = "https://xxxx.supabase.co"
SUPABASE_KEY = "tu-clave"
```

3. En Supabase → SQL Editor, ejecutar `supabase/schema_despachos_papas.sql`.
