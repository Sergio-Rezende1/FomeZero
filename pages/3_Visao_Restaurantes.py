# importando libraries
import plotly.express as px
import plotly.graph_objects as go
from haversine import haversine

# Bibliotecas necessárias
import pandas as pd
import streamlit as st
import numpy as np
import datetime as dt
from PIL import Image
import folium
from streamlit_folium import folium_static
import inflection

st.set_page_config( page_title='Fome Zero - Restaurantes', page_icon='✅', layout='wide')

# Funções


def ordena_rest_culinaria (culinaria, nota):
    """
    Função para classificar os restaurantes por tipo de culinária e nota.
    usa como critério de desempate a restaurante com menor 'restaurant_id'

    culinaria -> tipo de culinaria
    nota -> 'maior' ou 'menor'
    """
    if nota == 'maior':
        # Ordena o DataFrame por ordem decrescente de avaliações
        aux = df1.loc[:, ['restaurant_id', 'restaurant_name', 'cuisines', 'aggregate_rating']].sort_values('aggregate_rating',ascending=False)
        # Seleciona somente os restaurantes com a culinária solicitada
        seleciona_linhas = aux.loc[:, 'cuisines'] == culinaria
        aux1 = aux.loc[seleciona_linhas, ['restaurant_id', 'restaurant_name', 'cuisines', 'aggregate_rating']]
        # atribui a variavel a nota máxima entre os restaurantes italianos
        maximo = aux1.iloc[0,3]
        # Seleciona os restautantes com nota igual a máxima
        seleciona_linhas = aux1.loc[:, 'aggregate_rating'] == maximo
        # Ordena o dataframe por ordem crescente de ID
        aux2 = aux1.loc[seleciona_linhas, ['restaurant_id', 'restaurant_name', 'cuisines', 'aggregate_rating']].sort_values('restaurant_id', ascending=True)
        # Atribui a variavel o nome do restaurante de cozinha que atende as espectativas acima
        nome_restaurante = aux2.iloc[0, 1]
    else:
        # Ordena o DataFrame por ordem crescente de avaliações
        aux = df1.loc[:, ['restaurant_id', 'restaurant_name', 'cuisines', 'aggregate_rating']].sort_values('aggregate_rating',ascending=True)
        seleciona_linhas = aux.loc[:, 'cuisines'] == culinaria
        aux1 = aux.loc[seleciona_linhas, ['restaurant_id', 'restaurant_name', 'cuisines', 'aggregate_rating']]
        # atribui a variavel a nota minima entre os restaurantes italianos
        maximo = aux1.iloc[0,3]
        # Seleciona os restautantes com nota igual a minima
        seleciona_linhas = aux1.loc[:, 'aggregate_rating'] == maximo
        aux2 = aux1.loc[seleciona_linhas, ['restaurant_id', 'restaurant_name', 'cuisines', 'aggregate_rating']].sort_values('restaurant_id', ascending=True)
        nome_restaurante = aux2.iloc[0, 1]
    return ( nome_restaurante, culinaria, nota )


@st.cache_data
def prep_dataframe (df1):
    # Prepaarando o DataFrame
    # Tirando do DataSet as linhas duolicadas
    df1 = df1.drop_duplicates().copy()
    
   # Limpando linhas que contenham NaN
    df1.dropna(axis=0, how = 'any', inplace=True)
    
    # Inserindo a coluna 'country_name' com o nome dos paises
    df1['country_name'] = df1['Country Code'].replace({
                                                        1: "India",
                                                        14: "Australia",
                                                        30: "Brazil",
                                                        37: "Canada",
                                                        94: "Indonesia",
                                                        148: "New Zeland",
                                                        162: "Philippines",
                                                        166: "Qatar",
                                                        184: "Singapure",
                                                        189: "South Africa",
                                                        191: "Sri Lanka",
                                                        208: "Turkey",
                                                        214: "United Arab Emirates",
                                                        215: "England",
                                                        216: "United States of America",
                                                        })
    
    # Inserindo a coluna 'color_name' com o nome das cores
    df1['color_name'] = df1['Rating color'].replace({
                                                    "3F7E00": "darkgreen",
                                                    "5BA829": "green",
                                                    "9ACD32": "lightgreen",
                                                    "CDD614": "orange",
                                                    "FFBA00": "red",
                                                    "CBCBC8": "darkred",
                                                    "FF7800": "darkred",
                                                    })
    
    # Inserindo a coluna 'price_name' com o nome das categorias de preço
    df1['price_name'] = df1['Price range'].replace({
                                                    1: "cheap",
                                                    2: "normal",
                                                    3: "expensive",
                                                    4: "gtourmet",
                                                    })
                                                    
    # Categorizando todos os restaurantes por somente um tipo de culinaria. A primeira cadastrada.
    df1['Cuisines'] = df1.loc[:, 'Cuisines'].apply(lambda x: x.split(',')[0])
    
    # Renomeando as colunas do dataframe
    title = lambda x: inflection.titleize (x)
    snakcase = lambda x: inflection.underscore (x)
    spaces = lambda x: x.replace (" ", "")
    cols_old = list(df1.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakcase, cols_old))
    df1.columns = cols_new

    return df1

    
def clas_pelo_maior(df1, busca, classifica, desempata):
    aux = df1.loc[:, [classifica, desempata, busca, 'city', 'country_name']].sort_values(by= [classifica,  desempata], ascending=[False, True]).reset_index()
    aux1 = aux.drop('index', axis= 1).head(slider)
    return aux1


def clas_por_culinária(df1, busca, classifica, culinaria, tipo_culinaria, melhor, desempata):
    seleciona_linhas = (df1.loc[:, culinaria] == tipo_culinaria)
    aux = (df1.loc[seleciona_linhas, [classifica, desempata, busca, culinaria, 'city', 'country_name']]
           .sort_values(by= [classifica,  desempata], ascending=[melhor, True])
           .reset_index()
           .head(slider))
    aux1 = aux.drop('index', axis= 1).head(slider)
    return aux1


def preenche_criterio_um(df1, aux, i):
    seleciona_linhas = df1.loc[:, 'cuisines'] == aux.iloc[i, 0]
    aux1 = (df1.loc[seleciona_linhas, ['cuisines' , 'restaurant_name','aggregate_rating', 'restaurant_id', 'country_name', 'city', 'average_cost_for_two', 'currency' ]]
            .sort_values(by = ['aggregate_rating', 'restaurant_id'], ascending= [False, True]))
    label = aux1.iloc[0, 0] + ': ' + aux1.iloc[0, 1]
    valor = str(round(aux.iloc[i, 1],2)) + '/5.0'
    ajuda1 = 'País: ' + aux1.iloc[0, 4]
    ajuda2 = 'Cidade: ' + aux1.iloc[0, 5]
    ajuda3 = 'Média prato para dois: ' + str(aux1.iloc[0, 6]) + ' ' + aux1.iloc[0, 7]
    ajuda = (f"""
            {ajuda1}\n
            {ajuda2}\n
            {ajuda3}
            """
            )

    return label, valor, ajuda

def preenche_criterio_dois(df1, aux, i):
    seleciona_linhas = df1.loc[:, 'cuisines'] == aux.iloc[i, 0]
    aux1 = (df1.loc[seleciona_linhas, ['cuisines' , 'restaurant_name','aggregate_rating', 'restaurant_id', 'country_name', 'city', 'average_cost_for_two', 'currency' ]]
            .sort_values(by = ['aggregate_rating', 'restaurant_id'], ascending= [False, True]))
    label = aux1.iloc[0, 0] + ': ' + aux1.iloc[0, 1]
    valor = str(round(aux.iloc[i, 2],2)) + '/' + str(df1['restaurant_id'].nunique())
    ajuda0 = 'Nota média: ' + str(aux1.iloc[0,2]) + '/5.0' 
    ajuda1 = 'País: ' + aux1.iloc[0, 4]
    ajuda2 = 'Cidade: ' + aux1.iloc[0, 5]
    ajuda3 = 'Média prato para dois: ' + str(aux1.iloc[0, 6]) + ' ' + aux1.iloc[0, 7]
    ajuda = (f"""
            {ajuda0}\n
            {ajuda1}\n
            {ajuda2}\n
            {ajuda3}
            """
            )

    return label, valor, ajuda

def seleciona_unicos_ordena (df1, coluna, crescente):
    lista = df1.loc[:, coluna].unique()
    lista.sort()
    
    return lista
    
# ------------------------------    
# Carregando e tratando os dados
# ------------------------------ 
    
# Carregando
data_path = 'zomato.csv'
df = pd.read_csv(data_path)

df1 = prep_dataframe (df)

#++++++++++++++++++++++++++++++++++++++++++
# Layout Barra Lateral
#++++++++++++++++++++++++++++++++++++++++++

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown('## Marketplace')

image = Image.open( 'image.jpg' )
st.sidebar.image( image,use_column_width=True )

st.sidebar.markdown("""___""")

st.sidebar.markdown('### Filtros')
campos = seleciona_unicos_ordena (df1, 'country_name', True)
selecao_00 = st.sidebar.multiselect(key = 1, 
                                 label = "Escolha os Países que deseja visualizar os dados:",
                                 options = campos,
                                 default= campos)
st.sidebar.markdown("""___""")

slider = st.sidebar.slider(label='Selecione a quantidade de Restaurantes que deseja visualizar', min_value=1, max_value=20, value=10, step=1)
st.sidebar.markdown("""___""")

campos = seleciona_unicos_ordena (df1, 'cuisines', True)
selecao_01 = st.sidebar.multiselect("Escolha os Tipos de Culinária:",
                                    options = campos,
                                    default=['Home-made', 'BBQ', 'Japanese', 'Brazilian', 'Arabian', 'American', 'Italian' ])
st.sidebar.markdown("""___""")

st.sidebar.markdown("### Powered by Sergio Rezende")

#++++++++++++++++++++++++++++++++++++++++++
# Aplicando filtros ao DataFrame
#++++++++++++++++++++++++++++++++++++++++++

# Filtro de País
linhas_selecionadas = df1['country_name'].isin( selecao_00 )
df1 = df1.loc[ linhas_selecionadas, :]

# Filtro de culinária
linhas_selecionadas = df1['cuisines'].isin( selecao_01 )
df1 = df1.loc[ linhas_selecionadas, :]

#++++++++++++++++++++++++++++++++++++++++++
# Layout no Streamlit
#++++++++++++++++++++++++++++++++++++++++++

st.header('Visão Restaurantes')
st.divider()
st.markdown('#### Melhores restaurantes das principais culinárias')
radio_01 =st.radio(key = 4, label = 'Classificar por', options = ('Melhor avaliação média', 'Maior numero de restaurantes registrados'), horizontal=True)

with st.container():
    if radio_01 == 'Melhor avaliação média':
        aux = (df1.loc[:, ['cuisines' , 'aggregate_rating', 'restaurant_id' ]]
            .groupby('cuisines')
            .agg({'aggregate_rating' : 'mean', 'restaurant_id' : 'count'})
            .sort_values(by=['aggregate_rating',  'restaurant_id', 'cuisines' ], ascending= [False, False, True])
            .reset_index())

        col1, col2, col3, col4, col5 = st.columns(5, gap='small')
        with col1:
            label, valor, ajuda = preenche_criterio_um (df1, aux, 0)
            st.metric(label, valor, help=ajuda )
    
        with col2:
            label, valor, ajuda = preenche_criterio_um (df1, aux, 1)
            st.metric(label, valor, help=ajuda )
    
        with col3:
            label, valor, ajuda = preenche_criterio_um (df1, aux, 2)
            st.metric(label, valor, help=ajuda )
    
        with col4:
            label, valor, ajuda = preenche_criterio_um (df1, aux, 3)
            st.metric(label, valor, help=ajuda )
    
        with col5:
            label, valor, ajuda = preenche_criterio_um (df1, aux, 4)
            st.metric(label, valor, help=ajuda )
        
    else:
        aux = (df1.loc[:, ['cuisines' , 'aggregate_rating', 'restaurant_id' ]]
              .groupby('cuisines')
              .agg(nota_media = ('aggregate_rating', 'mean'), 
                   contagem_restaurantes= ('restaurant_id', 'count'))
              .sort_values(by=['contagem_restaurantes',  'nota_media', 'cuisines' ], ascending= [False, False, True])
              .reset_index())
        
        col1, col2, col3, col4, col5 = st.columns(5, gap='small')
        with col1:
            label, valor, ajuda = preenche_criterio_dois(df1, aux, 0)
            st.metric(label, valor, help=ajuda )
    
        with col2:
            label, valor, ajuda = preenche_criterio_dois(df1, aux, 1)
            st.metric(label, valor, help=ajuda )
    
        with col3:
            label, valor, ajuda = preenche_criterio_dois(df1, aux, 2)
            st.metric(label, valor, help=ajuda )
    
        with col4:
            label, valor, ajuda = preenche_criterio_dois(df1, aux, 3)
            st.metric(label, valor, help=ajuda )
    
        with col5:
            label, valor, ajuda = preenche_criterio_dois(df1, aux, 4)
            st.metric(label, valor, help=ajuda )      
st.divider()

radio_02 =st.radio(key = 5, label = 'Visulizar', options = ('Nome', 'Tabela (Usar "Slider" para definir a quantidade)'), horizontal=True)
with st.container():
    st.markdown('#### KPIs')
    col1, col2 = st.columns(2, gap='small')
    with col1:
        valor = clas_pelo_maior(df1, 'restaurant_name', 'votes', 'restaurant_id')
        valor.columns = ['Avaliações', 'ID do restaurante', 'Nome do restaurante', 'Cidade', 'País']
        if radio_02 == 'Nome':
            st.metric('###### Nome do restaurante que possui a maior quantidade de avaliações', valor.iloc[0, 2])
        else:
            st.markdown('###### Nome do restaurante que possui a maior quantidade de avaliações')
            st.dataframe(valor)
        
    with col2:
        valor = clas_pelo_maior(df1, 'restaurant_name', 'aggregate_rating', 'restaurant_id')
        valor.columns = ['Nota média', 'ID do restaurante', 'Nome do restaurante', 'Cidade', 'País']
        if radio_02 == 'Nome':
            st.metric('###### Nome do restaurante com a maior nota média', valor.iloc[0, 2])
        else:
            st.markdown('###### Nome do restaurante com a maior nota média')
            st.dataframe(valor)            
    st.divider()
        
with st.container():
    col1, col2 = st.columns(2, gap='small')
    with col1:
        valor = clas_pelo_maior(df1, 'restaurant_name', 'average_cost_for_two', 'restaurant_id')
        valor.columns = ['Preço médio prato p/ dois', 'ID do restaurante', 'Nome do restaurante', 'Cidade', 'País']
        if radio_02 == 'Nome':
            st.metric('###### Nome do restaurante que possui o maior valor de uma prato para duas pessoas', valor.iloc[0, 2])
        else:
            st.markdown('###### Nome do restaurante que possui o maior valor de uma prato para duas pessoas')
            st.dataframe(valor)
            
    with col2:
        valor = clas_por_culinária(df1, 'restaurant_name', 'aggregate_rating', 'cuisines', 'Brazilian', True, 'restaurant_id')
        valor.columns = ['Nota média', 'ID do restaurante', 'Nome do restaurante', 'Culinária', 'Cidade', 'País']
        if radio_02 == 'Nome':
            st.metric('###### Nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação', valor.iloc[0, 2])
        else:
            st.markdown('###### Nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação')
            st.dataframe(valor)            
    st.divider()
        
with st.container():
    df2 = df1.loc[df1['country_name'] == 'Brazil', :]
    valor = clas_por_culinária(df2, 'restaurant_name', 'aggregate_rating', 'cuisines', 'Brazilian', False, 'restaurant_id')
    valor.columns = ['Nota média', 'ID do restaurante', 'Nome do restaurante', 'Culinária', 'Cidade', 'País']
    if radio_02 == 'Nome':
        st.metric('###### Nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliaçãos', valor.iloc[0, 2])
    else:
        st.markdown('###### Nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliaçãos')
        st.dataframe(valor)        
    st.divider()
    
with st.container():
    # Pergunta 6
    # Monta um dataFrame que contem os restaurantes que aceitam pedidos online e apura a quantidade.
    seleciona_linhas = df1.loc[:, 'has_online_delivery'] == 1
    aux = df1.loc[seleciona_linhas, ['restaurant_id', 'has_online_delivery', 'votes']]
    pedido_online = len(aux)
    # Monta um DataFrame com um numero igual ao de restaurantes que aceitam pedidos online com o critério de mais avaliações.
    aux1 = df1[['restaurant_id', 'has_online_delivery', 'votes']].sort_values('votes',ascending=False).head(pedido_online)
    # Integra os dois dataFrames registrando o 'restaurant_id' que existem em ambos.
    aux2 = aux.merge(aux1, on=['restaurant_id'], how='outer', suffixes=['', '_'], indicator=True)
    aux3 = aux2.dropna()
    # calcula o percentual
    percentual =  np.round((len(aux3)/pedido_online)*100, 2)
    # Exibe a resposta
    st.markdown(f'##### Dos restaurantes que aceitam pedidos online, {percentual}% são também, os que mais possuem avaliações registradas.')
    st.divider()    
     
    # Pergunta 7
    # Monta um dataFrame que contem os restaurantes que fazem reserva e apura a quantidade.
    seleciona_linhas = df1.loc[:, 'has_table_booking'] == 0
    aux = df1.loc[seleciona_linhas, ['restaurant_id', 'has_table_booking', 'average_cost_for_two']]
    aceitam_reserva = len(aux)
    # Monta um DataFrame com um numero igual ao de restaurantes com maior valor médio de um prato para dois.
    aux1 = df1[['restaurant_id', 'has_table_booking', 'average_cost_for_two']].sort_values('average_cost_for_two',ascending=False).head(aceitam_reserva)
    # Integra os dois dataFrames registrando o 'restaurant_id' que existem em ambos.
    aux2 = aux.merge(aux1, on=['restaurant_id'], how='outer', suffixes=['', '_'], indicator=True)
    aux3 = aux2.dropna()
    # calcula o percentual
    percentual =  np.round((len(aux3)/aceitam_reserva)*100, 2)
    # Exibe a resposta
    st.markdown(f'##### Dos restaurantes que fazem reserva, {percentual}% são também, os que possuem os maiores preços médios em pratos para dois.')
    st.divider()

    #Pergunta 8
    seleciona_linhas = (df1.loc[:, 'country_name'] == 'United States of America') & (df1.loc[:, 'cuisines'] == 'Japanese')
    aux = df1.loc[seleciona_linhas, ['average_cost_for_two'] ].mean()
    aux = float(aux.iloc[0])
    seleciona_linhas = (df1.loc[:, 'country_name'] == 'United States of America') & (df1.loc[:, 'cuisines'] == 'BBQ')
    aux1 = df1.loc[seleciona_linhas, ['average_cost_for_two'] ].mean()
    aux1 = float(aux1.iloc[0])
    percentual = np.round((aux / aux1) * 100, 2)
    st.markdown(f'##### Os restaurantes do tipo culinária japonesa dos EUA possuem um valor médio de prato para duas pessoas {percentual}% maior que as churrascarias nos EUA.')    
    st.divider()
        














