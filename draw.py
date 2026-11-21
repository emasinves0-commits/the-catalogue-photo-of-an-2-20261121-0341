#!/usr/bin/env python3
"""Draw the catalogue photo: VITREX GH-1, a glass hammer.

Offline builder (PIL). Deterministic: no randomness, fixed coordinates.
Output: entry.png (1024x1024) next to this file.
The graded entrypoint is main.ts (Node stdlib), which only copies entry.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

# --- fonts: Liberation Sans vendored in the passport repo, else system DejaVu ---
def font(bold, size):
    cands = [
        os.path.expanduser("~/workspace/makefun/the-passport-page-of-a-countr-2-20261121-0318/fonts/LiberationSans-Bold.ttf")
        if bold else
        os.path.expanduser("~/workspace/makefun/the-passport-page-of-a-countr-2-20261121-0318/fonts/LiberationSans-Regular.ttf"),
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for c in cands:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def vgrad(size, top, bottom):
    """Vertical gradient RGB image."""
    w, h = size
    base = Image.new("RGB", (1, h))
    px = base.load()
    for y in range(h):
        t = y / max(1, h - 1)
        px[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return base.resize((w, h))


def glass_fill(draw, box, outline, top, bottom, radius=18):
    """Glass panel: vertical gradient + outline, drawn on an RGBA layer."""
    x0, y0, x1, y1 = box
    g = vgrad((x1 - x0, y1 - y0), top, bottom).convert("RGBA")
    mask = Image.new("L", (x1 - x0, y1 - y0), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, x1 - x0 - 1, y1 - y0 - 1], radius=radius, fill=255)
    draw._image.paste(g, (x0, y0), mask)
    draw.rounded_rectangle(box, radius=radius, outline=outline, width=3)


def main():
    img = vgrad((W, H), (238, 236, 231), (206, 203, 196)).convert("RGBA")

    # soft radial glow behind the product
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([212, 150, 812, 750], fill=(255, 255, 255, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    img.alpha_composite(glow)

    # studio sweep: floor darkens gently toward the bottom
    floor = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fd = ImageDraw.Draw(floor)
    for i, y in enumerate(range(760, H)):
        a = int(46 * (i / (H - 760)) ** 1.6)
        fd.line([(0, y), (W, y)], fill=(120, 116, 108, a))
    img.alpha_composite(floor)

    # ---------- hammer on its own layer, drawn horizontal, then rotated ----------
    layer = Image.new("RGBA", (1200, 1200), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    GLASS_TOP, GLASS_BOT = (223, 234, 238), (176, 199, 208)
    GLASS_EDGE = (127, 152, 164)
    HL = (255, 255, 255, 150)   # highlight white

    # handle: long glass bar (150,560)-(950,640)
    glass_fill(d, [150, 560, 950, 640], GLASS_EDGE, GLASS_TOP, GLASS_BOT, radius=38)
    d.rounded_rectangle([168, 572, 932, 592], radius=10, fill=HL)  # top highlight
    d.line([(168, 628), (932, 628)], fill=(255, 255, 255, 70), width=3)

    # head: shorter, chunkier glass block (870,430)-(1020,760)
    glass_fill(d, [870, 430, 1020, 760], GLASS_EDGE, GLASS_TOP, GLASS_BOT, radius=24)
    # striking face: slightly wider polished cap on top
    glass_fill(d, [856, 402, 1034, 458], GLASS_EDGE, (235, 243, 245), (196, 214, 221), radius=16)
    d.rounded_rectangle([874, 414, 1016, 430], radius=8, fill=(255, 255, 255, 170))
    # inner refraction diagonals on the head
    d.line([(895, 500), (985, 700)], fill=(255, 255, 255, 80), width=6)
    d.line([(915, 485), (995, 660)], fill=(255, 255, 255, 55), width=4)
    d.line([(885, 560), (950, 730)], fill=(160, 185, 195, 90), width=5)

    # claw: two short curved prongs hugging the head's bottom
    prong1 = [(885, 752), (838, 828), (812, 838), (806, 816), (842, 760), (872, 748)]
    prong2 = [(950, 752), (928, 824), (908, 842), (896, 824), (918, 758), (940, 748)]
    for prong in (prong1, prong2):
        d.polygon(prong, fill=(196, 212, 219, 255), outline=GLASS_EDGE)
    d.line([(895, 762), (845, 822)], fill=(255, 255, 255, 110), width=4)

    # steel collar where head meets handle
    collar = vgrad((34, 96), (168, 172, 176), (110, 114, 118)).convert("RGBA")
    cmask = Image.new("L", (34, 96), 0)
    ImageDraw.Draw(cmask).rounded_rectangle([0, 0, 33, 95], radius=10, fill=255)
    layer.paste(collar, (862, 552), cmask)
    d.rounded_rectangle([862, 552, 896, 648], radius=10, outline=(88, 92, 96), width=2)
    d.line([(868, 560), (868, 640)], fill=(255, 255, 255, 120), width=3)

    # hairline crack on the head (second-look reward) + chip on the face corner
    crack = [(1012, 470), (996, 498), (1006, 522), (990, 552), (1000, 578), (986, 606)]
    d.line(crack, fill=(255, 255, 255, 235), width=3, joint="curve")
    d.line([(996, 498), (982, 506)], fill=(255, 255, 255, 200), width=2)
    d.line([(990, 552), (976, 562)], fill=(255, 255, 255, 200), width=2)
    d.polygon([(1034, 402), (1018, 402), (1034, 422)], fill=(255, 255, 255, 220))

    # etched brand text on the head + model on the handle (rotates with product)
    f_brand = font(True, 30)
    f_model = font(False, 24)
    d.text((892, 585), "VITREX", font=f_brand, fill=(110, 135, 146, 255))
    d.text((895, 622), "GH-1", font=f_model, fill=(110, 135, 146, 255))
    d.text((250, 592), "GH-1", font=f_model, fill=(110, 135, 146, 255))

    # contact shadow from the hammer's own silhouette
    alpha = layer.split()[3]
    shadow = Image.new("RGBA", (1200, 1200), (0, 0, 0, 0))
    shadow.putalpha(alpha.point(lambda a: int(a * 0.28)))
    black = Image.new("RGBA", (1200, 1200), (60, 56, 50, 255))
    black.putalpha(shadow.split()[3])
    black = black.filter(ImageFilter.GaussianBlur(12))
    black = black.rotate(-28, resample=Image.BICUBIC, center=(600, 600))
    img.alpha_composite(black, (16, 40))

    # rotate hammer -28 deg (head rises to upper right) and place
    rot = layer.rotate(-28, resample=Image.BICUBIC, center=(600, 600))
    img.alpha_composite(rot, (-88, -78))

    # ---------- the one accessory: a single bent steel nail ----------
    nail = Image.new("RGBA", (340, 120), (0, 0, 0, 0))
    nd = ImageDraw.Draw(nail)
    # shadow under the nail
    nd.ellipse([20, 82, 300, 104], fill=(70, 66, 60, 90))
    # shaft: two segments with a bend at 2/3 (it already lost to the hammer once)
    nd.line([(40, 60), (230, 60)], fill=(150, 154, 158), width=12)
    nd.line([(40, 57), (230, 57)], fill=(215, 218, 220), width=4)
    nd.line([(230, 60), (300, 78)], fill=(150, 154, 158), width=12)
    nd.line([(230, 57), (298, 74)], fill=(215, 218, 220), width=4)
    nd.polygon([(300, 78), (318, 82), (300, 86)], fill=(150, 154, 158))
    # nail head (flat disc, seen at an angle)
    nd.ellipse([22, 44, 52, 76], fill=(178, 182, 186), outline=(120, 124, 128))
    nd.ellipse([28, 50, 46, 70], fill=(210, 213, 215))
    nail = nail.rotate(-8, resample=Image.BICUBIC, center=(170, 60))
    img.alpha_composite(nail, (120, 772))

    # ---------- catalogue plate (product text, not joke text) ----------
    d2 = ImageDraw.Draw(img)
    f_title = font(True, 30)
    f_sub = font(False, 21)
    d2.text((512, 928), "VITREX GH-1", font=f_title, fill=(74, 72, 68, 255), anchor="mm")
    d2.text((512, 962), "G L A S S   H A M M E R  ·  F O R   G E N T L E   T A P P I N G   O N L Y",
            font=f_sub, fill=(138, 135, 130, 255), anchor="mm")

    out = os.path.join(HERE, "entry.png")
    img.convert("RGB").save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
