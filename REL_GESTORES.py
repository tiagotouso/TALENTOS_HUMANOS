'''
GERADOR DE RELATÓRIO DOS SERVIDORES (GESTORES)
'''

from SQL import sqlpandas
from MENSAGEM import mensagemInformacao, mensagemErro
from AUXILIAR import salvarPandas

def ServidoresGestores():
    '''
    FUNÇÃO PARA CRIAR A LISTA DE SERVIDORES GESTORES
    ENTRA
        NULL
    SAI
        LISTA DE SERVIDORES GESTORES
    '''

    sql = """SELECT 
            A.CD_FUNCAO AS 'CD FUNÇÃO',
            a.cargo AS 'FUNÇÃO',
            a.DOC_LEGAL AS 'DOC LEGAL',
            B.GR_MATRICULA AS SIAPE,
            B.IT_NO_SERVIDOR AS SERVIDOR,
            B.IDADE,
            B.IT_CO_SEXO AS SEXO,
            B.DES_TITULACAO AS TITULAÇÃO,
            B.DES_ETNIA AS ETNIA,
            b.EMAIL,
            B.DES_REGIME_JURIDICO AS 'REG JUR',
            B.IT_CO_JORNADA_TRABALHO AS 'CARGA HORÁRIA',
            B.DES_CARREIRA AS CARREIRA,
            B.DES_CARGO AS CARGO,
            B.DES_GRUPO AS GRUPO,
            B.DES_LOTACAO AS 'LOTAÇÃO',
            B.DES_UPAG AS UPAG
        FROM
            ts_sis_chefias AS A
                JOIN
            tb_ser_rel AS B ON A.GR_MATRICULA = B.GR_MATRICULA;"""

    dados = sqlpandas(sql)
    if len(dados) > 0:
        salvarPandas(dados, 'SERVIDORES GESTORES')
        mensagemInformacao('Relatório dos Gestores criados com sucesso.')

    else:
        mensagemErro('Relatório dos Gestores não foi criados.')

