Original prompt: I want to make a jrpg but I want to make it simple as a demo. The game should be ultra modern with amazing pixel art graphics. the player should start with preset weapons and a simple inventory system consistening of a weapon, armor for body, and head, and ring and necklace slot. The weapons should be simple. The player should start in the overworld, be given their quest from a lonely old man, and be told of a dungeon nearby, the overworld should be a small island with only 2 locations, the quest giver, and the dungeon. when the players go to the dungeon they should first encounter simple goblins, the camera and mechanics and gameplay should be 2.5d and like Armor dragoon evolution the old 1999 game. The game should have amazing beautiful modern graphics and ui and amazing cinematic gameplay and effects. generate any assets needed. after the goblins are dealt with they are told to go fight the boss when they get to the boss it should be a cinematic cutscene describing the floating head I presented, and should shout things like I am gay., I play gay games, I like anime tiddies. before entering this room the player should be forced to read a note that says something extremely sinister and serious and the head should come out of a cloud of mist that makes it look terrifying. do this as a single index.html file and any generated assets and the head move into an assets folder. Generate any sounds needed with eleven labs api the game should look like trials of cascadia with the mechanics of Armor dragoon evolution the old 1999 game. ensure the art style matches the concept art presented and ensure you generate absolutely everything including full animations. the game should be 2.5d with amazing graphics that look as good as the concept image. create original locations and monsters and moves etc. Make sure the game is ultra clean, highly animated and looks and plays extremely good and not like a point and click adventure. ensure the combat is turn based and

## Decisions
- Single index.html canvas JRPG: Isle of Brineveil. Hero Lark, quest giver Bram, dungeon called the Maw, boss The Visage (the provided floating head).
- Overworld is free-walk 2.5D top-down pixel (not point-and-click). Battle is turn-based with a cinematic behind-the-hero camera, zoom, hit-stop, and generated pixel battle art.
- Inventory slots: weapon, body, head, ring, necklace, plus a small bag. Starter gear is equipped at the start.
- No ElevenLabs API key was present in the environment. Voices use the browser speech engine; music and effects are synthesized in the page so the demo still has sound.
- PixelLab characters (Lark, Bram, Goblin) and the hero walk cycle were still generating when the page was first assembled.

## Done
- `index.html` is the whole demo. Art lives in `assets/` (tiles, props, characters, walk cycles, battle paintings, and `boss-head.png`).
- Playable loop verified in the browser: title, talk to Bram, five-slot pack, enter the Maw, goblin fight (damage lands), forced stone, boss cutscene with the floating head and the first shout.
- No ElevenLabs key was available. Speech uses the browser voice. Music and hits are synthesized in the page.

## Scale and dungeon pass
- Idle uses the standing sprite only. Walk frames are pinned to the feet so they do not drift.
- Grass tufts sway. Tree and palm canopies sway a couple of degrees. Characters do not.
- After the title, Lark washes up a sand spit and walks onto the beach.
- People are smaller than the cottage and the trees. A little depth scale makes the near side of the screen slightly larger.
- The Maw is a long run of rooms: scouts, a brute, a west armory with the Tideblade and Scale Vest, then a shaman and two scouts, then the stone.

## Polish pass
- Dungeon now uses a real light mask: torches and Lark cut warm holes in the dark instead of a flat tint.
- Island has a sun grade and offset contact shadows.
- Collision is elliptical and sits on feet. Bram blocks. The east path, cottage, and gate are placed so you can walk the shore without clipping the sea or the trees.
- Pack is a worn column plus a bag grid. Item icons are in `assets/items/`.

## TODO
- Boss fight after the cutscene was not screenshot-verified end to end.
- Coastline autotiles are still blocky on some corners.
- The dungeon gate still includes its rocky frame.
- Diagonals use standing sprites.
