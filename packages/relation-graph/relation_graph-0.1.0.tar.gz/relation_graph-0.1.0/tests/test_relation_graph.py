import unittest
from relation_graph import run_relation_graph

class RelationGraphTest(unittest.TestCase):

    def test_rg(self):
        run_relation_graph("tests/input/test.csv", "tests/output/results.csv")

if __name__ == '__main__':
    unittest.main()

