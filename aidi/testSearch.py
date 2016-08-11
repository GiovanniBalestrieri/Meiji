from rdflib import URIRef, Graph, Literal
from rdflib.namespace import RDF, FOAF

g = Graph()

linda = URIRef("http://userk.co.uk/person/linda")
bob = URIRef("http://userk.co.uk/people/bob")
nameBob = "Bob"




g.add( (bob, RDF.type, FOAF.Person) )
g.add( (bob, FOAF.name, Literal('Bob')))
g.add( (bob, FOAF.knows, linda) )
g.add( (linda, RDF.type, FOAF.Person) )
g.add( (linda, FOAF.name, Literal('Linda')))



print g.serialize(format='turtle')

if ( bob, RDF.type, FOAF.Person ) in g:
   print "This graph knows that Bob is a person!"
