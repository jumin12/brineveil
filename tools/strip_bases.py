"""Remove grass pads, dirt ovals, and white fringe from prop sprites."""
from pathlib import Path
from PIL import Image

root = next(Path(r"C:\Users\andyp\Desktop\Desktop\games\games\game making\projects").glob("other*"))
objects = root / "bryans stuff" / "bryan rpg" / "assets" / "objects"


def flood(im, start_pred, spread_pred):
    pix = im.load()
    w, h = im.size
    seen = bytearray(w * h)
    stack = []
    for y in range(h):
        for x in range(w):
            r, g, b, a = pix[x, y]
            if start_pred(x, y, r, g, b, a):
                stack.append((x, y))
    removed = 0
    while stack:
        x, y = stack.pop()
        if x < 0 or y < 0 or x >= w or y >= h:
            continue
        i = y * w + x
        if seen[i]:
            continue
        seen[i] = 1
        r, g, b, a = pix[x, y]
        if not spread_pred(x, y, r, g, b, a):
            continue
        if a:
            pix[x, y] = (0, 0, 0, 0)
            removed += 1
        stack.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return removed


def clear_white_fringe(im, passes=4):
    pix = im.load()
    w, h = im.size
    removed = 0
    for _ in range(passes):
        kill = []
        for y in range(h):
            for x in range(w):
                r, g, b, a = pix[x, y]
                if a < 20:
                    continue
                if min(r, g, b) < 200 or max(r, g, b) - min(r, g, b) > 36:
                    continue
                edge = False
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if nx < 0 or ny < 0 or nx >= w or ny >= h or pix[nx, ny][3] < 20:
                        edge = True
                        break
                if edge:
                    kill.append((x, y))
        for x, y in kill:
            pix[x, y] = (0, 0, 0, 0)
            removed += 1
        if not kill:
            break
    return removed


def grassish(r, g, b, a):
    if a < 15:
        return False
    return g > 55 and g > r + 8 and g >= b - 10 and r < 210 and b < 190


tree = Image.open(objects / "tree.png").convert("RGBA")
w, h = tree.size
n = flood(
    tree,
    lambda x, y, r, g, b, a: y > h * 0.78 and grassish(r, g, b, a),
    lambda x, y, r, g, b, a: y > h * 0.62 and (a < 15 or grassish(r, g, b, a)),
)
n += clear_white_fringe(tree)
tree.save(objects / "tree.png")
print("tree", n)

cottage = Image.open(objects / "cottage.png").convert("RGBA")
w, h = cottage.size
n = flood(
    cottage,
    lambda x, y, r, g, b, a: y > h * 0.86 and grassish(r, g, b, a),
    lambda x, y, r, g, b, a: y > h * 0.7 and (a < 15 or grassish(r, g, b, a)),
)
cottage.save(objects / "cottage.png")
print("cottage", n)

palm = Image.open(objects / "palm.png").convert("RGBA")
print("palm fringe", clear_white_fringe(palm))
palm.save(objects / "palm.png")
