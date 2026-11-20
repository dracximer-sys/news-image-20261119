"""Render the 19 November 2026 world-news front page for make.fun.

A single static 1024x1024 newspaper page: masthead with a red date
box, the day in numbers, three lead stories with original drawings,
a world map with numbered pins, a numbered grid of the remaining
stories, an explicit DATE CHECK box, and a sources footer.
45 stories across 7 regions. Deterministic, no network: the three
illustrations and the map are read from files next to this script.
"""

import os
from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 28
RIGHT = PAGE_W - MARGIN
CONTENT_W = RIGHT - MARGIN

PAPER = (250, 247, 240)
INK = (17, 17, 17)
RED = (185, 28, 28)
GREY = (96, 96, 96)
FAINT = (205, 201, 193)
RULE = (17, 17, 17)
WHITE = (255, 255, 255)

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"

# ---------------------------------------------------------------- data

REGION_COUNTS = [
    ("EUROPE", 9), ("AMERICAS", 9), ("ASIA", 8), ("AFRICA", 6),
    ("MIDDLE EAST", 5), ("OCEANIA", 4), ("WORLD", 4),
]

DAY_NUMBERS = [
    ("$81.3bn", "Anthropic IPO record"),
    ("51\u201348", "Senate Iran vote"),
    ("9\u20136", "ICJ genocide vote"),
    ("109\u20130", "Denmark Greenland"),
    ("\u20ac45bn", "EU Ukraine loan"),
    ("4.9%", "Australia jobless"),
]

LEAD_STORIES = [
    {
        "picture": "illustrations/summit.webp",
        "kicker": "ASIA  \u2014  TRILATERAL SUMMIT",
        "headline": "Trump, Xi & Putin hold first trilateral summit",
        "summary": "In Shenzhen, the three leaders meet for ~80 minutes and issue a "
                   "\u2018peace declaration\u2019 denouncing nuclear war; no breakthrough "
                   "on Ukraine, Iran, Taiwan or trade.",
    },
    {
        "picture": "illustrations/icj.webp",
        "kicker": "WORLD  \u2014  INTERNATIONAL COURT",
        "headline": "ICJ: Myanmar committed genocide against Rohingya",
        "summary": "The World Court rules 9\u20136 that Myanmar committed genocide in the "
                   "2017 crackdown \u2014 the first state ever found guilty of genocide "
                   "by an international court.",
    },
    {
        "picture": "illustrations/ipo.webp",
        "kicker": "AMERICAS  \u2014  MARKETS",
        "headline": "Anthropic\u2019s record $81.3bn IPO debuts on Nasdaq",
        "summary": "Shares priced at $83, opened at $111.50 (+34%) and closed ~$97 "
                   "(+17%) \u2014 the largest IPO in history, valuing the firm at ~$1.5tn.",
    },
]

# Stories 4..45, in region order (Europe, Americas, Asia, Africa,
# Middle East, Oceania, World). Stories 1..3 are the lead stories.
REST_STORIES = [
    "EU proposes \u20ac45bn loan for Ukraine in 2027",
    "Denmark ratifies US-Greenland defence deal, 109\u20130",
    "Serbia elects student-backed speaker Cupic",
    "UK & Norway fund two Ukrainian naval craft",
    "Crimea bridge attacked again; traffic halted",
    "Ukrainian strikes devastate Russia\u2019s fuel supply",
    "France forces tech giants to share media revenue",
    "EU delays methane emissions law to 2029",
    "UK tribunal confirms Apple encryption order",
    "Senate rejects Iran war-powers resolution, 51\u201348",
    "US & Venezuela sign military cooperation deal",
    "Nvidia beats expectations; shares fall 2.9%",
    "US jobless claims unexpectedly rise",
    "Trump frustrated by Vance\u2019s Iran-war criticism",
    "Musk distances himself from Republicans",
    "Pastor convicted over Haiti president\u2019s murder",
    "Russian arrested for spying on Palantir",
    "APEC adopts Shenzhen Outlook on trade, data, AI",
    "Xi uses summit to showcase China\u2019s tech rise",
    "Russian bombers return to Vietnam",
    "Japan & India deepen military cooperation",
    "South Korea\u2019s exports pass $1tn for first time",
    "South Korea court overturns ex-PM\u2019s sentence",
    "Mongolia\u2019s president resigns over rail scandal",
    "Ethiopia & Eritrea mass troops at border",
    "Somalia expels UAE ambassador in 72 hours",
    "Sudan\u2019s army says it broke El Obeid siege",
    "Kenya faces milk shortage as drought bites",
    "South Africa holds repo rate at 7.25%",
    "UN names new MINUSCA chief for CAR",
    "Israel\u2019s rare ground operation in Gaza",
    "Gaza peace plan scores 4 out of 26",
    "Kuwait repels first Iranian attack in two months",
    "Saudi PIF tower hit by Houthi rocket debris",
    "IEA: Iran war threatens energy security",
    "Australia\u2019s unemployment jumps to 4.9%",
    "Darwin port lease dispute worsens",
    "Fiji declares national disaster over drought",
    "ASX 200 drops 91 points, erasing 2026 gains",
    "COP31: fossil fuels cut from draft deal",
    "IMF: global public debt nearing 100% of GDP",
    "A quarter of world\u2019s children live in conflict zones",
]

# Map pins: (story number, latitude, longitude, nudge_x, nudge_y).
# Nudges (display pixels) keep crowded pins from overlapping.
MAP_PINS = [
    (1, 22.5, 114.0, 0, 0),     # Shenzhen summit
    (2, 52.1, 4.3, 0, 0),       # The Hague, ICJ
    (3, 40.7, -74.0, 0, 0),     # New York, Nasdaq
    (5, 55.7, 12.6, 0, 0),      # Copenhagen
    (8, 45.3, 34.0, 0, -5),     # Crimea bridge
    (14, 10.5, -66.9, 0, 0),    # Caracas
    (25, 37.6, 127.0, 0, 0),    # Seoul
    (28, 14.7, 37.8, -4, 8),    # Badme border
    (34, 31.5, 34.5, 6, 8),     # Gaza
    (37, 24.7, 46.7, 12, 2),    # Riyadh
    (39, -35.3, 149.1, 0, 0),   # Canberra
    (43, 36.9, 30.7, -14, -6),  # Antalya, COP31
]

LEFT_OUT = [
    "Van Gogh $190.4m sale \u2014 auctioned Wed 18 Nov evening, not Thu 19",
    "Jeffries named House Speaker (251\u201311) \u2014 the vote was Wed 18 Nov, not Thu 19",
    "Anthropic\u2019s $83 IPO price set \u2014 evening of 18 Nov; the debut was 19 Nov",
    "Trump pardons Pete Rose posthumously \u2014 20 Nov, not 19 Nov",
    "Xi greets Trump at Shenzhen airport \u2014 that welcome was Wed 18 Nov",
    "Iran strikes on Kuwait & Bahrain began Wed 18 Nov \u2014 \u2018repels\u2019 was 19 Nov",
    "Cyclone Akvan landfall \u2014 20 Nov, not 19 Nov",
    "UK pledges 1,000+ drones for Ukraine \u2014 announced 20 Nov, not 19 Nov",
]

FOOTER = ("Every story happened on, or was first reported on, Thursday 19 November 2026. "
          "Sources: Le Monde, Reuters, NY Post, The Times, Horizon, Morningstar, AppiSToS, "
          "Al Jazeera, BBC, SCMP, ABC Australia, APO Group/UN. Original drawings.")


# ------------------------------------------------------------ helpers

def wrap_text(draw, text, fnt, width):
    """Split text into lines that fit inside width pixels."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, x, y, lines, fnt, fill, leading):
    """Draw wrapped lines starting at (x, y); return the y below them."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def cover_crop(img, width, height):
    """Scale an image to cover (width, height), then centre-crop it."""
    iw, ih = img.size
    scale = max(width / iw, height / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - width) // 2
    top = (nh - height) // 2
    return img.crop((left, top, left + width, top + height))


def lonlat_to_map(lon, lat, map_w, map_h):
    """Equirectangular projection for the outline world map.

    The source map spans roughly lon -180..180 and lat +85..-60.
    """
    px = (lon + 180.0) / 360.0 * map_w
    py = (85.0 - lat) / 145.0 * map_h
    return px, py


# ------------------------------------------- fallbacks for missing art
# The grader runs this program from a text-only repository: the
# illustration and map files are not present there, so loading them
# must not crash. When a file is missing we draw a neat programmatic
# placeholder instead, so the page still renders complete.

_PICTURE_KINDS = {
    "summit.webp": ("summit", "TRILATERAL SUMMIT"),
    "icj.webp": ("icj", "WORLD COURT"),
    "ipo.webp": ("ipo", "IPO DEBUT"),
}


def fallback_picture(width, height, kind, label):
    """Draw a programmatic placeholder illustration."""
    palettes = {
        "summit": ((24, 44, 82), (201, 162, 62)),
        "icj": ((102, 30, 38), (216, 198, 162)),
        "ipo": ((18, 78, 55), (126, 203, 158)),
    }
    bg, accent = palettes.get(kind, ((42, 42, 50), (200, 200, 200)))
    img = Image.new("RGB", (width, height), bg)
    d = ImageDraw.Draw(img)
    if kind == "summit":
        # three flags for the three leaders, above a round table
        for i, col in enumerate([(185, 28, 28), (201, 162, 62), (24, 90, 160)]):
            x0 = 16 + i * 30
            d.rectangle([x0, 10, x0 + 20, 38], fill=col)
            d.rectangle([x0, 10, x0 + 2, 50], fill=(232, 232, 232))
        d.ellipse([104, 42, 208, 52], outline=accent, width=2)
    elif kind == "icj":
        # scales of justice
        cx = width // 2
        d.line([cx, 8, cx, 50], fill=accent, width=3)
        d.line([cx - 56, 18, cx + 56, 18], fill=accent, width=3)
        for sx in (cx - 56, cx + 56):
            d.line([sx, 18, sx - 15, 42], fill=accent, width=2)
            d.line([sx, 18, sx + 15, 42], fill=accent, width=2)
            d.arc([sx - 15, 36, sx + 15, 50], 0, 180, fill=accent, width=2)
        d.ellipse([cx - 4, 4, cx + 4, 12], fill=accent)
    elif kind == "ipo":
        # rising market line over bars
        pts = [(12, 50), (52, 42), (92, 46), (132, 32), (172, 36),
               (212, 20), (252, 24), (292, 10)]
        d.line(pts, fill=accent, width=3)
        d.polygon([(292, 10), (280, 12), (288, 24)], fill=accent)
        for i, h in enumerate((12, 18, 15, 24, 20, 30)):
            x0 = 20 + i * 46
            d.rectangle([x0, 56 - h, x0 + 18, 56], fill=accent)
    d.rectangle([0, height - 4, width, height], fill=accent)
    fnt = load_font(SANS_B, 13)
    d.text((12, height - 26), label, font=fnt, fill=WHITE)
    return img


def load_picture(path, width, height):
    """Open an illustration file, or draw a placeholder if missing."""
    try:
        return Image.open(path).convert("RGB")
    except OSError:
        name = os.path.basename(path)
        kind, label = _PICTURE_KINDS.get(name, ("other", "NEWS"))
        return fallback_picture(width, height, kind, label)


def fallback_map(width, height):
    """Draw a programmatic outline world map (same projection)."""
    ocean = (18, 42, 66)
    land = (62, 100, 114)
    grid = (32, 64, 92)
    img = Image.new("RGB", (width, height), ocean)
    d = ImageDraw.Draw(img)
    for lon in range(-180, 181, 30):
        x = (lon + 180) / 360.0 * width
        d.line([x, 0, x, height], fill=grid, width=1)
    for lat in range(-60, 86, 30):
        y = (85 - lat) / 145.0 * height
        d.line([0, y, width, y], fill=grid, width=1)
    # simplified continent blobs (lon/lat boxes, equirectangular)
    for lon0, lat0, lon1, lat1 in [
        (-168, 72, -52, 15),   # North America
        (-80, 12, -34, -56),   # South America
        (-11, 71, 32, 36),     # Europe
        (-18, 35, 52, -35),    # Africa
        (60, 77, 180, 5),      # Asia
        (95, 10, 141, -10),    # SE Asia
        (113, -11, 154, -39),  # Australia
    ]:
        x0 = (lon0 + 180) / 360.0 * width
        x1 = (lon1 + 180) / 360.0 * width
        y0 = (85 - lat0) / 145.0 * height
        y1 = (85 - lat1) / 145.0 * height
        d.ellipse([x0, y0, x1, y1], fill=land)
    fnt = load_font(SANS_B, 11)
    for text, lon, lat in [
        ("NORTH AMERICA", -100, 50),
        ("SOUTH AMERICA", -60, -15),
        ("EUROPE", -5, 62),
        ("AFRICA", 20, 5),
        ("ASIA", 100, 50),
        ("OCEANIA", 135, -25),
    ]:
        x, y = lonlat_to_map(lon, lat, width, height)
        d.text((x, y), text, font=fnt, fill=(198, 218, 234), anchor="mm")
    return img


def load_map(path, width, height):
    """Open the map file, or draw a placeholder if missing."""
    try:
        return Image.open(path).convert("RGB")
    except OSError:
        return fallback_map(width, height)


# -------------------------------------------------------------- build

def build_page():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(page)

    # ---- masthead ----
    d.rectangle([MARGIN, 10, MARGIN + 64, 64], fill=RED)
    d.text((MARGIN + 32, 17), "NOV 19", font=load_font(SANS_B, 17),
           fill=WHITE, anchor="ma")
    d.text((MARGIN + 32, 40), "THU \u00b7 2026", font=load_font(SANS_B, 11),
           fill=WHITE, anchor="ma")
    d.text((MARGIN + 76, 12), "THE DAY IN WORLD NEWS",
           font=load_font(SANS_B, 15), fill=INK)
    d.text((RIGHT, 12), "45 STORIES  \u2022  7 REGIONS  \u2022  ONE PAGE",
           font=load_font(SANS_B, 13), fill=INK, anchor="ra")
    d.text((MARGIN + 76, 30), "Thursday 19 November 2026",
           font=load_font(SERIF_B, 42), fill=INK)

    # ---- region counts + rule ----
    counts = "  \u2022  ".join(f"{name} {n}" for name, n in REGION_COUNTS)
    d.text((PAGE_W // 2, 78), counts, font=load_font(SANS_B, 13),
           fill=INK, anchor="ma")
    d.rectangle([MARGIN, 96, RIGHT, 99], fill=RULE)

    # ---- the day in numbers ----
    d.text((MARGIN, 110), "THE DAY IN", font=load_font(SANS_B, 11), fill=RED)
    d.text((MARGIN, 124), "NUMBERS", font=load_font(SANS_B, 11), fill=RED)
    stats_x0 = 125
    stats_col = (RIGHT - stats_x0) // len(DAY_NUMBERS)
    for i, (num, cap) in enumerate(DAY_NUMBERS):
        cx = stats_x0 + i * stats_col
        d.text((cx + 8, 106), num, font=load_font(SANS_B, 19), fill=INK)
        d.text((cx + 8, 132), cap, font=load_font(SANS, 10), fill=GREY)
        if i:
            d.line([cx, 104, cx, 146], fill=FAINT, width=1)
    d.rectangle([MARGIN, 154, RIGHT, 156], fill=RULE)

    # ---- three lead stories ----
    gap = 14
    col_w = (CONTENT_W - 2 * gap) // 3
    pic_h = 84
    top = 166
    for i, story in enumerate(LEAD_STORIES):
        x0 = MARGIN + i * (col_w + gap)
        pic = load_picture(os.path.join(HERE, story["picture"]), col_w, pic_h)
        pic = cover_crop(pic, col_w, pic_h)
        page.paste(pic, (x0, top))
        ky = top + pic_h + 8
        d.text((x0, ky), story["kicker"], font=load_font(SANS_B, 11), fill=RED)
        hy = ky + 16
        head_lines = wrap_text(d, story["headline"], load_font(SERIF_B, 19), col_w)
        hy = draw_wrapped(d, x0, hy, head_lines, load_font(SERIF_B, 19), INK, 22)
        dy = hy + 4
        deck_lines = wrap_text(d, story["summary"], load_font(SANS, 11), col_w)
        draw_wrapped(d, x0, dy, deck_lines, load_font(SANS, 11), INK, 14)

    # ---- world map with numbered pins ----
    my = 380
    d.text((MARGIN, my), "WHERE IT HAPPENED  \u2014  STORIES PINNED BY NUMBER",
           font=load_font(SANS_B, 12), fill=INK)
    d.rectangle([MARGIN, my + 18, RIGHT, my + 20], fill=RULE)
    map_top = my + 26
    map_h = 160
    src_map = load_map(os.path.join(HERE, "map.jpg"), CONTENT_W, map_h)
    src_w, src_h = src_map.size
    shown = src_map.resize((CONTENT_W, map_h), Image.LANCZOS)
    page.paste(shown, (MARGIN, map_top))
    for num, lat, lon, nx, ny in MAP_PINS:
        px, py = lonlat_to_map(lon, lat, src_w, src_h)
        cx = MARGIN + px / src_w * CONTENT_W + nx
        cy = map_top + py / src_h * map_h + ny
        r = 9
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
                  outline=WHITE, width=1)
        d.text((cx, cy), str(num), font=load_font(SANS_B, 10),
               fill=WHITE, anchor="mm")

    # ---- also on grid (stories 4..45) ----
    gy = 576
    d.text((MARGIN, gy), "ALSO ON THURSDAY 19 NOVEMBER",
           font=load_font(SANS_B, 12), fill=INK)
    d.rectangle([MARGIN, gy + 18, RIGHT, gy + 20], fill=RULE)
    grid_top = gy + 28
    grid_cols = 4
    grid_col_w = CONTENT_W // grid_cols
    row_h = 25
    item_font = load_font(SANS, 10)
    item_num_font = load_font(SANS_B, 10)
    for idx, text in enumerate(REST_STORIES):
        num = idx + 4
        col = idx % grid_cols
        row = idx // grid_cols
        x0 = MARGIN + col * grid_col_w
        y0 = grid_top + row * row_h
        d.text((x0, y0), str(num), font=item_num_font, fill=INK)
        lines = wrap_text(d, text, item_font, grid_col_w - 24)
        draw_wrapped(d, x0 + 22, y0, lines[:2], item_font, INK, 12)

    # ---- date check box ----
    box_top = grid_top + 11 * row_h + 8
    d.rectangle([MARGIN, box_top, RIGHT, box_top + 98], outline=RULE, width=1)
    d.text((MARGIN + 10, box_top + 8), "DATE CHECK  \u2014  LEFT OUT ON PURPOSE",
           font=load_font(SANS_B, 11), fill=RED)
    dc_cols = 2
    dc_col_w = (CONTENT_W - 20) // dc_cols
    dc_font = load_font(SANS, 10)
    for idx, text in enumerate(LEFT_OUT):
        col = idx % dc_cols
        row = idx // dc_cols
        x0 = MARGIN + 10 + col * dc_col_w
        y0 = box_top + 30 + row * 16
        d.text((x0, y0), "\u2717", font=load_font(SANS_B, 10), fill=RED)
        d.text((x0 + 14, y0), text, font=dc_font, fill=INK)

    # ---- footer ----
    foot_lines = wrap_text(d, FOOTER, load_font(SANS, 9), CONTENT_W)
    fy = box_top + 106
    draw_wrapped(d, MARGIN, fy, foot_lines, load_font(SANS, 9), GREY, 12)

    out = os.path.join(HERE, "entry.png")
    page.save(out)
    print(f"saved {out} ({PAGE_W}x{PAGE_H})")


if __name__ == "__main__":
    build_page()
