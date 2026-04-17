import pandas as pd
from sqlalchemy import create_engine
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import RobustScaler

# 1. CONNECT TO THE DB
db_url = 'postgresql://postgres:password@localhost:5432/postgres'
engine = create_engine(db_url)

# 2. EXTRACT (Querying the DB directly)
print("📡 Pulling live data from PostgreSQL...")
query = "SELECT * FROM ucl_bet_stream;"
df = pd.read_sql(query, engine)

# 3. ENGINEER & SCALE
df['reaction_delta'] = (df['bet_placed_ts'] - df['market_update_ts']).dt.total_seconds()
scaler = RobustScaler()
X_scaled = scaler.fit_transform(df[['reaction_delta', 'bet_amount']])

# 4. DETECT (The Iron Triangle DBSCAN)
print("🧠 Running Unsupervised Forensic Clustering...")
dbscan = DBSCAN(eps=0.1, min_samples=150)
df['cluster_id'] = dbscan.fit_predict(X_scaled)

# 5. LOAD (Pushing the Audit back to the DB)
# We map the clusters to readable labels for Power BI
df['is_predicted_bot'] = df['cluster_id'].apply(lambda x: True if x != -1 else False)

audit_table = 'fact_forensic_audit'
print(f"💾 Saving forensic tags to new table: {audit_table}...")

# We only push the necessary columns to keep the BI table clean
export_df = df[['bet_id', 'event_name', 'bet_amount', 'reaction_delta', 'is_predicted_bot']]
export_df.to_sql(audit_table, engine, if_exists='replace', index=False)

print("✅ Audit Complete. Data is ready for Power BI.")