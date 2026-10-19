import json
import urllib.request
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "assets"
(root / "tiles").mkdir(parents=True, exist_ok=True)
(root / "objects").mkdir(parents=True, exist_ok=True)
(root / "battle").mkdir(parents=True, exist_ok=True)

tiles = {
    "coast": "4e408c3c-1861-4b9b-b736-7d7305b02e9f",
    "dungeon": "96aacc28-4337-46cf-b412-07061e799422",
}
objects = {
    "cottage": "27eec124-288c-41a9-b660-d998fa8d6612",
    "gate": "c4ad1cc7-8ff9-49c4-930f-4bbd4560e306",
    "tree": "0c68951e-d173-4a21-a3e1-11888e58d4a2",
    "palm": "5656cd02-3e84-4a41-9dc0-a381eb6b82ac",
    "rock": "cc83d22a-1497-4ab3-9b89-bbc28b066d88",
    "tablet": "715b48b6-a017-4769-8487-09c307aa36e0",
    "flowers": "24089542-e429-4c62-87bf-9eb901b5b95a",
    "chest": "8174b4d8-8df8-4568-8465-adb432c73f06",
}

for name, tid in tiles.items():
    png = root / "tiles" / f"{name}.png"
    meta = root / "tiles" / f"{name}.json"
    urllib.request.urlretrieve(
        f"https://api.pixellab.ai/mcp/tilesets/{tid}/image?inline=true", png
    )
    urllib.request.urlretrieve(
        f"https://api.pixellab.ai/mcp/tilesets/{tid}/metadata", meta
    )
    print(name, png.stat().st_size, meta.stat().st_size)

for name, oid in objects.items():
    dest = root / "objects" / f"{name}.png"
    urllib.request.urlretrieve(
        f"https://api.pixellab.ai/mcp/map-objects/{oid}/download", dest
    )
    print(name, dest.stat().st_size)

meta = json.loads((root / "tiles" / "coast.json").read_text(encoding="utf-8"))
print("TOP", list(meta.keys()))
tiles_list = meta.get("tiles")
print("tiles type", type(tiles_list).__name__, "len", len(tiles_list) if hasattr(tiles_list, "__len__") else None)
if isinstance(tiles_list, list) and tiles_list:
    sample = tiles_list[0]
    print("tile keys", list(sample.keys()))
    slim = {k: sample[k] for k in sample if k != "image"}
    print(json.dumps(slim, indent=2)[:2500])
