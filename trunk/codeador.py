#!/usr/bin/env python
#coding: utf8

from graph import *
from sd import simbolos_directrices, primeros

def codearGrafo(g):
	SD = simbolos_directrices(g)
	PR = primeros(g)
	raiz = g.root

	#Primero un par de includes
	print '#include <iostream>'
	print '#include <string>'
	print '#include "utilitario.cpp"'
	print
	print 'using namespace std;'
	print
	# Supongo que root es un nodo y no simplemente el nombre del simbolo distinguido
	# Si no es Vn tiro un assert, pa joder nomás
	assert(raiz.char.isupper()) # Root es Vn
	#Escribo primero los prototipos de las Funciones
	for n in g.nodes:
		if n.char.isupper():
			linea = 'void Proc_'+ n.char +'();'
			print linea
	print 'void parsear();'
	print
	#Escribo ahora los cuerpos de las funciones
	print 'void parsear(){'
	linea = 'Proc_'+ raiz.char + '();'
	print linea
	print '}'

	for n in g.nodes:
		if n.char.isupper():
			print
			codear_Vn(n,SD,PR)

	print 


def codear_Vn(n,SD,PR):
	linea = 'void Proc_' + n.char + '(){'
	print linea
	#print "".join(linea)
	if len(n.links) > 1:
		codear_Pipe(n,SD,PR)
	else:
		for h in n.links:
			codearNodo(h,SD,PR)
	print '}'

def codear_Vt(n):
	if n.char == '\\':
		linea = 'match(\'\\' + n.char + '\');'
	else:
		linea = 'match(\'' + n.char + '\');'
	print linea

def codear_Pipe(n,SD,PR):
	primero = True

	# Si no tiene ningun hijo, entonces no reconoce nada
	# Pasa solo en un caso muy patologico, donde la gramatica no  produce
	# nada. En general, el grafo tiene solo los nodos activos. Pero si
	# ninguno es activo, el g.root no se lo podemos sacar al grafo y
	# entonces hay que manejar ese caso.
	if len(n.links) == 0:
		print 'cout << "###################################################" <<endl;'
		print 'cout << "ERROR: Cadena invalida" << endl; '
		print 'cout << "Entrada: \'" << tc << "\'" << endl;'
		print 'cout << "Esperando:', SDHijos(n,SD) ,'"<< endl;'
		print 'cout << "###################################################" <<endl;'
		print 'throw 0;'
		return

	for h in n.links:
		if primero:
			linea = 'if' + cond_inDic(h,SD) + '{'
			primero = False
		else:
			linea = 'else if' + cond_inDic(h,SD) + '{'

		print linea
		codearNodo(h,SD,PR)
		print '}'
	# Si no estaba en ninguno de los SD de los hijos tengo que hacer que tire un error
	print 'else{'
	print 'cout << "###################################################" <<endl;'
	print 'cout << "ERROR: Cadena invalida" << endl;'
	print 'cout << "Entrada: \'" << tc << "\'" << endl;'
	print 'cout << "Esperando:', SDHijos(n,SD) ,'"<< endl;'
	print 'cout << "###################################################" <<endl;'
	print 'throw 0;'
	print '}'
	# No se como hacer para que el programa pare (en C++), entonces tiro una excepcion y listo

def codear_Y(n,SD,PR):
	for h in n.links:
		codearNodo(h,SD,PR)
	
def codear_Estr(n,SD,PR):
	# Supongo que tiene un solo hijo
	h = n.links[0]

	linea = 'while'+ cond_inDic(h,PR) + '{'
	print linea
	codearNodo(h,SD,PR)
	print '}'

def codear_Mas(n,SD,PR):
	# Supongo que tiene un solo hijo
	h = n.links[0]

	print 'do{'
	codearNodo(h,SD,PR)
	linea = '}while'+ cond_inDic(h,PR) + ';'
	print linea

def codear_Preg(n,SD,PR):
	h = n.links[0]
	linea =  'if' + cond_inDic(h,PR) + '{'
	print linea
	codearNodo(h,SD,PR)
	print '}'
	

def SDHijos(n,SD):
	sds = []
	for h in n.links:
		for simbd in SD[h]:
			sds += simbd
	return sds


def cond_inDic(n,dic):
	linea = '('
	for ed in dic[n]:
		linea += ' tc==\'' + ed + '\' ||'
	linea += 'false)'
	return linea



def codearNodo(h,SD,PR):
	if h.char.isupper(): # Vn
		# codear un no terminal es llamar a la funcion
		linea = 'Proc_'+ h.char +'();'
		print linea
	elif h.char.islower() or h.char == '\\': # Vt
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
		raise Exception('Tipo de nodo desconocido: ', h.char)



