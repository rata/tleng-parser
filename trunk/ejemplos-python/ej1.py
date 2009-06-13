#!/usr/bin/env python
#coding: utf-8

import sys


class NotPossible (Exception):
	pass


class Bucket:
	def __init__(self, dst = None, depth = 0):
		self.dst = dst
		self.depth = depth


class Partition:
	def __init__(self, n):
		self.n = n
		self.table = {}

		for i in range(1, n + 1):
			self.table[i] = Bucket()

	def get_id(self, i):
		b = self.table[i]
		while b.dst != None:
			b = b.dst
		return b

	def juntar(self, i, j):
		bi = self.get_id(i)
		bj = self.get_id(j)

		if bi == bj:
			return

		if bi.depth < bj.depth:
			bi.dst = bj
		elif bi.depth > bj.depth:
			bj.dst = bi
		else:
			bj.dst = bi
			bi.depth += 1

	def juntos(self, i, j):
		return self.get_id(i) == self.get_id(j)


def process_instrs(n, instrs):
	results = []

	p = Partition(n)
	for instr, i, j in instrs:
		if instr == 'Juntar':
			p.juntar(i, j)
			results.append(None)
		elif instr == 'Juntos':
			results.append(p.juntos(i, j))
		else:
			raise NotPossible

	return results


def process_in(f):
	input = []

	n, p = map(int, f.readline().split())
	while n != -1:
		linst = []
		for i in range(p):
			inst = f.readline().split()
			inst = ( inst[0], int(inst[1]), int(inst[2]) )
			linst.append(inst)
		input.append((n, linst))

		# por si en la ultima linea solo esta n y no p
		try:
			n, p = map(int, f.readline().split())
		except:
			n = -1

	return input

def process_out(f, results):
	for n, res in results:
		f.write("%d %d\n" % (n, len(res)))
		for i in res:
			if i == None:
				f.write("Hecho\n")
			elif i == True:
				f.write("Verdadero\n")
			elif i == False:
				f.write("Falso\n")
			else:
				raise NotPossible


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

	partitions = process_in(fin)

	results = []
	for n, instrs in partitions:
		results.append( (n, process_instrs(n, instrs)) )

	process_out(fout, results)



