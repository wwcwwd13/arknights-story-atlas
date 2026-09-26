"""Cache the story synopsis pages used to review every non-main event."""
import concurrent.futures
import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'data.js').read_text(encoding='utf-8').split('window.STORY_DATA = ', 1)[1].rsplit(';', 1)[0])
OUT = ROOT / 'work' / 'synopses'
OUT.mkdir(exist_ok=True)

def get(event):
    title = urllib.parse.unquote(event['summarySource'].split('/wiki/', 1)[1]).replace('_', ' ')
    page = title + '/Synopsis'
    params = urllib.parse.urlencode({'action': 'parse', 'page': page, 'prop': 'wikitext', 'format': 'json'})
    request = urllib.request.Request('https://arknights.wiki.gg/api.php?' + params,
                                     headers={'User-Agent': 'StoryGraphic/1.0 (local fan timeline)'})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.load(response)
        if 'parse' not in result:
            return event['id'], page, None, result.get('error', {}).get('code', 'missing')
        content = result['parse']['wikitext']['*']
        (OUT / f"{event['id']}.txt").write_text(content, encoding='utf-8')
        return event['id'], page, len(content), None
    except Exception as exc:
        return event['id'], page, None, str(exc)

events = [event for event in DATA['events'] if event['type'] != 'main']
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(get, events))
manifest = {key: {'page': page, 'chars': length, 'error': error} for key, page, length, error in results}
(ROOT / 'work' / 'synopsis_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print('synopsis pages', sum(item['chars'] is not None for item in manifest.values()), '/', len(manifest))
print('missing:', [(key, item['error']) for key, item in manifest.items() if item['chars'] is None])
