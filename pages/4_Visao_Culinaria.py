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

st.set_page_config( page_title='Fome Zero - Culinária', page_icon='✅', layout='wide')


# ------------------------------  
# Funções
# ------------------------------  

@st.cache_data
def prep_dataframe (df1):
    # Prepaarando o DataFrame
    # Tirando do DataSet as linhas duolicadas
    df1 = df1.drop_duplicates().copy()
    
    # Subistituindo o NaN na coluna 'Cuisines' por 'not_specified'
    df1['Cuisines'].fillna(value='not_specified' ,inplace=True)
    
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


def seleciona_unicos_ordena (df1, coluna):
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

st.sidebar.divider()

campos = seleciona_unicos_ordena (df1, 'country_name')
selecao_00 = st.sidebar.multiselect(key = 1, 
                                 label = "Escolha os Países que deseja visualizar os dados:",
                                 options = campos,
                                 default= campos)
st.sidebar.divider()

st.sidebar.markdown("### Powered by Sergio Rezende")

#++++++++++++++++++++++++++++++++++++++++++
# Aplicando filtros ao DataFrame
#++++++++++++++++++++++++++++++++++++++++++

# Filtro de paísews
linhas_selecionadas = df1['country_name'].isin( selecao_00 )
df1 = df1.loc[ linhas_selecionadas, :]

#++++++++++++++++++++++++++++++++++++++++++
# Preparando listas
#++++++++++++++++++++++++++++++++++++++++++

#Culinária
culinaria = seleciona_unicos_ordena (df1, 'cuisines')

#++++++++++++++++++++++++++++++++++++++++++
# Layout no Streamlit
#++++++++++++++++++++++++++++++++++++++++++

st.header('Visão Culinária')
st.divider()

with st.form(key= 'primeiro'):
    st.write('Escolhas os parametros abaixo:')
    culinaria_sel = st.selectbox(key= '01', label= 'Selecione uma culinária', options= culinaria)
    ordem = st.radio(key= '02', label= 'Selecione a avaliação?', options = ('Maior', 'Menor'), horizontal=True)
    
    enviar = st.form_submit_button("consultar")

    if ordem == 'Maior':
        bool_ordem = False
    else:
        bool_ordem = True
        
    if enviar:
        seleciona_linhas = df1.loc[:, 'cuisines'] == culinaria_sel
        aux = (df1.loc[seleciona_linhas, ['cuisines', 'restaurant_name', 'aggregate_rating', 'city', 'country_name', 'restaurant_id']]
               .sort_values(by= ['aggregate_rating','restaurant_id'], ascending= [bool_ordem, True])
               .reset_index()
               .head(1))
        st.write(f'''
                O restaurante "{aux.iloc[0, 2]}" na cidade de {aux.iloc[0, 4]}, {aux.iloc[0, 5]}, tem avaliação média de {aux.iloc[0, 3]} 
                que é a {ordem} nota média de entre os registrados para a culinária {aux.iloc[0, 1]}.
                ''')
    st.divider()

with st.form(key= 'segundo'):
    st.write('Culinária com os maiores ou menores valores médios de um prato para dois:')
    ordem = st.radio(key= '04', label= 'Selecione a ordem para a classificação', options = ('Maior', 'Menor'), horizontal=True)
    
    enviar_01 = st.form_submit_button("consultar")

    if ordem == 'Maior':
        bool_ordem = False
    else:
        bool_ordem = True
        
    if enviar_01:
        aux = df1.loc[:, ['cuisines', 'average_cost_for_two']].sort_values('average_cost_for_two', ascending= bool_ordem).reset_index()
        maximo_minimo = aux.loc[0, 'average_cost_for_two']
        seleciona_linhas = aux.loc[:, 'average_cost_for_two'] == maximo_minimo
        aux1= aux.loc[seleciona_linhas, ['cuisines', 'average_cost_for_two']]
        aux1.columns = ['Culinária', 'Valor médio de um prato para dois']
        st.dataframe(aux1)
            
with st.form(key= 'terceiro'):
    st.write('Culinária com as maiores ou menores avaliações:')
    ordem = st.radio(key= '05', label= 'Selecione a ordem para a classificação', options = ('Maior', 'Menor'), horizontal=True)
    
    enviar_01 = st.form_submit_button("consultar")

    if ordem == 'Maior':
        bool_ordem = False
    else:
        bool_ordem = True
        
    if enviar_01:
        aux = df1.loc[:, ['cuisines', 'aggregate_rating']].groupby('cuisines').mean().sort_values('aggregate_rating', ascending= bool_ordem).reset_index()
        maximo_minimo = aux.loc[0, 'aggregate_rating']
        seleciona_linhas = aux.loc[:, 'aggregate_rating'] == maximo_minimo
        aux1= aux.loc[seleciona_linhas, ['cuisines', 'aggregate_rating']]
        aux1.columns = ['Culinária', 'Avaliação Média']
        st.dataframe(aux1)

st.divider()
with st.container():
    seleciona_linhas = (df1.loc[:, 'has_online_delivery'] == 1) & (df1.loc[:, 'is_delivering_now'] == 1)
    aux= df1.loc[seleciona_linhas, ['cuisines', 'restaurant_id']].groupby('cuisines').count().sort_values('restaurant_id', ascending=False).reset_index()
    maximo = aux.loc[0, 'restaurant_id']
    seleciona_linhas = aux.loc[:, 'restaurant_id'] == maximo
    aux1= aux.loc[seleciona_linhas, ['cuisines', 'restaurant_id']]
    st.write(f'##### A culinária que possue mais restaurantes que aceitam pedidos on-line e fazem entregas, entre os países selecionados é: {aux1.iloc[0,0]}')


