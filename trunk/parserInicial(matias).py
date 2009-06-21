#!/usr/bin/env python
#coding: utf8

from pyparsing import *
from graph import *
from imprimir_grafo import imprimir

import string

graph = None
nodes = set()
#root = None


def prodInic(strg, loc, toks):
	global graph
	root = toks[0]
	graph = Graph(root)
	graph.add_link(root, toks[1])
#	print 'Entra en produccion inicial', toks
	return root


def produccion(strg, loc, toks):
	global graph
#	global root
	padre = toks[0]
	padre.add_link(toks[1])
#	print 'Entra en produccion, a ', toks[0], ' le pone de hijo ', toks[1]
	return padre
#	root = padre
	

def toNode(strg, loc, toks):
	global nodes
	n = Node(len(nodes), toks[0])
	nodes.add(n)
#	print 'Entra en toNodes para ', toks
	return n

def toNodeNoterm(strg, loc, toks):
	global nodes
	nomb = toks[0]
	n = dame(nomb,nodes)
	if not n:
		n = Node(len(nodes), toks[0])
		nodes.add(n)
#	print 'Entra en toNodeNoterm para ', toks
	return n

def dame(nomb, nodes):
	for n in nodes:
		if n.char == nomb:
			return n
#		else:
#			print n.char, 'es distinto de ', nomb
	return None

def esDisjunc(strg, loc, toks):
	global nodes
#	print 'Entra en disjunc para ', toks
	if not len(toks) == 1:
		n = Node(len(nodes), '|')
		nodes.add(n)
		for h in toks:
			n.add_link(h)
#		print 'Los hijos de ', n , 'son', n.links 
		return n
	else:
		return toks[0]

def esConcat(strg, loc, toks):
	global nodes
#	print 'Entra en concat para ', toks
	if len(toks) > 1:
		n = Node(len(nodes), '.')
		nodes.add(n)
		for h in toks:
			n.add_link(h)	
		return n
	else:
		return toks[0]

def opUnario(strg, loc, toks):
	#print 'Entra en opUnario para ', toks

	# El primero de la lista es el nodo "posta", el resto pueden ser muchos
	# operadores unarios pegados
	for i in range(0,len(toks)-1):
		h = toks[i]
		n = toks[i+1]
		n.add_link(h)
	return n

def nada(strg, loc, toks):
	return toks[0]

def lamb(strg, loc, toks):
	global nodes
	if not toks[0]:
		n = Node(len(nodes), '\\')
		nodes.add(n)
		return n
	else:
		return toks[0]

def makeLamb(strg, loc, toks):
	global nodes
	n = Node(len(nodes), '\\')
	nodes.add(n)
	return n

def impri(strg, loc, toks):
	print 'Reconoce otra produccion además de la inicial'
	print toks


signo = Word( " + , * , ? ", exact=1).setParseAction(toNode)
lamb = Literal('\\').setParseAction(makeLamb)
#terminal = Word(string.ascii_lowercase, exact=1).setParseAction(toNode)
terminal = (Literal('a') | Literal('b') | Literal('c') | Literal('d') | Literal('e') | Literal('f') | Literal('g') | Literal('h') | Literal('i') | Literal('j') | Literal('k') | Literal('l') | Literal('m') | Literal('n') | Literal('o') | Literal('p') | Literal('q') | Literal('r') | Literal('s') | Literal('t') | Literal('u') | Literal('v') | Literal('w') | Literal('x') | Literal('y') | Literal('z') | Literal('ñ') ).setParseAction(toNode)
#noterminal = Word(string.ascii_uppercase, exact=1 ).setParseAction(toNodeNoterm)
noterminal = (Literal('A') | Literal('B') | Literal('C') | Literal('D') | Literal('E') | Literal('F') | Literal('G') | Literal('H') | Literal('I') | Literal('J') | Literal('K') | Literal('L') | Literal('M') | Literal('N') | Literal('O') | Literal('P') | Literal('Q') | Literal('R') | Literal('S') | Literal('T') | Literal('U') | Literal('V') | Literal('W') | Literal('X') | Literal('Y') | Literal('Z') | Literal('Ñ') ).setParseAction(toNodeNoterm)

simbDisting = Word(string.ascii_uppercase, exact=1 ).setParseAction(toNodeNoterm)

produccionDer =  Forward()

#valorMin = (noterminal | terminal | (Suppress('(') + produccionDer + Suppress(')'))).setParseAction(nada)
valorMin = noterminal | Suppress('(') + produccionDer + Suppress(')') | terminal | lamb

valor = ((valorMin + OneOrMore(signo)).setParseAction(opUnario) | valorMin)		# Los valores son los valores minimos con algún simbolo o lambda

concat = OneOrMore(valor).setParseAction(esConcat)	 			# El '.' no está en la gramática que pasan

#OpConcat = concat | Empty().setParseAction(makeLamb)

produccionDer << (ZeroOrMore(Suppress('|').setParseAction(makeLamb)) + (concat | Empty().setParseAction(makeLamb)) + ZeroOrMore( Suppress('|') + (concat | Empty().setParseAction(makeLamb) ) ) ).setParseAction(esDisjunc)

produccion =         (noterminal + Suppress(':') + produccionDer + Suppress(';') ).setParseAction(produccion)
produccionInicial = (simbDisting + Suppress(':') + produccionDer + Suppress(';') ).setParseAction(prodInic)

gramaticaInicio = produccionInicial + ZeroOrMore(produccion) #.setParseAction(impri)

# Separo la inicial porque me pinta que se me va a hacer más fácil
#gramaticaInicio = OneOrMore(produccion)


gramaticaInicio.parseFile( "gramatica.txt" )

#graph = Graph(root)

for n in nodes:
	graph.add_node(n)
#print graph.nodes
#print graph.nodes

imprimir(graph)

"""
setParseAction( *fn ) - specify one or more functions to call after successful matching of the element; each function is defined as fn( s, loc, toks ), where:

    * s is the original parse string
    * loc is the location in the string where matching started
    * toks is the list of the matched tokens, packaged as a ParseResults object

Multiple functions can be attached to a ParserElement by specifying multiple arguments to setParseAction, or by calling setParseAction multiple times.

Each parse action function can return a modified toks list, to perform conversion, or string modifications. For brevity, fn may also be a lambda - here is an example of using a parse action to convert matched integer tokens from strings to integers:

intNumber = Word(nums).setParseAction( lambda s,l,t: [ int(t[0]) ] )

If fn does not modify the toks list, it does not need to return anything at all.
------------------------------------------------------------------------------------------------
parseFile( sourceFile ) ?

expr.parseFile( sourceFile )
"""



