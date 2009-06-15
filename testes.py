from codeador import *
from sd import *

r = Node(0, 'T')
n1 = Node(1, 'L')
n2 = Node(2, 'A')
n3 = Node(3, 'T')

n4 = Node(4, 'c')
n5 = Node(5, 'n')
n6 = Node(6, 'v')
n7 = Node(7, 'p')
n8 = Node(8, 'q')
n9 = Node(9, 'd')
n10 = Node(10, 'f')
n11 = Node(11, 'e')

n12 = Node(12, '*')
n13 = Node(13, '*')
n14 = Node(14, '.')
n15 = Node(15, '.')
n16 = Node(16, '.')
n17 = Node(17, '.')
n18 = Node(18, '|')
n19 = Node(19, '.')
n20 = Node(20, '.')
n21 = Node(21, '?')

g = Graph(r)

g.add_link(r, n14)

g.add_link(n14, n2)
g.add_link(n14, n12)
g.add_link(n12, n15)
g.add_link(n15, n10)
g.add_link(n15, n2)

g.add_link(n1, n16)
g.add_link(n16, n3)
g.add_link(n16, n13)
g.add_link(n13, n17)
g.add_link(n17, n4)
g.add_link(n17, n3)

g.add_link(n2, n18)
g.add_link(n18, n5)
g.add_link(n18, n6)
g.add_link(n18, n19)
g.add_link(n18, n20)
g.add_link(n19, n7)
g.add_link(n19, n21)
g.add_link(n19, n8)
g.add_link(n21, n1)
g.add_link(n20, n9)
g.add_link(n20, n3)
g.add_link(n20, n11)

#print buscar_utiles(g)
print utiles(g)

#sacar_inutiles(g)
print "anulables: ", anulables(g)
print "primeros: ", primeros(g)
print "siguientes: ", siguientes(g)

codearGrafo(g)
