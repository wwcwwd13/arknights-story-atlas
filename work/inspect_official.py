"""List image URLs embedded in an official Arknights news page."""
import html
import re
import sys
import urllib.request

url = sys.argv[1]
request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(request, timeout=25) as response:
    page = html.unescape(response.read().decode('utf-8', 'replace')).replace('\\/', '/')
urls = list(dict.fromkeys(re.findall(r'https?://[^\s"<>]+?\.(?:jpg|png|webp)', page)))
print('PAGE', url, len(page), 'IMAGES', len(urls))
for image in urls[:35]:
    print(image)
