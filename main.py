"""
extract highlights from a kindle device

first, the kindle has to be mounted:

    # figure out where the device is
    lsblk

    # mount it (create the mountpoint if necessary)
    sudo mount /dev/sdb1 /media/usb

one downside is that if you remove a highlight or annotation in the kindle,
the `My Clippings.txt` file is not updated to reflect this - you have to manually delete it.
"""

import os
import re
import yaml
MOUNT_POINT = '/media/usb'
ENTRY_DIVIDER = '=========='
HIGHLIGHTS_FILE = os.path.expanduser('~/notes/highlights.md')


def split_title_author(title_author):
    title, author = title_author.rsplit(' (', 1)
    author = author[:-1].strip()
    return title, author or None


def split_metadata(metadata):
    metadata = metadata[2:]
    type = re.search(r'^\w+', metadata).group().lower()
    if 'Page' in metadata:
        page, loc, date = metadata.split(' | ')
        page = int(re.search(r'\d+', page).group())
    else:
        loc, date = metadata.split(' | ')
        page = None
    if type == 'highlight':
        loc = re.search(r'\d+-\d+', loc).group()
    else:
        loc = re.search(r'\d+', loc).group()
    date = date.replace('Added on ', '')
    return type, page, loc, date


if __name__ == '__main__':
    if os.path.exists(HIGHLIGHTS_FILE):
        highlights = yaml.load(open(HIGHLIGHTS_FILE, 'r'))
    else:
        highlights = []

    path = '{}/documents/My Clippings.txt'.format(MOUNT_POINT)
    try:
        with open(path, 'r', encoding='utf-8-sig') as f:
            contents = f.readlines()
    except FileNotFoundError:
        print('couldn\'t find the clippings file at {} - is the kindle mounted?'.format(path))
        exit(1)

    current = []
    existing = [hash(frozenset(hl)) for hl in highlights]
    for line in contents:
        line = line.strip()
        if line == ENTRY_DIVIDER:
            title, author = split_title_author(current[0])
            type, page, loc, date = split_metadata(current[1])
            highlight = {
                'title': title,
                'author': author,
                'page': page,
                'type': type,
                'location': loc,
                'added': date,
                'text': current[2]
            }
            if hash(frozenset(highlight)) not in existing:
                highlights.append(highlight)
            current = []
        elif line:
            current.append(line)

    yaml.dump(
        highlights,
        open(HIGHLIGHTS_FILE, 'w'),
        default_flow_style=False,
        allow_unicode=True)
    print('saved to {}'.format(HIGHLIGHTS_FILE))
