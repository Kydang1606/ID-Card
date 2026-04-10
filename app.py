# -*- coding: utf-8 -*-
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import math
import os

# ================= CONFIG =================
COMPANY_NAME = "Triac Composites Co., LTD"
COMPANY_ADDRESS = "Factory 4, Depot Saigon, No9, Nguyen Van Tao, Hiep Phuoc commune, HCMC"

# ================= HELPER =================
def mm_to_px(mm):
    return int(mm * 3.78)

# ===== SAFE FONT LOADER (NO CRASH) =====
def get_font(size, bold=False):
    font_paths = [
        "assets/fonts/NotoSans-Bold.ttf" if bold else "assets/fonts/NotoSans-Regular.ttf",
        "./assets/fonts/NotoSans-Bold.ttf" if bold else "./assets/fonts/NotoSans-Regular.ttf"
    ]

    for path in font_paths:
        try:
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
        except:
            continue

    return ImageFont.load_default()

# ===== TEXT WRAP =====
def wrap_text(draw, text, font, max_w):
    words = text.split()
    lines, current = [], ""

    for word in words:
        test = current + (" " if current else "") + word
        w = draw.textbbox((0,0), test, font=font)[2]

        if w <= max_w:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines

# ===== FIT TEXT =====
def fit_and_wrap(draw, text, max_w, max_h, max_size, bold=False):
    for size in range(max_size, 12, -1):
        font = get_font(size, bold)
        lines = wrap_text(draw, text, font, max_w)

        line_h = int(size * 1.2)
        total_h = line_h * len(lines)

        if total_h <= max_h and len(lines) <= 2:
            return font, lines, line_h

    font = get_font(12, bold)
    lines = wrap_text(draw, text, font, max_w)
    return font, lines[:2], int(12*1.2)

# ================= UI =================
st.set_page_config(page_title="Card Creator", layout="centered")
st.title("🎫 Card Creator")

lang = st.selectbox("Language / Ngôn ngữ", ["English", "Tiếng Việt"])
orientation = st.selectbox("Orientation", ["Dọc", "Ngang"])

name = st.text_input("Name / Tên").strip()
emp_id = st.text_input("ID").strip()
team = st.selectbox("Team", ["Worker", "Offices"])
level = st.text_input("Level / Chức vụ").strip()

photo = st.file_uploader("Upload Photo", type=["jpg","png"])

color = (200,0,0) if team == "Worker" else (0,102,153)

def t(en, vi):
    return en if lang == "English" else vi

# ================= CARD =================
def create_card():
    is_vertical = orientation == "Dọc"

    width = mm_to_px(60 if is_vertical else 100)
    height = mm_to_px(100 if is_vertical else 60)

    card = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(card)

    header_h = int(height * 0.15)
    footer_h = int(height * 0.08)
    padding = int(height * 0.03)

    # ===== HEADER =====
    draw.rectangle((0,0,width,header_h), fill=color)

    logo_w = 0
    try:
        logo = Image.open("logo.png").convert("RGBA")
        logo.thumbnail((int(width*0.18), int(header_h*0.8)))
        logo_y = (header_h - logo.height)//2
        card.paste(logo, (10, logo_y), logo)
        logo_w = logo.width + 15
    except:
        pass

    # COMPANY NAME AUTO FIT
    font_size = int(header_h * 0.5)
    font_header = get_font(font_size, True)

    while font_size > 10:
        font_header = get_font(font_size, True)
        bbox = draw.textbbox((0,0), COMPANY_NAME, font=font_header)
        if bbox[2] <= width - logo_w - 20:
            break
        font_size -= 1

    text_y = (header_h - (bbox[3]-bbox[1]))//2
    draw.text((logo_w + 10, text_y), COMPANY_NAME, fill="white", font=font_header)

    # ===== CONTENT =====
    content_top = header_h + padding
    content_bottom = height - footer_h - padding

    if is_vertical:
        photo_h = int((content_bottom - content_top) * 0.45)

        if photo:
            img = Image.open(photo).convert("RGB")
            frame_w = int(width * 0.5)
            img = img.resize((frame_w, photo_h))

            mask = Image.new("L", (frame_w, photo_h), 0)
            ImageDraw.Draw(mask).rounded_rectangle((0,0,frame_w,photo_h), 20, fill=255)

            img_x = (width - frame_w)//2
            card.paste(img, (img_x, content_top), mask)

        text_start_y = content_top + photo_h + padding
        label_x = int(width * 0.08)
        value_x = int(width * 0.38)
        max_text_width = width - value_x - padding
        line_h = int(height * 0.085)

    else:
        content_h = content_bottom - content_top
        photo_w = int(width * 0.32)

        if photo:
            img = Image.open(photo).convert("RGB")
            img = img.resize((photo_w, content_h))

            mask = Image.new("L", (photo_w, content_h), 0)
            ImageDraw.Draw(mask).rounded_rectangle((0,0,photo_w,content_h), 20, fill=255)

            card.paste(img, (padding, content_top), mask)

        label_x = photo_w + padding*2
        value_x = label_x + int(width * 0.12)
        max_text_width = width - value_x - padding
        line_h = int(content_h * 0.2)
        text_start_y = content_top + (content_h - line_h*4)//2

    # ================= TEXT =================
    font_label = get_font(int(height*0.045), True)

    data = [
        (t("Name","Tên"), name),
        ("ID", emp_id),
        (t("Team","Bộ phận"), team),
        (t("Level","Chức vụ"), level)
    ]

    for i,(label,value) in enumerate(data):
        y = text_start_y + i*line_h

        draw.text((label_x,y), f"{label}:", fill="black", font=font_label)

        # ===== BIG NAME / ID =====
        if i == 0:
            max_size = int(height * 0.11)   # NAME BIGGEST
            bold = True
            limit_h = int(line_h * 1.4)
        elif i == 1:
            max_size = int(height * 0.095)  # ID BIG
            bold = True
            limit_h = int(line_h * 1.2)
        else:
            max_size = int(height * 0.05)
            bold = False
            limit_h = line_h

        font_val, lines, lh = fit_and_wrap(
            draw,
            value,
            max_text_width,
            limit_h,
            max_size,
            bold
        )

        for j, line in enumerate(lines):

            # center NAME
            if i == 0:
                w = draw.textbbox((0,0), line, font=font_val)[2]
                x = (width - w)//2
            else:
                x = value_x

            draw.text((x, y + j*lh), line, fill="black", font=font_val)

    # ================= FOOTER =================
    draw.rectangle((0,height-footer_h,width,height), fill=color)

    font_footer, lines, lh = fit_and_wrap(
        draw,
        COMPANY_ADDRESS,
        width - 20,
        footer_h,
        int(footer_h*0.5)
    )

    for i, line in enumerate(lines):
        draw.text((10, height-footer_h + i*lh), line, fill="white", font=font_footer)

    return card

# ================= A4 =================
def create_a4(cards):
    a4_w = mm_to_px(210)
    a4_h = mm_to_px(297)

    page = Image.new("RGB", (a4_w, a4_h), "white")

    cols = 2
    rows = math.ceil(len(cards)/cols)

    card_w, card_h = cards[0].size

    margin_x = (a4_w - cols*card_w)//(cols+1)
    margin_y = (a4_h - rows*card_h)//(rows+1)

    i = 0
    y = margin_y

    for r in range(rows):
        x = margin_x
        for c in range(cols):
            if i >= len(cards):
                break
            page.paste(cards[i], (x,y))
            x += card_w + margin_x
            i += 1
        y += card_h + margin_y

    return page

# ================= RUN =================
qty = st.number_input("Number of cards", 1, 20, 1)

if st.button("Create Card"):
    cards = [create_card() for _ in range(qty)]

    img = cards[0] if qty == 1 else create_a4(cards)

    buf = io.BytesIO()
    img.save(buf, format="PNG")

    st.image(img)
    st.download_button("Download", buf.getvalue(), "card.png", "image/png")
