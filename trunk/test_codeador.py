from codeador import *

r = Node(0, 'S')
#n1 = Node(1, 'A')
n2 = Node(2, '|')

n3 = Node(3, 'A')
n4 = Node(4, 'B')
n5 = Node(5, 'C')

n6 = Node(6, 'a')
n7 = Node(7, 'b')
n8 = Node(8, 'c')
g = Graph(r)
#g.add_link(r, n1)
g.add_link(r, n2)
#g.add_link(n1, n3)
g.add_link(n2, n3)
g.add_link(n2, n4)
g.add_link(n2, n5)

g.add_link(n3, n6)
g.add_link(n4, n7)
g.add_link(n5, n8)

#print buscar_utiles(g)
#print utiles(g)

#sacar_inutiles(g)
#print "anulables: ", anulables(g)
#print "primeros: ", primeros(g)
#print "siguientes: ", siguientes(g)

codearGrafo(g)
