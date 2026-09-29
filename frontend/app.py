import streamlit as st

st.set_page_config(page_title="Marine Oil Spill Intelligence", page_icon="🌊", layout="wide")

if "vessels" not in st.session_state:
    st.session_state.vessels = None
if "spill" not in st.session_state:
    st.session_state.spill = None
if "analysis" not in st.session_state:
    st.session_state.analysis = None

BACKGROUND_URL = "https://upload.wikimedia.org/wikipedia/commons/a/af/Exxon_Valdez_Oil_Spill_%2813266806523%29.jpg"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(3, 24, 39, 0.58), rgba(3, 24, 39, 0.68)),
                          url('{BACKGROUND_URL}');
        background-size: cover;
        background-position: center 42%;
        background-attachment: fixed;
    }}

    .block-container {{
        padding-top: 5rem;
        padding-bottom: 3rem;
    }}

    .hero {{
        max-width: 1050px;
        margin: 5vh auto 2rem auto;
        padding: 3.5rem 3rem;
        border-radius: 24px;
        background: rgba(0, 0, 0, 0.42);
        border: 1px solid rgba(255,255,255,0.22);
        backdrop-filter: blur(5px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.35);
        text-align: center;
    }}

    .hero h1 {{
        color: white;
        font-size: clamp(2.2rem, 5vw, 4rem);
        margin-bottom: 0.8rem;
        line-height: 1.1;
    }}

    .hero p {{
        color: #e7f7ff;
        font-size: 1.25rem;
        margin: 0;
    }}

    .info-card {{
        max-width: 1050px;
        margin: 0 auto 1.5rem auto;
        padding: 1.25rem 1.5rem;
        border-radius: 16px;
        background: rgba(255,255,255,0.92);
        color: #102a43;
        box-shadow: 0 10px 30px rgba(0,0,0,0.18);
    }}

    .workflow {{
        max-width: 1050px;
        margin: 0 auto;
        padding: 1.4rem 1.6rem;
        border-radius: 16px;
        background: rgba(4, 25, 40, 0.82);
        border: 1px solid rgba(255,255,255,0.18);
        color: white;
        text-align: center;
        font-size: 1.05rem;
    }}

    .credit {{
        max-width: 1050px;
        margin: 1rem auto 0 auto;
        color: rgba(255,255,255,0.72);
        font-size: 0.75rem;
        text-align: right;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>🌊 Marine Oil Spill Intelligence Platform</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    """,
    unsafe_allow_html=True,
)
