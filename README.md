# CompiladorC
Compilador feito em Python para a leitura de códigos em C.


## **Analisador Lexico**
Primeira etapa da compilacao que recebe o arquivo em C como entrada e retorna um arquivo de tokens.

O analizador percorre o arquivo de entrada caractere por caractere, armazenando os caracteres lidos em um buffer. Assim que o um separador ou operador e' encontrado, o buffer e' analizado para categorizar a palavra armazenada em algum tipo de token.

Os tipos de Token utilizados foram:

  **Variavel:**
  Os tokens de variaveis sao as palavras comecadas em letras ou "_" seguidas por qualquer numero de letras, numeros ou tambem "_".
  
  **Numeros:**
  Os tokens de numeros sao as palavras que contem somente numerais.
  
  **Palavras Reservadas:**
  Os tokens de palavras reservadas sao consultados em uma lista de palavras.
  
  **Separadores:**
  Os tokens de separadores sao quaisquer tipo de espaco ou quebra de linha, alem de ";" e ",".
  
  **Operadores:**
  Os tokens de operadores incluem todos os operadores matematicos e aritmeticos, alem de "()","[]","{}".
  
  **Texto:**
  Os tokens de texto sao todas as strings comecadas e terminadas em """.
  
  **Comentarios:**
  Os tokens de comentario sao todas as strings comecadas em "//" ou comecadas e terminadas em "*/" e "*/"
  
  **ERROS:**
  Os tokens de erro sao dividos em *tipo A* e *tipo B*. Sendo o tipo **A** para a identificacao de caracteres que   nao estao presentes em nenhum regex e nao podem ser identificados. E o tipo **B** para palavras que nao estao presentes em nenhum regex. 
  

## **Parser**
  **Em desenvolvimento**
  
