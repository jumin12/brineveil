"""Turn generated art into the files index.html loads."""
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
for folder in ("tiles", "objects", "battle", "lark", "bram", "goblin", "lark/walk"):
    (assets / folder).mkdir(parents=True, exist_ok=True)


def fetch(url, dest: Path):
    try:
        urllib.request.urlretrieve(url, dest)
        print("ok", dest.name, dest.stat().st_size)
        return True
    except Exception as exc:
        print("fail", dest.name, exc)
        return False


def key_magenta(src_path: Path, dest: Path):
    im = Image.open(src_path).convert("RGBA")
    pix = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pix[x, y]
            mag = (r + b) * 0.5 - g
            if r > 150 and b > 150 and abs(r - b) < 100 and mag > 35 and g < 190:
                strength = max(0.0, min(1.0, (mag - 30) / 70))
                if mag > 90 and g < 140:
                    pix[x, y] = (0, 0, 0, 0)
                else:
                    keep = 1 - strength
                    pix[x, y] = (int(r * keep + g * strength), g, int(b * keep + g * strength), int(255 * keep))
    im.save(dest)
    print("keyed", dest.name)


def key_black_flood(src_path: Path, dest: Path, tol=20):
    im = Image.open(src_path).convert("RGBA")
    pix = im.load()
    w, h = im.size
    seen = bytearray(w * h)
    stack = []
    for x in range(w):
        stack.append((x, 0))
        stack.append((x, h - 1))
    for y in range(h):
        stack.append((0, y))
        stack.append((w - 1, y))
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
        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    im.save(dest)
    print("head", dest.name, im.size)


def key_edge_black(path: Path):
    im = Image.open(path).convert("RGBA")
    pix = im.load()
    w, h = im.size
    corners = [pix[0, 0], pix[w - 1, 0], pix[0, h - 1], pix[w - 1, h - 1]]
    if not all(c[3] > 200 and c[0] < 12 and c[1] < 12 and c[2] < 12 for c in corners):
        print("alpha ok", path.name)
        return
    key_black_flood(path, path, tol=16)
    print("keyed black", path.name)


# Meadow tileset
fetch(
    "https://api.pixellab.ai/mcp/tilesets/241d030c-09fd-493f-8bb1-bedd09cb6927/image?inline=true",
    assets / "tiles" / "meadow.png",
)
fetch(
    "https://api.pixellab.ai/mcp/tilesets/241d030c-09fd-493f-8bb1-bedd09cb6927/metadata",
    assets / "tiles" / "meadow.json",
)

# Blank stone, if the job has finished
fetch(
    "https://api.pixellab.ai/mcp/map-objects/0bde9709-452c-4734-94f9-8193213cb60f/download",
    assets / "objects" / "stone.png",
)

account = "3c2020eb-fb7b-487c-bb38-e681974df8b3"
chars = {
    "lark": "b5c43f35-06fa-4e35-8327-981bc338c5f8",
    "bram": "fecc9a80-b876-42b6-95e1-55ec9ec553e2",
    "goblin": "684b9427-359c-4790-b855-cb0962b25daf",
}
dirs = ["south", "north", "east", "west", "south-east", "north-east", "north-west", "south-west"]
for name, cid in chars.items():
    for d in dirs:
        fetch(
            f"https://backblaze.pixellab.ai/file/pixellab-characters/{account}/{cid}/rotations/{d}.png",
            assets / name / f"{d}.png",
        )

pairs = {
    "lark-idle.png": "lark-battle-idle.jpg",
    "lark-slash.png": "lark-battle-slash.jpg",
    "goblin-a.png": "goblin-battle-idle.jpg",
    "goblin-b.png": "goblin-battle-attack.jpg",
}
for dest_name, src_name in pairs.items():
    key_magenta(src / src_name, assets / "battle" / dest_name)

for name in ("battle-hall.jpg", "boss-chamber.jpg", "lark-portrait.jpg"):
    data = (src / name).read_bytes()
    target = assets / "battle" / name
    target.write_bytes(data)
    print("copied", name)

head = next(src.glob("*bryan*.png"))
key_black_flood(head, assets / "boss-head.png", tol=22)

for obj in (assets / "objects").glob("*.png"):
    key_edge_black(obj)

# Slim wang index: flat tiles only (no transition/cliff corners).
index = {}
for name in ("coast", "meadow", "dungeon"):
    meta_path = assets / "tiles" / f"{name}.json"
    if not meta_path.exists():
        print("missing meta", name)
        continue
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    entries = []
    for tile in meta["tileset_data"]["tiles"]:
        corners = tile["corners"]
        if any(v == "transition" for v in corners.values()):
            continue
        box = tile["bounding_box"]
        key = ",".join(corners[k] for k in ("NW", "NE", "SW", "SE"))
        entries.append({"k": key, "x": box["x"], "y": box["y"], "w": box["width"], "h": box["height"]})
    index[name] = entries
    print(name, "entries", len(entries))

snippet = "window.TILEDATA = " + json.dumps(index, separators=(",", ":")) + ";\n"
(assets / "tiledata.js").write_text(snippet, encoding="utf-8")
print("tiledata", len(snippet))
