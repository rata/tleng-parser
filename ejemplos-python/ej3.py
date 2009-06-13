#!/usr/bin/env python
#coding: utf-8

class Node:
	def __init__(self, id = None):
		self.id = id
		self.links = set()

	def __repr__(self):
		return "<Node %s>" % self.id

	def __cmp__(self, other):
		return cmp(self.id, other.id)

	def __hash__(self):
		if self.id is None:
			return id(self)
		return hash(self.id)

if 0:
	class NDEdge:
		def __init__(self, n1, n2):
			self.nodes = set((n1, n2))

		def __repr__(self):
			return "<NDEdge %s - %s>" % list(self.nodes)

		def __cmp__(self, other):
			return cmp(self.nodes, other.nodes)


class Graph:
	def __init__(self):
		self.nodes = set()
		#self.edges = set()

	def add_node(self, node):
		self.nodes.add(node)

	def add_link(self, n1, n2):
		n1.links.add(n2)
		n2.links.add(n1)
		#self.edges.append((n1, n2))


def orientable(g):
	n = g.nodes.pop()
	n.id = 1
	if orientable_rec(n) != 1:
		return False

	# tenemos que ver ahora si todos los nodos estan marcados
	for n in g.nodes:
		if n.id == None:
			return False

	# todos marcados
	return True

def orientable_rec(n, parent = None):
	rmin = None
	for neighbour in n.links:
		if parent and neighbour.id == parent.id:
			# no tomamos en cuenta el enlace por donde vinimos
			continue

		if neighbour.id:
			# si por aca llego mas lejos, actualizo nuestro minimo
			if rmin is None or neighbour.id < rmin:
				rmin = neighbour.id
			continue

		# siempre si no tengo id le pongo el nuestro mas 1; ver
		# explicación en el informe
		neighbour.id = n.id + 1
		nmin = orientable_rec(neighbour, parent = n)

		# ya sabemos que no puede pasar, devolvemos False para arriba
		if nmin == False:
			return False

		# si una rama no llega como minimo a mi, tampoco vale
		if nmin > n.id:
			return False

		# como antes, si por aca llegamos mas lejos, actualizamos
		# nuestro minimo
		if rmin is None or nmin < rmin:
			rmin = nmin

	#print n.id, rmin, n.links
	if rmin is None:
		# no tuvimos hijitos, ya sabemos que no se puede seguir
		return False
	elif rmin <= n.id:
		# devolvemos cuan lejos se llega por aca
		return rmin
	else:
		# no llegan ni hasta mi, tampoco vale la pena seguir
		return False



def tests():
	n1 = Node()
	n2 = Node()
	n3 = Node()

	g = Graph()
	g.add_node(n1)
	g.add_node(n2)
	g.add_node(n3)

	g.add_link(n1, n2)
	g.add_link(n2, n3)
	g.add_link(n3, n1)

	print 't', orientable(g)


	n1 = Node(); n2 = Node(); n3 = Node()
	n4 = Node(); n5 = Node(); n6 = Node()
	g = Graph()
	for n in (n1, n2, n3, n4, n5, n6):
		g.add_node(n)

	# isla
	g.add_link(n1, n2)
	g.add_link(n2, n3)
	g.add_link(n3, n1)

	# isla
	g.add_link(n4, n5)
	g.add_link(n5, n6)
	g.add_link(n6, n4)

	# puente
	g.add_link(n3, n4)

	print 'f', orientable(g)

tests()


