

from ast import mod


def analise(modified):
    
    z = 0
    declared = []
    matching = []
    instruc = []
    variablecount = 0

    while z < len(modified):

        if modified[z].get('type') == 2:
            if modified[z].get('value') == '%':
                z = z+1
                continue
            elif modified[z+1].get('type') == 3 or modified[z+1].get('type') == 4:
                if modified[z-1].get('type') == 4 or modified[z+1].get('type') == 3:
                    instruc.append({
                        'Tipo': 'Operacao',
                        'Parametro1': modified[z -1].get('value'),
                        'Parametro2': modified[z +1].get('value'),
                        'TipoOP': modified[z].get('value')
                    })
                    z= z +2
                    continue
            else:
                print(f"Erro Sintatico! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")                  
        
        if modified[z].get('type') == 20:
            matching.append(modified[z].get('type')) 

            
        
        if modified[z].get('type') == 21:
            if matching[-1] == 20:
                matching.pop  
            else:
                print(f"Erro Sintatico! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}") 
 
        
        if modified[z].get('type') == 22:
            matching.append(modified[z].get('type')) 


        
        if modified[z].get('type') == 23:
            if matching[-1] == 22:
                matching.pop                    
            else:
                print(f"Erro Sintatico! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}") 
 
        
        if modified[z].get('type') == 24:
            matching.append(modified[z].get('type')) 
            

        
        if modified[z].get('type') == 25:
            if matching[-1] == 24:
                matching.pop                    
            else:
                print(f"Erro Sintatico Sintatico! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}") 
        
        if modified[z].get('type') == 3:
            if modified[z].get('value') not in declared:
                if modified[z -1].get('type') == 600:
                    instruc.append({
                        'Tipo': 'Declaracao',
                        'Parametro1': modified[z -1].get('value'),
                        'Parametro2': modified[z].get('value')
                    })
                    declared.append(modified[z].get('value')) 
                    z = z +1
                    continue
                else:
                    print(f"Erro Sintatico Sintatico! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  
            else:
                if modified[z+1].get('type') == 26:
                    if modified[z+2].get('type') == 26:
                        instruc.append({
                            'Tipo': 'Comparacao',
                            'Parametro1': modified[z].get('value'),
                            'Parametro2': modified[z + 3].get('value')
                        })
                        z = z+4
                        continue
                    else:
                        instruc.append({
                            'Tipo': 'Atribuicao',
                            'Parametro1': modified[z].get('value'),
                            'Parametro2': modified[z + 2].get('value')
                        })
                        z = z+3
                        continue
                elif modified[z+1].get('type') == 10:
                    z = z+1
                    continue
                elif modified[z+1].get('type') == 11:
                    z = z+1
                    continue
                elif modified[z+1].get('type') == 21:
                    z = z+1
                    continue
                else:
                    print(f"Erro Sintatico Sintatico! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")   
            
        if modified[z].get('type') == 4:
            if modified[z+1].get('type') == 2:
                instruc.append({
                    'Tipo': 'Operacao',
                    'Parametro1': modified[z].get('value'),
                    'Parametro2': modified[z + 2].get('value'),
                    'TipoOP': modified[z + 1].get('value')                
                })
                z = z+3
                continue
            elif modified[z+1].get('type') == 11:
                    z = z+1
                    continue
            elif modified[z+1].get('type') == 26:
                if modified[z+2].get('type') == 26:
                    instruc.append({
                        'Tipo': 'Comparacao',
                        'Parametro1': modified[z].get('value'),
                        'Parametro2': modified[z + 3].get('value')
                    })
                    z = z+4
                    continue
            elif modified[z-1].get('type') == 2:
                instruc.append({
                    'Tipo': 'Operacao',
                    'Parametro1': modified[z -2].get('value'),
                    'Parametro2': modified[z].get('value'),
                    'TipoOP': modified[z - 1].get('value')                
                })
                z =z+1
                continue
            elif modified[z-1].get('type') == 65:
                z = z +1
                continue
                        
            else:
                print(f"Erro Sintatico! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")    
        
        if modified[z].get('type') == 5:
            if modified[z-1].get('type') == 20 or modified[z-1].get('value') == '%':

                if modified[z+1].get('type') == 21:
                    z = z +1
                    continue
            else:
                print(f"Erro Sintatico! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")    
        
        if modified[z].get('type') == 6:
            if modified[z+1].get('type') == 20:
                z = z +1
                continue
            elif modified[z+1].get('type') == 4:
                z = z +1
                continue
            else:
                print(f"Erro Sintatico! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")   
        
        if modified[z].get('type') == 60:
            if modified[z+1].get('type') == 20:
                z = z +1
                continue 
            else:
                print(f"Erro Sintatico! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  

        if modified[z].get('type') == 61:
            if modified[z+1].get('type') == 20:
                z = z +1
                continue
            else:
                print(f"Erro Sintatico! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  
        
    
        if modified[z].get('type') == 62:
            if modified[z+1].get('type') == 11:
                z = z +1
                continue
            else:
                print(f"Erro Sintatico! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  

        if modified[z].get('type') == 63:
            if modified[z+1].get('type') == 11:
                z = z +1
                continue
            else:
                print(f"Erro Sintatico! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  
        
        if modified[z].get('type') == 64:
            if modified[z+1].get('type') == 11:
                z = z +1
                continue
            else:
                print(f"Erro Sintatico! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  
        
        if modified[z].get('type') == 65:
            if modified[z+1].get('type') == 4:
                z = z +1
                continue 
            else:
                print(f"Erro Sintatico! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  
        
        if modified[z].get('type') == 66:
            if modified[z+1].get('type') == 20:
                z = z +1
                continue
            else:
                print(f"Erro Sintatico! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  
            
        if modified[z].get('type') == 67:
            if modified[z+1].get('type') == 24:
                if modified[z-1].get('type') == 25:
                    z = z +1
                    continue
            else:
                print(f"Erro Sintatico! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  
        
        if modified[z].get('type') == 68:
            if modified[z+1].get('type') == 24:
                z = z +1
                continue
            else:
                print(f"Erro Sintatico! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  
        
        if modified[z].get('type') == 600:
            if modified[z+1].get('type') == 3:
                z = z +1
                continue
            elif modified[z+1].get('type') == 6:
                z = z +1
                continue
            else:
                print(f"Erro Sintatico! Linha: {modified[z].get('line')} Coluna: {modified[z].get('column')}")  

        if modified[z].get('type') == 7:
            if modified[z+1].get('type') == 20:
                z = z +1
                continue
            else:
                print("Erro Sintatico! Linha: modified[z].get('line') Coluna: modified[z].get('column')") 
        
        if modified[z].get('type') == 70:
            if modified[z+1].get('type') == 20:
                z = z +1
                continue
            else:
                print("Erro Sintatico! Linha: modified[z].get('line') Coluna: modified[z].get('column')") 
        
        if modified[z].get('type') == 71:
            if modified[z+1].get('type') == 20:
                z = z +1
                continue
            else:
                print("Erro Sintatico! Linha: modified[z].get('line') Coluna: modified[z].get('column')") 


        
        z = z+1
    return instruc