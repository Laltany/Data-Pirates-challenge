## Objetivo

Coletar dados referentes a registros de faixas de cep das UFs presentes no site dos correios (http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm), e salvá-las em formato jsonl.

# Bibliotecas utilizadas

Neste desafio foram utilizadas as bibliotecas:
  - Requests: para de realizar a requição da captura das UFs e dos registros.
  - Beautifulsoup: para realizar o parser do html
  - json: para a criação do arquivo em formato jsonl
  - sys: para capturar o argumento passado pelo usuário
  - uuid: para gerar IDs automaticos para cada registro

# Como rodar

Para rodar o código basta executar a seguinte linha de comando no seu terminal:

```
$ python neoway.py x
```

Onde x é igual a quantidade de UFs que você deseja coletar registros. Para o valor de x o código aceita minimamente o número 2, e no máximo o número 27. Visto que existem 27 UFs no Brasil e, de acordo com as regras do desafio, deve-se extrair no mínimo registros de 2 (duas) UFs.
    
# Desafios

Apesar de reconhecer que o parâmetro 'qtdrow' tem a capacidade de recuperar todas as informações em apenas 1 requisição para cada UF, não foi encontrado o valor necessário para a ação. Infelizmente sem obter sucesso, tentou-se valores como:
  - ALL
  - all
  - \*
  - **
  - (vazio)

## Solução

No parâmetro 'qtdrow', utilizou-se um número maior para abranger todos as regiões. Observa-se que não se obteve maleficio em utilizar tal abordagem, porém um novo valor esta sendo estudado para que se possa recuperar todas as informações, sem a necessidade da abordagem solução deste código. 


