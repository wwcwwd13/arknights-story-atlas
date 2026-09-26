"""Inspect high resolution images on a Bwiki event page."""
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser


class Images(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag != 'img':
            return
        item = dict(attrs)
        if int(item.get('data-file-width') or 0) >= 700:
            print(item.get('alt'), item.get('data-file-width'), item.get('data-file-height'), item.get('src'))


title = sys.argv[1]
url = 'https://wiki.biligame.com/arknights/' + urllib.parse.quote(title)
request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(request, timeout=25) as response:
    page = response.read().decode('utf-8', 'replace')
print('PAGE', title, len(page))
Images().feed(page)
