'''
GERADOR DE RELATÓRIO DOS SERVIDORES (SERVIDORES ANO A ANO)
'''

from SQL import sqlpandas
from MENSAGEM import mensagemInformacao, mensagemErro
from AUXILIAR import salvarPandas

def servidoresanoano():
    '''
    FUNÇÃO PARA CRIAR A TABELA ANO A ANO, COM ENTRADA E SAÍDA DOS SERVIDORES
    ENTRA
        NULL
    SAI
        RELATÓRIO ANO A ANO EM CSV (CSV)
    '''

    sql = '''
    SELECT A.*,
    IT_NO_SERVIDOR AS 'SERVIDOR',
    B.DES_ETNIA AS 'ETNIA',
    B.DES_NACIONALIDADE AS 'NACIONALIDADE',
    b.DES_REGIME_JURIDICO AS 'REG-JUR',
    B.DES_CARREIRA AS 'CARREIRA',
    B.DES_CARGO AS 'CARGO',
    B.DES_GRUPO AS 'GRUPO',
    B.DES_UPAG AS 'UPAG',
    B.IT_CO_JORNADA_TRABALHO AS 'CH',
    B.IT_DA_OCOR_INGR_SPUB_SERV AS 'DT I SP',
    B.IT_DA_OCOR_INGR_ORGAO_SERV AS 'DT I O',
    B.IT_DA_OCOR_INATIVIDADE_SERV AS 'DT APO',
    B.IT_DA_OCOR_EXCLUSAO_SERV AS 'DT DES',
    b.email
    FROM
    anoano AS A
    join tb_ser_rel AS B ON A.SIAPE=B.GR_MATRICULA;
    '''
    dados = sqlpandas(sql)

    if len(dados) > 0:
        dados.sort_values(['SERVIDOR', 'SIAPE'], inplace=True)

        salvarPandas(dados, 'SERVIDORES ANO-ANO')
        mensagemInformacao('Relatório dos servidores - ANO-ANO - criados com sucesso.')
    else:
        mensagemErro('Relatório dos servidores - ANO-ANO - criados com sucesso.')

