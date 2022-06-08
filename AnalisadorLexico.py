from dbm import error
from operator import index
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


def parser(tokens):
    x = 0
    y = 0
    z = 0
    modified = []
    declared = []
    matching = []
    variablecount = 0
    while x < len(tokens):
        modified.append(tokens[x])
        if modified[x].get('type') == 'SEPARADOR':
            if modified[x].get('value') == ',':
                modified[x].update({'type' : 10})
            elif modified[x].get('value') == ';':
                modified[x].update({'type' : 11})
            else:
                modified[x].update({'type' : 1})
        
        if modified[x].get('type') == 'OPERADOR':
            if modified[x].get('value') == '(':
                modified[x].update({'type' : 20})
            elif modified[x].get('value') == ')':
                modified[x].update({'type' : 21})
            elif modified[x].get('value') == '[':
                modified[x].update({'type' : 22})
            elif modified[x].get('value') == ']':
                modified[x].update({'type' : 23})
            elif modified[x].get('value') == '{':
                modified[x].update({'type' : 24})
            elif modified[x].get('value') == '}':
                modified[x].update({'type' : 25})
            else:
                modified[x].update({'type' : 2})
        
        if modified[x].get('type') == 'VARIAVEL':
            modified[x].update({'type' : 3})

                
        if modified[x].get('type') == 'NUMERAL':
            modified[x].update({'type' : 4})
        if modified[x].get('type') == 'TEXTO':
            modified[x].update({'type' : 5})
        if modified[x].get('type') == 'PALAVRA RESERVADA':
            if modified[x].get('value') == 'for':
                modified[x].update({'type' : 60})
            elif modified[x].get('value') == 'while':
                modified[x].update({'type' : 61})
            elif modified[x].get('value') == 'break':
                modified[x].update({'type' : 62})
            elif modified[x].get('value') == 'continue':
                modified[x].update({'type' : 63})
            elif modified[x].get('value') == 'switch':
                modified[x].update({'type' : 64})
            elif modified[x].get('value') == 'case':
                modified[x].update({'type' : 65})
            elif modified[x].get('value') == 'if':
                modified[x].update({'type' : 66})
            elif modified[x].get('value') == 'else':
                modified[x].update({'type' : 67})
            elif modified[x].get('value') == 'do':
                modified[x].update({'type' : 68})
            elif modified[x].get('value') == 'int':
                modified[x].update({'type' : 600})
            elif modified[x].get('value') == 'char':
                modified[x].update({'type' : 600})
            elif modified[x].get('value') == 'float':
                modified[x].update({'type' : 600})
            elif modified[x].get('value') == 'double':
                modified[x].update({'type' : 600})
            elif modified[x].get('value') == 'long':
                modified[x].update({'type' : 600})
            elif modified[x].get('value') == 'short':
                modified[x].update({'type' : 600})
            else:
                modified[x].update({'type' : 6})
        
        if modified[x].get('type') == 'PALAVRA RESERVADA STDIO.H':
            if modified[x].get('value') == 'printf':
                modified[x].update({'type' : 70})
            elif modified[x].get('value') == 'scanf':
                modified[x].update({'type' : 71})
            else:
                modified[x].update({'type' : 7})
        
        if modified[x].get('type') == 'COMENTARIO TIPO A - UMA LINHA':
            modified[x].update({'type' : 8})
        
        if modified[x].get('type') == 'COMENTARIO TIPO B - N LINHAS':
            modified[x].update({'type' : 9})
        
        if modified[x].get('type') == 'ERRO TIPO A - QUE CARACTERE E ESSE?':
            modified[x].update({'type' : 98})
        
        if modified[x].get('type') == 'ERRO TIPO B - ISSO NAO FAZ SENTIDO':
            modified[x].update({'type' : 99})

        x = x+1


    

    while y < len(modified):
        if modified[y].get('type') == 1:
            del modified[y]
            y = 0
        y = y+1
        
    
    while z < len(modified):

        if modified[z].get('type') == 2:
            if modified[z].get('value') == '%':
                print('ok')
            elif modified[z+1].get('type') == 3:
                if modified[z-1].get('type') == 4:
                    print('ok')
                if modified[z-1].get('type') == 3:
                    print('ok')  
            elif modified[z+1].get('type') == 4:
                if modified[z-1].get('type') == 4:
                    print('ok')
                if modified[z-1].get('type') == 3:
                    print('ok')  
            else:
                print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")                  
        
        if modified[z].get('type') == 20:
            if modified[z+1].get('type') == 3:
                print('ok')
            elif modified[z+1].get('type') == 4:
                print('ok')  
            elif modified[z+1].get('type') == 600:
                print('ok') 
            elif modified[z+1].get('type') == 20:
                print('ok')  
            else:
                print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}") 
            matching.append(modified[z].get('value'))             
        
        if modified[z].get('type') == 21:
            if matching[z-1] == 20:
                if modified[z+1].get('type') == 11:
                    print('ok')
                elif modified[z+1].get('type') == 24:
                    print('ok')  
                elif modified[z+1].get('type') == 2:
                    print('ok')
                elif modified[z+1].get('type') == 21:
                    print('ok')  
                elif modified[z+1].get('type') == 22:
                    print('ok')
                elif modified[z+1].get('type') == 23:
                    print('ok')  
                elif modified[z+1].get('type') == 25:
                    print('ok')     
            else:
                print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}") 
 
        
        if modified[z].get('type') == 22:
            if modified[z+1].get('type') == 3:
                print('ok')
            elif modified[z+1].get('type') == 4:
                print('ok')  
            elif modified[z+1].get('type') == 600:
                print('ok')
            elif modified[z+1].get('type') == 20:
                print('ok')   
            elif modified[z+1].get('type') == 22:
                print('ok')    
            else:
                print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}") 
            matching.append(modified[z].get('value')) 
        
        if modified[z].get('type') == 23:
            if matching[z-1] == 22:
                if modified[z+1].get('type') == 11:
                    print('ok')
                elif modified[z+1].get('type') == 24:
                    print('ok')  
                elif modified[z+1].get('type') == 2:
                    print('ok')
                elif modified[z+1].get('type') == 22:
                    print('ok')
                elif modified[z+1].get('type') == 25:
                    print('ok')
                elif modified[z+1].get('type') == 20:
                    print('ok') 
                elif modified[z+1].get('type') == 23:
                    print('ok') 
            else:
                print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}") 
 
        
        if modified[z].get('type') == 24:
            if modified[z+1].get('type') == 3:
                print('ok')
            elif modified[z+1].get('type') == 4:
                print('ok')  
            elif modified[z+1].get('type') == 600:
                print('ok')
            elif modified[z+1].get('type') == 20:
                print('ok')
            elif modified[z+1].get('type') == 22:
                print('ok')
            elif modified[z+1].get('type') == 24:
                print('ok')       
            else:
                print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}") 
            matching.append(modified[z].get('value')) 
        
        if modified[z].get('type') == 25:
            if matching[z-1] == 24:
                if modified[z+1].get('type') == 11:
                    print('ok')
                elif modified[z+1].get('type') == 24:
                    print('ok')  
                elif modified[z+1].get('type') == 2:
                    print('ok')
                elif modified[z+1].get('type') == 22:
                    print('ok')
                elif modified[z+1].get('type') == 25:
                    print('ok')
                elif modified[z+1].get('type') == 20:
                    print('ok')
            else:
                print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}") 
        
        if modified[z].get('type') == 3:
            if modified[z].get('value') not in declared:
                if modified[z -1].get('type') == 600:
                    print('ok')
                    declared.append(modified[z].get('value')) 
                else:
                    print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  
            else:
                if modified[z+1].get('type') == 2:
                    print('ok')  
                elif modified[z+1].get('type') == 10:
                    print('ok')
                elif modified[z+1].get('type') == 11:
                    print('ok')
                elif modified[z+1].get('type') == 21:
                    print('ok')    
                else:
                    print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")   
            
        if modified[z].get('type') == 4:
            if modified[z+1].get('type') == 2:
                    print('ok')
            elif modified[z+1].get('type') == 11:
                    print('ok')  
            elif modified[z-1].get('type') == 2:
                    print('ok')  
            elif modified[z-1].get('type') == 65:
                    print('ok')  
                        
            else:
                print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")    
        
        if modified[z].get('type') == 5:
            if modified[z-1].get('type') == 20 or modified[z-1].get('value') == '%':

                if modified[z+1].get('type') == 21:
                    print('ok')  
            else:
                print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")    
        
        if modified[z].get('type') == 6:
            if modified[z+1].get('type') == 20:
                print('ok')
            elif modified[z+1].get('type') == 4:
                print('ok')
            else:
                print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")   
        
        if modified[z].get('type') == 60:
            if modified[z+1].get('type') == 20:
                print('ok')  
            else:
                print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  

        if modified[z].get('type') == 61:
            if modified[z+1].get('type') == 20:
                print('ok')  
            else:
                print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  
        
    
        if modified[z].get('type') == 62:
            if modified[z+1].get('type') == 11:
                print('ok')  
            else:
                print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  

        if modified[z].get('type') == 63:
            if modified[z+1].get('type') == 11:
                print('ok')  
            else:
                print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  
        
        if modified[z].get('type') == 64:
            if modified[z+1].get('type') == 11:
                print('ok')  
            else:
                print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  
        
        if modified[z].get('type') == 65:
            if modified[z+1].get('type') == 4:
                print('ok')  
            else:
                print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  
        
        if modified[z].get('type') == 66:
            if modified[z+1].get('type') == 20:
                print('ok')  
            else:
                print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  
            
        if modified[z].get('type') == 67:
            if modified[z+1].get('type') == 24:
                if modified[z-1].get('type') == 25:
                    print('ok')  
            else:
                print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  
        
        if modified[z].get('type') == 68:
            if modified[z+1].get('type') == 24:
                print('ok')  
            else:
                print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  
        
        if modified[z].get('type') == 600:
            if modified[z+1].get('type') == 3:
                    print('ok')
            elif modified[z+1].get('type') == 6:
                    print('ok')
            else:
                print(f"Erro! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  

        if modified[z].get('type') == 7:
            if modified[z+1].get('type') == 20:
                    print('ok')  
            else:
                print("Erro! Linha: modified[z].get('line') Coluna: modified[z].get('column')") 
        
        if modified[z].get('type') == 70:
            if modified[z+1].get('type') == 20:
                    print('ok')  
            else:
                print("Erro! Linha: modified[z].get('line') Coluna: modified[z].get('column')") 
        
        if modified[z].get('type') == 71:
            if modified[z+1].get('type') == 20:
                    print('ok')  
            else:
                print("Erro! Linha: modified[z].get('line') Coluna: modified[z].get('column')") 


        
        z = z+1
        
        

  

parser(tokens)
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
