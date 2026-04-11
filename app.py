import os
from PIL import Image, ImageDraw, ImageFont

# =========================
# FONT LOADER (FIX UNICODE + STABLE)
# =========================
def get_font(size, bold=False):
    font_list = [
        "assets/fonts/NotoSans-Bold.ttf" if bold else "assets/fonts/NotoSans-Regular.ttf",

        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",

        "C:/Windows/Fonts/arialbd.ttf" if bold
        else "C:/Windows/Fonts/arial.ttf",
    ]

    for f in font_list:
        if os.path.exists(f):
            try:
                return ImageFont.truetype(f, size)
            except:
                pass

    return ImageFont.load_default()


# =========================
# TEXT FIT + WRAP + HEIGHT CONTROL (FIX CORE)
# =========================
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

        # giới hạn max 2 dòng
        if len(lines) > 2:
            continue

        line_height = int(size * 1.2)
        total_height = len(lines) * line_height

        if total_height <= max_height:
            return font, lines, line_height

    # fallback
    font = get_font(14, bold)
    return font, [text[:30] + "..."], int(14 * 1.2)


# =========================
# CREATE ID CARD PRO
# =========================
def create_card():
    width, height = 1011, 638

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    # ===== DATA =====
    name = "ĐẶNG VĨNH KỲ"
    emp_id = "2026001"
    team = "Engineering Department"
    level = "Senior Technician"

    # ===== MARGIN =====
    margin_x = 60
    margin_y = 50

    # ===== LAYOUT =====
    label_x = margin_x
    value_x = 320
    start_y = 180
    line_h = 90   # tăng để tránh đè

    max_text_width = width - value_x - margin_x

    # ===== HEADER =====
    header_font = get_font(48, True)
    title = "EMPLOYEE ID CARD"

    w = draw.textbbox((0, 0), title, font=header_font)[2]
    draw.text(((width - w)//2, 60), title, fill="black", font=header_font)

    draw.line((margin_x, 130, width - margin_x, 130), fill="black", width=2)

    # ===== LABEL FONT =====
    label_font = get_font(30, True)

    data = [
        ("NAME", name),
        ("ID", emp_id),
        ("DEPARTMENT", team),
        ("POSITION", level),
    ]

    # ===== AUTO CENTER BLOCK =====
    total_block_height = line_h * len(data)
    start_y = (height - total_block_height) // 2 + 40

    for i, (label, value) in enumerate(data):
        y = start_y + i * line_h

        # LABEL
        draw.text((label_x, y), label, fill="black", font=label_font)

        # SIZE RULE
        if i == 0:
            max_size = 72
            bold = True
            max_h = line_h

        elif i == 1:
            max_size = 60
            bold = True
            max_h = line_h * 0.9

        else:
            max_size = 42
            bold = False
            max_h = line_h * 0.9

        font_val, lines, lh = fit_text_block(
            draw,
            value,
            max_text_width,
            max_h,
            max_size,
            bold
        )

        # DRAW VALUE
        for j, line in enumerate(lines):
            draw.text(
                (value_x, y + j * lh),
                line,
                fill="black",
                font=font_val
            )

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
