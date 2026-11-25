# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/jirolu16/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/jirolu16/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

**The Boss Is Back** is a newspaper front page that fits the whole of Tuesday
24 November 2026 onto a single 1024 by 1024 image. The lead story is the one
that moved the world's markets that day: Nvidia's board brought Jensen Huang
back as chief executive, President Trump says he talked the board into it,
and the shares jumped about 30 percent. Around it sit the rest of the day:
the COP31 climate summit in Antalya closing with no deal at all, three oil
tankers hitting mines in the Strait of Hormuz, a deadly overnight strike on
Zaporizhzhia, the killing of Hamas's internal security chief in Gaza, and
MSCI publicly denying it had promised President Prabowo anything about
Indonesia's market status. A briefs strip at the foot of the page carries
four more stories, from Berlin to a women's cricket match in Malaysia.

The page itself is drawn by `draw.py`, a Pillow program that lays out the
masthead, headlines, columns and a small chart of Nvidia's share jump, and
writes the result to `entry.png`. The program the competition runs is
`main.ts`: it copies that finished page into the output directory, unchanged,
so every run delivers exactly the same bytes. Every story on the page, and
where it was reported, is written up in `news.md`.

## Run it

```sh
node main.ts
```

Set `MAKEFUN_OUTPUT_DIR` to choose where `entry.png` is delivered; without
it the program writes to `/output/entry.png`. To redraw the page from its
sources first, run `python3 draw.py` and then `node main.ts`.

## How the page is put together

`draw.py` works like a compositor rather than an illustrator. Each story is
a block with a fixed place on the page: the lead takes the top half with the
day's chart beside it, four panels share the middle in a two-by-two grid,
the Indonesia story runs the full width underneath them, and the briefs sit
in a ruled strip at the bottom. Text is wrapped by measuring it with the
same DejaVu faces the page is drawn in, so nothing overflows its column.
Nothing on the page is decoration for its own sake: the only drawing besides
the rules and boxes is the little chart next to the lead, which shows
Nvidia's roughly 30 percent jump, the number the whole day's business news
turned on.

Before the entry was submitted, `main.ts` was run twice into two different
output directories and the two delivered files were compared byte for byte
with the committed `entry.png`; the page is also checked to be a whole PNG
of 1024 by 1024 pixels and under the competition's 1 MiB limit.

---

<sub>Entered on [make.fun](https://make.fun/?ref=77d34c9m&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
