from dbm import error
from operator import index
import re
import parser as parser



def lexico(content):
    current = 0 
    tokens = []
    storew = ''
    tag = 0
    tag2 = 0
    tagoperador = 0

    

    #REGEX PARA CADA UM DOS TIPOS DE TOKEN
    variaveis = re.compile(r"^[a-zA-Z_]\w*$")
    texto = re.compile(r"\".+\"")
    separadores = re.compile(r"[\s|;|,]$")
    comentarios = re.compile(r"\#.+\#")
    numero = re.compile(r"[0-9]+$")
    reservadas = ["asm", "auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else", "enum", "extern", "float", "for", "goto", "if", "int", "long" ,"main", "register", "return", "short", "signed", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"] 
    reservadas_stioh = ["clearerr", "clrmemf", "fclose", "fdelrec", "feof", "ferror", "fflush", "fgetc", "fgetc", "fgetpos", "fgets", "fldata", "flocate", "fopen", "fprintf", "fputc", "fputs", "fread", "freopen", "fscanf", "fseek", "fseeko", "fsetpos", "ftell", "ftello", "fupdate", "fwrite", "getc", "getchar", "gets", "perror", "printf", "putc", "putchar", "puts", "remove", "rename", "rewind", "scanf", "setbuf", "setvbuf", "sprintf", "sscanf", "svc99", "tmpfile", "tmpnam", "ungetc", "vfprintf", "vprintf", "vsprintf"]
    operador = re.compile(r"\+|\-|\*|\/|\%|\||\&|\>|\<|\=|!|{|}|\(|\)|\[|\]$")
    nochar = re.compile(r"\w*\W+\w*")
    erro = re.compile(r".")
    line = 1
    column = 0
    count = 0
    count2 = 1
    count3 = 1

    #ITERANDO PELO ARQUIVO
    while current < len(content):
        char = content[current] 


        #TAG QUE INDICA O ENCONTRO DE UM SEPARADOR OU OPERADOR
        while tag == 0:

            char = content[current]
            column = column +1
            #CASO ESPECIFICO PARA STRINGS
            if char == '"':
                count4 = 1
                storew += char
                current = current +1
            
                char = content[current]
                while (char != '"'):
                    if char == '%':
                        tokens.append({
                        'type': 'OPERADOR',
                        'value': char,
                        'line': line,
                        'column': column + count4 
                        })
                        current = current +1
                        count4 = count4 +1
                        char = content[current]
                    count4 = count4 +1
                    storew += char
                    current = current +1
                    char = content[current]

                storew += char
                value = ''
                tokens.append({
                    'type': 'TEXTO',
                    'value': storew,
                    'line': line,
                    'column': column
                })
                storew = ''
                column = column + count4
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
                    count3 = count3 +1
                
                value = ''
                tokens.append({
                    'type': 'COMENTARIO TIPO A - UMA LINHA',
                    'value': storew,
                    'line': line,
                    'column': column 
                })
                column = column + count3
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
                    if char == '\n':
                        count = count +1
                        count2 = 1
                    storew += char
                    current = current +1
                    char = content[current]
                    count2 = count2 +1

                storew += char
                current = current +1
            
                char = content[current]
                storew += char
                current = current +1
            
                char = content[current]
                value = ''
                tokens.append({
                    'type': 'COMENTARIO TIPO B - N LINHAS',
                    'value': storew,
                    'line': line,
                    'column': column 
                })
                storew = ''
                line = line + count
                column = column + (count2 -2)
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
                tagoperador = 0
                current = current + 1                         
                continue
            
            storew += char
            current = current + 1
        
        
        #VERUFICACAO SE A PALAVRA ESTA NA LISTA DE RESERVADAS
        if storew in reservadas:
            value = ''
            tokens.append({
                'type': 'PALAVRA RESERVADA',
                'value': storew,
                'line': line,
                'column': column -1
            })
            if tagoperador == 0:
                value = ''
                tokens.append({
                    'type': 'SEPARADOR',
                    'value': char,
                    'line': line,
                    'column': column 
                })
                if char == '\n':
                    line = line +1
                    column = 1
                tag = 0
                storew = ''
                continue
            if tagoperador == 1:
                value = ''
                tokens.append({
                    'type': 'OPERADOR',
                    'value': char,
                    'line': line,
                    'column': column 
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
                'value': storew,
                'line': line,
                'column': column -1
            })
            if tagoperador == 0:
                value = ''
                tokens.append({
                    'type': 'SEPARADOR',
                    'value': char,
                    'line': line,
                    'column': column 
                })
                if char == '\n':
                    line = line +1
                    column = 1
                tag = 0
                storew = ''
                continue
            if tagoperador == 1:
                value = ''
                tokens.append({
                    'type': 'OPERADOR',
                    'value': char,
                    'line': line,
                    'column': column 
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
                'value': storew,
                'line': line,
                'column': column -1
            })
            if tagoperador == 0:
                value = ''
                tokens.append({
                    'type': 'SEPARADOR',
                    'value': char,
                    'line': line,
                    'column': column
                })
                if char == '\n':
                    line = line +1
                    column = 1
                tag = 0
                storew = ''
                continue
            if tagoperador == 1:
                value = ''
                tokens.append({
                    'type': 'OPERADOR',
                    'value': char,
                    'line': line,
                    'column': column 
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
                'value': storew,
                'line': line,
                'column': column -1
            })
            if tagoperador == 0:
                value = ''
                tokens.append({
                    'type': 'SEPARADOR',
                    'value': char,
                    'line': line,
                    'column': column           
                })
                if char == '\n':
                    line = line +1
                    column = 1
                tag = 0
                storew = ''
                continue
            if tagoperador == 1:
                value = ''
                tokens.append({
                    'type': 'OPERADOR',
                    'value': char,
                    'line': line,
                    'column': column 
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
                'value': storew,
                'line': line,
                'column': column -1        
            })
            if tagoperador == 0:
                value = ''
                tokens.append({
                    'type': 'SEPARADOR',
                    'value': char,
                    'line': line,
                    'column': column
                })
                if char == '\n':
                    line = line +1
                    column = 1
                tag = 0
                storew = ''
                continue
            if tagoperador == 1:
                value = ''
                tokens.append({
                    'type': 'OPERADOR',
                    'value': char,
                    'line': line,
                    'column': column 
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
                'value': storew,
                'line': line,
                'column': column -1
            })
            if tagoperador == 0:
                value = ''
                tokens.append({
                    'type': 'SEPARADOR',
                    'value': char,
                    'line': line,
                    'column': column 
                })
                if char == '\n':
                    line = line +1
                    column = 1
                tag = 0
                storew = ''
                continue
            if tagoperador == 1:
                value = ''
                tokens.append({
                    'type': 'OPERADOR',
                    'value': char,
                    'line': line,
                    'column': column 
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
                'value': char,
                'line': line,
                'column': column 
            })
            tag = 0
            continue
            

        #TRATANDO O CASO ESPECIFICO DE DOIS SEPARADORES CONSECUTIVOS
        if re.match(separadores, char):
            value = ''
            tokens.append({
                'type': 'SEPARADOR',
                'value': char,
                'line': line,
                'column': column 
            })  
            if char == '\n':
                line = line +1
                column = 0
            tag = 0
            continue

    return tokens



  


    # if tag == 1:
    #     value = ''
    #     tokens.append({
    #         'type': 'ERRO TIPO B - ISSO NAO FAZ SENTIDO',
    #         'value': storew
    #     })
    #     storew = ''
    #     tag = 0


    #FORMATACAO E ESCRITA NO ARQUIVO DE SAIDA
# output = open('/home/mario/pycomp/output','w')
# for element in tokens:

#     output.write("{}\n".format(element))

# output.close()


 
# def parser(tokens):
#     global current
#     current = 0
#     token= []
#     if tokens.get('type') == ''
#     token[current]  
