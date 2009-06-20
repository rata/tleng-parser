from graph import *
from sd import *

def imprimir(g):

	print "digraph finite_state_machine {"
	print "rankdir=LR;"
	print 'size="8,5"'

	# marcamos con doble circulo al distinguido
	print "node [shape = doublecircle];", char2str(g.root.char) + "_" + str(g.root.id)
	print "node [shape = circle];"


	def f(node):

		for h in node.links:

			# No usamos solo el char, porque esto "identifica" al
			# nodo. Y no usamos solo el id porque eso no nos dice
			# nada a la vista. Entonces, combinamos los dos =)
			# Y usamos char2str porque los '.' y esos no son validos
			# en dot para nombre de nodos
			print '"' + char2str(node.char) + "_" + str(node.id) + '"', \
					'-> "' + char2str(h.char) + "_" + str(h.id) + '"'
	
	# FIN
	iterar_grafo(g, f)

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


