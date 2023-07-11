# 1. Problema de negócio
A empresa Fome Zero é um marketplace de restaurantes. Ou seja, seu core business é facilitar o encontro e negociação de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas, e uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações. A principal tarefa é ajudar ao CEO da empresa Kleiton Guerra a identificar pontos chaves, respondendo às perguntas de negócio, explorando a base de dados fornecida.

O desafio do CEO que também foi recentemente contratado é entender melhor o negócio para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a empresa, e para isso, ele precisa que seja feita uma análise dos dados da empresa e que sejam gerados dashboards, a partir desta análise, para responder as seguintes perguntas: 

## Geral: 
1. Quantos restaurantes únicos estão registrados? 
2. Quantos países únicos estão registrados? 
3. Quantas cidades únicas estão registradas? 
4. Qual o total de avaliações feitas? 
5. Qual o total de tipos de culinária registrados?

## Pais:
1. Qual o nome do país que possui mais cidades registradas? 
2. Qual o nome do país que possui mais restaurantes registrados? 
3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados? 
4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos? 
5. Qual o nome do país que possui a maior quantidade de avaliações feitas? 
6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega? 
7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas? 8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada? 
9. Qual o nome do país que possui, na média, a maior nota média registrada? 
10. Qual o nome do país que possui, na média, a menor nota média registrada? 
11. Qual a média de preço de um prato para dois por país?

## Cidade: 
1. Qual o nome da cidade que possui mais restaurantes registrados? 
2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4? 
3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5? 
4. Qual o nome da cidade que possui o maior valor médio de um prato para dois? 
5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas? 
6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?
7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas?
8. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?

## Restaurantes: 
1. Qual o nome do restaurante que possui a maior quantidade de avaliações? 
2. Qual o nome do restaurante com a maior nota média? 
3. Qual o nome do restaurante que possui o maior valor de uma prato para duas pessoas? 
4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação? 
5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação? 
6. Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas? 
7. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas? 
8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)?

## Tipos de Culinária: 
1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação? 
2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação? 
3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação? 
4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a menor média de avaliação? 
5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a maior média de avaliação? 
6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a menor média de avaliação? 
7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a maior média de avaliação? 
8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a menor média de avaliação? 
9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a maior média de avaliação? 
10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a menor média de avaliação? 
11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas pessoas? 
12. Qual o tipo de culinária que possui a maior nota média? 
13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas?


# 2. Premissas assumidas para a análise
1. Marketplace foi o modelo de negócio assumido.
2. As 5 principais visões do negócio foram: 
      Visão Geral, 
      Visão por País, 
      Visão por Cidades, 
      Visão por Restaurantes, e 
      Visão por Culinária.
3. A análise foi realizada a partir de um DataFrame originariamente com 21 colunas e 7527 linhas.
4. Foram feitas as seguintes transformações no DataFrame:
	Remoção de linhas duplicadas,
Foram excluídas todas as linhas com informações faltantes (NaN).
	Inserção da coluna “contry_mane” com base em seus códigos,
	Inserção da coluna “price_name” com base em seus códigos,
	Inserção da coluna “color_name” com base em seus códigos, e
Foi atribuído a todos os restaurantes somente um tipo de culinária (A primeira cadastrada)
5. Como critério de desempate para a análise de País foi usada ordem alfabética.
6. Como critério de desempate para a análise de cidades foi usada ordem alfabética. 
7. Como critério de desempate para análise de restaurantes, foi usado o número de identificação do restaurante. (Menor o id mais qualificado).

# 3. Estratégia da solução
O painel estratégico foi desenvolvido utilizando as métricas que refletem as 5 principais visões do modelo de negócio da empresa:
1. Visão Geral, 
2. Visão por País, 
3. Visão por Cidades, 
4. Visão por Restaurantes, e 
5. Visão por Culinária


Cada visão é representada pelo seguinte conjunto de métricas:
### 1. Visão Geral
#### KPIs
a. Número de restaurantes cadastrados,
b. Número de países cadastrados,
c. Número de cidades cadastradas,
d. Número de avaliações feitas, e 
e. Número distintos de culinárias cadastradas
- Engloba todos os dados fornecidos 

#### Mapa
a. Mapa com a localização de todos os restaurantes cadastrados
- É possível filtrar os países apresentados no mapa
- Os restaurantes são agrupados conforme o zoom aplicado ao mapa.

### 2. Visão por País
Esta Visão é dividida em duas partes:
#### Gráficos
a. Quantidade de restaurantes cadastrados por país,
b. Quantidade de cidades registrada por país,
c. Quantidade de avaliações feitas por país, e
d. Média no preço do prato para dois por país. 
- Além do gráfico é possível consultar a tabela que gerou a informação e alterar seu     ordenamento. 
- É possível filtrar os países apresentados nos gráficos

#### Indicadores
Nestes indicadores são respondidas as questões colocadas pelo CEO.
a. Qual o nome do país que possui mais cidades registradas? 
b. Qual o nome do país que possui mais restaurantes registrados? 
c. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados? 
d. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos? 
e. Qual o nome do país que possui a maior quantidade de avaliações feitas? 
f. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega? 
g. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas? h. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada? 
h. Qual o nome do país que possui, na média, a maior nota média registrada? 
i. Qual o nome do país que possui, na média, a menor nota média registrada? 
j. Qual a média de preço de um prato para dois por país?
- É possível filtrar os países apresentados nos gráficos


### 3. Visão por Cidades
#### Gráficos / Tabelas
Nestes gráficos são respondidas as questões colocadas pelo CEO.
a. Qual o nome da cidade que possui mais restaurantes registrados? 
b. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4? 
c. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5? 
d. Qual o nome da cidade que possui o maior valor médio de um prato para dois? 
e. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas? 
f. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?
g. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas?
h. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?
- É possível filtrar os países apresentados nos gráficos
- Os gráficos podem se apresentados, com as 10 primeiras cidades ordenadas pelo critério de pesquisa, ou somente por aquelas que atenderam ao critério da pesquisa. As tabelas são apresentadas segundo este último critério.

### 4. Visão por Restaurantes
#### Cinco melhores culinárias e o seu principal restaurante
Estão disponíveis dois critérios de avaliação para definir a melhor culinária: Pela média das avaliações entre as categorias culinárias, e pelo número de restaurantes cadastrados por categoria culinária.

#### KPIs
Nestes indicadores são respondidas as questões colocadas pelo CEO.
a. Qual o nome do restaurante que possui a maior quantidade de avaliações? 
b. Qual o nome do restaurante com a maior nota média? 
c. Qual o nome do restaurante que possui o maior valor de uma prato para duas pessoas? 
d. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação? 
e. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação? 
f. Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas? 
g. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas? 
h. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)?
	- Nesta visão é possível utilizar três filtros:
		Filtrar por país,
      		Filtrar por culinária
		Escolher a quantidade de restaurantes que serão exibidos nas tabelas


### 5. Visão por Culinária
Foram criados três formulários para responder as questões 1 a 12, feitas pelo CEO, ficando assim possível consultar todas as opções culinárias, preços e avaliações, classificando pela menor ou maior delas.
	- É possível filtrar os países apresentados nos formulários.


# 4. Top 3 Insights de dados
1. A empresa Fome Zero está presente em 15 países, porém a Índia e os Estados Unidos da América, concentram 64,7% dos restaurantes cadastrados. Indicando que a distribuição regional por país da empresa está desbalanceada. 

2. Das 125 cidades cadastradas existem 53 delas estão empatadas com o número de restaurantes cadastrados, indicando neste ponto uma melhor distribuição da atuação da empresa por cidade.

3. Dos 6.929 restaurantes cadastrados, 5.681 pertencem aos 20% das culinárias mais significativas, muito próximo a proporção 80/20 proposta pelo Princípio de Pareto.

# 5. O produto do projeto
Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet.
O painel pode ser acessado através desse link: https://fomezero-1.streamlit.app/

# 6. Conclusão
O objetivo desse projeto é criar, dos dados apresentados, um conjunto de gráficos e tabelas que respondam as questões colocadas pelo CEO da melhor forma possível. Como não há datas no DataFrame, fica impossível fazer qualquer análise temporal do desempenho da empresa.

# 7. Próximo passos
1. Receber o retorno do CEO com a confirmação se conseguiu as respostas desejadas,
2. Rever o projeto apresentado e procurar aprimorar as soluções apresentadas,
3. Verificar a possibilidade de a fazer análises temporais dos dados, e
4. Verificar a possibilidade da inclusão de valores de faturamento no DataFrame para melhor qualificar as segmentações de mercado.

