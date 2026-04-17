import pandas as pd
import numpy as np
import uuid
from datetime import datetime, timedelta

# 1. SETTING THE SEED
# Using a seed ensures that "random" data is reproducible. 
# If ran again, we would get the exact same "random" numbers.
np.random.seed(42)

def generate_delta_league_data(num_records=10000, bot_ratio=0.02):
    """
    Generates a synthetic dataset of UCL betting traffic.
    Includes 'Noise' (Humans) and 'The Pulse' (Courtsider Swarm).
    """
    
    data = []
    
    # 2. DEFINING THE CONSTANTS
    # All bots and humans are betting on the same UCL event for this slice.
    event_name = "Real Madrid vs Man City"
    market_update_base = datetime(2026, 4, 14, 21, 0, 0) # 9:00 PM Match Time
    
    # Calculate how many bots vs humans
    num_bots = int(num_records * bot_ratio)
    num_humans = num_records - num_bots

    # 3. GENERATING HUMAN BEHAVIOR (The Noise)
    # Humans take between 2 to 30 seconds to react.
    # rvs = Random Variates (numbers drawn from the distribution)
    human_deltas = np.random.lognormal(mean=2.0, sigma=0.5, size=num_humans) + 2.0
    
    for delta in human_deltas:
        bet_time = market_update_base + timedelta(seconds=delta)
        data.append({
            "bet_id": uuid.uuid4(),
            "user_id": uuid.uuid4(),
            "event_name": event_name,
            "market_update_ts": market_update_base,
            "bet_placed_ts": bet_time,
            "bet_amount": round(np.random.uniform(10, 500), 2),
            "is_bot_label": 0  # We keep this for validation, but the model won't see it!
        })

    # 4. GENERATING THE COURTSIDER SWARM (The Pulse)
    # Bots react in milliseconds (0.04s to 0.06s). 
    # Tiny scale (0.005) compared to humans.
    bot_deltas = np.random.normal(loc=0.05, scale=0.005, size=num_bots)
    
    for delta in bot_deltas:
        bet_time = market_update_base + timedelta(seconds=delta)
        data.append({
            "bet_id": uuid.uuid4(),
            "user_id": uuid.uuid4(),
            "event_name": event_name,
            "market_update_ts": market_update_base,
            "bet_placed_ts": bet_time,
            "bet_amount": round(np.random.normal(250, 10), 2), # Bots often bet similar amounts
            "is_bot_label": 1
        })

    # 5. CONVERT TO DATAFRAME AND SHUFFLE
    # We shuffle so the bots aren't all at the end of the file.
    df = pd.DataFrame(data)
    df = df.sample(frac=1).reset_index(drop=True)
    
    return df

# EXECUTION
if __name__ == "__main__":
    print("🚀 Generating Delta League Forensic Data...")
    df_final = generate_delta_league_data()
    
    # Save to your new data folder
    df_final.to_csv("ucl_bet_stream_raw.csv", index=False)
    print(f"✅ Success! Saved {len(df_final)} records to ucl_bet_stream_raw.csv")
