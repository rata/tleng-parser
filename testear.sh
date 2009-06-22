#/bin/bash

echo '//////////////////////////////////////////////////////////////////////////////////////////' #;
echo 'Gramatica 0' #;
echo 'No es ll1, sd iguales' #;
python2.6 parser.py "./gramaticas/gramatica0.txt" > codigoParser.cpp #;
echo '//////////////////////////////////////////////////////////////////////////////////////////' #;
echo 'Gramatica 1' #;
echo 'No es ll1, recursion a izq' #;
python2.6 parser.py "./gramaticas/gramatica1.txt" > codigoParser.cpp #;
echo '//////////////////////////////////////////////////////////////////////////////////////////' #;
echo 'Gramatica 2' #;
python2.6 parser.py "./gramaticas/gramatica2.txt" > codigoParser.cpp #;
g++ parserEll1.cpp -o parser #;
echo 'Empieza a aceptar'
./parser "hoooola" #;
./parser "hola" #;
./parser "hoooolasss" #;
./parser "holassssss" #;
./parser "chaussssss" #;
./parser "chau" #;
echo 'Fin aceptar'
echo 'No acepta'
./parser "" #;
./parser "hlas" #;
./parser "f" #;
./parser "holsss" #;
./parser "chass" #;
./parser "haussssss" #;
./parser "cholas" #;
echo 'Fin' #;
echo '//////////////////////////////////////////////////////////////////////////////////////////' #;
echo 'Gramatica 3' #;
python2.6 parser.py "./gramaticas/gramatica3.txt" > codigoParser.cpp #;
g++ parserEll1.cpp -o parser #;
echo 'Empieza a aceptar'
./parser "u" #;
./parser "c" #;
./parser "cu" #;
./parser "cucucucuc" #;
./parser "cuuuc" #;
./parser "uuccucucuuu" #;
./parser "" #;
echo 'Fin aceptar'
echo 'Empieza a no-aceptar'
./parser "uucucuo" #;
./parser "suc" #;
./parser "as" #;
echo 'Fin' #;
echo '//////////////////////////////////////////////////////////////////////////////////////////' #;
echo 'Gramatica 4' #;
echo 'No es LL1'
python2.6 parser.py "./gramaticas/gramatica4.txt" > codigoParser.cpp #;
echo '//////////////////////////////////////////////////////////////////////////////////////////' #;
echo 'Gramatica 5' #;
python2.6 parser.py "./gramaticas/gramatica5.txt" > codigoParser.cpp #;
g++ parserEll1.cpp -o parser #;
echo 'Empieza a aceptar'
./parser "ucd" #;
./parser "uuuccdd" #;
./parser "uuuuucduuuu" #;
./parser "uuuuucdddddu" #;
./parser "ucccddduuuuuuuu" #;
./parser "ucccccddd" #;
echo 'Fin aceptar'
echo 'Empieza a no-aceptar'
./parser "u" #;
./parser "uuuuuuuuuu" #;
./parser "ucccc" #;
./parser "uc" #;
./parser "c" #;
./parser "ccccccccc" #;
./parser "uucc" #;
./parser "uuuuuc" #;
./parser "uuuuucccc" #;
./parser "uuuuucu" #;
./parser "" #;
./parser "a" #;
./parser "aaaaaaaaaa" #;
./parser "au" #;
./parser "cccccccccu" #;
./parser "ccccacccc" #;
echo 'Fin' #;
echo '//////////////////////////////////////////////////////////////////////////////////////////' #;
echo 'Gramatica 6' #;
python2.6 parser.py "./gramaticas/gramatica6.txt" > codigoParser.cpp #;
g++ parserEll1.cpp -o parser #;
echo 'Empieza a aceptar'
./parser "nfv" #;
./parser "nfdvfve" #;
./parser "dvfnefpvqfn" #;
echo 'Fin aceptar'
echo 'Empieza a no-aceptar'
./parser "nf" #;
./parser "dncve" #;
./parser "" #;
echo 'Fin' #;

