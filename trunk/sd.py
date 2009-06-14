#!/usr/bin/env python
#coding: utf8

import string
from graph import *

import sys

# permitimos mas recursion que la normal; con esto manejamos hasta
# grafos de un poco mas de 15000 nodos
sys.setrecursionlimit(20000)

# XXX: falta considerar en todas las funciones que node.char == lambda

def buscar_utiles(g):
	"""Devuelve un set con los nodos utiles"""

	# Si cambio algo del grafo en esta iteracion
	# HACK: si usamos bool se crea un nuevo objeto, no lo modificamos.
	# Entonces usamos una lista de un elemento, que si nos deja modificar
	changed = [True]
	#changed = True

	# Ningun nodo es util salvo que demuestre lo contrario
	utiles = set()

	# Ningun nodo fue visitado todavia
	visited = set()

	def buscar_utiles_desde(node):
		if node in visited:
			return

		visited.add(node)

		# Nos llamamos recursivamente con todos los hijos
		for n in node.links:
			buscar_utiles_desde(n)

		# Analizamos el nodo actual
		if node.char in string.lowercase or node.char == '*' or \
			node.char == '\\' or node.char == '?':
			# Un terminal siempre es util :)
			# El resto tmb son utiles, producen lambda
			if node not in utiles:
				utiles.add(node)
				#changed = True
				changed[0] = True

		elif node.char in string.uppercase or node.char == '|':
			# Si es un no terminal, deriva en un "|" o en una
			# produccion "posta": asique siempre tiene un hijo, y es
			# util si ese hijo es util
			# Si es un '|' es util si algun hijo es util

			some_util = False

			for n in node.links:
				some_util = some_util | (n in utiles)

			if some_util and node not in utiles:
				utiles.add(node)
				changed[0] = True

		elif node.char == '.' or node.char == '+':
			# Es util si todos los hijos son utiles
			all_util = True

			for n in node.links:
				all_util = all_util & (n in utiles)

			if all_util and node not in utiles:
				utiles.add(node)
				changed[0] = True

		else:
			# Todos los nodos deberian tener algun caracter
			# de los anteriores
			print "ERROR! nodo invalido en sacar_inutiles!"

		# FIN

	while changed[0]:
		changed[0] = False
		visited = set()
		buscar_utiles_desde(g.root)

	return utiles

def sacar_inutiles(g):

	utiles = buscar_utiles(g)
	print utiles

	# Sacar los nodos pertenecientes a producciones inutiles o las
	# producciones o hacer algo al respecto! :)
	# XXX: si '*' tiene un hijo inutil, borrarlo y poner lambda ?
	# XXX: estamos seguros que es necesario hacer esto ???

def buscar_anulables(g):
	"""Devuelve un set con los nodos anulables"""

	# Si cambio algo del grafo en esta iteracion
	changed = [True]
	#changed = True

	# Ninguno es anulable hasta que demuestre lo contrario
	anulables = set()

	# Ningun nodo fue visitado todavia
	visited = set()

	def buscar_anulables_desde(node):
		if node in visited:
			return

		visited.add(node)

		# Nos llamamos recursivamente con todos los hijos
		for n in node.links:
			buscar_anulables_desde(n)

		# Analizamos el nodo actual
		if node.char in string.lowercase:
			# Un terminal nunca es anulable
			return

		elif node.char == '*' or node.char == '?' or node.char == '\\':
			# Siempre es anulable
			if node not in anulables:
				anulables.add(node)
				changed[0] = True

		elif node.char in string.uppercase or node.char == '|':
			# Es anulable si algun hijo es anulable

			some_anul = False

			for n in node.links:
				some_anul = some_anul | (n in anulables)

			if some_anul and node not in anulables:
				anulables.add(node)
				changed[0] = True

		elif node.char == '.' or node.char == '+':
			# Es anulable si todos los hijos son anulables
			all_anul = True

			for n in node.links:
				all_anul = all_anul & (n in anulables)

			if all_anul and node not in utiles:
				anulables.add(node)
				changed[0] = True

		else:
			# Todos los nodos deberian tener algun caracter
			# de los anteriores
			print "ERROR! nodo invalido en sacar_inutiles!"

		# FIN

	while changed[0]:
		changed[0] = False
		visited = set()
		buscar_anulables_desde(g.root)

	return anulables

def anulables(g):
	""" Devuelve un diccionario con una clave por nodo y True/False como
	valor asociado representando si el nodo es anulable o no"""

	anulables = buscar_anulables(g)

	# Hacerlo diccionario
	anul_dicc = {}
	for node in g.nodes:
		anul_dicc[node] = (node in anulables)
	
	return anul_dicc


def buscar_primeros(g, anulable):
	"""Devuelve un diccionario con una clave por nodo y los primeros de ese
	nodo como valor asociado"""

	# Si cambio algo del grafo en esta iteracion
	changed = [True]

	# Ponemos todas las claves con el conjunto vacio (no tienen primeros)
	primeros = {}
	for node in g.nodes:
		primeros[node] = set()

	# Ningun nodo fue visitado todavia
	visited = set()

	def buscar_primeros_desde(node):
		if node in visited:
			return

		visited.add(node)

		# Nos llamamos recursivamente con todos los hijos
		for n in node.links:
			buscar_primeros_desde(n)

		# Analizamos el nodo actual
		if node.char in string.lowercase:
			# Los primeros de un terminal, es el terminal
			if node.char not in primeros[node]:
				primeros[node].add(node.char)
				changed[0] = True

		elif node.char == '\\':
			# lambda no tiene primeros, y NO deberia tener hijos
			# XXX: y si lambda pertenece al lenguaje ? no deberia
			# tener primeros ?
			# XXX: que lambda forme parte de primeros de este nodo
			# no es lo mismo que este nodo sea anulable ?
			return

		elif node.char == '|' or node.char == '*' or node.char == '?' \
				or node.char in string.uppercase \
				or node.char ==	'+':

			# El nodo actual debe contener a todos los primeros de
			# sus hijos
			for hijo in node.links:
				if not primeros[node].issuperset(primeros[hijo]):
					primeros[node] = primeros[node].union(primeros[hijo])
					changed[0] = True

				# Para cada nodo que esta en primeros del hijo
				# pero no en primeros del nodo, lo agregamos
				#for n in primeros[hijo].difference(primeros[node]):
				#	primeros[node].add(n.char)
				#	changed[0] = True

		elif node.char == '.':
			# si el primer hijo es anulable, agregamos los del otro
			# hijo y asi hasta que no sea anulable
			for hijo in node.links:

				if not primeros[node].issuperset(primeros[hijo]):
					primeros[node] = primeros[node].union(primeros[hijo])
					changed[0] = True

				# seguimos mientras sea anulable
				if not anulable[hijo]:
					break

		else:
			# Todos los nodos deberian tener algun caracter
			# de los anteriores
			print "ERROR! nodo invalido en sacar_inutiles!"

		# FIN

	while changed[0]:
		changed[0] = False
		visited = set()
		buscar_primeros_desde(g.root)

	return primeros

def primeros(g):
	""" Devuelve un diccionario con una clave por nodo y como valor asociado
	los primeros de ese nodo"""

	anul = anulables(g)
	prim = buscar_primeros(g, anul)

	return prim

def buscar_siguientes(g, anul, prim):

	# Si cambio algo del grafo en esta iteracion
	changed = [True]

	# Ponemos todas las claves con el conjunto vacio (no tienen siguientes)
	sig = {}
	for node in g.nodes:
		sig[node] = set()

	# Ningun nodo fue visitado todavia
	visited = set()

	def buscar_sig_desde(node):
		if node in visited:
			return

		visited.add(node)

		# Nos llamamos recursivamente con todos los hijos
		for n in node.links:
			buscar_sig_desde(n)

		# Analizamos el nodo actual
		if node.char in string.lowercase or node.char == '\\':
			return

		elif node.char == '|' or node.char == '*' or node.char == '?' \
				or node.char in string.uppercase \
				or node.char ==	'+':

			for hijo in node.links:
				if not sig[hijo].issuperset(sig[node]):
					sig[hijo] = sig[hijo].union(sig[node])
					changed[0] = True

		elif node.char == '.':
			# Los siguientes de '.' son tambien siguientes del
			# ultimo nodo
			l = node.links
			last_node = l[len(l) - 1]
			if not sig[last_node].issuperset(sig[node]):
				sig[last_node] = sig[last_node].union(sig[node])
				changed[0] = True

			# Para todos dos hijos x, y consecutivos, siguientes de
			# x incluye a primeros y
			for x in range(0, len(l) - 1):
				# x es un elemento e y es el siguiente
				y = l[x+1]
				x = l[x]
				if not sig[x].issuperset(prim[y]):
					sig[x] = sig[x].union(prim[y])
					changed[0] = True

		else:
			# Todos los nodos deberian tener algun caracter
			# de los anteriores
			print "ERROR! nodo invalido en sacar_inutiles!"

		# FIN

	# siguientes del simbolo distinguido es '$'
	sig[g.root] = '$'
	while changed[0]:
		changed[0] = False
		visited = set()
		buscar_sig_desde(g.root)

	return sig

def siguientes(g):
	"""Devuelve un diccionario con una clave por nodo y los siguientes de
	ese nodo como valor asociado"""

	anul = anulables(g)
	prim = primeros(g)
	sig = buscar_siguientes(g, anul, prim)

	return sig



def test1():
	a = [True]

	def test2():
		a[0] = False

	test2()
	print a

print "Hola!"

#d_reverse = reverse_dict(d)
#print d_reverse
#r = Node(0, 'S')
##n1 = Node(1, 'A')
#n2 = Node(2, '.')
#n3 = Node(3, 'B')
#n4 = Node(4, 'a')
#n5 = Node(5, 'b')
#g = Graph(r)
##g.add_link(r, n1)
#g.add_link(r, n2)
##g.add_link(n1, n3)
#g.add_link(n2, n3)
#g.add_link(n2, n4)
#g.add_link(n3, n5)
##sacar_inutiles(g)
#print "anulables: ", anulables(g)
#print "primeros: ", primeros(g)
#print "siguientes: ", siguientes(g)
##test1(0)
