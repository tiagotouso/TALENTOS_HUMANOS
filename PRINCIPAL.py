from datetime import datetime

from IMPORTEXTRATOR import documentos, enderecos
from SQL import sqlexecute
from SQLCOMANDOS import correcaodobanco

from IMPORTAMBIENTE import importarAmbienteServidores
from IMPORTCEDIDOS import ImportarServidoresCedidos
from IMPORTCHEFIAS import importarChefias
from IMPORTEMAIL import importarEmailServidor

from REL_ERROSBANCO import relatorioerrosistema
from REL_AGENTESPUBLICOS import agentespublicos
from REL_dashboarGESTORES import dashboardGestores
from REL_dashboarSERVIDORES import dashboardServidores
from REL_DOCENTESDEPARTAMENTOS import docentespordepartamentos
from REL_GESTORES import ServidoresGestores
from REL_SERVIDORES import arquivostodosnovos
from REL_SERVIDORESanoano import servidoresanoano
from REL_SERVIDORESdeficiente import arquivoservidoresdeficientes
from REL_SERVIDORESdoiscargos import ServidoresComDoisCargos
from REL_SERVIDORESqs import quandroServidores


data = datetime.now()

tbsql = '''delete from tb_ser_doc;
delete from tb_ser_end;'''.split('\n')

sql = documentos() #IMPORTAR DADOS DO EXTRATOR (DOCUMENTOS)
tbsql.append(sql)

sql = enderecos() #IMPORTAR DADOS DO EXTRATOR (ENDERECOS)
tbsql.append(sql)

tbsql.append('commit;')


for sql in tbsql: # LOOP PARA EXECUTAR TABELA DE SQL
    sqlexecute(sql)


# IMPORTAÇÕES
importarAmbienteServidores() # IMPORTAR DA PLANILHA OS AMBIENTE DOS SERVIDORES
ImportarServidoresCedidos() # IMPORTAR DO SIAPE OS CEDIDOS
importarChefias() # IMPORTAR A LISTA DE CHEFIA DA PLANILHA
importarEmailServidor() # IMPORTAR E-MAIL DO SERVIDORES DA PLANILHA



# CORREÇÕES
correcaodobanco() # SQL DE CORREÇÃO DO BANCO DE DADOS
relatorioerrosistema() # RELATÓRIO DE DADOS VAZIOS NO BANCO



# RELATÓRIOS
agentespublicos()
dashboardGestores()
dashboardServidores()
docentespordepartamentos()
ServidoresGestores()
arquivostodosnovos()
servidoresanoano()
arquivoservidoresdeficientes()
ServidoresComDoisCargos()
quandroServidores()


# CORREÇÕES
correcaodobanco() # SQL DE CORREÇÃO DO BANCO DE DADOS
#relatorioerrosistema() # RELATÓRIO DE DADOS VAZIOS NO BANCO


dataii = datetime.now()
print(data)
print(dataii)
print(dataii - data)



