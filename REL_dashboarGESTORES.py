'''
GERADOR DE RELATÓRIO DOS SERVIDORES (DASHBOARD GESTORES)
'''

from SQL import sqlpandas
from MENSAGEM import mensagemInformacao, mensagemErro
from AUXILIAR import salvarPandas


def dashboardGestores():
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
        A.CD_FUNCAO AS 'FUNÇÃO',
        B.GR_MATRICULA	AS	SIAPE,
        B.IT_NO_SERVIDOR	AS	SERVIDOR,
        B.IDADE, 
        B.IT_CO_SEXO	AS	SEXO,
        B.DES_TITULACAO	AS	TITULAÇÃO,
        B.DES_ETNIA	AS	ETNIA,
        B.DES_REGIME_JURIDICO	AS	'REG JUR',
        B.IT_CO_JORNADA_TRABALHO as 'CARGA HORÁRIA',
        B.DES_CARREIRA	AS	CARREIRA,
        B.DES_CARGO	AS	CARGO,
        B.DES_GRUPO	AS	GRUPO,
        B.DES_UPAG	AS	UPAG
        FROM 
        ts_sis_chefias AS A
        JOIN tb_ser_rel AS B ON A.GR_MATRICULA = B.GR_MATRICULA'''


    dados = sqlpandas(sql)

    if len(dados) > 0:

        dados['IDADE'] = dados['IDADE'].apply(faixa)

        dados['TITULAÇÃO'] = dados['TITULAÇÃO'].replace(['10 DOUTORADO', '08 ESPECIALIZAÇÃO', '09 MESTRADO', '06 MEDIO',
                                                         '04 FUNDAMENTAL I', '05 FUNDAMENTAL', '07 SUPERIOR',
                                                         '07 ENSINO SUPERIOR', '10 PHD', '07 SUPERIOR-INCOMPLETO'],
                                                        ['DOUTORADO', 'ESPECIALIZAÇÃO', 'MESTRADO', 'ENSINO MÉDIO',
                                                         'ENSINO FUNDAMENTAL', 'ENSINO FUNDAMENTAL', 'ENSINO SUPERIOR',
                                                         'ENSINO SUPERIOR', 'DOUTORADO', 'ENSINO MÉDIO'])

        dados['GRUPO FUNÇÃO'] = dados['FUNÇÃO'].replace(
            ['FG-2', 'CD-2', 'FG-1', 'FG-3', 'FG-5', 'CD-3', 'SEM ÔNUS', 'FCC',
             'FG-4', 'CD-4', 'CD-1'],
            ['FG', 'CD', 'FG', 'FG', 'FG', 'CD', 'SEM ÔNUS', 'FCC',
             'FG', 'CD', 'CD'])

        dados['TOTAL'] = 1

        salvarPandas(dados, 'DAHSBOARD - GESTORES')
        mensagemInformacao('Relatório DAHSBOARD - GESTORES criado com sucesso.')
    else:
        mensagemErro('Relatório DAHSBOARD - GESTORES não foi criado.')

