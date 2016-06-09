"""
tests constructing of reverse fln hash
"""

# to make module importable: pip install -e . 
    # in the main directory
    # -e flag ensures changes are reflected in import

from tools import build_reverse_fln
from tools import get_first_link


def test_sample_rev_fln():
    """
    compares sample reversed network against result of rev_fln function
    """
    sample_fln = {'a': 'b', 'b': 'c', 'd': 'a', 'e': 'a'} 
    correct_rev_fln = {'a': ['d', 'e'], 'b': ['a'], 'c': ['b'], 'd': [], 'e': []}
    rev_fln = build_reverse_fln.reverse_fln(sample_fln)
    #ensure comparison is set-based since membership doesn't depend on order
    assert set(rev_fln['a']) == set(correct_rev_fln['a'])
    assert set(rev_fln['b']) == set(correct_rev_fln['b'])
    assert set(rev_fln['e']) == set(correct_rev_fln['e'])
    
def test_parser():
    """
    test whether rail transport is first link of train
    on a sample of the train page's xml
    """
    train_xml = "{{About|the rail vehicle|the American rock band|Train (band)|the act of teaching or developing skills or knowledge|Training|other uses}} {{pp-vandalism|expiry=8 October 2016|small=yes}} {{Use dmy dates|date=September 2015}} [[File:BNSF 5350 20040808 Prairie du Chien WI.jpg|thumb|240px|A [[BNSF Railway|BNSF]] [[intermodal freight transport|intermodal]] freight train passes through [[Wisconsin]], United States]] {{train topics}} A '''train''' is a form of [[rail transport]] consisting of a series of [[vehicle]]s that usually runs along a [[rail track]] to transport [[cargo]] or [[passenger]]s. Motive power is provided by a separate [[locomotive]] or individual motors in self-propelled [[multiple unit]]s. Although historically [[steam locomotive|steam]] propulsion dominated, the most common modern forms are [[diesel locomotive|diesel]] and [[Electric locomotive|electric]] locomotives"
    assert get_first_link.run_parser(train_xml) == "rail transport"

