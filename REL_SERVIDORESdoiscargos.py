'''
GERADOR DE RELATÓRIO DOS SERVIDORES (SERVIDORES COM DOIS CARGOS)
'''

from SQL import sqlpandas
from MENSAGEM import mensagemInformacao, mensagemErro
from AUXILIAR import salvarPandas


def ServidoresComDoisCargos():
    '''
    FUNÇAO PARA GERAR A LISTA DE SERVIDORES COM DOIS CARGOS
    ENTRA
        NULL
    SAI
        LISTA DE SERVIDORES COM DOIS CARGOS ATIVOS
    '''

    sql = '''SELECT 
            GR_MATRICULA as SIAPE,
            IT_NO_SERVIDOR AS SERVIDOR,
            DES_CARREIRA AS CARREIRA,
            DES_CARGO AS CARGO, 
            DES_LOTACAO AS LOTAÇÃO,
            DES_GRUPo AS GRUPO
        FROM
            tb_ser_rel
        WHERE
            IT_NU_CPF IN (SELECT 
                    IT_NU_CPF
                FROM
                    tb_ser_rel
                WHERE
                    IT_DA_OCOR_EXCLUSAO_SERV IS NULL
                        AND IT_DA_OCOR_INATIVIDADE_SERV IS NULL
                        AND IT_NU_CPF IN (SELECT 
                            IT_NU_CPF
                        FROM
                            tb_ser_rel
                        WHERE
                            IT_DA_OCOR_EXCLUSAO_SERV IS NULL
                                AND IT_DA_OCOR_INATIVIDADE_SERV IS NULL
                                AND DES_CARREIRA in ('{0}')
                        GROUP BY 1)
                GROUP BY IT_NU_CPF
                HAVING COUNT(IT_NU_CPF) >= 2)
                AND IT_DA_OCOR_EXCLUSAO_SERV IS NULL
                AND IT_DA_OCOR_INATIVIDADE_SERV IS NULL
        ORDER BY 2'''

    cargos = ['TÉCN', 'PROF 2º', 'PROF 3º']

    for cargo in cargos:
        sqlii = sql
        sqlii = sqlii.format(str(cargo))

        dados = sqlpandas(sqlii)

        if len(dados) > 0:
            narquivo = ' SERVIDORES - ATIVOS - (COM 2 VÍNCULOS) - ' + cargo
            salvarPandas(dados, narquivo)

    sql = sql.format("""TÉCN', 'PROF 2º', 'PROF 3º""")

    dados = sqlpandas(sql)

    if len(dados) > 0:
        narquivo = ' SERVIDORES - ATIVOS - (COM 2 VÍNCULOS) - (TODOS)'
        salvarPandas(dados, narquivo)
        mensagemInformacao('Relatório dos Servidores com 2 vínculos criados com sucesso.')
    else:
        mensagemErro('Relatório dos Servidores com 2 vínculos não foi criados.')

