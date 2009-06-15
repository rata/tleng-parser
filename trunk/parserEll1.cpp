#include <iostream>
#include <string>
#include "codigoParser.cpp"

using namespace std;

int main(){
	cout << "Ingrese una cadena a analizar:\n";
	cin >> cadena;
	cadena = cadena + '$';
//	cout << cadena << endl;
	tc = cadena[0];
//	cout << tc<< endl;

	do{
		try
		{
			parsear();
			if (tc == '$')
			{
				cout << "Cadena válida reconocida exitosamente" << endl;
				cout << "---------------------------------------------------" << endl;
			}
			else
			{
				cout << "###################################################" <<endl;
				cout << "Error, Cadena inválida." <<endl;
				cout << "Entrada: " << tc << endl;
				cout << "Se esperaba final de cadena." <<endl;
				cout << "###################################################" <<endl;
			}
		}
		catch(int num)
		{
		}
	cout << "Ingrese una cadena a analizar o 0 para terminar:\n";
	en = 0;
	cin >> cadena;
	cadena = cadena + '$';
//	cout << cadena << endl;
	tc = cadena[0];
//	cout << tc<< endl;
	}while(tc != '0');

	return 0;

}
