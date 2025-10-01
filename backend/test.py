import pandas as pd
import numpy as np

# Load the actual data
df = pd.read_csv('../data/cumulative_2025.09.16_22.42.55.csv')

# Calculate actual statistics
total = len(df)
confirmed = len(df[df['koi_disposition'] == 'CONFIRMED'])
candidates = len(df[df['koi_disposition'] == 'CANDIDATE'])
false_positives = len(df[df['koi_disposition'] == 'FALSE POSITIVE'])

print(f'Total exoplanets: {total:,}')
print(f'Confirmed: {confirmed:,}')
print(f'Candidates: {candidates:,}')
print(f'False positives: {false_positives:,}')

# Calculate habitability (simplified version)
habitable = 0
for _, row in df.iterrows():
    if pd.notna(row['koi_teq']) and pd.notna(row['koi_prad']) and pd.notna(row['koi_insol']):
        score = 0
        if 273 <= row['koi_teq'] <= 373:
            score += 40
        if 0.8 <= row['koi_prad'] <= 1.5:
            score += 30
        if 0.25 <= row['koi_insol'] <= 1.5:
            score += 30
        if score >= 70:
            habitable += 1

print(f'Potentially habitable: {habitable:,}')