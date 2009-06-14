from sd import *


r = Node(0, 'S')
#n1 = Node(1, 'A')
n2 = Node(2, '.')
n3 = Node(3, 'B')
n4 = Node(4, 'a')
n5 = Node(5, 'b')
g = Graph(r)
#g.add_link(r, n1)
g.add_link(r, n2)
#g.add_link(n1, n3)
g.add_link(n2, n3)
g.add_link(n2, n4)
g.add_link(n3, n5)

#print buscar_utiles(g)
#print utiles(g)

print 
#sacar_inutiles(g)
print "anulables: ", anulables(g)
print "primeros: ", primeros(g)
print "siguientes: ", siguientes(g)
