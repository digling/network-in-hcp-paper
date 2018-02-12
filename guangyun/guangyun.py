from lingpy import *
import networkx as nx
from collections import defaultdict
import sinopy 
import html

def sandeng(pron):
    bx = sinopy.parse_baxter(pron)
    if 'j' in bx[1] or 'i' in bx[2]:
        return 'j'
    return bx[1].strip('w')

wl = Wordlist('guangyun.tsv', row='character')
G = nx.DiGraph()
for idx, char, fanqie, reading in wl.iter_rows('character', 'fanqie', 'reading'):
    if sinopy.is_chinese(fanqie[0]):
        G.add_node(fanqie[0], reading='')
all_nodes = list(G.nodes())
visited = set()
for idx, char, fanqie, reading in wl.iter_rows('character', 'fanqie', 'reading'):
    if char in all_nodes and sinopy.is_chinese(fanqie[0]):
        if char in visited and (char, fanqie[0]) not in visited:
            idx = 2
            while True:
                charn = char + str(idx)
                if charn not in visited:
                    char = charn
                    visited.add(char)
                    break
                idx += 1
            G.add_node(char, reading=reading)
        G.node[char]['reading'] = reading
        if char in G[fanqie[0]]:
            G[fanqie[0]][char]['weight'] += 1
        elif char != fanqie[0]:
            G.add_edge(fanqie[0], char, weight=1)
            visited.add((char))
        visited.add((char, fanqie[0]))
    
with open('guangyun.gml', 'w') as f:
    for x in nx.generate_gml(G):
        f.write(html.unescape(x)+'\n') 
