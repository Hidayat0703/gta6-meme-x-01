#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme (v3). Vice City sunset, make.fun ghost driving a
pink convertible, holding its magenta star coin. PIL only, deterministic.
Canvas 1024x1024. Run: python3 draw_meme.py -> meme.png (+ meme-480.png preview).
v3 fixes (from v1 inspection): ghost hem hidden behind car; sun bigger so its
rim shows around the ghost; palms redrawn as drooping curved fronds; plate
moved clear of the wheels; lane dashes stop above the bottom caption."""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def sky_color(y):
    stops = [(0, (26, 11, 46)), (280, (123, 30, 110)), (480, (214, 51, 108)),
             (600, (255, 122, 61)), (660, (255, 201, 61))]
    for i in range(len(stops) - 1):
        y0, c0 = stops[i]; y1, c1 = stops[i + 1]
        if y0 <= y <= y1:
            return lerp(c0, c1, (y - y0) / max(1, y1 - y0))
    return stops[-1][1]

def star5(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

def sparkle(cx, cy, r):
    return [(cx, cy - r), (cx + r * 0.28, cy - r * 0.28), (cx + r, cy),
            (cx + r * 0.28, cy + r * 0.28), (cx, cy + r),
            (cx - r * 0.28, cy + r * 0.28), (cx - r, cy),
            (cx - r * 0.28, cy - r * 0.28)]

def text_fit(draw, text, max_w, start, font_path=BOLD):
    size = start
    while size > 20:
        f = ImageFont.truetype(font_path, size)
        if draw.textbbox((0, 0), text, font=f)[2] <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(font_path, 20)

def outlined(draw, xy, text, font, fill=(255, 255, 255), stroke=(10, 8, 20), sw=8):
    draw.text(xy, text, font=font, fill=fill, stroke_width=sw,
              stroke_fill=stroke, anchor="ma")

img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)

# --- sky gradient 0-660 ---
for y in range(0, 660):
    d.line([(0, y), (W, y)], fill=sky_color(y))

# stars in upper sky
random.seed(6)
for _ in range(70):
    x = random.randint(0, W); y = random.randint(0, 250); r = random.choice([1, 1, 2])
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255))

# --- synthwave sun (center 512, 470, r 175) with slats ---
sx, sy, sr = 512, 470, 175
d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 233, 168))
for yy, hh in [(505, 5), (530, 7), (556, 9), (584, 11), (612, 13)]:
    d.rectangle([sx - sr - 4, yy, sx + sr + 4, yy + hh], fill=sky_color(yy))

# --- ocean (620-700) ---
d.rectangle([0, 620, W, 700], fill=(11, 61, 77))
for yy in range(632, 695, 13):
    d.line([(60, yy), (964, yy)], fill=(64, 160, 190), width=3)
for i in range(5):
    yy = 630 + i * 12
    w = 55 - i * 8
    d.line([(512 - w, yy), (512 + w, yy)], fill=(255, 220, 130), width=5)

# --- road (700-1024) ---
d.rectangle([0, 700, W, H], fill=(20, 16, 31))
d.polygon([(0, 700), (W, 700), (700, H), (324, H)], fill=(28, 22, 44))
for i in range(3):
    y0 = 730 + i * 48
    w0 = 5 + i * 5
    d.polygon([(512 - w0, y0), (512 + w0, y0), (512 + w0 + 13, y0 + 26), (512 - w0 - 13, y0 + 26)],
              fill=(255, 214, 80))
d.line([(0, 700), (W, 700)], fill=(255, 120, 90), width=3)

# --- palm silhouettes: drooping curved fronds ---
PALM = (14, 7, 24)
def palm(x_base, y_base, s, lean):
    d.line([(x_base, y_base), (x_base + lean, y_base - 250 * s)], fill=PALM, width=int(15 * s))
    tx, ty = x_base + lean, y_base - 250 * s
    for ang in (-165, -130, -95, -60, -25, 10):
        a = math.radians(ang)
        x2 = tx + math.cos(a) * 150 * s
        y2 = ty + math.sin(a) * 90 * s + 55 * s
        cx, cy = (tx + x2) / 2, min(ty, y2) - 55 * s
        pts = []
        for k in range(13):
            t = k / 12
            x = (1 - t) ** 2 * tx + 2 * (1 - t) * t * cx + t * t * x2
            y = (1 - t) ** 2 * ty + 2 * (1 - t) * t * cy + t * t * y2
            pts.append((x, y))
        d.line(pts, fill=PALM, width=int(9 * s), joint="curve")
palm(70, 720, 1.0, 40)
palm(950, 720, 0.9, -35)

# --- ghost driver FIRST (car drawn over its lower half) ---
GX = 512
OUT = (10, 8, 20)
DY, S = 530, 0.9
def ghost_body(dx, dy, scale, fill):
    pts = []
    for a in range(180, 361, 6):
        pts.append((dx + 150 * scale * math.cos(math.radians(a)),
                    dy + 150 * scale * math.sin(math.radians(a)) * 0.95))
    pts += [(dx + 150 * scale, dy + 260 * scale),
            (dx + 110 * scale, dy + 300 * scale),
            (dx + 75 * scale, dy + 262 * scale),
            (dx + 38 * scale, dy + 300 * scale),
            (dx + 0 * scale, dy + 262 * scale),
            (dx - 38 * scale, dy + 300 * scale),
            (dx - 75 * scale, dy + 262 * scale),
            (dx - 110 * scale, dy + 300 * scale),
            (dx - 150 * scale, dy + 260 * scale)]
    d.polygon(pts, fill=fill)
ghost_body(GX, DY, S, OUT)
ghost_body(GX, DY, S * 0.93, (255, 255, 255))
for ex in (GX - 52, GX + 52):
    d.polygon(sparkle(ex, DY - 38, 29), fill=(10, 8, 20))
# right hand + magenta star coin (raised)
d.ellipse([GX + 115, 575, GX + 185, 645], fill=(255, 255, 255), outline=OUT, width=8)
d.ellipse([GX + 114, 534, GX + 186, 606], fill=(255, 46, 136), outline=OUT, width=8)
d.polygon(star5(GX + 150, 570, 24, 10), fill=(255, 255, 255))
# left hand + steering wheel are drawn after the car (see below, on the windshield)

# --- convertible (side view, facing right) ---
CAR = (255, 46, 136); CAR_D = (10, 8, 20)
d.rounded_rectangle([180, 745, 844, 815], radius=26, fill=CAR, outline=CAR_D, width=6)
d.rounded_rectangle([180, 720, 420, 760], radius=18, fill=CAR, outline=CAR_D, width=6)
d.polygon([(430, 752), (470, 690), (600, 690), (640, 752)], fill=(150, 225, 255), outline=CAR_D)
d.line([(430, 752), (470, 690)], fill=CAR_D, width=6)
d.line([(640, 752), (600, 690)], fill=CAR_D, width=6)
for wx in (300, 710):
    d.ellipse([wx - 42, 758, wx + 42, 842], fill=(8, 8, 14), outline=(255, 255, 255), width=4)
    d.ellipse([wx - 18, 782, wx + 18, 818], fill=(220, 220, 230))
d.ellipse([800, 758, 838, 788], fill=(255, 240, 150), outline=CAR_D, width=4)
d.rounded_rectangle([762, 786, 840, 812], radius=6, fill=(255, 255, 255), outline=CAR_D, width=3)
pf = ImageFont.truetype(BOLD, 15)
d.text((801, 799), "MAKEFUN", font=pf, fill=(10, 8, 20), anchor="mm")

# steering wheel on the windshield + ghost's left hand on it
d.ellipse([415, 672, 475, 732], fill=(150, 225, 255), outline=OUT, width=7)
d.line([(445, 702), (445, 672)], fill=OUT, width=6)
d.line([(445, 702), (425, 722)], fill=OUT, width=6)
d.line([(445, 702), (465, 722)], fill=OUT, width=6)
d.ellipse([423, 680, 467, 724], fill=(255, 255, 255), outline=OUT, width=7)

# --- captions ---
f_top = text_fit(d, "13 YEARS. 2 DELAYS. 212 GB.", 950, 72)
outlined(d, (512, 40), "13 YEARS. 2 DELAYS. 212 GB.", f_top)
f_bot = text_fit(d, "MY AI AGENT PAID FOR IT.", 950, 64)
outlined(d, (512, 884), "MY AI AGENT PAID FOR IT.", f_bot)
f_sub = text_fit(d, "VICE CITY  —  make.fun", 950, 40)
outlined(d, (512, 952), "VICE CITY  —  make.fun", f_sub, fill=(255, 214, 80))

img.save("meme.png")
img.resize((480, 480), Image.LANCZOS).save("meme-480.png")
print("saved meme.png + meme-480.png")
