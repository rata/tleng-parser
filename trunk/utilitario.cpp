#include <iostream>
#include <string>

using namespace std;

string cadena;
char tc;
int en = 0;

void match(char letra){
	if (letra == '\\') ;
	else
	{
		if (tc != letra )
		{
			cout << "###################################################" <<endl;
			cout << "Error, Cadena inválida." <<endl;
			if (tc == '$')
				cout << "La cadena se terminó de analizar."<< endl;
			else
				cout << "Entrada: " << tc << endl;
			cout << "Esperado: " << letra << endl;
			cout << "###################################################" <<endl;			
			throw 0;
		}
		else
		{
			en++;
//			cout << "matcheo " << tc << endl;
			tc = cadena[en];
		}
	}
}

