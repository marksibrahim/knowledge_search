"""
builds a reverse hash lookup of the First Link Network
    input:
        {'article1': 'first link', 'article2': 'first link', ....}
    output:
        {'article1': ['direct link1', 'direct link2', ...], ...}
stores output in json file
"""

from collections import defaultdict


def reverse_fln(fln):
    rev_fln = defaultdict(list)
    for k, v in fln.items():
        rev_fln[v].append(k)
    return rev_fln



