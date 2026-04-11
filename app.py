import streamlit as st
import base64
from PIL import Image
import io

st.set_page_config(layout="centered")

# =========================
# CONFIG
# =========================
COMPANY = "TRIAC COMPOSITES CO., LTD"
ADDRESS = """UniDepot, Factory No 4, Nguyen Van Tao St,
Hiep Phuoc Commune,
HCMC, 700000, Vietnam"""

# =========================
# IMAGE → BASE64
# =========================
def img_to_base64(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

def file_to_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

# =========================
# UI
# =========================
st.title("TRIAC ID CARD")

name = st.text_input("Name")
id_ = st.text_input("ID")
team = st.selectbox("Team", ["Worker", "Office"])
level = st.text_input("Level")
photo = st.file_uploader("Upload Photo", type=["jpg", "png"])

logo_base64 = file_to_base64("logo.png")

# =========================
# GENERATE
# =========================
if st.button("Generate") and photo:

    img = Image.open(photo)
    photo_base64 = img_to_base64(img)

    # =========================
    # MATERIAL STYLE COLORS
    # =========================
    if team == "Worker":
        primary = "#D32F2F"   # đỏ material
        layout = "horizontal"
    else:
        primary = "#1976D2"   # xanh material
        layout = "vertical"

    # =========================
    # HTML + CSS
    # =========================
    html = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

    .card {{
        font-family: 'Roboto', sans-serif;
        background: white;
        border-radius: 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        overflow: hidden;
        margin-top: 20px;
    }}

    .header {{
        background: {primary};
        color: white;
        display: flex;
        align-items: center;
        padding: 16px;
    }}

    .logo {{
        height: 50px;
    }}

    .company {{
        font-size: 22px;
        font-weight: 600;
        margin-left: 16px;
    }}

    .footer {{
        background: {primary};
        color: white;
        text-align: center;
        padding: 12px;
        font-size: 13px;
        line-height: 1.4;
    }}

    .name {{
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 6px;
    }}

    .id {{
        font-size: 20px;
        font-weight: 500;
        margin-bottom: 12px;
        color: #555;
    }}

    .small {{
        font-size: 16px;
        color: #444;
    }}

    .photo img {{
        object-fit: cover;
        border-radius: 12px;
    }}
    """

    # =========================
    # WORKER (NGANG)
    # =========================
    if layout == "horizontal":
        html += f"""
        .card {{ width: 850px; }}

        .body {{
            display: flex;
            padding: 20px;
        }}

        .photo {{
            width: 35%;
        }}

        .photo img {{
            width: 100%;
            height: 260px;
        }}

        .info {{
            width: 65%;
            padding-left: 20px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        """

        html += f"""
        <div class="card">
            <div class="header">
                <img class="logo" src="data:image/png;base64,{logo_base64}">
                <div class="company">{COMPANY}</div>
            </div>

            <div class="body">
                <div class="photo">
                    <img src="data:image/png;base64,{photo_base64}">
                </div>

                <div class="info">
                    <div class="name">{name}</div>
                    <div class="id">ID: {id_}</div>
                    <div class="small">Level: {level}</div>
                    <div class="small">Team: {team}</div>
                </div>
            </div>

            <div class="footer">{ADDRESS}</div>
        </div>
        """

    # =========================
    # OFFICE (DỌC)
    # =========================
    else:
        html += f"""
        .card {{ width: 500px; }}

        .photo {{
            text-align: center;
            padding: 20px;
        }}

        .photo img {{
            width: 70%;
            height: 260px;
        }}

        .info {{
            text-align: center;
            padding: 10px 20px 20px;
        }}
        """

        html += f"""
        <div class="card">
            <div class="header">
                <img class="logo" src="data:image/png;base64,{logo_base64}">
                <div class="company">{COMPANY}</div>
            </div>

            <div class="photo">
                <img src="data:image/png;base64,{photo_base64}">
            </div>

            <div class="info">
                <div class="name">{name}</div>
                <div class="id">ID: {id_}</div>
                <div class="small">Level: {level}</div>
                <div class="small">Team: {team}</div>
            </div>

            <div class="footer">{ADDRESS}</div>
        </div>
        """

    html += "</style>"

    st.markdown(html, unsafe_allow_html=True)
