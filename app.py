import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io, textwrap
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

# ===== CONFIG =====
st.set_page_config(page_title="Card Creator", layout="centered")

COMPANY_NAME = "Triac Composites Co., LTD"
COMPANY_ADDRESS = "Factory 4, Depot Saigon, No9, Nguyen Van Tao, Hiep Phuoc commune, HCMC"

# ===== LANGUAGE =====
lang = st.selectbox("🌐 Language / Ngôn ngữ", ["English", "Tiếng Việt"])

def t(en, vi):
    return en if lang == "English" else vi

# ===== UI HEADER =====
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

# ===== MULTI =====
st.markdown("### 📄 Batch Generate (Optional)")
quantity = st.number_input(t("Number of cards", "Số lượng thẻ"), min_value=1, max_value=50, value=1)

# ===== COLOR =====
color = (200, 0, 0) if team == "Worker" else (0, 102, 204)

# ===== UTIL =====
def mm_to_px(mm, dpi=300):
    return int(mm * dpi / 25.4)

def mm_to_pt(mm):
    return mm * 2.83465

def get_font(size, bold=False):
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()

def fit_text(draw, text, max_width, start_size, bold=False):
    size = start_size
    while size > 10:
        font = get_font(size, bold)
        if draw.textbbox((0,0), text, font=font)[2] <= max_width:
            return font
        size -= 2
    return get_font(10, bold)

def draw_center(draw, text, y, font, width):
    w = draw.textbbox((0,0), text, font=font)[2]
    draw.text(((width-w)//2, y), text, fill="black", font=font)

def wrap_text(text, n=20):
    return "\n".join(textwrap.wrap(text, n))

# ===== CREATE CARD =====
def create_card():
    is_vertical = orientation == "Dọc"
    width = mm_to_px(60 if is_vertical else 100)
    height = mm_to_px(100 if is_vertical else 60)

    card = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(card)

    header_h = int(height * 0.18)
    footer_h = int(height * 0.12)

    # HEADER
    draw.rectangle((0,0,width,header_h), fill=color)

    # LOGO
    logo_w = 0
    try:
        logo = Image.open("logo.png").convert("RGBA")
        logo.thumbnail((int(width*0.15), header_h-10))
        card.paste(logo,(10,(header_h-logo.height)//2),logo)
        logo_w = logo.width
    except:
        pass

    draw.text((logo_w+20, header_h//3), COMPANY_NAME, fill="white", font=get_font(int(header_h*0.35),True))

    # PHOTO
    if photo:
        img = Image.open(photo).convert("RGB")
        fw, fh = int(width*0.5), int(height*0.35)
        img.thumbnail((fw*2, fh*2))
        img = img.crop((0,0,fw,fh))
        card.paste(img, ((width-fw)//2, header_h+10))

    # TEXT
    y = header_h + int(height*0.42)
    max_w = width - 40

    lines = [
        f"{t('Name','Tên')}: {name}",
        f"ID: {emp_id}",
        f"{t('Team','Bộ phận')}: {team}",
        f"{t('Level','Chức vụ')}: {level}"
    ]

    sizes = [0.07,0.065,0.05,0.05]

    for i, line in enumerate(lines):
        line = wrap_text(line, 22)
        font = fit_text(draw, line, max_w, int(height*sizes[i]), i<2)
        draw_center(draw, line, y + i*60, font, width)

    # FOOTER
    draw.rectangle((0,height-footer_h,width,height), fill=color)
    draw.text((10,height-footer_h+10), COMPANY_ADDRESS, fill="white", font=get_font(int(footer_h*0.35)))

    return card

# ===== PDF EXPORT =====
def export_pdf(cards):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    page_w, page_h = A4
    card_w = mm_to_pt(60)
    card_h = mm_to_pt(100)

    cols = int(page_w // card_w)
    rows = int(page_h // card_h)

    x_margin = (page_w - cols*card_w)/2
    y_margin = (page_h - rows*card_h)/2

    i = 0
    for card in cards:
        col = i % cols
        row = (i // cols) % rows

        if i > 0 and i % (cols*rows) == 0:
            c.showPage()

        x = x_margin + col*card_w
        y = page_h - y_margin - (row+1)*card_h

        img_buf = io.BytesIO()
        card.save(img_buf, format="PNG")

        c.drawImage(ImageReader(img_buf), x, y, card_w, card_h)
        i += 1

    c.save()
    buffer.seek(0)
    return buffer

# ===== GENERATE =====
st.markdown("---")

if st.button(t("Generate", "Tạo"), use_container_width=True):
    if name == "" or emp_id == "":
        st.warning(t("Please fill Name and ID", "Vui lòng nhập Tên và Mã"))
    else:
        cards = [create_card() for _ in range(quantity)]

        st.image(cards[0], caption="Preview")

        # PNG
        buf = io.BytesIO()
        cards[0].save(buf, format="PNG")

        st.download_button("⬇ PNG", buf.getvalue(), file_name="card.png")

        # PDF
        pdf = export_pdf(cards)

        st.download_button("📄 PDF A4", pdf, file_name="cards.pdf")
