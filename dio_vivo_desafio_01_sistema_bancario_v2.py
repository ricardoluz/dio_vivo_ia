"""Sistema Bancário - versão 2 : objetos"""

import os
from abc import ABC, abstractmethod
from datetime import datetime as dt

# Dados para conta corrente.
LIMITE: int = 500
LIMITE_SAQUES: int = 3

class Historico:
    '''Classe de Histórico das operações'''
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        '''Retorno da transação'''
        return self._transacoes

    def adicionar_transacao(self, transacao):
        '''Adição de uma transação ao Histórico'''
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": dt.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Conta:
    """Conta de Cliente"""

    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        '''Criar uma conta para o cliente'''
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        '''Retornar o Histórico de operações'''
        return self._historico

    def depositar(self, valor):
        '''Realizar o depósito.'''

        if valor > 0:
            self._saldo += valor
            linha_msg(tipo=1,msg="Depósito realizado com sucesso.")
            return True
        else:
            linha_msg(tipo=-1,msg="Operação falhou: O valor informado é inválido.")
            return False

    def sacar(self, valor):
        '''Realizar o saque - básico.'''
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            linha_msg(tipo=-1,msg="Operação falhou: Você não tem saldo suficiente.")
            return False

        if valor > 0:
            self._saldo -= valor
            linha_msg(tipo=1,msg="Saque realizado com sucesso.")
            return True
        else:
            linha_msg(tipo=-1,msg="Operação falhou: O valor informado é inválido.")
            return False


class ContaCorrente(Conta):
    """Classe ContaCorrente - um tipo de Conta"""

    def __init__(self, numero, cliente, limite=LIMITE, limite_saques=LIMITE_SAQUES):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        'Sacar em conta corrente. Avalia limite e número de saques.'
        numero_saques = len(
            [
                transacao
                for transacao in self.historico.transacoes
                if transacao["tipo"] == Saque.__name__
            ]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            linha_msg(tipo=-1,msg=f"Operação falhou: O valor do saque excede o limite(R$ {self._limite:.2f}).")

        elif excedeu_saques:
            linha_msg(tipo=-1,msg=f"Operação falhou: Número saques excedido. (> {self._limite_saques}).")
        else:
            return super().sacar(valor) #Após validações, realiza o saque da conta.

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}\tNum. Conta:\t{self.numero}
        """


class Transacao(ABC):
    """Classe abstrata definindo a estrutura das transações"""

    @property
    @abstractmethod
    def valor(self):
        """Propriedade: Valor"""

    @classmethod
    @abstractmethod
    def registrar(cls, conta):
        """Registrar uma transação"""


class Cliente:
    """Classe Cliente"""

    def __init__(self, endereco: str):
        self._endereco = endereco
        self._contas = []

    @property
    def contas(self):
        '''Retorna as contas do cliente.'''
        return self._contas
    
    @property
    def endereco(self):
        '''Retorna o endereço do cliente.'''
        return self._endereco

    def realizar_transacao(self, conta, transacao: Transacao):
        """Realizar um transação"""
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """Adicionar uma conta a lista de contas do cliente"""
        self._contas.append(conta)

    def __str__(self):
        return f"{self.__class__.__name__}: \
            {", ".join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"


class PessoaFisica(Cliente):
    """Classe Pessoa Física"""

    def __init__(self, cpf: str, nome: str, data_nascimento: str, endereco: str):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        super().__init__(endereco)


class Deposito(Transacao):
    """Classe Depósito"""

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    """Classe Saque"""
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def limpar_tela():
    """Limpar a tela"""
    os.system("cls" if os.name == "nt" else "clear")


def linha_msg(*, tipo: int, msg: str):
    """Apresentaçao de mensagem em tela."""

    if tipo == -1:
        adereco = "@@@"  # Erro
    elif tipo == 0:
        adereco = "..."  # Neutra
    else:
        adereco = "==="  # Positiva

    # TODO: Trocar por switch.
    # TODO: Melhorar esta rotina, padronizando as mensagens.

    print(f"\n{adereco} {msg} {adereco}\n")


def localizar_cliente(*, cpf: str, clientes: list):
    """Verificar a existência de CPF"""

    cliente_localizado = [cliente for cliente in clientes if cliente.cpf == cpf]
    return cliente_localizado[0] if cliente_localizado else None


def criar_cliente(clientes: list):
    """Criação de Cliente"""

    linha_msg(tipo=0, msg="Criação de Cliente")

    cpf = "".join([x for x in input("Digite o CPF do novo Cliente: ") if x.isdigit()])
    if cpf == "":
        linha_msg(tipo=-1,msg="CPF deve ser númerico.")
        return

    if localizar_cliente(cpf=cpf, clientes=clientes):
        linha_msg(tipo=-1, msg=f"Cliente já cadastrado com este CPF: ({cpf})")
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

        cliente = PessoaFisica(
            nome=nome,
            data_nascimento=data_nascimento,
            cpf=cpf,
            endereco=" - ".join(endereco_tmp),
        )

        clientes.append(cliente)


def criar_conta_corrente(clientes, contas):
    """Criação de Conta"""

    linha_msg(tipo=0, msg="Criação de Conta")

    cpf = "".join([x for x in input("Digite o CPF do Cliente: ") if x.isdigit()])
    cliente: Cliente = localizar_cliente(cpf=cpf, clientes=clientes)

    if not cliente:
        linha_msg(
            tipo=-1,
            msg="Cliente não cadastrado. Crie um este cliente com este CPF antes.",
        )
        return

    numero_conta = len(contas) + 1
    conta_corrente = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)

    contas.append(conta_corrente)                    # Adicionar a conta a lista de contas.
    cliente.adicionar_conta(conta=conta_corrente)    # Adicionar a conta ao cliente.

    linha_msg(
        tipo=1,
        msg=f"Conta criada: Agência: {conta_corrente.agencia} - Núm. Conta: {numero_conta} - CPF: {cliente.cpf}"
    )


def escolher_conta_cliente(cliente: Cliente):
    """Escolher a conta do cliente"""
    if not cliente.contas:
        linha_msg(tipo=-1, msg="Cliente não possui conta.")
        return

    # TODO: criar rotina para escolha de uma conta, quando houver + que uma.
    if len(cliente.contas) == 1:
        return cliente.contas[0]
    else:
        return cliente.contas[0]


def depositar(clientes):
    '''Depositar na conta de cliente'''

    linha_msg(tipo=0,msg="Depósito em Conta")

    cpf = input("Informe o CPF do cliente: ")

    cliente: Cliente = localizar_cliente(cpf=cpf, clientes=clientes)
    if not cliente:
        linha_msg(
            tipo=-1,
            msg="Cliente não cadastrado. Crie um este cliente com este CPF antes.",
        )
        return

    conta = escolher_conta_cliente(cliente)
    if not conta:
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao: Transacao = Deposito(valor)

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    '''Sacar na conta de cliente'''

    linha_msg(tipo=0,msg="Saque em Conta")

    cpf = input("Informe o CPF do cliente: ")

    cliente: Cliente = localizar_cliente(cpf=cpf, clientes=clientes)
    if not cliente:
        linha_msg(
            tipo=-1,
            msg="Cliente não cadastrado. Crie um este cliente com este CPF antes.",
        )
        return

    conta = escolher_conta_cliente(cliente)
    if not conta:
        return

    valor = float(input("Informe o valor do saque: "))
    transacao: Transacao = Saque(valor)

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(*, clientes):
    '''Exibir o extrato'''

    cpf = input("Informe o CPF do cliente: ")
    cliente: Cliente = localizar_cliente(cpf=cpf, clientes=clientes)

    if not cliente:
        linha_msg(
            tipo=-1,
            msg="Cliente não cadastrado. Crie um este cliente com este CPF antes.",
        )
        return

    conta = escolher_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}\t:\tR$ {transacao['valor']:.2f}".expandtabs(10)
            # extrato += f'{0}\t{1}'.format(transacao['tipo'],transacao['valor']).expandtabs(13)
    print(extrato)
    print(f"\nSaldo\t:\tR$ {conta.saldo:.2f}".expandtabs(10))
    print("==========================================")


def listar_clientes(*, clientes):
    """Listar os clientes"""

    linha_msg(tipo=0,msg="Lista de Clientes")

    for cliente in clientes:
        print(
            f"\nCliente: {cliente.nome}",
            f"CPF: {cliente.cpf}",
            f"Nasc.: {cliente.data_nascimento}",
            sep="\t",
        )
        print(f"Endereço: {cliente.endereco}")

        linha_msg(tipo=0,msg="Contas")

        for conta in cliente.contas:
            print(conta)


def main():
    """Função principal"""

    clientes = []
    contas = []

    MENU = """
    ------------- Menu de acesso -------------
    [d] Depositar\t[s] Sacar\t[e] Extrato

    [u] Criar cliente (usuário)
    [lu] Listar clientes

    [c] Criar conta

    [q] Sair

    Selecione a opção: """

    limpar_tela()

    while True:

        opcao = input(MENU).lower()
        limpar_tela()

        if opcao == "u":
            criar_cliente(clientes=clientes)

        elif opcao == "lu":
            listar_clientes(clientes=clientes)            

        elif opcao == "c":
            criar_conta_corrente(clientes, contas)

        elif opcao == "d":
            depositar(clientes=clientes)

        elif opcao == "s":
            sacar(clientes=clientes)

        elif opcao == 'e':
            exibir_extrato(clientes=clientes)

        elif opcao == "q":
            break

        else:
            linha_msg(
                tipo=-1,
                msg="Operação inválida, por favor selecione novamente a operação desejada.",
            )


if __name__ == "__main__":
    main()
