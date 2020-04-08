'''
GERADOR DE RELATÓRIO DOS SERVIDORES (SERVIDORES DEFICIENTES)
'''

from SQL import sqlpandas
from MENSAGEM import mensagemInformacao, mensagemErro
from AUXILIAR import salvarPandas


def arquivoservidoresdeficientes():
    '''
    FUNÇÃO PARA GERAR A LSITA DE SERVIDORES DEFICIENTES DA UFTM
    ENTRA
        NULL
    SAI
        LISTA DE SERVIDORES DEFICIENTES DA UFTM
    '''

    sql = '''SELECT 
            b.IT_DA_OCOR_EXCLUSAO_SERV as 'DT DELIGADO',
            b.IT_DA_OCOR_INATIVIDADE_SERV AS 'DT APOSENTADO',
            b.GR_MATRICULA as 'SIAPE',
            b.IT_NO_SERVIDOR AS 'SERVIDOR',
            b.IT_DA_NASCIMENTO AS 'DT NASCIMENTO',
            b.IT_CO_SEXO AS 'SEXO',
            b.DES_ESCOLARIDADE AS 'ESCOLARIDADE',
            b.DES_TITULACAO AS 'TITULAÇÃO',
            b.DES_CARREIRA AS 'CARREIRA',
            b.DES_CARGO AS 'CARGO',
            b.DES_LOTACAO AS 'LOTAÇÃO',
            b.AMBIENTE AS 'AMBIENTE',
            b.EXERCICIO AS 'EXERCÍCIO',
            b.INSTITUTO AS 'INSTITUTO',
            b.DEPARTAMENTO AS 'DEPARTAMENTOS',
            b.DES_GRUPO AS 'GRUPO',
            b.DES_UPAG AS 'UPAG',
            b.IT_CO_JORNADA_TRABALHO AS 'CH',
            a.tipo_deficiencia AS 'TIPO-COD', 
            a.COD_SIAPECAD
            FROM ts_sis_deficientes AS A
            JOIN tb_ser_rel AS B ON A.GR_MATRICULA = B.GR_MATRICULA
            ORDER BY 4;'''

    dados = sqlpandas(sql)
    if len(dados) > 0:
        salvarPandas(dados, 'SERVIDORES DEFICIENTES')
        mensagemInformacao('Relatório dos servidores deficientes criado com sucesso.')
    else:
        mensagemErro('Relatório dos servidores deficientes não foi criado.')

