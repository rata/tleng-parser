#!/usr/bin/env python
#coding: utf8

from pyparsing import *
from graph import *
from imprimir_grafo import imprimir
from codeador import *

import string

graph = None
nodes = set()


def prodInic(strg, loc, toks):
	global graph
	root = toks[0]
	graph = Graph(root)
	graph.add_link(root, toks[1])
	return root


def produccion(strg, loc, toks):
	global graph
	padre = toks[0]
	padre.add_link(toks[1])
	return padre
	

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

	# El primero de la lista es el nodo "posta", el resto pueden ser muchos
	# operadores unarios pegados
	for i in range(0,len(toks)-1):
		h = toks[i]
		n = toks[i+1]
		n.add_link(h)
	return n

def makeLamb(strg, loc, toks):
	global nodes
	n = Node(len(nodes), '\\')
	nodes.add(n)
	return n


signo = Word( " + , * , ? ", exact=1).setParseAction(toNode)
lamb = Literal('\\').setParseAction(makeLamb)
terminal = Word(string.ascii_lowercase, exact=1).setParseAction(toNode)
noterminal = Word(string.ascii_uppercase, exact=1 ).setParseAction(toNodeNoterm)

simbDisting = Word(string.ascii_uppercase, exact=1 ).setParseAction(toNodeNoterm)

produccionDer =  Forward()

valorMin = noterminal | Suppress('(') + produccionDer + Suppress(')') | terminal | lamb

# Los valores son los valores minimos con algún simbolo o lambda
valor = ((valorMin + OneOrMore(signo)).setParseAction(opUnario) | valorMin)

# El '.' no está en la gramática que pasan
concat = OneOrMore(valor).setParseAction(esConcat)

produccionDer << (ZeroOrMore(Suppress('|').setParseAction(makeLamb)) + (concat | Empty().setParseAction(makeLamb)) + ZeroOrMore( Suppress('|') + (concat | Empty().setParseAction(makeLamb) ) ) ).setParseAction(esDisjunc)

produccion =        (noterminal + Suppress(':') + produccionDer + Suppress(';') ).setParseAction(produccion)
produccionInicial = (simbDisting + Suppress(':') + produccionDer + Suppress(';') ).setParseAction(prodInic)

# Separo la inicial porque me va a ser más fácil
gramaticaInicio = produccionInicial + ZeroOrMore(produccion)


gramaticaInicio.parseFile( "gramatica.txt", parseAll = True )

for n in nodes:
	graph.add_node(n)

#imprimir(graph)
codearGrafo(graph)
