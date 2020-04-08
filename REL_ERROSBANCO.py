'''
GERADOR DE RELATÓRIO DOS SERVIDORES (DADOS FALTANDO NO BANCO)
'''

from SQL import sqlpandas
from MENSAGEM import mensagemInformacao
from AUXILIAR import salvarPandas

def relatorioerrosistema():
    '''
    FUNÇÃO PARA VERIFICAR DADOS FALTANTES NO BANCO DE DADOS
    ENTRA
        SQL CONCULTA DOS SERVIDORES ATIVOS
    SAI
        PLANILHA DAS INFORMAÇÕES FALTANTE
    '''

    sql = '''select
            GR_MATRICULA	AS	'SIAPE',
            IT_NU_IDEN_SERV_ORIGEM	AS	'ID SERVIDOR',
            IT_NO_SERVIDOR	AS	'SERVIDOR',
            IT_NO_MAE	AS	'MÃE',
            IT_DA_NASCIMENTO	AS	'DT NASCIMENTO',
            IDADE	AS	'IDADE',
            IT_NU_CPF	AS	'CPF',
            IT_NU_PIS_PASEP	AS	'PIS',
            IT_SG_UF_UORG_EMISSAO	AS	'PIS UF',
            IT_CO_REGISTRO_GERAL	AS	'RG UF',
            IT_SG_ORGAO_EXPEDIDOR_IDEN	AS	'RG ÓRGÃO',
            IT_DA_EXPEDICAO_IDEN	AS	'RG DT',
            IT_SG_UF_IDEN	AS	'RG UF',
            EMAIL	AS	'E-MAIL',
            IT_CO_SEXO	AS	'SEXO',
            DES_ESTADO_CIVIL	AS	'ESTADO CIVIL',
            DES_ESCOLARIDADE	AS	'ESCOLARIDADE',
            DES_TITULACAO	AS	'TITULAÇÃO',
            DES_ETNIA	AS	'ETNIA',
            IT_SG_GRUPO_SANGUINEO	AS	'TIPO SANGUE',
            IT_SG_FATOR_RH	AS	'FATOR RH',
            IT_CO_BANCO_PGTO_SERVIDOR	AS	'BANCO',
            IT_CO_AGENCIA_BANCARIA_PGTO_SERV	AS	'AGÊNCIA',
            IT_NU_CCOR_PGTO_SERVIDOR	AS	'CONTA',
            IT_CO_TIPO_CONTA	AS	'TIPO CONTA',
            IT_NO_LOGRADOURO	AS	'ENDEREÇO',
            IT_NO_BAIRRO	AS	'BAIRRO',
            IT_NO_MUNICIPIO	AS	'CIDADE',
            IT_CO_CEP	AS	'CEP',
            IT_NU_ENDERECO	AS	'NÚMERO',
            IT_NU_COMPLEMENTO_ENDERECO	AS	'COMPLEMENTO',
            DES_NACIONALIDADE	AS	'NACIONALIDADE',
            DES_PAIS	AS	'PAÍS',
            DES_REGIME_JURIDICO	AS	'REG JUR',
            TEMPO_SERVICO	AS	'TEMPO SERVIÇO',
            DES_CARREIRA	AS	'CARREIRA',
            DES_CARGO	AS	'CARGO',
            DES_CLASSE	AS	'CLASSE',
            DES_LOTACAO	AS	'LOTAÇÃO',
            AMBIENTE	AS	'AMBIENTE',
            EXERCICIO	AS	'EXERCÍCIO',
            INSTITUTO	AS	'INSTITUTO',
            DEPARTAMENTO	AS	'DEPARTAMENTO',
            DES_GRUPO	AS	'GRUPO',
            DES_UPAG	AS	'UPAG',
            IT_DA_PUBL_DIPL_INGR_SPUB	AS	'DT PORTARIA NOMEAÇÃO',
			IT_DA_PUBL_DIPL_INGR_ORGAO	AS	'DT PORTARIA',
            IT_DA_OCOR_INGR_ORGAO_SERV	AS	'DT INGRESSO ÓRGÃO',
            DES_INGRESSO_SPUB	AS	'DESCRIÇÃO INGRESSO SP',
            IT_DA_OCOR_INGR_SPUB_SERV	AS	'DT INGRESSO SP',
            DES_INGRESSO_ORGAO	AS	'DESCRIÇÃO INGRESSO ÓRGÃO',
            IT_DA_OCOR_INATIVIDADE_SERV	AS	'DT INATIVIDADE',            
            DES_INATIVIDADE	AS	'DESCRIÇÃO INATIVIDADE',
            IT_DA_OCOR_EXCLUSAO_SERV	AS	'DESCRIÇÃO EXCLUSÃO',
            DES_EXCLUSAO	AS	'DT EXCLUSÃO',
        
            FLEXIBILIZADO	AS	'FLEXIBILIDADO'
            from
            tb_ser_rel
            where IT_DA_OCOR_EXCLUSAO_SERV is null
            and IT_DA_OCOR_INATIVIDADE_SERV is null
            and des_carreira in ('TÉCN', 'TÉCN-ESP', 'PROF 2º', 'PROF 3º');'''


    dados = sqlpandas(sql)
    if len(dados):
        lista = dados.isna().sum()
        for i in lista.items():
            if i[1] > 0 and i[0] not in ['DT EXCLUSÃO', 'DT INATIVIDADE', 'DT INGRESSO SP', 'DT PORTARIA', 'COMPLEMENTO', 'BAIRRO']:
                filtro = dados[dados[i[0]].isna()]
                salvarPandas(filtro, 'ERRO-DADOS FALTANDO - ' + str(i[0]), 'RELATORIOS DE ERRO\\')

        mensagemInformacao('Relatório de erro (DADOS FALTANDO) criado com sucesso.')

