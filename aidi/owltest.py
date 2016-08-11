#!/usr/bin/env python

from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF

g = Graph()
#g.parse("http://dbpedia.org/resource/Elvis_Presley")
#g.parse("semantic_map1.owl")

g.parse("test.owl")
print len(g)


for subj, pred, obj in g:
	print("\n New object\n")
	print((subj,pred,obj))
 	if (subj, pred, obj) not in g:
		raise Exception("It better be!")

print("--- printing mboxes ---")
for person in g.subjects(RDF.type, FOAF.Person):
    for mbox in g.objects(person, FOAF.mbox):
        print(mbox)


s = g.serialize(format='n3')
print s
