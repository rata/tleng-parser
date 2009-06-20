from graph import *
from sd import *

def imprimir(g):

	print "digraph finite_state_machine {"
	#print 'size="8,5"'

	# marcamos con doble circulo al distinguido
	print "node [shape = doublecircle];", g.root.id
	print "node [shape = circle];"

	# Que respete el orden en que ponemos los links
	print "ordering=out;"

	# Que haga el grafo "parado" (parado al reves en verdad...)
	print "rankdir=BT"


	def nombres(node):
		print node.id, '[ label = "' + char2str(node.char) + '"]'

	#FIN

	def links(node):

		for h in node.links:
			print node.id,  "->",  h.id
	
	# FIN


	# Primero imprimimos todos los nodos y sus nombres
	iterar_grafo(g, nombres)

	# Despues agregamos los links entre los nodos
	iterar_grafo(g, links)

	print "}"


def char2str(c):

	if c == '.':
		return '\.'
	elif c == '+':
		return '\+'
	elif c == '?':
		return '\?'
	elif c == '*':
		return '\*'
	elif c == '|':
		return '\|'
	elif c == '\\':
		return '\\\\'
	else:
		return c


