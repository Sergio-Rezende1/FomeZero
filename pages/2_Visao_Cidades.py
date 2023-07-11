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

st.set_page_config( page_title='Fome Zero - Cidades', page_icon='✅', layout='wide')

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

    
def class_dois_itens_nunique (df1, grupo, classifica, cor, grup_ord, clas_ord): 
    aux = (df1.loc[:, [grupo, classifica, cor]]
           .groupby([grupo, cor])
           .nunique()
           .sort_values(by= [classifica, grupo],ascending=[clas_ord, True])
           .reset_index())
    tabela_10 =aux.head(10)
    selecao = aux.iloc[0, 2]
    seleciona_linhas = aux.loc[:, classifica] == selecao
    tabela_correta = aux.loc[seleciona_linhas, [grupo, cor, classifica] ].sort_values(grupo, ascending=grup_ord)
    return tabela_10, tabela_correta


def class_dois_itens_max (df1, grupo, classifica, cor, grup_ord, clas_ord):
    aux = (df1.loc[:, [grupo, classifica, cor]]
           .groupby([grupo, cor])
           .max()
           .sort_values(by= [classifica, grupo],ascending=[clas_ord, True])
           .reset_index())
    tabela_10 =aux.head(10)
    selecao = aux.iloc[0, 2]
    seleciona_linhas = aux.loc[:, classifica] == selecao
    tabela_correta = aux.loc[seleciona_linhas, [grupo, cor, classifica] ].sort_values(grupo, ascending=grup_ord)
    return tabela_10, tabela_correta


def class_tres_itens(df1, corte, valor_corte, grupo, classifica, cor, maior_igual, grup_ord, clas_ord):
    if maior_igual == "sim":
        seleciona_linhas = df1.loc[:, corte] >= valor_corte
    elif maior_igual == "nao": 
        seleciona_linhas = df1.loc[:, corte] <= valor_corte
    else:
        seleciona_linhas = df1.loc[:, corte] == valor_corte
        
    aux = (df1.loc[seleciona_linhas, [grupo, classifica, cor] ]
           .groupby([grupo, cor])
           .count()
           .sort_values(by= [classifica, grupo],ascending=[clas_ord, True])
           .reset_index())
    tabela_10 = aux.head(10)
    selecao = aux.iloc[0, 2]
    seleciona_linhas1 = aux.loc[:, classifica] == selecao
    tabela_correta = aux.loc[seleciona_linhas1, [grupo, classifica, cor]].sort_values(grupo, ascending=grup_ord)
    return tabela_10, tabela_correta


def plota_grafico(tab1, camp1, nome1, camp2, nome2, camp3, nome3):
    fig = px.bar(tab1, x= tab1[camp1], y= tab1[camp2],  
                color= camp3, 
                labels= {camp1: nome1, camp2: nome2, camp3: nome3},
                color_discrete_sequence=px.colors.qualitative.Dark24,
                category_orders={camp1: tab1[camp1][::1]})
    fig.update_traces(texttemplate='%{y}', textposition='auto')
    return fig
        

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
selecao = st.sidebar.multiselect("Escolha os Países que deseja visualizar os dados:", 
                                 ['Philippines', 'Brazil', 'Australia', 'United States of America','Canada', 'Singapure', 'United Arab Emirates', 'India',
                                 'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa','Sri Lanka', 'Turkey'],
                                default=['Philippines', 'Brazil', 'Australia', 'United States of America','Canada', 'Singapure', 'United Arab Emirates', 'India',
                                 'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa','Sri Lanka', 'Turkey'])

st.sidebar.markdown("""___""")

st.sidebar.markdown("### Powered by Sergio Rezende")

#++++++++++++++++++++++++++++++++++++++++++
# Aplicando filtros ao DataFrame
#++++++++++++++++++++++++++++++++++++++++++

# Filtro de transito
linhas_selecionadas = df1['country_name'].isin( selecao )
df1 = df1.loc[ linhas_selecionadas, :]


#++++++++++++++++++++++++++++++++++++++++++
# Layout no Streamlit
#++++++++++++++++++++++++++++++++++++++++++

st.header('Visão Cidades')
st.divider()
radio_01 = st.radio("Escolha uma opção:", ("Gráfico  com as 10 primeiras", 'Gráfico com critério completo',  "Tabela"), horizontal=True)
st.divider()

with st.container():
    st.markdown("##### Cidade com o maior numero de restaurantes registrados:")   
    tab1, tab2 = class_dois_itens_nunique (df1, 'city', 'restaurant_id', 'country_name', grup_ord=True, clas_ord=False )
    if radio_01 == "Gráfico  com as 10 primeiras":
        fig = plota_grafico(tab1, 'city', 'Cidades', 'restaurant_id', 'Número de restaurantes', 'country_name', 'País')
        st.plotly_chart(fig, use_container_width=True)
    elif radio_01 == "Gráfico com critério completo":
        fig = plota_grafico(tab2, 'city', 'Cidades', 'restaurant_id', 'Número de restaurantes', 'country_name', 'País')
        st.plotly_chart(fig, use_container_width=True)
    else:                
        tab2.columns = ['Cidade', 'País', 'Numero de restaurantes cadastrados']
        st.write(f'Tabela composta de {len(tab2)} linhas.')
        st.dataframe(tab2, use_container_width=True, hide_index=True)
    
    st.divider()

with st.container():
    col1, col2 = st.columns(2, gap='small')

    with col1:
        st.markdown("##### Cidade que possuem mais restaurantes com nota média acima de 4:")
        tab1, tab2 = class_tres_itens(df1, 'aggregate_rating', 4.0, 'city', 'restaurant_id', 'country_name', 'sim',  grup_ord=True, clas_ord=False)
        if radio_01 == "Gráfico  com as 10 primeiras":
            fig = plota_grafico(tab1, 'city', 'Cidades', 'restaurant_id', 'Número de restaurantes', 'country_name', 'País')
            st.plotly_chart(fig, use_container_width=True)
        elif radio_01 == "Gráfico com critério completo":
            fig = plota_grafico(tab2, 'city', 'Cidades', 'restaurant_id', 'Número de restaurantes', 'country_name', 'País')
            st.plotly_chart(fig, use_container_width=True)
        else:                
            tab2.columns = ['Cidade', 'Numero de restaurantes cadastrados',  'País']
            st.write(f'Tabela composta de {len(tab2)} linhas.')               
            st.dataframe(tab2, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("##### Cidade que possuem mais restaurantes com nota média abaixo de 2,5:")
        tab1, tab2 = class_tres_itens(df1, 'aggregate_rating', 2.5, 'city', 'restaurant_id', 'country_name', 'nao',  grup_ord=True, clas_ord=False)
        if radio_01 == "Gráfico  com as 10 primeiras":
            fig = plota_grafico(tab1, 'city', 'Cidades', 'restaurant_id', 'Número de restaurantes', 'country_name', 'País')
            st.plotly_chart(fig, use_container_width=True)
        elif radio_01 == "Gráfico com critério completo":
            fig = plota_grafico(tab2, 'city', 'Cidades', 'restaurant_id', 'Número de restaurantes', 'country_name', 'País')
            st.plotly_chart(fig, use_container_width=True)
        else:
            tab2.columns = ['Cidade', 'Numero de restaurantes cadastrados',  'País']
            st.write(f'Tabela composta de {len(tab2)} linhas.')               
            st.dataframe(tab2, use_container_width=True, hide_index=True)

    st.divider()

with st.container():
    col1, col2 = st.columns(2, gap='small')

    with col1:
        st.markdown("##### Cidade com o maior valor médio de um prato para dois:")
        tab1, tab2 = class_dois_itens_max (df1, 'city', 'average_cost_for_two', 'country_name', grup_ord=True, clas_ord=False )
        if radio_01 == "Gráfico  com as 10 primeiras":
            fig = plota_grafico(tab1, 'city', 'Cidades', 'average_cost_for_two', 'Custo médio de um prato para dois', 'country_name', 'País')
            st.plotly_chart(fig, use_container_width=True)
        elif radio_01 == "Gráfico com critério completo":
            fig = plota_grafico(tab2, 'city', 'Cidades', 'average_cost_for_two', 'Custo médio de um prato para dois', 'country_name', 'País')
            st.plotly_chart(fig, use_container_width=True)
        else:
            tab2.columns = ['Cidade', 'País', 'Preço médio prato p/ dois']
            st.write(f'Tabela composta de {len(tab2)} linhas.')                 
            st.dataframe(tab2, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("##### Cidade com o maior numero de culinárias distintas:")
        tab1, tab2 = class_dois_itens_nunique (df1, 'city', 'cuisines', 'country_name', grup_ord=True, clas_ord=False )
        if radio_01 == "Gráfico  com as 10 primeiras":
            fig = plota_grafico(tab1, 'city', 'Cidades', 'cuisines', 'Número de diferentes culinárias', 'country_name', 'País')
            st.plotly_chart(fig, use_container_width=True)
        elif radio_01 == "Gráfico com critério completo":
            fig = plota_grafico(tab2, 'city', 'Cidades', 'cuisines', 'Número de diferentes culinárias', 'country_name', 'País')
            st.plotly_chart(fig, use_container_width=True)
        else:
            tab2.columns = ['Cidade', 'País', 'Culinária']
            st.write(f'Tabela composta de {len(tab2)} linhas.')                
            st.dataframe(tab2, use_container_width=True, hide_index=True)

    st.divider()

with st.container():
    col1, col2 = st.columns(2, gap='small')

    with col1:
        st.markdown("##### Cidade com o maior numero de restaurantes que fazem reservas:")
        tab1, tab2 = class_tres_itens(df1, 'has_table_booking', 0, 'city', 'has_table_booking', 'country_name', 'igual',  grup_ord=True, clas_ord=False)
        if radio_01 == "Gráfico  com as 10 primeiras":
            fig = plota_grafico(tab1, 'city', 'Cidades', 'has_table_booking', 'Restaurantes com reserva de mesas', 'country_name', 'País')
            st.plotly_chart(fig, use_container_width=True)
        elif radio_01 == "Gráfico com critério completo":
            fig = plota_grafico(tab2, 'city', 'Cidades', 'has_table_booking', 'Restaurantes com reserva de mesas', 'country_name', 'País')
            st.plotly_chart(fig, use_container_width=True)
        else:
            tab2.columns = ['Cidade', 'Numero de restaurantes cadastrados',  'País']
            st.write(f'Tabela composta de {len(tab2)} linhas.')                 
            st.dataframe(tab2, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("##### Cidade com o maior numero de restaurantes que fazem entregas:")
        tab1, tab2 = class_tres_itens(df1, 'is_delivering_now', 0, 'city', 'is_delivering_now', 'country_name', 'igual',  grup_ord=True, clas_ord=False)
        if radio_01 == "Gráfico  com as 10 primeiras":
            fig = plota_grafico(tab1, 'city', 'Cidades', 'is_delivering_now', 'Restaurantes com delivery', 'country_name', 'País')
            st.plotly_chart(fig, use_container_width=True)
        elif radio_01 == "Gráfico com critério completo":
            fig = plota_grafico(tab2, 'city', 'Cidades', 'is_delivering_now', 'Restaurantes com delivery', 'country_name', 'País')
            st.plotly_chart(fig, use_container_width=True)
        else:
            tab2.columns = ['Cidade', 'Numero de restaurantes cadastrados',  'País']
            st.write(f'Tabela composta de {len(tab2)} linhas.')                 
            st.dataframe(tab2, use_container_width=True, hide_index=True)

    st.divider()

with st.container():
    st.markdown("##### Cidade com o maior numero de restaurantes que aceitam pedidos on-line:")   
    tab1, tab2 = class_tres_itens(df1, 'is_delivering_now', 0, 'city', 'is_delivering_now', 'country_name', 'igual',  grup_ord=True, clas_ord=False)
    if radio_01 == "Gráfico  com as 10 primeiras":
        fig = plota_grafico(tab1, 'city', 'Cidades', 'is_delivering_now', 'Restaurantes com delivery', 'country_name', 'País')
        st.plotly_chart(fig, use_container_width=True)
    elif radio_01 == "Gráfico com critério completo":
        fig = plota_grafico(tab2, 'city', 'Cidades', 'is_delivering_now', 'Restaurantes com delivery', 'country_name', 'País')
        st.plotly_chart(fig, use_container_width=True)
    else:
        tab2.columns = ['Cidade', 'Numero de restaurantes cadastrados',  'País']
        st.write(f'Tabela composta de {len(tab2)} linhas.')               
        st.dataframe(tab2, use_container_width=True, hide_index=True)
    
    st.divider()
