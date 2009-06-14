#!/usr/bin/env python
#coding: utf8

import string
from graph import *

import sys

# permitimos mas recursion que la normal; con esto manejamos hasta
# grafos de un poco mas de 15000 nodos
sys.setrecursionlimit(20000)


# Variable glogal que usa iterar grafo y el parametro f de iterar grafo, nos
# dice si debemos hacer otra recorrida por el grafo
changed = True
def iterar_grafo(g, f):
	global changed
	changed = True

	visisted = set()

	def iterar_desde(node):
		if node in visited:
			return
		visited.add(node)

		# Nos llamamos recursivamente con todos los hijos
		for n in node.links:
			iterar_desde(n)

		# Aplicamos la funcion a este nodo
		f(node)

	# FIN
	
	while changed:
		changed = False
		visited = set()
		iterar_desde(g.root)


def utiles(g):

	util = set()

	def f(node):
		global changed
		# Analizamos el nodo actual
		if node.char in string.lowercase or node.char == '*' or \
			node.char == '\\' or node.char == '?':
			# Un terminal siempre es util :)
			# El resto tmb son utiles, producen lambda
			if node not in util:
				util.add(node)
				changed = True
	
		elif node.char in string.uppercase or node.char == '|':
			# Es util si algun hijo es util
	
			some_util = False
	
			for n in node.links:
				some_util = some_util | (n in util)
	
			if some_util and node not in util:
				util.add(node)
				changed = True
	
		elif node.char == '.' or node.char == '+':
			# Es util si todos los hijos son utiles
			all_util = True
	
			for n in node.links:
				all_util = all_util & (n in util)
	
			if all_util and node not in util:
				util.add(node)
				changed = True
	
		else:
			# Todos los nodos deberian tener algun caracter
			# de los anteriores
			raise Exception('Tipo de nodo desconocido', node.char)

	iterar_grafo(g, f)
	return util



def anulables(g):

	anul = set()

	def f(node):
		global changed
	
		if node.char in string.lowercase:
			# Un terminal nunca es anulable
			return
	
		elif node.char == '*' or node.char == '?' or node.char == '\\':
			# Siempre es anulable
			if node not in anul:
				anul.add(node)
				changed = True
	
		elif node.char in string.uppercase or node.char == '|':
			# Es anulable si algun hijo es anulable
	
			some_anul = False
	
			for n in node.links:
				some_anul = some_anul | (n in anul)
	
			if some_anul and node not in anul:
				anul.add(node)
				changed = True
	
		elif node.char == '.' or node.char == '+':
			# Es anulable si todos los hijos son anulables
			all_anul = True
	
			for n in node.links:
				all_anul = all_anul & (n in anul)
	
			if all_anul and node not in utiles:
				anul.add(node)
				changed = True
	
		else:
			# Todos los nodos deberian tener algun caracter
			# de los anteriores
			raise Exception('Tipo de nodo desconocido: ', node.char)
	
	# FIN


	iterar_grafo(g, f)

	# Hacerlo diccionario
	anul_dicc = {}
	for node in g.nodes:
		anul_dicc[node] = (node in anul)
	return anul_dicc


def primeros(g):

	anul = anulables(g)

	# Ponemos todas las claves con el conjunto vacio (no tienen primeros)
	prim = {}
	for node in g.nodes:
		prim[node] = set()

	def f(node):
		global changed

		# Analizamos el nodo actual
		if node.char in string.lowercase:
			# Los primeros de un terminal, es el terminal
			if node.char not in prim[node]:
				prim[node].add(node.char)
				changed = True

		elif node.char == '\\':
			return

		elif node.char == '|' or node.char == '*' or node.char == '?' \
				or node.char in string.uppercase \
				or node.char ==	'+':

			# El nodo actual debe contener a todos los primeros de
			# sus hijos
			for hijo in node.links:
				if not prim[node].issuperset(prim[hijo]):
					prim[node] = prim[node].union(prim[hijo])
					changed = True

		elif node.char == '.':
			# si el primer hijo es anulable, agregamos los del otro
			# hijo y asi hasta que no sea anulable
			for hijo in node.links:

				if not prim[node].issuperset(prim[hijo]):
					prim[node] = prim[node].union(prim[hijo])
					changed = True

				# seguimos mientras sea anulable
				if not anul[hijo]:
					break

		else:
			# Todos los nodos deberian tener algun caracter
			# de los anteriores
			raise Exception('Tipo de nodo desconocido', node.char)

	# FIN


	iterar_grafo(g, f)
	return prim

def siguientes(g):

	anul = anulables(g)
	prim = primeros(g)

	# Ponemos todas las claves con el conjunto vacio (no tienen siguientes)
	sig = {}
	for node in g.nodes:
		sig[node] = set()

	def f(node):
		global changed
		# Analizamos el nodo actual
		if node.char in string.lowercase or node.char == '\\':
			return

		elif node.char == '|' or node.char == '*' or node.char == '?' \
				or node.char in string.uppercase \
				or node.char ==	'+':
			# los siguientes de este nodo, son siguientes de todos
			# sus hijos

			for hijo in node.links:
				if not sig[hijo].issuperset(sig[node]):
					sig[hijo] = sig[hijo].union(sig[node])
					changed = True

		elif node.char == '.':
			# Los siguientes de este nodo, son siguientes del
			# ultimo. Y si el ultimo es anulable, son siguientes del
			# anterior tambien, y así sucesivamente.
			# (No hay do-while, asique lo hacemos a mano)
			l = node.links
			i = len(l) - 1

			if not sig[l[i]].issuperset(sig[node]):
				sig[l[i]] = sig[l[i]].union(sig[node])
				changed = True

			anulable = anul[l[i]]
			while anulable:
				i = i -1
				if i >= 0:
					anulable = anul[l[i]]
				else:
					break

				if not sig[l[i]].issuperset(sig[node]):
					sig[l[i]] = sig[l[i]].union(sig[node])
					changed = True


			# Para todos dos hijos x, y consecutivos, siguientes de
			# x incluye a primeros y
			for x in range(0, len(l) - 1):
				# x es un elemento e y es el siguiente
				y = l[x+1]
				x = l[x]
				if not sig[x].issuperset(prim[y]):
					sig[x] = sig[x].union(prim[y])
					changed = True

		else:
			# Todos los nodos deberian tener algun caracter
			# de los anteriores
			raise Exception('Tipo de nodo desconocido: ', node.char)

	# FIN


	sig[g.root].add('$')
	iterar_grafo(g, f)
	return sig


