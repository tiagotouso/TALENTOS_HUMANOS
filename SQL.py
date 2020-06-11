'''
ARQUIVO PARA CONEXÃO COM BANCO DE DADOS

SERVICE Mysql@localhost:3306
User root
Password ROOT123
'''
import pandas as pd
import pymysql
from datetime import datetime


host = 'localhost'
user = 'root'
passwd = 'root123'
db = 'talentoshumanos'

def sqlpandas(sql):
    '''
     FUNÇÃO PARA EXECUTAR PESQUISA SQL NO BANCO
     ENTRA
         COMANDO SQL
     SAI
         PANDAS COM DADOS DA PESQUISADA NO BANCO DE DADOS
     '''
    conn = pymysql.connect(
        host=host,
        user=user,
        passwd=passwd,
        db=db)
    dd = pd.read_sql_query(sql, conn)
    return dd


def teste_conexao():
    '''
    FUNÇÃO
        REALIZAR TESTE DE CONEXÃO
    ENTRA
        NULL
    SAI
        CONEXÃO CONCLUÍDA OU NÃO
    '''
    try:
        conexao = pymysql.connect(host=host, user=user, passwd=passwd, db=db, autocommit=True)
        cursor = conexao.cursor()
        print('Conexão realizada com sucesso.')
    except:
        print('Erro ao acessar o banco')


def contadorerro():
    '''
    FUNÇÃO PARA GERAR O CONTADOR DE ERROS
    ENTRA
        NULL
    SAI
        NUMERO DE ERRO
    '''
    for n in range(1, 500):
        yield n

#VERIFICAR DE PODE SER EXCLUÍDO
contador = contadorerro()

def arquivotexto(texto):
    '''
    FUNÇÃO
        SALVAR MENSAGEM DE ERRO DO SQL
    ENTRA
        O ARQUIVO SQL E A MENSAGEM
    SAI
        SAI O ARQUIVO TXT COM O SQL E O ERRO
    '''

    numero = str(next(contador)).rjust(5, '0')

    data = str(datetime.now())[:10]
    arquivo = 'RELATORIOS DE ERRO\\' + data + ' ' + numero +' ERRO SISTEMA.TXT'

    arq = open(arquivo, 'w')
    arq.write(texto)
    arq.close()

def sqlinclusaotabela(planilha, tabela):
    '''
    FUNÇÃO PARA CRIAR UM INSERT E GRAVAR UMA TABELA NO BANCO DE DADOS
    ENTRA
        TABELA (LIST) COM DADOS
    SAI
        DADOS GRAVADOS NO BANCO DE DADOS
    '''
    try:
        conexao = pymysql.connect(host=host, user=user, passwd=passwd, db=db, autocommit=True)
        cursor = conexao.cursor()
        campos = str(planilha[0])
        campos = '(' + campos[1:-1] + ')'
        campos = campos.replace('\'','')
        contador = 0
        total = len(planilha)
        for linha in planilha[1:]:
            sql = ('INSERT INTO ' + tabela + ' ' + campos + ' VALUES (' + str(linha)[1:-1].replace('\'null\'', 'null') + ')')
            contador += 1
            valor = round(contador * 100 / total)
            print(contador,valor,'%','#' * valor)
            cursor.execute(sql)
        cursor.close()
        conexao.close()
    except Exception:
        sql = sql.replace(',', ',\n')
        men = 'Erro ao conectar com MYSQL - sqlinclusaotabela'
        arquivotexto(men + '\n\n' + sql)
        print(men)

def sqlexecute(sql):
    '''
    FUNÇÃO PARA EXECUTAR COMANDO SQL NO BANCO
    ENTRA
        COMANDO SQL
    SAI
        COMANDO SQL EXETUTADO NO BANCO DE DADOS
    '''
    try:
        conexao = pymysql.connect(host=host, user=user, passwd=passwd, db=db, autocommit=True)
        cursor = conexao.cursor()
        cursor.execute(sql)
        cursor.close()
        conexao.close()
    except Exception:
        men = 'Erro ao conectar com MYSQL - sqlexecute'
        arquivotexto(men + '\n\n' + sql)
        print(men)

def sqlpesquisar(sql):
    '''
    FUNÇÃO PARA EXECUTAR PESQUISA SQL NO BANCO
    ENTRA
        COMANDO SQL
    SAI
        COMANDO SQL PESQUISADA NO BANCO DE DADOS
    '''
    try:
        conexao = pymysql.connect(host=host, user=user, passwd=passwd, db=db)
        cursor = conexao.cursor()
        cursor.execute(sql)
        linha = cursor.fetchall()
        if len(linha) > 0:
            return 1, linha
        else:
            return 0, 0
            print('Nenhum valor encontrado.')
        cursor.close()
        conexao.close()
    except Exception:
        men = 'Erro ao conectar com MYSQL - sqlpesquisar'
        arquivotexto(men + '\n\n' + sql)
        print(men)

