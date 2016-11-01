#!/usr/bin/env python

from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF, RDF

g = Graph()
g.parse("semantic_mapChairs.owl")

#print len(g)

chair = URIRef("http://www.semanticweb.org/ontologies/2016/1/semantic_mapping_domain_model#Chair")

table = URIRef("http://www.semanticweb.org/ontologies/2016/1/semantic_mapping_domain_model#Table")

lexicalRef = URIRef("http://www.semanticweb.org/ontologies/2016/1/semantic_mapping_domain_model#lexicalReference")

altRefPred = URIRef("http://www.semanticweb.org/ontologies/2016/1/semantic_mapping_domain_model#hasAlternativeReference")

prefRefPred = URIRef("http://www.semanticweb.org/ontologies/2016/1/semantic_mapping_domain_model#hasPreferredReference")

positionPred = URIRef("http://www.semanticweb.org/ontologies/2016/1/semantic_mapping_domain_model#hasPosition")

coordXPred = URIRef("http://www.semanticweb.org/ontologies/2016/1/semantic_mapping_domain_model#float_coordinates_x")

coordYPred = URIRef("http://www.semanticweb.org/ontologies/2016/1/semantic_mapping_domain_model#float_coordinates_y")

coordZPred = URIRef("http://www.semanticweb.org/ontologies/2016/1/semantic_mapping_domain_model#float_coordinates_z")

sizePred = URIRef("http://www.semanticweb.org/ontologies/2016/1/semantic_mapping_domain_model#hasSize")

sizeXPred = URIRef("http://www.semanticweb.org/ontologies/2016/1/semantic_mapping_domain_model#float_size_x")

sizeYPred = URIRef("http://www.semanticweb.org/ontologies/2016/1/semantic_mapping_domain_model#float_size_y")

sizeZPred = URIRef("http://www.semanticweb.org/ontologies/2016/1/semantic_mapping_domain_model#float_size_z")

numOfChairs = 0
numOfTables = 0

for subj, pred, obj in g:
	#print("\n New object\n")
	print((subj,pred,obj))
 	if (subj, pred, obj) not in g:
		raise Exception("Iterator / Container Protocols are Broken!!")

print("\n\nChairs:\n\n")

# Find Triples in which an instance of the type Chair is defined
for chairs in g.subjects(RDF.type,chair):
	
	print("------------------------------------------\n")
	print("Found a Chair\n"+ chairs +"\n")
	numOfChairs += 1
	print("------------------------------------------")
	
	# Search all predicates of this instance
	print("### Predicates ###\n\n")
	for pred,obj in g.predicate_objects(chairs):
		# Look for Alternative References
		
		if (pred==altRefPred):
			print("# Lexical Reference #\n")
			for o in g.objects(obj,lexicalRef):
				print("Alternative: "+o+"\n")
		
		# Look for Preferred Lexical Ref
		if (pred == prefRefPred):
			for o in g.objects(obj,lexicalRef):
				print("*Favourite*: "+o+"\n")

		# Look for size
		if (pred == sizePred):
			print("# Dimensions #\n")
			for o in g.objects(obj,sizeXPred):
				print("Size X: " +o+"\n")
			
			for o in g.objects(obj,sizeYPred):
				print("Size Y: "+o+"\n")
				

			for o in g.objects(obj,sizeZPred):
				print("Size Z: "+o+"\n")
			

		# Look for coordinates
		if (pred == positionPred):
			print("# Coordinates #\n")
			for o in g.objects(obj,coordXPred):
				print("X: "+o+"\n")
			
			for o in g.objects(obj,coordYPred):
				print("Y: "+o+"\n")
				

			for o in g.objects(obj,coordZPred):
				print("Z:  "+o+"\n")
							
		# Generic object and predicate
		#print("Predicate:\n " + pred)
		#print("Object:\n " + obj + "\n\n")
		#for o in g.objects(obj,None):
		#	print("\nFuther Infos:\n")
		#	print("Oggetto: \n" + o+ "\n\n")
	print("\n\n")


for tables in g.subjects(RDF.type,table):
	print("------------------------------------------\n")
	print("\nFound a table!!\n\n" + tables+"\n")
	numOfTables += 1
	print("------------------------------------------\n")

print("Total Number of Chairs:",numOfChairs) 
print("Total Number of Tables:",numOfTables) 


#print("--- printing mboxes ---")
for person in g.subjects(RDF.type, FOAF.Person):
    for mbox in g.objects(person, FOAF.mbox):
        #print(mbox)
	pass


#s = g.serialize(format='n3')
#print s
