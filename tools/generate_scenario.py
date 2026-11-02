#!/usr/bin/env python3
"""Generate a first CK3 1936 bookmark from the scenario tables.

Writes only inside this mod checkout. Never reads or writes the CK3 installation.
"""
import csv
import unicodedata
from pathlib import Path

root = Path(__file__).resolve().parents[1]
mod = root / 'Crusaderreich'
def rows(name):
    with (root/'data'/name).open(newline='') as f: return list(csv.DictReader(f))
nations = rows('nations.csv')
people = {r['id']: r for r in rows('characters.csv')}
counties = rows('county_map.csv')
assignments = rows('title_assignments.csv')
complete_titles = rows('complete_titles.csv')
custom_titles = {'k_cr_corsica': ('c_ajaccio', (78, 67, 115)), 'k_cr_flanders_wallonia': ('c_brabant', (199, 166, 55)), 'k_cr_italian_republic': ('c_lombardia', (64, 135, 91)), 'k_cr_socialist_italy': ('c_turin', (139, 55, 55)), 'k_cr_papal_state': ('c_roma', (228, 210, 135))}
valid_title = {r['ck3_title'] for r in assignments} | {'e_germany', 'e_russia', 'e_carpathia', 'k_maghreb', 'k_galicia-volhynia', 'k_sardinia'} | set(custom_titles)
active = [n for n in nations if n['leader_id'] and n['ck3_region'] in valid_title]
bookmarked = [n for n in active if people[n['leader_id']]['role'] == 'head_of_state' and 'republic' not in n['government'].lower() and 'theocracy' not in n['government'].lower()]
# These are deliberately scenario defaults; exact identities and birth dates can be refined.
culture = {'GER':'german','AUS':'german','GAL':'german','HUN':'hungarian','UKR':'russian','CRB':'croatian','FRA':'french','COR':'french','ENG':'english','POL':'german','FLW':'german','WHR':'german','LIT':'german','FIN':'german','RUS':'russian','UBD':'german','ALB':'german','SWI':'swabian','ICE':'norwegian','IRE':'irish','DEN':'danish','NOR':'norwegian','SWE':'swedish','BOH':'czech','ROM':'romanian','SER':'serbian','BUL':'bulgarian','GRE':'greek','SPA':'castilian','POR':'portuguese','DKU':'russian','GEO':'georgian','ARM':'armenian','AZE':'azerbaijani','MOR':'maghrebi','ITA':'italian','SRI':'italian','SIC':'italian','PAP':'italian','SRD':'italian','OTT':'turkish','JAP':'japanese','NED':'dutch'}
dynasty_name = {'GER':'Hohenzollern','POL':'Hohenzollern','FLW':'Hohenzollern','WHR':'Hohenzollern','AUS':'Habsburg','GAL':'Habsburg','HUN':'Habsburg','UKR':'Habsburg','CRB':'Habsburg','FRA':'Orléans','COR':'Bonaparte','ENG':'Windsor','RUS':'Romanov','LIT':'Urach','FIN':'Hesse-Kassel','UBD':'Mecklenburg-Schwerin','ALB':'Wied','IRE':'Collins','DEN':'Glücksburg','NOR':'Glücksburg','SWE':'Bernadotte','ROM':'Hohenzollern-Sigmaringen','SER':'Karađorđević','BUL':'Saxe-Coburg-Gotha','GRE':'Glücksburg','SPA':'Bourbon','POR':'Braganza','MOR':'Alaouite','SIC':'Bourbon-Two Sicilies','SRD':'Savoy','OTT':'Osman','JAP':'Yamato','NED':'Orange-Nassau'}
dynasty_ids = {name: 9900000 + index for index, name in enumerate(sorted(set(dynasty_name.values())), 1)}
given_name = {'GER':'Wilhelm II','FRA':'Jean','ENG':'George V','AUS':'Karl I','HUN':'Joseph August','POL':'August Wilhelm','UKR':'Wilhelm Franz','RUS':'Vladimir Kirillovich','COR':'Louis','GAL':'Karl Albrecht','CRB':'Leopold Salvator','ALB':'Wilhelm','FLW':'Adalbert','WHR':'Oskar','LIT':'Karl Gero','FIN':'Friedrich Karl','UBD':'Adolf Friedrich','SWI':'Federal Council','IRE':'Michael','DEN':'Christian X','NOR':'Haakon VII','SWE':'Gustaf V','ROM':'Carol II','SER':'Peter II','BUL':'Boris III','GRE':'George II','SPA':'Alfonso XIII','POR':'Duarte II','MOR':'Mohammed V','SIC':'Ferdinando III','SRD':'Victor Emmanuel III','OTT':'Abdülmecid II','JAP':'Hirohito','NED':'Wilhelmina'}
dynasty_key = {name: 'dynn_cr_' + ''.join(c for c in unicodedata.normalize('NFKD', name.lower().replace('ß', 'ss')) if c.isascii() and (c.isalnum() or c == '-')).replace('-', '_') for name in dynasty_ids}
dynasty_culture = {'Alaouite':'maghrebi','Bernadotte':'swedish','Bonaparte':'french','Bourbon':'castilian','Bourbon-Two Sicilies':'italian','Braganza':'portuguese','Collins':'irish','Glücksburg':'danish','Habsburg':'german','Hesse-Kassel':'german','Hohenzollern':'german','Hohenzollern-Sigmaringen':'german','Karađorđević':'serbian','Mecklenburg-Schwerin':'german','Orange-Nassau':'dutch','Orléans':'french','Osman':'turkish','Romanov':'russian','Savoy':'italian','Saxe-Coburg-Gotha':'german','Urach':'german','Wied':'german','Windsor':'english','Yamato':'japanese'}
assert dynasty_ids.keys() <= dynasty_culture.keys()
(mod/'common/dynasties').mkdir(exist_ok=True)
dynasty_lines = []
for name, value in dynasty_ids.items():
    family_culture = dynasty_culture[name]
    prefix = ' prefix = dynnp_cr_d' if name == 'Orléans' else ' prefix = dynnp_cr_zu' if name == 'Wied' else ' prefix = dynnp_cr_de' if name == 'Braganza' else ' prefix = dynnp_cr_von' if name in ('Hohenzollern', 'Hohenzollern-Sigmaringen', 'Urach', 'Hesse-Kassel', 'Mecklenburg-Schwerin') else ''
    dynasty_lines.append(f'{value} = {{ name = {dynasty_key[name]} culture = {family_culture}{prefix} }}')
(mod/'common/dynasties/crusaderreich_dynasties.txt').write_text('\n'.join(dynasty_lines)+'\n')
(mod/'common/landed_titles').mkdir(exist_ok=True)
(mod/'common/landed_titles/crusaderreich_titles.txt').write_text('\n'.join(
    f'{title} = {{ color = {{ {r} {g} {b} }} capital = {capital} }}'
    for title, (capital, (r, g, b)) in custom_titles.items()
)+'\n')
chars = ['# Generated Crusaderreich 1936 rulers.']
for n in active:
    p = people[n['leader_id']]
    born = p['birth'] or '1885.1.1'
    chars += [f"{p['id']} = {{",f'    name = "{given_name.get(n["tag"], p["name"])}"',f'    culture = "{p["culture"] or culture.get(n["tag"],"german")}"']
    if n['tag'] in dynasty_name:
        chars.append(f'    dynasty = {dynasty_ids[dynasty_name[n["tag"]]]}')
    rite = {'orthodox':'byzantine_rite','ashari':'ashari','shinto':'shinto'}.get(p['religion'], 'roman_rite')
    chars += (['    female = yes'] if n['tag'] == 'NED' else []) + [f'    rite = "{rite}"',f'    {born} = {{ birth = yes }}','}','']
(mod/'history/characters/crusaderreich_1936.txt').write_text('\n'.join(chars))
# Date entries in separate mod history files override the medieval holder at the bookmark.
holders = {}
for n in active:
    holders[n['ck3_region']] = n['leader_id']
for assignment in assignments:
    n = next((n for n in active if n['tag'] == assignment['nation']), None)
    rank = {'c': 0, 'd': 1, 'k': 2, 'e': 3}
    if n and rank[assignment['ck3_title'][0]] <= rank[n['ck3_region'][0]]:
        holders[assignment['ck3_title']] = n['leader_id']
for item in complete_titles:
    n = next((n for n in active if n['tag'] == item['nation']), None)
    if n and rank[item['title'][0]] <= rank[n['ck3_region'][0]]:
        holders[item['title']] = n['leader_id']
for c in counties:
    n = next((n for n in active if n['tag'] == c['nation']), None)
    if n: holders[c['county']] = n['leader_id']
title_lines=['# Generated 1936 title holders for scenario-assigned titles.']
for title, holder in sorted(holders.items()):
    title_lines += [f'{title} = {{','    1936.1.1 = {',f'        holder = {holder}','        liege = 0']
    nation = next(n for n in active if n['leader_id'] == holder)
    if title == nation['ck3_region']:
        if 'republic' in nation['government'].lower():
            title_lines.append('        government = republic_government')
        elif 'theocracy' in nation['government'].lower():
            title_lines.append('        government = theocracy_government')
    title_lines += ['    }','}','']
(mod/'history/titles/crusaderreich_1936.txt').write_text('\n'.join(title_lines))
(mod/'common/bookmarks/groups/crusaderreich_groups.txt').write_text('bm_group_crusaderreich_1936 = {\n    default_start_date = 1936.1.1\n}\n')
bookmark=['bm_crusaderreich_1936 = {','    start_date = 1936.1.1','    is_playable = yes','    group = bm_group_crusaderreich_1936','    weight = { value = 100 }']
for n in bookmarked:
    p=people[n['leader_id']]
    bookmark += ['    character = {',f'        name = "cr_bookmark_{n["tag"].lower()}"',f'        history_id = {p["id"]}',f'        title = {n["ck3_region"]}',f'        birth = {p["birth"] or "1885.1.1"}','        type = female' if n['tag'] == 'NED' else '        type = male',f'        dynasty = {dynasty_ids[dynasty_name[n["tag"]]]}','        dynasty_splendor_level = 1',f'        culture = {p["culture"] or culture.get(n["tag"],"german")}',f'        religion = {p["religion"] or ("orthodox" if n["tag"] == "RUS" else "catholic")}','        government = feudal_government','        difficulty = "BOOKMARK_CHARACTER_DIFFICULTY_EASY"','    }']
bookmark += ['}','']
(mod/'common/bookmarks/bookmarks/crusaderreich_1936.txt').write_text('\n'.join(bookmark))
loc=['\ufeffl_english:',' bm_group_crusaderreich_1936:0 "Crusaderreich: 1936"',' bm_crusaderreich_1936:0 "The German Century"']
loc += [' dynnp_cr_d:0 "d\'"', ' dynnp_cr_von:0 "von "', ' dynnp_cr_zu:0 "zu "', ' dynnp_cr_de:0 "de "']
for name, key in dynasty_key.items():
    loc.append(f' {key}:0 "{name}"')
for n in active:
    loc.append(f' {n["ck3_region"]}:0 "{n["name"]}"')
for n in active:
    key=f'cr_bookmark_{n["tag"].lower()}'
    loc += [f' {key}:0 "{n["leader"]}"',f' {key}_desc:0 "Rule {n["name"]} in the German Century."',f' {key}_subheading:0 "{n["name"]}"']
(mod/'localization/english/crusaderreich_1936_l_english.yml').write_text('\n'.join(loc)+'\n',encoding='utf-8')
print(f'Generated {len(bookmarked)} bookmark rulers and {len(holders)} title holders')
