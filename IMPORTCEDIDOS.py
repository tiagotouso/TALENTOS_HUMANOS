'''
ARQUIVO PARA IMPORTAR OS SERVIDORES CEDIDOS DO RELATÓRIO DO SIAPE

OBS: IMPRIMIR RELATÓRIO (>CACOSEREEU (UPAGS 12 E 279) E SALVAR NA PASTA DADOS_EXTRATOR COM NOME DE 'CEDIDOS'
'''
import pandas as pd
import os
from SQL import sqlexecute
from MENSAGEM import mensagemErro, mensagemInformacao


def ImportarServidoresCedidos():
    '''
    FUNÇÃO PARA IMPORTAR O SERVIDORES CEDIDOS PARA O SISTEMA (IMFORMAÇÃO PARA AGENTES PÚBLICOS)
    ENTRA
        RELATÓRIO DO SIAPE COM O SERVIDORES CEDIDOS
    SAI
        BANCO DE DADOS ATUALIZADO COM SERVIDORES CEDIDOS
    '''

    listdir = os.listdir('DADOS_EXTRATOR\\')
    if 'CEDIDOS.TXT' in listdir:

        sql = 'delete  from ts_sis_cedidos;'
        sqlexecute(sql)

        arq = open('DADOS_EXTRATOR\\CEDIDOS.txt', 'r')
        texto = arq.read()
        arq.close()

        texto = texto.split('\n')
        newtb = []
        for vl in range(0, len(texto)):
            if texto[vl].count('INICIO:') > 0:
                l2 = texto[vl].split()
                l1 = texto[vl - 1].split()

                siapecad = l1[0]
                orgao = l1[-1]
                data = l2[1]

                ano = data[5:]
                mes = data[2:5]
                dia = data[0:2]

                txmes = 'JAN FEV MAR ABR MAI JUN JUL AGO SET OUT NOV DEZ'.split()

                dicmes = {}
                contador = 1
                for vl in txmes:
                    dicmes[vl] = contador
                    contador += 1

                mes = dicmes[mes]

                data = '{0}-{1}-{2}'.format(ano, mes, dia)

                lotacao = l2[-1]

                newtb.append((siapecad, data, lotacao, orgao))

        sql = ''
        for i in newtb:
            sql += str(i) + ',\n'
        sql = sql.replace('[', '(')
        sql = sql.replace(']', ')')
        sql = sql[:-1] + ';'
        sql = sql.replace(',;', ';')

        sql = '''INSERT INTO ts_sis_cedidos
        (SIAPECAD, DT_I, LOTACAO, ORGAO)
        VALUES\n''' + sql

        sqlexecute(sql)


        mensagemInformacao('Importaçaõ dos CEDIDOS-SIAPE concluída.')
    else:
        mensagemErro('Arquivo CEDIDOS.TX não encontrado.')

