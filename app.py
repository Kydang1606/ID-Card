# -*- coding: utf-8 -*-
import os
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# ===== FONT =====
def get_font(size, bold=False):
    font_list = [
        "assets/fonts/NotoSans-Bold.ttf" if bold else "assets/fonts/NotoSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]

    for f in font_list:
        if os.path.exists(f):
            try:
                return ImageFont.truetype(f, size)
            except:
                pass

    return ImageFont.load_default()

# ===== TEXT FIT =====
def fit_text_block(draw, text, max_width, max_height, max_size, bold=False):
    for size in range(max_size, 10, -2):
        font = get_font(size, bold)

        words = text.split()
        lines = []
        line = ""

        for w in words:
            test = (line + " " + w).strip()
            w_box = draw.textbbox((0, 0), test, font=font)[2]

            if w_box <= max_width:
                line = test
            else:
                if line:
                    lines.append(line)
                line = w

        if line:
            lines.append(line)

        if len(lines) > 2:
            continue

        line_height = int(size * 1.2)
        total_height = len(lines) * line_height

        if total_height <= max_height:
            return font, lines, line_height

    return get_font(14, bold), [text[:30] + "..."], int(14 * 1.2)

# ===== CREATE CARD =====
def create_card(name, emp_id, team, level):
    width, height = 1011, 638

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    margin_x = 60
    label_x = margin_x
    value_x = 320
    line_h = 90
    max_text_width = width - value_x - margin_x

    # HEADER
    header_font = get_font(48, True)
    title = "EMPLOYEE ID CARD"
    w = draw.textbbox((0, 0), title, font=header_font)[2]
    draw.text(((width - w)//2, 60), title, fill="black", font=header_font)

    draw.line((margin_x, 130, width - margin_x, 130), fill="black", width=2)

    label_font = get_font(30, True)

    data = [
        ("NAME", name),
        ("ID", emp_id),
        ("DEPARTMENT", team),
        ("POSITION", level),
    ]

    total_block_height = line_h * len(data)
    start_y = (height - total_block_height) // 2 + 40

    for i, (label, value) in enumerate(data):
        y = start_y + i * line_h

        draw.text((label_x, y), label, fill="black", font=label_font)

        if i == 0:
            max_size, bold, max_h = 72, True, line_h
        elif i == 1:
            max_size, bold, max_h = 60, True, int(line_h*0.9)
        else:
            max_size, bold, max_h = 42, False, int(line_h*0.9)

        font_val, lines, lh = fit_text_block(
            draw, value, max_text_width, max_h, max_size, bold
        )

        for j, line in enumerate(lines):
            draw.text((value_x, y + j * lh), line, fill="black", font=font_val)

    return img

# ===== STREAMLIT UI =====
st.set_page_config(page_title="Card Creator")

st.title("🎫 Employee Card Generator")

name = st.text_input("Name")
emp_id = st.text_input("ID")
team = st.text_input("Department")
level = st.text_input("Position")

if st.button("Create Card"):
    img = create_card(name, emp_id, team, level)

    buf = io.BytesIO()
    img.save(buf, format="PNG")

    st.image(img)

    st.download_button(
        "Download",
        buf.getvalue(),
        "card.png",
        "image/png"
    )
