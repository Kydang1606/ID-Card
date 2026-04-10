import os
from PIL import Image, ImageDraw, ImageFont

# =========================
# FONT LOADER (PRO DESIGN SAFE)
# =========================
def get_font(size, bold=False):
    """
    Font chuẩn design (Roboto/DejaVu fallback)
    chạy mọi môi trường (Windows/Linux/Cloud)
    """

    font_list = [
        # Linux (ổn định nhất)
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",

        # Ubuntu alternative
        "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/dejavu/DejaVuSans.ttf",

        # Windows
        "C:/Windows/Fonts/arialbd.ttf" if bold
        else "C:/Windows/Fonts/arial.ttf",

        # Roboto (nếu có cài)
        "/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/roboto/Roboto-Regular.ttf",
    ]

    for f in font_list:
        if os.path.exists(f):
            try:
                return ImageFont.truetype(f, size)
            except:
                pass

    return ImageFont.load_default()


# =========================
# TEXT WRAP + FIT
# =========================
def fit_text(draw, text, max_width, max_size, line_h, bold=False):
    size = max_size

    while size > 10:
        font = get_font(size, bold)
        words = text.split()
        lines = []
        line = ""

        for w in words:
            test = (line + " " + w).strip()
            if draw.textbbox((0, 0), test, font=font)[2] <= max_width:
                line = test
            else:
                lines.append(line)
                line = w

        if line:
            lines.append(line)

        if len(lines) * line_h <= line_h * 3:
            return font, lines, line_h

        size -= 2

    return get_font(12, bold), [text], line_h


# =========================
# CREATE ID CARD PRO
# =========================
def create_card():
    # ===== CARD SIZE (PVC STANDARD) =====
    width, height = 1011, 638  # ~ CR80 ratio upscale

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    # ===== MOCK DATA =====
    name = "NGUYEN VAN A"
    emp_id = "EMP ID: 2026001"
    team = "Engineering Department"
    level = "Senior Technician"

    # ===== SAFE MARGIN (PVC PRINT SAFE) =====
    margin_x = 60
    margin_y = 50

    # ===== LAYOUT =====
    label_x = margin_x
    value_x = 320
    start_y = 180
    line_h = 70

    max_text_width = width - value_x - margin_x

    # ===== HEADER =====
    header_font = get_font(48, True)
    title = "EMPLOYEE ID CARD"

    w = draw.textbbox((0, 0), title, font=header_font)[2]
    draw.text(((width - w)//2, 60), title, fill="black", font=header_font)

    # underline
    draw.line((margin_x, 130, width - margin_x, 130), fill="black", width=2)

    # ===== LABEL FONT =====
    label_font = get_font(30, True)

    data = [
        ("NAME", name),
        ("ID", emp_id),
        ("DEPARTMENT", team),
        ("POSITION", level),
    ]

    for i, (label, value) in enumerate(data):
        y = start_y + i * line_h

        # LABEL
        draw.text((label_x, y), label, fill="black", font=label_font)

        # ===== SIZE CONTROL =====
        if i == 0:   # NAME
            max_size = 72
            bold = True
            line_h2 = 50

        elif i == 1:  # ID
            max_size = 58
            bold = True
            line_h2 = 45

        else:
            max_size = 42
            bold = False
            line_h2 = 40

        font_val, lines, lh = fit_text(
            draw,
            value,
            max_text_width,
            max_size,
            line_h2,
            bold
        )

        # DRAW VALUE
        for j, line in enumerate(lines):
            x = value_x
            draw.text((x, y + j * lh), line, fill="black", font=font_val)

    return img


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)

    qty = 5
    for i in range(qty):
        img = create_card()
        img.save(f"output/id_card_{i+1}.png")

    print("DONE -> output/id_card_*.png")
