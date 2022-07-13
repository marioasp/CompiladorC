import AnalisadorLexico as analisador
import analise as parser
import padrao as padrao
import gerador as gerador
#ABRINDO O ARQUIVO

f = open("documento", "r")
content = f.read() 



tokens = analisador.lexico(content)

modified = padrao.padronizacao(tokens)

instruc = parser.analise(modified)

codigo = gerador.gerador(instruc)

