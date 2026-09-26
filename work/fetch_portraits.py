"""Save small character portraits for the local story timeline."""
import concurrent.futures
import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAMES = {
    'amiya': 'Amiya', 'doctor': 'Doctor', 'kaltsit': "Kal'tsit",
    'theresa': 'Theresa', 'theresis': 'Theresis', 'ascalon': 'Ascalon',
    'w': 'W', 'ines': 'Ines', 'nearl': 'Nearl',
    'maria-nearl': 'Blemishine', 'mlynar': 'Młynar', 'platinum': 'Platinum',
    'texas': 'Texas', 'lappland': 'Lappland', 'penance': 'Penance',
    'vigil': 'Vigil', 'specter': 'Specter', 'irene': 'Irene',
    'lumen': 'Lumen', 'ulpianus': 'Ulpianus', 'silverash': 'SilverAsh',
    'pramanix': 'Pramanix', 'gnosis': 'Gnosis', 'dorothy': 'Dorothy',
    'saria': 'Saria', 'kristen': 'Kristen Wright', 'skadi': 'Skadi',
    'gladiia': 'Gladiia', 'anita': 'Anita', 'quintus': 'Quintus',
    'dario': 'Dario', 'first-to-talk': 'The First To Talk', 'zima': 'Zima',
    'leto': 'Leto', 'gummy': 'Gummy', 'rosa': 'Rosa',
    'absinthe': 'Absinthe', 'dur-nar': 'Dur-nar',
    'crownslayer': 'Crownslayer', 'antosha': 'Antosha',
    'matvey': 'Matvey', 'pavlovich': 'Pavlovich',
}

def fetch(item):
    key, name = item
    params = urllib.parse.urlencode({
        'action': 'query', 'titles': f'File:{name} icon.png',
        'prop': 'imageinfo', 'iiprop': 'url', 'format': 'json',
    })
    request = urllib.request.Request('https://arknights.wiki.gg/api.php?' + params,
                                     headers={'User-Agent': 'StoryGraphic/1.0 (local fan timeline)'})
    data = json.load(urllib.request.urlopen(request, timeout=20))
    page = next(iter(data['query']['pages'].values()))
    if 'imageinfo' not in page:
        return key, None, None
    url = page['imageinfo'][0]['url']
    image = urllib.request.urlopen(urllib.request.Request(url, headers={
        'User-Agent': 'StoryGraphic/1.0 (local fan timeline)'}), timeout=20).read()
    if image[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError(f'{key}: not PNG')
    path = ROOT / 'assets' / 'portraits' / f'{key}.png'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(image)
    return key, url, len(image)

def main():
    sources = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(fetch, NAMES.items()))
    for key, url, size in results:
        print(key, size or 'MISSING')
        if url:
            sources[key] = url
    (ROOT / 'work' / 'portrait_sources.json').write_text(
        json.dumps(sources, ensure_ascii=False, indent=2), encoding='utf-8')
    print('saved', len(sources), 'of', len(NAMES))

if __name__ == '__main__':
    main()
