import pandas as pd
from dataset import df
import streamlit as st
import time

#Formato valor de números em milhares e milhões
def format_number(value, prefix = ''):
    for unit in ['', 'mil']:
        if value < 1000:
            return f'{prefix} {value:.2f} {unit}'
        value /= 1000
    return f'{prefix} {value:.2f} milhões'    

#1 - Dataframe Receita por Estado
#Faz o agrupamento dos dados do dataframe por local de compra
df_rec_estado = df.groupby('Local da compra')[['Preço']].sum()
#Retira as informações duplicadas
df_rec_estado = df.drop_duplicates(subset='Local da compra')[['Local da compra','lat','lon']].merge(df_rec_estado, left_on='Local da compra', right_index=True).sort_values('Preço', ascending=False)

#2 - Dataframe Receita Mensal
#Faz o agrupamento dos dados do dataframe por Data da Compra
df_rec_mensal = df.set_index('Data da Compra').groupby(pd.Grouper(freq='ME'))['Preço'].sum().reset_index()
df_rec_mensal['Ano'] = df_rec_mensal['Data da Compra'].dt.year
df_rec_mensal['Mes'] = df_rec_mensal['Data da Compra'].dt.month_name()

#3 - Dataframe Receita por Categoria
df_rec_categoria = df.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço', ascending=False)

#4 - Dataframe vendedores
df_vendedores = pd.DataFrame(df.groupby('Vendedor')['Preço'].agg(['sum','count']))

#Função para converter arquivo CSV
@st.cache
def convert_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def mensagem_sucesso():
    success = st.success('Arquivo baixado com sucesso',
                         #icon="" 
                        )
    time.sleep(3)
    success.empty()                     
