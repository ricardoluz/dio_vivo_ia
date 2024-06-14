"""Sistema Bancário"""
import os

def limpar_tela():
    '''Limpar a tela'''
    os.system('cls' if os.name == 'nt' else 'clear')


def f_deposito(valor, saldo, extrato, /):
    """Operação de depósito"""
    saldo += valor
    extrato += f"Depósito: R$ {valor:.2f}\n"

    print(f"\nDepósito de R$ {valor:.2f} efetuado.")

    return saldo, extrato


def f_saque(*, valor, saldo, extrato, limite, numero_saques, limite_saques):
    """Operação de saque"""

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print(f"Operação falhou! O valor do saque excede o limite de R$ {limite:.2f}")

    elif excedeu_saques:
        print(
            f"Operação falhou! Número máximo de saques excedido, limite máximo = {limite_saques}"
        )

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques


def f_extrato(saldo: float, /, *, extrato: str):
    """Apresentar o extrato"""

    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


def f_localizar_usuario(*, cpf: str, usuarios: list):
    """Verificar a existência de CPF"""
    usuario_localizado = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuario_localizado[0] if usuario_localizado else None


def f_criar_cliente(*, usuarios: list):
    """Criação de Cliente"""
    print("\n---Criação de Cliente ---")

    cpf = "".join([x for x in input("Digite o CPF do novo Cliente: ") if x.isdigit()])

    if f_localizar_usuario(cpf=cpf, usuarios=usuarios):
        print(f"\nCliente já cadastrado com este CPF. {cpf}\n")
    else:
        nome = input("\nDigite o nome: ")
        data_nascimento = input("\nDigite a data de nascimento (dd/mm/aaaa): ")

        print("\nDigite os dados do endereço\n", "." * 40)
        endereco_tmp = []
        endereco_tmp.append(input("Logradouro: "))
        endereco_tmp.append(input("Número: "))
        endereco_tmp.append(input("Bairro: "))
        endereco_tmp.append(input("Cidade: "))
        endereco_tmp.append(input("UF: "))

        usuarios.append(
            {
                "nome": nome,
                "data_nascimento": data_nascimento,
                "cpf": cpf,
                "endereco": " - ".join(endereco_tmp),
            }
        )


def f_listar_clientes(*, usuarios: list):
    """Listar os clientes"""

    print("\n--- Lista de Clientes ---")

    for usuario in usuarios:
        print(
            f"\nCliente: {usuario['nome']}",
            f"CPF: {usuario['cpf']}",
            f"Nasc.: {usuario['data_nascimento']}",
            sep="\t",
        )
        print(f"Endereço: {usuario['endereco']}")


def f_criar_conta(*, agencia: str, num_conta: int, usuarios: list, contas: list):
    """Criação de Conta Corrente"""
    print("\n---Criação de Conta Corrente ---\n")

    cpf = input("\nDigite o CPF do Cliente: ")

    usuario = f_localizar_usuario(cpf=cpf, usuarios=usuarios)
    if not usuario:
        print("\nUsuário não está cadastrado. Crie um este usuário antes.\n")
    else:
        contas.append(
            {
                "agencia": agencia,
                "num_conta": num_conta,
                "usuario": usuario,
            }
        )
        print(
            f"\nConta criada:\nAgência: {agencia} Núm. Conta: {num_conta} CPF: {cpf}\n",
            "." * 40,
        )
        num_conta += 1

    return num_conta


def f_listar_contas(*, contas):
    """Listar os contas"""

    print("\n--- Lista de Contas ---")

    for conta in contas:
        print(f"\nAgência: {conta['agencia']}\tNúm. Conta: {conta['num_conta']}")
        print(f"Cliente: {conta['usuario']['nome']}\tCPF: {conta['usuario']['cpf']}")
        print("." * 80)


def main():
    """Programa principal"""

    MENU = """
    ------------- Menu de acesso -------------
    [d] Depositar\t[s] Sacar\t[e] Extrato

    [u] Criar usuário
    [lu] Listar usuários

    [c] Criar conta
    [lc] Listar conta

    [q] Sair

    Selecione a opção: """

    saldo: float = 0.0
    extrato: str = ""
    numero_saques: int = 0

    LIMITE: int = 500
    LIMITE_SAQUES: int = 3

    usuarios = []

    num_conta_base: int = 1
    NUM_AGENCIA = "0001"
    contas = []

    limpar_tela()

    while True:

        opcao = input(MENU).lower()
        limpar_tela()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            if valor > 0:
                saldo, extrato = f_deposito(valor, saldo, extrato)
            else:
                print("Operação falhou! O valor informado é inválido.")

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            if valor > 0:
                saldo, extrato, numero_saques = f_saque(
                    valor=valor,
                    saldo=saldo,
                    extrato=extrato,
                    limite=LIMITE,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUES,
                )
            else:
                print("Operação falhou! O valor informado é inválido.")

        elif opcao == "e":
            f_extrato(saldo, extrato=extrato)

        elif opcao == "u":
            f_criar_cliente(usuarios=usuarios)

        elif opcao == "lu":
            f_listar_clientes(usuarios=usuarios)

        elif opcao == "c":
            num_conta_base = f_criar_conta(
                agencia=NUM_AGENCIA,
                num_conta=num_conta_base,
                usuarios=usuarios,
                contas=contas,
            )

        elif opcao == "lc":
            f_listar_contas(contas=contas)

        elif opcao == "q":
            break

        else:
            print(
                "Operação inválida, por favor selecione novamente a operação desejada."
            )

if __name__ == '__main__':
    main()
