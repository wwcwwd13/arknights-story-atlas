import urllib.request
from pathlib import Path

root = Path(__file__).resolve().parents[1]
out = root / 'assets' / 'emblems-official'
out.mkdir(exist_ok=True)
names = {
    'rhodes':'logo_rhodes.png', 'kazimierz':'logo_kazimierz.png',
    'yan':'logo_yan.png', 'leithanien':'logo_Leithanien.png',
    'babel':'logo_babel.png', 'sargon':'logo_sargon.png',
    'columbia':'logo_columbia.png', 'iberia':'logo_iberia.png',
    'victoria':'logo_victoria.png', 'kjerag':'logo_kjerag.png',
    'laterano':'logo_Laterano.png', 'siracusa':'logo_siracusa.png',
    'ursus':'logo_ursus.png', 'bolivar':'logo_bolivar.png',
    'aegir':'logo_egir.png',
}
for id, name in names.items():
    url = f'https://raw.githubusercontent.com/fexli/ArknightsResource/main/camplogo/{name}'
    request = urllib.request.Request(url, headers={'User-Agent':'StoryGraphic personal local atlas'})
    with urllib.request.urlopen(request, timeout=20) as response:
        content = response.read()
    if not content.startswith(b'\x89PNG\r\n\x1a\n'):
        raise RuntimeError(f'{id}: invalid PNG')
    (out / f'{id}.png').write_bytes(content)
    print(id, len(content))
