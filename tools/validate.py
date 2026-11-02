#!/usr/bin/env python3
import csv
from collections import Counter
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
assert len({row['ck3_title'] for row in assignments}) == len(assignments)
assert all(not row['leader_id'] or row['leader_id'] in {c['id'] for c in characters} for row in nations)
print(f'{len(nations)} nations, {len(characters)} characters, {len(assignments)} source titles, {len(counties)} counties validated')
bookmark = (root/'Crusaderreich/common/bookmarks/bookmarks/crusaderreich_1936.txt').read_text()
character_history = (root/'Crusaderreich/history/characters/crusaderreich_1936.txt').read_text()
title_history = (root/'Crusaderreich/history/titles/crusaderreich_1936.txt').read_text()
for row in nations:
    if row['leader_id'] and row['ck3_region'] in {a['ck3_title'] for a in assignments} | {'e_germany','e_russia','e_carpathia', 'k_maghreb'}:
        person = next(c for c in characters if c['id'] == row['leader_id'])
        if person['role'] == 'head_of_state' and 'republic' not in row['government'].lower() and 'theocracy' not in row['government'].lower():
            assert f'history_id = {row["leader_id"]}' in bookmark
        assert f'{row["leader_id"]} = {{' in character_history
        assert f'{row["ck3_region"]} = {{' in title_history
assert bookmark.count('character = {') == sum(
    c['role'] == 'head_of_state' and 'republic' not in next(n['government'] for n in nations if n['tag'] == c['nation']).lower() and 'theocracy' not in next(n['government'] for n in nations if n['tag'] == c['nation']).lower()
    for c in characters
)
print('1936 bookmark and ruler/title references validated')

for block in bookmark.split("    character = {")[1:]:
    entry = block.split("    }", 1)[0]
    for required in ("history_id =", "title =", "government =", "culture =", "religion =", "dynasty =", "dynasty_splendor_level =", "difficulty ="):
        assert required in entry, f"Bookmark character missing {required}"
print("Required bookmark character fields validated")
county_counts = Counter(row['nation'] for row in counties)
assert all(county_counts[row['tag']] for row in nations if row['leader_id']), 'A bookmarked ruler has no assigned county'
county_owner = {row['county']: row['nation'] for row in counties}
for county, owner in {
    'c_ajaccio': 'COR', 'c_bern': 'SWI', 'c_zurich': 'SWI',
    'c_vienna': 'AUS', 'c_krakowska': 'GAL', 'c_lviv': 'GAL',
    'c_minsk': 'WHR', 'c_konigsberg': 'GER', 'c_roma': 'PAP',
    'c_lisboa': 'POR', 'c_savoie': 'SWI', 'c_aosta': 'SRI',
}.items():
    assert county_owner.get(county) == owner, f'{county} must belong to {owner}'
dynasties = (root/'Crusaderreich/common/dynasties/crusaderreich_dynasties.txt').read_text()
localization = (root/'Crusaderreich/localization/english/crusaderreich_1936_l_english.yml').read_text(encoding='utf-8-sig')
for line in dynasties.splitlines():
    key = line.split('name = ', 1)[1].split()[0]
    assert f'{key}:0 ' in localization, f'Missing dynasty localization: {key}'
assert 'Fletcher' not in character_history + dynasties + localization
assert 'name = "George V Windsor"' not in character_history
custom_titles = (root/'Crusaderreich/common/landed_titles/crusaderreich_titles.txt').read_text()
for row in nations:
    if row['ck3_region'].startswith('k_cr_'):
        assert f'{row["ck3_region"]} = {{' in custom_titles
    if row['leader_id']:
        assert f' {row["ck3_region"]}:0 "{row["name"]}"' in localization
assert title_history.count('liege = 0') == title_history.count('1936.1.1 = {')
print('Dynasty names, landed rulers, and 1936 independence validated')
