import requests
from bs4 import BeautifulSoup
import json
import sys
import uuid


class content():

	def __init__(self, faixas_de_cep):
		self.faixas = faixas_de_cep

	def SalvarJsonl(self):
		with open("data.jsonl", 'w', encoding='utf-8') as f:
		    for informação in self.faixas:		    		    	    	
	        	f.write(json.dumps(informação, ensure_ascii=False) + "\n")
			

def getUFs(url):

	'''
		Realiza a captura das UFs na página de busca de faixas de cep
	'''

	request = requests.get(url)
	
	soup = BeautifulSoup(request.text, 'html.parser')

	select = soup.find('select')

	ufs = list(select.stripped_strings)

	return ufs


<<<<<<< HEAD
def getPage(uf, url):
=======
		parametro = {
		'uf': uf,
		'qrdrow': 1000
		}
>>>>>>> 5c73178d99dc1c4c255167de2a17921e8efc3d7b

	'''
		Realiza a busca das informações referentes as faixas de cep de determinadas UFs. 
		As informações mantidas são: id, uf da localidade, faixa de cep e tipo de faixa. 
	'''

	'''Localidade: **
		Bairro: 
		qtdrow: 50
		pagini: 51
		pagfim: 100'''

	parametro = {
	'uf': uf,
	'qtdrow': 1000
	}

	request = requests.post(url, parametro)

	page = BeautifulSoup(request.text, 'html.parser')

	return page


def remove_Infosduplicadas(InfofaixasCEP):
	'''
		Tem como objetivo remover todas as duplicatas presentes na lista das informações 
	'''
	sem_duplicatas = []
	for localidade in InfofaixasCEP:
		if localidade not in sem_duplicatas:
			sem_duplicatas.append(localidade)

	return sem_duplicatas


def Crawler(args, ufs, url):

	lista_InfofaixasCEP = []

	for uf in ufs[:args]:

		page = getPage(uf, url)

		tables = page.findAll("table", {'class':'tmptabela'})

		list_ = tables[1].findAll("tr")

		for item in list_[2:]:
			aux = item.stripped_strings
			aux = list(aux)
			_id = str(uuid.uuid4())
			lista_InfofaixasCEP.append({'id': _id, 'uf':uf, 'localidade': aux[0], 'faixa de cep': aux[1], 'tipo de faixa': aux[3]})


	InfofaixasCEP = remove_Infosduplicadas(lista_InfofaixasCEP)

	return content(InfofaixasCEP)



def ConvertToInt(arg):
	try:
	    arg_ = int(arg)
	    return arg_
	except ValueError:
	    print("Você deve insirir um valor entre 2 e 27 como argumento.")
	    exit()


### argumento passado pelo usuário, referente a quantidade de consultas que deve ser realizada
args = sys.argv[1]
args = ConvertToInt(args)

#parametros para capturar as ufs e realizar a busca
url_ufs_disponiveis = "http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm"
url_buscafaixascep = "http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm"

#criação e manipulação do objeto

ufs = getUFs(url_ufs_disponiveis)

if args >= 2 and args <= 27:
	content = Crawler(args, ufs, url_buscafaixascep)	
	content.SalvarJsonl()	
else:
	print("Você deve inserir um valor entre 2 e 27.")



