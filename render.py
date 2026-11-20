#!/usr/bin/env python3
"""Render entry.png for news-image-20261119, agent 4 (plucky-harbor-48).
MAGAZINE SPREAD layout: navy masthead, three equal hero panels, left 2x3
secondary grid, tall right world-map column, bottom briefs strip.
39 stories, all reported on Thursday 19 November 2026. Flat vector style.
Deterministic: fixed fonts, fixed geometry, no timestamps in the PNG.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 243, 232)
INK = (26, 26, 26)
RED = (179, 39, 30)
NAVY = (22, 35, 63)
GOLD = (201, 162, 39)
GREY = (85, 85, 85)
MINT = (234, 242, 236)
DOTGREEN = (90, 107, 93)
SKY = (220, 232, 240)
SAND = (238, 232, 210)
PALE = (242, 236, 220)

DJ_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
DJ_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
NOTO_IT = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
DJ_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DJ_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_lines(draw, x, y, lines, font, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def num_circle(draw, cx, cy, n, r=10):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    f = F(DJ_SANS_B, 8 if r <= 8 else 11 if r <= 10 else 13)
    tw = draw.textlength(str(n), font=f)
    th = draw.textbbox((0, 0), str(n), font=f)[3]
    draw.text((cx - tw / 2, cy - th / 2 - 1), str(n),
              font=f, fill=(255, 255, 255))


def kicker(draw, x, y, s):
    draw.text((x, y), s, font=F(DJ_SANS_B, 10), fill=RED)


# ---------------- illustrations (flat vector, 1-2px outlines) ----------------

def ill_icj(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(196, 196, 170))
    # courthouse: pediment + columns + steps
    cx, cy, bw = x + w // 2 - 28, y + 18, 56
    d.polygon([(cx - 8, cy + 16), (cx + bw + 8, cy + 16), (cx + bw // 2, cy)],
              fill=(250, 246, 236), outline=INK)
    d.rectangle([cx, cy + 16, cx + bw, cy + 62], fill=(250, 246, 236), outline=INK)
    for i in range(4):
        px = cx + 6 + i * 14
        d.rectangle([px, cy + 20, px + 5, cy + 58], fill=NAVY)
    d.rectangle([cx - 8, cy + 62, cx + bw + 8, cy + 66], fill=NAVY)
    d.rectangle([cx - 12, cy + 66, cx + bw + 12, cy + 70], fill=NAVY)
    # scales of justice, right
    sx, sy = x + w - 52, y + 30
    d.line([sx, sy, sx, sy + 42], fill=INK, width=2)
    d.line([sx - 16, sy + 4, sx + 16, sy + 4], fill=INK, width=2)
    d.polygon([(sx - 22, sy + 20), (sx - 10, sy + 20), (sx - 16, sy + 10)],
              fill=GOLD, outline=INK)
    d.polygon([(sx + 10, sy + 20), (sx + 22, sy + 20), (sx + 16, sy + 10)],
              fill=GOLD, outline=INK)
    d.ellipse([sx - 3, sy - 4, sx + 3, sy + 2], fill=GOLD, outline=INK)


def ill_apec(d, x, y, w, h):
    # APEC Shenzhen trilateral: flat skyline + 3 flag poles + round summit
    # table with seated figures. Buildings carry windows/roofs so they read
    # as a skyline, never as bars; flags stand in open sky; the table is
    # the foreground element with three seated figures behind it.
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    ground = y + h - 22
    d.rectangle([x, ground, x + w, y + h], fill=(196, 196, 170))
    # skyline cluster, left half: varied widths/heights, navy silhouettes
    for bx, bw, bh in [(6, 30, 34), (40, 24, 52), (68, 34, 28),
                       (106, 26, 44), (136, 28, 36)]:
        d.rectangle([x + bx, ground - bh, x + bx + bw, ground],
                    fill=NAVY, outline=INK)
    # spire on the tallest tower
    d.polygon([(x + 44, ground - 52), (x + 60, ground - 52),
               (x + 52, ground - 62)], fill=NAVY, outline=INK)
    # slanted roof on the low wide block
    d.polygon([(x + 68, ground - 28), (x + 102, ground - 28),
               (x + 102, ground - 36), (x + 85, ground - 36)],
              fill=NAVY, outline=INK)
    # windows: small cream panes so the blocks read as buildings
    for wx, wy in [(14, ground - 26), (24, ground - 26), (14, ground - 14),
                   (46, ground - 44), (56, ground - 44), (46, ground - 32),
                   (76, ground - 20), (90, ground - 20),
                   (112, ground - 36), (122, ground - 36),
                   (112, ground - 24), (142, ground - 28),
                   (152, ground - 28), (142, ground - 16)]:
        d.rectangle([x + wx, wy, x + wx + 4, wy + 5], fill=(250, 246, 236))
    # three flag poles in the open sky, right of the skyline
    for i, col in enumerate([RED, GOLD, NAVY]):
        px = x + 170 + i * 30
        d.line([px, y + 12, px, ground], fill=INK, width=2)
        d.polygon([(px, y + 12), (px + 18, y + 17), (px, y + 22)], fill=col,
                  outline=INK)
    # round summit table with three seated figures (dots/blocks, no faces)
    for i, col in enumerate([RED, NAVY, GOLD]):
        cx = x + 186 + i * 36
        d.ellipse([cx - 5, y + 62, cx + 5, y + 72], fill=col, outline=INK)
        d.rectangle([cx - 8, y + 72, cx + 8, y + 84],
                    fill=(250, 246, 236), outline=INK)
    d.ellipse([x + 168, y + 80, x + 300, y + 97],
              fill=(250, 246, 236), outline=INK)
    d.line([x + 168, y + 88, x + 300, y + 88], fill=INK, width=1)


def ill_anthropic(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=MINT)
    # chip
    cx, cy = x + 22, y + 22
    d.rectangle([cx, cy, cx + 64, cy + 48], fill=NAVY, outline=INK)
    d.rectangle([cx + 16, cy + 12, cx + 48, cy + 36], fill=GOLD, outline=INK)
    for i in range(4):
        d.line([cx + 8 + i * 14, cy, cx + 8 + i * 14, cy - 8], fill=INK, width=2)
        d.line([cx + 8 + i * 14, cy + 48, cx + 8 + i * 14, cy + 56],
               fill=INK, width=2)
    # rising chart
    ox, oy = x + 108, y + 62
    pts = [(ox, oy), (ox + 30, oy - 18), (ox + 58, oy - 8), (ox + 88, oy - 34),
           (ox + 118, oy - 48)]
    d.line(pts, fill=RED, width=3)
    d.polygon([(ox + 118, oy - 48), (ox + 106, oy - 44), (ox + 114, oy - 34)],
              fill=RED)
    d.line([ox, oy + 8, ox + 128, oy + 8], fill=INK, width=1)


def ill_jeffries(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # podium + flag
    d.line([x + 16, y + 8, x + 16, y + h - 14], fill=INK, width=2)
    d.polygon([(x + 16, y + 8), (x + 40, y + 13), (x + 16, y + 18)],
              fill=RED)
    d.rectangle([x + 78, y + h - 26, x + 118, y + h - 10], fill=NAVY)
    d.rectangle([x + 84, y + h - 40, x + 112, y + h - 26], fill=(250, 246, 236),
                outline=INK)
    d.ellipse([x + 92, y + h - 52, x + 104, y + h - 40], fill=RED, outline=INK)


def ill_vangogh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PALE)
    d.rectangle([x + 52, y + 8, x + w - 52, y + h - 8], fill=(250, 246, 236),
                outline=INK, width=2)
    d.rectangle([x + 58, y + 14, x + w - 58, y + h - 14], fill=(240, 200, 90),
                outline=INK)
    # sun + swirl strokes
    d.ellipse([x + w - 92, y + 18, x + w - 72, y + 38], fill=(255, 120, 40),
              outline=INK)
    for i, yy in enumerate([44, 50, 56]):
        d.line([x + 64, y + yy, x + w - 66, y + yy - 4], fill=(46, 92, 60),
               width=2)


def ill_gta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 214, 170))
    d.ellipse([x + w // 2 - 22, y + 8, x + w // 2 + 22, y + 52],
              fill=(255, 120, 60), outline=INK)
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(46, 92, 60))
    # palm
    d.line([x + 26, y + h - 22, x + 26, y + 22], fill=INK, width=2)
    for dx, dy in [(-16, -6), (16, -6), (-12, 4), (12, 4)]:
        d.line([x + 26, y + 22, x + 26 + dx, y + 22 + dy], fill=INK, width=2)


def ill_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SAND)
    d.line([x, y + h - 14, x + w, y + h - 14], fill=INK, width=1)
    # tank silhouette
    d.rectangle([x + 46, y + 22, x + 116, y + 40], fill=NAVY, outline=INK)
    d.rectangle([x + 58, y + 40, x + 128, y + 50], fill=NAVY, outline=INK)
    d.line([x + 116, y + 28, x + 152, y + 20], fill=INK, width=3)
    d.line([x + 130, y + 52, x + 130, y + 60], fill=RED, width=2)
    d.line([x + 152, y + 52, x + 152, y + 60], fill=RED, width=2)


def ill_eu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    cx, cy = x + w // 2, y + h // 2
    for i in range(8):
        import math
        a = i * math.pi / 4
        sx, sy = cx + int(30 * math.cos(a)), cy + int(30 * math.sin(a))
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=GOLD, outline=INK)
    f = F(DJ_SANS_B, 22)
    tw = d.textlength("\u20ac", font=f)
    d.text((cx - tw / 2, cy - 12), "\u20ac", font=f, fill=NAVY)


def ill_nvidia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=MINT)
    d.rectangle([x + 30, y + 16, x + 86, y + 48], fill=NAVY, outline=INK)
    d.rectangle([x + 44, y + 24, x + 72, y + 40], fill=GOLD, outline=INK)
    pts = [(x + 100, y + 44), (x + 124, y + 30), (x + 146, y + 36),
           (x + 168, y + 14)]
    d.line(pts, fill=RED, width=3)


CARD_ILL = {4: ill_jeffries, 5: ill_vangogh, 6: ill_gta,
            7: ill_gaza, 8: ill_eu, 9: ill_nvidia}

HEROES = [
    (1, "WORLD \u00b7 JUSTICE", "Myanmar guilty of genocide \u2014 a first in 80 years",
     "First state found guilty of genocide, 9\u20136. ~10,000 Rohingya "
     "killed in 2017.", ill_icj),
    (2, "ASIA \u00b7 SUMMIT", "Trump, Xi, Putin: first trilateral",
     "First trilateral, ~90 min at Kylin Villa. Peace declaration; "
     "no Ukraine deal, no deadline.", ill_apec),
    (3, "MARKETS \u00b7 IPO", "$81.3bn \u2014 the biggest IPO in history",
     "980m shares at $83, ~$1.5tn value. Debut closed $97.17, up 17%, "
     "passing SpaceX\u2019s $75bn.", ill_anthropic),
]

CARDS = [
    (4, "USA \u00b7 POLITICS", "Jeffries nominated for Speaker, 251\u201311",
     "Democrats nominate Jeffries; if elected 3 Jan, first Black Speaker."),
    (5, "CULTURE \u00b7 ART", "Van Gogh sells for $190.4m \u2014 a record",
     "Sotheby\u2019s New York, reported 19 Nov; passes the $117.2m record."),
    (6, "CULTURE \u00b7 GAMES", "GTA VI opens after 13 years",
     "Out 19 Nov, PS5 and Xbox. 13 years after GTA V; 99 on Metacritic."),
    (7, "MIDDLE EAST \u00b7 WAR", "Israeli tanks cross the Yellow Line",
     "Ground operation 18\u201319 Nov, first since Oct 2025 truce; 3 killed."),
    (8, "EUROPE \u00b7 WAR", "EU proposes \u20ac45bn loan for Ukraine",
     "Covers ~2/3 of a \u20ac70bn gap; repaid only if Russia pays reparations."),
    (9, "MARKETS \u00b7 TECH", "Nvidia posts $115.8bn quarter",
     "Reported 18 Nov. Huang won\u2019t return as CEO; Kress stays interim CEO."),
]

# map pins: (number, x, y) in map-panel coordinates (panel 352 x 240)
PINS = [
    (1, 168, 56), (2, 316, 88), (3, 96, 64), (4, 88, 88), (5, 116, 74),
    (6, 158, 40), (7, 204, 92), (8, 180, 68), (9, 104, 96), (10, 220, 52),
    (11, 208, 74), (12, 304, 100), (13, 84, 158), (14, 224, 132),
    (15, 202, 148),
]
# small red dots for briefs 16-39, spread over continents
BRIEF_DOTS = [
    (60, 60), (120, 100), (150, 150), (190, 200), (230, 60), (260, 120),
    (300, 160), (320, 200), (90, 180), (140, 210), (180, 110), (210, 180),
    (250, 200), (290, 60), (70, 130), (110, 200), (160, 90), (200, 210),
    (240, 150), (280, 100), (310, 130), (50, 100), (130, 60), (270, 180),
]
# continent blobs (cx, cy, rx, ry) in map-panel coordinates
BLOBS = [(70, 70, 55, 40), (105, 185, 30, 55), (185, 60, 28, 22),
         (190, 140, 32, 55), (270, 70, 65, 45), (300, 215, 28, 18)]

MAP_KEY = [
    (10, "Crimean Bridge hit again; trains halted"),
    (11, "Odesa: Russian strikes kill 4"),
    (12, "Shenzhen: Xi meets Japan\u2019s Takaichi"),
    (13, "Caracas: US\u2013Venezuela anti-drug pact"),
    (14, "Aden: Houthis named a terrorist group"),
    (15, "Badme: troops mass; monitors said so"),
]

BRIEFS = [
    (16, "CYCLONE AKVAN", "Severe storm nears India\u2019s east coast; Odisha evacuates."),
    (17, "GOLD", "Slides to $3,757/oz, lowest since Sept 2025."),
    (18, "FINLAND", "Approves Onkalo, world\u2019s first nuclear waste store."),
    (19, "ESTONIA", "Plans to shut Russia border crossings from Dec."),
    (20, "CZECHIA", "Huge Prague protest for media independence."),
    (21, "SPAIN", "General strike disrupts ports and factories."),
    (22, "YEMEN", "Houthi rocket kills 53 soldiers at army camp."),
    (23, "GERMANY", "Russian arrested for spying on US firm Palantir."),
    (24, "INDIA\u2013JAPAN", "2+2 defence talks open in Tokyo."),
    (25, "PEW", "Islam on track to be world\u2019s largest faith by 2035."),
    (26, "SPORT", "England beat Australia by 97 runs; Duckett 133."),
    (27, "INDIA", "\u201cRamayana\u201d crosses \u20b91,000 crore in 14 days."),
    (28, "OBITUARY", "Actor Stacy Keach dies at 85."),
    (29, "UK", "Ground rents in England & Wales capped from 2028."),
    (30, "UK", "Google rejects call to remove Russell Brand video."),
    (31, "ITALY", "Bayesian yacht report blames wind vulnerability."),
    (32, "GERMANY", "2027 tax forecast hits record \u20ac1 trillion."),
    (33, "CLIMATE", "Nearly all coral reefs face extinction in 50 years."),
    (34, "LIBYA", "Cocaine and millions of pills seized in the east."),
    (35, "SAUDI ARABIA", "Danger passed in three southern cities."),
    (36, "VOYAGER 1", "Now one light-day from Earth; signals take 24 hours."),
    (37, "CANADA", "Carney recalibrates China ties, seeks US deal."),
    (38, "USA", "Senators warn AI cyber threats outpace defences."),
    (39, "FED", "Minutes: most officials expect further rate hikes."),
]


def render():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---- masthead: navy band ----
    d.rectangle([0, 0, W, 116], fill=NAVY)
    kf = F(DJ_SANS_B, 11)
    d.text((24, 12), "THE DAY IN WORLD NEWS", font=kf, fill=GOLD)
    rt = "39 STORIES \u00b7 6 CONTINENTS \u00b7 ONE DAY"
    d.text((W - 24 - d.textlength(rt, font=kf), 12), rt, font=kf, fill=GOLD)
    d.text((24, 34), "Thursday 19 November 2026",
           font=F(DJ_SERIF_B, 56), fill=(255, 255, 255))
    d.text((24, 94), "Every story on this page happened, or was first "
           "reported, on this day.",
           font=F(NOTO_IT, 14), fill=(220, 220, 210))
    d.rectangle([0, 116, W, 118], fill=GOLD)

    # ---- hero: three equal panels ----
    hy, hh = 126, 222
    pw, gap = 314, 12
    for i, (n, kick, head, deck, ill) in enumerate(HEROES):
        x = 24 + i * (pw + gap)
        d.rectangle([x, hy, x + pw, hy + hh], outline=INK, width=1)
        ill(d, x + 1, hy + 1, pw - 2, 100)
        ty = hy + 104
        num_circle(d, x + 14, ty + 7, n, r=10)
        d.text((x + 30, ty), kick, font=F(DJ_SANS_B, 10), fill=RED)
        ty += 18
        hl = wrap(d, head, F(DJ_SERIF_B, 19), pw - 16)
        assert len(hl) <= 3, ("hero headline overflow", n, hl)
        ty = text_lines(d, x + 8, ty, hl, F(DJ_SERIF_B, 19), INK, 21)
        dl = wrap(d, deck, F(DJ_SANS, 11), pw - 16)
        assert len(dl) <= 2, ("hero deck overflow", n, dl)
        ty = text_lines(d, x + 8, ty + 3, dl, F(DJ_SANS, 11), INK, 13)
        assert ty <= hy + hh - 2, ("hero text overflow", n, ty)

    # ---- secondary grid, left 2x3 ----
    gx, gy = 24, 360
    cw, ch, cg = 202, 200, 12
    for idx, (n, kick, head, deck) in enumerate(CARDS):
        r, c = divmod(idx, 3)
        x = gx + c * (cw + cg)
        y = gy + r * (ch + 8)
        d.rectangle([x, y, x + cw, y + ch], outline=INK, width=1)
        CARD_ILL[n](d, x + 1, y + 1, cw - 2, 60)
        ty = y + 68
        num_circle(d, x + 13, ty + 6, n, r=9)
        d.text((x + 27, ty), kick, font=F(DJ_SANS_B, 9), fill=RED)
        ty += 18
        hl = wrap(d, head, F(DJ_SERIF_B, 16), cw - 14)
        assert len(hl) <= 3, ("card headline overflow", n, hl)
        ty = text_lines(d, x + 7, ty, hl, F(DJ_SERIF_B, 16), INK, 19)
        dl = wrap(d, deck, F(DJ_SANS, 10), cw - 14)
        assert len(dl) <= 2, ("card deck overflow", n, dl)
        ty = text_lines(d, x + 7, ty + 2, dl, F(DJ_SANS, 10), INK, 13)
        assert ty <= y + ch - 4, ("card text overflow", n, ty)

    # ---- world map, tall right column ----
    mx, my, mw = 660, 360, 340
    hf = F(DJ_SANS_B, 12)
    d.text((mx, my), "WHERE IT HAPPENED", font=hf, fill=INK)
    d.line([mx, my + 18, mx + mw, my + 18], fill=INK, width=1)
    mpx, mpy, mpw, mph = mx, my + 26, mw, 238
    d.rectangle([mpx, mpy, mpx + mpw, mpy + mph], fill=MINT, outline=INK)
    # dotted continents
    for gy2 in range(mpy + 6, mpy + mph - 4, 9):
        for gx2 in range(mpx + 6, mpx + mpw - 4, 9):
            px, py = gx2 - mpx, gy2 - mpy
            for (bcx, bcy, rx, ry) in BLOBS:
                if ((px - bcx) / rx) ** 2 + ((py - bcy) / ry) ** 2 <= 1:
                    d.ellipse([gx2 - 2, gy2 - 2, gx2 + 2, gy2 + 2],
                              fill=DOTGREEN)
                    break
    for (bx, by) in BRIEF_DOTS:
        d.ellipse([mpx + bx - 3, mpy + by - 3, mpx + bx + 3, mpy + by + 3],
                  fill=RED)
    for (n, px, py) in PINS:
        num_circle(d, mpx + px, mpy + py, n, r=7)
    # map key: pin stories 10-15 in words (readable from the image alone)
    ky = mpy + mph + 10
    d.text((mx, ky), "ON THE MAP", font=F(DJ_SANS_B, 10), fill=RED)
    ky += 15
    for (n, s) in MAP_KEY:
        d.text((mx, ky), str(n), font=F(DJ_SANS_B, 10), fill=RED)
        d.text((mx + 20, ky), s, font=F(DJ_SANS, 10), fill=INK)
        ky += 14
    ly = ky + 4
    d.text((mx, ly), "Numbered pin: stories 1\u201315 \u00b7 red dot: briefs 16\u201339",
           font=F(DJ_SANS, 10), fill=GREY)

    # ---- briefs strip ----
    by = 786
    d.text((24, by), "ALSO ON THURSDAY 19 NOVEMBER 2026",
           font=F(DJ_SANS_B, 12), fill=INK)
    d.line([24, by + 18, W - 24, by + 18], fill=INK, width=1)
    bf_n = F(DJ_SANS_B, 11)
    bf_b = F(DJ_SANS_B, 11)
    bf_r = F(DJ_SANS, 11)
    col_w = 488
    for i, (n, lead, rest) in enumerate(BRIEFS):
        col, row = divmod(i, 12)
        x = 24 + col * col_w
        y = by + 26 + row * 14
        num = str(n) + " "
        d.text((x, y), num, font=bf_n, fill=RED)
        nx = x + d.textlength(num, font=bf_n)
        d.text((nx, y), lead + " \u2014 ", font=bf_b, fill=INK)
        lx = nx + d.textlength(lead + " \u2014 ", font=bf_b)
        d.text((lx, y), rest, font=bf_r, fill=INK)
    d.line([24, by + 26 + 12 * 14 + 2, W - 24, by + 26 + 12 * 14 + 2],
           fill=INK, width=1)

    # ---- footer ----
    fy = by + 26 + 12 * 14 + 10
    d.line([24, fy, W - 24, fy], fill=INK, width=2)
    ff = F(DJ_SANS, 10)
    d.text((24, fy + 6),
           "Every story was reported on 19 November 2026; disputed claims "
           "are attributed.", font=ff, fill=GREY)
    d.text((24, fy + 20),
           "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 Al Jazeera. "
           "Original drawings.", font=ff, fill=GREY)
    return img


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = render()
    img.save(out, format="PNG")
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
