'''
GERADOR DE RELATÓRIO DOS SERVIDORES (SERVIDORES ATIVOS NA DATA X)
'''

from SQL import sqlpandas
from MENSAGEM import mensagemInformacao, mensagemErro
from AUXILIAR import salvarPandas


def servidoresNaData():
    '''
    FUNÇÃO PARA VOLTAR EM UMA DETERMINADA DATA
    ENTRA
        DATA
    SAI
        PLANILHA (CSV) DOS SERVIDORES ATIVOS NA DATA
    '''

    data = input('Qual é a data')

    sql = '''select GR_MATRICULA, IT_NO_SERVIDOR, DES_CARREIRA, DES_CARGO, INSTITUTO, DES_GRUPO, IT_DA_OCOR_INGR_ORGAO_SERV, IT_DA_OCOR_INATIVIDADE_SERV, IT_DA_OCOR_EXCLUSAO_SERV
        from tb_ser_rel
        where DES_CARREIRA in ('PROF 3º', 'PROF 2º', 'TÉCN', 'TÉCN-ESP')
        AND GR_MATRICULA IN
        ( -- ATIVOS
        SELECT GR_MATRICULA
        FROM talentoshumanos.tb_ser_rel
        where IT_DA_OCOR_INGR_ORGAO_SERV <= '{0}'
        and IT_DA_OCOR_INATIVIDADE_SERV IS NULL
        and IT_DA_OCOR_EXCLUSAO_SERV IS NULL
        union
        
        -- APOSENTADO
        SELECT GR_MATRICULA
        FROM talentoshumanos.tb_ser_rel
        where IT_DA_OCOR_INGR_ORGAO_SERV <= '{0}'
        and IT_DA_OCOR_INATIVIDADE_SERV > '{0}'
        and IT_DA_OCOR_EXCLUSAO_SERV IS NULL
        UNION
        
        -- APOSENTADO - FALECIDO
        SELECT GR_MATRICULA
        FROM talentoshumanos.tb_ser_rel
        where IT_DA_OCOR_INGR_ORGAO_SERV <= '{0}'
        and IT_DA_OCOR_INATIVIDADE_SERV > '{0}'
        and IT_DA_OCOR_EXCLUSAO_SERV > '{0}'
        UNION
        
        -- DESLIGADOS
        SELECT GR_MATRICULA
        FROM talentoshumanos.tb_ser_rel
        where IT_DA_OCOR_INGR_ORGAO_SERV <= '{0}'
        and IT_DA_OCOR_INATIVIDADE_SERV IS NULL
        and IT_DA_OCOR_EXCLUSAO_SERV > '{0}' );'''.replace('{0}', data)


    dados = sqlpandas(sql)

    if len(dados) > 0:
        salvarPandas(dados, 'SERVIDORES NA DATA - {0}'.format(data))
        mensagemInformacao('Relatório dos Servidores na DAta criado com sucesso.')
    else:
        mensagemErro('Relatório dos Gestores não foi criado.')



servidoresNaData()


