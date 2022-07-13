def operacao(param, param2, tipo):
    if tipo == '+':
        print(f"add s0, {param}, {param2}")
    if tipo == '-':
        print(f"sub s1, {param}, {param2}")
    if tipo == '*':
        print(f"mul s2, {param}, {param2}")
    if tipo == '/':
        print(f"div s3, {param}, {param2}")
    if tipo == '>':
        print(f"bgt s4, {param}, {param2}, 100")
    if tipo == '<':
        print(f"blt s5, {param}, {param2}, 100")

def comparacao(param, param2):
    print(f"beq s6, {param}, {param2}, 100")

def atribuicao(param, param2):
    print(f"lw s7, {param}, {param2}")    

def declaracao(param, param2):
    if param == 'int':
        print(f".{param2}:   .word 20")
    if param == 'char':  
        print(f".{param2}:   .word 30")   
    if param == 'float':
        print(f".{param2}:   .word 40")       

def gerador(instruc):
    cont = 0
    while cont< len(instruc):
        if instruc[cont].get('Tipo') == 'Operacao':
            operacao(instruc[cont].get('Parametro1'),instruc[cont].get('Parametro2'),instruc[cont].get('TipoOP'))
        if instruc[cont].get('Tipo') == 'Comparacao':
            comparacao(instruc[cont].get('Parametro1'),instruc[cont].get('Parametro2'))
        if instruc[cont].get('Tipo') == 'Atribuicao':
            atribuicao(instruc[cont].get('Parametro1'),instruc[cont].get('Parametro2'))
        if instruc[cont].get('Tipo') == 'Declaracao':
            declaracao(instruc[cont].get('Parametro1'),instruc[cont].get('Parametro2'))
        cont = cont +1