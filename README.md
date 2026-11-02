# Crusaderreich

Crusaderreich adapts Kaiserreich into a monarchist German century after the Central Powers' victory. The present build uses CK3's original Old World map. It contains a 1936 bookmark and initial rulers and territory; events and decisions are deferred.

## Install and test

Copy this repository's `Crusaderreich` directory and `Crusaderreich.mod` file into your CK3 user `mod` directory, enable it in the launcher, and look for **The German Century** bookmark. The game installation is never modified. Start as a listed ruler, check their top title and counties, let one day pass, then inspect CK3's `error.log` for script errors. The launcher descriptor's supported-version line may need updating to your installed CK3 version.

This build has **not been launched in CK3** in the cloud environment. The supplied archive was read as source data only; the machine does not have the game executable. CK3 may reject the 1936 date or require additional title, government, religion, or map-history work. Do not treat the bookmark's presence in files as proof that the game loads it.

## Files

- `data/nations.csv` and `data/characters.csv` record the user-defined dynastic settlement.
- `data/title_assignments.csv` maps CK3 titles to nations. This is an approximation, not final Kaiserreich borders.
- `data/county_map.csv` is generated from the supplied CK3 landed-title hierarchy.
- `Crusaderreich/history/characters/crusaderreich_1936.txt` defines 17 initial rulers.
- `Crusaderreich/history/titles/crusaderreich_1936.txt` assigns their primary titles and 514 counties on 1936.1.1.
- `Crusaderreich/common/bookmarks` provides a selectable 1936 start.
- `Crusaderreich/common/dynasties` and localization provide ruler dynasties and bookmark names.

Some nations in the roster still lack a named ruler or map territory. Unknown birth dates are currently set to `1885.1.1` in generated game files as a temporary age placeholder; the source roster leaves those dates blank. Corsica's French African holdings and several borders need manual county work. No American territory is planned. The supplied CK3 title tree confirms Japan is on the original map.

Run `python3 tools/validate.py` for data and reference checks. To update the map from CK3's landed-title files, run `python3 tools/build_map.py /path/to/game/common/landed_titles`, then `python3 tools/generate_scenario.py`. Both generators write only inside this mod repository.
