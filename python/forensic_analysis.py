import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. LOAD THE DATA
# We are reading the CSV we just generated
df = pd.read_csv('ucl_bet_stream_raw.csv')

# 2. FEATURE ENGINEERING: THE REACTION DELTA
# We convert strings to datetime objects so we can do math
df['market_update_ts'] = pd.to_datetime(df['market_update_ts'])
df['bet_placed_ts'] = pd.to_datetime(df['bet_placed_ts'])

# Calculate Delta (Time difference in seconds)
# This is our primary forensic metric.
df['reaction_delta'] = (df['bet_placed_ts'] - df['market_update_ts']).dt.total_seconds()

# 3. VISUALIZING THE "GHOST SIGNAL"
# We'll use a histogram to see the distribution of reaction times.
plt.figure(figsize=(12, 6))

# Plotting the humans (long tail) and the bots (sharp spike)
sns.histplot(df['reaction_delta'], bins=100, kde=True, color='blue')

# Formatting for the "Delta League" Boardroom
plt.title('Delta League: Distribution of Bet Reaction Times (UCL Quarter-Finals)', fontsize=14)
plt.xlabel('Reaction Time (Seconds from Odds Update)', fontsize=12)
plt.ylabel('Number of Bets', fontsize=12)
plt.xlim(0, 15) # Zooming in on the first 15 seconds
plt.grid(axis='y', alpha=0.3)

# Save the evidence
plt.savefig('reaction_distribution.png')
print("📊 Forensic plot saved toreaction_distribution.png")

# 4. STATISTICAL SUMMARY
print("\n--- Forensic Summary ---")
print(f"Total Bets Analyzed: {len(df)}")
print(f"Minimum Reaction Time: {df['reaction_delta'].min():.4f}s")
print(f"Average Reaction Time: {df['reaction_delta'].mean():.2f}s")
