import pandas as pd
from sqlalchemy import create_engine

# Database connection parameters
POSTGRES_USER = 'admin'
POSTGRES_PASSWORD = 'admin'
POSTGRES_DB = 'neo_bank'
POSTGRES_HOST = 'localhost'  
POSTGRES_PORT = '5433'

# Parquet file path
parquet_file_path = 'raw_data/neo-bank-non-sub-churn-prediction/train_2008.parquet'

# Define table name
table_name = 'train_2008_data'

# Create a connection string
conn_string = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

# Create an SQLAlchemy engine
engine = create_engine(conn_string)

# Load Parquet file into DataFrame
df = pd.read_parquet(parquet_file_path)

# Convert object-type columns to string to prevent psycopg2 errors
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].astype(str)
    
# Load the DataFrame into PostgreSQL, and automatically handle type mapping
df.to_sql(table_name, engine, if_exists='replace', index=False)

print(f"Data from {parquet_file_path} successfully loaded into the {table_name} table.")
