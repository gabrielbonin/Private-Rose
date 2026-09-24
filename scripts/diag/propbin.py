"""Minimal reader/writer for League PROP .bin files (ritobin layout)."""
import struct

# primitive type ids -> struct format (None = special)
PRIM = {
    0: None, 1: '<?', 2: '<b', 3: '<B', 4: '<h', 5: '<H', 6: '<i', 7: '<I',
    8: '<q', 9: '<Q', 10: '<f', 11: '<2f', 12: '<3f', 13: '<4f', 14: '<16f',
    15: '<4B', 16: None, 17: '<I', 18: '<Q',
}
LIST, LIST2, POINTER, EMBED, LINK, OPTION, MAP, FLAG = range(0x80, 0x88)


class Reader:
    def __init__(self, b):
        self.b, self.o = b, 0

    def u(self, fmt):
        v = struct.unpack_from(fmt, self.b, self.o)
        self.o += struct.calcsize(fmt)
        return v if len(v) > 1 else v[0]

    def string(self):
        n = self.u('<H')
        s = self.b[self.o:self.o + n].decode('utf-8', 'replace')
        self.o += n
        return s

    def value(self, t):
        if t in PRIM and t != 16:
            return None if PRIM[t] is None else self.u(PRIM[t])
        if t == 16:
            return self.string()
        if t in (LIST, LIST2):
            vt = self.u('<B'); self.u('<I'); n = self.u('<I')
            return (vt, [self.value(vt) for _ in range(n)])
        if t in (POINTER, EMBED):
            h = self.u('<I')
            if h == 0:
                return (0, [])
            self.u('<I'); n = self.u('<H')
            return (h, [self.field() for _ in range(n)])
        if t == LINK:
            return self.u('<I')
        if t == OPTION:
            vt = self.u('<B'); n = self.u('<B')
            return (vt, [self.value(vt) for _ in range(n)])
        if t == MAP:
            kt = self.u('<B'); vt = self.u('<B'); self.u('<I'); n = self.u('<I')
            return (kt, vt, [(self.value(kt), self.value(vt)) for _ in range(n)])
        if t == FLAG:
            return self.u('<B')
        raise ValueError(f'unknown type {t:#x} at {self.o}')

    def field(self):
        name = self.u('<I'); t = self.u('<B')
        return (name, t, self.value(t))


def fix_type(t):
    # newer bins renumber complex types; ritobin maps >= 0x12+ legacy ids
    return t


def read(b):
    r = Reader(b)
    magic = r.b[:4]; r.o = 4
    patch = None
    if magic == b'PTCH':
        patch = r.u('<Q'); magic = r.b[r.o:r.o + 4]; r.o += 4
    assert magic == b'PROP', magic
    ver = r.u('<I')
    links = []
    if ver >= 2:
        links = [r.string() for _ in range(r.u('<I'))]
    n = r.u('<I')
    types = [r.u('<I') for _ in range(n)]
    entries = []
    for et in types:
        start = r.o
        size = r.u('<I'); key = r.u('<I'); nf = r.u('<H')
        fields = [r.field() for _ in range(nf)]
        assert r.o == start + 4 + size, (hex(key), r.o, start + 4 + size)
        entries.append((et, key, fields))
    return dict(ver=ver, links=links, entries=entries, rest=r.b[r.o:])


class Writer:
    def __init__(self):
        self.parts = []

    def raw(self, b):
        self.parts.append(b)

    def u(self, fmt, *v):
        self.parts.append(struct.pack(fmt, *v))

    def getvalue(self):
        return b''.join(self.parts)


def enc_string(s):
    b = s.encode('utf-8')
    return struct.pack('<H', len(b)) + b


def enc_value(t, v):
    if t in PRIM and t != 16:
        if PRIM[t] is None:
            return b''
        return struct.pack(PRIM[t], *(v if isinstance(v, tuple) else (v,)))
    if t == 16:
        return enc_string(v)
    if t in (LIST, LIST2):
        vt, items = v
        body = struct.pack('<I', len(items)) + b''.join(enc_value(vt, i) for i in items)
        return struct.pack('<BI', vt, len(body)) + body
    if t in (POINTER, EMBED):
        h, fields = v
        if h == 0:
            return struct.pack('<I', 0)
        body = struct.pack('<H', len(fields)) + b''.join(enc_field(f) for f in fields)
        return struct.pack('<II', h, len(body)) + body
    if t == LINK:
        return struct.pack('<I', v)
    if t == OPTION:
        vt, items = v
        return struct.pack('<BB', vt, len(items)) + b''.join(enc_value(vt, i) for i in items)
    if t == MAP:
        kt, vt, pairs = v
        body = struct.pack('<I', len(pairs)) + b''.join(enc_value(kt, k) + enc_value(vt, x) for k, x in pairs)
        return struct.pack('<BBI', kt, vt, len(body)) + body
    if t == FLAG:
        return struct.pack('<B', v)
    raise ValueError(t)


def enc_field(f):
    name, t, v = f
    return struct.pack('<IB', name, t) + enc_value(t, v)


def write(d):
    out = [b'PROP', struct.pack('<I', d['ver'])]
    if d['ver'] >= 2:
        out.append(struct.pack('<I', len(d['links'])))
        out += [enc_string(l) for l in d['links']]
    out.append(struct.pack('<I', len(d['entries'])))
    out += [struct.pack('<I', et) for et, _, _ in d['entries']]
    for et, key, fields in d['entries']:
        body = struct.pack('<IH', key, len(fields)) + b''.join(enc_field(f) for f in fields)
        out.append(struct.pack('<I', len(body)) + body)
    out.append(d.get('rest', b''))
    return b''.join(out)


def fnv1a(s):
    h = 0x811c9dc5
    for c in s.lower().encode():
        h = ((h ^ c) * 0x01000193) & 0xffffffff
    return h
