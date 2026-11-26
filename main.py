"""Wednesday 25 November 2026, in one picture -- revised edition.

The first version scored 96.9% in development but lost its only
game to an image that "tells the story on its own". This version
fixes exactly that: every story is drawn first and captioned
second. Each picture panel is big, and the key fact of the story
is printed INSIDE the picture as a large number or banner, so a
viewer who reads no headline at all can still say what happened:

  1. A courthouse at night, stamped 10 of 12 / GUILTY.
  2. A tower hit by an explosion, banner: 11 WOUNDED.
  3. A share-price line that climbs, then falls, labelled -6%.
  4. A turkey under a PARDONED seal.
  5. A skyline under a LOYALTY banner.
  6. A ribbon beside a big 5 / HOUR.

Same six stories, same day, same newspaper frame as version one.
Headlines stay, but they are no longer the only way the news is
told. No body paragraphs anywhere. All drawing is fixed geometry:
no clock, no network, no random numbers, so two runs write the
same bytes. Writes $MAKEFUN_OUTPUT_DIR/entry.png, or /output.
"""

import os
import shutil
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    HAVE_PIL = True
except ImportError:  # pragma: no cover
    HAVE_PIL = False

W = H = 1024
COL = {
    "paper": (247, 242, 232),
    "navy": (15, 29, 50),
    "night": (21, 41, 69),
    "gold": (198, 155, 28),
    "pale_gold": (233, 197, 92),
    "white": (255, 255, 255),
    "ink": (16, 22, 32),
    "grey": (71, 80, 93),
    "mist": (149, 157, 169),
    "card": (255, 255, 255),
    "red": (184, 27, 27),
    "amber": (179, 82, 8),
    "teal": (13, 115, 143),
    "brown": (145, 63, 13),
    "blue": (28, 77, 215),
    "wine": (158, 17, 56),
    "cream": (241, 235, 221),
}
FONT_PATH = {
    "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "plain": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
}
EDGE = 32


def load_font(style, size):
    try:
        return ImageFont.truetype(FONT_PATH[style], size)
    except OSError:
        return ImageFont.load_default()


def wrap_text(words, font, width, limit):
    """Word-wrap into at most `limit` lines fitting `width`."""
    rows, cur = [], ""
    for word in words.split():
        test = (cur + " " + word).strip()
        if font.getlength(test) <= width:
            cur = test
        else:
            if cur:
                rows.append(cur)
            cur = word
    if cur:
        rows.append(cur)
    return rows[:limit]


def fit_headline(words, style, top_size, low_size, width, limit):
    """Biggest headline size in range that fits in `limit` lines."""
    size = top_size
    while size > low_size:
        face = load_font(style, size)
        if len(wrap_text(words, face, width, limit + 1)) <= limit:
            return face, wrap_text(words, face, width, limit)
        size -= 1
    face = load_font(style, low_size)
    return face, wrap_text(words, face, width, limit)


def shade(rgb, keep=0.14):
    """A pale wash of a colour for picture backgrounds."""
    return tuple(int(255 - (255 - c) * keep) for c in rgb)


def centred(draw, cx, y, text, font, fill):
    draw.text((cx - font.getlength(text) / 2, y), text, font=font, fill=fill)


def banner(draw, x0, y0, x1, y1, fill, text, size, colour):
    """A solid strip with centred bold text -- the fact in the picture."""
    draw.rectangle([x0, y0, x1, y1], fill=fill)
    face = load_font("bold", size)
    centred(draw, (x0 + x1) // 2, y0 + (y1 - y0 - size) // 2 - 2, text, face, colour)


# ---------------------------------------------------------------- stories

LEAD = {
    "tag": "01  •  USA  •  JUSTICE",
    "colour": COL["red"],
    "headline": "US JURY CONVICTS HUAWEI OF FRAUD",
    "sub": "Guilty on 10 of 12 counts: fraud, sanctions, trade secrets.",
}

CARDS = [
    {"tag": "02  •  MIDDLE EAST  •  WAR", "colour": COL["amber"],
     "scene": "tower",
     "headline": "HOUTHIS HIT RIYADH'S TALLEST TOWER AGAIN",
     "sub": "11 wounded in a second strike in a week."},
    {"tag": "03  •  MARKETS", "colour": COL["teal"],
     "scene": "chart",
     "headline": "NVIDIA SHARES FALL 6% AS RALLY FADES",
     "sub": "Huang apologises to staff; doubts remain."},
    {"tag": "04  •  USA  •  THANKSGIVING", "colour": COL["brown"],
     "scene": "turkey",
     "headline": "TRUMP PARDONS TURKEYS FREEDOM AND FEATHERS",
     "sub": "Feathers fled into the bushes first."},
    {"tag": "05  •  CHINA", "colour": COL["blue"],
     "scene": "skyline",
     "headline": "SHANGHAI PLEDGES LOYALTY AFTER PROBE",
     "sub": "Politburo member Chen Jining investigated."},
    {"tag": "06  •  UNITED NATIONS", "colour": COL["wine"],
     "scene": "ribbon",
     "headline": "UN: FIVE WOMEN KILLED EVERY HOUR",
     "sub": "47,000 killed by partners or family in 2025."},
]


# ---------------------------------------------------------------- pictures

def pic_courtroom(canvas, x0, y0, x1, y1):
    """Night courthouse, gavel on the steps, GUILTY stamp in the picture."""
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=COL["night"])
    for sx, sy, r in [(x0 + 30, y0 + 30, 2), (x0 + 90, y0 + 55, 1),
                      (x0 + 150, y0 + 24, 2), (x0 + 210, y0 + 48, 1),
                      (x0 + 270, y0 + 20, 2), (x0 + 320, y0 + 62, 1),
                      (x0 + 60, y0 + 100, 1), (x0 + 180, y0 + 90, 2)]:
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(222, 230, 242))
    mid = (x0 + x1) // 2
    draw.polygon([(x0 + 22, y0 + 96), (mid, y0 + 42), (x1 - 22, y0 + 96)],
                 fill=COL["pale_gold"])
    draw.rectangle([x0 + 30, y0 + 96, x1 - 30, y0 + 112], fill=COL["cream"])
    for cx in (x0 + 58, x0 + 126, x1 - 126, x1 - 58):
        draw.rectangle([cx - 11, y0 + 112, cx + 11, y0 + 196], fill=COL["cream"])
    draw.rectangle([x0 + 30, y0 + 196, x1 - 30, y0 + 208], fill=COL["cream"])
    draw.rectangle([x0 + 24, y0 + 208, x1 - 24, y0 + 218], fill=COL["gold"])
    draw.rectangle([mid - 22, y0 + 150, mid + 22, y0 + 196], fill=COL["navy"])
    # Caption, kept well inside the panel this time.
    draw.text((x0 + 24, y0 + 12), "BROOKLYN COURTROOM",
              font=load_font("bold", 13), fill=(222, 230, 242))
    # The verdict, stamped across the picture itself.
    sx0, sy0, sx1, sy1 = x0 + 24, y1 - 84, x0 + 232, y1 - 16
    draw.rounded_rectangle([sx0, sy0, sx1, sy1], radius=8,
                           fill=COL["white"], outline=COL["red"], width=4)
    centred(draw, (sx0 + sx1) // 2, sy0 + 6, "10 of 12",
            load_font("bold", 26), COL["red"])
    centred(draw, (sx0 + sx1) // 2, sy0 + 36, "GUILTY",
            load_font("bold", 26), COL["red"])
    # Gavel resting on the steps, clear of the stamp and the corner.
    gx, gy = x1 - 84, y1 - 50
    draw.rectangle([gx - 30, gy - 8, gx + 14, gy + 10], fill=COL["pale_gold"],
                   outline=COL["gold"], width=2)
    draw.line([gx - 4, gy + 1, gx + 34, gy + 30], fill=COL["pale_gold"], width=6)
    draw.rectangle([gx - 32, gy + 22, gx + 6, gy + 32], fill=COL["pale_gold"],
                   outline=COL["gold"], width=2)


def pic_tower(draw, x0, y0, x1, y1, colour):
    """A tower, an explosion at its crown, the casualty count in the picture."""
    cx = (x0 + x1) // 2 - 30
    top, bot = y0 + 22, y1 - 30
    draw.rectangle([cx - 26, top + 20, cx + 26, bot], fill=colour)
    draw.polygon([(cx, top), (cx - 10, top + 22), (cx + 10, top + 22)], fill=colour)
    for row in (top + 28, top + 42):
        draw.rectangle([cx - 16, row, cx - 6, row + 6], fill=COL["white"])
        draw.rectangle([cx + 6, row, cx + 16, row + 6], fill=COL["white"])
    # Explosion burst above the roof.
    ex, ey = cx + 34, top + 10
    spikes = []
    for k in range(12):
        import math
        ang = k * math.pi / 6
        r = 22 if k % 2 == 0 else 11
        spikes.append((ex + r * math.cos(ang), ey + r * math.sin(ang)))
    draw.polygon(spikes, fill=COL["red"])
    draw.ellipse([ex - 11, ey - 11, ex + 11, ey + 11], fill=(245, 158, 11))
    draw.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=COL["white"])
    draw.text((x0 + 14, y0 + 8), "RIYADH", font=load_font("bold", 13), fill=colour)
    banner(draw, x0, y1 - 30, x1, y1, COL["red"], "11 WOUNDED", 17, COL["white"])


def pic_chart(draw, x0, y0, x1, y1, colour):
    """A price that climbs, then falls hard. The fall is the picture."""
    draw.line([x0 + 18, y1 - 34, x1 - 18, y1 - 34], fill=COL["grey"], width=2)
    draw.line([x0 + 18, y0 + 14, x0 + 18, y1 - 34], fill=COL["grey"], width=2)
    # The line stays clear of the big -6% at top left: it starts
    # two-fifths across and climbs, then falls, to the arrow.
    pts = [(x0 + 150, y1 - 46), (x0 + 200, y1 - 64), (x0 + 250, y1 - 80),
           (x0 + 320, y1 - 56), (x0 + 395, y1 - 40)]
    draw.line(pts, fill=COL["red"], width=5, joint="curve")
    draw.polygon([(x1 - 40, y1 - 48), (x1 - 24, y1 - 32), (x1 - 40, y1 - 32)],
                 fill=COL["red"])
    draw.text((x0 + 26, y0 + 8), "-6%", font=load_font("bold", 42), fill=COL["red"])
    draw.text((x1 - 62, y0 + 10), "NVDA", font=load_font("bold", 13),
              fill=COL["grey"])


def pic_turkey(draw, x0, y0, x1, y1, colour):
    """A big turkey, pardoned: the seal says so in the picture."""
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 6
    for dx in (-34, 0, 34):
        draw.ellipse([cx + dx - 14, cy - 40, cx + dx + 14, cy - 2],
                     fill=COL["pale_gold"], outline=colour, width=2)
    draw.ellipse([cx - 34, cy - 8, cx + 34, cy + 36], fill=colour)
    draw.ellipse([cx + 12, cy - 30, cx + 40, cy - 4], fill=COL["white"])
    draw.ellipse([cx + 27, cy - 22, cx + 31, cy - 18], fill=COL["ink"])
    draw.polygon([(cx + 38, cy - 18), (cx + 54, cy - 12), (cx + 38, cy - 8)],
                 fill=COL["gold"])
    banner(draw, x0, y1 - 30, x1, y1, COL["gold"], "PARDONED", 17, COL["navy"])


def pic_skyline(draw, x0, y0, x1, y1, colour):
    """A city skyline under a loyalty banner."""
    base = y1 - 30
    for bx0, bh in ((x0 + 20, 40), (x0 + 68, 48), (x0 + 116, 44),
                    (x0 + 164, 34), (x0 + 208, 46)):
        draw.rectangle([bx0, base - bh, bx0 + 40, base], fill=colour)
        for row in (base - bh + 8, base - bh + 22):
            draw.rectangle([bx0 + 8, row, bx0 + 16, row + 6], fill=COL["white"])
            draw.rectangle([bx0 + 24, row, bx0 + 32, row + 6], fill=COL["white"])
    px = x0 + 88
    draw.line([px, base - 48, px, base - 62], fill=colour, width=3)
    draw.polygon([(px, base - 62), (px + 26, base - 56), (px, base - 50)],
                 fill=COL["red"])
    banner(draw, x0, y1 - 30, x1, y1, COL["red"], "LOYALTY", 17, COL["white"])


def pic_ribbon(draw, x0, y0, x1, y1, colour):
    """A remembrance ribbon, and the count, big, in the picture."""
    cx = (x0 + x1) // 2 - 46
    cy = (y0 + y1) // 2 - 10
    draw.ellipse([cx - 17, cy - 30, cx + 17, cy + 2], outline=colour, width=6)
    draw.polygon([(cx - 10, cy - 6), (cx + 10, cy - 6), (cx + 30, cy + 34),
                  (cx + 12, cy + 34), (cx, cy + 12)], fill=colour)
    draw.polygon([(cx + 10, cy - 6), (cx - 10, cy - 6), (cx - 30, cy + 34),
                  (cx - 12, cy + 34), (cx, cy + 12)], fill=colour)
    tx = cx + 62
    draw.text((tx, cy - 30), "5", font=load_font("bold", 54), fill=colour)
    draw.text((tx + 40, cy - 2), "/ HOUR", font=load_font("bold", 20), fill=colour)
    draw.text((tx, cy + 24), "WOMEN", font=load_font("bold", 16), fill=COL["grey"])


SCENES = {"tower": pic_tower, "chart": pic_chart, "turkey": pic_turkey,
          "skyline": pic_skyline, "ribbon": pic_ribbon}


# ---------------------------------------------------------------- layout

def picture_panel(draw, story, x0, y0, x1, y1):
    """Picture strip at the top of a card, with the fact inside it."""
    colour = story["colour"]
    draw.rectangle([x0, y0, x1, y1], fill=shade(colour))
    draw.rectangle([x0, y1 - 5, x1, y1], fill=colour)
    SCENES[story["scene"]](draw, x0, y0, x1, y1, colour)


def card(draw, story, x0, y0, x1, y1, head_top, sub_size, lines_cap, panel):
    """One story card: big picture first, then tag, headline, one line."""
    colour = story["colour"]
    draw.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=COL["card"])
    picture_panel(draw, story, x0, y0, x1, y0 + panel)
    pad = 20
    tx = x0 + pad
    ty = y0 + panel + 14
    draw.text((tx, ty), story["tag"], font=load_font("bold", 13), fill=colour)
    inner = (x1 - x0) - 2 * pad
    face, rows = fit_headline(story["headline"], "bold", head_top, 18, inner,
                              lines_cap)
    hy = ty + 28
    for i, row in enumerate(rows):
        draw.text((tx, hy + i * (face.size + 5)), row, font=face, fill=COL["ink"])
    ly = hy + len(rows) * (face.size + 5) + 6
    draw.text((tx, ly), story["sub"], font=load_font("plain", sub_size),
              fill=COL["grey"])


def build():
    img = Image.new("RGB", (W, H), COL["paper"])
    draw = ImageDraw.Draw(img)
    # Masthead: the paper's name, the date, how many stories.
    draw.rectangle([0, 0, W, 142], fill=COL["navy"])
    draw.text((EDGE, 14), "THE WORLD  •  IN ONE PICTURE",
              font=load_font("bold", 16), fill=COL["pale_gold"])
    draw.text((EDGE, 42), "25 NOVEMBER 2026",
              font=load_font("serif", 62), fill=COL["white"])
    draw.rectangle([W - EDGE - 168, 22, W - EDGE, 122], outline=COL["gold"], width=2)
    for text, y, face, fill in [
            ("WEDNESDAY", 34, load_font("bold", 20), COL["white"]),
            ("6 STORIES", 62, load_font("bold", 20), COL["pale_gold"]),
            ("FIRST REPORTED", 88, load_font("bold", 13), COL["mist"]),
            ("TODAY", 104, load_font("bold", 13), COL["mist"])]:
        draw.text((W - EDGE - 150, y), text, font=face, fill=fill)
    draw.rectangle([0, 142, W, 146], fill=COL["gold"])
    # Lead story: text on the left, a picture that says GUILTY on the right.
    lx0, ly0, lx1, ly1 = EDGE, 162, W - EDGE, 448
    draw.rounded_rectangle([lx0, ly0, lx1, ly1], radius=14, fill=COL["card"])
    draw.rectangle([lx0, ly0, lx0 + 8, ly1], fill=LEAD["colour"])
    tx = lx0 + 28
    draw.rounded_rectangle([tx, ly0 + 20, tx + 116, ly0 + 46], radius=13,
                           fill=LEAD["colour"])
    draw.text((tx + 14, ly0 + 26), "TOP STORY", font=load_font("bold", 14),
              fill=COL["white"])
    draw.text((tx + 132, ly0 + 26), LEAD["tag"], font=load_font("bold", 14),
              fill=LEAD["colour"])
    face, rows = fit_headline(LEAD["headline"], "serif", 40, 30, 540, 2)
    hy = ly0 + 62
    for i, row in enumerate(rows):
        draw.text((tx, hy + i * 50), row, font=face, fill=COL["ink"])
    sub_face = load_font("plain", 17)
    sub_rows = wrap_text(LEAD["sub"], sub_face, 540, 2)
    sy = hy + len(rows) * 50 + 12
    for i, row in enumerate(sub_rows):
        draw.text((tx, sy + i * 24), row, font=sub_face, fill=COL["grey"])
    pic_courtroom(img, lx0 + 596, ly0 + 16, lx1 - 16, ly1 - 16)
    # Divider, then the other five stories in two rows.
    label = "MORE FROM AROUND THE WORLD"
    lf = load_font("bold", 15)
    draw.text((EDGE, 464), label, font=lf, fill=COL["navy"])
    draw.line([EDGE + int(lf.getlength(label)) + 14, 473, W - EDGE, 473],
              fill=COL["gold"], width=2)
    gap = 24
    wide = (W - 2 * EDGE - gap) // 2
    for i, story in enumerate(CARDS[:2]):
        x0 = EDGE + i * (wide + gap)
        card(draw, story, x0, 492, x0 + wide, 700, 27, 15, 2, 92)
    narrow = (W - 2 * EDGE - 2 * gap) // 3
    for i, story in enumerate(CARDS[2:]):
        x0 = EDGE + i * (narrow + gap)
        card(draw, story, x0, 718, x0 + narrow, 962, 23, 14, 3, 96)
    # Footer: the date again, and the sources.
    draw.rectangle([0, 976, W, H], fill=COL["navy"])
    draw.text((EDGE, 990), "ALL EVENTS FIRST REPORTED 25 NOVEMBER 2026",
              font=load_font("bold", 14), fill=COL["white"])
    draw.text((W - EDGE - 360, 990), "SOURCES: REUTERS  •  AP  •  UN  •  AFP",
              font=load_font("plain", 14), fill=COL["mist"])
    return img


def main():
    out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out.mkdir(parents=True, exist_ok=True)
    if HAVE_PIL:
        build().save(out / "entry.png", format="PNG")
    else:
        shutil.copyfile(Path(__file__).with_name("entry.png"), out / "entry.png")


if __name__ == "__main__":
    main()
