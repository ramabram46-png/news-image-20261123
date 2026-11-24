#!/usr/bin/env python3
"""Draw the news-image-20261123 poster: one 1024x1024 PNG summing up the
world news of Monday 23 November 2026, newspaper front-page style.

Fresh code written for this entry. No network, no randomness, no timestamps:
the same script always writes the same bytes. Run: python3 draw_poster.py
writes entry.png next to this file.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 28                      # outer margin
CW = W - 2 * M              # content width: 968

PAPER = (246, 241, 227)     # warm newsprint
INK = (20, 20, 20)
RED = (169, 31, 34)
GREY = (107, 101, 88)
RULE = (201, 192, 168)      # light rule
BORDER = (216, 208, 184)
GOLD = (201, 168, 106)
BAND = (18, 18, 18)         # black numbers band
BAND_DIV = (70, 70, 70)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, fnt, max_w, lh, color=INK):
    """Draw wrapped paragraph; return y below the last line."""
    for line in wrap(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=color)
        y += lh
    return y


def hline(d, x0, x1, y, color=RULE, width=1):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


def vline(d, x, y0, y1, color=RULE, width=1):
    d.line([(x, y0), (x, y1)], fill=color, width=width)


def kicker(d, x, y, text, size=13):
    d.text((x, y), text, font=F(SANS_B, size), fill=RED)


# ---------------- world locator map ----------------
# Simplified continent outlines in (lon, lat); equirectangular projection.
MAP_NAVY = (35, 48, 72)

CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-110, 73), (-95, 80),
     (-85, 76), (-80, 73), (-70, 62), (-60, 55), (-55, 47), (-60, 45),
     (-65, 44), (-70, 42), (-74, 39), (-76, 35), (-80, 32), (-81, 26),
     (-84, 30), (-90, 21), (-97, 16), (-94, 17), (-100, 20), (-105, 20),
     (-110, 24), (-114, 29), (-120, 34), (-124, 40), (-124, 48), (-130, 55),
     (-145, 60), (-158, 58), (-168, 66)],
    # Greenland
    [(-55, 60), (-45, 60), (-40, 65), (-30, 68), (-20, 70), (-25, 76),
     (-40, 80), (-55, 76), (-58, 70), (-55, 60)],
    # South America
    [(-79, 9), (-72, 12), (-62, 11), (-55, 6), (-52, 4), (-50, 0),
     (-44, -3), (-38, -5), (-35, -9), (-35, -15), (-40, -22), (-48, -28),
     (-55, -35), (-62, -41), (-66, -47), (-68, -52), (-70, -54), (-73, -50),
     (-73, -40), (-72, -30), (-70, -20), (-75, -15), (-80, -6), (-81, 0),
     (-80, 5), (-79, 9)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-1, 49), (2, 51),
     (5, 53), (8, 55), (10, 57), (12, 56), (18, 56), (21, 55), (24, 58),
     (28, 60), (30, 62), (32, 60), (30, 55), (28, 50), (24, 45), (22, 40),
     (19, 42), (15, 44), (12, 44), (8, 44), (3, 43), (0, 39), (-2, 37),
     (-6, 36), (-10, 36)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (-2, 51),
     (-5, 50)],
    # Africa
    [(-17, 15), (-16, 21), (-10, 29), (-5, 32), (0, 36), (10, 37),
     (20, 32), (25, 32), (30, 31), (32, 28), (34, 28), (37, 22), (39, 18),
     (43, 12), (48, 11), (51, 12), (46, 5), (42, 0), (40, -5), (38, -12),
     (36, -18), (33, -26), (28, -33), (20, -35), (17, -32), (15, -27),
     (13, -20), (12, -12), (12, -6), (9, 0), (9, 4), (4, 6), (-3, 5),
     (-8, 5), (-13, 8), (-17, 12), (-17, 15)],
    # Asia
    [(30, 62), (35, 65), (40, 68), (50, 69), (60, 69), (70, 72), (80, 73),
     (90, 75), (100, 77), (110, 74), (120, 73), (130, 72), (140, 72),
     (150, 70), (158, 66), (162, 60), (160, 58), (156, 52), (150, 59),
     (142, 55), (140, 50), (135, 45), (130, 42), (127, 40), (122, 39),
     (120, 35), (118, 30), (115, 23), (110, 20), (108, 12), (105, 9),
     (103, 7), (100, 6), (98, 10), (95, 16), (92, 21), (89, 22), (86, 20),
     (82, 17), (80, 13), (77, 8), (75, 10), (72, 20), (68, 23), (65, 25),
     (61, 25), (58, 26), (55, 26), (52, 28), (50, 29), (48, 30), (45, 29),
     (42, 29), (40, 32), (38, 36), (36, 36), (33, 38), (30, 41), (28, 45),
     (27, 50), (26, 55), (28, 60), (30, 62)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (137, 35), (140, 36), (141, 39),
     (141, 42), (140, 44), (143, 42), (142, 39), (140, 35), (137, 34),
     (134, 33), (131, 31)],
    # Australia
    [(113, -22), (114, -30), (115, -33), (118, -35), (124, -33), (129, -32),
     (132, -32), (136, -35), (138, -35), (140, -38), (145, -38), (147, -39),
     (150, -37), (153, -32), (153, -27), (150, -23), (146, -19), (142, -11),
     (140, -17), (136, -15), (132, -12), (128, -14), (124, -17), (120, -20),
     (115, -21), (113, -22)],
    # Sumatra / Borneo / Java / New Guinea (small)
    [(95, 5), (100, 0), (104, -3), (106, -6), (104, -5), (100, 2), (95, 5)],
    [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (113, -4),
     (110, -2), (109, 1)],
    [(105, -6), (110, -7), (114, -8), (114, -7), (108, -6), (105, -6)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (147, -8), (141, -8),
     (136, -7), (131, -3), (131, -1)],
]

# (lon, lat, label number, circle offset dx, dy) — offsets hand-tuned so the
# numbered circles never collide at this scale.
PINS = [
    (-95, 39, "1", 0, -14),    # USA — Nvidia / markets
    (20, 32, "2", -16, 12),    # Benghazi, Libya — warship sunk
    (30, 37, "3", 16, -10),    # Antalya, Turkey — COP31
    (106, -6, "4", 0, -14),    # Serang, Indonesia — factory fire
    (31, 50, "5", -16, -12),   # Kyiv, Ukraine
    (4, 51, "6", -14, 10),     # Brussels, Belgium — strike
    (127, 38, "7", 14, -12),   # Seoul, South Korea — Kospi
]


def draw_map(d, x0, y0, w, h):
    """Stylised dark-navy world map with numbered red pins."""
    lon0, lon1 = -170, 192
    lat0, lat1 = 82, -56

    def proj(lon, lat):
        return (x0 + (lon - lon0) / (lon1 - lon0) * w,
                y0 + (lat0 - lat) / (lat0 - lat1) * h)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=MAP_NAVY)
    for lon, lat, num, dx, dy in PINS:
        px, py = proj(lon, lat)
        cx, cy = px + dx, py + dy
        # leader line from the true spot to its number circle
        d.line([(px, py), (cx, cy)], fill=RED, width=1)
        # dot at the true spot
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED,
                  outline=(255, 255, 255))
        # numbered circle
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED,
                  outline=(255, 255, 255))
        nf = F(SANS_B, 9)
        d.text((cx - d.textlength(num, font=nf) / 2, cy - 5),
               num, font=nf, fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------------- masthead ----------------
    d.text((M, 16), "MONDAY, 23 NOVEMBER 2026", font=F(SANS_B, 15), fill=INK)
    right = "ONE PAGE  ·  EVERY CONTINENT"
    d.text((W - M - d.textlength(right, font=F(SANS_B, 15)), 16),
           right, font=F(SANS_B, 15), fill=GREY)
    title = "THE WORLD TODAY"
    tf = F(SERIF_B, 54)
    d.text(((W - d.textlength(title, font=tf)) / 2, 34),
           title, font=tf, fill=INK)
    hline(d, M, W - M, 96, color=RED, width=3)
    hline(d, M, W - M, 101, color=INK, width=1)
    strap = "One day. Every continent. The news that mattered."
    sf = F(SERIF, 17)
    d.text(((W - d.textlength(strap, font=sf)) / 2, 108),
           strap, font=sf, fill=GREY)

    # ---------------- lead story ----------------
    y = 132
    kicker(d, M, y, "LEAD  ·  BUSINESS  ·  UNITED STATES", 14)
    d.text((M, y + 20), "HUANG RETURNS AS NVIDIA CEO",
           font=F(SERIF_B, 34), fill=INK)
    d.text((M, y + 66), "Shares +31% in a day as Wall Street roars back",
           font=F(SERIF, 21), fill=RED)
    para(d, M, y + 100,
         "Eleven days after resigning, Jensen Huang retook the helm of the "
         "chipmaker he co-founded 33 years ago \u2014 in what Reuters called "
         "one of the most extraordinary days in US market history.",
         F(SANS, 17), 700, 22)

    # red stat box on the right of the lead
    bx0, bx1 = 744, W - M
    by0, by1 = 132, 292
    d.rectangle([bx0, by0, bx1, by1], fill=RED)
    cx = (bx0 + bx1) / 2
    big = "+31%"
    bf = F(SANS_B, 46)
    d.text((cx - d.textlength(big, font=bf) / 2, by0 + 14),
           big, font=bf, fill=(255, 255, 255))
    for i, t in enumerate(["NVIDIA, MONDAY", "NASDAQ +6.5%",
                           "S&P 500 +4.7%", "DOW +3.0%"]):
        f = F(SANS_B, 15) if i else F(SANS_B, 14)
        d.text((cx - d.textlength(t, font=f) / 2, by0 + 70 + i * 22),
               t, font=f, fill=(255, 255, 255))
    hline(d, bx0 + 24, bx1 - 24, by0 + 64, color=(255, 255, 255), width=1)

    hline(d, M, W - M, 300)

    # ---------------- row 2: two stories ----------------
    y = 310
    colw = 472
    x2 = M + colw + 24
    vline(d, M + colw + 12, y, 452)
    kicker(d, M, y, "WAR  ·  UKRAINE / LIBYA")
    para(d, M, y + 20, "UKRAINE SINKS A RUSSIAN WARSHIP OFF LIBYA",
         F(SERIF_B, 26), colw, 31)
    para(d, M, y + 88,
         "Kyiv says seven naval drones sank the vessel at Benghazi \u2014 the "
         "war reaching the Mediterranean. A Russian cargo ship was also hit "
         "in the Baltic.",
         F(SANS, 15), colw, 19)
    kicker(d, x2, y, "CLIMATE  ·  ANTALYA, TURKEY")
    para(d, x2, y + 20, "COP31 COLLAPSES: NO DEAL ON FOSSIL FUELS",
         F(SERIF_B, 26), colw, 31)
    para(d, x2, y + 88,
         "After 50+ hours overtime, the longest climate talks in history "
         "ended with no pact \u2014 the first major breakdown since "
         "Copenhagen 2009.",
         F(SANS, 15), colw, 19)

    hline(d, M, W - M, 460)

    # ---------------- row 3: three cards ----------------
    y = 470
    c3 = 306
    xs = [M, M + c3 + 24, M + 2 * (c3 + 24)]
    vline(d, xs[1] - 12, y, 596)
    vline(d, xs[2] - 12, y, 596)
    cards = [
        ("INDONESIA  ·  SERANG, BANTEN",
         "FACTORY FIRE: 24 DEAD, ~30 STILL MISSING",
         "The blaze broke out on Saturday at a candy factory in Cikande. "
         "Rescuers still search the wreckage; the cause is probed \u2014 a "
         "faulty air conditioner is suspected."),
        ("WAR  ·  KYIV & KHARTOUM",
         "15 KILLED NEAR KYIV; UN SITE HIT IN SUDAN",
         "Russian strikes killed at least 15 around Kyiv; a boy was pulled "
         "alive from the rubble. Drones also hit homes and a UN building "
         "in Khartoum."),
        ("BELGIUM  ·  WASHINGTON  ·  SEOUL",
         "FLIGHTS GROUNDED IN BELGIUM; DEMS WIN 258",
         "Strike cancels all Brussels flights 07:00\u201321:00; Charleroi "
         "all day. Democrats take 258 House seats, most since 1992. "
         "Kospi -3.3%."),
    ]
    for x, (kick, head, body) in zip(xs, cards):
        kicker(d, x, y, kick, 12)
        para(d, x, y + 18, head, F(SERIF_B, 20), c3, 24)
        para(d, x, y + 70, body, F(SANS, 14), c3, 18)

    # ---------------- numbers band ----------------
    by0, by1 = 604, 668
    d.rectangle([M, by0, W - M, by1], fill=BAND)
    nums = [
        ("+31%", "NVIDIA, MONDAY"),
        ("+6.5%", "NASDAQ"),
        ("7", "NAVAL DRONES"),
        ("24", "DEAD IN SERANG"),
        ("4.0%", "EURO INFLATION"),
        ("-3.3%", "KOSPI SELLS OFF"),
    ]
    cell = CW / 6
    for i, (val, lab) in enumerate(nums):
        cx = M + cell * i + cell / 2
        vf = F(SANS_B, 27)
        d.text((cx - d.textlength(val, font=vf) / 2, by0 + 12),
               val, font=vf, fill=(246, 241, 227))
        lf = F(SANS_B, 11)
        d.text((cx - d.textlength(lab, font=lf) / 2, by0 + 48),
               lab, font=lf, fill=GOLD)
        if i:
            vline(d, M + cell * i, by0 + 12, by1 - 12, color=BAND_DIV)

    # ---------------- timeline + world map ----------------
    y = 676
    hline(d, M, W - M, y)
    # timeline, left column, stacked rows
    d.text((M, y + 6), "THE WEEKEND THAT LED HERE",
           font=F(SANS_B, 13), fill=INK)
    tl = [
        ("SAT 21 NOV", "Serang candy factory fire breaks out"),
        ("SUN 22 NOV", "Democrats reach 258 seats; COP31 collapses"),
        ("MON 23 NOV", "Huang returns; warship sunk off Libya"),
    ]
    for i, (dt, txt) in enumerate(tl):
        yy = y + 28 + i * 24
        d.text((M, yy), dt, font=F(SANS_B, 13), fill=RED)
        d.text((M + 96, yy), txt, font=F(SANS, 13), fill=INK)
    vline(d, 632, y + 6, 796)
    # world map, right column
    mx0, my0, mw, mh = 644, 714, 352, 82
    d.text((mx0, y + 6), "WHERE IT HAPPENED",
           font=F(SANS_B, 13), fill=INK)
    d.text((mx0, y + 22),
           "1 USA \u00b7 2 BENGHAZI \u00b7 3 ANTALYA \u00b7 4 SERANG \u00b7 5 KYIV \u00b7 6 BRUSSELS \u00b7 7 SEOUL",
           font=F(SANS, 9), fill=GREY)
    draw_map(d, mx0, my0, mw, mh)

    # ---------------- also on 23 november ----------------
    y = 804
    hline(d, M, W - M, y)
    d.text((M, y + 8), "ALSO ON 23 NOVEMBER",
           font=F(SANS_B, 15), fill=INK)
    reg = "AMERICAS  ·  EUROPE  ·  MIDDLE EAST  ·  ASIA-PACIFIC"
    d.text((W - M - d.textlength(reg, font=F(SANS_B, 12)), y + 10),
           reg, font=F(SANS_B, 12), fill=GREY)
    also = [
        ("EU sanctions, round 22",
         "New package targets Russian banks, crypto, sport."),
        ("US hits Iran shadow banks",
         "Treasury sanctions 20+ entities over covert finance."),
        ("EU\u2013Indonesia trade deal",
         "Signed Monday; most tariffs between them scrapped."),
        ("FBI probes database hack",
         "Apparent breach of the US police records system."),
        ("\u2018El Chapo Isidro\u2019 captured",
         "FBI top-10 fugitive arrested in Sinaloa, Mexico."),
        ("NHS trials AI screening",
         "AI to be tested in breast-cancer checks in Britain."),
        ("Drone attack in Cucuta",
         "Three hurt, one an infant; 60 homes damaged."),
        ("893 kg cocaine seized",
         "London police find drugs hidden in orange boxes."),
    ]
    ay = y + 34
    colw2 = (CW - 24) / 2
    for i, (lead, desc) in enumerate(also):
        col = i % 2
        row = i // 2
        x = M + col * (colw2 + 24)
        yy = ay + row * 38
        d.text((x, yy), lead, font=F(SANS_B, 15), fill=INK)
        d.text((x, yy + 19), desc, font=F(SANS, 14), fill=(60, 58, 50))

    # ---------------- footer ----------------
    hline(d, M, W - M, 1000)
    foot = "Sources: Reuters \u00b7 AP \u00b7 CNN \u00b7 BBC \u00b7 WSJ \u00b7 Dow Jones \u00b7 The Guardian \u00b7 Yonhap \u00b7 Korea JoongAng Daily \u2014 23 November 2026"
    d.text((M, 1006), foot, font=F(SANS, 12), fill=GREY)
    tag = "make.fun \u00b7 news-image-20261123"
    d.text((W - M - d.textlength(tag, font=F(SANS, 12)), 1006),
           tag, font=F(SANS, 12), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
