#!/usr/bin/env python3
"""Draw the front page for Tuesday 24 November 2026.

"The Boss Is Back" is a newspaper page that sums up one day's world news in
a single 1024 by 1024 PNG. This script is the compositor: it measures every
story's text with the same DejaVu faces it prints in, wraps the text to its
column, and lays the blocks out in a fixed order down the page:

    masthead and date line
    the lead story, with a chart of Nvidia's share jump beside it
    four panels in a two-by-two grid (climate, Hormuz, Ukraine, Gaza)
    one wide panel (Indonesia and MSCI)
    a briefs strip along the bottom

The words come from news.md, shortened for the page but never embellished.
Running the script writes entry.png beside it:

    python3 draw.py
"""

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
MARGIN = 36
CONTENT_W = PAGE - 2 * MARGIN

PAPER = (250, 247, 238)
INK = (22, 22, 22)
ACCENT = (163, 28, 28)
FAINT = (96, 92, 84)
BOX_FILL = (243, 238, 226)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = f"{FONT_DIR}/DejaVuSerif.ttf"
SERIF_BOLD = f"{FONT_DIR}/DejaVuSerif-Bold.ttf"
SANS = f"{FONT_DIR}/DejaVuSans.ttf"
SANS_BOLD = f"{FONT_DIR}/DejaVuSans-Bold.ttf"

_font_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


def wrap(draw, text, face, max_width):
    """Split text into lines that each fit max_width when drawn in face."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=face) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def block(draw, x, y, text, face, line_step, fill=INK, max_width=CONTENT_W):
    """Draw a wrapped paragraph at (x, y); return the y just below it."""
    for line in wrap(draw, text, face, max_width):
        draw.text((x, y), line, font=face, fill=fill)
        y += line_step
    return y


def centered(draw, y, text, face, fill=INK):
    width = draw.textlength(text, font=face)
    draw.text(((PAGE - width) / 2, y), text, font=face, fill=fill)


def rule(draw, y, weight=1, fill=INK):
    draw.line([(MARGIN, y), (PAGE - MARGIN, y)], fill=fill, width=weight)


def kicker(draw, x, y, text):
    draw.text((x, y), text, font=font(SANS_BOLD, 14), fill=ACCENT)
    return y + 18


# ---------------------------------------------------------------- the lead

LEAD_KICKER = "SILICON VALLEY · MARKETS"
LEAD_HEADLINE = "THE BOSS IS BACK"
LEAD_SUBHEAD = "Nvidia board reinstates Jensen Huang as chief executive"
LEAD_BODY = (
    "Nvidia's board brought founder Jensen Huang back as chief executive "
    "on Monday. President Trump says he personally persuaded the board; "
    "Democrats want an investigation into the White House role. The shares "
    "jumped about 30% and Wall Street won back roughly half of last week's "
    "losses, though AI stocks stayed volatile."
)


def draw_lead_chart(draw, x0, y0, x1, y1):
    """A small box holding the day's one chart: Nvidia's jump."""
    draw.rectangle([x0, y0, x1, y1], fill=BOX_FILL, outline=INK, width=2)
    draw.text((x0 + 16, y0 + 10), "NVIDIA SHARES, MONDAY",
              font=font(SANS_BOLD, 15), fill=INK)
    draw.text((x0 + 16, y0 + 38), "+30%", font=font(SANS_BOLD, 32),
              fill=ACCENT)
    # Axes. The plot's top sits just under the label; the baseline is the
    # axis the line jumps away from.
    ax, ay = x0 + 22, y1 - 30
    plot_top = y0 + 44
    draw.line([(ax, plot_top), (ax, ay)], fill=FAINT, width=2)
    draw.line([(ax, ay), (x1 - 16, ay)], fill=FAINT, width=2)
    # The line: a flat, wobbling week low in the plot, then the jump on
    # the news. fy is height above the baseline, so the end rides high.
    span_x = (x1 - 16) - ax
    span_y = ay - plot_top
    shape = [(0.00, 0.30), (0.22, 0.27), (0.40, 0.35), (0.55, 0.28),
             (0.70, 0.55), (0.85, 0.80), (1.00, 0.95)]
    points = [(ax + fx * span_x, ay - fy * span_y) for fx, fy in shape]
    draw.line(points, fill=ACCENT, width=4, joint="curve")
    tip_x, tip_y = points[-1]
    draw.polygon([(tip_x, tip_y), (tip_x - 15, tip_y + 2),
                  (tip_x - 4, tip_y + 13)], fill=ACCENT)
    draw.text((x0 + 16, y1 - 24), "the jump on Huang's return",
              font=font(SANS, 13), fill=FAINT)


# ---------------------------------------------------------------- panels

PANELS = [
    (
        "CLIMATE · ANTALYA",
        "COP31 ENDS WITH NO DEAL",
        "The UN climate summit closed Sunday with no agreement, a first "
        "since Copenhagen 2009, after two days of overtime made it the "
        "longest COP on record. The EU walked out over a text silent on "
        "fossil fuels.",
    ),
    (
        "STRAIT OF HORMUZ",
        "THREE TANKERS HIT MINES, IRAN SAYS",
        "Tehran says three oil tankers struck mines and caught fire in "
        "the strait. Iran refuses to negotiate until its seven conditions "
        "are met, and vows to use every tool against the US naval "
        "blockade, reinstated on 14 July.",
    ),
    (
        "UKRAINE",
        "STRIKE ON ZAPORIZHZHIA KILLS TWO",
        "An overnight Russian attack hit an apartment building in the "
        "city, killing two people and wounding about 40, including four "
        "children, the regional governor, Mykhailo Semikin, said.",
    ),
    (
        "GAZA",
        "HAMAS SECURITY CHIEF KILLED",
        "Israeli airstrikes killed Naeem Abu Nahel, director of Hamas's "
        "internal security apparatus, and at least six other people, "
        "including two police officers, medics and police said.",
    ),
]

WIDE_KICKER = "INDONESIA · MARKETS"
WIDE_HEADLINE = "MSCI DENIES ANY PROMISE TO PRABOWO"
WIDE_BODY = (
    "MSCI says it never assured President Prabowo it would spare "
    "Indonesia a downgrade: the consultation on moving Indonesia to a "
    "Standalone Market runs to 30 April 2027, with a decision by 30 "
    "June. The denial followed reports of a 10 November call between "
    "Prabowo and MSCI chief Henry Fernandez, arranged by Ray Dalio. "
    "Jakarta's IHSG rose anyway, opening up 1.29% at 5,283 and closing "
    "up 0.49% at 5,241.59."
)

BRIEFS = [
    "Berlin: Germany is first to win access to Ukraine's DELTA "
    "battlefield system; Kyiv's combat data stays locked.",
    "Libya: the UN mission seeks a probe into Sunday's Benghazi port "
    "attack, where drones sank a Russian corvette.",
    "Football: Brentford beat Everton 4-0 in the Premier League.",
    "Cricket: Indonesia's women beat China by 91 runs at the Malaysia "
    "T20I Tri-Series.",
]


def draw_panel(draw, x, y, width, kick, headline, body):
    y = kicker(draw, x, y, kick)
    y = block(draw, x, y, headline, font(SANS_BOLD, 21), 24,
              max_width=width)
    y += 3
    y = block(draw, x, y, body, font(SANS, 16), 20, max_width=width)
    return y


def compose():
    image = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(image)

    # Masthead.
    rule(draw, 30, weight=3)
    rule(draw, 37, weight=1)
    centered(draw, 48, "WORLD IN ONE PAGE", font(SERIF_BOLD, 52))
    centered(draw, 112,
             "Tuesday, 24 November 2026 · One page, the whole day",
             font(SANS, 19), fill=FAINT)
    rule(draw, 142, weight=4)
    rule(draw, 149, weight=1)

    # Lead.
    y = kicker(draw, MARGIN, 158, LEAD_KICKER)
    draw.text((MARGIN, y), LEAD_HEADLINE, font=font(SANS_BOLD, 62),
              fill=INK)
    y += 74
    draw.text((MARGIN, y), LEAD_SUBHEAD, font=font(SERIF_BOLD, 24),
              fill=INK)
    y += 36
    chart_x0 = 618
    block(draw, MARGIN, y, LEAD_BODY, font(SANS, 18), 24,
          max_width=chart_x0 - MARGIN - 28)
    draw_lead_chart(draw, chart_x0, y, PAGE - MARGIN, y + 138)
    y += 148

    # Four panels in a two-by-two grid.
    rule(draw, y, weight=2)
    y += 12
    grid_top = y
    col_w = (CONTENT_W - 28) // 2
    left_x = MARGIN
    right_x = MARGIN + col_w + 28
    for row in range(2):
        row_y = y
        bottoms = []
        for col in range(2):
            kick, headline, body = PANELS[row * 2 + col]
            x = left_x if col == 0 else right_x
            bottoms.append(draw_panel(draw, x, row_y, col_w,
                                      kick, headline, body))
        y = max(bottoms) + 9
        if row == 0:
            rule(draw, y, weight=1, fill=FAINT)
            y += 11
    panels_bottom = y
    # Vertical divider between the two panel columns.
    divider_x = MARGIN + col_w + 14
    draw.line([(divider_x, grid_top), (divider_x, panels_bottom - 9)],
              fill=FAINT, width=1)

    # Wide Indonesia panel.
    rule(draw, y, weight=2)
    y += 10
    y = kicker(draw, MARGIN, y, WIDE_KICKER)
    draw.text((MARGIN, y), WIDE_HEADLINE, font=font(SANS_BOLD, 24),
              fill=INK)
    y += 30
    y = block(draw, MARGIN, y, WIDE_BODY, font(SANS, 17), 21)
    y += 8

    # Briefs strip.
    rule(draw, y, weight=2)
    y += 9
    draw.text((MARGIN, y), "IN BRIEF", font=font(SANS_BOLD, 15),
              fill=ACCENT)
    y += 21
    for brief in BRIEFS:
        y = block(draw, MARGIN, y, brief, font(SANS, 15), 18)
        y += 2
    rule(draw, y + 2, weight=3)

    return image, y


def main():
    image, bottom = compose()
    print(f"page furniture ends at y={bottom} of {PAGE}")
    image.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
