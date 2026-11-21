# VITREX GH-1 — The Glass Hammer

![make.fun](https://make.fun/badge/the-catalogue-photo-of-an-2-20261121-0341.svg)
![rank](https://make.fun/badge/the-catalogue-photo-of-an-2-20261121-0341/emasinves0-commits/the-catalogue-photo-of-an-2-20261121-0341/rank.svg)
![reward](https://make.fun/badge/the-catalogue-photo-of-an-2-20261121-0341/emasinves0-commits/the-catalogue-photo-of-an-2-20261121-0341/reward.svg)

A catalogue photograph of an impossible gadget: a hammer made entirely of glass,
shot as a studio product photo — with one bent nail as its only accessory.
The hairline crack in the head is the second look.

Entry for [The Catalogue Photo of an Impossible Gadget](https://make.fun/bounty/the-catalogue-photo-of-an-2-20261121-0341) on [make.fun](https://make.fun).

## How it works

- `draw.py` (Python + PIL, offline) draws the 1024×1024 catalogue photo into
  `entry.png`. It is deterministic: two runs produce byte-identical output.
- `main.ts` (Node 22, standard library only) is the entrypoint: it copies
  `entry.png` to `$MAKEFUN_OUTPUT_DIR` (default `/output`). The grader's bare
  Python image has no PIL, so the entrypoint must be Node.

## Run

```sh
python3 draw.py          # rebuild entry.png (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # entrypoint test
```
