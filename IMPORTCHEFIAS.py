'''
ARQUIVO PARA IMPORTAR CHEFIA

OSB: COLOCAR A LISTA DE CHEFIAS (XLSX) COM OS CAMPOS [SIAPE - CD FUNÇÃO - CARGO - DOC LEGAL]
'''
import os
import pandas as pd

from SQL import sqlexecute
from MENSAGEM import mensagemErro, mensagemInformacao

def importarChefias():
    '''
    FUNÇÃO PARA IMPORTAR AS CHEFIAS PARA O BANCO DE DADOS
    ENTRA
        PLANILHA DE CHEFIAS DA DIVISÃO DE CADASTRO
    SAI
        BANCO DE DADOS ATUALIZADOS COM AS CHEFIAS
    '''

    listdir = os.listdir('DADOS_EXTRATOR\\')
    if 'Relação de Chefias.xlsx' in listdir:

        xls = 'DADOS_EXTRATOR\\Relação de Chefias.xlsx'
        folha = 'FG E CD - ATIVOS'

        arq = pd.read_excel(xls, folha)
        dados = arq[['SIAPE', 'FUNÇÃO', 'CARGO', 'DOC. LEGAL']].copy()
        dados.dropna(inplace=True, axis=0)
        planilha = [['GR_MATRICULA', 'CD_FUNCAO', 'CARGO', 'DOC_LEGAL']]
        for i in dados.values:
            aux = []
            aux.append(str(int(i[0])).rjust(7, '0')[0:7])
            aux.append(i[1])
            aux.append(i[2])
            aux.append(i[3])
            planilha.append(aux)

        sql = '''delete from ts_sis_chefias;'''
        sqlexecute(sql)

        sql = '''INSERT INTO ts_sis_chefias\n(GR_MATRICULA, CD_FUNCAO, CARGO, DOC_LEGAL)\nvalues\n'''
        contador = len(planilha[1:])
        for i in planilha[1:]:
            contador -= 1
            if contador != 0:
                sql += '(' + str(i)[1:-1] + '),\n'
            else:
                sql += '(' + str(i)[1:-1] + ');'
        sqlexecute(sql)

        mensagemInformacao('Importação da LISTA DE CHEFIAS concluída.')
    else:
        mensagemErro('Arquivo Relação de Chefias.xlsx não encontrado.')

