#!/usr/bin/env python
#coding: utf8

import sys
from random import randint, shuffle

# permitimos mas recursion que la normal; con esto manejamos hasta
# grafos de un poco mas de 15000 nodos
sys.setrecursionlimit(20000)


"""
class Node:
	def __init__(self, id = None):
		self.id = id
		self.links = set()

	def __repr__(self):
		return "<Node %s (%s)>" % (self.id, id(self))

	def __hash__(self):
		# para poder ponerlos en un set necesitamos que sean
		# hasheables. Vamos a asumir que no nos interesa tener un hash
		# consistente y con el id alcanza
		return id(self)
"""


class CompleteGraph:
	def __init__(self, nnodes):
		# nnodes es la cantidad de nodos
		# los nodos van de 0 a nnodes - 1
		self.nnodes = nnodes
		self.wtable = {}

	def add_link(self, n1, n2, weight):
		k = [n1, n2]
		k.sort()
		k = tuple(k)
		self.wtable[k] = weight

	def get_weight(self, n1, n2):
		k = [n1, n2]
		k.sort()
		k = tuple(k)
		return self.wtable[k]


def dup_node(g, src):
	g.nnodes = g.nnodes + 1

	# el nro del nodo nuevo es el nro mayor
	newnode = g.nnodes - 1

	for (i, j), w in g.wtable.iteritems():
		if src == i:
			g.add_link(newnode, j, w)
		elif src == j:
			g.add_link(newnode, i, w)

	g.add_link(newnode, src, 0)

	return newnode


def for_each_perm(elems, f):
	"""Para cada permutación (completa o parcial) de los elementos de la
	lista "elems", aplica la función f(perm, partial, intres)."""

	# funcion auxiliar para la iteracion
	def gperm(hay, quedan, f, intres = None):
		if not quedan:
			#print '~ F', hay, intres
			f(hay, partial = 0, intres = intres)
			return

		for e in quedan:
			nq = quedan[:]
			nq.remove(e)
			nh = hay + [e]

			#print '~ p', nh, nq, intres

			cont, nir = f(nh, partial = 1, intres = intres)
			if not cont:
				#print '~ X'
				continue

			gperm(nh, nq, f, nir)

	hay = []
	quedan = elems
	gperm(hay, quedan, f)


def tsp_exacto(g, src):
	"""TSP exacto por backtracking. Devuelve el camino mínimo y su
	longitud."""
	# minp[0] es el camino minimo, minp[1] es su longitud
	minp = [(), sys.maxint]

	def esminima(perm, partial, intres):
		"""Función que determina si la permutación dada es menor que
		la de minp, y de serlo la graba en minp."""

		perm = [src] + perm

		if not intres:
			intres = 0

		if partial:
			if len(perm) == 1:
				# hay un solo nodo, no sumamos nada y seguimos
				# recorriendo
				return True, 0

			#print ' - p', perm, intres, g.get_weight(perm[-1], perm[-2])
			suma = intres + g.get_weight(perm[-1], perm[-2])
			if suma > minp[1]:
				#print '   X'
				# no me interesa devolver el parcial porque
				# estamos cortando
				return False, None

			# seguimos recorriendo
			return True, suma
		else:
			# esta todo sumado, agregamos el ultimo link al origen
			# para completar la vuelta
			#print ' - f', perm, intres, g.get_weight(perm[-1], src)
			suma = intres + g.get_weight(perm[-1], src)
			if minp[1] > suma:
				minp[0] = perm + [src]
				minp[1] = suma
				#print '    !', minp

	# las permutaciones las queremos sobre todos los nodos menos src
	elems = range(0, g.nnodes)
	elems.remove(src)
	for_each_perm(elems, esminima)

	return tuple(minp[0]), minp[1]


def tsp_greedy(g, src):
	"""TSP con heuristica golosa. Devuelve el camino mínimo y su
	longitud."""
	path = [src]
	weight = 0

	n = 0
	while len(path) < g.nnodes:
		# nro de nodo, peso
		min_neigh = (None, sys.maxint)

		s = path[-1]
		for i in range(0, g.nnodes):
			if i in path:
				continue

			nw = g.get_weight(s, i)
			if nw < min_neigh[1]:
				min_neigh = (i, nw)

		path.append(min_neigh[0])
		weight += min_neigh[1]

	weight += g.get_weight(src, path[-1])
	path.append(src)

	return tuple(path), weight



def gen_test_graphs_simple(nmin, nmax, step):
	"""Generador de grafos completos para TSP simples: el camino mínimo es
	siempre el que tiene todos 1s, y el resto de los enlaces tiene valores
	mayores a 3. Genera el grafo, el camino mínimo, y la longitud de
	este."""
	g = CompleteGraph(nmin)

	# llenamos el grafo con valores al azar mayores a 3
	for n1 in range(0, nmin):
		for n2 in range(0, nmin):
			if n1 == n2:
				continue
			g.add_link(n1, n2, randint(3, 30))

	while g.nnodes < nmax:
		prevnnodes = g.nnodes
		g.nnodes = g.nnodes + step

		# para todos los nuevos, creamos un camino
		for n1 in range(prevnnodes, g.nnodes):
			for n2 in range(0, g.nnodes):
				if n1 == n2:
					continue
				g.add_link(n1, n2, randint(3, 30))

		# actualizamos el camino mínimo, re-generandolo asi sale
		# distinto que el anterior
		l = range(0, g.nnodes)
		shuffle(l)
		l.append(l[0])
		for n1, n2 in ( (n1, l[i + 1])
					for i, n1 in enumerate(l[:-1]) ):
			g.add_link(n1, n2, 1)

		minpath = tuple(l)
		weight = len(minpath) - 1

		yield (g, minpath, weight)

		# "tapamos" el camino mínimo para que la proxima iteración
		# podamos generar uno distinto
		for n1, n2 in ( (n1, l[i + 1])
					for i, n1 in enumerate(l[:-1]) ):
			g.add_link(n1, n2, randint(3, 30))


def test(nmin, nmax, step = 1):
	"""Testea los algoritmos de TSP con los distintos generadores
	disponibles."""
	for g, minpath, weight in gen_test_graphs_simple(nmin, nmax, step):
		for tsp_f in tsp_exacto, tsp_greedy:
			print tsp_f.__name__,
			opath, oweight = tsp_f(g, minpath[0])
			if weight == oweight and (minpath == opath or
					minpath == opath[::-1]):
				print 'Pass', g.nnodes
			else:
				print 'Fail', g.nnodes
				t = g.wtable.items()
				#t.sort(key = lambda x: (x[1], x[0]))
				t.sort()
				print '  Table:'
				for i in range(g.nnodes):
					print '    ', [ x for x in t
							if x[0][0] == i ]
				print ' ', minpath, weight, '--', opath, oweight
				return False

	return True


"""
def process_in(f):
	input = []

	n = int(f.readline().strip())
	while n != -1:
		nlist = []
		g = Graph()
		for i in range(n):
			node = Node()
			g.add_node(node)
			nlist.append(node)

		for i in range(n):
			l = map(int, f.readline().split())
			for neighbour in l[1:]:
				g.add_link(nlist[i], nlist[neighbour - 1])

		input.append(g)
		n = int(f.readline().strip())

	return input

def process_out(f, reslist):
	for r in reslist:
		if r:
			f.write('Ejercicios 5.10 y 5.29\n')
		else:
			f.write('Ay, caramba!\n')


if __name__ == '__main__':
	if len(sys.argv) != 3:
		fin = open('Tp2Ej1.in')
		fout = open('Tp2Ej1.out', 'w')
	else:
		if sys.argv[1] == '-':
			fin = sys.stdin
		else:
			fin = open(sys.argv[1])

		if sys.argv[2] == '-':
			fout = sys.stdout
		else:
			fout = open(sys.argv[2], 'w')

	graphs = process_in(fin)
	results = map(orientable, graphs)
	process_out(fout, results)
"""

if __name__ == '__main__':
	while True:
		if not test(3, 20, 1):
			break

