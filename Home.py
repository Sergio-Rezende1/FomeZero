# Importando libraries
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
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import inflection

st.set_page_config( page_title='Fome Zero - Mundo', page_icon='✅', layout='wide')

# ------------------------------    
# Funções
# ------------------------------ 


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


def mapa_restaurantes (df2):
    """
    Este gráfico plota: A localização de cada restaurante com agrupamento por área
    """
    df1_aux = (df2.loc[:, ['restaurant_name', 'latitude', 'longitude', 'color_name' ]])

    map_obj = folium.Map(location= [0.00, 0.00], zoom_start=2,control_scale=True)
    map_clusters = MarkerCluster( name="Restaurantes").add_to(map_obj)
    
    for index, location_info in df1_aux.iterrows():
        folium.Marker(location=[location_info[1], location_info[2]], 
                      popup=location_info[0], 
                      icon=folium.Icon(color=location_info[3])).add_to(map_clusters)
    
    folium.LayerControl().add_to(map_obj)
    folium_static(map_obj, width=1100, height=550)


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

image = Image.open( 'image.jpg' )
st.sidebar.image( image,use_column_width=True )

st.sidebar.markdown("""___""")

st.sidebar.markdown('### Filtros')
selecao = st.sidebar.multiselect("Escolha os Países que deseja visualizar os Restaurantes no mapa:", 
                                 ['Philippines', 'Brazil', 'Australia', 'United States of America','Canada', 'Singapure', 'United Arab Emirates', 'India',
                                 'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa','Sri Lanka', 'Turkey'],
                                default=['Philippines', 'Brazil', 'Australia', 'United States of America','Canada', 'India'])
st.sidebar.markdown("""___""")

st.sidebar.markdown("### Powered by Sergio Rezende")


#++++++++++++++++++++++++++++++++++++++++++
# Aplicando filtros ao DataFrame
#++++++++++++++++++++++++++++++++++++++++++

# Filtro de transito
linhas_selecionadas = df1['country_name'].isin( selecao )
df2 = df1.loc[ linhas_selecionadas, :]


#++++++++++++++++++++++++++++++++++++++++++
# Layout no Streamlit
#++++++++++++++++++++++++++++++++++++++++++

st.markdown('## Fome Zero!')
st.markdown('### O melhor lugar para encontrar seu mais novo restaurante favorito!')
st.markdown('#### Temos as seguintes marcas dentro da nossa plataforma:')

with st.container():
    st.subheader( 'KPIs' )
    col1, col2, col3, col4, col5 = st.columns(5, gap='small')
        
    with col1:
        st.write( 'Restaurantes cadastrados:' )
        metrica = df1.loc[:, 'restaurant_id'].nunique()
        converte = f'{metrica:_.0f}'
        converte = converte.replace('_','.')
        col1.metric( '', converte)

    with col2:
        st.write( 'Países cadastrados:' )
        metrica = df1.loc[:, 'country_code'].nunique()
        converte = f'{metrica:_.0f}'
        converte = converte.replace('_','.')
        col2.metric( '', converte)    

    with col3:
        st.write( 'Cidades cadastrados:' )
        metrica = df1.loc[:, 'city'].nunique()
        converte = f'{metrica:_.0f}'
        converte = converte.replace('_','.')
        col3.metric( '', converte)  

    with col4:
        st.write( 'Avaliações feitas na Plataforma:' )
        metrica = df1.loc[:, 'votes'].sum()
        converte = f'{metrica:_.0f}'
        converte = converte.replace('_','.')
        col4.metric( '', converte)     

    with col5:
        st.write( 'Tipo de culinárias oferecidas:' )
        metrica = df1.loc[:, 'cuisines'].nunique()
        converte = f'{metrica:_.0f}'
        converte = converte.replace('_','.')        
        col5.metric( '', converte)     

with st.container():
        st.write("Localização dos restaurantes cadastreados (Filtro)")
        mapa_restaurantes (df2)            



