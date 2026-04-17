import pandas as pd
from sqlalchemy import create_engine

# 1. THE CONNECTION STRING
# Format: postgresql://postgres:password@host:port/database_name
db_url = 'postgresql://postgres:password@localhost:5432/postgres'
engine = create_engine(db_url)

print("🔌 Connected to PostgreSQL...")

# 2. LOAD THE FLAT FILE
# We are picking up the CSV we generated in Phase 1
df = pd.read_csv('ucl_bet_stream_raw.csv')

# Ensure our timestamps are clean before pushing
df['market_update_ts'] = pd.to_datetime(df['market_update_ts'])
df['bet_placed_ts'] = pd.to_datetime(df['bet_placed_ts'])

# 3. PUSH TO POSTGRESQL (The Data Engineering Magic)
# This automatically creates the table 'ucl_bet_stream' and loads the data.
# We use 'replace' so you can run this multiple times without duplicating data.
table_name = 'ucl_bet_stream'

print(f"📦 Pushing {len(df)} records to table: {table_name}...")
df.to_sql(table_name, engine, if_exists='replace', index=False)

print("✅ Data Ingestion Complete! The CSV is now a live database table.")
