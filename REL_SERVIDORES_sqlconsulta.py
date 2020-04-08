'''
GERADOR DE RELATÓRIO MODELO PARA CONSULTAR A TABELA TB_SER_REL
'''

from SQL import sqlpandas
from AUXILIAR import salvarPandas

def sqlConsultaNova(narquivo, colunas, tipo, carreira, grupo, renomear=True):
    '''
    FUNÇÃO MODELO PARA CONSULTAR A TABELA TB_SER_REL
           CRIAR CONSULTA SQL E SALVAR ARQUIVO NA PASTA DE RELATÓRIOS - PADRÃO PARA GERAR SQL DE CONSULTA DO SISTEMA DE RELATÓRIO
    ENTRA
        NOME DA CONSULTA  PARA SALVAR O ARQUIVO GERADO
        CAMPOS, PARAMETROS ([ATIVOS, APOSENTADOS, DESLIGADOS, TODOS],
        [TÉCN, TÉCN-ESP, PROF 3º, PROF 2º, OUTROS])PARA CONSULTA SQL
    SAI
        TABELA EM CSV DA CONSULTA REALIZADA
    '''

    # PEGAR OS NOMES DOS CAMPOS NA TABELA TS_SIS__CONFIG_TABELAS
    sql = '''SELECT CAMPO, AS_NOME FROM talentoshumanos.ts_sis__config_tabelas;'''
    dados = sqlpandas(sql)
    oldcampo = list(dados['CAMPO'])
    newcampo = list(dados['AS_NOME'])


    #MONTAR DICIONÁRIO COM OS CAMPOS DA TABELA (MAIS OS NOMES PARA EXIBIÇÃO)
    diccampos = {}

    for n, v in enumerate(newcampo):
        if str(v).strip() != '-':
            diccampos[str(v).strip()] = str(oldcampo[n]).strip()
    titulo = colunas
    #MONTAR SQL PARA CONSULTA
    sql = '''select {0} from tb_ser_rel'''
    if renomear == False: #SQL SEM RENOMEAR OS CAMPOS
        ax = []
        for coluna in colunas:
            ax.append(diccampos[coluna])
        titulo = ax
    else: #SQL RENOMEANDO OS CAMPOS
        ax = []
        for coluna in colunas:
            ax.append(diccampos[coluna] + ' AS \'' + coluna + '\'')
    axtx = ', '.join(ax)
    sql = sql.format(axtx)

    #FILTRO NA ATIVIDADE
    where = ''''''
    if tipo == 'ATI':
        where = '''\nwhere IT_DA_OCOR_INGR_ORGAO_SERV is not null
        and IT_DA_OCOR_INATIVIDADE_SERV is null
        and IT_DA_OCOR_EXCLUSAO_SERV is null'''
    elif tipo == 'APO':
        where = '''\nwhere IT_DA_OCOR_INGR_ORGAO_SERV is not null
        and IT_DA_OCOR_INATIVIDADE_SERV is not null
        and IT_DA_OCOR_EXCLUSAO_SERV is null'''
    elif tipo == 'DES':
        where = '''\nwhere IT_DA_OCOR_INGR_ORGAO_SERV is not null
        and IT_DA_OCOR_EXCLUSAO_SERV is not null'''
    elif tipo == 'TODOS':
        where = '''\nwhere IT_DA_OCOR_INGR_ORGAO_SERV is not null'''
    sql = sql + where

    #FILTRO NA CARREIRA
    if len(carreira) != 0:
        wherecarreira = ''
        axcarreira = ''
        if len(carreira) > 1:
            axcarreira = '\', \''.join(carreira)
            axcarreira = '\'' + axcarreira + '\''
        else:
            axcarreira = '\'' + carreira[0] + '\''
        wherecarreira = '''\nand DES_CARREIRA in ({0})'''.format(axcarreira)
        sql = sql + wherecarreira

    #FILTRO NO GRUPO
    if len(grupo) > 0:
        axgrupo = '\', \''.join(grupo)
        axgrupo = '\'' + axgrupo + '\''
        sqlgrupo = '''\nand DES_GRUPO in ({0})'''.format(axgrupo)
        sql = sql + sqlgrupo

    #SALVAR TABELA GERADA

    dados = sqlpandas(sql)

    if len(dados) > 0:
        salvarPandas(dados, narquivo)