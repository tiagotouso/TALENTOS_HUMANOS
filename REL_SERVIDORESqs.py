'''
GERADOR DE RELATÓRIO DOS SERVIDORES (SQ)
'''

from MENSAGEM import mensagemInformacao
from REL_SERVIDORES_sqlconsulta import sqlConsultaNova


def quandroServidores():
    '''
    FUNÇÃO PARA CRIAR O QUADRO DE SERVIDORES CSV (CSV)
    ENTRA
        NULL
    SAI
        PLANILHA QUADRO DE SERVIDORES CSV (CSV)
    '''

    ### GERAR NOVO QS
    colunas = '''SIAPE
    ID SERVIDOR
    SERVIDOR
    MÃE
    DT NASCIMENTO
    IDADE
    CPF
    PIS
    PIS UF
    RG
    RG ÓRGÃO
    RG DT
    RG UF
    E-MAIL
    SEXO
    ESTADO CIVIL
    ESCOLARIDADE
    TITULAÇÃO
    ETNIA
    CD-BANCO
    CD-AGÊNCIA
    CD-CONTA
    CD-TIPO CONTA
    ENDEREÇO
    END. BAIRRO
    END. CIDADE
    END. CEP
    END. NÚMERO
    END. COMPLEMENTO
    CD-PAÍS ENDEREÇO
    CD-NACIONALIDADE
    CD-REGIME JURÍDICO
    CD-REG JUR SIT
    REG JUR
    CD-CARREIRA
    CD-CARGO
    CARREIRA
    CARGO
    CD-CLASSE
    CD-CLASSE REFERÊNCIA
    CD-CLASSE PADRÃO
    CLASSE
    CD-CLASSE NÍVEL
    CÓDIGO VAGA
    CD-LOTAÇÃO
    LOTAÇÃO
    AMBIENTE
    EXERCÍCIO
    INSTITUTO
    DEPARTAMENTO
    GRUPO
    UPAG
    CH
    CD-UPAG
    DT PORTARIA NOMEAÇÃO
    DT INGRESSO ÓRGÃO SP
    CD-INGRESSO GRUPO SP
    CD-INGRESSO OCORRÊNCIA SP
    DESC INGRESSO SP
    DT INGRESSO SP
    DT PORTARIA NOMEAÇÃO ÓRGÃO
    CD-INGRESSO GRUPO ÓRGÃO
    CD-INGRESSO OCORRÊNCIA ÓRGÃO
    DESC INGRESSO ÓRGÃO
    PORTARIA NOMEAÇÃO NÚMERO
    CD-INATIVIDADE GRUPO
    CD-INATIVIDADE OCORRÊNCIA
    DESC INATIVIDADE
    DT INATIVIDADE
    CD-EXCLUSÃO GRUPO
    CD-EXCLUSÃO OCORRÊNCIA
    DESC EXCLUSAO
    DT EXCLUSÃO
    CD-GRUPO DEFICIÊNCIA FÍSICA
    CD-DEFICIÊNCIA FÍSICA'''
    colunas = colunas.replace('    ', '')
    colunas = colunas.split('\n')

    sqlConsultaNova('NOVO QS 2019',
                    colunas,
                    'TODOS', [], [], False)

    mensagemInformacao('Relatório QS - SERVIDORES criado com sucesso.')

