'''
ARQUIVO PARA CORREÇÃO DO BANCO DE DADOS
'''

from SQL import sqlexecute, sqlpandas
from MENSAGEM import mensagemInformacao

def correcaodobanco():
    '''
    FUNÇÃO PARA CORRIGIR INFORMAÇÕES NO BANDO DE DADOS
    ENTRA
        ENTRA UM SQL COM A INSTRUÇÃO
    SAI
        BANCO DE DADOS ATUALIZADO
    '''
    sql = []

    # 001 DATA DA EXTRAÇÃO
    sql.append('''
                INSERT INTO  tb_dt_extracao (MATRICULA, DTEXTRACAO)
                select b.GR_MATRICULA, CURDATE() from tb_ser_doc as b
                where b.gr_matricula not in(
                SELECT a.MATRICULA from tb_dt_extracao as a);
                ''')


    # 002 CORRIGIR LOTAÇÃO DE STRING PARA NÚMERO
    sql.append('''update tb_ser_doc set IT_CO_UORG_LOTACAO_SERVIDOR = IT_CO_UORG_LOTACAO_SERVIDOR * 1;''')


    # 003 ADD LOCAÇÃO DOS SERVIDORES ATIVO NA TABELA HISTORICO DE LOCAÇÃO DOS APOSENTADOS
    sql.append('''insert into ts_sis__correcao_lot_aposentado
                (select a.GR_MATRICULA, a.IT_CO_UORG_LOTACAO_SERVIDOR  from tb_ser_rel as a
                where IT_DA_OCOR_INATIVIDADE_SERV is null
                and IT_DA_OCOR_EXCLUSAO_SERV is null
                and DES_CARREIRA in ('TÉCN', 'PROF 3º', 'PROF 2º'));''')


    # HISTORICO DO APOSENTADOS
    # 004 SERVIDOR APOSENTADO FICA LOTADO NO PRORH - GUARDAR A ÚLTIMA LOTAÇÃO E SALVAR EM UMA TABELA PARA FAZER ATUALIZAÇÃO
    sql.append('''
                DELETE FROM ts_sis__correcao_lot_aposentado AS A
                where A.GR_MATRICULA not in( SELECT b.GR_MATRICULA FROM tb_ser_doc as b
                WHERE concat(b.IT_SG_REGIME_JURIDICO, b.IT_CO_SITUACAO_SERVIDOR) in ('EST02', 'EST15')
                AND B.IT_DA_OCOR_INATIVIDADE_SERV IS NOT NULL);
                ''')


    ### CORREÇÕES EM DOCUMENTOS - INICIO
    # 005 CORREÇÕES NOS CARGOS - SERVIDORES SEM CARGO - ESTAGIÁRIOS - RESIDENTES
    sql.append('''
                update tb_ser_doc as a, ts_sis__correcao_cargo as b
                set
                a.IT_CO_GRUPO_CARGO_EMPREGO = b.IT_CO_GRUPO_CARGO_EMPREGO, 
                a.IT_CO_CARGO_EMPREGO = b.IT_CO_CARGO_EMPREGO
                where 
                a.GR_MATRICULA = b.GR_MATRICULA;
                ''')


    # 006 CORREÇÃO NA LOTAÇÃO DOS SERVIDORES APOSENTADOS
    sql.append('''
                UPDATE 
                tb_ser_doc AS A 
                INNER JOIN
                ts_sis__correcao_lot_aposentado AS B ON 
                A.GR_MATRICULA = B.GR_MATRICULA 
                SET A.IT_CO_UORG_LOTACAO_SERVIDOR = B.CD_LOTACAO;
                ''')


    # 007 CORREÇÃO NA LOTAÇÃO DOS RESITENDES DO HC
    sql.append('''
                UPDATE 
                tb_ser_doc as a
                SET 
                a.IT_CO_UORG_LOTACAO_SERVIDOR = '12'
                WHERE 
                a.IT_SG_REGIME_JURIDICO='MRD' 
                or a.IT_SG_REGIME_JURIDICO='RMP';
                ''')


    # 008 CORREÇÃO NO CARGO DO ESTAGIÁRIOS
    sql.append('''
                UPDATE 
                tb_ser_doc as a 
                SET 
                a.IT_CO_GRUPO_CARGO_EMPREGO = "999",
                a.IT_CO_CARGO_EMPREGO = "997"
                WHERE a.IT_SG_REGIME_JURIDICO="ETG";
                ''')


    # 009 CORREÇÃO NO CARGO DOS RESIDENTES
    sql.append('''
                UPDATE 
                tb_ser_doc as a
                SET 
                a.IT_CO_GRUPO_CARGO_EMPREGO = "999",
                a.IT_CO_CARGO_EMPREGO = "999"
                WHERE 
                a.IT_SG_REGIME_JURIDICO="MRD";
                ''')


    # 010 CORREÇÃO NO CARGO DOS RESIDENTES
    sql.append('''
                UPDATE 
                tb_ser_doc as a 
                SET 
                a.IT_CO_GRUPO_CARGO_EMPREGO = "999", 
                a.IT_CO_CARGO_EMPREGO = "998"
                WHERE a.IT_SG_REGIME_JURIDICO="RMP";
                ''')


    # 011 CORREÇÃO NA LOTAÇÃO DOS SERVIDORES - COLABORAÇÃO TÉCNICA - CARGO EM COMISSÃO
    sql.append('''
                UPDATE 
                tb_ser_doc AS A 
                INNER JOIN
                ts_sis__correcao_lot_outros AS B ON 
                A.GR_MATRICULA = B.GR_MATRICULA 
                SET 
                A.IT_CO_UORG_LOTACAO_SERVIDOR = B.CD_LOTACAO;
                ''')


    # 012 CORREÇÃO NA JORNADA DE TRABALHO DO PROFESSOR DE 40
    sql.append('''
                UPDATE 
                tb_ser_doc as a 
                SET
                a.IT_CO_JORNADA_TRABALHO = '40 DE'
                WHERE a.IT_CO_JORNADA_TRABALHO='99';
                ''')


    ### CORREÇÕES EM DOCUMENTOS - FIM

    ### CORRECOES RELACIONAMENTO - INÍCIO

    # 013 DELETAR TABELA RELACIONAMENTO
    sql.append('''delete from tb_ser_rel;''')


    ## 014 INCLUIR DADOS NA TABELA RELACIONAMENTO
    # CRIAR SQL INSERT TABELA TB_SER_END
    axsql = '''SELECT  tabela, campo FROM talentoshumanos.ts_sis__config_tabelas
        where tb_relaciona = 'SIM'
        AND TABELA != 'RELACIONA';'''

    dados = sqlpandas(axsql)
    axsql = 'INSERT INTO tb_ser_rel\n'
    campos = '(' + str(list(dados['campo']))[1:-1] + ')\n'
    campos = campos.replace('\'', '`')
    axsql += campos

    ax = 'select '
    dic = {'DOCUMENTOS': 'A.', 'ENDERECOS': 'B.'}
    for vl in dados.values:
        ax += '{0}{1}, '.format(dic[vl[0]], vl[1])
    ax = ax[0:-2]
    ax += ''' from tb_ser_doc as a, tb_ser_end as b
        where a.gr_matricula = b.GR_MATRICULA_SERV_DISPONIVEL'''
    ax = '( ' + ax + ' )'
    axsql += ax + ';'

    sql.append(axsql)


    # 015 ATUALIZAÇÃO DA CARREIRA DO PENSIONISTA
    sql.append('''
               UPDATE 
               tb_ser_rel AS A 
               SET 
               A.DES_CARREIRA = 'PEN'
               WHERE 
               concat(A.IT_SG_REGIME_JURIDICO, IT_CO_SITUACAO_SERVIDOR) = 'NES84';
               ''')


    # 016 ATUALIZAR A CARREIRA DOS SERVIDORES
    sql.append('''UPDATE TB_SER_REL AS A
            LEFT JOIN tp_cargos AS B ON concat(A.IT_CO_GRUPO_CARGO_EMPREGO, A.IT_CO_CARGO_EMPREGO) = B.cd_cargo_emprego
            SET A.DES_CARREIRA = B.DESC_CARREIRA;''')


    # 017 ATUALIZAÇÃO DA CARREIRA DO DOCENTE - ALUIZIO ROSA PRATA - PROFESSOR QUE NÃO TEM CARGO
    sql.append('''
               UPDATE 
               tb_ser_rel AS A 
               SET 
               A.DES_CARREIRA = 'PROF 3º'
               WHERE 
               concat(A.IT_SG_REGIME_JURIDICO,
               IT_CO_SITUACAO_SERVIDOR) = 'NES05' 
               AND A.GR_MATRICULA = '0389972';
               ''')


    # 018 ATUALIZAÇÃO DA CARREIRA DO SERVIDOR - IZILDINHA MARIA SILVA MUNHOZ - SAIU ANTES DE 94
    sql.append('''
               UPDATE 
               tb_ser_rel AS A SET 
               A.DES_CARREIRA = 'TÉCN'
               WHERE 
               concat(A.IT_SG_REGIME_JURIDICO,
               IT_CO_SITUACAO_SERVIDOR)='NES05'
               AND A.GR_MATRICULA = '2085597';
               ''')


    # 019 ATUALIZAÇÃO DA CARREIRA DO SERVIDOR - ANTONIO LUIZ VENEU JORDÃO - CARGO EM COMISSÃO - ESPIÃO DO BOZO
    sql.append('''
                UPDATE tb_ser_rel AS A 
                SET 
                    A.DES_CARREIRA = 'TÉCN-ESP'
                WHERE A.GR_MATRICULA = '3140616';
               ''')


    # 020 ATUALIZAR - RESIDENTE NÃO TEM OS DADOS
    sql.append('''
                update
                tb_ser_rel
                set
                DES_CLASSE = 'V.N.O. (RES)',
                EMAIL = 'V.N.O. (RES)',
                AMBIENTE = 'V.N.O. (RES)',
                EXERCICIO = 'V.N.O. (RES)'
                where
                DES_CARREIRA = 'RES';
                ''')


    # 021 ATUALIZAR - ESTAGIÁRIO NÃO TEM OS DADOS
    sql.append('''
                update
                tb_ser_rel
                set
                DES_CLASSE = 'V.N.O. (ETG)',
                EMAIL = 'V.N.O. (ETG)',
                AMBIENTE = 'V.N.O. (ETG)',
                EXERCICIO = 'V.N.O. (ETG)'
                where
                DES_CARREIRA = 'ETG';
                ''')


    # 022 ATUALIZAR - PENSIONISTA NÃO TEM OS DADOS
    sql.append('''
                update
                tb_ser_rel
                set
                DES_CLASSE = 'V.N.O. (PEN)',
                EMAIL = 'V.N.O. (PEN)',
                AMBIENTE = 'V.N.O. (PEN)',
                EXERCICIO = 'V.N.O. (PEN)'
                where
                DES_CARREIRA = 'PEN';
                ''')


    # 023 ATUALIZAÇÃO DA CARREIRA DO DOCENTE - HELENICE GOBBI - CARREIRA DE PROFESSOR
    sql.append('''
               UPDATE 
               tb_ser_rel AS A 
               SET 
               A.IT_CO_GRUPO_CARGO_EMPREGO = '705'
               WHERE A.GR_MATRICULA = '0315630';
               ''')


    # 024 ATUALIZAR E-MAIL INSTITUCIONAL DOS SERVIDORES
    sql.append('''
                update
                tb_ser_rel as a
                join ts_sis_email as b on a.IT_NU_CPF = B.CPF
                SET 
                a.EMAIL = b.EMAIL_INST;
                ''')


    # 025 ATUALIZAR AMBIENTE E EXERCÍCIOS DOS SERVIDORES
    sql.append('''
                update
                tb_ser_rel as a
                join ts_sis_ambientes as b on b.GR_MATRICULA = a.GR_MATRICULA
                SET
                a.AMBIENTE = b.AMBIENTE, 
                a.EXERCICIO = b.EXERCICIO;
                ''')


    # 026 ATUALIZAR ESTADO CIVIL DOS SERVIDORES
    sql.append('''
                update
                tb_ser_rel as a
                join tp_estado_civil as b on a.IT_CO_ESTADO_CIVIL = B.CD_ESTADO_CIVIL
                SET
                A.DES_ESTADO_CIVIL = DESC_ESTADO_CIVIL;
                ''')


    # 027 ATUALIZAR ESCOLARIDADE DOS SERVIDORES
    sql.append('''
                update 
                tb_ser_rel as a
                join tp_escolaridade as b on a.IT_CO_NIVEL_ESCOLARIDADE = b.CD_ESCOLARIDADE
                set
                a.DES_ESCOLARIDADE = b.DESC_ESCOLARIDADE;
                ''')


    # 028 ATUALIZAR TITULAÇÃO DOS SERVIDORES
    sql.append('''
                update 
                tb_ser_rel as a
                join tp_titulacao as b on a.IT_CO_TITULACAO_FORMACAO_RH = b.CD_TITULACAO
                set
                a.DES_TITULACAO = b.DESC_TITULACAO;
                ''')


    # 029 ATUALIZAR ETNIA DOS SERVIDORES
    sql.append('''
                update 
                tb_ser_rel as a
                join tp_cores as b on a.IT_CO_COR_ORIGEM_ETNICA = b.CD_COR
                set
                a.DES_ETNIA  = b.DESC_COR;
                ''')


    # 030 ATUALIZAR NACIONALIDADE DOS SERVIDORES
    sql.append('''
                update 
                tb_ser_rel as a
                join tp_nacionalidade as b on a.IT_CO_NACIONALIDADE  = b.IT_CO_NACIONALIDADE
                set
                a.DES_NACIONALIDADE  = b.NACIONALIDADE;
                ''')


    # 031 ATUALIZAR PAIS DOS SERVIDORES
    sql.append('''
                update
                tb_ser_rel a
                join tp_nacionalidade b on a.IT_CO_PAIS = b.IT_CO_NACIONALIDADE
                set
                a.DES_PAIS = b.NACIONALIDADE;
                ''')


    # 032 ATUALIZAR REGIME JURÍDICO DOS SERVIDORES
    sql.append('''
                update
                tb_ser_rel a
                join tp_reg_jur b on 
                concat(a.IT_SG_REGIME_JURIDICO, a.IT_CO_SITUACAO_SERVIDOR)= b.CD_JURIDICO_SITUACAO
                set
                a.DES_REGIME_JURIDICO = b.DESC_JURIDICO_SITUACAO;
                ''')


    # 033 ATUALIZAR CARGO DOS SERVIDORES
    sql.append('''
                update
                tb_ser_rel a
                join tp_cargos b on 
                concat(a.IT_CO_GRUPO_CARGO_EMPREGO
                , a.IT_CO_CARGO_EMPREGO
                )= b.CD_CARGO_EMPREGO
                set
                a.DES_CARGO = b.DESC_CARGO_EMPREGO;
                ''')


    # 034 ATUALIZAR LOTAÇÃO DOS SERVIDORES
    sql.append('''
                update
                tb_ser_rel a
                join tp_organograma b on 
                a.IT_CO_UORG_LOTACAO_SERVIDOR = b.CD_LOTACAO
                set
                a.DES_LOTACAO = b.DESC_LOTACAO;
                ''')


    # 035 ATUALIZAR DESCRIÇÃO DA INGRESSO NO ÓRGÃO DOS SERVIDORES
    sql.append('''
                update
                tb_ser_rel a
                join tp_ocorrencias b on 
                concat(a.IT_CO_GRUPO_OCOR_INGR_ORGAO, a.IT_CO_OCOR_INGR_ORGAO)= b.CD_GRUPO_EXCLUSAO
                set
                a.DES_INGRESSO_ORGAO = b.DESC_EXCLUSAO;
                ''')


    # 036 ATUALIZAR REGIME JURÍDICO DOS SERVIDORES CONCATENANDO DOIS CAMPOS
    sql.append('''update tb_ser_rel
                SET COD_REG_JUR = concat( IT_SG_REGIME_JURIDICO, IT_CO_SITUACAO_SERVIDOR);''')


    # 037 ATUALIZAR DESCRIÇÃO DA INCLUSÃO NO SERVIÇO PÚBLICO DOS SERVIDORES
    sql.append('''
                update
                tb_ser_rel a
                join tp_ocorrencias b on 
                concat(a.IT_CO_GRUPO_OCOR_INGR_SPUB, 
                a.IT_CO_OCOR_INGR_SPUB)= b.CD_GRUPO_EXCLUSAO
                set
                a.DES_INGRESSO_SPUB = b.DESC_EXCLUSAO;
                ''')


    # 038 ATUALIZAR DESCRIÇÃO DA INATIVIDADE DOS SERVIDORES
    sql.append('''
                update
                tb_ser_rel a
                join tp_ocorrencias b on 
                concat(a.IT_CO_GRUPO_OCOR_INATIVIDADE, 
                a.IT_CO_OCOR_INATIVIDADE)= b.CD_GRUPO_EXCLUSAO
                set
                a.DES_INATIVIDADE = b.DESC_EXCLUSAO;
                ''')


    # 039 ATUALIZAR DESCRIÇÃO DA EXCLUSÃO DOS SERVIDORES
    sql.append('''
                update
                tb_ser_rel a
                join tp_ocorrencias b on 
                concat(a.IT_CO_GRUPO_OCOR_EXCLUSAO, 
                a.IT_CO_OCOR_EXCLUSAO)= b.CD_GRUPO_EXCLUSAO
                set
                a.DES_EXCLUSAO = b.DESC_EXCLUSAO;
                ''')


    # 040 ATUALIZAR IDADE DOS SERVIDORES
    sql.append('''
                UPDATE tb_ser_rel 
                SET 
                IDADE =  ((YEAR(NOW()) * 12 + MONTH(NOW())) - (YEAR(IT_DA_NASCIMENTO) * 12 + MONTH(IT_DA_NASCIMENTO))) / 12;
                ''')

    # 041 ATUALIZAR TEMPO DE SERVIÇO DOS SERVIDORES
    sql.append('''
                UPDATE tb_ser_rel 
                SET 
                    TEMPO_SERVICO =  ((YEAR(NOW()) * 12 + MONTH(NOW())) - (YEAR(IT_DA_OCOR_INGR_ORGAO_SERV) * 12 + MONTH(IT_DA_OCOR_INGR_ORGAO_SERV)))/12
                where IT_DA_OCOR_INGR_ORGAO_SERV is not null;
                ''')


    # 042 ATUALIAR GRUPO E UPAG DOS SERVIDORES
    sql.append('''
                update
                tb_ser_rel a
                join tp_organograma AS b on a.IT_CO_UORG_LOTACAO_SERVIDOR = b.CD_LOTACAO
                SET
                a.DES_GRUPO = b.GRUPO,
                a.DES_UPAG = b.DESC_UPG;
                ''')


    # 043 ATUALIZAR AMBIENTE E EXERCÍCIO DOS DOCENTES 3º
    sql.append('''
                update
                tb_ser_rel
                set
                AMBIENTE = 'V.N.O. (PROF 3º)',
                EXERCICIO = 'V.N.O. (PROF 3º)'
                where
                DES_CARREIRA = 'PROF 3º';
                ''')


    # 044 ATUALIZAR AMBIENTE E EXERCÍCIO DOS DOCENTES 2º
    sql.append('''
                update
                tb_ser_rel
                set
                AMBIENTE = 'V.N.O. (PROF 2º)',
                EXERCICIO = 'V.N.O. (PROF 2º)'
                where
                DES_CARREIRA = 'PROF 2º';
                ''')


    # 045 ATUALIAR AMBIENTE E EXERCÍCIOS DOS SERVIDORES DO HC
    sql.append('''
                update
                tb_ser_rel
                set
                AMBIENTE = 'V.N.O. (HC)',
                EXERCICIO = 'V.N.O. (HC)'
                where
                DES_UPAG = 'HC';
                ''')


    # 046 ATUALIAR TITUÇÃO DOS SERVIDORES - NÃO TEM TITULAÇÃO, REPETE ESCOLARIDADE
    sql.append('''
                update
                tb_ser_rel
                set
                DES_TITULACAO = DES_ESCOLARIDADE
                where
                DES_TITULACAO is null;
                ''')


    # 047 ATUALIZAR CARREIRA DOS SERVIDORES EM SITUAÇÃO ESPECIAL - PROCURADOR E COLABORAÇÃO TÉCNICA
    sql.append('''
                UPDATE 
                tb_ser_rel AS A SET 
                A.DES_CARREIRA = 'TÉCN-ESP'
                WHERE 
                concat(A.IT_SG_REGIME_JURIDICO,
                IT_CO_SITUACAO_SERVIDOR) IN ('EST18', 'EST19', 'EST41');
                ''')


    # 048 ATUALIAR CLASSE DOS SERVIDORES
    sql.append('''
                update
                tb_ser_rel as a
                join tp_classes as b on 
                b.CD_CLASSE = a.IT_CO_CLASSE
                set
                a.DES_CLASSE = b.DESC_CLASSE;
                ''')


    # 049 EXCLUIR DA TABELA - CÓDIGO 02027 - ERRO DE CADASTRAMENTO OU DUPLICIDADE
    sql.append('''
                delete
                from tb_ser_rel
                where
                concat(IT_CO_GRUPO_OCOR_EXCLUSAO,IT_CO_OCOR_EXCLUSAO) = '02027';
                ''')


    # 050 ATUALIZAR DEPARTAMENTO/INSTITUTO DOS SERVIDORES TÉCNICOS
    sql.append('''
                update
                tb_ser_rel
                SET
                DEPARTAMENTO = concat('V.N.O. (', DES_CARREIRA , ')'),
                INSTITUTO = concat('V.N.O. (', DES_CARREIRA , ')')
                WHERE DES_CARREIRA <> 'PROF 3º'
                ''')


    # 051 ATUALIAR DEPARTAMENTOS DOS DOCENTES 3º
    sql.append('''
				update
                tb_ser_rel as a
                join ts_sis_departamentos_docentes as b on a.GR_MATRICULA=b.GR_MATRICULA
                SET
                a.DEPARTAMENTO = b.DEPARTAMENTO,
                a.INSTITUTO = B.INSTITUTO;
                ''')


    # 052 ATUALIAR CIDADE, ESTADO, NATURALIDADE DOS SERVIDORES
    sql.append('''
                #update tb_ser_rel as a
                #join ts_sis_naturalidade as b on a.it_nu_cpf = b.it_nu_cpf
                #set
                #a.DES_PAIS = b.PAIS,
                #a.ESTADO = b.ESTADO,
                #a.CIDADE = b.CIDADE;                ''')


    # 053 CORRIGIR NO BANCO DATA DE ANIVERSÁRIO DE QUEM NASCEU EM ANO BISSEXTO - ERRO NA MENSAGEM DE ANIVERSÁRIO
    sql.append('''
                update
                tb_ser_rel
                set
                IT_DA_NASCIMENTO = concat(year(IT_DA_NASCIMENTO), '-03-01')
                where
                concat( month(IT_DA_NASCIMENTO), '-', day(IT_DA_NASCIMENTO)) = '2-29';
                ''')


    # INCLUIR SIAPE NA TABELA DE SERVIDORES CEDIDOS DO MES
    # 054 TB IMPORTADA DO SIAPE
    sql.append('''UPDATE 
                ts_sis_cedidos as a 
                join tb_ser_rel as b on a.siapecad = b.IT_NU_IDEN_SERV_ORIGEM 
                SET
                a.GR_MATRICULA = b.gr_matricula;''')


    # 055 INCLUIR CEDIDO NA TB REL
    sql.append('''UPDATE tb_ser_rel AS A
                    JOIN
                ts_sis_cedidos AS B ON B.GR_MATRICULA = A.GR_MATRICULA 
            SET 
                A.CEDIDO_ORGAO = B.ORGAO,
                A.CEDIDO_DT = B.DT_I;''')


    # 056 COLOCAR OBSERVAÇÃO NOS PENSIONISTAS CADASTRADOS NO SIAPE
    sql.append('''UPDATE TB_SER_REL AS A
            SET A.OBS = 'PENSIONISTAS CASDASTRADOS NO SIAPE - PENSÃO JUDICIAL'
            WHERE A.IT_SG_REGIME_JURIDICO = 'NES' 
            AND A.IT_CO_SITUACAO_SERVIDOR = '84';''')


    # 057 COLOCAR PAIS DOS SERVIDORES BRASILEIROS
    sql.append('''update tb_ser_rel
                set des_pais = 'BRASIL'
                where des_nacionalidade = 'BRASILEIRO';''')


    ### CORRECOES RELACIONAMENTO - FIM

    contador = 1
    total = len(sql)
    for comando in sql:
        valor = round(contador * 100 / total)
        print(contador, valor, '%', '#' * valor)
        sqlexecute(comando)
        contador += 1

    mensagemInformacao('Correção no banco concluída.')

