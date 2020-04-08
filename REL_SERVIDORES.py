'''
GERADOR DE RELATÓRIO DOS SERVIDORES (ATIVOS - INATIVOS - DESLIGADOS)
'''

from SQL import sqlpandas
from MENSAGEM import mensagemInformacao, mensagemErro
from AUXILIAR import salvarPandas
from REL_SERVIDORES_sqlconsulta import sqlConsultaNova


def arquivostodosnovos():
    '''
    FUNÇÃO PARA AGRUPAR OS RELATÓRIOS GERADOS
    ENTRA
        NULL
    SAI
        ARQUIVOS GERADOS
    '''

    colunas = ['SIAPE',
               'SERVIDOR',
               'DT NASCIMENTO',
               'IDADE',
               'E-MAIL',
               'SEXO',
               'ESTADO CIVIL',
               'ESCOLARIDADE',
               'TITULAÇÃO',
               'ETNIA',
               'NACIONALIDADE',
               'NASC PAÍS',
               'REG JUR',
               'TEMPO SERVIÇO',
               'CARREIRA',
               'CARGO',
               'CLASSE',
               'LOTAÇÃO',
               'AMBIENTE',
               'EXERCÍCIO',
               'GRUPO',
               'UPAG',
               'CH',
               'DT INGRESSO ÓRGÃO SP',
               'DT INATIVIDADE',
               'DT EXCLUSÃO']

    sqlConsultaNova('SERVIDORES - ATIVOS - (TODOS)',
                    colunas,
                    'ATI', ['TÉCN', 'TÉCN-ESP', 'PROF 3º', 'PROF 2º'], [])

    sqlConsultaNova('SERVIDORES - ATIVOS - HC',
                    colunas,
                    'ATI', ['TÉCN', 'TÉCN-ESP', 'PROF 3º', 'PROF 2º'], ['HC'])

    sqlConsultaNova('SERVIDORES - ATIVOS - TÉCNICOS',
                    colunas,
                    'ATI', ['TÉCN', 'TÉCN-ESP'], [])

    sqlConsultaNova('SERVIDORES - ATIVOS - DOCENTES 2º',
                    colunas,
                    'ATI', ['PROF 2º'], [])

    sqlConsultaNova('SERVIDORES - ATIVOS - DOCENTES 3º',
                    colunas,
                    'ATI', ['PROF 3º'], [])

    sqlConsultaNova('SERVIDORES - (APOSENTADOS)',
                    colunas,
                    'APO', ['TÉCN', 'TÉCN-ESP', 'PROF 3º', 'PROF 2º'], [])

    sqlConsultaNova('SERVIDORES - (DESLIGADOS)',
                    colunas,
                    'DES', ['TÉCN', 'TÉCN-ESP', 'PROF 3º', 'PROF 2º'], [])

    ### CEFORES
    sqlConsultaNova('SERVIDORES - ATIVOS - (LOTAÇÃO {0}) - PROF 2º'.format('CEFORES'),
                    colunas,
                    'ATI', ['PROF 2º'], ['CEFORES'])

    sqlConsultaNova('SERVIDORES - ATIVOS - (LOTAÇÃO {0}) - TÉCNICOS'.format('CEFORES'),
                    colunas,
                    'ATI', ['TÉCN', 'TÉCN-ESP'], ['CEFORES'])

    ### INSTITUTOS E ITURAMA
    institutos = ['ICBN', 'ICENE', 'ICS', 'ICTE', 'IELAHS', 'ITURAMA']
    for it in institutos:
        sqlConsultaNova('SERVIDORES - ATIVOS - (LOTAÇÃO {0}) - PROF 3º'.format(str(it)),
                        colunas,
                        'ATI', ['PROF 3º'], [it])

    for it in institutos:
        sqlConsultaNova('SERVIDORES - ATIVOS - (LOTAÇÃO {0}) - TÉCNICOS'.format(str(it)),
                        colunas,
                        'ATI', ['TÉCN', 'TÉCN-ESP'], [it])

    mensagemInformacao('Relatório dos servidores - ATIVOS E INATIVOS - criados com sucesso.')

