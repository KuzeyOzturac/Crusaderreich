#!/usr/bin/env python3
"""Generate a first CK3 1936 bookmark from the scenario tables.

Writes only inside this mod checkout. Never reads or writes the CK3 installation.
"""
import csv
from pathlib import Path

root = Path(__file__).resolve().parents[1]
mod = root / 'Crusaderreich'
def rows(name):
    with (root/'data'/name).open(newline='') as f: return list(csv.DictReader(f))
nations = rows('nations.csv')
people = {r['id']: r for r in rows('characters.csv')}
counties = rows('county_map.csv')
assignments = rows('title_assignments.csv')
valid_title = {r['ck3_title'] for r in assignments} | {'e_germany', 'e_russia'}
active = [n for n in nations if n['leader_id'] and n['ck3_region'] in valid_title]
bookmarked = [n for n in active if n['tag'] != 'SWI']
# These are deliberately scenario defaults; exact identities and birth dates can be refined.
culture = {'GER':'german','AUS':'german','GAL':'german','HUN':'hungarian','UKR':'russian','CRB':'croatian','FRA':'french','COR':'french','ENG':'english','POL':'german','FLW':'german','WHR':'german','LIT':'german','FIN':'german','RUS':'russian','UBD':'german','ALB':'german','SWI':'swabian'}
dynasty_name = {'GER':'Hohenzollern','POL':'Hohenzollern','FLW':'Hohenzollern','WHR':'Hohenzollern','AUS':'Habsburg','GAL':'Habsburg','HUN':'Habsburg','UKR':'Habsburg','CRB':'Habsburg','FRA':'Orléans','COR':'Bonaparte','ENG':'Windsor','RUS':'Romanov','LIT':'Urach','FIN':'Hesse-Kassel','UBD':'Mecklenburg-Schwerin','ALB':'Wied'}
dynasty_ids = {name: 9900000 + index for index, name in enumerate(sorted(set(dynasty_name.values())), 1)}
given_name = {'GER':'Wilhelm','FRA':'Jean','ENG':'George','AUS':'Karl','HUN':'Joseph August','POL':'August Wilhelm','UKR':'Wilhelm Franz','RUS':'Vladimir','COR':'Louis','GAL':'Karl Albrecht','CRB':'Leopold Salvator','ALB':'Wilhelm','FLW':'Adalbert','WHR':'Oskar','LIT':'Karl Gero','FIN':'Friedrich Karl','UBD':'Adolf Friedrich','SWI':'Federal Council'}
dynasty_key = {name: 'dynn_cr_' + name.lower().replace('-', '_').replace('é','e') for name in dynasty_ids}
(mod/'common/dynasties').mkdir(exist_ok=True)
(mod/'common/dynasties/crusaderreich_dynasties.txt').write_text('\n'.join(f'{value} = {{ name = {dynasty_key[name]} culture = {"french" if name in ("Bonaparte", "Orléans") else "english" if name == "Windsor" else "russian" if name == "Romanov" else "german"} }}' for name,value in dynasty_ids.items())+'\n')
chars = ['# Generated Crusaderreich 1936 rulers.']
for n in active:
    p = people[n['leader_id']]
    born = p['birth'] or '1885.1.1'
    chars += [f"{p['id']} = {{",f'    name = "{given_name[n["tag"]]}"',f'    culture = "{p["culture"] or culture.get(n["tag"],"german")}"']
    if n['tag'] in dynasty_name:
        chars.append(f'    dynasty = {dynasty_ids[dynasty_name[n["tag"]]]}')
    chars += ['    rite = "roman_rite"',f'    {born} = {{ birth = yes }}','}','']
(mod/'history/characters/crusaderreich_1936.txt').write_text('\n'.join(chars))
# Date entries in separate mod history files override the medieval holder at the bookmark.
holders = {}
for n in active:
    holders[n['ck3_region']] = n['leader_id']
for assignment in assignments:
    n = next((n for n in active if n['tag'] == assignment['nation']), None)
    if n:
        holders[assignment['ck3_title']] = n['leader_id']
for c in counties:
    n = next((n for n in active if n['tag'] == c['nation']), None)
    if n: holders[c['county']] = n['leader_id']
title_lines=['# Generated 1936 title holders for scenario-assigned titles.']
for title, holder in sorted(holders.items()):
    title_lines += [f'{title} = {{','    1936.1.1 = {',f'        holder = {holder}','        liege = 0']
    if holder == '9000032' and title == 'k_switzerland':
        title_lines.append('        government = republic_government')
    title_lines += ['    }','}','']
(mod/'history/titles/crusaderreich_1936.txt').write_text('\n'.join(title_lines))
(mod/'common/bookmarks/groups/crusaderreich_groups.txt').write_text('bm_group_crusaderreich_1936 = {\n    default_start_date = 1936.1.1\n}\n')
bookmark=['bm_crusaderreich_1936 = {','    start_date = 1936.1.1','    is_playable = yes','    group = bm_group_crusaderreich_1936','    weight = { value = 100 }']
for n in bookmarked:
    p=people[n['leader_id']]
    bookmark += ['    character = {',f'        name = "cr_bookmark_{n["tag"].lower()}"',f'        history_id = {p["id"]}',f'        title = {n["ck3_region"]}',f'        birth = {p["birth"] or "1885.1.1"}','        type = male',f'        dynasty = {dynasty_ids[dynasty_name[n["tag"]]]}','        dynasty_splendor_level = 1',f'        culture = {p["culture"] or culture.get(n["tag"],"german")}',f'        religion = {"orthodox" if n["tag"] == "RUS" else "catholic"}','        government = feudal_government','        difficulty = "BOOKMARK_CHARACTER_DIFFICULTY_EASY"','    }']
bookmark += ['}','']
(mod/'common/bookmarks/bookmarks/crusaderreich_1936.txt').write_text('\n'.join(bookmark))
loc=['\ufeffl_english:',' bm_group_crusaderreich_1936:0 "Crusaderreich: 1936"',' bm_crusaderreich_1936:0 "The German Century"']
for name, key in dynasty_key.items():
    loc.append(f' {key}:0 "{name}"')
for n in active:
    key=f'cr_bookmark_{n["tag"].lower()}'
    loc += [f' {key}:0 "{n["leader"]}"',f' {key}_desc:0 "Rule {n["name"]} in the German Century."',f' {key}_subheading:0 "{n["name"]}"']
(mod/'localization/english/crusaderreich_1936_l_english.yml').write_text('\n'.join(loc)+'\n',encoding='utf-8')
print(f'Generated {len(bookmarked)} bookmark rulers and {len(holders)} title holders')
