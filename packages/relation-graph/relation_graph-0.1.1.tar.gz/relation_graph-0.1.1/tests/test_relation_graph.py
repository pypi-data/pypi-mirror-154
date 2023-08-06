import unittest
from relation_graph import run_relation_graph

INPUT = "tests/input/test.csv"
OUTPUT = "tests/output/results.csv"

FINGERNAIL = 'fingernail'
BODY = 'body'
HAND = 'hand'
FOOT = 'hand'
ENTITY = 'entity'
SUBCLASS_OF = 'rdfs:subClassOf'
PART_OF = 'PART_OF'
OVERLAPS = 'OVERLAPS'

class RelationGraphTest(unittest.TestCase):

    def test_run_relation_graph(self):
        run_relation_graph(INPUT, OUTPUT)
        triples = []
        with open(OUTPUT, 'r') as file:
            for line in file.readlines():
                [s, p, o] = line.strip().split(',')
                triples.append((s, p, o))
        self.assertIn((FINGERNAIL, PART_OF, BODY), triples)
        self.assertIn((FINGERNAIL, PART_OF, HAND), triples)
        self.assertIn((HAND, PART_OF, BODY), triples)
        self.assertIn((HAND, SUBCLASS_OF, ENTITY), triples)
        self.assertIn((FINGERNAIL, SUBCLASS_OF, ENTITY), triples)



if __name__ == '__main__':
    unittest.main()

