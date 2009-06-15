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
			cout << "No es posible matchear " << tc << "con " << letra << endl;
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

