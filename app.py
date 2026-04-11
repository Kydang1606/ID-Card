import streamlit as st
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(layout="centered")

# =========================
# CONFIG
# =========================
COMPANY = "TRIAC COMPOSITES CO., LTD"
ADDRESS = """UniDepot, Factory No 4, Nguyen Van Tao St,
Hiep Phuoc Commune,
HCMC, 700000, Vietnam"""

LOGO_PATH = "logo.png"

# =========================
# LOAD FONT (VIETNAMESE OK)
# =========================
def load_font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("Roboto-Bold.ttf", size)
        return ImageFont.truetype("Roboto-Regular.ttf", size)
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

        line_h = draw.textbbox((0,0), "A", font=font)[3] + 5
        total_h = len(lines) * line_h

        if len(lines) <= 2 and total_h <= h:
            break

        size -= 2

    yy = y + (h - total_h)//2

    for line in lines:
        bbox = draw.textbbox((0,0), line, font=font)
        xx = x + (w - bbox[2])//2
        draw.text((xx, yy), line, fill="black", font=font)
        yy += line_h

# =========================
# MULTILINE (ADDRESS)
# =========================
def draw_multiline(draw, text, box, size):
    x, y, w, h = box
    font = load_font(size)
    lines = text.split("\n")

    line_h = draw.textbbox((0,0), "A", font=font)[3] + 4
    total_h = len(lines) * line_h

    yy = y + (h - total_h)//2

    for line in lines:
        bbox = draw.textbbox((0,0), line, font=font)
        xx = x + (w - bbox[2])//2
        draw.text((xx, yy), line, fill="white", font=font)
        yy += line_h

# =========================
# IMAGE FIT
# =========================
def fit_image(img, box):
    target_w, target_h = box
    ratio = img.width / img.height
    box_ratio = target_w / target_h

    if ratio > box_ratio:
        new_h = target_h
        new_w = int(new_h * ratio)
    else:
        new_w = target_w
        new_h = int(new_w / ratio)

    img = img.resize((new_w, new_h))

    left = (new_w - target_w)//2
    top = (new_h - target_h)//2

    return img.crop((left, top, left+target_w, top+target_h))

# =========================
# CREATE CARD
# =========================
def create_card(name, id_, team, level, photo):

    if team == "Worker":
        W, H = 1000, 600
        color = (200, 0, 0)
        layout = "horizontal"
    else:
        W, H = 600, 1000
        color = (0, 102, 153)
        layout = "vertical"

    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)

    # HEADER
    draw.rectangle((0, 0, W, 100), fill=color)

    # LOGO
    try:
        logo = Image.open(LOGO_PATH).convert("RGBA")
        logo = logo.resize((80, 80))
        img.paste(logo, (10, 10), logo)
    except:
        pass

    # COMPANY NAME (2/3)
    draw_text_block(draw, COMPANY, (W//3, 0, int(W*2/3)-20, 100), 28, True)

    # FOOTER
    draw.rectangle((0, H-100, W, H), fill=color)
    draw_multiline(draw, ADDRESS, (0, H-100, W, 100), 16)

    # PHOTO
    if layout == "horizontal":
        photo_box = (int(W*0.33), int(H*0.6))
        photo = fit_image(photo, photo_box)
        img.paste(photo, (20, 120))

        # TEXT RIGHT
        draw_text_block(draw, name, (350, 150, 600, 80), 36, True)
        draw_text_block(draw, f"ID: {id_}", (350, 230, 600, 70), 28, True)
        draw_text_block(draw, f"Level: {level}", (350, 320, 600, 60), 20)
        draw_text_block(draw, f"Team: {team}", (350, 380, 600, 60), 20)

    else:
        photo_box = (int(W*0.6), int(H*0.33))
        photo = fit_image(photo, photo_box)
        img.paste(photo, (int(W*0.2), 120))

        # TEXT BELOW
        draw_text_block(draw, name, (50, 450, W-100, 80), 36, True)
        draw_text_block(draw, f"ID: {id_}", (50, 530, W-100, 70), 28, True)
        draw_text_block(draw, f"Level: {level}", (50, 620, W-100, 60), 20)
        draw_text_block(draw, f"Team: {team}", (50, 680, W-100, 60), 20)

    return img

# =========================
# UI
# =========================
st.title("ID Card - TRIAC")

name = st.text_input("Name")
id_ = st.text_input("ID")
team = st.selectbox("Team", ["Worker", "Office"])
level = st.text_input("Level")
photo = st.file_uploader("Upload Photo", type=["jpg","png"])

if st.button("Generate"):
    if photo:
        img = Image.open(photo)
        card = create_card(name, id_, team, level, img)

        st.image(card, use_column_width=True)
