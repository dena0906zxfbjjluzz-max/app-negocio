# Lisbeth · Papas y Pollerías

App Streamlit para despachos a pollerías, gastos, cobranza, gráficos y reportes Excel/PDF.

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
usuario = "lisbeth"
clave = "tu_clave"

SUPABASE_URL = "https://xxxx.supabase.co"
SUPABASE_KEY = "tu-clave"
```

3. En Supabase → SQL Editor, ejecutar en este orden:
   - `supabase/schema_despachos_papas.sql`
   - `supabase/schema_gastos_negocio.sql`
   - (si la tabla vieja tenía `sacos`) `supabase/migrar_sacos_a_kilos.sql`
