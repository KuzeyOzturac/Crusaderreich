#!/usr/bin/env python3
import csv
from pathlib import Path
root = Path(__file__).resolve().parents[1]
def rows(name):
    with (root / 'data' / name).open(newline='') as file:
        return list(csv.DictReader(file))
nations = rows('nations.csv')
characters = rows('characters.csv')
assignments = rows('title_assignments.csv')
counties = rows('county_map.csv')
tags = {row['tag'] for row in nations}
assert len(tags) == len(nations)
assert len({row['id'] for row in characters}) == len(characters)
assert all(row['nation'] in tags for row in characters)
assert all(row['nation'] in tags for row in assignments + counties)
assert len({row['county'] for row in counties}) == len(counties)
assert all(not row['leader_id'] or row['leader_id'] in {c['id'] for c in characters} for row in nations)
print(f'{len(nations)} nations, {len(characters)} characters, {len(assignments)} source titles, {len(counties)} counties validated')
bookmark = (root/'Crusaderreich/common/bookmarks/bookmarks/crusaderreich_1936.txt').read_text()
character_history = (root/'Crusaderreich/history/characters/crusaderreich_1936.txt').read_text()
title_history = (root/'Crusaderreich/history/titles/crusaderreich_1936.txt').read_text()
for row in nations:
    if row['leader_id'] and row['ck3_region'] in {a['ck3_title'] for a in assignments} | {'e_germany','e_russia'}:
        assert f'history_id = {row["leader_id"]}' in bookmark
        assert f'{row["leader_id"]} = {{' in character_history
        assert f'{row["ck3_region"]} = {{' in title_history
assert bookmark.count('character = {') == 17
print('1936 bookmark and ruler/title references validated')
