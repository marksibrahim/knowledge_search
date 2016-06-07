"""
tests constructing of reverse fln hash
"""

import build_reverse_fln


sample_fln = {'a': 'b', 'b': 'c', 'd': 'a', 'e': 'a'} 
correct_rev_fln = {'a': ['d', 'e'], 'b': ['a'], 'c': ['b'], 'd': [], 'e': []}


def test_sample_rev_fln():
    rev_fln = build_reverse_fln.reverse_fln(sample_fln)
    #ensure comparison is set-based since membership doesn't depend on order
    assert set(rev_fln['a']) == set(correct_rev_fln['a'])
    assert set(rev_fln['b']) == set(correct_rev_fln['b'])
    assert set(rev_fln['e']) == set(correct_rev_fln['e'])
    

