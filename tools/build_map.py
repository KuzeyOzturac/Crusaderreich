#!/usr/bin/env python3
"""Derive county-level scenario planning assignments from a CK3 landed-title tree."""
import csv
from collections import Counter, defaultdict
import re
import sys
from pathlib import Path

source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/tmp/ck3map/common/landed_titles')
root = Path(__file__).resolve().parents[1]
parent = {}
for path in sorted(source.glob('*.txt')):
    stack = []
    for raw in path.read_text(encoding='utf-8-sig').splitlines():
        line = raw.split('#', 1)[0]
        match = re.search(r'\b([ekdcb]_[A-Za-z0-9_-]+)\s*=\s*\{', line)
        title = match.group(1) if match else None
        if title:
            parent[title] = next((item for item in reversed(stack) if item and item.startswith(('e_', 'k_', 'd_', 'c_'))), '')
        for char in re.sub(r'"[^"]*"', '', line):
            if char == '{':
                stack.append(title)
                title = None
            elif char == '}' and stack:
                stack.pop()

with (root / 'data' / 'title_assignments.csv').open(newline='') as file:
    assignments = list(csv.DictReader(file))
missing = [row['ck3_title'] for row in assignments if row['ck3_title'] not in parent]
if missing:
    raise SystemExit(f'Unknown CK3 titles: {missing}')

def ancestor(county, target):
    seen = set()
    current = county
    while current and current not in seen:
        if current == target:
            return True
        seen.add(current)
        current = parent.get(current)
    return False

out = []
for county in sorted(title for title in parent if title.startswith('c_')):
    matches = [row for row in assignments if ancestor(county, row['ck3_title'])]
    if matches:
        distance = {}
        current = county
        depth = 0
        while current:
            distance[current] = depth
            current = parent.get(current)
            depth += 1
        selected = min(matches, key=lambda row: distance[row['ck3_title']])
        out.append({'county': county, 'nation': selected['nation'], 'source_title': selected['ck3_title']})
with (root / 'data' / 'county_map.csv').open('w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['county', 'nation', 'source_title'], lineterminator='\n')
    writer.writeheader()
    writer.writerows(out)
owner_by_county = {row['county']: row['nation'] for row in out}
total_count = Counter()
owner_count = defaultdict(Counter)
for county in (title for title in parent if title.startswith('c_')):
    current = parent.get(county)
    while current:
        if current.startswith(('d_', 'k_')):
            total_count[current] += 1
            if county in owner_by_county:
                owner_count[current][owner_by_county[county]] += 1
        current = parent.get(current)
complete_titles = []
for title, count in sorted(total_count.items()):
    owners = owner_count[title]
    if len(owners) == 1 and sum(owners.values()) == count:
        complete_titles.append({'title': title, 'nation': next(iter(owners)), 'counties': count})
with (root / 'data' / 'complete_titles.csv').open('w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['title', 'nation', 'counties'], lineterminator='\n')
    writer.writeheader()
    writer.writerows(complete_titles)
print(f'Mapped {len(out)} counties from {len(assignments)} CK3 titles')
