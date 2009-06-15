#include <iostream>
#include <string>
#include "utilitario.cpp"

using namespace std;

void Proc_S();
void Proc_A();
void Proc_B();
void Proc_C();
void parsear();

void parsear(){
Proc_S();
}

void Proc_S(){
if( tc=='a' ||false){
Proc_A();
}
else if( tc=='b' ||false){
Proc_B();
}
else if( tc=='c' ||false){
Proc_C();
}
else{
cout << "###################################################" <<endl;
cout << "Error, cadena invalida" << endl << "Entrada: " << tc << endl;
cout << "Esperando: ['a', 'b', 'c'] "<< endl;
cout << "###################################################" <<endl;
throw 0;
}
}

void Proc_A(){
match('a');
}

void Proc_B(){
match('b');
}

void Proc_C(){
match('c');
}

