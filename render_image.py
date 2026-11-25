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


def draw_medical(draw, box):
    """A white cross in a red roundel, with a map pin for the place."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = min(x1 - x0, y1 - y0) // 2 - 12
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    w = r // 3
    draw.rectangle([cx - w // 2, cy - r + 16, cx + w // 2, cy + r - 16], fill=(255, 255, 255))
    draw.rectangle([cx - r + 16, cy - w // 2, cx + r - 16, cy + w // 2], fill=(255, 255, 255))


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


def draw_mercury(draw, box):
    """A grey cratered planet and the little probe that reached it."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(10, 12, 26))
    for sx, sy in [(16, 12), (64, 30), (104, 8), (36, 62), (150, 52), (88, 74)]:
        if x0 + sx < x1 - 6 and y0 + sy < y1 - 6:
            draw.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3], fill=(230, 232, 240))
    r = min(46, (y1 - y0) // 2 - 4)
    cx, cy = x0 + r + 8, (y0 + y1) // 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 164, 158))
    for dx, dy, dr in [(-r // 3, -r // 4, r // 5), (r // 4, r // 8, r // 4), (-r // 8, r // 3, r // 6), (r // 3, -r // 3, r // 7)]:
        draw.ellipse([cx + dx - dr, cy + dy - dr, cx + dx + dr, cy + dy + dr], outline=(128, 124, 118), width=3)
    px, py = x1 - 44, y0 + (y1 - y0) // 3
    draw.rectangle([px - 8, py - 8, px + 8, py + 8], fill=(222, 200, 130))
    draw.rectangle([px - 34, py - 6, px - 11, py + 6], fill=(64, 116, 190))
    draw.rectangle([px + 11, py - 6, px + 34, py + 6], fill=(64, 116, 190))
    draw.line([px, py + 8, px - 12, py + 24], fill=(200, 200, 200), width=3)


# --- the page -----------------------------------------------------------------
# Layout, top to bottom: the masthead naming the day, the lead story's band,
# three panels in a row (art above the words), two wide panels (art at the
# left), and a dark ticker of three shorter items along the foot. Captions are
# kept short on purpose: the picture must still read at 300 pixels across.

STORIES = {
    'lead': {
        'kicker': 'MIDDLE EAST · STRAIT OF HORMUZ',
        'headline': 'Hormuz Crisis Deepens as Iran Warns Shipping',
        'body': 'Tankers were hit by mines in the strait. Iran ruled out talks with '
                'the US unless seven conditions are met. A Houthi attack on '
                'Riyadh injured 11 people.',
        'art': draw_tanker,
    },
    'panels': [
        {
            'kicker': 'US · TECH VERDICT',
            'headline': 'Huawei Guilty of Stealing Trade Secrets',
            'body': 'Guilty on 10 of 12 counts in the New York trial.',
            'art': draw_chip,
        },
        {
            'kicker': 'CLIMATE · ANTALYA',
            'headline': 'COP31 Ends Without a Deal',
            'body': 'Oil and gas states blocked the phaseout text.',
            'art': draw_globe_thermometer,
        },
        {
            'kicker': 'AFRICA · HEALTH',
            'headline': 'WHO Evacuates Ebola Staff in Congo',
            'body': 'Evacuated from an Ituri hospital amid fighting.',
            'art': draw_medical,
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
            'kicker': 'SCIENCE · SPACE',
            'headline': 'Europe–Japan Probe Reaches Mercury',
            'body': 'BepiColombo arrives after an eight-year journey.',
            'art': draw_mercury,
        },
    ],
    'ticker': [
        'SENEGAL REGAIN AFRICA CUP TITLE IN COURT RULING',
        'CIA & ODNI HIT BY CYBERATTACK',
        'INDONESIA VP GIBRAN RESIGNS',
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
    y = text_block(draw, (tx, y0 + 36), story['headline'], font(SERIF_BOLD, 25), INK, x1 - tx - 14, 1.1)
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
    while draw.textlength(ticker, font=font(SANS_BOLD, size)) > W - 110 and size > 12:
        size -= 1
    draw.text((512, 986), ticker, font=font(SANS_BOLD, size), fill=(246, 239, 220), anchor='ma')

    img.save('entry.png')
    print('wrote entry.png', img.size)


if __name__ == '__main__':
    main()
