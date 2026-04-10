import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# ===== CONFIG =====
st.set_page_config(page_title="Triac Employee Card", layout="centered")

COMPANY_NAME = "Triac Composites Co., LTD"
COMPANY_ADDRESS = "Factory 4, Depot Saigon, No9, Nguyen Van Tao, Hiep Phuoc commune, HCMC"

# ===== UI =====
st.markdown("## 🎫 Employee Card Generator")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("👤 Name")
    emp_id = st.text_input("🆔 Employee ID")

with col2:
    team = st.text_input("🏢 Team")
    level = st.selectbox("🎯 Level", ["Công nhân", "Văn phòng"])

orientation = st.radio("📐 Orientation", ["Dọc", "Ngang"], horizontal=True)

photo = st.file_uploader("📷 Upload Photo", type=["jpg", "png"])

# ===== COLOR =====
color = (200, 30, 30) if level == "Công nhân" else (0, 120, 215)

# ===== MM → PX =====
def mm_to_px(mm, dpi=300):
    return int(mm * dpi / 25.4)

# ===== CREATE CARD =====
def create_card():
    is_vertical = orientation == "Dọc"

    if is_vertical:
        width = mm_to_px(60)
        height = mm_to_px(100)
    else:
        width = mm_to_px(100)
        height = mm_to_px(60)

    card = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(card)

    header_h = int(height * 0.15)
    footer_h = int(height * 0.12)

    # HEADER
    draw.rectangle((0, 0, width, header_h), fill=color)

    # FOOTER
    draw.rectangle((0, height - footer_h, width, height), fill=color)

    # FONT
    try:
        font_name = ImageFont.truetype("DejaVuSans-Bold.ttf", int(height * 0.08))
        font_id = ImageFont.truetype("DejaVuSans-Bold.ttf", int(height * 0.055))
        font_small = ImageFont.truetype("DejaVuSans.ttf", int(height * 0.045))
    except:
        font_name = ImageFont.load_default()
        font_id = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # LOGO
    try:
        logo = Image.open("assets/logo.png").convert("RGBA")
        logo.thumbnail((int(width * 0.2), header_h - 10))
        card.paste(logo, (10, int((header_h - logo.height)/2)), logo)
    except:
        pass

    # COMPANY NAME
    draw.text(
        (int(width * 0.25), int(header_h / 3)),
        COMPANY_NAME,
        fill="white",
        font=font_small
    )

    # FOOTER TEXT
    draw.text(
        (10, height - footer_h + 10),
        COMPANY_ADDRESS,
        fill="white",
        font=font_small
    )

    # ===== LAYOUT =====
    if is_vertical:
        photo_x = 10
        photo_y = header_h + 10
        frame_w = int(width * 0.32)
        frame_h = int(height * 0.35)

        text_x = photo_x + frame_w + 15
        text_y = photo_y
    else:
        photo_x = 10
        photo_y = header_h + 10
        frame_w = int(width * 0.28)
        frame_h = int(height * 0.6)

        text_x = photo_x + frame_w + 20
        text_y = photo_y + 10

    # ===== PHOTO =====
    if photo:
        img = Image.open(photo).convert("RGB")

        img_ratio = img.width / img.height
        frame_ratio = frame_w / frame_h

        if img_ratio > frame_ratio:
            new_height = frame_h
            new_width = int(img_ratio * new_height)
        else:
            new_width = frame_w
            new_height = int(new_width / img_ratio)

        img = img.resize((new_width, new_height))

        left = (new_width - frame_w) // 2
        top = (new_height - frame_h) // 2
        img = img.crop((left, top, left + frame_w, top + frame_h))

        card.paste(img, (photo_x, photo_y))

    # ===== TEXT =====
    draw.text((text_x, text_y), name, fill="black", font=font_name)
    draw.text((text_x, text_y + int(height * 0.12)), f"ID: {emp_id}", fill="black", font=font_id)
    draw.text((text_x, text_y + int(height * 0.22)), f"{team} - {level}", fill="black", font=font_small)

    return card

# ===== GENERATE =====
st.markdown("---")

if st.button("🚀 Generate Card", use_container_width=True):
    if name == "" or emp_id == "":
        st.warning("⚠️ Please fill Name and ID")
    else:
        card = create_card()

        st.image(card, caption="Preview", use_container_width=True)

        buf = io.BytesIO()
        card.save(buf, format="PNG")

        st.download_button(
            label="⬇️ Download Card",
            data=buf.getvalue(),
            file_name=f"{name}_{emp_id}.png",
            mime="image/png",
            use_container_width=True
        )
