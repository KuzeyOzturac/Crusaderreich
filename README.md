# Crusaderreich

Crusaderreich adapts Kaiserreich into a monarchist German century after the Central Powers' victory. The present build uses CK3's original Old World map. It contains a 1936 bookmark and initial rulers and territory; events and decisions are deferred.

## Install and test

Copy this repository's `Crusaderreich` directory and `Crusaderreich.mod` file into your CK3 user `mod` directory, enable it in the launcher, and look for **The German Century** bookmark. The game installation is never modified. Start as a listed ruler, check their top title and counties, let one day pass, then inspect CK3's `error.log` for script errors. The launcher descriptor's supported-version line may need updating to your installed CK3 version.

This build has **not been launched in CK3** in the cloud environment. The supplied archive was read as source data only; the machine does not have the game executable. CK3 may reject the 1936 date or require additional title, government, religion, or map-history work. Do not treat the bookmark's presence in files as proof that the game loads it.

## Files

- `data/nations.csv` and `data/characters.csv` record the user-defined dynastic settlement.
- `data/title_assignments.csv` maps CK3 titles to nations. This is an approximation, not final Kaiserreich borders.
- `data/county_map.csv` is generated from the supplied CK3 landed-title hierarchy.
- `Crusaderreich/history/characters/crusaderreich_1936.txt` defines the named rulers and a non-playable Swiss council proxy.
- `Crusaderreich/history/titles/crusaderreich_1936.txt` assigns dated holders and resets inherited lieges on 1936.1.1. Only nations with a defined holder appear in the generated game history.
- `Crusaderreich/common/bookmarks` provides a selectable 1936 start.
- `Crusaderreich/common/dynasties` uses localization keys for surnames; given names are defined separately in character history. The localization file supplies dynasty names and bookmark names.

Some nations in the roster still lack a named ruler or map territory. The map is **not yet a complete or exact Kaiserreich map**; unassigned Old World counties retain vanilla history. The current assignments correct identified border errors but still need a comprehensive county pass. Unknown birth dates are currently set to `1885.1.1` in generated game files as a temporary age placeholder; the source roster leaves those dates blank. Corsica has selected North African holdings; its full French African territory and several borders still need manual county work. No American territory is planned. The supplied CK3 title tree confirms Japan is on the original map.

Run `python3 tools/validate.py` for data and reference checks. To update the map from CK3's landed-title files, run `python3 tools/build_map.py /path/to/game/common/landed_titles`, then `python3 tools/generate_scenario.py`. Both generators write only inside this mod repository.

## References and limits

The CK3 title and bookmark formats were checked against the game-data archive supplied by the user and the public [CK3 modding wiki mirror](https://github.com/jesec/ck3-modding-wiki), especially its dynasty, bookmark, and title-history pages. Baseline 1936 ownership was checked against [Kaiserreich’s public starting-state files](https://github.com/Kaiserreich/Kaiserreich-4) at commit `699a5d0f49236e5033fa619f02a2078e93b84f5c`. Crusaderreich’s user-defined monarchies override Kaiserreich’s politics. The reference files are not copied into the mod.

In-game testing remains required. A user reported that the earlier bookmark did not appear and that dynasties displayed as “Fletcher.” The bookmark government requirement and dynasty localization have been corrected in source, but those corrections have not yet been verified in CK3.
