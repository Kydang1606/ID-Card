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
# LOAD IMAGE → BASE64
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
# UI INPUT
# =========================
st.title("ID Card - TRIAC")

name = st.text_input("Name")
id_ = st.text_input("ID")
team = st.selectbox("Team", ["Worker", "Office"])
level = st.text_input("Level")
photo = st.file_uploader("Upload Photo", type=["jpg", "png"])

logo_base64 = file_to_base64("logo.png")

# =========================
# GENERATE CARD (HTML)
# =========================
if st.button("Generate") and photo:

    img = Image.open(photo)
    photo_base64 = img_to_base64(img)

    if team == "Worker":
        # CARD NGANG
        html = f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

        .card {{
            width: 900px;
            height: 520px;
            border-radius: 16px;
            overflow: hidden;
            font-family: 'Roboto', sans-serif;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}

        .header {{
            background: #c80000;
            height: 90px;
            display: flex;
            align-items: center;
            padding: 0 20px;
        }}

        .logo {{
            height: 60px;
        }}

        .company {{
            color: white;
            font-size: 26px;
            font-weight: 700;
            margin-left: 20px;
        }}

        .body {{
            display: flex;
            height: 340px;
        }}

        .photo {{
            width: 35%;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .photo img {{
            width: 90%;
            height: 90%;
            object-fit: cover;
            border-radius: 12px;
        }}

        .info {{
            width: 65%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 20px;
        }}

        .name {{
            font-size: 34px;
            font-weight: 700;
            margin-bottom: 10px;
        }}

        .id {{
            font-size: 26px;
            font-weight: 500;
            margin-bottom: 20px;
        }}

        .small {{
            font-size: 18px;
            color: #333;
            margin-bottom: 5px;
        }}

        .footer {{
            background: #c80000;
            height: 90px;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-size: 14px;
            padding: 10px;
        }}
        </style>

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

    else:
        # CARD DỌC
        html = f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

        .card {{
            width: 520px;
            height: 900px;
            border-radius: 16px;
            overflow: hidden;
            font-family: 'Roboto', sans-serif;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}

        .header {{
            background: #006699;
            height: 100px;
            display: flex;
            align-items: center;
            padding: 0 20px;
        }}

        .logo {{
            height: 70px;
        }}

        .company {{
            color: white;
            font-size: 24px;
            font-weight: 700;
            margin-left: 20px;
        }}

        .photo {{
            height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .photo img {{
            width: 70%;
            height: 90%;
            object-fit: cover;
            border-radius: 12px;
        }}

        .info {{
            padding: 20px;
            text-align: center;
        }}

        .name {{
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 10px;
        }}

        .id {{
            font-size: 24px;
            font-weight: 500;
            margin-bottom: 20px;
        }}

        .small {{
            font-size: 18px;
            margin-bottom: 5px;
        }}

        .footer {{
            background: #006699;
            height: 100px;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-size: 14px;
            padding: 10px;
        }}
        </style>

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

    st.markdown(html, unsafe_allow_html=True)
