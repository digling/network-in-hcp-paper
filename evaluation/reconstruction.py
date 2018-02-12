"""Similarities of Reconstruction Systems based on Vowel Quality

This script computes the similarity among seven different reconstruction
systems based on the comparison of the quality of the vowels.
"""
from lingpy import *
from collections import defaultdict
from lingpy.evaluate.acd import bcubes
import json

# create the matrix
matrix = [[0 for i in range(8)] for j in range(8)]
corrs = defaultdict(list)

# load the data
data = csv2list('reconstructions.tsv')
header = [h.lower() for h in data[0]]
D = {0: ['doculect', 'concept', 'ipa']+header[1:]}

DT = json.load(open('reconstructions.json'))
data = [['character', 'karlgren', 'starostin', 'pwy', 'zzsf', 'wangli', 'lfk',
        'ocbs', 'schuessler']]
for char in DT:
    data += [[char] + [DT[char].get(h, ('?', ''))[0] for h in data[0][1:]]]
header = data[0]
         

for i, headA in enumerate(header[1:]):
    for j, headB in enumerate(header[1:]):
        if i < j:
            idx = 1
            D = {0: ['doculect', 'concept', 'ipa', headA, headB]}
            for line in data[1:]:
                row = dict(zip(header, line))
                vow1 = row[headA].split(' / ')[0]
                vow2 = row[headB].split(' / ')[0]
                if not '?' in (vow1, vow2):
                    D[idx] = ['doculect', 'concept', line[0], vow1, vow2]
                idx += 1
            wl = Wordlist(D)
            wl.renumber(headA)
            wl.renumber(headB)
            print(wl.height, wl.width, headA, headB)
            print(bcubes(wl, headA+'id', headB+'id', pprint=False,
                    per_concept=True))
            matrix[i][j] = 1 - bcubes(wl, headA+'id', headB+'id', pprint=False,
                    per_concept=True)[-1] 
            matrix[j][i] = matrix[i][j]

            print('{0:20}'.format(headA), '\t', '{0:20}'.format(headB), '\t', '{0:.4f}'.format(matrix[i][j]))

text = ' 8\n'
for i, line in enumerate(matrix):
    text += '{0:10}'.format(header[1:][i])+'  '+' '.join(['{0:.2f}'.format(x) for
        x in line])+'\n'

print(Tree(upgma(matrix, header[1:])).asciiArt())
with open('matrix.dst', 'w') as f:
    f.write(text)




