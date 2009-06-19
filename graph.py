#!/usr/bin/env python
#coding: utf8

class Node:
	def __init__(self, id = None, char = None):
		self.id = id
		self.links = []
		self.char = char

	def __repr__(self):
		return "<Node char: %s>" % self.char

	def __cmp__(self, other):
		return cmp(self.id, other.id)

	def __hash__(self):
		if self.id is None:
			return id(self)
		return hash(self.id)

	def add_link(self, n1):
		""" Agrega un link de self a n1. Como es un grafo dirigido, esto
		NO es lo mismo que agregar un link al revés"""
		if n1 not in self.links:
			self.links.append(n1)

class Graph:
	def __init__(self, root):
		self.nodes = set([root])
		# "root" es el simbolo distinguido
		self.root = root

	def add_node(self, node):
		self.nodes.add(node)

	def add_link(self, n1, n2):
		""" Agrega un link de n1 a n2. Como es un grafo dirigido, esto
		NO es lo mismo que agregar un link de n2 a n1"""
		if n2 not in n1.links:
			n1.links.append(n2)
		self.nodes.add(n1)
		self.nodes.add(n2)

	# TODO: testear 
	# XXX: no pasa nada si un llamado recursivo borra algun elemento de
	# node.links ? sigue iterando bien despues ?
	def remove_subgraph(self, node):

		# Si esta, lo sacamos (lo puede haber sacado un llamado
		# recursivo)
		if node in self.nodes:
			self.nodes.remove(node)

		# Sacamos todos los hijos de este nodo tambien
		for n in node.links:
			remove_subgraph(self, n)

