'''
GERADOR DE RELATÓRIO DOS SERVIDORES (AGENTES PÚBLICOS)
'''

from SQL import sqlpandas
from MENSAGEM import mensagemInformacao, mensagemErro
from AUXILIAR import salvarPandas


def agentespublicos():
    '''
    FUNÇÃO PARA CRIAR OS AGENTES PÚBLICOS
    ENTRA
        NULL
    SAI
        PLANILHA DOS AGENTES PÚBLICOS DO MÊS
    '''

    sql = '''SELECT 
            a.IT_NO_SERVIDOR AS 'SERVIDOR',
            a.GR_MATRICULA AS 'SIAPE',
            a.DES_CARGO AS 'CARGO',
            b.CARGO AS 'FUNÇÃO',
            a.DES_LOTACAO AS 'LOTAÇÃO',
            A.IT_DA_OCOR_INGR_ORGAO_SERV AS 'DT EXERCÍCIO',
            a.IT_DA_PUBL_DIPL_INGR_ORGAO AS 'DT PUBLICAÇÃO',
            a.IT_CO_VAGA AS 'ATO NOMEAÇÃO',
            case
            when c.ORGAO <> '' then  c.orgao 
            ELSE 'UFTM'
            end  AS 'ÓRGÃO',
            a.DES_UPAG AS 'UPAG',
            a.DES_grupo AS 'GRUPO'
        FROM
            tb_ser_rel AS a 
            LEFT JOIN  ts_sis_chefias AS b ON a.GR_MATRICULA = b.GR_MATRICULA 
            LEFT JOIN  ts_sis_cedidos AS c ON a.gr_matricula = c.gr_matricula
        WHERE
            IT_DA_OCOR_EXCLUSAO_SERV IS NULL
            AND IT_DA_OCOR_INATIVIDADE_SERV IS NULL
            AND DES_CARREIRA IN ('TÉCN' , 'TÉCN-ESP', 'PROF 2º', 'PROF 3º')
        ORDER BY 1;'''


    dados = sqlpandas(sql)

    if len(dados) > 0:
        salvarPandas(dados, 'PUBLICAÇÕES - AGENTES PÚBLICOS')
        mensagemInformacao('Relatório dos AGENTES PÚBLICOS criado com sucesso.')
    else:
        mensagemErro('Relatório dos AGENTES PÚBLICOS não foi criado.')

