import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Employee Card", layout="centered")

st.title("🎫 Employee Card Generator")

# ===== INPUT =====
name = st.text_input("👤 Name")
emp_id = st.text_input("🆔 Employee ID")
team = st.text_input("🏢 Team")
level = st.selectbox("🎯 Level", ["Công nhân", "Văn phòng"])

photo = st.file_uploader("📷 Upload Photo", type=["jpg", "png"])

# ===== COLOR =====
if level == "Công nhân":
    color = (200, 30, 30)  # đỏ
else:
    color = (0, 120, 215)  # xanh

# ===== FUNCTION TẠO THẺ =====
def create_card():
    width, height = 600, 350
    card = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(card)

    # Header
    draw.rectangle((0, 0, width, 60), fill=color)
    draw.text((20, 15), "COMPANY NAME", fill="white")

    # Footer
    draw.rectangle((0, height - 50, width, height), fill=color)
    draw.text((20, height - 35), "company.com", fill="white")

    # Font
    try:
        font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
        font_small = ImageFont.truetype("DejaVuSans.ttf", 18)
    except:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Text
    draw.text((200, 120), name, fill="black", font=font_big)
    draw.text((200, 160), f"ID: {emp_id}", fill="black", font=font_small)
    draw.text((200, 200), f"{team} - {level}", fill="black", font=font_small)

    # Photo (auto fit)
    if photo:
        img = Image.open(photo).convert("RGB")

        frame_w, frame_h = 140, 180
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

        card.paste(img, (40, 100))

    return card

# ===== GENERATE =====
if st.button("🚀 Generate Card"):
    if name == "" or emp_id == "":
        st.warning("⚠️ Please fill Name and ID")
    else:
        card = create_card()
        st.image(card, caption="Preview")

        # Download
        buf = io.BytesIO()
        card.save(buf, format="PNG")
        st.download_button(
            label="⬇️ Download Card",
            data=buf.getvalue(),
            file_name=f"{name}_{emp_id}.png",
            mime="image/png"
        )
