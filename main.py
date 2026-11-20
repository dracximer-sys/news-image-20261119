"""Render the 19 November 2026 world-news front page (make.fun entry),
1024x1024 PNG. Winners' pattern: masthead + red date box, region counts,
THE DAY IN NUMBERS, 3 lead stories with original illustrations, a big world
map with numbered pins, a numbered ALSO ON grid, an explicit DATE CHECK box,
and a sources footer. 45 stories. Deterministic, no network: the three
illustrations and the world map are read from local files next to this
script (illustrations/ and map.jpg).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 247, 240)
INK = (17, 17, 17)
RED = (185, 28, 28)
GREY = (90, 90, 90)
RULE = (17, 17, 17)
LIGHT = (200, 196, 188)
BASE = os.path.dirname(os.path.abspath(__file__))
ILL = os.path.join(BASE, "illustrations")
MAP = os.path.join(BASE, "map.jpg")

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def fit_photo(path, w, h, focus_y=0.5, focus_x=0.5):
    im = Image.open(path).convert("RGB")
    iw, ih = im.size
    target = w / h
    src = iw / ih
    if src > target:
        cw = int(ih * target)
        left = int((iw - cw) * focus_x)
        im = im.crop((left, 0, left + cw, ih))
    else:
        ch = int(iw / target)
        top = int((ih - ch) * focus_y)
        im = im.crop((0, top, iw, top + ch))
    return im.resize((w, h), Image.LANCZOS)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 28
CW = W - 2 * M  # 968

# ---------- masthead ----------
d.rectangle([M, 14, W - M, 16], fill=RULE)
# red date box
d.rectangle([M, 18, M + 68, 64], fill=RED)
f_db1 = font(SANS_B, 13)
f_db2 = font(SANS_B, 8)
d.text((M + 34, 23), "NOV 19", font=f_db1, fill=(255, 255, 255), anchor="ma")
d.text((M + 34, 42), "THU · 2026", font=f_db2, fill=(255, 255, 255), anchor="ma")
f_top = font(SANS_B, 13)
d.text((M + 80, 24), "THE DAY IN WORLD NEWS", font=f_top, fill=INK)
d.text((W - M, 24), "45 STORIES  •  7 REGIONS  •  ONE PAGE", font=f_top, fill=INK, anchor="ra")
f_date = font(SERIF_B, 44)
d.text((W / 2, 42), "Thursday 19 November 2026", font=f_date, fill=INK, anchor="ma")
d.rectangle([M, 96, W - M, 98], fill=RULE)

# ---------- region counts ----------
f_reg = font(SANS_B, 11)
d.text((W / 2, 105), "EUROPE 9   •   AMERICAS 9   •   ASIA 8   •   AFRICA 6   •   MIDDLE EAST 5   •   OCEANIA 4   •   WORLD 4",
       font=f_reg, fill=INK, anchor="ma")

# ---------- THE DAY IN NUMBERS ----------
f_nl = font(SANS_B, 10)
d.text((M, 124), "THE DAY IN NUMBERS", font=f_nl, fill=RED)
numbers = [
    ("$81.3bn", "Anthropic IPO record"),
    ("51–48", "Senate Iran vote"),
    ("9–6", "ICJ genocide vote"),
    ("109–0", "Denmark Greenland"),
    ("€45bn", "EU Ukraine loan"),
    ("4.9%", "Australia jobless"),
]
f_nv = font(SANS_B, 17)
f_nt = font(SANS, 9)
cell = CW // 6
for i, (val, lab) in enumerate(numbers):
    cx = M + i * cell
    d.text((cx, 138), val, font=f_nv, fill=INK)
    d.text((cx, 158), lab, font=f_nt, fill=(60, 60, 60))
    if i < 5:
        d.line([cx + cell - 8, 138, cx + cell - 8, 172], fill=LIGHT, width=1)
d.rectangle([M, 174, W - M, 176], fill=RULE)

# ---------- top row: 3 lead stories with illustrations ----------
leads = [
    ("ASIA  —  TRILATERAL SUMMIT", "Trump, Xi & Putin hold first trilateral summit",
     "In Shenzhen on the APEC sidelines, the three leaders meet for ~80 minutes and issue a "
     "'peace declaration' denouncing nuclear war; no breakthrough on Ukraine, Iran, Taiwan or trade.",
     "summit.webp", 0.5),
    ("WORLD  —  INTERNATIONAL COURT", "ICJ: Myanmar committed genocide against Rohingya",
     "The World Court rules 9–6 that Myanmar committed genocide in the 2017 crackdown — the first "
     "time a state has been found guilty of genocide by an international court.",
     "icj.webp", 0.55),
    ("AMERICAS  —  MARKETS", "Anthropic's record $81.3bn IPO debuts on Nasdaq",
     "Shares priced at $83, opened at $111.50 (+34%) and closed ~$97 (+17%) — the largest IPO in "
     "history, valuing the firm at ~$1.5tn.",
     "ipo.webp", 0.4),
]
col_w = (CW - 2 * 16) // 3  # 312
y0 = 184
ph_h = 95
f_lk = font(SANS_B, 11)
f_lh = font(SERIF_B, 19)
f_ls = font(SANS, 11)
for i, (kick, head, summ, fname, fy) in enumerate(leads):
    cx = M + i * (col_w + 16)
    pic = fit_photo(os.path.join(ILL, fname), col_w, ph_h, focus_y=fy)
    img.paste(pic, (cx, y0))
    yy = y0 + ph_h + 6
    d.text((cx, yy), kick, font=f_lk, fill=RED)
    yy += 16
    hl = wrap(d, head, f_lh, col_w)
    yy = draw_lines(d, hl[:2], cx, yy, f_lh, INK, 22)
    sl = wrap(d, summ, f_ls, col_w)
    draw_lines(d, sl[:3], cx, yy + 2, f_ls, (40, 40, 40), 13)
    if i < 2:
        d.line([cx + col_w + 8, y0, cx + col_w + 8, y0 + 200], fill=LIGHT, width=1)
y = y0 + 208
d.rectangle([M, y, W - M, y + 2], fill=RULE)
y += 8

# ---------- world map with numbered pins ----------
f_mh = font(SANS_B, 11)
d.text((M, y), "WHERE IT HAPPENED  —  STORIES PINNED BY NUMBER", font=f_mh, fill=INK)
y += 18
map_y = y
map_h = 200
map_im = Image.open(MAP).convert("RGB")
mw, mh = map_im.size
scale = CW / mw
map_scaled = map_im.resize((CW, int(mh * scale)), Image.LANCZOS)
# crop a horizontal band (scaled coords y 86..286) to keep the map wide
band = map_scaled.crop((0, 86, CW, 86 + map_h))
d.rectangle([M, map_y, W - M, map_y + map_h], fill=(255, 255, 255))
img.paste(band, (M, map_y))

# Pins are direct band coordinates (x, y within the 968x200 cropped map),
# read off the rendered map and nudged so the crowded European cluster
# does not overlap. Pin numbers 1-3 are the lead stories above; the rest
# match the story numbers in the ALSO ON grid below (stories 4-45).
pins = [
    (1, 830, 175),   # Shenzhen summit
    (2, 492, 110),   # The Hague ICJ
    (3, 272, 102),   # New York IPO
    (4, 510, 128),   # Brussels EU loan
    (7, 458, 100),   # London
    (8, 590, 115),   # Kerch / Crimea bridge
    (13, 250, 127),  # Washington, Senate vote
    (25, 850, 120),  # Seoul
    (34, 575, 140),  # Gaza
    (36, 605, 150),  # Kuwait City
    (37, 605, 172),  # Riyadh PIF tower
]
f_pin = font(SANS_B, 8)
for num, bx, by in pins:
    px = M + bx
    py = map_y + by
    r = 9
    d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=(255, 255, 255), width=1)
    d.text((px, py - 6), str(num), font=f_pin, fill=(255, 255, 255), anchor="ma")
y = map_y + map_h + 8
d.rectangle([M, y, W - M, y + 2], fill=RULE)
y += 8

# ---------- ALSO ON: numbered grid, 4 columns x 11 rows (stories 4-45) ----------
f_ah = font(SANS_B, 13)
d.text((M, y), "ALSO ON THURSDAY 19 NOVEMBER", font=f_ah, fill=INK)
y += 20
also = [
    "EU proposes €45bn loan for Ukraine in 2027",
    "Denmark ratifies US–Greenland defence deal, 109–0",
    "Serbia elects student-backed speaker Cupic",
    "UK & Norway fund two Ukrainian naval craft",
    "Crimea bridge attacked again; traffic halted",
    "Ukrainian strikes devastate Russia's fuel supply",
    "France forces tech giants to share media revenue",
    "EU delays methane emissions law to 2029",
    "UK tribunal confirms Apple encryption order",
    "Senate rejects Iran war-powers resolution, 51–48",
    "US & Venezuela sign military cooperation deal",
    "Nvidia beats expectations; shares fall 2.9%",
    "US jobless claims unexpectedly rise",
    "Trump frustrated by Vance's Iran-war criticism",
    "Musk distances himself from Republicans",
    "Pastor convicted over Haiti president's murder",
    "Russian arrested for spying on Palantir",
    "APEC adopts Shenzhen Outlook on trade, data, AI",
    "Xi uses summit to showcase China's tech rise",
    "Russian bombers return to Vietnam",
    "Japan & India deepen military cooperation",
    "South Korea's exports pass $1tn for first time",
    "South Korea court overturns ex-PM's sentence",
    "Mongolia's president resigns over rail scandal",
    "Ethiopia & Eritrea mass troops at border",
    "Somalia expels UAE ambassador in 72 hours",
    "Sudan's army says it broke El Obeid siege",
    "Kenya faces milk shortage as drought bites",
    "South Africa holds repo rate at 7.25%",
    "UN names new MINUSCA chief for CAR",
    "Israel's rare ground operation in Gaza",
    "Gaza peace plan scores 4 out of 26",
    "Kuwait repels first Iranian attack in two months",
    "Saudi PIF tower hit by Houthi rocket debris",
    "IEA: Iran war threatens energy security",
    "Australia's unemployment jumps to 4.9%",
    "Darwin port lease dispute worsens",
    "Fiji declares national disaster over drought",
    "ASX 200 drops 91 points, erasing 2026 gains",
    "COP31: fossil fuels cut from draft deal",
    "IMF: global public debt nearing 100% of GDP",
    "A quarter of world's children live in conflict zones",
]
f_num = font(SANS_B, 9)
f_ah2 = font(SANS_B, 9)
col_a = (CW - 3 * 14) // 4  # 231
row_h = 21
for idx, head in enumerate(also):
    num = idx + 4
    cx = M + (idx % 4) * (col_a + 14)
    cy = y + (idx // 4) * row_h
    d.text((cx, cy), str(num), font=f_num, fill=RED)
    tx = cx + 20
    tw = col_a - 20
    hl = wrap(d, head, f_ah2, tw)
    draw_lines(d, hl[:2], tx, cy, f_ah2, INK, 10)
y = y + 11 * row_h + 4
d.rectangle([M, y, W - M, y + 2], fill=RULE)
y += 8

# ---------- DATE CHECK box ----------
f_dc = font(SANS_B, 10)
f_dci = font(SANS, 9)
box_y = y
d.rectangle([M, box_y, W - M, box_y + 92], outline=RULE, width=1)
d.text((M + 10, box_y + 6), "DATE CHECK  —  LEFT OUT ON PURPOSE", font=f_dc, fill=RED)
dc = [
    "Van Gogh $190.4m sale — auctioned Wed 18 Nov evening, not Thu 19",
    "Xi greets Trump at Shenzhen airport — that welcome was Wed 18 Nov",
    "Jeffries named House Speaker (251–11) — the vote was 18 Nov, not 19 Nov",
    "Iran strikes on Kuwait & Bahrain began Wed 18 Nov — 'repels' was 19 Nov",
    "Anthropic's $83 IPO price set — evening of 18 Nov; the debut was 19 Nov",
    "Cyclone Akvan landfall — 20 Nov, not 19 Nov",
    "Trump pardons Pete Rose posthumously — 20 Nov, not 19 Nov",
    "UK pledges 1,000+ drones for Ukraine — announced 20 Nov, not 19 Nov",
]
for i, item in enumerate(dc):
    cx = M + 10 + (i % 2) * ((CW - 20) // 2)
    cy = box_y + 26 + (i // 2) * 16
    d.text((cx, cy), "✕", font=f_dci, fill=RED)
    d.text((cx + 12, cy), item, font=f_dci, fill=(40, 40, 40))
y = box_y + 92 + 6

# ---------- footer ----------
f_ft = font(SANS, 8)
foot = ("Every story happened on, or was first reported on, Thursday 19 November 2026. "
        "Sources: Le Monde, Reuters, NY Post, The Times, Horizon, Morningstar, AppiSToS, "
        "Al Jazeera, BBC, SCMP, ABC Australia, APO Group/UN. Original drawings.")
fl = wrap(d, foot, f_ft, CW)
draw_lines(d, fl, M, y, f_ft, GREY, 10)
y = y + len(fl) * 10

out = os.path.join(BASE, "entry.png")
img.save(out, format="PNG", optimize=True)
print("saved", out, "final y =", y)
if os.path.isdir("/output"):
    img.save("/output/entry.png", format="PNG", optimize=True)
    print("saved /output/entry.png")
