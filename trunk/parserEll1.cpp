#include <iostream>
#include <string>
#include "codigoParser.cpp"

using namespace std;

int main(int argc, char* argv[]){

	if (argc < 2) {
		cout << "Debe escribir como parametro la cadena a analizar" <<
			endl;
		return 0;
	}

	cadena = string(argv[1]) + '$';
	tc = cadena[0];

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
			cout << "Entrada: '" << tc << "'" << endl;
			cout << "Se esperaba final de cadena." <<endl;
			cout << "###################################################" <<endl;
		}
	}
	catch(int num)
	{
	}

	return 0;

}
