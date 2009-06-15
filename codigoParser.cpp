set([<Node char: T>, <Node char: A>, <Node char: c>, <Node char: n>, <Node char: v>, <Node char: p>, <Node char: q>, <Node char: d>, <Node char: f>, <Node char: e>, <Node char: *>, <Node char: *>, <Node char: .>, <Node char: .>, <Node char: |>, <Node char: .>, <Node char: ?>])
anulables:  {<Node char: T>: False, <Node char: L>: False, <Node char: A>: False, <Node char: T>: False, <Node char: c>: False, <Node char: n>: False, <Node char: v>: False, <Node char: p>: False, <Node char: q>: False, <Node char: d>: False, <Node char: f>: False, <Node char: e>: False, <Node char: *>: True, <Node char: *>: True, <Node char: .>: False, <Node char: .>: False, <Node char: .>: False, <Node char: .>: False, <Node char: |>: False, <Node char: .>: False, <Node char: .>: False, <Node char: ?>: True}
primeros:  {<Node char: T>: set(['p', 'n', 'd', 'v']), <Node char: L>: set([]), <Node char: A>: set(['p', 'n', 'd', 'v']), <Node char: T>: set([]), <Node char: c>: set(['c']), <Node char: n>: set(['n']), <Node char: v>: set(['v']), <Node char: p>: set(['p']), <Node char: q>: set(['q']), <Node char: d>: set(['d']), <Node char: f>: set(['f']), <Node char: e>: set(['e']), <Node char: *>: set(['f']), <Node char: *>: set(['c']), <Node char: .>: set(['p', 'v', 'd', 'n']), <Node char: .>: set(['f']), <Node char: .>: set([]), <Node char: .>: set(['c']), <Node char: |>: set(['p', 'v', 'd', 'n']), <Node char: .>: set(['p']), <Node char: .>: set(['d']), <Node char: ?>: set([])}
siguientes:  {<Node char: T>: set(['$']), <Node char: L>: set(['q']), <Node char: A>: set(['$', 'f']), <Node char: T>: set(['q', 'c', 'e']), <Node char: c>: set([]), <Node char: n>: set(['$', 'f']), <Node char: v>: set(['$', 'f']), <Node char: p>: set(['q']), <Node char: q>: set(['$', 'f']), <Node char: d>: set([]), <Node char: f>: set(['p', 'v', 'd', 'n']), <Node char: e>: set(['$', 'f']), <Node char: *>: set(['$']), <Node char: *>: set(['q']), <Node char: .>: set(['$']), <Node char: .>: set(['$']), <Node char: .>: set(['q']), <Node char: .>: set(['q']), <Node char: |>: set(['$', 'f']), <Node char: .>: set(['$', 'f']), <Node char: .>: set(['$', 'f']), <Node char: ?>: set(['q'])}
#include <iostream>
#include <string>
#include "utilitario.cpp"

using namespace std;

void Proc_T();
void Proc_A();
void parsear();

void parsear(){
Proc_T();
}

void Proc_T(){
Proc_A();
while( tc=='f' ||false){
match('f');
Proc_A();
}
}

void Proc_A(){
if( tc=='n' ||false){
match('n');
}
else if( tc=='v' ||false){
match('v');
}
else if( tc=='p' ||false){
match('p');
match('\\');
match('q');
}
else{
cout << "###################################################" <<endl;
cout << "ERROR: Cadena invalida" << endl << "Entrada: " << tc << endl;
cout << "Esperando: ['n', 'v', 'p'] "<< endl;
cout << "###################################################" <<endl;
throw 0;
}
}

