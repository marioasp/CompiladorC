def padronizacao(tokens):
    x = 0
    y = 0
    z = 0
    modified = []

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
            elif modified[x].get('value') == '=':
                modified[x].update({'type' : 26})
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
    
    return modified