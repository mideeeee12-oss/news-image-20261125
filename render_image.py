# The World in One Picture — 25 November 2026: the local tool that draws the
# entry image. It renders a one-page newspaper of the day at 1024x1024 with
# Pillow and the system fonts, and writes entry.png beside this file. The
# program that runs on make.fun (main.py) only copies entry.png to the output;
# this renderer is kept in the repository so the picture's making is on record.
#
# Stories are the day's reporting as gathered on 25-26 November 2026 from the
# news services named in README.md; the layout names the day in the masthead,
# gives the lead story the top band, five more stories panels of their own,
# and three short items in the ticker along the foot.

from PIL import Image, ImageDraw, ImageFont

W = 1024
PAPER = (246, 239, 220)
CARD = (255, 253, 244)
INK = (28, 26, 23)
RED = (179, 53, 43)
NAVY = (23, 56, 74)
GOLD = (201, 147, 43)
GREY = (96, 92, 84)
SEA = (64, 116, 148)
SAND = (214, 183, 128)

FONT_DIR = '/usr/share/fonts/truetype'
SERIF_BLACK = f'{FONT_DIR}/noto/NotoSerif-Black.ttf'
SERIF_BOLD = f'{FONT_DIR}/noto/NotoSerif-Bold.ttf'
SANS_BOLD = f'{FONT_DIR}/noto/NotoSans-Bold.ttf'
SANS_BLACK = f'{FONT_DIR}/noto/NotoSans-Black.ttf'
SANS = f'{FONT_DIR}/noto/NotoSans-Regular.ttf'


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns the list of lines."""
    lines, line = [], ''
    for word in text.split():
        trial = f'{line} {word}'.strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def text_block(draw, xy, text, fnt, fill, width, leading=1.18, align='left'):
    """Draw wrapped text; returns the y just below the block."""
    x, y = xy
    size = fnt.size
    for line in wrap(draw, text, fnt, width):
        lx = x if align == 'left' else x + (width - draw.textlength(line, font=fnt)) / 2
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += size * leading
    return y


# --- small flat illustrations, one per story ---------------------------------

def draw_tanker(draw, box):
    """A tanker crossing a strait between two headlands, under a low sun."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(168, 205, 226))
    draw.ellipse([x1 - 92, y0 + 14, x1 - 30, y0 + 76], fill=(244, 190, 82))
    draw.polygon([(x0, y1 - 58), (x0 + 120, y1 - 96), (x0 + 150, y1), (x0, y1)], fill=SAND)
    draw.polygon([(x1, y1 - 44), (x1 - 104, y1 - 84), (x1 - 128, y1), (x1, y1)], fill=SAND)
    draw.rectangle([x0, y1 - 52, x1, y1], fill=SEA)
    for wy in range(y1 - 44, y1 - 4, 12):
        for wx in range(x0 + 8, x1 - 30, 46):
            draw.arc([wx, wy, wx + 26, wy + 9], 0, 180, fill=(214, 234, 246), width=3)
    hx, hy = x0 + (x1 - x0) // 2, y1 - 66
    draw.polygon([(hx - 108, hy), (hx + 108, hy), (hx + 82, hy + 22), (hx - 82, hy + 22)], fill=(38, 42, 48))
    draw.rectangle([hx - 96, hy - 20, hx + 60, hy], fill=(179, 53, 43))
    for i, colour in enumerate([(64, 116, 148), (201, 147, 43), (90, 140, 90), (120, 90, 160)]):
        draw.rectangle([hx - 88 + i * 34, hy - 38, hx - 60 + i * 34, hy - 20], fill=colour)
    draw.rectangle([hx + 66, hy - 46, hx + 92, hy], fill=(240, 236, 224))
    draw.rectangle([hx + 72, hy - 40, hx + 86, hy - 28], fill=NAVY)


def draw_chip(draw, box):
    """A microchip with a verdict gavel resting on it."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    s = min(x1 - x0, y1 - y0) // 2 - 18
    for i in range(-2, 3):
        off = i * s // 3
        draw.line([cx - s - 10, cy + off, cx - s, cy + off], fill=GREY, width=5)
        draw.line([cx + s, cy + off, cx + s + 10, cy + off], fill=GREY, width=5)
        draw.line([cx + off, cy - s - 10, cx + off, cy - s], fill=GREY, width=5)
        draw.line([cx + off, cy + s, cx + off, cy + s + 10], fill=GREY, width=5)
    draw.rounded_rectangle([cx - s, cy - s, cx + s, cy + s], 8, fill=NAVY)
    draw.rounded_rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2], 5, outline=GOLD, width=4)
    draw.line([cx + 2, cy + s + 12, cx + 40, cy + 2], fill=(122, 79, 34), width=9)
    draw.rounded_rectangle([cx + 30, cy - 16, cx + 64, cy + 4], 5, fill=(160, 104, 44))


def draw_globe_thermometer(draw, box):
    """A globe with a thermometer beside it: the climate talks."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2 - 12, (y0 + y1) // 2
    r = min(x1 - x0, y1 - y0) // 2 - 8
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(104, 168, 205))
    draw.ellipse([cx - r // 2, cy - r // 2 - 4, cx - r // 6, cy - r // 6], fill=(90, 150, 96))
    draw.ellipse([cx + r // 8, cy + r // 10, cx + r // 2, cy + r // 2], fill=(90, 150, 96))
    draw.ellipse([cx - r // 3, cy + r // 3, cx, cy + r // 2 + 3], fill=(90, 150, 96))
    tx = cx + r + 5
    draw.rounded_rectangle([tx, cy - r, tx + 15, cy + r - 13], 7, outline=INK, width=3, fill=(255, 253, 244))
    draw.rectangle([tx + 4, cy - r // 4, tx + 11, cy + r - 17], fill=RED)
    draw.ellipse([tx - 5, cy + r - 27, tx + 20, cy + r - 2], fill=RED)


def draw_warship(draw, box):
    """A grey warship on a dark sea, and the drone that found it."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(38, 54, 74))
    sea_y = y1 - 16
    draw.rectangle([x0, sea_y, x1, y1], fill=(24, 40, 58))
    hx, hy = (x0 + x1) // 2, sea_y - 4
    draw.polygon([(hx - 62, hy), (hx + 62, hy), (hx + 44, hy + 10), (hx - 44, hy + 10)], fill=(96, 104, 116))
    draw.rectangle([hx - 34, hy - 14, hx + 20, hy], fill=(120, 128, 140))
    draw.rectangle([hx - 6, hy - 26, hx + 8, hy - 14], fill=(120, 128, 140))
    draw.line([hx + 1, hy - 26, hx + 1, hy - 38], fill=(160, 166, 176), width=3)
    draw.line([hx - 30, hy - 10, hx - 52, hy - 16], fill=(70, 76, 86), width=5)
    dx, dy = x0 + 34, y0 + 14
    draw.line([dx - 10, dy - 6, dx + 10, dy + 6], fill=(220, 224, 230), width=4)
    draw.line([dx - 10, dy + 6, dx + 10, dy - 6], fill=(220, 224, 230), width=4)
    draw.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=RED)
    for wx in range(x0 + 6, x1 - 20, 34):
        draw.arc([wx, sea_y + 3, wx + 20, sea_y + 11], 0, 180, fill=(120, 160, 190), width=2)


def draw_shanghai(draw, box):
    """The Shanghai skyline: a pearl tower between two towers, at dusk."""
    x0, y0, x1, y1 = box
    h = y1 - y0
    draw.rectangle(box, fill=(58, 62, 96))
    draw.ellipse([x0 + 10, y0 + 6, x0 + 34, y0 + 30], fill=(240, 226, 170))
    base = y1 - 4
    draw.rectangle([x0 + 10, base - h // 3, x0 + 34, base], fill=(24, 26, 40))
    draw.rectangle([x1 - 36, base - (h * 5) // 12, x1 - 12, base], fill=(24, 26, 40))
    tx = (x0 + x1) // 2
    draw.line([tx - 9, base, tx - 3, base - h // 3], fill=(24, 26, 40), width=5)
    draw.line([tx + 9, base, tx + 3, base - h // 3], fill=(24, 26, 40), width=5)
    r1 = max(7, h // 9)
    draw.ellipse([tx - r1, base - h // 3 - 2 * r1 + 4, tx + r1, base - h // 3 + 4], fill=(214, 92, 120))
    r2 = max(5, h // 13)
    top = base - h // 3 - 2 * r1 - 2 * r2 + 6
    draw.ellipse([tx - r2, top, tx + r2, top + 2 * r2], fill=(214, 92, 120))
    draw.line([tx, top, tx, max(y0 + 2, top - h // 10)], fill=(24, 26, 40), width=3)
    for wx in range(x0 + 14, x1 - 16, 13):
        for wy in range(base - (h * 5) // 12 + 6, base - 8, 13):
            if (wx * 7 + wy * 13) % 3:
                draw.rectangle([wx, wy, wx + 4, wy + 5], fill=(250, 214, 120))
    draw.rectangle([x0, base, x1, y1], fill=(16, 18, 30))


def draw_rocket(draw, box):
    """A rocket lifting off into a starry sky, on a plume of fire."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(12, 16, 36))
    for sx, sy in [(14, 10), (52, 26), (96, 8), (30, 52), (104, 44), (66, 66)]:
        if x0 + sx < x1 - 4 and y0 + sy < y1 - 40:
            draw.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3], fill=(230, 232, 240))
    cx = (x0 + x1) // 2
    top, base = y0 + 10, y1 - 34
    draw.polygon([(cx - 13, base), (cx - 13, top + 16), (cx, top), (cx + 13, top + 16), (cx + 13, base)], fill=(238, 236, 228))
    draw.rectangle([cx - 13, base - 12, cx + 13, base - 4], fill=RED)
    draw.ellipse([cx - 5, top + 20, cx + 5, top + 30], fill=NAVY)
    draw.polygon([(cx - 13, base - 8), (cx - 24, base + 8), (cx - 13, base + 6)], fill=(150, 156, 168))
    draw.polygon([(cx + 13, base - 8), (cx + 24, base + 8), (cx + 13, base + 6)], fill=(150, 156, 168))
    draw.polygon([(cx - 8, base), (cx, base + 22), (cx + 8, base)], fill=(244, 160, 60))
    draw.polygon([(cx - 4, base), (cx, base + 13), (cx + 4, base)], fill=(250, 214, 120))
    for dx, r in [(-30, 12), (-12, 15), (10, 16), (28, 11)]:
        draw.ellipse([cx + dx - r, y1 - 18 - r // 2, cx + dx + r, y1 - 18 + r // 2], fill=(214, 216, 220))
    draw.rectangle([x0, y1 - 6, x1, y1], fill=(8, 10, 22))


# --- the page -----------------------------------------------------------------
# Layout, top to bottom: the masthead naming the day, the lead story's band,
# three panels in a row (art above the words), two wide panels (art at the
# left), and a dark ticker of three shorter items along the foot. Captions are
# kept short on purpose: the picture must still read at 300 pixels across.

STORIES = {
    'lead': {
        'kicker': 'MIDDLE EAST · STRAIT OF HORMUZ',
        'headline': 'Hormuz Crisis Deepens as Iran Warns Shipping',
        'body': 'Iran says mines hit four tankers in the strait; the US disputes '
                'the claim. A Houthi attack on a Riyadh tower injured 11, '
                'and talks with Washington are ruled out.',
        'art': draw_tanker,
    },
    'panels': [
        {
            'kicker': 'US · TECH VERDICT',
            'headline': 'Huawei Guilty of Stealing Trade Secrets',
            'body': 'Convicted of conspiracy in New York; cleared of racketeering.',
            'art': draw_chip,
        },
        {
            'kicker': 'CLIMATE · ANTALYA',
            'headline': 'COP31 Ends Without a Deal',
            'body': 'Oil and gas states blocked the phaseout text.',
            'art': draw_globe_thermometer,
        },
        {
            'kicker': 'EUROPE · WAR AT SEA',
            'headline': 'Ukraine Drones Sink Russian Warship in Libya',
            'body': 'Kyiv’s drones hit Russian ships from the Baltic to Benghazi.',
            'art': draw_warship,
        },
    ],
    'wide': [
        {
            'kicker': 'CHINA · POLITICS',
            'headline': 'Beijing Probes a Politburo Member',
            'body': 'A rare graft case against Shanghai chief Chen Jining.',
            'art': draw_shanghai,
        },
        {
            'kicker': 'ASIA · SPACE',
            'headline': 'Pakistan’s First Astronaut in Orbit',
            'body': 'Shenzhou-24 takes Muhammad Zeeshan Ali to space.',
            'art': draw_rocket,
        },
    ],
    'ticker': [
        'SENEGAL REGAIN AFRICA CUP TITLE IN COURT RULING',
        'WHO EVACUATES EBOLA STAFF IN CONGO',
        'COLOMBIA FREES SUPERMARKET HOSTAGES',
    ],
}


def row_panel(draw, box, story):
    """A panel with its picture as a banner above the words."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, 6, fill=CARD, outline=INK, width=2)
    draw.text((x0 + 14, y0 + 10), story['kicker'], font=font(SANS_BOLD, 16), fill=RED)
    story['art'](draw, (x0 + 14, y0 + 34, x1 - 14, y0 + 104))
    y = text_block(draw, (x0 + 14, y0 + 112), story['headline'], font(SERIF_BOLD, 24), INK, x1 - x0 - 28, 1.1)
    text_block(draw, (x0 + 14, y + 6), story['body'], font(SANS, 17), (52, 49, 44), x1 - x0 - 28, 1.2)


def wide_panel(draw, box, story):
    """A panel with its picture at the left and the words beside it."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, 6, fill=CARD, outline=INK, width=2)
    story['art'](draw, (x0 + 14, y0 + 14, x0 + 134, y1 - 14))
    tx = x0 + 162
    draw.text((tx, y0 + 12), story['kicker'], font=font(SANS_BOLD, 16), fill=RED)
    y = text_block(draw, (tx, y0 + 36), story['headline'], font(SERIF_BOLD, 23), INK, x1 - tx - 14, 1.1)
    text_block(draw, (tx, y + 6), story['body'], font(SANS, 18), (52, 49, 44), x1 - tx - 14, 1.2)


def main():
    img = Image.new('RGB', (W, W), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, W - 10, W - 10], outline=INK, width=3)

    # Masthead: the day, named as large as the page allows.
    draw.text((512, 32), 'THE WORLD IN ONE PICTURE', font=font(SANS_BOLD, 25), fill=NAVY, anchor='ma')
    draw.text((512, 62), 'WEDNESDAY', font=font(SERIF_BLACK, 96), fill=INK, anchor='ma')
    draw.text((512, 164), '25 NOVEMBER 2026', font=font(SERIF_BLACK, 84), fill=RED, anchor='ma')
    draw.line([36, 262, W - 36, 262], fill=INK, width=4)
    draw.line([36, 270, W - 36, 270], fill=INK, width=1)

    # The lead story.
    lead = STORIES['lead']
    draw.rounded_rectangle([36, 286, W - 36, 544], 6, fill=CARD, outline=INK, width=2)
    draw.text((56, 300), lead['kicker'], font=font(SANS_BOLD, 19), fill=RED)
    lead['art'](draw, (56, 336, 420, 502))
    y = text_block(draw, (448, 300), lead['headline'], font(SERIF_BOLD, 44), INK, W - 448 - 56, 1.08)
    text_block(draw, (448, y + 12), lead['body'], font(SANS, 21), (52, 49, 44), W - 448 - 56, 1.25)

    # Three panels in a row.
    for i, story in enumerate(STORIES['panels']):
        x0 = 36 + i * 322
        row_panel(draw, (x0, 560, x0 + 306, 804), story)

    # Two wide panels.
    for i, story in enumerate(STORIES['wide']):
        x0 = 36 + i * 483
        wide_panel(draw, (x0, 820, x0 + 467, 968), story)

    # The ticker along the foot.
    draw.rectangle([36, 980, W - 36, 1012], fill=NAVY)
    ticker = 'ALSO TODAY   •   ' + '    •    '.join(STORIES['ticker'])
    size = 19
    while draw.textlength(ticker, font=font(SANS_BOLD, size)) > W - 76 and size > 10:
        size -= 1
    draw.text((512, 986), ticker, font=font(SANS_BOLD, size), fill=(246, 239, 220), anchor='ma')

    img.save('entry.png')
    print('wrote entry.png', img.size)


if __name__ == '__main__':
    main()
