import sys
import time
import oracledb

login = 'rm551938'
senha = '080105'

conn = oracledb.connect( user = login, password = senha, dsn="oracle.fiap.com.br/orcl")

cursor = conn.cursor()



def encerrar_programa():
    print("Encerrando o programa.")
    sys.exit()   

    
def ler_quadro(saida):
    #leitura do banco' ''
    print(saida)
    quadro = []
    #banana,mamao,papaia
    acumulador = ""
    for n in range(len(saida)):
        if saida[n] == ",":
            quadro.append(acumulador)
            acumulador = ""
        else:
            acumulador += saida[n]
    return quadro    

def detectar_quadro_diabetes(quadro):
    teste = 0
    for n in quadro:
        if n in ["sede", "muita sede", "água"]:
            teste += 1
        elif n in ["muito uso do banheiro", "mijar", "mijo", "urinar", "urina"]:
            teste += 1
        elif n in ["não cicatriza", "cicatrização", "falta de cicatrização", "sangramento não para"]:
            teste += 1
        elif n in ["dormência na perna", "dormência na mão", "dormência", "não sinto as pernas"]:
            teste += 1
    if teste > 3:
        exame = realizar_pergunta(pergunta="Você tem o hemograma completo recente contigo? ", resposta1="sim", resposta2="não")
        if exame =="não":
            print("Volte com os exames, você pode estar com diabetes")
        else:
            print("REALIZAR CONSUMO DE API")
            
        


def corrigir_tipo_pergunta(tipo, pergunta):
    while True:
        try:
            valor = tipo(input(f"{pergunta} "))
            return valor
        except (TypeError, ValueError):
            print("Valor incorreto passado")


def realizar_pergunta(pergunta, resposta1, resposta2):
    conta = input(pergunta).lower()
    tentativa = 0

    while conta != resposta1 and conta != resposta2:
        conta = input(
            f"Resposta inválida, você ainda tem {3 - tentativa} tentativas. Digite {resposta1}/{resposta2}: "
        ).lower()
        tentativa += 1
        if tentativa == 3:
            print("Você excedeu o limite de tentativas. Recomece o processo.")
            encerrar_programa()

    return conta


def finalizar():
    print("A Jannos Enterprise agradece a visita!")
    encerrar_programa()


def fazer_login():
    nome = input("Digite o seu nome: ")
    cpf = input("Digite seu cpf: ")
    time.sleep(3)

    sql = "SELECT * FROM t_hosp_janus_paciente WHERE nr_cpf = :cpf"

    cursor.execute(
        sql,
        {
            "cpf": {cpf}
        })
    
    dadosCliente = cursor.fetchall()[0]

    if dadosCliente != None:
            return print(f"Login Feito! Bem vindo, {nome}!")
    else: 
        return print(f"Erro ao fazer login! Não foi possivel encontrar o cpf: {cpf}")



def select_paciente(cpf, email):

    select_cpf = "SELECT * FROM t_hosp_janus_paciente WHERE nr_cpf = :cpf"
    select_email = "SELECT * FROM t_hosp_janus_paciente WHERE ds_email = :email"

    cursor.execute(select_cpf,{"cpf": cpf})
    
    cursor.execute(select_email,{"email": email})

    cpf_banco = cursor.fetchall()[0]
    email_banco = cursor.fetchall()[1]

    if cpf_banco == cpf and email_banco == email:
        return("Dados já existentes no banco de dados!")
    
    if cpf_banco == cpf:
        return("CPF já cadastrados anteriormente, por favor utilize um cpf valido")
    
    if email_banco == email:
        return("Email já existente em nosso banco de dados, por favor utilize outro não cadastro anteriormente")
    
    return ("Dados válidos! ")


def  insert_paciente(nome, dtNascimento, cpf, email, peso, altura):

    sql = "INSERT INTO t_hosp_janus_paciente VALUES (SEQ_PACIENTE.NEXTVAL, :nm_cliente, to_date(:dt_nascimento, 'dd-mm-yyyy'), :nr_cpf, :ds_email, :ds_peso, :ds_altura)"

    try:
        cursor.execute(sql, {
            "nm_paciente": nome,
            "dt_nascimento": dtNascimento,
            "nr_cpf": cpf,
            "ds_email": email,
            "ds_peso": peso,
            "ds_altura": altura
        })
    finally:
        conn.commit()


def cadastro():
    nome = corrigir_tipo_pergunta(tipo=str, pergunta="Qual seu nome completo? ")
    email = corrigir_tipo_pergunta(tipo=str, pergunta="Qual seu email? ")
    cpf = corrigir_tipo_pergunta(tipo=str, pergunta="Qual seu cpf? ")
    dtNascimento = corrigir_tipo_pergunta(tipo=str, pergunta="Qual sua data de nascimento? ")
    peso = corrigir_tipo_pergunta(tipo=str, pergunta="Qual sua data de nascimento? ")
    altura = corrigir_tipo_pergunta(tipo=str, pergunta="Qual sua data de nascimento? ")

    returnoSelect = select_paciente(cpf, email)

    if returnoSelect == "Dados válidos!":
        insert_paciente(nome, dtNascimento,  cpf, email, peso, altura)
        return(f"Bem-vindo {nome}, é um prazer ter você conosco")
    else: 
        return("Erro no insert!")
    

def  inserir_medicamento(remedio_nome):

    sql = "INSERT INTO t_hosp_janus_remedio VALUES (SEQ_REMEDIO.NEXTVAL, SEQ_REMEDIO.CURRVAL, :nm_remedio)"

    try:
        cursor.execute(sql,{
            "nm_remedio": remedio_nome
        })

    finally:
        conn.commit()

    return("Medicamento inserido com sucesso! ")

def  insert_sintomas(sintomas, data_sintomas):

    sql = "INSERT INTO t_hosp_janus_sintoma VALUES (SEQ_SINTOMA.NEXTVAL, SEQ_SINTOMA.CURRVAL, :ds_sintoma, to_date(:dt_inicio , 'dd-mm-yyyy'))"

    try:
        cursor.execute(sql, {
            "ds_sintoma": sintomas,
            "dt_inicio": data_sintomas
        })
    finally:
        conn.commit()

    return("Sintomas cadastrados com sucesso!")

    

    


