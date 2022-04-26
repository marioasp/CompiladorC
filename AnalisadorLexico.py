from dbm import error
import re

from soupsieve import match

current = 0 
tokens = []
storew = ''
tag = 0
tag2 = 0
tagoperador = 0

#ABRINDO O ARQUIVO

f = open("/home/mario/pycomp/documento", "r")
content = f.read()    

#REGEX PARA CADA UM DOS TIPOS DE TOKEN
variaveis = re.compile(r"^[a-zA-Z_]\w*$")
texto = re.compile(r"\".+\"")
separadores = re.compile(r"[\s|;|,]$")
comentarios = re.compile(r"\#.+\#")
numero = re.compile(r"[0-9]+$")
reservadas = ["asm", "auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else", "enum", "extern", "float", "for", "goto", "if", "int", "long" ,"register", "return", "short", "signed", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"] 
reservadas_stioh = ["clearerr", "clrmemf", "fclose", "fdelrec", "feof", "ferror", "fflush", "fgetc", "fgetc", "fgetpos", "fgets", "fldata", "flocate", "fopen", "fprintf", "fputc", "fputs", "fread", "freopen", "fscanf", "fseek", "fseeko", "fsetpos", "ftell", "ftello", "fupdate", "fwrite", "getc", "getchar", "gets", "perror", "printf", "putc", "putchar", "puts", "remove", "rename", "rewind", "scanf", "setbuf", "setvbuf", "sprintf", "sscanf", "svc99", "tmpfile", "tmpnam", "ungetc", "vfprintf", "vprintf", "vsprintf"]
operador = re.compile(r"\+|\-|\*|\/|\%|\||\&|\>|\<|\=|!|{|}|\(|\)|\[|\]$")
nochar = re.compile(r"\w*\W+\w*")
erro = re.compile(r".")


#ITERANDO PELO ARQUIVO
while current < len(content):
    char = content[current] 
    #TAG QUE INDICA O ENCONTRO DE UM SEPARADOR OU OPERADOR
    while tag == 0:

        char = content[current]
        
        #CASO ESPECIFICO PARA STRINGS
        if char == '"':
            storew += char
            current = current +1
            char = content[current]
            while not (char == '"'):
                if char == '%':
                    tokens.append({
                    'type': 'OPERADOR',
                    'value': char
                    })
                    current = current +1
                    char = content[current]

                storew += char
                current = current +1
                char = content[current]
            storew += char
            value = ''
            tokens.append({
                'type': 'TEXTO',
                'value': storew
            })
            storew = ''
            current = current +1 
            continue
        
        #CASO ESPECIFICO PARA COMENTARIOS DE UMA LINHA
        if char == '/' and (content[current + 1] == '/'):
            storew += char
            current = current +1
            char = content[current]
            storew += char
            current = current +1
            char = content[current]
            while not (char == '\n'):
                storew += char
                current = current +1
                char = content[current]
            value = ''
            tokens.append({
                'type': 'COMENTARIO TIPO A - UMA LINHA',
                'value': storew
            })
            storew = ''
            continue
        
        #CASO ESPECIFICO PARA COMENTARIOS DE MAIS UMA LINHA
        if char == '/' and (content[current + 1] == '*'):
            storew += char
            current = current +1
            char = content[current]
            storew += char
            current = current +1
            char = content[current]
            while not (char == '*') and not (content[current + 1] == '/'):
                storew += char
                current = current +1
                char = content[current]
            storew += char
            current = current +1
            char = content[current]
            storew += char
            current = current +1
            char = content[current]
            value = ''
            tokens.append({
                'type': 'COMENTARIO TIPO B - N LINHAS',
                'value': storew
            })
            storew = ''
            continue        
        

        #MODIFICANDO A TAG QUANDO ENCONTRA OPERADOR
        if re.match(operador, char):
            tag = 1
            tagoperador= 1
            current = current +1
            continue
        
        #MODIFICANDO A TAG QUANDO ENCONTRA SEPARADOR
        if re.match(separadores, char):
            tag = 1
            current = current + 1            
            continue
        
        storew += char
        current = current + 1

    #VERUFICACAO SE A PALAVRA ESTA NA LISTA DE RESERVADAS
    if storew in reservadas:
        value = ''
        tokens.append({
            'type': 'PALAVRA RESERVADA',
            'value': storew
        })
        if tagoperador == 0:
            value = ''
            tokens.append({
                'type': 'SEPARADOR',
                'value': char
            })
            tag = 0
            storew = ''
            continue
        if tagoperador == 1:
            value = ''
            tokens.append({
                'type': 'OPERADOR',
                'value': char
            })
            tag = 0
            tagoperador = 0
            storew = ''
            continue
    
    
    #VERUFICACAO SE A PALAVRA ESTA NA LISTA DE RESERVADAS DO STDIO
    if storew in reservadas_stioh:
        value = ''
        tokens.append({
            'type': 'PALAVRA RESERVADA STDIO.H',
            'value': storew
        })
        if tagoperador == 0:
            value = ''
            tokens.append({
                'type': 'SEPARADOR',
                'value': char
            })
            tag = 0
            storew = ''
            continue
        if tagoperador == 1:
            value = ''
            tokens.append({
                'type': 'OPERADOR',
                'value': char
            })
            tag = 0
            tagoperador = 0
            storew = ''
            continue

    #TESTE DE MATCH COM NUMERAIS
    if re.match(numero, storew):
        value = ''
        tokens.append({
            'type': 'NUMERAL',
            'value': storew
        })
        if tagoperador == 0:
            value = ''
            tokens.append({
                'type': 'SEPARADOR',
                'value': char
            })
            tag = 0
            storew = ''
            continue
        if tagoperador == 1:
            value = ''
            tokens.append({
                'type': 'OPERADOR',
                'value': char
            })
            tag = 0
            tagoperador = 0
            storew = ''
            continue
    
    #TESTE DE MATCH COM VARIAVEIS
    if re.match(variaveis, storew):
        value = ''
        tokens.append({
            'type': 'VARIAVEL',
            'value': storew
        })
        if tagoperador == 0:
            value = ''
            tokens.append({
                'type': 'SEPARADOR',
                'value': char
            })
            tag = 0
            storew = ''
            continue
        if tagoperador == 1:
            value = ''
            tokens.append({
                'type': 'OPERADOR',
                'value': char
            })
            tag = 0
            tagoperador = 0
            storew = ''
            continue

    #TESTE DE MATCH COM CARACTERES QUE NAO ESTAO PRESENTES EM NENHUM REGEX
    if re.match(nochar, storew):
        value = ''
        tokens.append({
            'type': 'ERRO TIPO A - QUE CARACTERE E ESSE?',
            'value': storew
        })
        if tagoperador == 0:
            value = ''
            tokens.append({
                'type': 'SEPARADOR',
                'value': char
            })
            tag = 0
            storew = ''
            continue
        if tagoperador == 1:
            value = ''
            tokens.append({
                'type': 'OPERADOR',
                'value': char
            })
            tag = 0
            tagoperador = 0
            storew = ''
            continue
    #TESTE DE ERRO DE PALAVRAS QUE NAO ESTAO PRESENTES EM NENHUM REGEX    
    if re.match(erro, storew):
        value = ''
        tokens.append({
            'type': 'ERRO TIPO B - ISSO NAO FAZ SENTIDO',
            'value': storew
        })
        if tagoperador == 0:
            value = ''
            tokens.append({
                'type': 'SEPARADOR',
                'value': char
            })
            tag = 0
            storew = ''
            continue
        if tagoperador == 1:
            value = ''
            tokens.append({
                'type': 'OPERADOR',
                'value': char
            })
            tag = 0
            tagoperador = 0
            storew = ''
            continue
    
    #TRATANDO O CASO ESPECIFICO DE DOIS OPERADORES CONSECUTIVOS
    if re.match(operador, char):
        value = ''
        tokens.append({
            'type': 'OPERADOR',
            'value': char
        })
        tag = 0
        continue
        

    #TRATANDO O CASO ESPECIFICO DE DOIS SEPARADORES CONSECUTIVOS
    if re.match(separadores, char):
        value = ''
        tokens.append({
            'type': 'SEPARADOR',
            'value': char
        })  
        tag = 0
        continue
                


    # if tag == 1:
    #     value = ''
    #     tokens.append({
    #         'type': 'ERRO TIPO B - ISSO NAO FAZ SENTIDO',
    #         'value': storew
    #     })
    #     storew = ''
    #     tag = 0



print(tokens)

    #FORMATACAO E ESCRITA NO ARQUIVO DE SAIDA
output = open('/home/mario/pycomp/output','w')
for element in tokens:

    output.write("{}\n".format(element))

output.close()