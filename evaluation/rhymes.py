from lingpy import *
from lingpy.evaluate.acd import *
from collections import defaultdict, OrderedDict
from lingpy.evaluate.acd import _get_bcubed_score

def get_rhymes(dataset):
    csv = csv2list(dataset+'.tsv',
            strip_lines=False)
    header = [h.lower() for h in csv[0]]
    rest = csv[1:]
    out = []
    for line in rest:
        out += [OrderedDict(zip(header, line))]
    return out

def to_dict(csv):
    out = {}
    for d in csv:
        out[d['line'], d['stanza'], d['line_number']] = d
    return out

wang = get_rhymes('Wang1980')
baxt = get_rhymes('Baxter1992')
wand, baxd = to_dict(wang), to_dict(baxt)


# add rhyme_id to wang's data
idxs, cogid = {}, 0
for key, val in wand.items():
    if val['rhyme']:
        rhyme = key[1] + '.' + val['rhyme']
        if rhyme in idxs:
            wand[key]['rhymeid'] = idxs[rhyme]
        else:
            idxs[rhyme] = cogid
            cogid += 1
            wand[key]['rhymeid'] = idxs[rhyme]
    else:
        wand[key]['rhymeid'] = 0
        cogid += 1

for key, val in baxd.items():
    if val['rhymeid'] == '0':
        val['rhymeid'] = 0
        cogid += 1
    else:
        val['rhymeid'] = int(val['rhymeid'])


def compare_stanza(rhymes1, rhymes2, stanza):
    def get_rhymes(stanza, rhymes):
        vals = sorted([x for x in rhymes.items() if stanza in x[0]], 
                key=lambda x: int(x[1]['id']))
        patterns = [x[1]['rhymeid'] for x in vals]
        cogid, rem = 0, {}
        out = []
        for p in patterns:
            if p == 0:
                out += [0]
            elif p in rem:
                out += [rem[p]]
            else:
                rem[p] = cogid
                cogid += 1
                out += [rem[p]]
        return out
    rhymes1p, rhymes2p = get_rhymes(stanza, rhymes1), get_rhymes(
            stanza, rhymes2)
    if rhymes1p == rhymes2p:
        return 1, 1, 1

    else:
        rhymes1p_, rhymes2p_ = [], []
        for a, b in zip(rhymes1p, rhymes2p):
            if not (a == 0 and b == 0):
                rhymes1p_ += [a]
                rhymes2p_ += [b]

    p = _get_bcubed_score(rhymes1p, rhymes2p)
    r = _get_bcubed_score(rhymes2p, rhymes1p)
    f = 2 * ((p*r) / (p+r))

    return p, r, f


diffs = []
missed = []
stanzas = defaultdict(list)
missed_stanzas = []
for (l, s, n), d in wand.items():
    if (l, s, n) in baxd:
        stanzas[s] += [(l, s, n)]
    else:
        missed += [(l, s, n)]

for l, s, n in baxd:
    if (l, s, n) in wand:
        if wand[l, s, n]['rhyme'].strip():
            rhyme = wand[l, s, n]['stanza'] + '.'+wand[l, s, n]['rhyme']
            reconstruction = wand[l, s, n]['reconstruction']
        else:
            rhyme = ''
            reconstruction = ''
    else:
        rhyme = ''
        reconstruction = ''
    baxd[l, s, n]['wangli_rhyme'] = rhyme
    baxd[l, s, n]['wangli_reconstruction'] = reconstruction
        
missed_stanzas = [m[1] for m in missed]
for stanza in stanzas:
    if stanza not in missed_stanzas:
        a, b, c = compare_stanza(wand, baxd, stanza)
        diffs += [(stanza, a, b, c)]
print('Total different lines', sum([1 for d in diffs if d[3] != 1]), len(diffs))
print('Proportion per stanza', sum([d[3] for d in diffs]) / len(diffs))

