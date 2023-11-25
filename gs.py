import time
from funcoes import *

 


while True:
    menu = realizar_pergunta(
        pergunta="Seja bem vindo ao Jannos Enterprise, você já tem cadastro? ou deseja fazer login?",
        resposta1="login",
        resposta2="cadastro",
    )
    if menu == "login":
        fazer_login()
        """este método precisa verificar com o banco se ele realmente tem login"""
        escolha = realizar_pergunta(
            pergunta="Deseja vizualizar algum quadro passado ou iniciar telemedicina? (vizualizar/telemedicina)",
            resposta1="vizualizar",
            resposta2="telemedicina",
        )
        if escolha == "vizualizar":
            """precisamos exibir os dados dele com um select"""
        else:
            print("Iniciando contato com o medico...")
            time.sleep(3)
            print("Telemedicina iniciada")
    if menu == "cadastro":
        """vai cair no resposta2 de qualquer maneira mesmo sendo else"""
        cadastro()
        escolha = realizar_pergunta(
            pergunta="Deseja adicionar seus dados de saúde no nosso aplicativo agora? ",
            resposta1="sim",
            resposta2="não",
        )
        if escolha == "sim":
            """alterar ou criar os dados de saúde do cliente no banco"""
            sintomas = input("Resuma em poucas palavras os sintomas: ")
            data_sintomas = input("Informe o inicio dos sintomas com datas(DD-MM-YYYY): ")
            insert_sintomas(sintomas, data_sintomas)

            remedio = realizar_pergunta(
            pergunta="Foi tomado algum medicamento? ",
            resposta1="sim",
            resposta2="não",
        )
            if remedio == "sim":
                remedio_nome = input("Qual o nome do medicamento? ")
                inserir_medicamento(remedio_nome)
            else:
                print("Seus dados foram adicionados")

            consulta = realizar_pergunta(
                pergunta="Deseja iniciar uma consulta de telemedicina? ",
                resposta1="sim",
                resposta2="não",
            )
            if consulta == "sim":
                print("Iniciando contato com o medico...")
                time.sleep(3)
                print("Telemedicina iniciada")
            else:
                finalizar()
        else:
            finalizar()
