#!/usr/bin/env python
#coding: utf8

from pyparsing import *
from graph import *
from imprimir_grafo import imprimir

import string

graph = None
nodes = set()


def prodInic(strg, loc, toks):
	global graph
	root = toks[0]
	graph = Graph(root)
	graph.add_link(root, toks[1])

def produccion(strg, loc, toks):
	global graph
	padre = toks[0]
	padre.add_link(toks[1])
	

def toNode(strg, loc, toks):
	global nodes
	n = Node(len(nodes), toks[0])
	nodes.add(n)
	return n

def toNodeNoterm(strg, loc, toks):
	global nodes
	nomb = toks[0]
	n = dame(nomb,nodes)
	if not n:
		n = Node(len(nodes), toks[0])
		nodes.add(n)
	return n

def dame(nomb, nodes):
	for n in nodes:
		if n.char == nomb:
			return n
	return None

def esDisjunc(strg, loc, toks):
	global nodes
	if not len(toks) == 1:
		n = Node(len(nodes), '|')
		nodes.add(n)
		for h in toks:
			n.add_link(h)	
		return n
	else:
		return toks[0]

def esConcat(strg, loc, toks):
	global nodes
	if len(toks) > 1:
		n = Node(len(nodes), '.')
		nodes.add(n)
		for h in toks:
			n.add_link(h)	
		return n
	else:
		return toks[0]

def opUnario(strg, loc, toks):
		n = toks[1]
		h = toks[0]
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


signo = Word( " + , * , ? ", max=1).setParseAction(toNode)
lamb = Literal('\\').setParseAction(makeLamb)
terminal = Word(string.ascii_lowercase, max=1).setParseAction(toNode)
"""terminal = Literal('a').setParseAction(toNode) | Literal('b').setParseAction(toNode) | Literal('c').setParseAction(toNode) | Literal('d').setParseAction(toNode) | Literal('e').setParseAction(toNode) | Literal('f').setParseAction(toNode) | Literal('g').setParseAction(toNode) | Literal('h').setParseAction(toNode) | Literal('i').setParseAction(toNode) | Literal('j').setParseAction(toNode) | Literal('k').setParseAction(toNode) | Literal('l').setParseAction(toNode) | Literal('m').setParseAction(toNode) | Literal('n').setParseAction(toNode) | Literal('o').setParseAction(toNode) | Literal('p').setParseAction(toNode) | Literal('q').setParseAction(toNode) | Literal('r').setParseAction(toNode) | Literal('s').setParseAction(toNode) | Literal('t').setParseAction(toNode) | Literal('u').setParseAction(toNode) | Literal('v').setParseAction(toNode) | Literal('w').setParseAction(toNode) | Literal('x').setParseAction(toNode) | Literal('y').setParseAction(toNode) | Literal('z').setParseAction(toNode) | Literal('ñ').setParseAction(toNode)"""
noterminal = Word(string.ascii_uppercase, max=1 ).setParseAction(toNodeNoterm)
simbDisting = Word(string.ascii_uppercase, max=1 ).setParseAction(toNodeNoterm)

produccionDer =  Forward()

#valorMin = (noterminal | terminal | (Suppress('(') + produccionDer + Suppress(')'))).setParseAction(nada)
valorMin = Suppress('(') + produccionDer + Suppress(')') | terminal | noterminal | lamb

valor = (valorMin + signo).setParseAction(opUnario) | valorMin		# Los valores son los valores minimos con algún simbolo o lambda

concat = OneOrMore(valor).setParseAction(esConcat)	 			# El '.' no está en la gramática que pasan

OpConcat = concat | Empty().setParseAction(makeLamb)

produccionDer << ( Optional( Suppress('|').setParseAction(makeLamb) ) + concat + ZeroOrMore( Suppress('|') + OpConcat ) ).setParseAction(esDisjunc)

produccion = (noterminal + Suppress(':') + produccionDer + Suppress(';') ).setParseAction(produccion)
produccionInicial = (simbDisting + Suppress(':') + produccionDer + Suppress(';') ).setParseAction(prodInic)
gramaticaInicio = produccionInicial + ZeroOrMore( produccion )		# Separo la inicial porque me pinta que se me va a hacer más fácil



gramaticaInicio.parseFile( "gramatica.txt" )

for n in nodes:
	graph.add_node(n)

print graph.nodes

#imprimir(graph)

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



