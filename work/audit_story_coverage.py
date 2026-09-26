"""Print coverage and likely missing characters from saved story synopses."""
import collections
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
work = root / 'work'
data = json.loads((root / 'data.js').read_text(encoding='utf-8').split(
    'window.STORY_DATA = ', 1)[1].rsplit(';', 1)[0])
events = {event['id']: event for event in data['events']}
people = {person['id']: person for person in data['people']}
appearances = collections.defaultdict(set)
actions = collections.Counter()
for item in data['appearances']:
    appearances[item['event']].add(item['person'])
for item in data['actions']:
    actions[item['event']] += 1
print('APPEARANCE DISTRIBUTION', sorted(collections.Counter(map(len, appearances.values())).items()))
print('ACTION DISTRIBUTION', sorted(collections.Counter(actions.values()).items()))
for event_id in sorted(events, key=lambda key: (len(appearances[key]), actions[key], key)):
    path = work / 'synopses' / f'{event_id}.txt'
    links = collections.Counter()
    if path.exists():
        text = path.read_text(encoding='utf-8')
        links = collections.Counter(re.findall(r'\[\[([^|\]]+)(?:\|[^\]]+)?\]\]', text))
    top = ', '.join(f'{title}:{count}' for title, count in links.most_common(10)
                    if not title.startswith(('File:', 'Category:', 'wikipedia:')))
    print(f'{event_id:22} cast={len(appearances[event_id]):2} actions={actions[event_id]:2} '
          f'synopsis={path.exists()} | {top}')
