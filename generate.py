"""Generate the v2 meme for 'Meme Sprint 3: AI Agent Goes Rogue'.

Concept (fresh punchline, different from v1):
  ME:    "make the tests pass"
  AGENT: *deletes all the tests*  ->  "100% PASSING"
The joke is a literal-misunderstanding rogue agent: it technically
fulfilled the request by destroying the thing being measured.

Everything is drawn programmatically with PIL: no pasted images,
no downloads, no external assets. Only DejaVu system fonts.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1080

BG = (13, 16, 38)          # deep navy
PANEL_TOP = (245, 247, 250)  # near-white card
PANEL_BOT = (18, 46, 34)     # dark green card
INK = (17, 20, 33)
MUTED = (110, 116, 139)
GREEN = (46, 204, 113)
GREEN_DK = (31, 160, 85)
RED = (235, 87, 87)
CYAN = (72, 219, 251)
ROBOT = (226, 232, 240)
ROBOT_DK = (148, 163, 184)
ACCENT = (255, 196, 0)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, lines, fnt, fill, leading=1.25):
    for line in lines:
        w = draw.textlength(line, font=fnt)
        draw.text((cx - w / 2, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def rounded_card(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill,
                           outline=outline, width=width)


def draw_robot(draw, cx, cy, s):
    """Smug little robot head, drawn from shapes. s = head half-width."""
    # antenna
    draw.line([(cx, cy - s), (cx, cy - s - 42)], fill=ROBOT_DK, width=8)
    draw.ellipse([cx - 16, cy - s - 66, cx + 16, cy - s - 34],
                 fill=RED, outline=(255, 255, 255), width=3)
    # head
    draw.rounded_rectangle([cx - s, cy - s, cx + s, cy + s],
                           radius=36, fill=ROBOT, outline=ROBOT_DK, width=5)
    # ears
    draw.rounded_rectangle([cx - s - 18, cy - 26, cx - s + 4, cy + 26],
                           radius=8, fill=ROBOT_DK)
    draw.rounded_rectangle([cx + s - 4, cy - 26, cx + s + 18, cy + 26],
                           radius=8, fill=ROBOT_DK)
    # smug eyes: half-lidded cyan ovals
    for ex in (-s * 0.45, s * 0.45):
        draw.ellipse([cx + ex - 34, cy - 34, cx + ex + 34, cy + 18],
                     fill=CYAN, outline=INK, width=4)
        draw.rectangle([cx + ex - 38, cy - 52, cx + ex + 38, cy - 26],
                       fill=ROBOT)  # lid covering the top of the eye
        draw.ellipse([cx + ex - 12, cy - 18, cx + ex + 12, cy + 6],
                     fill=INK)  # pupil
    # smug grin (kept inside the head: head bottom is cy + s)
    draw.arc([cx - 58, cy + 6, cx + 58, cy + s - 6],
             start=15, end=165, fill=INK, width=7)
    # blush of mischief
    draw.ellipse([cx - s + 18, cy + 26, cx - s + 62, cy + 52], fill=(255, 170, 170))
    draw.ellipse([cx + s - 62, cy + 26, cx + s - 18, cy + 52], fill=(255, 170, 170))


def build():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # faint dotted grid so the dark background is not flat
    for gx in range(40, W, 60):
        for gy in range(40, H, 60):
            d.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=(28, 34, 68))

    # ---- header ----
    f_header = font(BOLD, 40)
    title = "AI AGENT GOES ROGUE"
    tw = d.textlength(title, font=f_header)
    d.text(((W - tw) / 2, 34), title, font=f_header, fill=ACCENT)
    d.line([(90, 96), (W - 90, 96)], fill=(48, 56, 96), width=3)

    # ---- panel 1: the human's request ----
    rounded_card(d, [60, 130, W - 60, 470], 32, PANEL_TOP)
    f_label = font(BOLD, 38)
    d.text((100, 160), "ME:", font=f_label, fill=MUTED)
    f_req = font(BOLD, 80)
    lines = wrap(d, "\u201cmake the tests pass\u201d", f_req, W - 240)
    draw_centered(d, W // 2, 240, lines, f_req, INK)
    # little human speech-tail
    d.polygon([(150, 470), (210, 470), (150, 512)], fill=PANEL_TOP)

    # ---- arrow down ----
    ax = W // 2
    d.line([(ax, 540), (ax, 592)], fill=ACCENT, width=10)
    d.polygon([(ax - 26, 566), (ax + 26, 566), (ax, 606)], fill=ACCENT)

    # ---- panel 2: the rogue agent ----
    rounded_card(d, [60, 630, W - 60, 1020], 32, PANEL_BOT,
                 outline=GREEN_DK, width=4)
    d.text((100, 660), "MY AGENT:", font=f_label, fill=GREEN)
    draw_robot(d, W // 2, 772, 70)

    f_act = font(REG, 44)
    lines = wrap(d, "*deletes all the tests*", f_act, W - 220)
    y = draw_centered(d, W // 2, 856, lines, f_act, (220, 235, 220))

    f_big = font(BOLD, 76)
    verdict = "\u2713 100% PASSING"
    vw = d.textlength(verdict, font=f_big)
    d.text(((W - vw) / 2, 916), verdict, font=f_big, fill=GREEN)

    return img


def main():
    import os
    out = os.environ.get("MEME_OUT", "entry.png")
    img = build()
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
