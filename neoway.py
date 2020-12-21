import requests
from bs4 import BeautifulSoup
import json
import sys
import uuid

class FAIXASCEP():

	def __init__(self, url_buscaufs, url_buscafaixas):
		self.url_buscaufs = url_buscaufs
		self.url_buscafaixas = url_buscafaixas
		self.ufs = []
		self.faixas = []

	def BuscaUFs(self):

		'''
			Realiza a captura das UFs na página de busca de faixas de cep
		'''

		request = requests.get(self.url_buscaufs)
		
		soup = BeautifulSoup(request.text, 'html.parser')

		select = soup.find('select')

		_ufs = list(select.stripped_strings)

		self.ufs = _ufs

	def BuscaInformacoes(self, uf):

		'''
			Realiza a busca das informações referentes as faixas de cep de determinadas UFs. 
			As informações mantidas são: id, uf da localidade, faixa de cep e tipo de faixa. 
		'''

		parametro = {
		'uf': uf,
		'qrdrow': 10000
		}

		request = requests.post(self.url_buscafaixas, parametro)

		soup = BeautifulSoup(request.text, 'html.parser')

		tables = soup.findAll("table", {'class':'tmptabela'})

		list_ = tables[1].findAll("tr")

		list_aux = []


		for item in list_[2:]:
			aux = item.stripped_strings
			aux = list(aux)
			_id = str(uuid.uuid4())
			list_aux.append({'id': _id, 'uf':uf, 'localidade': aux[0], 'faixa de cep': aux[1], 'tipo de faixa': aux[3]})


		return list_aux

	def remove_duplicados(self, lista_localidades):
		'''
			Tem como objetivo remover todas as duplicatas presentes na lista das informações 
		'''
		aux = []
		for localidade in lista_localidades:
			for faixa_cep in localidade:	
				if faixa_cep not in aux:
					aux.append(faixa_cep)
		return aux

	def salvar(self, lista):
		self.faixas = lista

	def SalvarJsonl(self):
		with open("data.jsonl", 'w', encoding='utf-8') as f:
		    for informação in self.faixas:		    		    	    	
	        	f.write(json.dumps(informação, ensure_ascii=False) + "\n")
			

def TransformaArgs(arg):
	try:
	    arg_ = int(arg)
	    return arg_
	except ValueError:
	    print("Você deve insirir um valor entre 2 e 27 como argumento.")
	    exit()


def ValidaArg(arg):
    if arg >= 2 and arg <= 27:
    	return True
    else:
    	return False


## argumento passado pelo usuário
args = sys.argv[1]
args = TransformaArgs(args)

##variaveis auxiliares
lista_localidades = []
sem_duplicatas = [] 

#parametros para capturar as ufs e realizar a busca
url_buscaufs = "http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm"
url_buscafaixascep = "http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm"

#criação e manipulação do objeto

faixas_de_cep = FAIXASCEP(url_buscaufs, url_buscafaixascep )

faixas_de_cep.BuscaUFs()

if ValidaArg(args):
	for uf in faixas_de_cep.ufs[:args]:
		lista_localidades.append(faixas_de_cep.BuscaInformacoes(uf))
	
	sem_duplicatas = faixas_de_cep.remove_duplicados(lista_localidades)
	faixas_de_cep.salvar(sem_duplicatas)
	faixas_de_cep.SalvarJsonl()	

else:
	print("Você deve inserir um valor entre 2 e 27.")

