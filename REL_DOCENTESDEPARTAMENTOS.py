'''
GERADOR DE RELATÓRIO DOS SERVIDORES (DOCENTES POR DEPARTAMENTOS)
'''

from SQL import sqlpandas
from MENSAGEM import mensagemInformacao, mensagemErro
from AUXILIAR import salvarPandas

def docentespordepartamentos():
    '''
    FUNÇÃO PARA CRIAR OS DOCENTES POR DEPARTAMENTO
    ENTRA
        NULL
    SAI
        PLANLHA DOS DOCENTES POR DEPARTAMENTO DO MÊS
    '''

    sql = '''SELECT
    A.GR_MATRICULA AS 'SIAPE',
    A.IT_NO_SERVIDOR AS 'SERVIDOR',
    A.IT_CO_JORNADA_TRABALHO AS 'CH',
    A.DES_TITULACAO AS 'TITULAÇÃO',
    A.DES_LOTACAO AS 'LOTAÇÃO',
    A.INSTITUTO AS 'INSTITUTO',
    A.DEPARTAMENTO AS 'DEPARTAMENTO',
    A.DES_CARREIRA AS 'CARREIRA',
    A.DES_CARGO AS 'CARGO',
    A.DES_CLASSE AS 'CLASSE',
    A.DES_REGIME_JURIDICO AS 'REGIME JURÍDICO',
    b.CARGO AS 'FUNÇÃO'
    FROM
    tb_ser_rel AS A
    left join ts_sis_chefias as b on a.GR_MATRICULA = b.GR_MATRICULA
    WHERE IT_DA_OCOR_EXCLUSAO_SERV is null
    and IT_DA_OCOR_INATIVIDADE_SERV is null
    AND DES_CARREIRA = 'PROF 3º'
    order by SERVIDOR;
    '''

    dados = sqlpandas(sql)

    if len(dados) > 0:
        dados['TITULAÇÃO'] = dados['TITULAÇÃO'].apply(lambda x: x[3:])
        salvarPandas(dados, 'PUBLICAÇÕES - DOCENTES POR DEPARTAMENTO')
        mensagemInformacao('Relatório dos DOCENTES POR DEPARTAMENTO criado com sucesso.')
    else:
        mensagemErro('Relatório dos DOCENTES POR DEPARTAMENTO não foi criado.')

