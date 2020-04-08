
'''SCRIPT PARA CRIAR AS TABELAS PRINCIPAIS NO SISTEMA
ENTRA
    ARQUIVO TXT COM O NOME DO CAMPO, TIPO E NOME DA TABELA
SAI
    SQL COM DADOS DAS TABELA PARA CRIAR NO BANCO MYSQL
SAI'''


def salva(arquivo, nome):
    arq = open(nome, 'w')
    arq.write(arquivo)
    arq.close()

arq = open('CAMPOS.txt', 'r')
texto = arq.read()
arq.close()
tabela = []
for i in texto.split('\n'):
    a, b, c = i.split(';')
    tabela.append([a, b, c])
# CRIAR TABELA DOCUMENTOS
tbdoc = '''drop table tb_ser_doc;\n\n'''
tbdoc += '''CREATE TABLE tb_ser_doc (\n'''
for i in tabela:
    if i[2] == 'DOCUMENTOS':
        tbdoc += i[0] + ' ' + i[1] +',<q>'
tbdoc = tbdoc[:-4]
tbdoc = tbdoc.replace('<q>', '\n')
tbdoc += ');'
salva(tbdoc, '_DOCUMENTO.SQL')

# CRIAR TABELA ENDERECOS
tbdoc = '''drop table tb_ser_end;\n\n'''
tbdoc += '''CREATE TABLE tb_ser_end (\n'''
for i in tabela:
    if i[2] == 'ENDERECOS':
        tbdoc += i[0] + ' ' + i[1] +',<q>'
tbdoc = tbdoc[:-4]
tbdoc = tbdoc.replace('<q>', '\n')
tbdoc += ');'
salva(tbdoc, '_ENDERECOS.SQL')

# CRIAR TABELA RELACIONAMENTO
tbdoc = '''drop table tb_ser_rel;\n\n'''
tbdoc += '''CREATE TABLE tb_ser_rel (\n'''
for i in tabela:
    if i[0] != 'GR_MATRICULA_SERV_DISPONIVEL':
        tbdoc += i[0] + ' ' + i[1] +',<q>'
tbdoc = tbdoc[:-4]
tbdoc = tbdoc.replace('<q>', '\n')
tbdoc += ');'
salva(tbdoc, '_RELACIONAMENTO.SQL')

# INSERT INTO RELACIONAMENTO
tbdoc = '''delete from tb_ser_rel;\n\n'''
tbdoc += '''INSERT INTO tb_ser_rel (\n'''
for i in tabela:
    if i[2] in ['DOCUMENTOS','ENDERECOS']:
        if i[0] != 'GR_MATRICULA_SERV_DISPONIVEL':
            tbdoc += i[0] + ',<q>'
tbdoc = tbdoc[:-4]
tbdoc = tbdoc.replace('<q>', '\n')
tbdoc += ')\n'
tbdoc += '(Select \n'
aux = str()
for i in tabela:
    if i[2] == 'DOCUMENTOS':
        aux += 'a.' + i[0] + '<q>'
    elif i[2] =='ENDERECOS':
        if i[0] != 'GR_MATRICULA_SERV_DISPONIVEL':
            aux += 'b.' + i[0] + '<q>'
aux = aux[:-3]
aux = aux.replace('<q>', ',\n')
tbdoc += aux
tbdoc += '\nfrom tb_ser_doc a \n'
tbdoc += 'left join tb_ser_end b on a.GR_MATRICULA = b.GR_MATRICULA_SERV_DISPONIVEL);'
salva(tbdoc, '_INSERT RELACIONAMENTO.SQL')







