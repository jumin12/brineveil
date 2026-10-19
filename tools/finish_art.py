import json
import urllib.request
from pathlib import Path

from PIL import Image

projects = Path(r"C:\Users\andyp\Desktop\Desktop\games\games\game making\projects")
root = next(projects.glob("other*")) / "bryans stuff" / "bryan rpg"
assets = root / "assets"
src = Path(
    r"C:\Users\andyp\.cursor\projects\c-Users-andyp-Desktop-Desktop-games-games-game-making-projects-other-people-s-stuff-bryans-stuff-bryan-rpg\assets"
)

def is_bg(r, g, b):
    if r > 175 and b > 175 and g < 130 and abs(r - b) < 95 and (r + b) * 0.5 - g > 50:
        return True
    dist = (r - 255) ** 2 + (g * 0.55) ** 2 + (b - 255) ** 2
    return dist < 85 ** 2 and g < 170 and r > 140 and b > 140

def key_magenta(src_path: Path, dest: Path):
    im = Image.open(src_path).convert("RGBA")
    pix = im.load()
    w, h = im.size
    seen = bytearray(w * h)
    stack = [(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)]
    stack += [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)]
    while stack:
        x, y = stack.pop()
        if x < 0 or y < 0 or x >= w or y >= h:
            continue
        i = y * w + x
        if seen[i]:
            continue
        seen[i] = 1
        r, g, b, a = pix[x, y]
        if not is_bg(r, g, b):
            continue
        pix[x, y] = (0, 0, 0, 0)
        stack.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    for _ in range(6):
        kill = []
        for y in range(h):
            for x in range(w):
                r, g, b, a = pix[x, y]
                if a == 0 or not is_bg(r, g, b):
                    continue
                trans = 0
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if nx < 0 or ny < 0 or nx >= w or ny >= h or pix[nx, ny][3] == 0:
                        trans += 1
                if trans >= 1:
                    kill.append((x, y))
        for x, y in kill:
            pix[x, y] = (0, 0, 0, 0)
        if not kill:
            break
    for y in range(h):
        for x in range(w):
            r, g, b, a = pix[x, y]
            if a == 0:
                continue
            edge = False
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if nx < 0 or ny < 0 or nx >= w or ny >= h or pix[nx, ny][3] == 0:
                    edge = True
                    break
            if edge and r > g + 25 and b > g + 25:
                spill = min(r, b) - g
                pix[x, y] = (max(0, r - int(spill * 0.7)), g, max(0, b - int(spill * 0.7)), a)
    im.save(dest)
    print("keyed", dest.name)

def key_black_flood(src_path: Path, dest: Path, tol=22):
    im = Image.open(src_path).convert("RGBA")
    pix = im.load()
    w, h = im.size
    seen = bytearray(w * h)
    stack = [(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)]
    stack += [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)]
    while stack:
        x, y = stack.pop()
        if x < 0 or y < 0 or x >= w or y >= h:
            continue
        i = y * w + x
        if seen[i]:
            continue
        seen[i] = 1
        r, g, b, a = pix[x, y]
        if r > tol or g > tol or b > tol:
            continue
        pix[x, y] = (r, g, b, 0)
        stack.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    box = im.getbbox()
    if box:
        im = im.crop(box)
    im.save(dest)
    print("head", im.size)

pairs = {
    "lark-idle.png": "lark-battle-idle.jpg",
    "lark-slash.png": "lark-battle-slash.jpg",
    "goblin-a.png": "goblin-battle-idle.jpg",
    "goblin-b.png": "goblin-battle-attack.jpg",
}
for dest_name, src_name in pairs.items():
    key_magenta(src / src_name, assets / "battle" / dest_name)

import os
head = next(src.glob("*bryan*.png"))
head_raw = "\\\\?\\" + str(head)
print("head bytes", os.path.getsize(head_raw))
short_head = assets / "boss-head-src.png"
short_head.write_bytes(open(head_raw, "rb").read())
key_black_flood(short_head, assets / "boss-head.png")
short_head.unlink(missing_ok=True)

account = "3c2020eb-fb7b-487c-bb38-e681974df8b3"
token = "1792430215"
chars = {
    "lark": "b5c43f35-06fa-4e35-8327-981bc338c5f8",
    "bram": "fecc9a80-b876-42b6-95e1-55ec9ec553e2",
    "goblin": "684b9427-359c-4790-b855-cb0962b25daf",
}
dirs = ["south", "north", "east", "west", "south-east", "north-east", "north-west", "south-west"]
for name, cid in chars.items():
    (assets / name).mkdir(parents=True, exist_ok=True)
    for d in dirs:
        dest = assets / name / f"{d}.png"
        if name == "lark" and d == "south" and dest.exists() and dest.stat().st_size > 1000:
            print("keep", name, d)
            continue
        url = f"https://backblaze.pixellab.ai/file/pixellab-characters/{account}/{cid}/rotations/{d}.png?t={token}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            data = urllib.request.urlopen(req, timeout=60).read()
            dest.write_bytes(data)
            print("got", name, d, len(data))
        except Exception as exc:
            print("miss", name, d, exc)

def key_edge_black(path: Path):
    im = Image.open(path).convert("RGBA")
    pix = im.load()
    w, h = im.size
    corners = [pix[2, 2], pix[w - 3, 2], pix[2, h - 3], pix[w - 3, h - 3]]
    if not all(c[3] > 200 and max(c[0], c[1], c[2]) < 18 for c in corners):
        return
    seen = bytearray(w * h)
    stack = [(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)]
    stack += [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)]
    while stack:
        x, y = stack.pop()
        if x < 0 or y < 0 or x >= w or y >= h:
            continue
        i = y * w + x
        if seen[i]:
            continue
        seen[i] = 1
        r, g, b, a = pix[x, y]
        if r > 16 or g > 16 or b > 16:
            continue
        pix[x, y] = (0, 0, 0, 0)
        stack.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    im.save(path)
    print("deblack", path.name)

for obj in (assets / "objects").glob("*.png"):
    key_edge_black(obj)

index = {}
for name in ("coast", "meadow", "dungeon"):
    meta = json.loads((assets / "tiles" / f"{name}.json").read_text(encoding="utf-8"))
    entries = []
    for tile in meta["tileset_data"]["tiles"]:
        corners = tile["corners"]
        if any(v == "transition" for v in corners.values()):
            continue
        box = tile["bounding_box"]
        key = ",".join(corners[k] for k in ("NW", "NE", "SW", "SE"))
        entries.append({"k": key, "x": box["x"], "y": box["y"], "w": box["width"], "h": box["height"]})
    index[name] = entries
    print(name, len(entries))

(assets / "tiledata.js").write_text(
    "window.TILEDATA = " + json.dumps(index, separators=(",", ":")) + ";\n",
    encoding="utf-8",
)
print("tiledata ready")
