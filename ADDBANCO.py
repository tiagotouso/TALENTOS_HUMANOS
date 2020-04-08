'''
ARQUIVO PARA CRIAR TABELAS DOC - END - REL E CAMPOS NO MYSQL

IMPORTANDO DADOS DA PASTA '_MYSQLBANCO' ARQUIVO '_BANCO_DOC_END_REL' COM AS CONFIGURAÇÕES
'''

import pandas as pd
from SQL import sqlexecute, sqlpesquisar, sqlpandas

from MENSAGEM import mensagemErro, mensagemInformacao

def cadastraConfigTabela():
    '''
    FUNÇÃO PARA CRIAR NO BANCO A TABELA DE CONFIGURAÇÃPO DO BANCO DE DADO
    ENTRA
        TABELA DE CONFIGURAÇÃO DO BANCO "_BANCO_DOC_END_REL.xlsx
    SAI
        TABELA CADASTRADA NO BANCO MYSQL "ts_sis__config_tabelas"
    '''

    # LÊ A PLANILHA COM OS DADOS
    dados = pd.read_excel('_MYSQLBANCO\_BANCO_DOC_END_REL.xlsx')

    dados.fillna('', inplace=True)

    # DELETA OS DADOS DA TABELA NO BANCO
    sql = 'delete from ts_sis__config_tabelas;'
    sqlexecute(sql)

    sql = ''
    for vl in dados.values:
        sql += "( {0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}'),\n".format(vl[0], vl[1], vl[2], vl[3], vl[4], vl[5], vl[6])
    sql = 'Insert into ts_sis__config_tabelas \nvalues\n' + sql[0:-2] + ';'
    sqlexecute(sql)

    mensagemInformacao('Tabela de configuração importada com sucesso.')


def backuptabela():
    txt = ''
    sql = 'show tables;'
    vl, tb = sqlpesquisar(sql)
    for vl in tb:
        sql = 'show create table '+vl[0]
        vl, tbii = sqlpesquisar(sql)
        txt += tbii[0][1] + '\n\n'

    arq = open('tabelas.txt', 'w')
    arq.write(txt)
    arq.close()


def addTabelaBanco():
    '''
    FUNÇÃO PARA CRIAR AS TABELAS DOC END REL NO BANCO DE DADOS CONFORME A TABELA E OS CAMPOS DEFINIDOS
    ENTRA
        PLANILHA _MYSQLBANCO _BANCO_DOC_END_REL.xlsx
    SAI
        TABELAS CRIADA NO BANCO
    '''

    # LÊ A PLANILHA COM OS DADOS
    #dados = pd.read_excel('_MYSQLBANCO\_BANCO_DOC_END_REL.xlsx')
    dados = sqlpandas('SELECT * FROM ts_sis__config_tabelas;')

    # CRIA A TABELA PARA QUARDAR OS SQL
    tbsql = []
    # ADD O SQL DA WIEW
    tbsql.append('drop view anoano;')
    tbsql.append('drop view anoanoc;')
    # ADD O SQL DA TABELA DOCUMENTOS
    tbsql.append('drop table tb_ser_doc;')
    sqltxt = ''
    # FILTRA A TABELA DOCUMENTOS E LOOP
    for vl in dados[dados['tabela'] == 'DOCUMENTOS'][['campo', 'tamanho']].values:
        sqltxt += ' {0} {1},\n'.format(vl[0], vl[1])
    sqltxt = sqltxt[1:-2]
    sqltxt = '''CREATE TABLE tb_ser_doc (\n''' + sqltxt + ');'
    tbsql.append(sqltxt)

    # ADD O SQL DA TABELA ENDEREÇO
    tbsql.append('drop table tb_ser_end;')
    sqltxt = ''
    # FILTRA A TABELA DOCUMENTOS E LOOP
    for vl in dados[dados['tabela'] == 'ENDERECOS'][['campo', 'tamanho']].values:
        sqltxt += ' {0} {1},\n'.format(vl[0], vl[1])
    sqltxt = sqltxt[1:-2]
    sqltxt = '''CREATE TABLE tb_ser_end (\n''' + sqltxt + ');'
    tbsql.append(sqltxt)

    # ADD O SQL DA TABELA RELACIONAMENTO
    tbsql.append('drop table tb_ser_rel;')
    sqltxt = ''
    # FILTRA A TABELA RELACIONAMENTO
    for vl in dados[dados['tb_relaciona'] == 'SIM'][['campo', 'tamanho']].values:
        sqltxt += ' {0} {1},\n'.format(vl[0], vl[1])
    sqltxt = sqltxt[1:-2]
    sqltxt = 'CREATE TABLE tb_ser_rel (\n''' + sqltxt + ');'
    tbsql.append(sqltxt)

    tbsql.append('''ALTER TABLE `talentoshumanos`.`tb_ser_doc` 
    CHANGE COLUMN `GR_MATRICULA` `GR_MATRICULA` CHAR(7) NOT NULL ,
    ADD PRIMARY KEY (`GR_MATRICULA`);''')

    tbsql.append('''ALTER TABLE `talentoshumanos`.`tb_ser_end` 
    CHANGE COLUMN `GR_MATRICULA_SERV_DISPONIVEL` `GR_MATRICULA_SERV_DISPONIVEL` CHAR(7) NOT NULL ,
    ADD PRIMARY KEY (`GR_MATRICULA_SERV_DISPONIVEL`);''')

    tbsql.append('''ALTER TABLE `talentoshumanos`.`tb_ser_rel` 
    CHANGE COLUMN `GR_MATRICULA` `GR_MATRICULA` CHAR(7) NOT NULL ,
    ADD PRIMARY KEY (`GR_MATRICULA`);''')


    for vl in tbsql:
        sqlexecute(vl)

    mensagemInformacao('Tabelas (tb_ser_doc, tb_ser_end, tb_ser_end) criado com sucesso.')


def addWiew():
    '''
    FUNÇÃO PARA CRIAR A WIEW ANO-ANO E ANO-ANO C
    ENTRA
        SQL COM A WIEW
    SAI
        WIEW CRIADA NO BANCO
    '''

    tbsql = []

    sql = '''CREATE 
        VIEW `anoano` AS
            SELECT 
                "T" AS `TRABALHANDO`,
                "ADM" AS `SITUACAO`,
                1 AS `VALOR`,
                YEAR(`tb_ser_rel`.`IT_DA_OCOR_INGR_ORGAO_SERV`) AS `ANO`,
                MONTH(`tb_ser_rel`.`IT_DA_OCOR_INGR_ORGAO_SERV`) AS `MES`,
                `tb_ser_rel`.`GR_MATRICULA` AS `SIAPE`
            FROM
                `tb_ser_rel`
            WHERE
                (ISNULL(`tb_ser_rel`.`IT_DA_OCOR_INATIVIDADE_SERV`)
                    AND ISNULL(`tb_ser_rel`.`IT_DA_OCOR_EXCLUSAO_SERV`)) 
            UNION SELECT 
                "NT" AS `NT`,
                "ADM" AS `ADM`,
                1 AS `1`,
                YEAR(`tb_ser_rel`.`IT_DA_OCOR_INGR_ORGAO_SERV`) AS `year(IT_DA_OCOR_INGR_ORGAO_SERV)`,
                MONTH(`tb_ser_rel`.`IT_DA_OCOR_INGR_ORGAO_SERV`) AS `month(IT_DA_OCOR_INGR_ORGAO_SERV)`,
                `tb_ser_rel`.`GR_MATRICULA` AS `GR_MATRICULA`
            FROM
                `tb_ser_rel`
            WHERE
                ((`tb_ser_rel`.`IT_DA_OCOR_INATIVIDADE_SERV` IS NOT NULL)
                    OR (`tb_ser_rel`.`IT_DA_OCOR_EXCLUSAO_SERV` IS NOT NULL)) 
            UNION SELECT 
                "NT" AS `NT`,
                "APO" AS `APO`,
                -(1) AS `-1`,
                YEAR(`tb_ser_rel`.`IT_DA_OCOR_INATIVIDADE_SERV`) AS `year(IT_DA_OCOR_INATIVIDADE_SERV)`,
                MONTH(`tb_ser_rel`.`IT_DA_OCOR_INATIVIDADE_SERV`) AS `month(IT_DA_OCOR_INATIVIDADE_SERV)`,
                `tb_ser_rel`.`GR_MATRICULA` AS `GR_MATRICULA`
            FROM
                `tb_ser_rel`
            WHERE
                (`tb_ser_rel`.`IT_DA_OCOR_INATIVIDADE_SERV` IS NOT NULL) 
            UNION SELECT 
                "NT" AS `NT`,
                "FAL" AS `FAL`,
                -(1) AS `-1`,
                YEAR(`tb_ser_rel`.`IT_DA_OCOR_EXCLUSAO_SERV`) AS `year(IT_DA_OCOR_EXCLUSAO_SERV)`,
                MONTH(`tb_ser_rel`.`IT_DA_OCOR_EXCLUSAO_SERV`) AS `month(IT_DA_OCOR_EXCLUSAO_SERV)`,
                `tb_ser_rel`.`GR_MATRICULA` AS `GR_MATRICULA`
            FROM
                `tb_ser_rel`
            WHERE
                ((`tb_ser_rel`.`IT_DA_OCOR_EXCLUSAO_SERV` IS NOT NULL)
                    AND (`tb_ser_rel`.`DES_EXCLUSAO` LIKE 'FALECI%')
                    AND ISNULL(`tb_ser_rel`.`IT_DA_OCOR_INATIVIDADE_SERV`)) 
            UNION SELECT 
                "NT" AS `NT`,
                "DES" AS `DES`,
                -(1) AS `-1`,
                YEAR(`tb_ser_rel`.`IT_DA_OCOR_EXCLUSAO_SERV`) AS `year(IT_DA_OCOR_EXCLUSAO_SERV)`,
                MONTH(`tb_ser_rel`.`IT_DA_OCOR_EXCLUSAO_SERV`) AS `month(IT_DA_OCOR_EXCLUSAO_SERV)`,
                `tb_ser_rel`.`GR_MATRICULA` AS `GR_MATRICULA`
            FROM
                `tb_ser_rel`
            WHERE
                ((`tb_ser_rel`.`IT_DA_OCOR_EXCLUSAO_SERV` IS NOT NULL)
                    AND ISNULL(`tb_ser_rel`.`IT_DA_OCOR_INATIVIDADE_SERV`)
                    AND (NOT ((`tb_ser_rel`.`DES_EXCLUSAO` LIKE 'FALECI%'))))'''


    tbsql.append(sql)


    sql = '''CREATE 

    VIEW `anoanoc` AS
        SELECT 
            `a`.`TRABALHANDO` AS `TRABALHANDO`,
            `a`.`SITUACAO` AS `SITUACAO`,
            `a`.`VALOR` AS `VALOR`,
            `a`.`ANO` AS `ANO`,
            `a`.`MES` AS `MES`,
            `a`.`SIAPE` AS `SIAPE`,
            `b`.`IT_NO_SERVIDOR` AS `SERVIDOR`,
            `b`.`IT_NU_CPF` AS `CPF`,
            `b`.`DES_ETNIA` AS `ETNIA`,
            `b`.`DES_NACIONALIDADE` AS `NACIONALIDADE`,
            `b`.`DES_REGIME_JURIDICO` AS `REG_JUR`,
            `b`.`DES_CARREIRA` AS `CARREIRA`,
            `b`.`DES_CARGO` AS `CARGO`,
            `b`.`DES_LOTACAO` AS `LOTACAO`,
            `b`.`DES_GRUPO` AS `GRUPO`,
            `b`.`DES_UPAG` AS `UPAG`,
            `b`.`IT_CO_JORNADA_TRABALHO` AS `CH`,
            `b`.`IT_DA_OCOR_INGR_SPUB_SERV` AS `DT_I_SP`,
            `b`.`IT_DA_OCOR_INGR_ORGAO_SERV` AS `DT_I_O`,
            `b`.`IT_DA_OCOR_INATIVIDADE_SERV` AS `DT_APO`,
            `b`.`IT_DA_OCOR_EXCLUSAO_SERV` AS `DT_DES`
        FROM
            (`anoano` `a`
            JOIN `tb_ser_rel` `b` ON ((`a`.`SIAPE` = `b`.`GR_MATRICULA`)))'''

    tbsql.append(sql)
    tbsql.append('commit;')

    for sql in tbsql:
        sqlexecute(sql)

    mensagemInformacao('Tabelas Wiew ANO-ANO - ANO-ANO-C criado com sucesso.')


#addTabelaBanco()
addWiew()

