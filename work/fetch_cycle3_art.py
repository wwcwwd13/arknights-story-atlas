import ssl
import urllib.request
from pathlib import Path

root = Path(__file__).resolve().parents[1]
out = root / 'work' / 'candidates'
out.mkdir(exist_ok=True)
images = {
    'under-tides.jpg': 'https://ak.hycdn.cn/announce/images/20210424/5b73957f1556ecd805b62d4f08967af0.jpg',
    'lone-trail.jpg': 'https://gamerbraves.sgp1.cdn.digitaloceanspaces.com/2023/11/Arknights-Lone-Trail-Banner.jpg',
    'darknights.png': 'https://pinoygamer.ph/attachments/darknights-memoir-png.2320/',
    'break-ice.jpg': 'https://media.pocketgamer.com/artwork/na-31007-1656651840/arknights-break-the-ice-header_jpg_820.jpg',
    'lone-trail-mobile.jpg': 'https://pic.kts.g.mi.com/7dd485aae2b0540ddef84754b16067534142784951818178541.jpg',
}
for name, url in images.items():
    try:
        request = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(request, context=ssl._create_unverified_context(), timeout=20) as response:
            content = response.read()
            mime = response.headers.get('Content-Type', '')
        if not mime.startswith('image/') or not content.startswith((b'\xff\xd8', b'\x89PNG')):
            raise ValueError(f'unexpected response: {mime}, {len(content)} bytes')
        (out / name).write_bytes(content)
        print(name, mime, len(content))
    except Exception as exc:
        print(name, 'FAILED', exc)
