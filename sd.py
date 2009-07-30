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


def activos(g):

	activo = set()

	def f(node):
		global changed
		# Analizamos el nodo actual
		if node.char in string.lowercase or node.char == '*' or \
			node.char == '\\' or node.char == '?':
			# Un terminal siempre es activo :)
			# El resto tmb son activos, producen lambda
			if node not in activo:
				activo.add(node)
				changed = True
	
		elif node.char in string.uppercase or node.char == '|':
			# Es activo si algun hijo es activo
	
			some_activo = False
	
			for n in node.links:
				some_activo = some_activo | (n in activo)
	
			if some_activo and node not in activo:
				activo.add(node)
				changed = True
	
		elif node.char == '.' or node.char == '+':
			# Es activo si todos los hijos son activos
			all_activo = True
	
			for n in node.links:
				all_activo = all_activo & (n in activo)
	
			if all_activo and node not in activo:
				activo.add(node)
				changed = True
	
		else:
			# Todos los nodos deberian tener algun caracter
			# de los anteriores
			raise Exception('Tipo de nodo desconocido: ' + node.char)

	iterar_grafo(g, f)
	return activo

def sacar_link_a_inactivos(g):
	"""Saca el link de un nodo cualquiera a un nodo inactivo. Tambien,
	si el nodo es * o ? y el hijo inactivo, reemplaza * o ? por lambda
	NOTA: pueden quedar cosas feas, como un | con un solo hijo, y que encima
	ese hijo sea lambda y cosas así"""

	activo = activos(g)

	def f(node):
		global changed
		
		if (node.char == '*' or node.char == '?'): 
			for n in node.links:
				if n not in activo:
					node.char = '\\'
					changed = True

		for n in node.links:
			if n not in activo:
				node.links.remove(n)
				changed = True

	# FIN
	iterar_grafo(g, f)

def sacar_inalcanzables(g):
	"""Saca del grafo todo los nodos inalcanzables desde el simbolo distinguido"""
	
	alcan = set()

	def f(node):
		alcan.add(node)

	iterar_grafo(g, f)

	# Los nodos del grafo son los alcanzables
	g.nodes = alcan

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
	
			if all_anul and node not in anul:
				anul.add(node)
				changed = True
	
		else:
			# Todos los nodos deberian tener algun caracter
			# de los anteriores
			raise Exception('Tipo de nodo desconocido: ' + node.char)
	
	# FIN


	iterar_grafo(g, f)

	# Hacerlo diccionario
	anul_dicc = {}
	for node in g.nodes:
		anul_dicc[node] = (node in anul)

	return anul_dicc


def primeros(g):
	# XXX: si encontramos un bug aca, fijarse si afecta a check_rec_iz

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
			raise Exception('Tipo de nodo desconocido: ' + node.char)

	# FIN


	iterar_grafo(g, f)
	return prim

def check_rec_iz(g):
	"""Checkea si hay recursividad a iz en el grafo. Devuelve un excepcion
	(explicando donde) si hay, es void sino"""
	# XXX: es CASI igual a primeros. Por lo que capaz si encontramos un bug
	# en alguna de las dos, afecta a la otra

	anul = anulables(g)

	# Ponemos todas las claves con el conjunto vacio (no tienen primeros)
	prim = {}
	for node in g.nodes:
		prim[node] = set()

	def f(node):
		global changed

		# Analizamos el nodo actual
		if node.char in string.lowercase \
				or  node.char == '\\':
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

				if hijo not in prim[node] \
						and hijo.char in string.uppercase:

					prim[node].add(hijo)
					changed = True

		elif node.char == '.':
			# si el primer hijo es anulable, agregamos los del otro
			# hijo y asi hasta que no sea anulable
			for hijo in node.links:

				if not prim[node].issuperset(prim[hijo]):
					prim[node] = prim[node].union(prim[hijo])
					changed = True

				if hijo not in prim[node] \
						and hijo.char in string.uppercase:

					prim[node].add(hijo)
					changed = True

				# seguimos mientras sea anulable
				if not anul[hijo]:
					break

		else:
			# Todos los nodos deberian tener algun caracter
			# de los anteriores
			raise Exception('Tipo de nodo desconocido: ' + node.char)

	# FIN


	iterar_grafo(g, f)

	for k in prim.keys():

		for v in prim[k]:
			if v.char == k.char:
				raise Exception('No es ELL(1). Hay recursion a izquierda en el nodo ' + k.char)
	

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

			# Ademas, SOLO si el nodo es "*" o "+", entonces los
			# primeros del hijo, pertenecen a siguientes del hijo
			if node.char == '*' or node.char == '+':
				hijo = node.links[0]
				if not sig[hijo].issuperset(prim[hijo]):
					sig[hijo] = sig[hijo].union(prim[hijo])
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
			# Y si y es anulable, incluye a los siguientes de y
			for x in range(0, len(l) - 1):
				# x es un elemento e y es el siguiente
				y = l[x+1]
				x = l[x]
				if not sig[x].issuperset(prim[y]):
					sig[x] = sig[x].union(prim[y])
					changed = True

				if anul[y] and not sig[x].issuperset(sig[y]):
					sig[x] = sig[x].union(sig[y])
					changed = True

		else:
			# Todos los nodos deberian tener algun caracter
			# de los anteriores
			raise Exception('Tipo de nodo desconocido: ' + node.char)

	# FIN


	sig[g.root].add('$')
	iterar_grafo(g, f)
	return sig

def check_inutiles(g):

	# Primero chequeo que sean todos alcanzables
	ok = True
	alcan = set()

	def f(node):
		alcan.add(node)

	iterar_grafo(g, f)

	if len(g.nodes) > len(alcan):
		for n in g.nodes:
			if n not in alcan:
				ok = False
				if n.char.isupper():
					raise Exception( 'La gramática posee un noterminal inalcanzable: '+ n.char + '.')

	# Por último chequeo que sean activos
	ok = True
	activo = activos(g)

	def f(node):
		global changed
		
		for n in node.links:
			if n not in activo:
				ok = False

				# Es necesario esto?
				changed = True

				if n.char.isupper():
					raise Exception('La gramática posee un noterminal inactivo: ' + n.char + '.')

	# FIN
	iterar_grafo(g, f)

def calcular_sd(g):

	anul = anulables(g)
	prim = primeros(g)
	sig = siguientes(g)

	sd = {}

	for node in g.nodes:
		sd[node] = prim[node]
		if anul[node]:
			sd[node] = sd[node].union(sig[node])
	return sd

def calcular_ell1(g, anul, prim, sig, sd):
	"""Checkea que el grafo g sea de una gramatica ELL(1)"""
	# XXX: es un asco el codigo (las lineas de las excepciones son
	# larguisimas) y nose si no sera necesario checkear algo mas. Puede ser
	# tranquilamente que no ande :)
	
	def f(node):
		if node.char in string.lowercase \
				or node.char in	string.uppercase\
				or node.char == '\\'\
				or node.char == '.' :

			return

		elif node.char == '|':
			for x in node.links:
				for y in node.links:
					if x == y:
						continue

					# Si la interseccion no es el conjunto vacio
					if sd[x].intersection(sd[y]) != set():
						raise Exception('No es ELL(1). Se encontro '+ str(list(sd[x].intersection(sd[y]))) + ' en comun entre los sd de ' + x.char + ' y los de ' + y.char + '. Ambos hijos de un ' + node.char)

		elif node.char == '+' or node.char == '?' or node.char == '*':
			for n in node.links:
				if prim[n].intersection(sig[node]) != set():
					raise Exception('No es ELL(1). Se encontro ' + str(list(prim[n].intersection(sig[node]))) + ' en comun entre primeros de: ' + n.char + ' y siguientes de: ' + node.char)

				if anul[n]:
					raise Exception('No es ELL(1). ' + n.char + ' es anulable y es hijo de un ' + node.char)

		else:
			raise Exception('Tipo de nodo desconocido: ' + node.char)

	# FIN

	iterar_grafo(g, f)


def simbolos_directrices(g):
	"""Arregla la gramatica y calcula los simbolos directrices de ese grafo
	si la gramatica es ELL(1), sino tira una excepcion.
	Para arreglar la gramatica MODIFICA EL GRAFO dado como parametro.
	Devuelve un diccionario de nodo en simbolos directrices del nodo"""

#	# reducimos la gramatica
#	sacar_link_a_inactivos(g)
#	sacar_inalcanzables(g)

	# Chequeo de que no tenga simbolos inútiles
	check_inutiles(g)

	# checkeamos que la gramatica reducida no sea recursiva a izquierda
	check_rec_iz(g)

	anul = anulables(g)
	prim = primeros(g)
	sig = siguientes(g)
	sd = calcular_sd(g)

	calcular_ell1(g, anul, prim, sig, sd)

	return sd
