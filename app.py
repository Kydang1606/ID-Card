import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(layout="centered")

# =========================
# CONFIG
# =========================
COMPANY = "ABC COMPANY"
ADDRESS = "123 ABC STREET"
LOGO_PATH = "logo.png"  # để cùng folder

# =========================
# LOAD FONT
# =========================
def load_font(size, bold=False):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()

# =========================
# AUTO TEXT (WRAP + FIT)
# =========================
def draw_text_block(draw, text, box, base_size, bold=False):
    x, y, w, h = box
    size = base_size
    
    while size > 10:
        font = load_font(size, bold)
        words = text.split()
        lines = []
        current = ""

        for word in words:
            test = current + " " + word if current else word
            bbox = draw.textbbox((0,0), test, font=font)
            if bbox[2] <= w:
                current = test
            else:
                lines.append(current)
                current = word

        if current:
            lines.append(current)

        if len(lines) <= 2:
            total_h = len(lines) * (bbox[3] + 5)
            if total_h <= h:
                break

        size -= 2

    yy = y + (h - total_h)//2
    for line in lines:
        bbox = draw.textbbox((0,0), line, font=font)
        xx = x + (w - bbox[2])//2
        draw.text((xx, yy), line, fill="black", font=font)
        yy += bbox[3] + 5

# =========================
# PROCESS IMAGE
# =========================
def fit_image(img, box):
    target_w, target_h = box
    img_ratio = img.width / img.height
    box_ratio = target_w / target_h

    if img_ratio > box_ratio:
        new_h = target_h
        new_w = int(new_h * img_ratio)
    else:
        new_w = target_w
        new_h = int(new_w / img_ratio)

    img = img.resize((new_w, new_h))
    
    left = (new_w - target_w)//2
    top = (new_h - target_h)//2
    
    return img.crop((left, top, left+target_w, top+target_h))

# =========================
# CREATE CARD
# =========================
def create_card(name, id_, team, level, photo):
    
    if team == "Worker":
        W, H = 900, 600
        color = (200, 0, 0)
        layout = "horizontal"
    else:
        W, H = 600, 900
        color = (0, 100, 200)
        layout = "vertical"

    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)

    # HEADER
    draw.rectangle((0, 0, W, 80), fill=color)

    # LOGO
    try:
        logo = Image.open(LOGO_PATH)
        logo = logo.resize((60,60))
        img.paste(logo, (10,10))
    except:
        pass

    # COMPANY NAME (2/3)
    draw.text((W//3, 25), COMPANY, fill="white", font=load_font(20, True))

    # FOOTER
    draw.rectangle((0, H-60, W, H), fill=color)
    draw.text((W//2 - 100, H-45), ADDRESS, fill="white", font=load_font(14))

    # PHOTO
    photo = fit_image(photo, (int(W*0.33), int(H*0.5)))

    if layout == "horizontal":
        img.paste(photo, (20, 120))

        # TEXT RIGHT
        draw_text_block(draw, f"Name: {name}", (350, 120, 500, 80), 28, True)
        draw_text_block(draw, f"ID: {id_}", (350, 200, 500, 80), 28, True)
        draw_text_block(draw, f"Level: {level}", (350, 300, 500, 60), 18)
        draw_text_block(draw, f"Team: {team}", (350, 360, 500, 60), 18)

    else:
        img.paste(photo, (int(W*0.33), 120))

        # TEXT BELOW
        draw_text_block(draw, f"Name: {name}", (50, 400, W-100, 80), 28, True)
        draw_text_block(draw, f"ID: {id_}", (50, 480, W-100, 80), 28, True)
        draw_text_block(draw, f"Level: {level}", (50, 580, W-100, 60), 18)
        draw_text_block(draw, f"Team: {team}", (50, 640, W-100, 60), 18)

    return img

# =========================
# UI
# =========================
st.title("ID Card Generator")

name = st.text_input("Name")
id_ = st.text_input("ID")
team = st.selectbox("Team", ["Worker", "Office"])
level = st.text_input("Level")
photo = st.file_uploader("Upload Photo", type=["jpg","png"])

if st.button("Generate"):
    if photo:
        img = Image.open(photo)
        card = create_card(name, id_, team, level, img)
        
        st.image(card)

        buf = io.BytesIO()
        card.save(buf, format="PNG")
        
        st.download_button("Download", buf.getvalue(), "card.png")
