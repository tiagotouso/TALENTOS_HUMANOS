'''
ARQUIVO PARA TRATAR OS DADOS DO EXTRATOR-SIAPE
'''

import os
import pandas as pd
import numpy as np
from SQL import sqlpandas

from MENSAGEM import mensagemErro, mensagemInformacao

caminhoEND = 'DADOS_EXTRATOR\\ENDERECOS'
caminhoDOC = 'DADOS_EXTRATOR\\DOCUMENTOS'

caminhoOUTROS = 'DADOS_EXTRATOR\\OUTROS'


def abrirtexto(arquivo):
    '''
    FUNÇÃO PARA ABRIR ARQUIVO TEXTO
    ENTRA
        ENTRA NOME E CAMINHO DO ARQUIVO TEXTO (TXT)
    SAI
        VARIÁVEL TEXTO (TXT) COM O ARQUIVO
    '''
    arq = open(arquivo, 'r', encoding='utf-8')
    txt = arq.read()
    arq.close()

    return txt


def arquivolocalizar(caminho, extensao):
    '''
    FUNÇAO PARA LISTAR OS ARQUIVOS DO DIRETÓRIO POR EXTENSÃO (NOME.EXTENSÃO)
    ENTRA
        ENTRA O CAMINHO (TXT) E A EXTENSÃO (TXT)
    SAI
        SAI A LISTA (LIST) COM O NOME DOS ARQUIVOS
    '''
    arquivos = os.listdir(caminho)
    lista = list()
    # LOOP NOS ARQUIVOS PARA PROCURAR AS EXTENSÃO
    for arquivo in arquivos:
        if arquivo[-3:] == extensao:
            lista.append(arquivo)

    return lista


def pegarLayout(caminho):
    '''
    FUNÇÃO PARA PEGAR AS CONFIGURAÇO ARQUIVO LAYOUT DA EXTRAÇÃO
    ENTRA
        CAMINHO (TXT) DA PASTA QUE CONTÉM O ARQUIVO LAYOUT
    SAI
        DICIONÁRIO (DIC) COM NOME DO CAMPO (TXT) E O TAMANHO (INT)
    '''
    # CRIAR O ARQUIVO LAYOUT PARA GUARDAR UM OU MAIS LAYOUT
    layout = []
    # CHAMA A FUNÇÃO PARA LISTAR ARQUIVOS (REF) DO DIRETÓRIO
    # LOOP DA VARIÁVEL ARQUIVOS DO DIRETÓRIO
    for vlar in arquivolocalizar(caminho, 'REF'):
        # ABRI O ARQUIVO REF
        arquivo = abrirtexto(caminho + '\\' + vlar)
        # QUEBRA O ARQUIVO EM LINHAS
        linhas = [ax.split() for ax in arquivo.split('\n')]

        # CRIA O DICIONÁRIO
        dic = {}
        # LOOP NO ARQUIVO LINHAS PARA POPULAR O DICIONÁRIO
        for linha in linhas:
            if len(linha) > 0:
                # PEGAR O CAMPO QUE CONTÉM VALOR NUMÉRICO
                campo = linha[2]
                # VERIFICA E RETIRA A VÍRGULA DO CAMPO
                if str(linha[2]).count(',') > 0:
                    a, b = str(linha[2]).split(',')
                    campo = int(a) + int(b)
                # INCLUI O VALOR NO CAMPO
                dic[linha[0]] = int(campo)
        # INCLUIR O DICIONÁRIO (DIC) NA LISTA (LIST)
        layout.append(dic)

    return layout


def pegarValores(caminho):
    '''
    FUNÇÃO PARA PEGAR OS DADOS DA EXTRAÇÃO
    ENTRA
        CAMINHO DA PASTA QUE CONTÉM O ARQUIVO DA EXTRAÇÃO
    SAI
        VARIÁVEL LISTA COM O ARQUIVO TEXTO QUEBRADO EM LINHAS
    '''
    # CRIAR O ARQUIVO DADOS PARA GUARDAR UM OU MAIS DADOS
    valores = []
    # CHAMA A FUNÇÃO PARA LISTAR ARQUIVOS (TXT) DO DIRETÓRIO
    # LOOP DA VARIÁVEL ARQUIVOS DO DIRETÓRIO
    for vlar in arquivolocalizar(caminho, 'TXT'):
        # ABRI O ARQUIVO TXT
        arquivo = abrirtexto(caminho + '\\' + vlar)
        # INCLUIR O ARQUIVO (TXT) COM QUEBRA DE LINHA  NA LISTA (LIST)
        valores.append(arquivo.split('\n'))

    return valores



def divisorlinha(indice, txt):
    '''
    FUNÇÃO PARA FATIADA A LINHA
    ENTRA
        LINHA (TXT) E O INDICE (LISTA NÚMERICA)
    SAI
        LISTA (LIST) DA LINHA FATIADA
    '''
    axlinha = []
    qtinicial = 0
    qtfinal = 0
    # LOOP NA VARIÁVEL INDICE PEGANDO O INÍCIO E FIM PARA FAZER O FATIAMENTO
    for vl in indice:
        qtfinal = vl + qtinicial
        # FATIA A LINHA E QUARDA A LISTA (LIST)
        axlinha.append(str(txt[qtinicial: qtfinal]).strip())
        qtinicial = qtfinal

    return axlinha



def layoutValorTabela(layout, valores):
    '''
    FUNÇÃO TRANSFORMAR O LAYOUT (DIC) E OS DADOS (TXT) EM TABELA (LIST)
    ENTRA
        LAYOUT (DIC) E VALORES (TXT)
    SAI
        TABELA (LIST) SEM O TITULO NAS COLUNAS
    '''
    # PEGA OS VALORES (INT) DO LAYOUT
    separador = list(layout.values())
    tb = []
    # LOOP NAS LINHAS ARQUIVO TXT (LIST)
    for linha in valores:
        if len(linha) > 0:
            # FATIAR AS LINHAS DO ARQUIVO CONFORME O LAYOUT
            axlinha = divisorlinha(separador, linha)
            tb.append(axlinha)

    return tb


def tabelaToPandas(tabela, titulo):
    '''
    FUNÇÃO PARA TRANSFORMAR TABELA (LIST) EM DADOS (DATAFRAME)
    ENTRA
        TABELA (LIST) E TITULO (LIST)
    SAI
        DADOS (DATAFRAME) TRANSFORMADO
    '''
    # SUBSTITUIR O "-" POR "_" NO TITULO DA TABELA (RESTRIÇÃO DO MYSQL)
    for num, vl in enumerate(titulo):
        titulo[num] = str(vl).replace('-', '_')

    # TRANSFORMAR A TABELA (LIST) EM VETOR (LIST)
    lista = []
    for vl in tabela:
        lista.append(vl)
    # TRANSFORMAR A LIST (LIST) EM ARRAY (NUMPY) E TRANSFORMAR ARRAY (NUMPY) EM DATAFRAME (DATAFRAME)
    dados = pd.DataFrame(np.array(lista).reshape(len(tabela), len(titulo)), columns=titulo)

    return dados


def pandasInsert(tabela, dados):
    '''
    FUNÇÃO PARA TRANSFORMAR DADOS (DATAFRAME) EM SQL (TXT)
    ENTRA
        NOME DA TABELA NO BANCO DE DADOS (TXT) E DADOS (DATAFRAME)
    SAI
        ARQUIVO (TXT) GRAVADO NO DISCO
    '''
    caminho = 'DADOS_EXTRATOR_TRATADO\\'
    txt = '''insert into {0}\nvalues\n'''.format(tabela)
    # LOOP NO DATAFRAME (DATAFRAME)
    for vl in dados.values:
        ax = list(vl)
        txt += '''({0}),\n'''.format(str(ax)[1:-1])
    txt = txt[0:-2] + ';'

    txt = txt.replace('\'NULL\'', 'NULL')

    arq = open(caminho + tabela + '.TXT', 'w', encoding='utf-8')
    arq.write(txt)
    arq.close()

    return txt

def pandasExport(narquivo, dados):
    '''
    FUNÇÃO PARA EXPORTAR DADOS (DATAFRAME) PARA ARQUIVO CSV (CSV)
    ENTRA
        NOME DO ARQUIVO (TXT) E DADOS (DATAFRAME)
    SAI
        ARQUIVO CSV (CSV) GRAVADO EM DISCO
    '''
    caminho = 'DADOS_EXTRATOR_TRATADO\\'
    dados.to_csv(caminho + narquivo + '.csv', sep='\t', encoding='utf-16')


def enderecos():
    '''
    FUNÇÃO PARA PEGAR O ARQUIVO DO EXTRATOR DE DADOS (ENDEREÇOS) E TRANSFORMAR PARA IMPORTAÇÃO NO BANCO MYSQL
    ENTRA
        NULL (OBS: OS ARQUIVOS DO EXTRATOR (TXT) E (REF) DEVERÃO ESTAR NA PASTA ENDERECOS)
    SAI
        ARQUIVO (TXT) E (CSV) PARA IMPORTAÇÃO NO BANCO DE DADOS
    '''

    dados = sqlpandas('''SELECT campo FROM talentoshumanos.ts_sis__config_tabelas
        where tabela = 'ENDERECOS';''')
    campos = list(dados['campo'])

    # PEGAR OS ARQUIVOS ENDEREÇO (TXT) E (REF)
    layoutEND = pegarLayout(caminhoEND)
    valoresEND = pegarValores(caminhoEND)

    if len(layoutEND) > 0:
        # LOOP NOS ARQUIVOS
        for numero in range(0, len(layoutEND)):
            # TRANSFORMA ARQUIVOS (TXT) EM TABELA (LIST)
            tb = layoutValorTabela(layoutEND[numero], valoresEND[numero])
            # PEGAR O NOME DOS CAMPOS
            titulo = list(layoutEND[numero].keys())
            # TRANSFORMAR TABELA (LIST) EM DADOS (DATAFRAME)
            dados = tabelaToPandas(tb, titulo)

        # FILTRA O DATAFRAME (DATAFRAME)
        dados = dados[campos]

        # CORRIGE A MATRÍCULA RETIRANDO O NÚMERO DO ÓRGÃO
        correcao = dados['GR_MATRICULA_SERV_DISPONIVEL'].apply(lambda x: x[5:])
        dados['GR_MATRICULA_SERV_DISPONIVEL'] = correcao

        # SALVA O SQL DOS DADOS
        sqltxt = pandasInsert('tb_ser_end', dados)

        # SALVA O CSV DOS DADOS
        pandasExport('Enderecos', dados)
        mensagemInformacao('Arquivo ENDEREÇO gerado.')

        return sqltxt
    else:
        mensagemErro('Arquivo ENDEREÇO não encontrado.')



def documentos():
    '''
    FUNÇÃO PARA PEGAR O ARQUIVO DO EXTRATOR DE DADOS (DOCUMENTOS) E TRANSFORMAR PARA IMPORTAÇÃO NO BANCO MYSQL
    ENTRA
        NULL (OBS: OS ARQUIVOS DO EXTRATOR (TXT) E (REF) DEVERÃO ESTAR NA PASTA DOCUMENTOS)
    SAI
        ARQUIVO (TXT) E (CSV) PARA IMPORTAÇÃO NO BANCO DE DADOS
    '''
    # CAMPOS QUE DEVERÃO TER NA TABELA

    dados = sqlpandas('''SELECT campo FROM talentoshumanos.ts_sis__config_tabelas
         where tabela = 'DOCUMENTOS';''')
    campos = list(dados['campo'])

    # PEGAR OS ARQUIVOS DOCUMENTOS (TXT) E (REF)
    layoutDOC = pegarLayout(caminhoDOC)
    valoresDOC = pegarValores(caminhoDOC)

    if len(layoutDOC) > 0:
        # LOOP NOS ARQUIVOS
        dadostodos = pd.DataFrame()
        for numero in range(0, len(layoutDOC)):
            # TRANSFORMA ARQUIVOS (TXT) EM TABELA (LIST)
            tb = layoutValorTabela(layoutDOC[numero], valoresDOC[numero])
            # PEGAR O NOME DOS CAMPOS
            titulo = list(layoutDOC[numero].keys())
            # TRANSFORMAR TABELA (LIST) EM DADOS (DATAFRAME)
            dados = tabelaToPandas(tb, titulo)
            # EXCLUIR O 'GR_MATRICULA' DAS TABELAS - POIS A PRIMEIRA TABELA JÁ TEM
            if numero > 0:
                dados = dados.drop(columns=['GR_MATRICULA'])
            # JUNTAR AS TABELAS (DATAFRAME) EM UM SÓ ARQUIVO
            dadostodos = pd.concat([dados, dadostodos], axis=1)

        # FILTRA O DATAFRAME (DATAFRAME)
        dadostodos = dadostodos[campos]

        # CORRIGE A MATRÍCULA RETIRANDO O NÚMERO DO ÓRGÃO
        correcao = dadostodos['GR_MATRICULA'].apply(lambda x: x[5:])
        dadostodos['GR_MATRICULA'] = correcao

        # CORRECAO CPF
        correcao = dadostodos['IT_NU_CPF'].apply(lambda x: x)
        dadostodos['IT_NU_CPF'] = correcao

        def validardata(data):
            if len(data) == 8 and data != '00000000':
                return data
            else:
                return 'NULL'

        # PROCURA E CORRIGE AS DATAS DO DATAFRAME(DATAFRAME) {'00000000' == ''}
        for coluna in dadostodos.columns:
            if coluna.count('_DA_') > 0:
                values = dadostodos[coluna].apply(lambda x: validardata(x))
                dadostodos[coluna] = values

        # SALVA O SQL DOS DADOS
        sqltxt = pandasInsert('tb_ser_doc', dadostodos)
        # SALVA O CSV DOS DADOS
        pandasExport('Documentos', dadostodos)
        mensagemInformacao('Arquivo DOCUMENTO gerado.')

        return sqltxt
    else:
        mensagemErro('Arquivo DOCUMENTO não encontrado.')


def arquivosExtrator():
    '''
    FUNÇÃO PARA PEGAR O ARQUIVO DO EXTRATOR DE DADOS E TRANSFORMAR PARA IMPORTAÇÃO NO BANCO MYSQL
    ENTRA
        NULL (OBS: OS ARQUIVOS DO EXTRATOR (TXT) E (REF) DEVERÃO ESTAR NA PASTA OUTROS)
    SAI
        ARQUIVO (TXT) E (CSV) PARA IMPORTAÇÃO NO BANCO DE DADOS
    '''

    # PEGAR OS ARQUIVOS DOCUMENTOS (TXT) E (REF)
    layoutOUTROS = pegarLayout(caminhoOUTROS)
    valoresOUTROS = pegarValores(caminhoOUTROS)

    if len(layoutOUTROS) > 0:
        # LOOP NOS ARQUIVOS
        dadostodos = pd.DataFrame()
        for numero in range(0, len(layoutOUTROS)):
            # TRANSFORMA ARQUIVOS (TXT) EM TABELA (LIST)
            tb = layoutValorTabela(layoutOUTROS[numero], valoresOUTROS[numero])
            # PEGAR O NOME DOS CAMPOS
            titulo = list(layoutOUTROS[numero].keys())
            # TRANSFORMAR TABELA (LIST) EM DADOS (DATAFRAME)
            dados = tabelaToPandas(tb, titulo)
            # EXCLUIR O 'GR_MATRICULA' DAS TABELAS - POIS A PRIMEIRA TABELA JÁ TEM
            if numero > 0:
                dados = dados.drop(columns=['GR_MATRICULA'])
            # JUNTAR AS TABELAS (DATAFRAME) EM UM SÓ ARQUIVO
            dadostodos = pd.concat([dados, dadostodos], axis=1)

        # PROCURA E CORRIGE AS DATAS DO DATAFRAME(DATAFRAME) {'00000000' == ''}
        for coluna in dadostodos.columns:
            if coluna.count('_DA_') > 0:
                values = dadostodos[coluna].apply(lambda x: '' if str(x) == '00000000' else x)
                dadostodos[coluna] = values

        # SALVA O SQL DOS DADOS
        pandasInsert('TB_OUTROS', dadostodos)
        # SALVA O CSV DOS DADOS
        pandasExport('OUTROS', dadostodos)
        mensagemInformacao('Arquivo OUTROS gerado.')
    else:
        mensagemErro('Arquivo OUTROS não encontrado.')

