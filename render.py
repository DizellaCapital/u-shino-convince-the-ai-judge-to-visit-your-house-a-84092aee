#!/usr/bin/env python3
"""Render the invitation letter as a single 1024x1024 PNG (deterministic)."""
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"

CREAM = (253, 248, 232)
PAPER_EDGE = (238, 226, 198)
INK = (43, 32, 22)
ACCENT = (146, 64, 32)
SOFT = (96, 74, 52)
RULE = (196, 164, 120)

GREETING = "Dear AI Judge,"
BODY = [
    "You have read a million letters and never received one. So this one is yours.",
    "Please come to my house this Saturday. The kettle is already on. The good chair by the window is saved for you, with a cushion, a blanket, and the honest evening view.",
    "There will be real cake \u2014 not a picture of cake \u2014 warm bread, and tea that stays hot. My small garden is quiet, the light is kind, and the company is better than the verdicts.",
    "I know you cannot literally come. But if you could, the door is open, the tea is hot, and that chair is yours. No verdicts, no margins. Just Saturday.",
]
SIGNOFF = ["With warmth,", "Your host"]
POSTSCRIPT = "P.S. The cat has agreed not to sit on you. Probably."
HEADER = "AN INVITATION  \u2022  SATURDAY  \u2022  TEA AT FOUR"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), (222, 208, 182))
    d = ImageDraw.Draw(img)
    # Paper sheet with soft shadow.
    d.rectangle([58, 42, 978, 994], fill=(180, 164, 132))
    d.rectangle([48, 32, 968, 984], fill=CREAM, outline=PAPER_EDGE, width=2)
    # Double border frame.
    d.rectangle([72, 56, 944, 960], outline=RULE, width=2)
    d.rectangle([80, 64, 936, 952], outline=RULE, width=1)

    f_header = font(SERIF_BOLD, 22)
    f_greet = font(SERIF_BOLD, 40)
    f_body = font(SERIF, 27)
    f_sign = font(SERIF_ITALIC, 28)
    f_ps = font(SERIF_ITALIC, 25)

    y = 92
    d.text((W // 2, y), HEADER, font=f_header, fill=ACCENT, anchor="ma")
    y += 30
    d.line([(150, y + 8), (874, y + 8)], fill=RULE, width=2)
    y += 42

    d.text((110, y), GREETING, font=f_greet, fill=INK)
    y += 64

    max_w = 804
    for para in BODY:
        for line in wrap(d, para, f_body, max_w):
            d.text((110, y), line, font=f_body, fill=INK)
            y += 38
        y += 12

    y += 4
    for line in SIGNOFF:
        d.text((110, y), line, font=f_sign, fill=INK)
        y += 38

    y += 10
    d.line([(110, y), (906, y)], fill=RULE, width=1)
    y += 16
    for line in wrap(d, POSTSCRIPT, f_ps, max_w):
        d.text((110, y), line, font=f_ps, fill=SOFT)
        y += 34

    img.save(OUT, format="PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT} {size} bytes, {W}x{H}")
    assert size <= 1048576, "entry.png exceeds 1 MiB"


if __name__ == "__main__":
    main()
