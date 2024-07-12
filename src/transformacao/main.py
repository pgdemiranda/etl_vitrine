import pandas as pd
import sqlite3
from datetime import datetime

# Configuração para exibir todas as colunas do pandas
pd.options.display.max_columns = None

# Lê um arquivo JSON de linhas para um DataFrame do pandas
df = pd.read_json('../../data/data.jsonl', lines=True)

# Adiciona uma coluna '_source' com um valor constante
df['_source'] = 'https://lista.mercadolivre.com.br/tenis-corrida-masculino'

# Adiciona uma coluna '_data_coleta' com a data e hora atual
df['_data_coleta'] = datetime.now()

# Preenche valores ausentes e converte para float para colunas relacionadas a preço
df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_centavos'] = df['old_price_centavos'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float)

# Preenche valores ausentes e converte para float para a coluna de número de avaliações
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

# Remove parênteses de 'reviews_amount', preenche valores ausentes e converte para inteiro
df['reviews_amount'] = df['reviews_amount'].str.replace(r'[\(\)]', '', regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

# Calcula 'old_price' e 'new_price' combinando reais e centavos
df['old_price'] = df['old_price_reais'] + df['old_price_centavos'] / 100
df['new_price'] = df['new_price_reais'] + df['new_price_centavos'] / 100

# Remove colunas originais de preço após o cálculo dos preços combinados
df.drop(columns=['old_price_reais', 'old_price_centavos', 'new_price_reais', 'new_price_centavos'], inplace=True)

# Conecta ao banco de dados SQLite
conn = sqlite3.connect('../../data/quotes.db')

# Escreve o DataFrame no banco de dados SQLite na tabela 'mercadolivre_items'
df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

# Fecha a conexão com o banco de dados
conn.close()