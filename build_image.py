#!/usr/bin/env python3
"""Build the 27 Nov 2026 world-news front page, 1024x1024 PNG.

Own layout: deep-navy broadsheet with amber and red accents. Masthead,
one dominant lead story beside a drawn globe panel, a four-cell stat band,
two-column lower stories with category tags, and a bottom ticker strip.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (11, 22, 38)
PANEL = (18, 34, 56)
AMBER = (242, 169, 59)
RED = (214, 69, 69)
WHITE = (245, 240, 228)
MUTED = (178, 190, 205)
LINE = (64, 84, 112)
TEAL = (86, 178, 168)

FDIR = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(FDIR + name, size)

B = lambda s: font("DejaVuSans-Bold.ttf", s)
R = lambda s: font("DejaVuSans.ttf", s)
SB = lambda s: font("DejaVuSerif-Bold.ttf", s)

img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)


def wrap(text, fnt, width):
    return textwrap.wrap(text, width=width, break_long_words=False)


def block(x, y, lines, fnt, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def tag(x, y, label, color):
    w = d.textlength(label, font=B(17)) + 18
    d.rounded_rectangle([x, y, x + w, y + 26], radius=3, fill=color)
    d.text((x + 9, y + 4), label, font=B(17), fill=NAVY)
    return w


# ---- masthead -------------------------------------------------------------
d.text((28, 22), "THE WORLD IN ONE DAY", font=SB(52), fill=WHITE)
d.rectangle([28, 92, 996, 96], fill=AMBER)
d.text((28, 106), "FRIDAY, 27 NOVEMBER 2026", font=B(20), fill=AMBER)
d.text((700, 106), "THE DAY IN ONE PAGE", font=R(18), fill=MUTED)

# ---- lead story -----------------------------------------------------------
ly = 150
tag(28, ly, "LEAD STORY — UKRAINE", RED)
ly += 44
headline = ["TRUMP: PUTIN", "\u201cWOULD LIKE", "TO MAKE A DEAL\u201d"]
y = ly
for ln in headline:
    d.text((28, y), ln, font=SB(48), fill=WHITE)
    y += 56
y += 4
deck = wrap("Zelenskyy warns of a major Russian attack as Trump urges "
            "Putin to \u201cpull back\u201d — and says the US is too focused "
            "on the Middle East.", R(20), 44)
y = block(28, y, deck, R(20), MUTED, 26)
y += 14
d.line([28, y, 600, y], fill=LINE, width=1)
y += 14
d.text((28, y), "\u201cVICTORY AT HAND\u201d — TRUMP ON THE IRAN WAR",
       font=B(20), fill=AMBER)
y += 30
# (Iran deck dropped: the stat band starts at y=492, no room below)

# ---- drawn globe panel (right of lead) ------------------------------------
px, py, pw, ph = 640, 150, 356, 316
d.rounded_rectangle([px, py, px + pw, py + ph], radius=8, fill=PANEL)
d.rectangle([px, py, px + pw, py + 4], fill=AMBER)
cx, cy, r = px + 178, py + 150, 105
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=AMBER, width=3)
for k in range(-2, 3):
    off = k * 42
    d.arc([cx - r, cy - r + abs(off), cx + r, cy + r - abs(off)],
          start=90 if k >= 0 else 270, end=270 if k >= 0 else 90,
          fill=TEAL, width=2)
for k in range(-2, 3):
    d.arc([cx - r + abs(k * 42), cy - r, cx + r - abs(k * 42), cy + r],
          start=0, end=360, fill=TEAL, width=2)
d.line([cx - r, cy, cx + r, cy], fill=TEAL, width=2)
# dashed red arc: the deal line
for i in range(0, 90, 10):
    a0 = 200 + i
    d.arc([cx - r - 18, cy - r - 18, cx + r + 18, cy + r + 18],
          start=a0, end=a0 + 5, fill=RED, width=4)
d.text((px + 20, py + 268), "A DEAL, OR A NEW ATTACK?", font=B(19), fill=WHITE)
d.text((px + 20, py + 292), "Kyiv braces as talks stall.", font=R(16), fill=MUTED)

# ---- stat band ------------------------------------------------------------
sy = 498
stats = [("724,000", "US HOMES DARK"),
         ("7,000 t", "DIESEL OFF IBIZA"),
         ("31", "KILLED IN CAIRO"),
         ("24", "STATES BACK LOAN")]
cw = (996 - 28) // 4
d.rectangle([28, sy, 996, sy + 96], fill=PANEL)
for i, (num, lab) in enumerate(stats):
    x = 28 + i * cw
    if i:
        d.line([x, sy + 12, x, sy + 84], fill=LINE, width=1)
    nw = d.textlength(num, font=SB(40))
    d.text((x + (cw - nw) / 2, sy + 12), num, font=SB(40), fill=AMBER)
    lw = d.textlength(lab, font=B(15))
    d.text((x + (cw - lw) / 2, sy + 62), lab, font=B(15), fill=MUTED)

# ---- lower stories, two columns ------------------------------------------
stories = [
    ("STORM", RED, "Thanksgiving storm batters eastern US",
     "Flooding, flight delays and shut bridges; over 724,000 without power."),
    ("CYBER", AMBER, "AFP hit by cyberattack",
     "The global news agency shuts its content platform after the breach."),
    ("SPACE", TEAL, "US clears SpaceX for 1m satellites",
     "Orbital data-centre constellation approved — a million birds aloft."),
    ("EUROPE", RED, "EU split over $49bn Ukraine loan",
     "Leaders struggle to agree the long-term budget as 24 states back Kyiv."),
    ("ASIA", AMBER, "Kim vows more nuclear weapons",
     "North Korea expels a Swiss diplomat in a sanctions row."),
    ("VOTE", TEAL, "New Zealand count: Labour 29.9%",
     "National leads on 40 seats as the official tally lands."),
]
col_x = [28, 520]
col_w = 476
y0 = 620
for idx, (cname, color, head, deck) in enumerate(stories):
    col = idx % 2
    row = idx // 2
    x = col_x[col]
    y = y0 + row * 104
    tag(x, y, cname, color)
    d.text((x, y + 34), head, font=B(19), fill=WHITE)
    dl = wrap(deck, R(17), 42)
    block(x, y + 62, dl[:2], R(17), MUTED, 21)

# ---- ticker ----------------------------------------------------------------
ty = 940
d.rectangle([0, ty, W, H], fill=RED)
tick = ("ALSO TODAY  •  Andy Taylor dies at 65  •  "
        "Sinner out of Aus Open 2027  •  Mount Mayon erupts")
d.text((28, ty + 32), tick, font=B(18), fill=WHITE)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
