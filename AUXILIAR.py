'''

'''

import pandas as pd
from datetime import datetime


def salvarPandas(dados, narquivo, caminhoRelatorio = 'RELATORIOS\\'):
    '''
    FUNÇÃO PARA SALVAR DADOS DOS DATAFRAME (PANDAS)
    ENTRA
        DADOS (DATAFRAME)
    SAI
        RELATÓRIO EM CSV (CSV)
    '''

    sep = '\t'
    codificacao = 'utf-16'


    data = str(datetime.now().date()) + ' '
    nome = caminhoRelatorio + data + narquivo
    dados.to_csv(nome + '.csv', sep=sep, encoding=codificacao)


