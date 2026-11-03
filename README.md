# Crusaderreich

Crusaderreich adapts Kaiserreich into a 1936 German century shaped by monarchies. It uses CK3's original Old World map. The scenario contains the named dynastic rulers supplied for this project, plus additional European states and temporary map representatives where a CK3 character is required to hold territory. Events and decisions come later.

## Install and test

Copy `Crusaderreich` and `Crusaderreich.mod` into the CK3 user `mod` directory. Enable the mod in a launcher playset, select **The German Century**, and start a **new** 1936 game. Existing saves retain their old world state. The game installation is never modified.

Inspect Germany, France, Austria, Poland, Ukraine, Russia, Italy, Iberia, Scandinavia and the Balkans in the realm map. Open the dynasty panel for Wilhelm II and confirm **Hohenzollern**, rather than the fallback name “Fletcher.” Check CK3's `error.log` after starting and advancing one day. The user supplied screenshots confirming that the 1936 start loads. The latest ruler, government, and border changes still need an in-game check. The launcher descriptors target CK3 1.20; this is version metadata, not proof of in-game compatibility.

## Scenario data

- `data/nations.csv` and `data/characters.csv` record monarchs, governments, and explicitly marked temporary representatives. The user-defined rulers take precedence over Kaiserreich's base politics.
- `data/title_assignments.csv` maps CK3 titles to scenario states. Broad empire regions fill geography; specific titles override them at disputed borders.
- `data/county_map.csv` maps 1,623 CK3 counties to states. All counties in the supplied CK3 **European** geographical region now have an assignment. This is coverage, not proof that every border is exact.
- `data/complete_titles.csv` lists duchies and kingdoms whose counties all belong to one scenario state; those titles receive the matching holder in the generated 1936 history.
- `data/relatives.csv`, `data/parents.csv`, and `data/marriages.csv` define close royal families, including Wilhelm II's children and the Habsburg, Windsor, and other ruling lines. `Crusaderreich/history` defines dated characters and title holders. Lower titles point to their country crown; Egypt and Tripolitania are Ottoman vassals. `Crusaderreich/common/landed_titles` adds crowns needed for Corsica, Flanders-Wallonia, and the divided Italian states. `Crusaderreich/common/dynasties` uses localized dynasty names and prefixes so surnames render correctly.

The current adaptation gives Bohemia to Albrecht Franz von Habsburg, Tuscany to Peter Ferdinand, Italy to Robert von Habsburg, and Savoy and Piedmont to Sardinia. The Papal States hold all of Latium, Spoleto, and Ancona. Croatia and the United Baltic Duchy use the requested names. The Ottoman emperor holds the Sunni caliphate; Abbas II rules Egypt, Nubia, and Blemmya, while Idris I rules Tripolitania and Syrte as Ottoman vassals. Carol II uses CK3’s valid `vlach` culture so the game does not fall back to Akan. Title localization contains only place names, except the requested United Baltic Duchy. Some states outside Europe and some small border counties still need a visual review in CK3. Temporary council characters represent governments that CK3's medieval ruler model cannot express directly; they are excluded from the featured bookmark rulers. Unresearched birth dates use `1885.1.1` only as a marked game-data placeholder, while the source roster leaves them blank. Governments and religions are adapted through CK3's available mechanics.

Run `python3 tools/validate.py` for data consistency. To rebuild the map from CK3's landed-title files, run `python3 tools/build_map.py /path/to/game/common/landed_titles`, then `python3 tools/generate_scenario.py`. Both generators write only inside the mod repository.

The latest border pass transfers the specified Silesian, Polish, Lithuanian, Ukrainian, Russian, Scandinavian, and Lorraine counties and duchies. Joachim von Hohenzollern, a son of Wilhelm II, holds both Ireland and Georgia in this alternate history. Ferdinando's Sicilian titles and Palermo castle use feudal government. The Ottoman ruler uses CK3's Maturidi Sunni faith, the closest built-in representation of Hanafi Sunni practice, and holds the Sunni caliphate title. These changes require an in-game check after starting a new 1936 campaign.

All counties in CK3's Armenian kingdom are now Ottoman. Persia is playable under Ahmad Shah Qajar with Persian culture and Imami faith. Its 67 assigned counties cover the Iranian core of the CK3 Persian and Daylamite kingdoms, plus Iranian Khorasan, Sistan, and Baluchistan border counties. CK3's medieval counties only approximate the historical 1936 international boundary; Afghanistan, Turkmenistan, Pakistan, Iraq, and the Republic of Azerbaijan are not absorbed wholesale into Persia.

The Ottoman Empire now uses its own empire title, with dynasty-based title naming disabled. The Sultan, Abbas II of Egypt, and Idris I of Tripolitania all have Maturidi faith in generated character history; the Sultan also holds `d_sunni` as caliph. CK3 requires `religion =` in character history: earlier builds incorrectly wrote `rite =`, which caused the game to assign an unintended faith. The Ottoman-Persian borderlands in CK3's Jazira kingdom now belong to the Ottomans.

## References

The 1936 European layout was compared with the [Kaiserreich map supplied by the user](https://i.redd.it/qd9pz84qxji41.png) and [Kaiserreich's public starting-state files](https://github.com/Kaiserreich/Kaiserreich-4) at commit `699a5d0f49236e5033fa619f02a2078e93b84f5c`. CK3 file formats were checked against the user's game-data archive and the public [CK3 modding wiki mirror](https://github.com/jesec/ck3-modding-wiki). Those reference files are not copied into the mod.
