'''
ARQUIVO PARA IMPORTAR OS AMBIENTES DOS SERVIDORES

OSB: COLOCAR A LISTA DE SERVIDORES (XLSX) COM OS CAMPOS [SIAPE - AMBIENTE - SETOR EXERCÍCIO]
'''
import os
import pandas as pd

from SQL import sqlexecute
from MENSAGEM import mensagemErro, mensagemInformacao

def importarAmbienteServidores():
    '''
    FUNÇÃO IMPORTAR AMBIENTE E EXERCÍCIO DOS SERVIDORES PARA O BANCO DE DADOS
    ENTRA
        PLANILHA DOS SERVIDORES DO SISTEMA INTEGRADO (RELATÓRIO)
    SAI
        BANCO DE DADOS ATUALIZADO COM AMBIENTE E EXERCÍCIO DOS SERVIDORES
    '''

    listdir = os.listdir('DADOS_EXTRATOR\\')
    if 'servidores.xlsx' in listdir:

        xls = 'DADOS_EXTRATOR\\servidores.xlsx'
        folha = 'Servidores'

        arq = pd.read_excel(xls, folha)
        dados = arq[['Siape', 'Ambiente', 'Exercício']]
        dados = dados[dados['Siape'].notnull()]
        dados['Siape'] = dados['Siape'].apply(lambda x: str(x).rjust(7, '0'))
        dados = dados.dropna(thresh=2)
        dados = dados.fillna('null')
        dados = dados[dados.duplicated() == False]

        sql = '''delete from ts_sis_ambientes;'''
        sqlexecute(sql)

        sql = '''INSERT INTO ts_sis_ambientes\n(GR_MATRICULA, AMBIENTE, EXERCICIO)\nvalues\n'''
        lx = ''
        for i in dados.values:
            if len(i[0]) == 7:
                lx = '''( '{0}', '{1}', '{2}' ),\n'''.format(i[0], i[1], i[2])
                sql += lx
        sql = sql[:-2] + ';'
        sql = sql.replace('\'null\'', 'null')
        sqlexecute(sql)

        mensagemInformacao('Importação do AMBIENTE concluída.')
    else:
        mensagemErro('Arquivo "servidores.xlsx" não encontrado. (AMBIENTE)')

