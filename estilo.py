import base64
from pathlib import Path

import streamlit as st

from config import APP_BG, LOGIN_BG


def _imagen_base64(ruta: Path) -> str | None:
    if not ruta.is_file():
        return None
    return base64.b64encode(ruta.read_bytes()).decode("ascii")


def aplicar_estilo_login_fondo() -> None:
    b64 = _imagen_base64(LOGIN_BG)
    if not b64:
        return
    st.markdown(
        f"""
<style>
[data-testid="stAppViewContainer"] {{
  background:
    linear-gradient(90deg,
      rgba(18, 20, 16, 0.25) 0%,
      rgba(18, 20, 16, 0.35) 45%,
      rgba(18, 20, 16, 0.55) 100%),
    url("data:image/jpeg;base64,{b64}") left center / cover no-repeat fixed !important;
}}

[data-testid="stHeader"] {{
  background: transparent !important;
}}

div.block-container {{
  max-width: 26rem !important;
  margin-left: auto !important;
  margin-right: 4vw !important;
  padding-top: 2.2rem !important;
  padding-bottom: 2rem !important;
}}

.lisbet-hero {{
  text-align: left !important;
  background: rgba(18, 20, 16, 0.28) !important;
  border: 1px solid rgba(230, 180, 34, 0.22) !important;
  box-shadow: none !important;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}}

.lisbet-hero .brand {{
  color: #FAFAF7 !important;
  text-shadow: 0 2px 14px rgba(0,0,0,0.55);
}}

.lisbet-hero .tag {{
  color: #E6B422 !important;
}}

.lisbet-hero .sub {{
  margin-left: 0 !important;
  color: #E8EAE3 !important;
}}

div[data-testid="stForm"] {{
  background: rgba(18, 20, 16, 0.32) !important;
  border: 1px solid rgba(230, 180, 34, 0.25) !important;
  box-shadow: none !important;
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
}}

.stTextInput input {{
  background-color: rgba(18, 20, 16, 0.45) !important;
  color: #FAFAF7 !important;
}}

[data-testid="stCaption"],
[data-testid="stWidgetLabel"] p,
label, p, .stMarkdown {{
  color: #FAFAF7 !important;
}}

@media (max-width: 780px) {{
  div.block-container {{
    max-width: 100% !important;
    margin-left: 1rem !important;
    margin-right: 1rem !important;
  }}
  .lisbet-hero {{
    text-align: center !important;
  }}
  .lisbet-hero .sub {{
    margin-left: auto !important;
  }}
  [data-testid="stAppViewContainer"] {{
    background:
      linear-gradient(180deg, rgba(18, 20, 16, 0.4) 0%, rgba(18, 20, 16, 0.65) 100%),
      url("data:image/jpeg;base64,{b64}") left center / cover no-repeat fixed !important;
  }}
}}
</style>
        """,
        unsafe_allow_html=True,
    )


def aplicar_estilo_negocio() -> None:
    b64 = _imagen_base64(APP_BG)
    fondo = """
  background:
    radial-gradient(ellipse 85% 50% at 50% -5%, rgba(230, 180, 34, 0.16), transparent 55%),
    radial-gradient(ellipse 55% 40% at 0% 80%, rgba(90, 120, 60, 0.12), transparent 50%),
    #121410;
  background-attachment: fixed;
"""
    hero_extra = ""
    if b64:
        fondo = f"""
  background:
    linear-gradient(115deg,
      rgba(18, 20, 16, 0.94) 0%,
      rgba(18, 20, 16, 0.88) 48%,
      rgba(18, 20, 16, 0.62) 100%),
    url("data:image/jpeg;base64,{b64}") right center / cover no-repeat fixed !important;
"""
        hero_extra = f"""
.lisbet-hero {{
  background:
    linear-gradient(165deg, rgba(30, 36, 28, 0.82), rgba(18, 20, 16, 0.78)),
    url("data:image/jpeg;base64,{b64}") center / cover no-repeat !important;
  backdrop-filter: blur(2px);
  -webkit-backdrop-filter: blur(2px);
}}
"""

    st.markdown(
        f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,600;0,9..40,700;1,9..40,400&family=Literata:opsz,wght@7..72,600;7..72,700&display=swap');

:root {{
  --bg: #121410;
  --card: #1E241C;
  --accent: #E6B422;
  --accent-soft: #F0D078;
  --text: #FAFAF7;
  --muted: #C5C9BE;
}}

html, body, [data-testid="stAppViewContainer"] {{
  font-family: "DM Sans", sans-serif;
}}

[data-testid="stAppViewContainer"] {{
{fondo}
}}

[data-testid="stHeader"] {{
  background: rgba(18, 20, 16, 0.85);
}}

[data-testid="stSidebar"] {{
  background: rgba(30, 36, 28, 0.94) !important;
}}

[data-testid="stSidebar"] > div:first-child {{
  background: transparent;
}}

[data-testid="stSidebar"] * {{
  color: #FAFAF7 !important;
}}

.block-container {{
  padding-top: 1.1rem;
}}

.lisbet-hero {{
  text-align: center;
  padding: 1.75rem 1.1rem 1.35rem;
  margin: 0 0 1rem 0;
  border-radius: 20px;
  background:
    linear-gradient(165deg, rgba(30, 36, 28, 0.98), rgba(18, 20, 16, 0.96)),
    url("data:image/svg+xml,%3Csvg width='72' height='72' viewBox='0 0 72 72' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23E6B422' fill-opacity='0.09'%3E%3Cellipse cx='18' cy='20' rx='11' ry='9'/%3E%3Cellipse cx='50' cy='42' rx='13' ry='10'/%3E%3Cellipse cx='28' cy='55' rx='9' ry='7'/%3E%3C/g%3E%3C/svg%3E");
  border: 1px solid rgba(230, 180, 34, 0.4);
  box-shadow: 0 14px 36px rgba(0, 0, 0, 0.35);
}}
{hero_extra}

.lisbet-hero .brand {{
  font-family: Literata, Georgia, serif;
  font-size: clamp(2.5rem, 9vw, 3.5rem);
  font-weight: 700;
  letter-spacing: 0.02em;
  color: #FAFAF7;
  line-height: 1.05;
  margin: 0;
  text-shadow: 0 2px 20px rgba(230, 180, 34, 0.25);
}}

.lisbet-hero .tag {{
  margin: 0.55rem 0 0 0;
  font-size: 1.05rem;
  color: #E6B422;
  font-weight: 600;
}}

.lisbet-hero .sub {{
  margin: 0.5rem auto 0;
  max-width: 28rem;
  font-size: 0.95rem;
  color: #C5C9BE;
}}

.lisbet-potato {{
  font-size: 3.2rem;
  line-height: 1;
  margin: 0.35rem 0 0.15rem;
  filter: drop-shadow(0 4px 12px rgba(230, 180, 34, 0.35));
}}

div[data-testid="stForm"] {{
  background: rgba(30, 36, 28, 0.92);
  padding: 1.15rem 1rem 0.7rem;
  border-radius: 16px;
  border: 1px solid rgba(230, 180, 34, 0.28);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
}}

div[data-testid="stForm"] button[kind="primary"],
button[kind="primary"] {{
  background: linear-gradient(90deg, #E6B422, #C99512) !important;
  color: #121410 !important;
  border: none !important;
  font-weight: 700 !important;
}}

h1, h2, h3 {{
  font-family: Literata, Georgia, serif !important;
  color: #FAFAF7 !important;
}}

p, label, .stMarkdown, [data-testid="stCaption"],
[data-testid="stWidgetLabel"] p {{
  color: #FAFAF7 !important;
}}

[data-testid="stMetricLabel"] {{
  color: #C5C9BE !important;
}}

[data-testid="stMetricValue"] {{
  color: #E6B422 !important;
}}

.stTextInput input, .stNumberInput input, .stSelectbox [data-baseweb="select"] > div {{
  background-color: rgba(18, 20, 16, 0.85) !important;
  color: #FAFAF7 !important;
  border: 1px solid rgba(230, 180, 34, 0.32) !important;
  border-radius: 12px !important;
}}

.stTextInput input:focus, .stNumberInput input:focus {{
  border-color: #E6B422 !important;
  box-shadow: 0 0 0 1px #E6B422 !important;
}}

[data-testid="stAlert"] {{
  border-radius: 12px;
}}

@media (max-width: 780px) {{
  [data-testid="stAppViewContainer"] {{
    background:
      linear-gradient(180deg, rgba(18, 20, 16, 0.9) 0%, rgba(18, 20, 16, 0.78) 100%),
      url("data:image/jpeg;base64,{b64 or ''}") center top / cover no-repeat fixed !important;
  }}
}}
</style>
        """,
        unsafe_allow_html=True,
    )
