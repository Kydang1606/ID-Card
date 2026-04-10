import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap

# ===== CONFIG =====
st.set_page_config(page_title="Card Creator", layout="centered")

COMPANY_NAME = "Triac Composites Co., LTD"
COMPANY_ADDRESS = "Factory 4, Depot Saigon, No9, Nguyen Van Tao, Hiep Phuoc commune, HCMC"

# ===== LANGUAGE =====
lang = st.selectbox("🌐 Language / Ngôn ngữ", ["English", "Tiếng Việt"])

def t(en, vi):
    return en if lang == "English" else vi

# ===== HEADER UI =====
col_logo, col_title = st.columns([1, 4])

with col_logo:
    try:
        st.image("logo.png", width=60)
    except:
        pass

with col_title:
    st.markdown("## 🎫 Card Creator")
    st.caption(COMPANY_NAME)

st.markdown("---")

# ===== INPUT =====
col1, col2 = st.columns(2)

with col1:
    name = st.text_input(t("Name", "Tên"))
    emp_id = st.text_input(t("Employee ID", "Mã NV"))

with col2:
    team = st.selectbox(t("Team", "Bộ phận"), ["Worker", "Office"])
    level = st.text_input(t("Level", "Chức vụ"))

orientation = st.radio(t("Orientation", "Kiểu thẻ"), ["Dọc", "Ngang"], horizontal=True)

photo = st.file_uploader(t("Upload Photo", "Tải ảnh"), type=["jpg", "png"])

# ===== COLOR =====
color = (200, 0, 0) if team == "Worker" else (0, 102, 204)

# ===== UTIL =====
def mm_to_px(mm, dpi=300):
    return int(mm * dpi / 25.4)

def get_font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()

def fit_text(draw, text, max_width, start_size, bold=False):
    font_size = start_size
    while font_size > 10:
        font = get_font(font_size, bold)
        bbox = draw.textbbox((0, 0), text, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            return font
        font_size -= 2
    return get_font(10, bold)

def draw_center(draw, text, y, font, width):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (width - text_w) // 2
    draw.text((x, y), text, fill="black", font=font)

def wrap_text(text, max_chars=20):
    return "\n".join(textwrap.wrap(text, max_chars))

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

    header_h = int(height * 0.18)
    footer_h = int(height * 0.12)

    # HEADER
    draw.rectangle((0, 0, width, header_h), fill=color)

    # LOGO
    logo_w = 0
    try:
        logo = Image.open("logo.png").convert("RGBA")
        logo.thumbnail((int(width * 0.15), header_h - 10))
        card.paste(logo, (10, int((header_h - logo.height)/2)), logo)
        logo_w = logo.width
    except:
        pass

    # COMPANY NAME
    font_company = get_font(int(header_h * 0.35), True)
    draw.text((logo_w + 20, int(header_h/3)), COMPANY_NAME, fill="white", font=font_company)

    # PHOTO CENTER
    if photo:
        img = Image.open(photo).convert("RGB")

        frame_w = int(width * 0.5)
        frame_h = int(height * 0.35)

        img_ratio = img.width / img.height
        frame_ratio = frame_w / frame_h

        if img_ratio > frame_ratio:
            new_h = frame_h
            new_w = int(img_ratio * new_h)
        else:
            new_w = frame_w
            new_h = int(new_w / img_ratio)

        img = img.resize((new_w, new_h))

        left = (new_w - frame_w) // 2
        top = (new_h - frame_h) // 2
        img = img.crop((left, top, left + frame_w, top + frame_h))

        img_x = (width - frame_w) // 2
        img_y = header_h + 10

        card.paste(img, (img_x, img_y))

    # ===== TEXT =====
    text_y = header_h + int(height * 0.42)
    max_width = width - 40

    name_wrapped = wrap_text(name, 18)

    font_name = fit_text(draw, name_wrapped, max_width, int(height * 0.08), True)
    font_id = fit_text(draw, f"ID: {emp_id}", max_width, int(height * 0.07), True)
    font_team = fit_text(draw, team, max_width, int(height * 0.05))
    font_level = fit_text(draw, level, max_width, int(height * 0.05))

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap

# ===== CONFIG =====
st.set_page_config(page_title="Card Creator", layout="centered")

COMPANY_NAME = "Triac Composites Co., LTD"
COMPANY_ADDRESS = "Factory 4, Depot Saigon, No9, Nguyen Van Tao, Hiep Phuoc commune, HCMC"

# ===== LANGUAGE =====
lang = st.selectbox("🌐 Language / Ngôn ngữ", ["English", "Tiếng Việt"])

def t(en, vi):
    return en if lang == "English" else vi

# ===== HEADER UI =====
col_logo, col_title = st.columns([1, 4])

with col_logo:
    try:
        st.image("logo.png", width=60)
    except:
        pass

with col_title:
    st.markdown("## 🎫 Card Creator")
    st.caption(COMPANY_NAME)

st.markdown("---")

# ===== INPUT =====
col1, col2 = st.columns(2)

with col1:
    name = st.text_input(t("Name", "Tên"))
    emp_id = st.text_input(t("Employee ID", "Mã NV"))

with col2:
    team = st.selectbox(t("Team", "Bộ phận"), ["Worker", "Office"])
    level = st.text_input(t("Level", "Chức vụ"))

orientation = st.radio(t("Orientation", "Kiểu thẻ"), ["Dọc", "Ngang"], horizontal=True)

photo = st.file_uploader(t("Upload Photo", "Tải ảnh"), type=["jpg", "png"])

# ===== COLOR =====
color = (200, 0, 0) if team == "Worker" else (0, 102, 204)

# ===== UTIL =====
def mm_to_px(mm, dpi=300):
    return int(mm * dpi / 25.4)

def get_font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()

def fit_text(draw, text, max_width, start_size, bold=False):
    font_size = start_size
    while font_size > 10:
        font = get_font(font_size, bold)
        bbox = draw.textbbox((0, 0), text, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            return font
        font_size -= 2
    return get_font(10, bold)

def draw_center(draw, text, y, font, width):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (width - text_w) // 2
    draw.text((x, y), text, fill="black", font=font)

def wrap_text(text, max_chars=20):
    return "\n".join(textwrap.wrap(text, max_chars))

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

    header_h = int(height * 0.18)
    footer_h = int(height * 0.12)

    # HEADER
    draw.rectangle((0, 0, width, header_h), fill=color)

    # LOGO
    logo_w = 0
    try:
        logo = Image.open("logo.png").convert("RGBA")
        logo.thumbnail((int(width * 0.15), header_h - 10))
        card.paste(logo, (10, int((header_h - logo.height)/2)), logo)
        logo_w = logo.width
    except:
        pass

    # COMPANY NAME
    font_company = get_font(int(header_h * 0.35), True)
    draw.text((logo_w + 20, int(header_h/3)), COMPANY_NAME, fill="white", font=font_company)

    # PHOTO CENTER
    if photo:
        img = Image.open(photo).convert("RGB")

        frame_w = int(width * 0.5)
        frame_h = int(height * 0.35)

        img_ratio = img.width / img.height
        frame_ratio = frame_w / frame_h

        if img_ratio > frame_ratio:
            new_h = frame_h
            new_w = int(img_ratio * new_h)
        else:
            new_w = frame_w
            new_h = int(new_w / img_ratio)

        img = img.resize((new_w, new_h))

        left = (new_w - frame_w) // 2
        top = (new_h - frame_h) // 2
        img = img.crop((left, top, left + frame_w, top + frame_h))

        img_x = (width - frame_w) // 2
        img_y = header_h + 10

        card.paste(img, (img_x, img_y))

    # ===== TEXT =====
    text_y = header_h + int(height * 0.42)
    max_width = width - 40

    name_wrapped = wrap_text(name, 18)

    font_name = fit_text(draw, name_wrapped, max_width, int(height * 0.08), True)
    font_id = fit_text(draw, f"ID: {emp_id}", max_width, int(height * 0.07), True)
    font_team = fit_text(draw, team, max_width, int(height * 0.05))
    font_level = fit_text(draw, level, max_width, int(height * 0.05))

    draw_center(draw, name_wrapped, text_y, font_name, width)
    draw_center(draw, f"ID: {emp_id}", text_y + 60, font_id, width)
    draw_center(draw, team, text_y + 120, font_team, width)
    draw_center(draw, level, text_y + 160, font_level, width)

    # FOOTER
    draw.rectangle((0, height - footer_h, width, height), fill=color)

    font_footer = get_font(int(footer_h * 0.35))
    draw.text((10, height - footer_h + 10), COMPANY_ADDRESS, fill="white", font=font_footer)

    return card

# ===== GENERATE =====
st.markdown("---")

if st.button(t("Generate Card", "Tạo thẻ"), use_container_width=True):
    if name == "" or emp_id == "":
        st.warning(t("Please fill Name and ID", "Vui lòng nhập Tên và Mã"))
    else:
        card = create_card()

        st.image(card, caption="Preview", use_container_width=True)

        buf = io.BytesIO()
        card.save(buf, format="PNG")

        st.download_button(
            label=t("Download", "Tải về"),
            data=buf.getvalue(),
            file_name=f"{name}_{emp_id}.png",
            mime="image/png",
            use_container_width=True
        )

    # FOOTER
    draw.rectangle((0, height - footer_h, width, height), fill=color)

    font_footer = get_font(int(footer_h * 0.35))
    draw.text((10, height - footer_h + 10), COMPANY_ADDRESS, fill="white", font=font_footer)

    return card

# ===== GENERATE =====
st.markdown("---")

if st.button(t("Generate Card", "Tạo thẻ"), use_container_width=True):
    if name == "" or emp_id == "":
        st.warning(t("Please fill Name and ID", "Vui lòng nhập Tên và Mã"))
    else:
        card = create_card()

        st.image(card, caption="Preview", use_container_width=True)

        buf = io.BytesIO()
        card.save(buf, format="PNG")

        st.download_button(
            label=t("Download", "Tải về"),
            data=buf.getvalue(),
            file_name=f"{name}_{emp_id}.png",
            mime="image/png",
            use_container_width=True
        )
