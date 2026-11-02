"""Offline checks for the teaching HTML page; standard library only."""
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import sys

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.nodes = {}
        self.active = None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        key = attrs.get('id')
        if key in ('event-title', 'event-date', 'registration'):
            if key in self.nodes:
                raise ValueError('Duplicate id: ' + key)
            self.nodes[key] = [tag, attrs, '']
            self.active = key
    def handle_data(self, data):
        if self.active:
            self.nodes[self.active][2] += data
    def handle_endtag(self, tag):
        if self.active and self.nodes[self.active][0] == tag:
            self.active = None

def check(text):
    p = Page()
    try:
        p.feed(text)
    except ValueError as e:
        return [str(e)]
    errors = []
    title = p.nodes.get('event-title')
    if not title or title[0] != 'h1' or not title[2].strip():
        errors.append('TITLE: non-empty h1#event-title is required')
    event = p.nodes.get('event-date')
    try:
        if not event or event[0] != 'time':
            raise ValueError()
        raw = event[1].get('datetime', '')
        parsed = date.fromisoformat(raw)
        if raw != parsed.isoformat() or event[2].strip() != parsed.strftime('%d.%m.%Y'):
            raise ValueError()
    except ValueError:
        errors.append('DATE: use YYYY-MM-DD in datetime and matching DD.MM.YYYY text')
    link = p.nodes.get('registration')
    try:
        url = urlparse(link[1].get('href', '')) if link else urlparse('')
        valid = link and link[0] == 'a' and url.scheme == 'https' and url.hostname and link[2].strip()
    except ValueError:
        valid = False
    if not valid:
        errors.append('REGISTRATION: link must use https:// and include a hostname')
    return errors

if __name__ == '__main__':
    errors = check(Path(__file__).with_name('index.html').read_text(encoding='utf-8'))
    for error in errors:
        print('FAIL:', error)
    if not errors:
        print('PASS: HTML checks passed (README consistency requires human review)')
    sys.exit(1 if errors else 0)
