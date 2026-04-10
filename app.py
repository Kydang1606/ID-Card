def create_card():
    is_vertical = orientation == "Dọc"

    width = mm_to_px(60 if is_vertical else 100)
    height = mm_to_px(100 if is_vertical else 60)

    card = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(card)

    # ===== LAYOUT TỶ LỆ =====
    header_h = int(height * 0.18)
    footer_h = int(height * 0.12)
    photo_h = int(height * 0.35)
    padding = int(height * 0.03)

    text_area_h = height - (header_h + footer_h + photo_h + padding*3)

    # ===== HEADER =====
    draw.rectangle((0, 0, width, header_h), fill=color)

    # LOGO
    logo_w = 0
    try:
        logo = Image.open("logo.png").convert("RGBA")
        logo.thumbnail((int(width*0.15), header_h-10))
        card.paste(logo, (10, (header_h-logo.height)//2), logo)
        logo_w = logo.width
    except:
        pass

    draw.text(
        (logo_w + 20, header_h//3),
        COMPANY_NAME,
        fill="white",
        font=get_font(int(header_h*0.35), True)
    )

    # ===== PHOTO (CENTER FIT CHUẨN) =====
    if photo:
        img = Image.open(photo).convert("RGB")

        frame_w = int(width * 0.5)
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

        img_x = (width - frame_w)//2
        img_y = header_h + padding

        card.paste(img, (img_x, img_y))

    # ===== TEXT ZONE =====
    text_start_y = header_h + photo_h + padding*2
    max_w = width - 40

    lines = [
        f"{t('Name','Tên')}: {name}",
        f"ID: {emp_id}",
        f"{t('Team','Bộ phận')}: {team}",
        f"{t('Level','Chức vụ')}: {level}"
    ]

    # 👉 CHIA ĐỀU KHUNG TEXT
    line_spacing = text_area_h // len(lines)

    for i, line in enumerate(lines):
        line = wrap_text(line, 22)

        font = fit_text(
            draw,
            line,
            max_w,
            int(line_spacing * 0.6),   # 👈 key fix
            bold=(i < 2)
        )

        y = text_start_y + i * line_spacing
        draw_center(draw, line, y, font, width)

    # ===== FOOTER =====
    draw.rectangle((0, height-footer_h, width, height), fill=color)

    font_footer = fit_text(
        draw,
        COMPANY_ADDRESS,
        width - 20,
        int(footer_h * 0.4)
    )

    draw_center(draw, COMPANY_ADDRESS, height - footer_h + padding, font_footer, width)

    return card
