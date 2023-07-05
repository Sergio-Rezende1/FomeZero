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

st.set_page_config( page_title='Fome Zero - País', page_icon='✅', layout='wide')

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
    

def grafico_baras_contagem (col_a_agrupar, col_a_ordenar, nome_a_agrupar, nome_a_ordenar):
    colunas = {col_a_agrupar: nome_a_agrupar, col_a_ordenar: nome_a_ordenar }
    aux = df1.loc[:, [col_a_agrupar, col_a_ordenar]].groupby(col_a_agrupar).count().sort_values(col_a_ordenar, ascending=False).reset_index()
    fig = px.bar(aux, x= aux[col_a_agrupar], y= aux[col_a_ordenar], labels= colunas )
    fig.update_traces(texttemplate='%{y}', textposition='auto')
    return fig, aux, colunas


def grafico_baras_unicos (col_a_agrupar, col_a_ordenar, nome_a_agrupar, nome_a_ordenar):
    colunas = {col_a_agrupar: nome_a_agrupar, col_a_ordenar: nome_a_ordenar }
    aux = df1.loc[:, [col_a_agrupar, col_a_ordenar]].groupby(col_a_agrupar).nunique().sort_values(col_a_ordenar, ascending=False).reset_index()
    fig = px.bar(aux, x= aux[col_a_agrupar], y= aux[col_a_ordenar], labels= colunas )
    fig.update_traces(texttemplate='%{y}', textposition='auto')
    return fig, aux, colunas

def grafico_baras_media (col_a_agrupar, col_a_ordenar, nome_a_agrupar, nome_a_ordenar):
    colunas = {col_a_agrupar: nome_a_agrupar, col_a_ordenar: nome_a_ordenar }
    aux = df1.loc[:, [col_a_agrupar, col_a_ordenar]].groupby(col_a_agrupar).mean().sort_values(col_a_ordenar, ascending=False).reset_index()
    fig = px.bar(aux, x= aux[col_a_agrupar], y= aux[col_a_ordenar], labels= colunas )
    fig.update_traces(texttemplate='%{y}', textposition='auto')
    return fig, aux, colunas
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

st.header('Fome Zero - Visão Paises')
tab1, tab2 = st.tabs( ['Gráficos', 'Indicadores'] )

with tab1:
    selecao = st.radio("Escolha uma opção:", ("Gráfico", "Tabela"), horizontal=True)
    with st.container():
        st.write("Quantidade de restaurantes registrados por País.")
        fig, aux, colunas = grafico_baras_contagem ('country_name', 'restaurant_id', 'Pais', 'Restaurantes registrados')
        if selecao == "Gráfico":
            st.plotly_chart(fig, use_container_width=True)
        else:
            aux.rename(columns=colunas, inplace = True)
            st.dataframe(aux, use_container_width=True, hide_index=True)
        st.divider()
        
    with st.container():
            st.write("Quantidade de cidades registrados por País.")
            fig, aux, colunas = grafico_baras_unicos ('country_name', 'city', 'Pais', 'Cidades registrados')
            if selecao == "Gráfico":
                st.plotly_chart(fig, use_container_width=True)
            else:
                aux.rename(columns=colunas, inplace = True)
                st.dataframe(aux, use_container_width=True, hide_index=True)
            st.divider()
         
    with st.container():
            st.write("Avaliações feitas por País.")
            fig, aux, colunas = grafico_baras_media ('country_name', 'votes', 'Pais', 'Avaliações registradas')
            if selecao == "Gráfico":
                st.plotly_chart(fig, use_container_width=True)
            else:
                aux.rename(columns=colunas, inplace = True)
                st.dataframe(aux, use_container_width=True, hide_index=True)
            st.divider()
         
    with st.container():
            st.write("Média do preço no pratos para dois por País.")
            fig, aux, colunas = grafico_baras_media ('country_name', 'average_cost_for_two', 'Pais', 'Média do preço do pratos para dois')
            if selecao == "Gráfico":
                st.plotly_chart(fig, use_container_width=True)
            else:
                aux.rename(columns=colunas, inplace = True)
                st.dataframe(aux, use_container_width=True, hide_index=True)
            st.divider()
     

with tab2:
    with st.container():
        st.subheader( 'KPIs' )
        col1, col2, col3 = st.columns(3, gap='large')
        
        with col1:
            st.write( 'Pais com mais cidades registradas:' )
            maior_df = df1.loc[:, ['country_name', 'city']].groupby('country_name').nunique().sort_values('city',ascending=False).reset_index().head(1) 
            maior_vr = maior_df.loc[0,'country_name'] 
            st.subheader(maior_vr)

        with col2:
            st.write( 'País com mais restaurantes registradas:' )
            maior_df = df1.loc[:, ['country_name', 'restaurant_id']].groupby('country_name').nunique().sort_values('restaurant_id',ascending=False).reset_index().head(1)
            maior_vr = maior_df.loc[0,'country_name'] 
            st.subheader(maior_vr)      

        with col3:
            st.write( 'Pais com mais restaurantes de classificação Gourmet:' )
            nivel_preco = df1.loc[:, 'price_range'] == 4
            maior_df = df1.loc[nivel_preco, ['country_name', 'price_range']].groupby('country_name').count().sort_values('price_range',ascending=False).reset_index().head(1)
            maior_vr = maior_df.loc[0,'country_name']
            st.subheader(maior_vr)
            
        st.divider()

    with st.container():
        col1, col2, col3 = st.columns(3, gap='large')
        
        with col1:
            st.write( 'País com maior diversidade culinária:' )
            maior_df = df1.loc[:, ['country_name', 'cuisines']].groupby('country_name').nunique().sort_values('cuisines',ascending=False).reset_index().head(1)
            maior_vr = maior_df.loc[0,'country_name'] 
            st.subheader(maior_vr)

        with col2:
            st.write( 'País com maior numero de avaliações feitas:' )
            maior_df = df1.loc[:, ['country_name', 'votes']].groupby('country_name').sum().sort_values('votes',ascending=False).reset_index().head(1)
            maior_vr = maior_df.loc[0,'country_name'] 
            st.subheader(maior_vr)      

        with col3:
            st.write( 'Pais com maior numero de restaurantes que fazem entregas:' )
            delivery = df1.loc[:, 'is_delivering_now'] == 0
            maior_df =df1.loc[delivery, ['country_name', 'is_delivering_now']].groupby('country_name').count().sort_values('is_delivering_now',ascending=False).reset_index().head(1)
            maior_vr = maior_df.loc[0,'country_name'] 
            st.subheader(maior_vr)
            
        st.divider()

    with st.container():
        col1, col2, col3 = st.columns(3, gap='large')
        
        with col1:
            st.write( 'País com mais restaurantes que aceitam reservas:' )
            reserva = df1.loc[:, 'has_table_booking'] == 0
            maior_df = df1.loc[reserva, ['country_name', 'has_table_booking']].groupby('country_name').count().sort_values('has_table_booking',ascending=False).reset_index().head(1)
            maior_vr = maior_df.loc[0,'country_name'] 
            st.subheader(maior_vr)

        with col2:
            st.write( 'País que possui, na média, a maior quantidadede avaliações:' )
            maior_df = df1.loc[:, ['country_name', 'votes']].groupby('country_name').mean().sort_values('votes',ascending=False).reset_index().head(1)
            maior_vr = maior_df.loc[0,'country_name'] 
            st.subheader(maior_vr)      

        with col3:
            st.write( 'Pais que possue, na média, a maior nota média:' )
            maior_df = df1.loc[:, ['country_name', 'aggregate_rating']].groupby('country_name').mean().sort_values('aggregate_rating',ascending=False).reset_index().head(1)
            maior_vr = maior_df.loc[0,'country_name'] 
            st.subheader(maior_vr)
            
        st.divider()

    with st.container():
        st.write( 'Pais que possue, na média, a menor nota média:' )
        maior_df = df1.loc[:, ['country_name', 'aggregate_rating']].groupby('country_name').mean().sort_values('aggregate_rating',ascending=True).reset_index().head(1)
        maior_vr = maior_df.loc[0,'country_name'] 
        st.subheader(maior_vr)

        st.divider()

    
    with st.container():
        st.write( 'Média de preço de um prato para dois por País:' )
        maior_df = (df1.loc[:, ['country_name', 'currency', 'average_cost_for_two']]
                    .groupby(['country_name', 'currency'])
                    .mean()
                    .sort_values('average_cost_for_two',ascending=True)
                    .reset_index())
        st.dataframe(maior_df, column_config= {'country_name': 'País' ,'currency': 'Moeda' ,'average_cost_for_two': 'Preço médio de um prato para dois'}, use_container_width=True, hide_index=True)      
            
        st.divider()





        
