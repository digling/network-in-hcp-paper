from lingpy import *
import networkx as nx
from collections import defaultdict
import html
from itertools import combinations
from sinopy import parse_baxter

def sandeng(pron):
    bx = parse_baxter(pron)
    if 'j' in bx[1] or 'i' in bx[2]:
        return 'j'
    return bx[1]

comps_ = csv2list('xingsheng.tsv', strip_lines=False)

comp = {}
for row in comps_:
    comp[row[1]] = {
            'char': row[1],
            'utf8': row[0],
            'structure': row[2], 
            'sheng': row[3] if len(row) > 3 else ''}

karlgren_ = csv2list('karlgren1954.tsv', strip_lines=False)

# extract the series and subsume characters under one
gsr = defaultdict(lambda : defaultdict(dict))
for line in karlgren_[1:]:
    idx = line[5][:4]
    char = line[1]
    if line[3] == 'Middle_Chinese':
        if gsr[idx][char]:
            gsr[idx][char]['mch'] += [line[6]]
            gsr[idx][char]['pinyin'] += [line[2]]
            
        else:
            gsr[idx][char] = {
                    'mch': [line[6]],
                    'pinyin': [line[7]],
                    'gsr': line[5]
                    }

# make a network of all series
G = nx.DiGraph()
for series in gsr:
    for char in gsr[series]:
        if '聲' in comp.get(char, {'sheng': ''})['sheng'] and len(comp[char]['sheng']) == 2:
            sheng = comp[char]['sheng'][0]
            if sheng in G:
                G.node[sheng]['frequency'] += 1
            else:
                G.add_node(sheng, frequency=1,
                        mch=','.join(gsr[series][char]['mch']),
                        series=series)
            if char in G:
                G.node[char]['frequency'] += 1
            else:
                G.add_node(char, frequency=1,
                        mch=','.join(gsr[series][char]['mch']),
                        series=series)
            if char in G[sheng]:
                G[sheng]['frequency'] += 1
            else:
                G.add_edge(sheng, char, frequency=1)

with open('graph-all.gml', 'w') as f:
    for x in nx.generate_gml(G):
        f.write(html.unescape(x)+'\n')

# test for ab distinction across series
findings, count = [], 0
for group in gsr:
    subg = G.subgraph(gsr[group])
    groups = {}
    groupv = {}
    for node in subg:
        if G[node]:
            kids = [] #[x for x in G.node[node]['mch'].split(',') if x] 
            chars = []
            for nodeX in G[node]:
                kids += [x for x in G.node[nodeX]['mch'].split(',') if x]
                chars += [nodeX]
                    
            jods = [sandeng(k) for k in kids]
            if len(chars) > 1:
                groupv[node] = [jods, chars]
                if jods.count('j') / len(jods) >= 0.7:
                    groups[node] = 'j'
                elif jods.count('j') / len(jods) <= 0.3:
                    groups[node] = '-'
                else:
                    groups[node] = '?'
                    
    if len(groups) > 1:
        if 'j' in groups.values() and '-' in groups.values():
            count += 1
            for g, (j, c) in groupv.items():
                findings += [[str(count), group, g, groups[g], str(len(j)),
                    ''.join(c)]]
with open('ab-groups.tsv', 'w') as f:
    f.write('NUMBER\tGSR\tSUBGROUPS\tAB\tSIZE\tCHARACTERS\n')
    for line in findings:
        f.write('\t'.join(line)+'\n')


