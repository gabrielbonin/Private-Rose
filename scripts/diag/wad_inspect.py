"""Compare WAD v3 headers/TOCs, e.g. a game WAD against its overlay copy.

Usage:
    python scripts/diag/wad_inspect.py <game.wad.client> [<overlay.wad.client> ...]

Prints version, signature prefix, header checksum and entry count for each
file, and for every extra file how its TOC differs from the first one.
Since 16.19 the game rejects overlay WADs whose signature/checksum differ
from the original ("WadFile mount failed ... Corrupt").
"""
import struct
import sys
from collections import Counter

HEADER_SIZE = 268  # magic+version (4) + signature (256) + checksum (8)


def load(path):
    with open(path, 'rb') as f:
        data = f.read()
    if data[:2] != b'RW':
        raise SystemExit(f'{path}: not a WAD (magic {data[:2]!r})')
    count = struct.unpack_from('<I', data, HEADER_SIZE)[0]
    entries = {}
    for i in range(count):
        h, off, csz, usz, tb, dup, sub, chk = struct.unpack_from('<QIIIBBHQ', data, 272 + i * 32)
        entries[h] = (csz, usz, tb & 0xF, tb >> 4, chk)
    return data, entries


def describe(path, data, entries):
    types = Counter((t, n) for _, _, t, n, _ in entries.values())
    print(f'{path}')
    print(f'  version   {data[2]}.{data[3]}')
    print(f'  signature {data[4:12].hex()}...')
    print(f'  checksum  {data[260:268].hex()}')
    print(f'  entries   {len(entries)}  types(type,subchunks)={dict(types.most_common(6))}')


def main(paths):
    base_data, base = load(paths[0])
    describe(paths[0], base_data, base)
    for p in paths[1:]:
        data, entries = load(p)
        describe(p, data, entries)
        same_header = data[:HEADER_SIZE] == base_data[:HEADER_SIZE]
        changed = [h for h in base if h in entries and entries[h] != base[h]]
        print(f'  header == first file: {same_header}')
        print(f'  only in first: {len(set(base) - set(entries))}  only here: {len(set(entries) - set(base))}  '
              f'changed chunks: {len(changed)}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    main(sys.argv[1:])
