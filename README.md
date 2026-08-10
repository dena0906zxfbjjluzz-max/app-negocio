# Control de Papas y Pollerías

App Streamlit para registrar despachos semanales a pollerías, resúmenes y cuentas por cobrar.

## Local

```bash
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud

1. Deploy from this repo (`app.py`).
2. En **Settings → Secrets** (opcional por ahora):

```toml
SUPABASE_URL = "https://xxxx.supabase.co"
SUPABASE_KEY = "tu-clave"
```

Sin secrets la app funciona en memoria (session).
