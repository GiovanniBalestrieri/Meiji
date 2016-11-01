# test for https://github.com/RDFLib/rdflib/issues/457

import io
from xml.etree import ElementTree

import rdflib
from rdflib.plugins.stores.sparqlstore import _node_from_result
from rdflib.py3compat import b

s = b("""<ns0:literal xmlns:ns0="http://www.w3.org/2005/sparql-results#" />""")
node = ElementTree.parse(io.BytesIO(s)).getroot()
term = _node_from_result(node)
assert term == rdflib.Literal(''), repr(term)
