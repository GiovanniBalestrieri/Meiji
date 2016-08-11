#!/usr/bin/env python

from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF, RDF

g = Graph()
#g.parse("http://dbpedia.org/resource/Elvis_Presley")
g.parse("semantic_map2.owl")

#g.parse("test.owl")
#print len(g)

chair = URIRef("http://www.semanticweb.org/ontologies/2016/1/semantic_mapping_domain_model#Chair")

table = URIRef("http://www.semanticweb.org/ontologies/2016/1/semantic_mapping_domain_model#Table")



numOfChairs = 0
numOfTables = 0

for subj, pred, obj in g:
	#print("\n New object\n")
	#print((subj,pred,obj))
 	if (subj, pred, obj) not in g:
		raise Exception("Iterator / Container Protocols are Broken!!")


for chairs in g.subjects(RDF.type,chair):
	print("Found a Chair",chairs)
	numOfChairs += 1

for tables in g.subjects(RDF.type,table):
	print("Found a table",tables)
	numOfTables += 1

print("Total Number of Chairs:",numOfChairs) 
print("Total Number of Tables:",numOfTables) 


#print("--- printing mboxes ---")
for person in g.subjects(RDF.type, FOAF.Person):
    for mbox in g.objects(person, FOAF.mbox):
        #print(mbox)
	pass


#s = g.serialize(format='n3')
#print s
