import sqlite3

class Quarto:
    def __init__(self, numero, diaria, ocupacao_maxima=1):
        self.numero = numero
        self.diaria = diaria
        self.ocupacao_maxima = ocupacao_maxima
        self.reservas = []

class Hospede:
    def __init__(self, cpf, nome, idade, telefone):
        self.cpf = cpf
        self.nome = nome
        self.idade = idade
        self.telefone = telefone

class Pousada:
    def __init__(self):
        self.quartos = []
        self.conexao = sqlite3.connect('banco_de_dados.db')
        self.criar_tabela_hospedes()

    def criar_tabela_hospedes(self):
        cursor = self.conexao.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS hospedes
                          (cpf TEXT PRIMARY KEY, nome TEXT, idade INTEGER, telefone TEXT)''')
        self.conexao.commit()

    def cadastrar_quarto(self, numero, diaria, ocupacao_maxima=1):
        quarto = Quarto(numero, diaria, ocupacao_maxima)
        self.quartos.append(quarto)

    def cadastrar_hospede(self, cpf, nome, idade, telefone):
        cursor = self.conexao.cursor()
        cursor.execute("INSERT INTO hospedes VALUES (?, ?, ?, ?)", (cpf, nome, idade, telefone))
        self.conexao.commit()
        print("Hóspede cadastrado com sucesso!")

    def buscar_hospede(self, cpf):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM hospedes WHERE cpf = ?", (cpf,))
        resultado = cursor.fetchone()
        if resultado:
            cpf, nome, idade, telefone = resultado
            hospede = Hospede(cpf, nome, idade, telefone)
            return hospede
        else:
            return None

    def fazer_reserva(self, cpf, quarto_numero, periodo):
        hospede = self.buscar_hospede(cpf)
        if not hospede:
            print("Hóspede não encontrado.")
            return

        quarto = next((q for q in self.quartos if q.numero == quarto_numero), None)
        if not quarto:
            print("Quarto não encontrado.")
            return

        if len(quarto.reservas) >= quarto.ocupacao_maxima:
            print("Este quarto atingiu sua ocupação máxima.")
            return

        valor_total = quarto.diaria * periodo

        reserva = {
            'hospede': hospede,
            'periodo': periodo,
            'quarto': quarto,
            'valor_diaria': quarto.diaria,
            'valor_total': valor_total
        }

        quarto.reservas.append(reserva)

        if quarto.ocupacao_maxima > 1:
            print(f"O quarto {quarto.numero} pode acomodar até {quarto.ocupacao_maxima} pessoas.")
            print("Gostaria de adicionar mais hóspedes? (S/N)")
            resposta = input()
            while resposta.lower() == 's':
                cpf_hospede = input("Digite o CPF do hóspede adicional: ")
                hospede_adicional = self.buscar_hospede(cpf_hospede)
                if not hospede_adicional:
                    print("Hóspede não encontrado.")
                else:
                    reserva['hospede'].append(hospede_adicional)
                    print(f"Hóspede adicionado com sucesso!")
                print("Gostaria de adicionar mais hóspedes? (S/N)")
                resposta = input()

        print("Reserva efetuada com sucesso!")
        print(f"Valor da diária: R$ {quarto.diaria}")
        print(f"Valor total: R$ {valor_total}")
        self.exibir_tabela_disponibilidade()
        self.imprimir_recibo(reserva)
        def remover_reserva(self, cpf, quarto_numero):
         quarto = next((q for q in self.quartos if q.numero == quarto_numero), None)

         for reserva in quarto.reservas:
            if reserva['hospede'].cpf == cpf:
                quarto.reservas.remove(reserva)
                print("Reserva removida com sucesso!")
                break
            else:
             print("Nenhuma reserva encontrada para o hóspede informado.")

        self.exibir_tabela_disponibilidade()

    def fazer_checkout(self, cpf, quarto_numero):
        quarto = next((q for q in self.quartos if q.numero == quarto_numero), None)

        for reserva in quarto.reservas:
            if reserva['hospede'].cpf == cpf:
                self.imprimir_comprovante_checkout(reserva)
                quarto.reservas.remove(reserva)
                print("Check-out realizado com sucesso!")
                break
        else:
            print("Nenhuma reserva encontrada para o hóspede informado.")

        self.exibir_tabela_disponibilidade()

    def exibir_tabela_disponibilidade(self):
        print("Tabela de Disponibilidade:")
        print("----------------------------------")
        print("| Número | Disponibilidade | Hóspede")
        print("----------------------------------")

        for quarto in self.quartos:
            if quarto.reservas:
                reserva = quarto.reservas[0]
                disponibilidade =  f"Reservado   | {reserva['hospede'].nome}"
            else:
                disponibilidade = "Disponível  |"

            print(f"|   {quarto.numero}   |   {disponibilidade}   |")

        print("----------------------------------")
        disponiveis = sum(1 for quarto in self.quartos if not quarto.reservas)
        print(f"Quartos disponíveis: {disponiveis}\n")

    def imprimir_recibo(self, reserva):
        print("\nRECIBO DE RESERVA")
        print("------------------")
        print(f"Hóspede: {reserva['hospede'].nome}")
        print(f"Quarto: {reserva['quarto'].numero}")
        print(f"Diária: R$ {reserva['valor_diaria']}")
        print(f"Período: {reserva['periodo']} dias")
        print(f"Total a pagar: R$ {reserva['valor_total']}")
        print("------------------\n")

    def imprimir_comprovante_checkout(self, reserva):
        print("\nCOMPROVANTE DE CHECK-OUT")
        print("-------------------------")
        print(f"Hóspede: {reserva['hospede'].nome}")
        print(f"Quarto: {reserva['quarto'].numero}")
        print(f"Diária: R$ {reserva['valor_diaria']}")
        print(f"Período: {reserva['periodo']} dias")
        print(f"Total pago: R$ {reserva['valor_total']}")
        print("-------------------------\n")


pousada = Pousada()

# Cadastro de quartos
for i in range(1, 16):
    if i < 6:
        pousada.cadastrar_quarto(i, 100, 1)
    elif i < 11:
        pousada.cadastrar_quarto(i, 150, 2)
    else:
        pousada.cadastrar_quarto(i, 200, 3)

print("Bem-vindo à Pousada!")
print("Tabela de Preços:")
print("------------------")
print("| Número |   Diária   | Ocupação Máxima |")
print("------------------")
for quarto in pousada.quartos:
    print(f"|   {quarto.numero}   |  R$ {quarto.diaria}  |       {quarto.ocupacao_maxima}       |")
print("------------------\n")

# Reservas e check-out
while True:
    continuar_reservas = True

    print("O que deseja realizar?")
    print(" 1 - Cadastrar hóspede")
    print(" 2 - Realizar reserva")
    print(" 3 - Fazer check-out")
    print(" 4 - Encerrar sessão")
    opcao = int(input("Digite um número: "))
    if opcao == 1:
        cpf = input("Digite o CPF do hóspede: ")
        nome = input("Digite o nome do hóspede: ")
        idade = int(input("Digite a idade do hóspede: "))
        telefone = input("Digite o telefone do hóspede: ")
        pousada.cadastrar_hospede(cpf, nome, idade, telefone)
    elif opcao == 2:
        cpf = input("Digite o CPF do hóspede: ")
        quarto_numero = int(input("Digite o número do quarto desejado: "))
        periodo = int(input("Digite o período de dias da reserva: "))
        pousada.fazer_reserva(cpf, quarto_numero, periodo)
    elif opcao == 3:
        cpf = input("Digite o CPF do hóspede: ")
        quarto_numero = int(input("Digite o número do quarto da reserva: "))
        pousada.fazer_checkout(cpf, quarto_numero)
    elif opcao == 4:
        continuar_reservas = False
        print("Sessão encerrada.")
    else:
        print("Opção inválida.")

    if not continuar_reservas:
        break