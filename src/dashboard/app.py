import streamlit as st
import pandas as pd
import sqlite3

# Conectando ao banco de dados SQLite
conn = sqlite3.connect('./data/quotes.db')

# Lendo os dados do banco de dados para um DataFrame
df = pd.read_sql_query('SELECT * FROM mercadolivre_items', conn)

# Fechando a conexão com o banco de dados
conn.close()

# Título e subtítulo do aplicativo
st.title('Pesquisa de Mercado - Tênis Esportivos no Mercado Livre')
st.subheader('KPIs principais do sistema')

# Definindo as colunas para os KPIs principais
col1, col2, col3 = st.columns(3)

# KPI 1: Total de itens
total_itens = df.shape[0]
col1.metric(label='Total de itens', value=total_itens)

# KPI 2: Número de Marcas Únicas
unique_brands = df['brand'].nunique()
col2.metric(label='Número de Marcas Únicas', value=unique_brands)

# KPI 3: Preço Médio Novo (R$)
average_new_price = df['new_price'].mean()
col3.metric(label='Preço Médio Novo (R$)', value=f"R$ {average_new_price:.2f}")

# Análise das marcas mais encontradas até a 10ª página
st.subheader('Marcas mais encontradas até a 10ª página')
col1, col2 = st.columns([4, 2])

# Limitando a análise às primeiras 500 linhas para simular até a 10ª página
top_10_pages_brands = df.head(500)['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_10_pages_brands)
col2.write(top_10_pages_brands)

# Análise do preço médio por marca
st.subheader('Preço médio por marca')
col1, col2 = st.columns([4, 2])

# Filtrando apenas itens com preço maior que zero
df_non_zero_prices = df[df['new_price'] > 0]
average_price_by_brand = df_non_zero_prices.groupby('brand')['new_price'].mean().sort_values(ascending=False)
col1.bar_chart(average_price_by_brand)
col2.write(average_price_by_brand)

# Análise da satisfação por marca
st.subheader('Satisfação por Marca')
col1, col2 = st.columns([4, 2])

# Filtrando apenas itens com avaliação de satisfação maior que zero
df_non_zero_reviews = df[df['reviews_rating_number'] > 0]
satisfaction_by_brand = df_non_zero_reviews.groupby('brand')['reviews_rating_number'].median().sort_values(ascending=False)
col1.bar_chart(satisfaction_by_brand)
col2.write(satisfaction_by_brand)
