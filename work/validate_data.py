"""Check referential integrity and offline asset coverage for the story atlas."""
import json
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root / 'data.js').read_text(encoding='utf-8').split('window.STORY_DATA = ', 1)[1].rsplit(';', 1)[0])
events = {item['id']: item for item in data['events']}
lanes = {item['id']: item for item in data['lanes']}
people = {item['id']: item for item in data['people']}
assert len(events) == len(data['events']) == 89
assert len(lanes) == len(data['lanes'])
assert [lane['id'] for lane in data['lanes'][:7]] == [
    'rhodes', 'reunion', 'victoria', 'ursus', 'kazimierz', 'siesta', 'yan']
remaining_lanes = data['lanes'][4:]
assert remaining_lanes == sorted(remaining_lanes, key=lambda lane: (
    min(event['date'] for event in data['events'] if event['lane'] == lane['id']),
    lane['name'],
))
assert len(people) == len(data['people'])
assert len(data['art']) == len(data['artCredits']) == len(events)
assert [event['date'] for event in data['events']] == sorted(event['date'] for event in data['events'])
assert {event['id'] for event in data['events'] if event['dateStatus'] == 'projected'} == {
    'main-17', 'foam-thunder', 'jungle-knot', 'lime', 'moon-water'}
assert events['people-us']['lane'] == 'ursus'
assert data['artKind'] == {'main-00-04': 'shared'}
sequences = {item['id']: item for item in data['sequences']}
assert len(sequences) == len(data['sequences']) == 18
sequence_members = [event_id for item in data['sequences'] for event_id in item['events']]
assert len(sequence_members) == 92
assert set(sequence_members) == set(events)
assert sum(item.get('kind') == 'theme' for item in data['sequences']) == 8
crosslinks = data['crosslinks']
assert len(crosslinks) == 31
assert len({frozenset((item['from'], item['to'])) for item in crosslinks}) == len(crosslinks)
for item in crosslinks:
    assert item['from'] in events and item['to'] in events and item['from'] != item['to'], item
    assert item['label'] and item['note'] and item['source'].startswith('https://'), item
assert sum(event['summarySource'].endswith('/Synopsis') for event in events.values()) == 82
assert events['dreamtalk']['summarySource'] == 'https://arknights.wiki.gg/wiki/SS-8/Story'
assert sum('koreanStoryUrl' in event for event in events.values()) == 85
assert sum('koreanInfoUrl' in event for event in events.values()) == 3
assert [event['id'] for event in data['events'] if not event.get('koreanStoryUrl') and not event.get('koreanInfoUrl')] == ['moon-water']
assert events['main-00-04']['koreanStoryExtraUrl'].endswith('#s-2')
for sequence in data['sequences']:
    assert len(sequence['events']) >= 2, sequence['id']
    assert sequence['events'] == sorted(sequence['events'], key=lambda event_id: (events[event_id]['date'], event_id)), sequence['id']
    if sequence.get('source'):
        assert sequence['source'].startswith('https://'), sequence['id']

for event in events.values():
    assert event['lane'] in lanes, event['id']
    assert event['summary'] and event['summarySource'], event['id']
    for field in ('koreanStoryUrl', 'koreanInfoUrl', 'koreanStoryExtraUrl'):
        if event.get(field):
            assert event[field].startswith('https://namu.moe/w/'), (event['id'], field)
    assert len(event['summary']) >= 100, event['id']
    assert event['sequences'] == [item['id'] for item in data['sequences'] if event['id'] in item['events']], event['id']
    assert event['factions'] and len(event['factions']) == len(set(event['factions'])), event['id']
    assert event['id'] in data['art'], event['id']
    assert event['id'] in data['artCredits'], event['id']
    if event['dateStatus'] == 'projected':
        assert event['date'] == event['projectionMonth'] + '-15', event['id']
    asset = root / data['art'][event['id']]
    assert asset.is_file() and asset.stat().st_size > 50000, asset
    header = asset.read_bytes()[:12]
    assert header.startswith((b'\xff\xd8\xff', b'\x89PNG')) or (header.startswith(b'RIFF') and header[8:12] == b'WEBP'), asset
for lane in lanes.values():
    assert (root / lane['emblem']).is_file(), lane['id']
    if lane.get('secondaryEmblem'):
        assert (root / lane['secondaryEmblem']).is_file(), lane['id']
for person in people.values():
    if person.get('portrait'):
        assert person['portraitSource'], person['id']
        portrait = root / person['portrait']
        assert portrait.is_file() and portrait.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'), person['id']
for relation in data['appearances']:
    assert relation['event'] in events and relation['person'] in people, relation
    assert relation.get('source', events[relation['event']]['summarySource']).startswith('https://'), relation
for relation in data['affiliations']:
    assert relation['lane'] in lanes and relation['person'] in people, relation
for action in data['actions']:
    assert action['event'] in events and action['person'] in people, action
    assert action['text'] and len(action['text']) >= 10, action
assert len({(item['event'], item['person']) for item in data['appearances']}) == len(data['appearances'])
appearance_pairs = {(item['event'], item['person']) for item in data['appearances']}
assert all((item['event'], item['person']) in appearance_pairs for item in data['actions'])
appearances_by_event = Counter(item['event'] for item in data['appearances'])
actions_by_event = Counter(item['event'] for item in data['actions'])
assert all(appearances_by_event[event_id] >= 1 for event_id in events)
assert all(actions_by_event[event_id] >= 10 for event_id in events)
assert {'wiki-botani', 'wiki-fyodor-vladimirovich', 'prts-faddey', 'prts-leonid-grashvili'} <= {
    item['person'] for item in data['appearances'] if item['event'] == 'people-us'}
assert all(appearances_by_event[event_id] >= 9 for event_id in
           ('main-17', 'foam-thunder', 'jungle-knot', 'lime', 'moon-water'))
assert len({(action['event'], action['text']) for action in data['actions']}) == len(data['actions'])
for event in events.values():
    cast = {item['person'] for item in data['appearances'] if item['event'] == event['id']}
    order = event['peopleOrder']
    protagonists = event['protagonists']
    assert len(order) == len(cast) and set(order) == cast, event['id']
    assert protagonists and order[:len(protagonists)] == protagonists, event['id']
assert 'id="visibleCount"' not in (root / 'index.html').read_text(encoding='utf-8')
print(f"PASS: {len(events)} events, {len(lanes)} lanes, {len(data['art'])} offline images, "
      f"{len(people)} people, {len(data['appearances'])} appearances, {len(data['actions'])} actions, "
      f"{len(sequences)} story groups, {len(set(sequence_members))} linked cards, {len(crosslinks)} cross-story links")
