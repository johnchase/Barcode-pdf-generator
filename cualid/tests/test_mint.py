import unittest
import itertools

from cualid import create_ids
from cualid.mint import at_least_distance


class TestCreateIDS(unittest.TestCase):
    def test_create_ids(self):
        self.assertEqual(len(list(create_ids(10, 5))), 10)
        self.assertEqual(len(list(create_ids(0, 3))), 0)
        self.assertEqual(len(list(create_ids(1, 6))), 1)

    def test_create_ids_fail(self):
        result = list(create_ids(1000, 3))
        self.assertTrue(len(result) > 0)
        self.assertTrue(len(result) < 1000)


class TestAtLeastDistance(unittest.TestCase):

    def test_empty(self):
        self.assertTrue(at_least_distance('12345', []))

    def test_single(self):
        self.assertTrue(at_least_distance('12345', ['54321']))

    def test_hypercube(self):
        full = ['0000', '0111']
        all_possible = [''.join(e) for e in itertools.product('01', repeat=4)]

        for s in all_possible:
            self.assertFalse(at_least_distance(s, full))

    def test_long(self):
        collection = ['abcdefghijk', 'a-c^efghijk', 'abcdef@h$jk']

        self.assertFalse(at_least_distance('bcdefghijk', collection))
        self.assertTrue(at_least_distance('a_defghi_k', collection))
        self.assertTrue(at_least_distance('abcd___hijk', collection))

        self.assertFalse(at_least_distance('abc_efghijk', collection))
        self.assertFalse(at_least_distance('abcdefghijk', collection))

if __name__ == "__main__":
    unittest.main()
