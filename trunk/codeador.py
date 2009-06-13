#!/usr/bin/env python
#coding: utf8

from graph import *

def codearGrafo(g,SD,PR):
	#Primero un par de includes
	print '#include <iostream>'
	print '#include <string>'
	print 'using namespace std;'

	raiz = g.root
	# Supongo que root es un nodo y no simplemente el nombre del simbolo distinguido
	# Si no es Vn tiro un assert
	assert(isVn(raiz))
	for n in g.nodes:
		if isVn(n):
			codear_Vn(n,SD,PR)

def codear_Vn(n,SD,PR):
	linea = 'Proc_' + n.char + '(){'
	print linea
	#print "".join(linea)
	for h in n.links:
		codearNodo(h,SD,PR)
	print '}'

def codear_Vt(n,SD,PR):
	linea = 'match(' + n.char + ');'
	print linea

def codear_Pipe(n,SD,PR):
	for h in n.links:
		linea = 'if' + cond_inDic(h,SD) + '{'

		print linea
		codearNodo(h,SD,PR)
		print '}'
	# Si no estaba en ninguno de los SD de los hijos tengo que hacer que tire un error
	print '"cout << Se esperaba alguno de los siguientes caracteres:">>endl;'
	print '"cout <<"'+ SDHijos(n,SD) +'"<< endl;'
	print '"cout << Se tiene: " << tc << endl;'
	print 'throw 0\n'
	# No se como hacer para que el programa pare (en C++), entonces tiro una excepcion y listo

def codear_Y(n,SD,PR):
	for h in n.links:
		codearNodo(h,SD,PR)
	
def codear_Estr(n,SD,PR):
	# Supongo que tiene un solo hijo
	h = n.links[0]:

	linea = 'while'+ cond_inDic(h,PR) + '{'
	print linea
	codearNodo(h,SD,PR)
	print '}'

def codear_Mas(n,SD,PR):
	# Supongo que tiene un solo hijo
	h = n.links[0]:

	print 'do{'
	codearNodo(h,SD,PR)
	linea = '}while'+ cond_inDic(h,PR) + '{'
	print linea + ';'

def codear_Preg(n,SD,PR):
	h = n.links[0]:
	linea =  'if' + cond_inDic(h,PR) + '{'
	print linea
	codearNodo(h,SD,PR)
	

def SDHijos(n,SD):
	sds = ''
	for h in n.links:
		for sd in SD[h]:
			sds += sd + ', '
	return sds


def cond_inDic(n,dic):
	linea = '('
	for sd in dic[n]:
		linea += ' tc==' + sd + '||'
		linea += 'false)'
	return linea



def codearNodo(h,SD,PR):
	if h.char.isupper(): # Vn
		linea = 'Proc_'+ h.char +'();'
		print linea
		# codear un no terminal es llamar a la funcion
	elif h.char.islower(): # Vt
		codear_Vt(h)
	elif h.char == '|':
		codear_Pipe(h,SD,PR)
	elif h.char == '*':
		codear_Estr(h,SD,PR)
	elif h.char == '+':
		codear_Mas(h,SD,PR)
	elif h.char == '.':
		codear_Y(h,SD,PR)
	elif h.char == '?':
		codear_Preg(h,SD,PR)
	else:
		# Tirar error
		raise Exception('Tipo de nodo desconocido\n')



