"""
Generate Swahili edition cover — Kujua Bitcoin.
East African / Swahili kanga-inspired design with giraffe motif.
"""
from PIL import Image, ImageDraw, ImageFont
import os, math

W, H = 2100, 2756
FONT_DIR = r"C:/Windows/Fonts"

# ── Palette ───────────────────────────────────────────────────────────────────
BG_TOP       = (255, 250, 228)
BG_MID       = (255, 238, 190)
BG_BOT       = (250, 220, 155)
GIRAFFE_BODY = (212, 135, 38)
GIRAFFE_SPOT = (58,  25,   3)
GIRAFFE_OUT  = (42,  16,   2)
BORDER_RED   = (176,  30,  10)
BORDER_DARK  = (40,   16,   3)
BORDER_CREAM = (255, 248, 220)
SUN_OUTER    = (255, 200, 80)
SUN_INNER    = (255, 228, 140)
TITLE_COL    = (28,   12,   2)
SUBTITLE_COL = (88,   40,   8)
FOOTER_BG    = (40,   16,   3)
FOOTER_TEXT  = (255, 232, 168)
ACCENT_RED   = (176,  30,  10)

# ── Canvas with gradient ──────────────────────────────────────────────────────
img = Image.new("RGB", (W, H))
pix = img.load()
for y in range(H):
    t = y / H
    if t < 0.55:
        s = t / 0.55
        col = tuple(int(BG_TOP[i] + s * (BG_MID[i] - BG_TOP[i])) for i in range(3))
    else:
        s = (t - 0.55) / 0.45
        col = tuple(int(BG_MID[i] + s * (BG_BOT[i] - BG_MID[i])) for i in range(3))
    for x in range(W):
        pix[x, y] = col

draw = ImageDraw.Draw(img)

# ── African sun (background, upper-right) ─────────────────────────────────────
SUN_CX, SUN_CY, SUN_R = 1680, 820, 540
for r in range(SUN_R, 0, -1):
    t = r / SUN_R
    col = tuple(int(SUN_INNER[i] + t * (SUN_OUTER[i] - SUN_INNER[i])) for i in range(3))
    draw.ellipse([SUN_CX - r, SUN_CY - r, SUN_CX + r, SUN_CY + r], fill=col)

# Sun rays
for angle_deg in range(0, 360, 22):
    a = math.radians(angle_deg)
    for delta in (-4, 0, 4):
        ad = a + math.radians(delta)
        x1 = int(SUN_CX + SUN_R * math.cos(ad))
        y1 = int(SUN_CY + SUN_R * math.sin(ad))
        x2 = int(SUN_CX + (SUN_R + 110) * math.cos(a))
        y2 = int(SUN_CY + (SUN_R + 110) * math.sin(a))
    draw.line([(SUN_CX + SUN_R, SUN_CY), (SUN_CX + SUN_R + 80, SUN_CY)], fill=SUN_OUTER, width=3)
for angle_deg in range(0, 360, 22):
    a = math.radians(angle_deg)
    x1 = int(SUN_CX + (SUN_R + 10) * math.cos(a))
    y1 = int(SUN_CY + (SUN_R + 10) * math.sin(a))
    x2 = int(SUN_CX + (SUN_R + 120) * math.cos(a))
    y2 = int(SUN_CY + (SUN_R + 120) * math.sin(a))
    draw.line([(x1, y1), (x2, y2)], fill=(230, 185, 60), width=18)

# ── Kanga border bands ─────────────────────────────────────────────────────────
BAND_H = 185
FOOTER_BAND_TOP = H - 305

def kanga_band(y0, y1, flip=False):
    mid = (y0 + y1) // 2
    tw = 148  # triangle width
    draw.rectangle([0, y0, W, y1], fill=BORDER_RED)
    # Row pointing inward from outer edge
    x = 0
    while x < W + tw:
        if not flip:
            draw.polygon([(x, y0), (x + tw, y0), (x + tw//2, mid)], fill=BORDER_CREAM)
        else:
            draw.polygon([(x, y1), (x + tw, y1), (x + tw//2, mid)], fill=BORDER_CREAM)
        x += tw
    # Row pointing inward from inner edge (dark)
    x = tw // 2
    while x < W + tw:
        if not flip:
            draw.polygon([(x, y1), (x + tw, y1), (x + tw//2, mid)], fill=BORDER_DARK)
        else:
            draw.polygon([(x, y0), (x + tw, y0), (x + tw//2, mid)], fill=BORDER_DARK)
        x += tw
    # Diamond row along centre
    for dx in range(tw // 2, W, tw):
        s = 20
        draw.polygon([(dx, mid - s), (dx + s, mid), (dx, mid + s), (dx - s, mid)],
                     fill=BORDER_CREAM)

kanga_band(0, BAND_H, flip=False)
kanga_band(FOOTER_BAND_TOP, H - 295, flip=True)

# ── Footer strip ──────────────────────────────────────────────────────────────
draw.rectangle([0, H - 295, W, H], fill=FOOTER_BG)

# ── Thin side stripes ─────────────────────────────────────────────────────────
sw = 34
for y in range(BAND_H, FOOTER_BAND_TOP, 84):
    for side in [(0, sw), (W - sw, W)]:
        draw.rectangle([side[0], y, side[1], y + 62], fill=BORDER_RED)
        draw.rectangle([side[0], y + 62, side[1], y + 84], fill=BORDER_DARK)

# ── Giraffe silhouette ─────────────────────────────────────────────────────────
# Positioned on the RIGHT side of the canvas.
GX = 295   # global horizontal shift for all giraffe elements

def gp(pts, fill=GIRAFFE_BODY, outline=GIRAFFE_OUT):
    draw.polygon([(x + GX, y) for x, y in pts], fill=fill, outline=outline)

def ge(x0, y0, x1, y1, fill=GIRAFFE_BODY):
    draw.ellipse([x0 + GX, y0, x1 + GX, y1], fill=fill, outline=GIRAFFE_OUT)

def gr(x0, y0, x1, y1, fill=GIRAFFE_BODY):
    draw.rectangle([x0 + GX, y0, x1 + GX, y1], fill=fill)

# Ossicones
gr(1390, 300, 1430, 430, fill=GIRAFFE_OUT)
gr(1458, 290, 1498, 428, fill=GIRAFFE_OUT)
ge(1378, 290, 1442, 318, fill=GIRAFFE_OUT)
ge(1446, 280, 1510, 308, fill=GIRAFFE_OUT)

# Head
ge(1300, 390, 1530, 565, fill=GIRAFFE_BODY)
# Jaw extension
gp([(1300, 490), (1300, 565), (1250, 560), (1220, 530), (1240, 490)])
# Eye
ge(1340, 420, 1382, 454, fill=GIRAFFE_OUT)
ge(1350, 430, 1372, 448, fill=(255, 240, 200))
# Nostril
ge(1218, 510, 1248, 536, fill=GIRAFFE_SPOT)
# Ear
gp([(1508, 420), (1565, 355), (1590, 440), (1545, 468)])
gr(1518, 432, 1570, 458, fill=(230, 170, 120))

# Neck (long trapezoid)
gp([(1315, 548),
    (1500, 548),
    (1700, 1260),
    (1470, 1265)])

# Mane bumps along right side of neck
for i in range(10):
    t = i / 9
    nx = int(1498 + t * 202) + GX
    ny = int(548 + t * 712)
    draw.ellipse([nx - 16, ny - 20, nx + 16, ny + 20], fill=GIRAFFE_SPOT)

# Body
ge(1160, 1200, 1860, 1900, fill=GIRAFFE_BODY)

# Belly underline
gp([(1200, 1840), (1850, 1840), (1820, 1900), (1230, 1900)])

# Tail
gp([(1816, 1460), (1862, 1448), (1880, 1590), (1868, 1640), (1828, 1580)])
ge(1836, 1620, 1900, 1680, fill=GIRAFFE_SPOT)

# Legs — front pair
gr(1242, 1858, 1318, 2460)
gr(1352, 1872, 1428, 2460)
# hooves
gr(1234, 2438, 1326, 2490, fill=GIRAFFE_SPOT)
gr(1344, 2438, 1436, 2490, fill=GIRAFFE_SPOT)

# Rear pair
gr(1556, 1808, 1632, 2460)
gr(1660, 1800, 1736, 2460)
gr(1548, 2438, 1640, 2490, fill=GIRAFFE_SPOT)
gr(1652, 2438, 1744, 2490, fill=GIRAFFE_SPOT)

# Knee joints
for lx in [1248, 1358, 1562, 1666]:
    ge(lx, 2160, lx + 70, 2220, fill=GIRAFFE_SPOT)

# Giraffe shadow underfoot
for i in range(40):
    alpha = 1 - i / 40
    shade = int(210 - alpha * 55)
    draw.ellipse([1220 + GX, 2480 + i, 1810 + GX, 2510 + i],
                 fill=(shade, max(0, shade - 25), max(0, shade - 50)))

# --- Spots on neck ---
neck_spots = [
    [(1330,598),(1408,582),(1438,652),(1358,670)],
    [(1420,598),(1494,584),(1522,650),(1448,666)],
    [(1342,692),(1418,676),(1446,744),(1370,762)],
    [(1428,694),(1502,680),(1528,746),(1454,762)],
    [(1354,790),(1426,774),(1452,840),(1378,858)],
    [(1438,792),(1508,778),(1532,842),(1462,858)],
    [(1366,888),(1436,872),(1460,936),(1388,954)],
    [(1448,886),(1516,872),(1540,934),(1472,950)],
    [(1380,988),(1448,972),(1470,1034),(1400,1052)],
    [(1460,986),(1526,972),(1548,1032),(1482,1048)],
    [(1394,1084),(1460,1068),(1482,1128),(1414,1146)],
    [(1468,1082),(1532,1068),(1554,1126),(1490,1142)],
    [(1400,1180),(1464,1164),(1486,1224),(1422,1242)],
]
# --- Spots on body ---
body_spots = [
    [(1275,1290),(1378,1272),(1418,1372),(1312,1390)],
    [(1432,1278),(1542,1262),(1574,1360),(1462,1376)],
    [(1580,1266),(1678,1252),(1706,1346),(1598,1362)],
    [(1706,1262),(1794,1248),(1816,1338),(1724,1352)],
    [(1250,1408),(1354,1390),(1388,1486),(1282,1504)],
    [(1402,1396),(1506,1378),(1538,1472),(1432,1488)],
    [(1552,1384),(1648,1368),(1678,1460),(1580,1476)],
    [(1698,1380),(1784,1366),(1808,1454),(1718,1468)],
    [(1268,1522),(1368,1506),(1400,1596),(1296,1614)],
    [(1414,1510),(1512,1494),(1542,1582),(1446,1598)],
    [(1556,1500),(1648,1486),(1676,1572),(1582,1586)],
    [(1696,1494),(1776,1480),(1800,1562),(1714,1576)],
    [(1280,1630),(1376,1616),(1406,1700),(1308,1716)],
    [(1420,1618),(1516,1604),(1544,1686),(1448,1702)],
    [(1558,1608),(1646,1594),(1670,1674),(1580,1688)],
    [(1676,1600),(1756,1588),(1778,1664),(1692,1678)],
    [(1294,1732),(1386,1720),(1412,1798),(1318,1812)],
    [(1426,1720),(1516,1708),(1540,1782),(1452,1796)],
    [(1554,1710),(1636,1698),(1658,1770),(1572,1782)],
    [(1664,1702),(1740,1692),(1762,1760),(1680,1770)],
    [(1302,1828),(1390,1816),(1414,1880),(1324,1892)],
    [(1428,1818),(1512,1806),(1534,1870),(1450,1882)],
    [(1548,1808),(1626,1798),(1648,1860),(1564,1870)],
]
for spot in neck_spots + body_spots:
    shifted = [(x + GX, y) for x, y in spot]
    draw.polygon(shifted, fill=GIRAFFE_SPOT)

# ── Fonts ──────────────────────────────────────────────────────────────────────
def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

f_huge      = font("impact.ttf",        400)   # title (condensed, very bold)
f_sub       = font("Lato_Bold.ttf",     90)
f_pub       = font("Lato_Black.ttf",    72)
f_author    = font("Lato_Regular.ttf",  72)
f_trans     = font("Lato_Italic.ttf",   60)
f_badge     = font("Lato_BoldItalic.ttf", 60)

# ── Title block ────────────────────────────────────────────────────────────────
ML = 80   # left margin

# O'REILLY
draw.text((ML, BAND_H + 24), "O'REILLY", font=f_pub, fill=ACCENT_RED)
draw.rectangle([ML, BAND_H + 112, 540, BAND_H + 122], fill=ACCENT_RED)

# KUJUA
draw.text((ML, BAND_H + 132), "KUJUA", font=f_huge, fill=TITLE_COL)
# BITCOIN
draw.text((ML, BAND_H + 518), "BITCOIN", font=f_huge, fill=TITLE_COL)

# Subtitle
draw.text((ML, BAND_H + 932), "Kupanga Blockchain Wazi", font=f_sub, fill=SUBTITLE_COL)
draw.rectangle([ML, BAND_H + 1038, 860, BAND_H + 1052], fill=ACCENT_RED)

# ── Edition banner (left side, below subtitle) ────────────────────────────────
f_edition = font("Lato_BoldItalic.ttf", 58)
EB_Y = BAND_H + 1080
draw.rectangle([ML, EB_Y, ML + 710, EB_Y + 78], fill=BORDER_DARK)
draw.text((ML + 16, EB_Y + 10), "Toleo la Tatu  •  3rd Edition", font=f_edition,
          fill=FOOTER_TEXT)

# ── Footer ─────────────────────────────────────────────────────────────────────
FY = H - 290
draw.text((ML, FY + 6),
          "Andreas M. Antonopoulos", font=f_author, fill=FOOTER_TEXT)
draw.text((ML, FY + 88),
          "& David A. Harding", font=f_author, fill=FOOTER_TEXT)
draw.rectangle([ML, FY + 176, 680, FY + 186], fill=(190, 155, 75))
draw.text((ML, FY + 198),
          "Tafsiri ya Kiswahili na comwanga", font=f_trans, fill=(198, 172, 118))

# ── Save ───────────────────────────────────────────────────────────────────────
out_dir  = r"C:/Users/mwang/Desktop/bitcoinbook swahili/swahili/images"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "cover_swahili.png")
img.save(out_path)
print(f"Saved: {out_path}  ({W}×{H})")
