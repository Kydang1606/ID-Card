import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import math

# ===== CONFIG =====
COMPANY_NAME = "Triac Composites Co., LTD"
COMPANY_ADDRESS = "Factory 4, Depot Saigon, No9, Nguyen Van Tao, Hiep Phuoc commune, HCMC"

# ===== HELPER =====
def mm_to_px(mm):
    return int(mm * 3.78)

def get_font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("arialbd.ttf", size)
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()

def fit_text(draw, text, max_w, max_size, bold=False):
    for size in range(max_size, 10, -1):
        font = get_font(size, bold)
        bbox = draw.textbbox((0,0), text, font=font)
        if bbox[2] <= max_w:
            return font
    return get_font(12)

# ===== UI =====
st.set_page_config(page_title="Card Creator", layout="centered")

st.title("🎫 Card Creator")

lang = st.selectbox("Language / Ngôn ngữ", ["English", "Tiếng Việt"])
orientation = st.selectbox("Orientation", ["Dọc", "Ngang"])

name = st.text_input("Name / Tên")
emp_id = st.text_input("ID")
team = st.selectbox("Team", ["Worker", "Offices"])
level = st.text_input("Level / Chức vụ")

photo = st.file_uploader("Upload Photo", type=["jpg","png"])

# ===== TEAM COLOR =====
color = (200,0,0) if team == "Worker" else (0,102,153)

def t(en, vi):
    return en if lang == "English" else vi

# ===== CREATE CARD =====
def create_card():
    is_vertical = orientation == "Dọc"

    width = mm_to_px(60 if is_vertical else 100)
    height = mm_to_px(100 if is_vertical else 60)

    card = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(card)

    # ===== LAYOUT (FIX CHUẨN KHÔNG NGẮN) =====
    header_h = int(height * 0.15)
    footer_h = int(height * 0.08)
    photo_h  = int(height * 0.35)
    padding  = int(height * 0.03)

    # ===== HEADER =====
    draw.rectangle((0,0,width,header_h), fill=color)

    # LOGO
    logo_w = 0
    try:
        logo = Image.open("logo.png").convert("RGBA")
        logo.thumbnail((int(width*0.14), header_h-10))
        card.paste(logo, (10,(header_h-logo.height)//2), logo)
        logo_w = logo.width
    except:
        pass

    font_header = get_font(int(header_h*0.4), True)
    draw.text((logo_w+20, header_h//3), COMPANY_NAME, fill="white", font=font_header)

    # ===== PHOTO =====
    if photo:
        img = Image.open(photo).convert("RGB")

        frame_w = int(width * 0.45)
        frame_h = photo_h

        img_ratio = img.width / img.height
        frame_ratio = frame_w / frame_h

        if img_ratio > frame_ratio:
            new_h = frame_h
            new_w = int(img_ratio * new_h)
        else:
            new_w = frame_w
            new_h = int(new_w / img_ratio)

        img = img.resize((new_w, new_h))

        left = (new_w - frame_w)//2
        top = (new_h - frame_h)//2
        img = img.crop((left, top, left+frame_w, top+frame_h))

        mask = Image.new("L", (frame_w, frame_h), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle((0,0,frame_w,frame_h), radius=20, fill=255)

        img_x = (width - frame_w)//2
        img_y = header_h + padding

        card.paste(img, (img_x,img_y), mask)

    # ===== TEXT =====
    text_start_y = header_h + photo_h + padding*2

    label_x = int(width * 0.1)
    value_x = int(width * 0.35)

    line_h = int(height * 0.085)

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

        font_val = fit_text(draw, value, width-value_x-10, int(height*0.05))
        draw.text((value_x,y), value, fill="black", font=font_val)

    # ===== FOOTER =====
    draw.rectangle((0,height-footer_h,width,height), fill=color)

    font_footer = fit_text(draw, COMPANY_ADDRESS, width-20, int(footer_h*0.4))
    draw.text((10,height-footer_h+5), COMPANY_ADDRESS, fill="white", font=font_footer)

    return card

# ===== CREATE MULTIPLE CARDS (A4) =====
def create_a4(cards):
    a4_w = mm_to_px(210)
    a4_h = mm_to_px(297)

    page = Image.new("RGB", (a4_w, a4_h), "white")

    cols = 2
    rows = math.ceil(len(cards)/cols)

    card_w, card_h = cards[0].size

    margin_x = (a4_w - cols*card_w)//(cols+1)
    margin_y = (a4_h - rows*card_h)//(rows+1)

    x = margin_x
    y = margin_y

    i = 0
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

# ===== ACTION =====
qty = st.number_input("Number of cards", 1, 20, 1)

if st.button("Create Card"):
    cards = [create_card() for _ in range(qty)]

    if qty == 1:
        img = cards[0]
    else:
        img = create_a4(cards)

    buf = io.BytesIO()
    img.save(buf, format="PNG")

    st.image(img)
    st.download_button("Download", buf.getvalue(), "card.png", "image/png")
