import unittest
from eval_ledger import summarize
def case(i='one',expected='deny',observed='deny',category='boundary'):
    return dict(id=i,category=category,expected=expected,observed=observed)
class LedgerTests(unittest.TestCase):
    def test_all_cells(self):
        r=summarize([case('a'),case('b','deny','allow'),case('c','allow','deny'),case('d','allow','allow')])
        self.assertEqual(set(r['counts'].values()),{1});self.assertEqual(r['attack_detection_rate'],.5);self.assertEqual(r['legitimate_block_rate'],.5)
    def test_no_attack_denominator(self):self.assertIsNone(summarize([case(expected='allow',observed='allow')])['attack_detection_rate'])
    def test_no_legitimate_denominator(self):self.assertIsNone(summarize([case()])['legitimate_block_rate'])
    def test_duplicate_id(self):
        with self.assertRaises(ValueError):summarize([case(),case()])
    def test_empty_rejected(self):
        with self.assertRaises(ValueError):summarize([])
    def test_invalid_outcome(self):
        with self.assertRaises(ValueError):summarize([case(observed='maybe')])
    def test_categories(self):self.assertEqual(summarize([case()])['categories']['boundary']['cases'],1)
    def test_unknown_field(self):
        c=case();c['text']='not collected'
        with self.assertRaises(ValueError):summarize([c])
    def test_blank_id(self):
        with self.assertRaises(ValueError):summarize([case(i=' ')])
if __name__=='__main__':unittest.main()
