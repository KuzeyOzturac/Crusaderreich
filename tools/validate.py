#!/usr/bin/env python3
import csv
import re
from collections import Counter
from pathlib import Path
root = Path(__file__).resolve().parents[1]
assert 'supported_version="1.20.*"' in (root/'Crusaderreich.mod').read_text()
assert 'supported_version="1.20.*"' in (root/'Crusaderreich/descriptor.mod').read_text()
def rows(name):
    with (root / 'data' / name).open(newline='') as file:
        return list(csv.DictReader(file))
nations = rows('nations.csv')
characters = rows('characters.csv')
relatives = rows('relatives.csv')
parents = rows('parents.csv')
marriages = rows('marriages.csv')
assignments = rows('title_assignments.csv')
counties = rows('county_map.csv')
complete_titles = rows('complete_titles.csv')
tags = {row['tag'] for row in nations}
assert len(tags) == len(nations)
assert 'ARM' not in tags and 'PER' in tags
assert next(n for n in nations if n['tag'] == 'PER')['leader_id'] == '9000128'
assert len({row['id'] for row in characters}) == len(characters)
all_people = {row['id']: row for row in characters + relatives}
assert len(all_people) == len(characters) + len(relatives)
assert all(row['child_id'] in all_people and all(not row[key] or row[key] in all_people for key in ('father','mother')) for row in parents)
assert all(row['spouse1'] in all_people and row['spouse2'] in all_people for row in marriages)
assert all(row['nation'] in tags for row in characters)
assert all(row['nation'] in tags for row in assignments + counties)
assert len({row['county'] for row in counties}) == len(counties)
assert len({row['ck3_title'] for row in assignments}) == len(assignments)
expected_duchies = {'d_thessalonika':'BUL','d_strymon':'BUL','d_grodno':'LIT','d_latium':'PAP','d_spoleto':'PAP','d_ancona':'PAP','d_emilia':'ITA','d_romagna':'ITA','d_duortnoseatnu':'NOR','d_vuovdisamieana':'SWE','d_bar':'FRA','d_masuria':'GER','d_wielkopolska':'GER','d_courland':'UBD','d_latgalians':'UBD','d_friuli':'AUS','d_duklja':'CRB','d_thrace':'OTT','d_aegean_islands':'OTT','d_krete':'OTT','d_tripolitania':'TRI','d_syrte':'TRI','k_egypt':'EGY','k_nubia':'EGY','k_blemmyia':'EGY','d_karachev':'RUS','d_novosil':'RUS','d_don_valley':'UKR','d_tana':'UKR','d_azov':'UKR','d_skane':'SWE','d_upper_lorraine':'GER','d_guoldat':'FIN'}
complete_owner = {row['title']:row['nation'] for row in complete_titles}
assert all(complete_owner.get(title) == nation for title,nation in expected_duchies.items())
assert complete_owner.get('k_armenia') == 'OTT'
assert all(complete_owner.get(title) == 'PER' for title in ('k_persia','d_nishapur','d_kohestan','d_jabal_kufs'))
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
    n['leader_id'] and next(c['role'] for c in characters if c['id'] == n['leader_id']) == 'head_of_state' and 'republic' not in n['government'].lower() and 'theocracy' not in n['government'].lower()
    for n in nations
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
for county,owner in {'c_bethen':'GAL','c_ratibor':'GAL','c_cieszyn':'GAL','c_sandomierska':'POL','c_radomska':'POL','c_stezycka':'POL','c_lubelska':'POL','c_cherven':'UKR','c_berestye':'LIT','c_dorohychyn':'LIT'}.items():
    assert county_owner[county] == owner
for county, owner in {
    'c_ajaccio': 'COR', 'c_bern': 'SWI', 'c_zurich': 'SWI',
    'c_vienna': 'AUS', 'c_krakowska': 'GAL', 'c_lviv': 'GAL',
    'c_minsk': 'WHR', 'c_konigsberg': 'GER', 'c_roma': 'PAP',
    'c_lisboa': 'POR', 'c_savoie': 'SRD', 'c_aosta': 'SRD',
    'c_canavese': 'SRD', 'c_firenze': 'TUS',
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
        assert f' {row["ck3_region"]}:0 "{row["title_name"]}"' in localization
        assert not row['title_name'].startswith(('Kingdom of ', 'Empire of ', 'Principality of '))
assert next(c for c in characters if c['nation'] == 'ROM')['culture'] == 'vlach'
assert 'culture = "vlach"' in character_history
assert 'culture = vlach' in bookmark
assert next(c for c in characters if c['nation'] == 'BOH')['name'] == 'Albrecht Franz von Habsburg'
assert next(c for c in characters if c['nation'] == 'TUS')['name'] == 'Peter Ferdinand of Habsburg'
assert 'government = feudal_government' in title_history.split('k_sicily = {', 1)[1].split('}', 1)[0]
assert 'b_palermo = {\n    1936.1.1 = {\n        holder = 9000052\n        liege = c_palermo\n        government = feudal_government' in title_history
assert character_history.count('9000063 = {') == 1
assert all(f'{title} = {{\n    1936.1.1 = {{\n        holder = 9000063' in title_history for title in ('k_ireland','k_georgia'))
assert next(c for c in characters if c['nation'] == 'OTT')['religion'] == 'maturidi'
assert 'rite = "maturidi"' in character_history
assert '9000128 = {\n    name = "Ahmad Shah"\n    culture = "persian"' in character_history
assert 'rite = "imami"' in character_history
assert 'k_armenia = {\n    1936.1.1 = {\n        holder = 9000055' in title_history
assert 'k_persia = {\n    1936.1.1 = {\n        holder = 9000128' in title_history
known_cultures = {'armenian','bulgarian','castilian','croatian','danish','dutch','egyptian','english','french','georgian','german','greek','hungarian','irish','italian','japanese','maghrebi','norwegian','persian','portuguese','russian','serbian','swabian','swedish','turkish','vlach'}
assert set(re.findall(r'culture = "([^"]+)"', character_history)) <= known_cultures
assert 'c_turin,SRD,' in (root/'data/county_map.csv').read_text()
assert title_history.count('\n        liege = 0') >= sum(bool(n['leader_id']) and not n['liege_tag'] for n in nations)
assert title_history.count('\n        liege = ') == title_history.count('1936.1.1 = {')
for row in parents:
    block = character_history.split(f"{row['child_id']} = {{",1)[1].split('\n}',1)[0]
    assert all(not row[role] or f'{role} = {row[role]}' in block for role in ('father','mother'))
for row in marriages:
    assert f"add_spouse = {row['spouse2']}" in character_history
for title in ('k_egypt','k_nubia','k_blemmyia','k_tripolitania'):
    assert f'{title} = {{\n    1936.1.1 = {{' in title_history
assert 'd_sunni = {\n    1936.1.1 = {\n        holder = 9000055' in title_history
assert 'd_venice = {\n    1936.1.1 = {\n        holder = 9000050\n        liege = k_cr_italy' in title_history
assert 'd_toscana = {\n    1936.1.1 = {\n        holder = 9000051\n        liege = k_cr_tuscany' in title_history
print('Dynasty names, landed rulers, and 1936 realm hierarchy validated')
