from time import sleep

def menu():
    menu = '''
============ MENU ============
(1)Cadastrar Usuário
(2)Criar Conta
(3)Depositar
(4)Saque
(5)Listar Contas
(6)Extrato
(7)Sair
Escolha: '''
    return int(input(menu))

def filtrar_usuarios(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf] 
    return usuarios_filtrados[0] if usuarios_filtrados else None

def exibir_extrato(saldo, /, *, extrato):
    print("\n\033[34m================ EXTRATO ================")
    print("\033[31mNão foi feito nenhuma movimentação.\033[m" if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================\033[m")

def criar_usuario(usuarios):
    cpf = input('Informe o CPF(somente números): ')
    usuario = filtrar_usuarios(cpf, usuarios)

    if usuario:
        print('\033[31mEste CPF já está cadastrado!\033[m')
        return
    
    nome = str(input('Insira o seu Nome Completo: ')).strip()
    data_de_nascimento = str(input('Insira sua Data de Nascimento(dd-mm-aaaa): ')).strip()
    endereco = str(input('Insira seu endereço(logradouro - nº - bairro - cidade/sigla estado): ')).strip()

    usuarios.append({"nome": nome, "data_de_nascimento": data_de_nascimento, "endereco": endereco, "cpf": cpf})

    print('\033[32mUsuário Criado com Sucesso!\033[m')

def criar_conta(agencia, numero_conta, usuarios):
    cpf = str(input('Informe o número do CPF(somente números): ')).strip()
    usuario = filtrar_usuarios(cpf, usuarios)

    if usuario:
        print('\033[32mConta Criada com Sucesso!\033[m')
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print('\033[31mUsuário não encontrado, sessão finalizada!\033[m')

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n\033[32m=== Depósito realizado com sucesso! ===\033[m")
    else:
        print("\033[31mOperação Falhou! Valor Inválido!\033[m")

    return saldo, extrato

def sacar(*,saldo, valor, extrato, limite, numero_saques, limite_saques,):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print('\033[31mVocê não possui o valor suficiente para o saque!\033[m')
    elif excedeu_limite:
        print('\033[31mVocê excedeu o limite de valor!\033[m')
    elif excedeu_saques:
        print('\033[31mVocê excedeu o limite diário! Volte amanhã!\033[m')
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\033[32mSaque Realizado com Sucesso!\033[m")
        
    else:
        print("\n\033[31mOperação falhou! O valor informado é inválido.\033[m")

    return saldo, extrato

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
        Agência:\t{conta['agencia']}
        C/C:\t\t{conta['numero_conta']}
        Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 30)
        print(linha)

def main():
    AGENCIA = "0001"
    LIMITE_SAQUES = 3

    limite = 500
    usuarios = []
    contas = []
    saldo = 2500
    numero_saques = 0
    extrato = ""

    while True:
        opção = menu()

        if opção == 1:
            criar_usuario(usuarios)
        elif opção == 2:
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
        
        elif opção == 3:
            valor = float(input("Informe o valor do depósito: R$"))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opção == 4:
            valor = float(input('Digite o valor do saque: R$'))

            saldo, extrato = sacar(
                saldo=saldo,
                extrato= extrato,
                numero_saques=numero_saques,
                valor=valor,
                limite=limite,
                limite_saques=LIMITE_SAQUES,
                )
        elif opção == 5:
            listar_contas(contas)
        
        elif opção == 6:
            exibir_extrato(saldo, extrato=extrato)

        elif opção == 7:
            break

        else:
            print("\033[31mOpção inválida, por favor tente novamente.\033[m")
            
            

        

main()