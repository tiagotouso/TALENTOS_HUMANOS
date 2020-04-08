'''
GERADOR DE RELATÓRIO DOS SERVIDORES (DASHBOARD SERVIDORES)
'''

from SQL import sqlpandas
from MENSAGEM import mensagemInformacao, mensagemErro
from AUXILIAR import salvarPandas


def dashboardServidores():
    '''
    FUNÇÃO PARA CRIAR OS DASHDOARD
    ENTRA
        ENTRA NULL
    SAI
        PLANILHA COM OS DADOS PARA DASHBOARD
    '''


    def faixa(idade):
        if idade > 67:
            fx = '68-77'
        elif idade > 57:
            fx = '58-67'
        elif idade > 47:
            fx = '48-57'
        elif idade > 37:
            fx = '38-47'
        elif idade > 27:
            fx = '28-37'
        else:
            fx = '18-27'
        return fx

    sql = '''SELECT 
        GR_MATRICULA	AS	SIAPE,
        IT_NO_SERVIDOR	AS	SERVIDOR,
        IDADE, 
        IT_CO_SEXO	AS	SEXO,
        DES_TITULACAO	AS	TITULAÇÃO,
        DES_ETNIA	AS	ETNIA,
        DES_REGIME_JURIDICO	AS	'REG JUR',
        IT_CO_JORNADA_TRABALHO as 'CARGA HORÁRIA',
        DES_CARREIRA	AS	CARREIRA,
        DES_CARGO	AS	CARGO,
        DES_GRUPO	AS	GRUPO,
        DES_UPAG	AS	UPAG
        FROM tb_ser_rel
        where
        IT_DA_OCOR_EXCLUSAO_SERV is null
        and IT_DA_OCOR_INATIVIDADE_SERV is null
        and DES_CARREIRA in ('TÉCN', 'PROF 2º', 'PROF 3º');'''

    dados = sqlpandas(sql)

    if len(dados) > 0:
        dados['IDADE'] = dados['IDADE'].apply(faixa)

        dados['TITULAÇÃO'] = dados['TITULAÇÃO'].replace(['10 DOUTORADO', '08 ESPECIALIZAÇÃO', '09 MESTRADO', '06 MEDIO',
                                                         '04 FUNDAMENTAL I', '05 FUNDAMENTAL', '07 SUPERIOR',
                                                         '07 ENSINO SUPERIOR', '10 PHD', '07 SUPERIOR-INCOMPLETO'],
                                                        ['DOUTORADO', 'ESPECIALIZAÇÃO', 'MESTRADO', 'ENSINO MÉDIO',
                                                         'ENSINO FUNDAMENTAL', 'ENSINO FUNDAMENTAL', 'ENSINO SUPERIOR',
                                                         'ENSINO SUPERIOR', 'DOUTORADO', 'ENSINO MÉDIO'])
        dados['TOTAL'] = 1

        if len(dados) > 0:
            salvarPandas(dados, 'DAHSBOARD - SERVIDORES')
            mensagemInformacao('Relatório DAHSBOARD - SERVIDORES criado com sucesso.')
        else:
            mensagemErro('Relatório DAHSBOARD - SERVIDORES não foi criado.')

