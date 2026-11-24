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
        ("SCIENCE  ·  MATH & SPACE",
         "AI \u2018PROVES\u2019 RIEMANN; PROBE AT MERCURY",
         "Anthropic says AI helped prove the Riemann hypothesis \u2014 but "
         "can humans verify the proof? BepiColombo entered Mercury orbit "
         "after 8 years."),
    ]
    for x, (kick, head, body) in zip(xs, cards):
        kicker(d, x, y, kick, 12)
        para(d, x, y + 18, head, F(SERIF_B, 20), c3, 24)
        para(d, x, y + 70, body, F(SANS, 14), c3, 18)

    # ---------------- numbers band ----------------
    by0, by1 = 608, 684
    d.rectangle([M, by0, W - M, by1], fill=BAND)
    nums = [
        ("+31%", "NVIDIA, MONDAY"),
        ("+6.5%", "NASDAQ"),
        ("7", "NAVAL DRONES"),
        ("24", "DEAD IN SERANG"),
        ("4.0%", "EURO INFLATION"),
        ("$61K", "BITCOIN REBOUNDS"),
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

    # ---------------- timeline ----------------
    y = 692
    hline(d, M, W - M, y)
    d.text((M, y + 8), "THE WEEKEND THAT LED HERE",
           font=F(SANS_B, 13), fill=INK)
    ty = y + 28
    tcell = CW / 3
    timeline = [
        ("SAT 21 NOV", "Fire breaks out at the Serang candy factory"),
        ("SUN 22 NOV", "COP31 collapses in Antalya, no deal"),
        ("MON 23 NOV", "Huang returns; warship sunk off Libya"),
    ]
    for i, (dt, txt) in enumerate(timeline):
        x = M + tcell * i
        d.text((x, ty), dt, font=F(SANS_B, 13), fill=RED)
        para(d, x, ty + 18, txt, F(SANS, 13), tcell - 16, 16)
        if i:
            vline(d, x - 10, ty, ty + 34)

    # ---------------- also on 23 november ----------------
    y = 776
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
        ("Belgium flights grounded",
         "Austerity strike halts departures nationwide."),
        ("Drone attack in Cucuta",
         "Three hurt, one an infant; 60 homes damaged."),
        ("893 kg cocaine seized",
         "London police find drugs hidden in orange boxes."),
        ("Skubal\u2019s $450M deal",
         "Nine years with the Mets, a record for a pitcher."),
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
    foot = "Sources: Reuters \u00b7 AP \u00b7 CNN \u00b7 BBC \u00b7 WSJ \u00b7 Dow Jones \u00b7 The Guardian \u2014 23 November 2026"
    d.text((M, 1006), foot, font=F(SANS, 12), fill=GREY)
    tag = "make.fun \u00b7 news-image-20261123"
    d.text((W - M - d.textlength(tag, font=F(SANS, 12)), 1006),
           tag, font=F(SANS, 12), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
