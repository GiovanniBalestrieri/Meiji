import sys, os
from owlready import *

onto_path.append(os.path.dirname(__file__))

onto = get_ontology("http://test.org/semantic_mapChairs.owl")
onto.load()
