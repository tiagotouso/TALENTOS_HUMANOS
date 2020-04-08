'''
ARQUIVO PARA IMPORTAR E-MAIL DOS SERVIDORES

OSB: COLOCAR A LISTA DE SERVIDORES (XLSX) COM OS CAMPOS [SIAPE - E-MAIL]
'''
import os
import pandas as pd

from SQL import sqlexecute, sqlpesquisar
from MENSAGEM import mensagemErro, mensagemInformacao


def importarEmailServidor():
    '''
    FUNÇÃO PARA ATULALIZAR OS EMAIL DOS SEVIDORES QUE INGRESSARAM NA UFTM
    ENTRA
        PLANILHA COM OS DADOS DOS SERVIDORES
    SAI
        SAIR O BANCO DE DADO ATUALIZADO
    '''

    listdir = os.listdir('DADOS_EXTRATOR\\')
    if 'servidores.xlsx' in listdir:

        sql = '''select 
                  GR_MATRICULA, IT_NO_SERVIDOR, IT_NU_CPF, DES_CARREIRA, DES_CARGO, EMAIL
                  from tb_ser_rel 
                  WHERE EMAIL IS NULL
                  AND IT_DA_OCOR_INATIVIDADE_SERV IS NULL
                  AND IT_DA_OCOR_EXCLUSAO_SERV IS NULL
                  order by it_no_servidor;'''

        vl, tb = sqlpesquisar(sql)
        if vl == 1:
            xls = 'DADOS_EXTRATOR\\servidores.xlsx'
            folha = 'Servidores'
            arq = pd.read_excel(xls, folha)
            dados = arq
            dc = {}
            for i in tb:
                email = dados[dados['Siape'] == int(i[0])]['Email']
                if email.count() >= 1:
                    dc[i[2]] = email.values[0]

            for i in dc:
                sql = '''INSERT INTO ts_sis_email VALUES ('{0}', '{1}');'''.format(i, dc[i])
                sqlexecute(sql)

        mensagemInformacao('Importação do E-MAIL concluída.')
    else:
        mensagemErro('Arquivo "servidores.xlsx" não encontrado. (E-MAIL)')


