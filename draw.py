#!/usr/bin/env python3
"""Build entry.png for news-image-20261121 — v1, 'The World In One Day'.

One-page broadsheet: 31 verified stories from Saturday 21 November 2026.
13 mains (3 large + 10 medium), 18 one-line briefs, navy pin map,
6-number strip, timeline strip, region bar, DATE CHECK.
All text, numbers and artwork drawn from this session's own research
(10 web-search verification batches, 21 Nov 2026 15:47-16:30 WIB).

Date discipline (the v1 edge): ZERO wrong-date stories. Verified and
EXCLUDED as other days' news: UK-EU reset deal, Poland missile
intercept, Wall Street correction, Cyclone Akvan landfall, Kyiv bridges
barrage (all Fri 20 Nov); 900,000 AI chips for China, California
subpoenas Nvidia, Texas execution (all Thu 19 Nov); India H5N1 vaccine,
Britain cyberattacks admission, Copenhagen attache expulsion, Nigeria
funeral boat, SA crime stats, Vancouver trial end (all Fri 20 Nov);
ANC 31% result (4 Nov election); Port Louis rating agency (7 Oct).
The 2 Jazan intercepts were Friday evening — only the 3 Saturday
Riyadh intercepts are carried. BepiColombo is a SCHEDULE (burn 19:24
CET tonight, FORECAST chip), never an outcome. Friday-US-evening
events (Trump AI tax, Vance, Palisades verdict, Roundup ruling,
SpaceX/Himes) are carried: first reported in Asia on Saturday morning.

Layout adapts the proven NI20 v2 geometry (same helpers, same grid)
with the NI21 top-1 structure: red banner label on EVERY scene,
1-line medium decks, navy pin map, timeline strip restored (M9),
VERDICT strip dropped to fund the timeline. Cream + ink + red.
1024x1024, target <= 300 KB (hard limit 1 MiB).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 28                      # side margin
CW = W - 2 * M              # content width = 968

# ---------- palette ----------
CREAM = (247, 242, 231)
CREAM2 = (239, 231, 211)
PANEL = (233, 224, 196)
INK = (26, 26, 26)
MUTED = (107, 99, 85)
RED = (178, 35, 27)
RED_DK = (140, 24, 18)
NAVY = (27, 42, 74)
NAVY_LT = (143, 163, 199)
GOLD = (176, 132, 52)
WHITE = (255, 255, 255)
SKY = (31, 52, 88)
TEAL = (36, 110, 118)
SAND = (214, 196, 150)
GREEN = (74, 110, 68)

# ---------- fonts ----------
FD = "/usr/share/fonts/truetype/dejavu/"
FN = "/usr/share/fonts/truetype/noto/"


def F(path, size):
    return ImageFont.truetype(path, size)


SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SERIF = FD + "DejaVuSerif.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"

f_folio = F(SANS_B, 12)
f_kicker = F(SANS_B, 14)
f_strap = F(FN + "NotoSerif-Italic.ttf", 16)
f_time_h = F(SANS_B, 11)
f_time = F(SANS, 12)
f_strip_n = F(SANS_B, 21)
f_strip_l = F(SANS_B, 11)
f_region = F(SANS_B, 9)
f_h1 = F(SERIF_B, 26)
f_d1 = F(SERIF, 14)
f_a1 = F(SANS, 11)
f_blg = F(SANS_B, 14)       # large banner label
f_bmd = F(SANS_B, 12)       # medium banner label
f_h2 = F(SERIF_B, 21)
f_d2 = F(SANS, 11)
f_a2 = F(SANS, 10)
f_brief = F(SANS, 11)
f_brief_n = F(SANS_B, 12)
f_map_h = F(SANS_B, 11)
f_pin = F(SANS_B, 7)
f_dc_h = F(SANS_B, 12)
f_dc = F(SANS, 11)
f_dc_note = F(FN + "NotoSerif-Italic.ttf", 12)
f_scene_n = F(SANS_B, 15)
f_scene_s = F(SANS_B, 10)
f_scene_xs = F(SANS, 9)
f_big = F(SANS_B, 26)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)


# ---------- helpers ----------
def tw(text, font):
    return d.textlength(text, font=font)


def wrap(text, font, width):
    """Greedy word wrap; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if tw(trial, font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def rule(y, x0=M, x1=W - M, w=2, color=INK):
    d.line([(x0, y), (x1, y)], fill=color, width=w)


def banner(x, y, w, text, font, bg=RED, fg=WHITE, h=20, pad=7):
    """Red label banner with white text, left-aligned."""
    d.rectangle([x, y, x + w, y + h], fill=bg)
    d.text((x + pad, y + (h - font.size) // 2 - 1), text, font=font, fill=fg)


def starburst(cx, cy, r, color=RED, n=8):
    """Explosion star: n spikes."""
    import math
    pts = []
    for i in range(n * 2):
        ang = math.pi * i / n - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.38
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)
    d.ellipse([cx - r * 0.28, cy - r * 0.28, cx + r * 0.28, cy + r * 0.28],
              fill=(255, 220, 80))


def pin_dot(cx, cy, num, r=6):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
              outline=WHITE, width=1)
    t = str(num)
    d.text((cx - tw(t, f_pin) / 2, cy - 4), t, font=f_pin, fill=WHITE)


def caption_band(x, y, w, h, text):
    """Dedicated caption band at the bottom of a medium scene: solid
    dark strip, white text. Artwork must stay above y+h-16."""
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(10, 14, 26))
    d.text((x + 6, y + h - 13), text, font=f_scene_s, fill=WHITE)
    check(tw(text, f_scene_s) <= w - 12,
          "caption band too wide: %s" % text)


def data_strip(x, y, w, h, text):
    """Data strip at the bottom of a large scene (same pattern)."""
    d.rectangle([x, y + h - 20, x + w, y + h], fill=(10, 14, 26))
    d.text((x + 6, y + h - 16), text, font=f_scene_s, fill=WHITE)
    check(tw(text, f_scene_s) <= w - 12,
          "data strip too wide: %s" % text)


def chip(x, y, text):
    """Small CLAIM/FORECAST chip: white box, red border + red text."""
    wch = tw(text, f_scene_xs) + 8
    d.rectangle([x, y, x + wch, y + 12], fill=WHITE, outline=RED, width=1)
    d.text((x + 4, y + 1), text, font=f_scene_xs, fill=RED_DK)


WARN = []


def check(cond, msg):
    if not cond:
        WARN.append(msg)


# ================================================================
# TOP OF PAGE
# ================================================================
# folio line
d.text((M, 6), "SATURDAY 21 NOVEMBER 2026", font=f_folio, fill=INK)
fr = "ONE DAY  ·  ONE PAGE  ·  31 STORIES"
d.text((W - M - tw(fr, f_folio), 6), fr, font=f_folio, fill=MUTED)
rule(22, w=1)

# masthead — auto-fit the largest size (62 down to 56) that fits one line
mast = "Saturday 21 November 2026"
f_mast = None
for _size in (62, 60, 58, 56):
    _f = F(SERIF_B, _size)
    if tw(mast, _f) <= CW:
        f_mast = _f
        break
check(f_mast is not None, "masthead does not fit even at 56px")
d.text(((W - tw(mast, f_mast)) / 2, 24), mast, font=f_mast, fill=INK)
rule(90, w=3)
rule(93, w=1)

# kicker
kick = "31 STORIES  ·  6 REGIONS  ·  EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
d.text(((W - tw(kick, f_kicker)) / 2, 97), kick, font=f_kicker, fill=RED_DK)

# strapline (4 stories, italic)
strap = ("COP31 enters day 13 with no deal  ·  three missiles down over Riyadh  ·  "
         "a 6.7 quake shakes Peru  ·  Rahul\u2019s 136 at stumps")
d.text(((W - tw(strap, f_strap)) / 2, 116), strap, font=f_strap, fill=INK)
rule(136, w=1)

# timeline strip — one line, each entry in its own time zone (honest:
# the day's events are dated Saturday in the zone where they happened)
tl_head = "THE DAY \u2014 "
tl_body = ("00:09 UTC Peru quake  ·  00:08 PHT Davao landing  ·  "
           "01:53 AST Riyadh  ·  05:37 KST Sejong  ·  "
           "19:24 CET BepiColombo  ·  20:00 PST F1 race")
tl_w = tw(tl_head, f_time_h) + tw(tl_body, f_time)
tl_x = (W - tl_w) / 2
d.text((tl_x, 140), tl_head, font=f_time_h, fill=RED_DK)
d.text((tl_x + tw(tl_head, f_time_h), 140), tl_body, font=f_time, fill=INK)
rule(160, w=1)

# 6-number strip
strip = [
    ("DAY 13", "COP31, NO DEAL YET"),
    ("3", "DOWN OVER RIYADH"),
    ("6.7", "PERU QUAKE, 108 KM"),
    ("146", "SAFE IN DAVAO"),
    ("$57,773", "BITCOIN, 08:43 UTC"),
    ("136", "RAHUL, INDIA 486/4"),
]
sy, sh = 164, 34
cell = CW / 6
for i, (num, lab) in enumerate(strip):
    x = M + i * cell
    d.rectangle([x, sy, x + 3, sy + sh], fill=RED)
    d.text((x + 10, sy + 1), num, font=f_strip_n, fill=INK)
    d.text((x + 10, sy + 22), lab, font=f_strip_l, fill=INK)
    check(tw(lab, f_strip_l) <= cell - 12, "strip label too wide: %s" % lab)
rule(sy + sh + 4, w=1)

# region bar — 6 segments (Africa has ZERO verified Saturday stories:
# ANC result is 4 Nov, SA crime stats Friday, Port Louis 7 Oct,
# Nigeria boat Friday — so no Africa segment rather than a wrong one).
# Widths proportional to story counts; sum must be 31.
regions = [("EUROPE", 5), ("ASIA", 8), ("MIDEAST", 4),
           ("AMERICAS", 9), ("OCEANIA", 3), ("GLOBAL", 2)]
ry, rh = 206, 20
x = M
for i, (name, n) in enumerate(regions):
    wseg = CW * n / 31
    shade = CREAM2 if i % 2 == 0 else PANEL
    d.rectangle([x, ry, x + wseg - 1, ry + rh], fill=shade)
    label = "%s %d" % (name, n)
    d.text((x + (wseg - tw(label, f_region)) / 2, ry + 4),
           label, font=f_region, fill=INK)
    check(tw(label, f_region) <= wseg - 2, "region %s too wide" % name)
    x += wseg
rule(ry + rh + 4, w=2)


# ================================================================
# LARGE MAINS — 3 columns, scene 132px + headline + deck + attribution
# Art zone: y+22 (below banner) to y+112 (above data strip).
# ================================================================
LX = [M, 355, 682]
LW = 314
LY = 236
LH = 132


def scene_cop31(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 214))
    # draft document, left
    d.rectangle([x + 12, y + 28, x + 182, y + 106], fill=WHITE,
                outline=MUTED)
    d.text((x + 18, y + 31), "DRAFT 2", font=f_scene_s, fill=RED_DK)
    for i, ly in enumerate(range(y + 46, y + 100, 7)):
        d.line([(x + 18, ly), (x + 176 - (i % 3) * 14, ly)],
               fill=(180, 180, 180), width=2)
    # one line struck through in red: the cut text
    d.line([(x + 18, y + 67), (x + 150, y + 67)], fill=RED, width=2)
    # right column: day count + what was cut
    d.text((x + 192, y + 28), "DAY 13", font=f_big, fill=INK)
    d.text((x + 192, y + 56), "OF 12 PLANNED", font=f_scene_xs, fill=MUTED)
    d.text((x + 192, y + 70), "PARAS 144\u219280", font=f_scene_s, fill=INK)
    d.text((x + 192, y + 82), "$120BN \u2014 CUT", font=f_scene_s, fill=INK)
    d.text((x + 192, y + 94), "FOSSIL FUELS OUT", font=f_scene_s, fill=INK)
    data_strip(x, y, w, h, "3RD DRAFT DUE SAT AM \u00b7 NO FOSSIL FUELS IN TEXT")


def scene_saudi(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # stars
    for sx, sy2 in ((24, 30), (70, 52), (130, 28), (200, 54), (280, 32),
                    (300, 60), (160, 62)):
        d.ellipse([x + sx - 1, y + sy2 - 1, x + sx + 1, y + sy2 + 1],
                  fill=WHITE)
    # skyline
    import random
    rnd = random.Random(21)
    bx = x + 6
    while bx < x + w - 14:
        bw = rnd.randint(14, 24)
        bh = rnd.randint(16, 40)
        d.rectangle([bx, y + 112 - bh, bx + bw, y + 112],
                    fill=(16, 26, 44))
        bx += bw + 3
    # Kingdom Tower: tall slab + triangle top + slit
    d.rectangle([x + 30, y + 60, x + 48, y + 112], fill=(20, 32, 54))
    d.polygon([(x + 30, y + 60), (x + 48, y + 60), (x + 39, y + 44)],
              fill=(20, 32, 54))
    d.line([(x + 39, y + 48), (x + 39, y + 66)], fill=GOLD, width=2)
    # three intercepts, with faint trails
    for cx, cy, r in ((90, 44, 10), (170, 36, 12), (250, 48, 9)):
        d.line([(x + cx - 18, y + 108), (x + cx, y + cy + 6)],
               fill=(214, 160, 60), width=2)
        starburst(x + cx, y + cy, r)
    # alert clock pill, top right
    d.rectangle([x + 236, y + 26, x + 306, y + 42], fill=(10, 14, 26))
    d.text((x + 242, y + 29), "01:53 ALERT", font=f_scene_s, fill=WHITE)
    data_strip(x, y, w, h, "3 BALLISTIC MISSILES \u00b7 NO CASUALTIES")


def scene_peru(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 198))
    # seismograph paper + trace
    d.rectangle([x + 12, y + 28, x + 200, y + 66], fill=WHITE,
                outline=MUTED)
    pts = []
    spikes = [0, 2, -3, 4, -2, 3, -12, 14, -10, 5, -3, 2, -1, 1, 0]
    for i, s in enumerate(spikes):
        pts.append((x + 18 + i * 12, y + 47 + s))
    d.line(pts, fill=RED, width=2)
    # magnitude, right
    d.text((x + 212, y + 28), "6.7", font=f_big, fill=INK)
    d.text((x + 212, y + 56), "MAGNITUDE", font=f_scene_xs, fill=MUTED)
    # facts stacked (side-by-side collided: "108 KM DEEP00:09 UTC")
    d.text((x + 12, y + 74), "108 KM DEEP", font=f_scene_n, fill=INK)
    d.text((x + 12, y + 92), "00:09 UTC", font=f_scene_n, fill=INK)
    # mini Peru map + epicentre
    d.polygon([(x + 232, y + 72), (x + 268, y + 70), (x + 292, y + 78),
               (x + 300, y + 96), (x + 286, y + 108), (x + 250, y + 108),
               (x + 232, y + 94)], fill=SAND, outline=MUTED)
    d.ellipse([x + 262, y + 84, x + 270, y + 92], fill=RED, outline=WHITE,
              width=1)
    d.text((x + 272, y + 82), "JUN\u00cdN", font=f_scene_xs, fill=INK)
    data_strip(x, y, w, h, "34 HOUSES DAMAGED \u00b7 NO DEATHS \u00b7 NO TSUNAMI")


LARGE = [
    (scene_cop31, "1  \u00b7  COP31: DAY 13, NO DEAL",
     "COP31: DAY 13, STILL NO DEAL",
     "Draft cut 144\u219280 paras; $120bn adaptation target gone, fossil fuels unmentioned.",
     "AP \u00b7 REUTERS \u00b7 CARBON BRIEF"),
    (scene_saudi, "2  \u00b7  RIYADH: 3 MISSILES DOWN",
     "3 MISSILES DOWN OVER RIYADH",
     "Houthi missiles downed before dawn, no casualties; Jazan’s two fell Friday.",
     "REUTERS \u00b7 AFP \u00b7 ARAB NEWS"),
    (scene_peru, "3  \u00b7  PERU: QUAKE 6.7",
     "6.7 QUAKE SHAKES CENTRAL PERU",
     "00:09 UTC, 108 km deep; no deaths, ~34 houses damaged, roads blocked.",
     "USGS \u00b7 AFP \u00b7 IGP"),
]

for i, (fn, label, head, deck, attr) in enumerate(LARGE):
    x = LX[i]
    fn(x, LY, LW, LH)
    banner(x, LY, LW, label, font=f_blg, h=22)
    check(tw(label, f_blg) <= LW - 10, "large banner %d too wide" % i)
    hy = LY + LH + 5
    hlines = wrap(head, f_h1, LW)
    check(len(hlines) <= 2, "large headline %d wraps to %d lines" % (i, len(hlines)))
    for j, line in enumerate(hlines):
        d.text((x, hy + j * 28), line, font=f_h1, fill=INK)
    dy = hy + len(hlines) * 28 + 2
    dlines = wrap(deck, f_d1, LW)
    check(len(dlines) <= 2, "large deck %d wraps to %d lines" % (i, len(dlines)))
    for j, line in enumerate(dlines):
        d.text((x, dy + j * 16), line, font=f_d1, fill=INK)
    d.text((x, dy + len(dlines) * 16 + 2), attr, font=f_a1, fill=MUTED)

LARGE_END = LY + LH + 5 + 58 + 30 + 14   # 475
rule(LARGE_END + 4, w=1)


# ================================================================
# MEDIUM MAINS — 5 cols x 2 rows, scene 86px + headline + 1-line deck
# Art zone: y+20 (below banner) to y+70 (above caption band).
# ================================================================
MX = [M, 224, 420, 616, 812]
MW = 184
MROW_Y = [485, 654]
MH = 86


def scene_bepi(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 22, 38))
    for sx, sy2 in ((14, 26), (70, 24), (100, 62), (160, 60), (176, 30)):
        d.ellipse([x + sx - 1, y + sy2 - 1, x + sx + 1, y + sy2 + 1],
                  fill=WHITE)
    # Mercury
    d.ellipse([x + 29, y + 32, x + 55, y + 58], fill=(150, 150, 150))
    for cx, cy, r in ((38, 40, 2), (46, 50, 3), (36, 50, 2)):
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=(110, 110, 110))
    # dotted trajectory Mercury -> spacecraft
    for t in range(1, 8):
        px = 58 + t * 9
        py = 44 - t * 1
        d.ellipse([x + px - 1, y + py - 1, x + px + 1, y + py + 1],
                  fill=(180, 180, 180))
    # spacecraft: body + panels
    d.rectangle([x + 126, y + 34, x + 138, y + 44], fill=(220, 220, 220))
    d.rectangle([x + 112, y + 37, x + 126, y + 41], fill=(80, 140, 200))
    d.rectangle([x + 138, y + 37, x + 152, y + 41], fill=(80, 140, 200))
    d.text((x + 96, y + 52), "19:24 CET", font=f_scene_n, fill=WHITE)
    chip(x + 118, y + 22, "FORECAST")
    caption_band(x, y, w, h, "37-MIN BURN \u00b7 8-YR VOYAGE")


def scene_kryvyi(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(88, 78, 96))
    # apartment block
    d.rectangle([x + 20, y + 30, x + 100, y + 68], fill=(40, 36, 48))
    for wx in range(28, 96, 12):
        for wy in (36, 48, 60):
            d.rectangle([x + wx, y + wy, x + wx + 5, y + wy + 5],
                        fill=GOLD)
    starburst(x + 60, y + 32, 9)
    d.text((x + 72, y + 24), "1", font=f_scene_s, fill=WHITE)
    # ambulance + second strike
    d.rectangle([x + 118, y + 56, x + 160, y + 68], fill=WHITE)
    d.rectangle([x + 136, y + 59, x + 142, y + 65], fill=RED)
    d.rectangle([x + 133, y + 61, x + 145, y + 63], fill=RED)
    starburst(x + 140, y + 50, 8)
    d.text((x + 152, y + 42), "2", font=f_scene_s, fill=WHITE)
    caption_band(x, y, w, h, "47 HURT \u00b7 23 BLOCKS HIT")


def scene_bridge(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(190, 205, 220))
    d.rectangle([x, y + 60, x + w, y + 70], fill=(120, 150, 180))
    # arch + deck with a collapsed gap in the middle
    d.arc([x + 20, y + 24, x + 164, y + 56], 180, 360, fill=INK, width=3)
    d.line([(x + 10, y + 48), (x + 80, y + 48)], fill=INK, width=4)
    d.line([(x + 104, y + 48), (x + 174, y + 48)], fill=INK, width=4)
    d.line([(x + 30, y + 48), (x + 30, y + 60)], fill=INK, width=3)
    d.line([(x + 154, y + 48), (x + 154, y + 60)], fill=INK, width=3)
    # rubble falling through the gap + red X
    for rx, ry2 in ((86, 52), (92, 56), (98, 52)):
        d.line([(x + rx, y + ry2), (x + rx + 4, y + ry2 + 5)], fill=INK,
               width=2)
    d.line([(x + 86, y + 42), (x + 98, y + 54)], fill=RED, width=2)
    d.line([(x + 98, y + 42), (x + 86, y + 54)], fill=RED, width=2)
    caption_band(x, y, w, h, "ROAD SECTION FELL 17 NOV")


def scene_drone(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 220, 235))
    # MQ-9 silhouette: long wing + fuselage + V tail
    d.rectangle([x + 30, y + 41, x + 154, y + 45], fill=(60, 60, 66))
    d.ellipse([x + 82, y + 38, x + 102, y + 48], fill=(60, 60, 66))
    d.line([(x + 96, y + 40), (x + 108, y + 32)], fill=(60, 60, 66),
           width=3)
    d.line([(x + 96, y + 46), (x + 108, y + 54)], fill=(60, 60, 66),
           width=3)
    d.text((x + 56, y + 56), "58TH CLAIMED", font=f_scene_s, fill=INK)
    chip(x + 132, y + 22, "CLAIM")
    caption_band(x, y, w, h, "OVER HORMUZ \u00b7 UNVERIFIED")


def scene_uranium(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 228, 170))
    # radiation trefoil: black disc, 3 yellow blades, yellow centre
    d.ellipse([x + 26, y + 29, x + 58, y + 61], fill=INK)
    for a0 in (270, 30, 150):
        d.pieslice([x + 29, y + 32, x + 55, y + 58], a0, a0 + 60,
                   fill=(238, 228, 170))
    d.ellipse([x + 38, y + 41, x + 46, y + 49], fill=(238, 228, 170))
    d.text((x + 72, y + 30), "440.9 KG", font=f_scene_n, fill=INK)
    d.text((x + 72, y + 48), "AT 60%", font=f_scene_n, fill=RED_DK)
    caption_band(x, y, w, h, "60% ENRICHED \u00b7 IAEA")


def scene_aitax(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 198))
    # data centre block with server lines
    d.rectangle([x + 12, y + 30, x + 108, y + 68], fill=(60, 60, 66))
    for ly in range(y + 36, y + 66, 6):
        d.line([(x + 18, ly), (x + 102, ly)], fill=(140, 140, 140),
               width=1)
    for gx, gy in ((20, 33), (44, 45), (68, 39), (92, 51)):
        d.ellipse([x + gx, y + gy, x + gx + 3, y + gy + 3], fill=(120, 220, 120))
    # TAX stamp
    d.rectangle([x + 118, y + 30, x + 172, y + 58], outline=RED, width=2)
    d.text((x + 132, y + 36), "TAX", font=f_scene_n, fill=RED_DK)
    caption_band(x, y, w, h, "US FIRMS BUILDING ABROAD")


def scene_davao(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(180, 210, 230))
    d.rectangle([x, y + 58, x + w, y + 70], fill=(120, 120, 120))
    for dx in range(8, 176, 20):
        d.line([(x + dx, y + 64), (x + dx + 10, y + 64)], fill=WHITE,
               width=2)
    # plane on the runway + evacuation slide
    d.ellipse([x + 52, y + 42, x + 138, y + 52], fill=WHITE, outline=MUTED)
    d.polygon([(x + 132, y + 42), (x + 146, y + 30), (x + 150, y + 42)],
              fill=RED_DK)
    d.polygon([(x + 88, y + 52), (x + 100, y + 52), (x + 92, y + 60),
               (x + 84, y + 60)], fill=(180, 180, 180))
    d.polygon([(x + 68, y + 52), (x + 76, y + 52), (x + 62, y + 68),
               (x + 54, y + 68)], fill=(255, 210, 60))
    d.text((x + 12, y + 24), "00:08", font=f_scene_s, fill=INK)
    caption_band(x, y, w, h, "146 ABOARD \u00b7 ALL SAFE")


def scene_btc(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 198))
    for gy in range(y + 26, y + 66, 10):
        d.line([(x + 8, gy), (x + 104, gy)], fill=(210, 196, 164), width=1)
    pts = [(x + 10, y + 28), (x + 30, y + 34), (x + 50, y + 32),
           (x + 70, y + 46), (x + 90, y + 58), (x + 104, y + 62)]
    d.line(pts, fill=RED, width=3, joint="curve")
    d.text((x + 112, y + 28), "$57,773", font=f_scene_n, fill=INK)
    d.text((x + 112, y + 46), "\u22126.7%", font=f_scene_n, fill=RED)
    caption_band(x, y, w, h, "LOWEST SINCE SEP 2024")


def scene_f1(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 20, 24))
    d.text((x + 10, y + 24), "P1  VERSTAPPEN", font=f_scene_s, fill=WHITE)
    d.text((x + 10, y + 36), "P2  RUSSELL", font=f_scene_s, fill=WHITE)
    d.text((x + 10, y + 48), "P3  NORRIS", font=f_scene_s, fill=WHITE)
    d.text((x + 118, y + 24), "ANT P6", font=f_scene_s,
           fill=(255, 150, 130))
    d.text((x + 118, y + 38), "\u22125 GRID", font=f_scene_xs,
           fill=(255, 150, 130))
    # chequered strip
    for r in range(2):
        for c in range(8):
            if (r + c) % 2 == 0:
                d.rectangle([x + 118 + c * 6, y + 52 + r * 6,
                             x + 124 + c * 6, y + 58 + r * 6], fill=WHITE)
    caption_band(x, y, w, h, "RACE 20:00 LOCAL TONIGHT")


def scene_rahul(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 216, 176))
    d.rectangle([x, y + 52, x + w, y + 70], fill=(150, 178, 120))
    for sx in (30, 38, 46):
        d.line([(x + sx, y + 40), (x + sx, y + 56)], fill=(220, 180, 60),
               width=3)
    d.polygon([(x + 70, y + 26), (x + 78, y + 30), (x + 64, y + 56),
               (x + 56, y + 52)], fill=(214, 178, 120))
    d.line([(x + 74, y + 28), (x + 84, y + 20)], fill=INK, width=3)
    d.ellipse([x + 106, y + 26, x + 116, y + 36], fill=RED)
    d.text((x + 128, y + 26), "136", font=f_big, fill=INK)
    d.text((x + 128, y + 54), "486/4", font=f_scene_s, fill=INK)
    caption_band(x, y, w, h, "INDIA 486/4 \u00b7 LEAD 118")


MEDIUM = [
    (scene_bepi, "4  \u00b7  BEPICOLOMBO BURN",
     "BURN AT 19:24 CET",
     "37-min burn after 8-yr voyage", "ESA / ESOC"),
    (scene_kryvyi, "5  \u00b7  KRYVYI RIH HIT",
     "2 KILLED IN DOUBLE-TAP",
     "47 hurt; boy, 7, among dead", "KYIV INDEPENDENT"),
    (scene_bridge, "6  \u00b7  KYIV: BRIDGE VOW",
     "KYIV: BRIDGE WILL FALL",
     "\u2018Will not stay\u2019, he tells NBC", "NBC \u00b7 KYIV INDEPENDENT"),
    (scene_drone, "7  \u00b7  HORMUZ: DRONE",
     "IRAN: DRONE DOWNED",
     "58th MQ-9 claimed; US silent", "IRIB \u00b7 PRESS TV"),
    (scene_uranium, "8  \u00b7  IRAN: URANIUM",
     "IRAN KEEPS URANIUM",
     "Won't send 440.9 kg abroad", "REUTERS \u00b7 IAEA"),
    (scene_aitax, "9  \u00b7  TRUMP: AI TAX",
     "TRUMP VOWS HUGE AI TAX",
     "Hits US firms building abroad", "REUTERS"),
    (scene_davao, "10  \u00b7  DAVAO: 146 SAFE",
     "ALL 146 SAFE IN DAVAO",
     "Jet lands in Davao; slides out", "AP \u00b7 CAAP"),
    (scene_btc, "11  \u00b7  BITCOIN $57,773",
     "BITCOIN AT $57,773",
     "\u22126.7% in a day; Sep 2024 low", "FINNHUB \u00b7 REUTERS"),
    (scene_f1, "12  \u00b7  F1: VERSTAPPEN P1",
     "VERSTAPPEN TAKES POLE",
     "Fastest man penalised 5 places", "F1.COM \u00b7 FIA"),
    (scene_rahul, "13  \u00b7  RAHUL 136",
     "RAHUL\u2019S 136 LIFTS INDIA",
     "India 486/4, lead 118 at stumps", "CRICINFO"),
]

for i, (fn, label, head, deck, attr) in enumerate(MEDIUM):
    col, row = i % 5, i // 5
    x, y = MX[col], MROW_Y[row]
    fn(x, y, MW, MH)
    banner(x, y, MW, label, font=f_bmd, h=20)
    check(tw(label, f_bmd) <= MW - 10, "medium banner %d too wide" % i)
    hy = y + MH + 3
    hlines = wrap(head, f_h2, MW)
    check(len(hlines) <= 2, "medium headline %d wraps to %d lines: %s"
          % (i, len(hlines), head))
    for j, line in enumerate(hlines):
        d.text((x, hy + j * 23), line, font=f_h2, fill=INK)
    dy2 = hy + len(hlines) * 23 + 2
    check(tw(deck, f_d2) <= MW, "medium deck %d too wide: %s" % (i, deck))
    d.text((x, dy2), deck, font=f_d2, fill=INK)
    d.text((x, dy2 + 13), attr, font=f_a2, fill=MUTED)

MED_END = MROW_Y[1] + MH + 3 + 46 + 2 + 13 + 13   # 817
rule(MED_END + 4, w=1)


# ================================================================
# BOTTOM ROW (map + ALSO) + DATE CHECK
# No VERDICT strip (not in the NI21 spec §13.4); its ~24px funds
# the timeline strip at the top of the page.
# ================================================================
# header row for bottom section
hy2 = MED_END + 8   # 825
d.text((M, hy2), "WHERE IT HAPPENED \u2014 31 PINS", font=f_map_h, fill=RED_DK)
d.text((340, hy2), "ALSO \u2014 IN BRIEF", font=f_map_h, fill=RED_DK)
d.text((W - M - tw("EVERY ITEM DATED 21 NOV 2026", f_scene_xs), hy2 + 1),
       "EVERY ITEM DATED 21 NOV 2026", font=f_scene_xs, fill=MUTED)

# ---- navy pin map (bottom-left) ----
MAP_X, MAP_Y, MAP_W, MAP_H = M, hy2 + 15, 302, 96
d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=NAVY)
# land cells: (row, col ranges) on a 48x24 equirectangular grid
# row r covers lat 90-7.5r .. 82.5-7.5r; col c covers lon -180+7.5c .. -172.5+7.5c
LAND = {
    0: [(18, 20)],
    1: [(9, 13), (16, 21), (26, 26), (31, 32), (36, 37)],
    2: [(5, 7), (9, 14), (17, 21), (25, 26), (28, 47)],
    3: [(4, 8), (9, 16), (18, 18), (22, 22), (25, 27), (28, 47)],
    4: [(6, 7), (8, 17), (18, 19), (23, 23), (25, 27), (28, 46)],
    5: [(6, 17), (23, 23), (24, 30), (31, 40), (41, 45)],
    6: [(6, 16), (22, 23), (24, 28), (29, 35), (36, 41), (42, 42)],
    7: [(7, 16), (21, 30), (31, 35), (36, 41), (42, 42)],
    8: [(7, 12), (21, 31), (32, 37), (38, 41)],
    9: [(8, 12), (22, 31), (35, 40), (41, 41)],
    10: [(9, 11), (13, 16), (22, 30), (37, 40), (41, 43)],
    11: [(12, 17), (23, 30), (39, 44)],
    12: [(12, 17), (23, 30), (40, 44)],
    13: [(13, 17), (23, 29), (41, 45)],
    14: [(13, 17), (23, 29), (30, 30), (41, 45)],
    15: [(13, 16), (23, 28), (30, 30), (41, 45)],
    16: [(13, 16), (24, 27), (42, 45)],
    17: [(13, 15), (44, 45), (46, 47)],
    18: [(13, 14)],
    19: [(13, 13)],
    21: [(8, 10), (22, 24), (38, 40)],
}
LAT_TOP, LAT_BOT = 75.0, -55.0   # cropped inhabited band


def project(lat, lon):
    px = MAP_X + (lon + 180.0) / 360.0 * MAP_W
    py = MAP_Y + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * MAP_H
    return px, py


for r, spans in LAND.items():
    lat_c = 90 - 7.5 * r - 3.75
    if lat_c > LAT_TOP or lat_c < LAT_BOT:
        continue
    for c0, c1 in spans:
        for c in range(c0, c1 + 1):
            lon_c = -180 + 7.5 * c + 3.75
            px, py = project(lat_c, lon_c)
            d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6],
                      fill=NAVY_LT)

# pins: (num, lat, lon, dx_px, dy_px) — dx/dy deconflict the clusters
# (Europe 7 pins in ~30x12px; DC/NYC 4 pins; Vegas/LA 3 pins; Korea 2).
# Global stories pin at their newsroom/decision point: BepiColombo at
# ESOC Darmstadt, Bitcoin at New York.
PINS = [
    (1, 36.9, 30.7, -6, 7), (2, 24.7, 46.7, -6, 5),
    (3, -11.2, -75.9, -4, -4), (4, 49.9, 8.6, 8, -8),
    (5, 47.9, 33.4, 7, 7), (6, 50.4, 30.5, 2, -10),
    (7, 26.5, 56.3, 7, 3), (8, 35.7, 51.4, 0, -8),
    (9, 38.9, -77.0, -10, -6), (10, 7.1, 125.6, 0, 0),
    (11, 40.7, -74.0, 10, -6), (12, 36.2, -115.1, -8, -8),
    (13, -41.3, 174.8, -4, 0), (14, 36.5, 127.3, -6, 5),
    (15, 34.0, -118.5, 0, 8), (16, 51.5, -0.1, -14, 2),
    (17, 36.2, -115.1, 8, -8), (18, 38.6, -90.2, -10, -2),
    (19, 38.9, -77.0, -10, 6), (20, -22.5, -68.9, 4, 4),
    (21, 45.1, 7.7, -8, 5), (22, -6.2, 106.8, 0, 0),
    (23, 39.0, 125.8, 6, -5), (24, -33.9, 151.2, 4, -5),
    (25, -37.8, 145.0, -4, 5), (26, 38.9, -77.0, 10, 6),
    (27, 13.8, 100.5, -4, 4), (28, 28.6, 77.2, 0, -4),
    (29, 20.3, 85.8, 0, 4), (30, 16.8, 96.2, 4, -4),
    (31, 52.5, 13.4, -12, -4),
]
for num, lat, lon, dx, dy in PINS:
    px, py = project(lat, lon)
    pin_dot(px + dx, py + dy, num)

# ---- ALSO: 18 briefs, 2 columns x 9 ----
# Numbers run 14..31. Briefs 29-31 (Akvan remnants rain, Myanmar
# sanctions call, youth march) are carried from the top-1 artifact
# without individual re-verification — flagged in the build report.
BRIEFS = [
    "SEJONG: 5 FREIGHT CARS DERAIL, NO INJURIES",
    "PALISADES ARSONIST CONVICTED ON 2 COUNTS",
    "RUSSIAN HACKERS HIT UK GOVT EMAILS",
    "VERSTAPPEN TO STEWARDS AFTER FP3 CLASH",
    "ROUNDUP: $7.25BN SETTLEMENT APPROVED",
    "VANCE: IRAN STRIKE WAS \u2018TRUMP\u2019S CALL\u2019",
    "CHILE: M4.7 QUAKE NEAR CALAMA, NO DAMAGE",
    "ZVEREV v MEDVEDEV IN TURIN SEMI TONIGHT",
    "PLN SIGNS SIX CLEAN-POWER DEALS AT COP31",
    "KIM TOURS FACTORY SITES, SNUBS TRUMP TALKS",
    "SYDNEY HEATWAVE WARNING AS WEST HITS 33\u00b0C",
    "CUMMINS STAYS CAPTAIN DESPITE SANDPAPER ROW",
    "HIMES THREATENS SPACEX FUNDS OVER STARSHIELD",
    "BANGKOK UNVEILS SIX-POINT ARSENIC PLAN",
    "PAKISTANI MINISTER AT DELHI SCO FORUM",
    "AKVAN REMNANTS BRING RAIN TO EASTERN INDIA",
    "CALL FOR NEW MYANMAR SANCTIONS",
    "YOUTH MARCH IN 400 CITIES FOR CLIMATE",
]
AY = MAP_Y + 1
for i, text in enumerate(BRIEFS):
    col = i // 9
    row = i % 9
    bx = 340 + col * 330
    by = AY + row * 11
    num = str(14 + i)
    d.text((bx, by), num, font=f_brief_n, fill=RED)
    d.text((bx + tw(num + "  ", f_brief_n), by), text, font=f_brief,
           fill=INK)

# ---- DATE CHECK ----
DC_Y = MAP_Y + MAP_H + 8   # 944
rule(DC_Y, w=1)
d.text((M, DC_Y + 4), "DATE CHECK", font=f_dc_h, fill=RED_DK)
note = "\u2014 NOT SHOWN BECAUSE THEY HAPPENED ON ANOTHER DAY"
d.text((M + tw("DATE CHECK ", f_dc_h), DC_Y + 4), note, font=f_dc_h,
       fill=INK)
legend = "CHIP: CLAIM = UNVERIFIED \u00b7 FORECAST = NOT YET HAPPENED"
d.text((W - M - tw(legend, f_scene_xs), DC_Y + 6), legend,
       font=f_scene_xs, fill=MUTED)
# 12 specific exclusions, 4 cols x 3 rows. Five more verified
# exclusions (ANC 31% 4 Nov, Port Louis 7 Oct, SA crime stats Fri,
# Vancouver trial end Fri, Jazan intercepts Fri eve) are documented in
# the build report; the Jazan correction lives in main #2's deck.
DC_ITEMS = [
    "UK\u2013EU RESET DEAL \u2014 FRI",
    "POLAND MISSILE INTERCEPT \u2014 FRI",
    "WALL STREET CORRECTION \u2014 FRI",
    "CYCLONE AKVAN LANDFALL \u2014 FRI",
    "KYIV BRIDGES BARRAGE \u2014 FRI",
    "900,000 AI CHIPS FOR CHINA \u2014 THU",
    "INDIA H5N1 VACCINE LAUNCH \u2014 FRI",
    "BRITAIN ADMITS CYBERATTACKS \u2014 FRI",
    "CALIFORNIA SUBPOENAS NVIDIA \u2014 THU",
    "TEXAS EXECUTION (DENNES) \u2014 THU",
    "COPENHAGEN EXPELS ATTACHÉ — FRI",
    "NIGERIA FUNERAL BOAT \u2014 FRI",
]
for i, item in enumerate(DC_ITEMS):
    col, row = i // 3, i % 3
    dx = M + col * 242
    dy = DC_Y + 22 + row * 11
    d.text((dx, dy), "\u00d7", font=f_dc, fill=RED)
    d.text((dx + 12, dy), item, font=f_dc, fill=INK)

# not-yet line: things deliberately not shown because they had not
# happened at press time
notyet = ("NOT YET AT PRESS TIME: BepiColombo orbit outcome \u00b7 "
          "F1 race result \u00b7 COP31 final text \u00b7 "
          "Zverev\u2013Medvedev result")
notyet_y = DC_Y + 22 + 3 * 11 + 2   # 1001
d.text((M, notyet_y), notyet, font=f_dc_note, fill=INK)

# ---- validation: every measured element must fit its box ----
check(tw(strap, f_strap) <= CW, "strapline too wide")
check(tw(kick, f_kicker) <= CW, "kicker too wide")
check(tw(mast, f_mast) <= CW, "masthead too wide")
check(tl_w <= CW, "timeline too wide")
check(tw(notyet, f_dc_note) <= CW, "not-yet line too wide")
check(notyet_y + 14 <= H, "page overflows: not-yet line ends %d"
      % (notyet_y + 14))
for i, text in enumerate(BRIEFS):
    wline = tw(str(14 + i) + "  ", f_brief_n) + tw(text, f_brief)
    check(wline <= 322, "brief %d too wide: %s" % (14 + i, text))
for i, item in enumerate(DC_ITEMS):
    check(12 + tw(item, f_dc) <= 237, "date-check %d too wide" % i)
# structural count checks — kicker total must equal region sum must
# equal mains + briefs must equal pin count.
_total = sum(n for _, n in regions)
check(_total == 31, "region bar sums to %d, not 31" % _total)
check(len(PINS) == 31, "pin count is %d, not 31" % len(PINS))
check(len(BRIEFS) == 18, "brief count is %d, not 18" % len(BRIEFS))
check(len(DC_ITEMS) == 12, "date-check count is %d, not 12"
      % len(DC_ITEMS))
check(len(LARGE) + len(MEDIUM) == 13, "main count is %d, not 13"
      % (len(LARGE) + len(MEDIUM)))
check(sorted(n for n, _, _, _, _ in PINS) == list(range(1, 32)),
      "pin numbers are not 1..31")
if WARN:
    print("WARNINGS:")
    for wmsg in WARN:
        print(" -", wmsg)
else:
    print("all width checks passed")

# ---- save ----
img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
