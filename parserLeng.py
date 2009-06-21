from pyparsing import *
from graph import *

otraProdDerecha = Forward()
otraProdAnd		= Forward()
otraGram		= Forward()

mas				= "+"
por				= "*"
pregunta			= "?"
			

valor			= "(" + otraProdDerecha + ")" | Word("abcdefghijklmnopqrstuvwxyz", exact = 1) | Word("ABCDEFGHIJKLMNOPQRSTUVWXYZ", min = 1)
operador 		= Literal("+") | Literal("*") | Literal("?")
operadores		= valor + Optional(operador)
otroMas			= otraProdAnd
prodAnd			= operadores + Optional(otroMas)
prodOr			= "|" + otraProdDerecha
prodDerecha		= prodAnd + Optional(prodOr)
masProducciones	= otraGram
produccion 		= Word("ABCDEFGHIJKLMNOPQRSTUVWXYZ", min = 1) + ":" + prodDerecha + ";"
gram 			= produccion + Optional(masProducciones)
init 			= gram | Literal("$")

otraProdDerecha << prodDerecha
otraProdAnd		<< prodAnd
otraGram		<< gram

_diccNoTermEnProduccion = {}
_simboloInicial 		= "$"
_numeracion				= 1
_diccNoTermEnNumerito 	= {} 
_arboles 				= []

def sinPrimerosDosNiUltimo( lista ):
	
	listaRes = []
	
	for i in range(len(lista) - 3):
		listaRes.append(lista[i+2])
		listaRes.reverse
		
	return  listaRes
			
def test( cadena ):
	
	global _simboloInicial
	global _arboles
	
	try:
		greeting = init.parseString( cadena )
		#print greeting
	except ParseException, pe:
		print pe

	else:
		noTerm = greeting[0]
		
		if _simboloInicial == "$":
			_simboloInicial = noTerm
		
		if noTerm != "$":
			_diccNoTermEnProduccion[noTerm] = sinPrimerosDosNiUltimo( greeting )
			_arboles.append(armarArbol(noTerm,_diccNoTermEnProduccion[noTerm]))

	grafoFinal = armarGrafo(_arboles)	
	return grafoFinal	
					
def parsear():
	
	file = open("gramaticas.txt","r")
	
	for linea in file.readlines():
		#print linea
		grafoFinal = test( linea )
		#agregar a diccionrio
		
	file.close()
	return grafoFinal
	
def noTerminalInicial():
	
	global _simboloInicial
	return _simboloInicial

def esToNT( elemento ):
	res = False
	caracteres = "abcdefghijklmnopqrtsuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	if caracteres.count(elemento) == 1:
		res = True
	
	return res

def esNoTerminal( elemento ):
	res = False
	caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	if caracteres.count(elemento) == 1:
		res = True
	
	return res
	
def esOperador( elemento ):
	res = False
	caracteres = "*+?"
	if caracteres.count(elemento) == 1:
		res = True
	
	return res

def dameListaDesdeHasta(init,end,lista):
	
	listaRes = []
	
	for i in range(len(lista)):
		if i >= init and i <= end:
			listaRes.append(lista[i])
			
	return listaRes

def borrarDesde(lista,desde):
	
	listaTemp = []
	
	for i in range(len(lista)):
		if i < desde:
			listaTemp.append(lista[i])
			
	lista = listaTemp

def reasignarValores(listaDeNodos,val):	
	
	i = 0	

	for nodo in listaDeNodos:
		if not(nodo.char in _diccNoTermEnNumerito):
			nodo.id = nodo.id + val
			reasignarValores(nodo.links,val)

def armarRama( cadena ):

	global _numeracion	
	global _diccNoTermEnNumerito
	
	nodo_padre 		= Node(-1,'@')
	temp			= Node()
	
	elem_anterior 	= '@'
	id_padre		= -1
	numero			= -1
	
	rama 	   		= Graph(nodo_padre)
	
	estabaEnDicc	= False
	
	parentAbre		= 0
	parentCierra	= 0
	parentQueAbren	= []
	index			= 0
	huboCambio		= True
	
	
	revisarSiProxEsOp 	= False
	init				= 0
	end					= 0
	
	for elem in cadena:
		
		if esNoTerminal(elem) and (elem in _diccNoTermEnNumerito):
			
			estabaEnDicc = True
			numero = _diccNoTermEnNumerito[elem]
		else:
			numero = _numeracion
			if esNoTerminal(elem):
				_diccNoTermEnNumerito[elem] = numero
		
				
				
		
		if esToNT(elem):
			if nodo_padre.id == -1:
				nodo_padre.__init__(numero,elem)
				
			else:
				
				if esToNT(nodo_padre.char):
					
					id_padre = nodo_padre.id	
					
					if nodo_padre.char in _diccNoTermEnNumerito:
						temp = Node(id_padre,nodo_padre.char)
						nodo_padre.__init__(_numeracion,'.')
						_numeracion = _numeracion + 1
						nodo_elem = Node(_numeracion,elem)
						rama.add_link(nodo_padre,temp)
						rama.add_link(nodo_padre,nodo_elem)
					
					
					else:
						temp = Node(_numeracion,nodo_padre.char)
						if not estabaEnDicc:
							_numeracion = _numeracion + 1
							numero = _numeracion
							if esNoTerminal(elem):
								_diccNoTermEnNumerito[elem] = numero
						
						nodo_elem = Node(numero,elem)
						nodo_padre.__init__(id_padre,'.')
						rama.add_link(nodo_padre,temp)
						rama.add_link(nodo_padre,nodo_elem)
					
				else: 
					if nodo_padre.char == '.':
						#print "padre es puntito"
						nodo_elem = Node(numero,elem)
						rama.add_link(nodo_padre,nodo_elem)
					else:
						if esOperador(nodo_padre.char):
							
							id_padre = nodo_padre.id
							temp = Node(nodo_padre.id + 1,nodo_padre.char)
							
							temp.links = nodo_padre.links
							reasignarValores(temp.links,1)
							
							
							
							
							
							if not estabaEnDicc:
								_numeracion = _numeracion + 1
								numero = _numeracion
								if esNoTerminal(elem):
									_diccNoTermEnNumerito[elem] = numero
						
							nodo_elem = Node(numero,elem)
							nodo_padre.__init__(id_padre,'.')
							rama.add_link(nodo_padre,temp)
							rama.add_link(nodo_padre,nodo_elem)
						else: 
							if nodo_padre.char == '|':
								nodo_elem = Node(nodo_padre.id,nodo_padre.char)
								nodo_elem.links = nodo_padre.links
								nodo_padre = Node(numero,elem)
								rama.add_link(nodo_elem,nodo_padre)
								
							
								
						
			if revisarSiProxEsOp:
				print "LETRA"
				print elem
				parentQueAbren.pop()
				revisarSiProxEsOp = False			
						
		else:
			if esOperador(elem):
				print("PARTE DE OPERADORES")
				if esToNT(nodo_padre.char):
				 	id_padre = nodo_padre.id
					temp = Node(_numeracion,nodo_padre.char)
				 	nodo_padre.__init__(id_padre,elem)
				 	rama.add_node(temp)
				 	rama.add_link(nodo_padre,temp)
				else:
					if nodo_padre.char == '.':
				 		if elem_anterior == ')':
				 			
				 			init 	= parentQueAbren[len(parentQueAbren) - 1]
				 			print "INIT ES"
				 			print init
				 			end		= parentCierra - 2
				 			elem_id	= nodo_padre.links[init].id
				 			nodo_elem = Node(elem_id,elem)
							links_elem = dameListaDesdeHasta(init,end,nodo_padre.links)			 		
				 			
							if len(links_elem) == 1:
								
								nodo_elem.links = links_elem
								links_elem[0].id = elem_id + 1
								rama.add_link(nodo_padre,nodo_elem)
							
							else:
								if len(links_elem) == len(nodo_padre.links):
									
									
									id_padre = nodo_padre.id
									
									temp = Node(nodo_padre.id + 1,'.')
									temp.links = nodo_padre.links
									
									
									
									reasignarValores(temp.links,2)
									
									
									
									nodo_padre.__init__(id_padre,elem)
									
									rama.add_link(nodo_padre,temp)
									
									
									#nodo_elem.id = nodo_padre.id
									#nodo_padre.id = nodo_padre.id + 1
									#nodo_padre.reasignarValores(nodo_elem.id + 2)
									#rama.add_link(nodo_elem,nodo_padre)
									
								else:
									
									temp = Node(elem_id + 1, '.')
									temp.links = links_elem
									reasignarValores(temp.links,1)
									rama.add_link(nodo_elem,temp)
									borrarDesde(nodo_padre.links,init)
									rama.add_link(nodo_padre,nodo_elem)	
							
								
							
						else:
							
							last_id = nodo_padre.__lastID__()
							temp = Node(last_id,elem_anterior)
							rama.remove_subgraph(temp)
							nodo_padre.__removeLastLink__()
							nodo_elem 			= Node(last_id,elem)
							nodo_elem_anterior 	= Node(_numeracion,elem_anterior)
							rama.add_node(nodo_elem)
							rama.add_node(nodo_elem_anterior)
							rama.add_link(nodo_padre,nodo_elem)
							rama.add_link(nodo_elem,nodo_elem_anterior)
						
						parentQueAbren.pop()
						revisarSiProxEsOp = False	
						index = -1	
					else:
						if esOperador(nodo_padre.char) or nodo_padre.char == '|':
							
							temp = Node(nodo_padre.id+1,nodo_padre.char)
							temp.links = nodo_padre.links
							reasignarValores(temp.links,1)
							
							
						 
							
			else:
				if elem == '(':
					if revisarSiProxEsOp:
						print "ACAAAA"
						parentQueAbren.pop()
						revisarSiProxEsOp = False
						parentAbre = index - 1
					else:
						parentAbre = index
						
					parentQueAbren.append(parentAbre)
					huboCambio = False
						
						
				else:
					if elem == ')':
						parentCierra = index 
						revisarSiProxEsOp = True
						huboCambio = False
					else:
						if elem == '|':
							if esToNT(nodo_padre.char):
								id_padre = nodo_padre.id
								
								if nodo_padre.char in _diccNoTermEnNumerito:
									nodo_temp = Node(id_padre,nodo_padre.char)
									nodo_padre.__init__(numero,'|')
								else:
									nodo_temp = Node(numero,nodo_padre.char)
									nodo_padre.char = '|'
								
								
								rama.add_link(nodo_padre,nodo_temp)
							else:
								if nodo_padre.char == '.' or esOperador(nodo_padre.char) or nodo_padre.char == '|':
									id_padre = nodo_padre.id
									nodo_temp = Nodo(numero,nodo_padre.char)
									nodo_temp.links = nodo_padre.links
									nodo_padre.__init__(id_padre,'|')
									rama.add_link(nodo_padre,nodo_temp)
																		
									
									
						
									
		
		index = index + 1
		elem_anterior = elem
		if not estabaEnDicc and huboCambio:
			_numeracion = _numeracion + 1
		estabaEnDicc 	= False
		huboCambio 		= True
		
	
	
	
	
	return rama
								
def armarArbol(noTerm , produccionDer):

	#print "ARMAR ARBOL"
	#print noTerm
	global _numeracion
	global _diccNoTermEnNumerito

	arboles = []
	cadenas = []
	cadena = []
	
	
	if not (noTerm in _diccNoTermEnNumerito):
		#print "EN EL IF"
		_diccNoTermEnNumerito[noTerm] = _numeracion
		nodo = Node(_numeracion,noTerm)
		_numeracion = _numeracion + 1
	else:
		nodo = Node(_diccNoTermEnNumerito[noTerm],noTerm)
		
	#print "TIENE NUMERITO"
	#print _diccNoTermEnNumerito[noTerm]	
		
	grafoRes = Graph(nodo)
	grafoRama = armarRama(produccionDer)
	grafoRes.extend_graph(grafoRama,nodo,False)
	
	#longitud = len(produccionDer)
	#ultimoElemento = produccionDer[longitud - 1]
	
	#for token in produccionDer:
		
		#print token
	#	if token != '|':
	#		cadena.append(token)
	#		if token == ultimoElemento:
	#			cadenas.append(cadena)
	#	else:
	#		if len(cadena) > 0:
	#			cadenas.append(cadena)
	#			cadena = []
			
	#print cadenas

	
	#if len(cadenas) > 1:
	#	nodoBarrita = Node(_numeracion,"|")
	#	_numeracion = _numeracion + 1
	#	grafoRes.add_link(nodo,nodoBarrita)
		
	#for componente in cadenas:
	#	grafoRama = armarRama(componente)
		#print "grafo de la rama es"
		
	#	if len(cadenas) > 1:
	#		grafoRes.extend_graph(grafoRama,nodoBarrita,False)
	#	else:
	#		print "en el else"
	#		grafoRes.extend_graph(grafoRama,nodo,False)
		
	
	
	print "PRODUCCION A DERECHA"
	print produccionDer
	print "RAMA"
	grafoRama.print_graph()
	print "INICIO"
	grafoRes.print_graph()
	return grafoRes


def armarGrafo(listaDeArboles)	:

	#print "Armar Grafo"
	diccNumArbolEnBool = {}

	for j in range(len(listaDeArboles)):
		diccNumArbolEnBool[j] = True
	
	#print len(listaDeArboles)
		
	i = 0
	grafoRes = listaDeArboles[0]
	diccNumArbolEnBool[0] = False
		
	#print "Puse todos en true"
	
	while(not todosLinkeados(diccNumArbolEnBool)):
		
		for arbol in listaDeArboles:
			
			#arbol.print_graph()	
			raiz = arbol.root
			#print raiz.__repr__()
			if (diccNumArbolEnBool[i] == True) and raiz in grafoRes.nodes:
				#print "EN EL IF CON ARBOL NUMERO"
				#print i
				grafoRes.extend_graph(arbol,raiz,True)
				#print "EL GRAFO ESTA ASI"
				#grafoRes.print_graph()
				
				diccNumArbolEnBool[i] = False
				
			i = i+1		
		
		i = 0


	return grafoRes

def	todosLinkeados(diccNumBool):

	res = True

	for key in diccNumBool:
		if diccNumBool[key]:
			res = False
			
	return res
	
				
grafoEnd = parsear()
#grafoEnd.print_graph()
#grafoFinal = armarGrafo(_arboles)
#grafoFinal.print_graph()
#print noTerminalInicial()

#nodo = Node(1,'R')
#nodo_dos = Node(2,'S')

#grafo1 = armarRama("abc",2)
#grafo2 = Graph(nodo)
#grafo2.add_link(nodo,nodo_dos)
#grafo2.extend_graph(grafo1,nodo_dos)
#grafo2.print_graph()

#_numeracion = 5
#_diccNoTermEnNumerito['T'] = 3
#grafoRes = armarArbol('A',"marTin|diego")
#grafoRes.print_graph()
#print _diccNoTermEnNumerito

#grafoRes = armarArbol('D',"Ad")