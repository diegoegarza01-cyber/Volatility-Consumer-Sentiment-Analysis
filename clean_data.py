import pandas as pd

# 1. Get the raw data from the web
url = "https://raw.githubusercontent.com/OxCGRT/covid-policy-dataset/main/data/OxCGRT_compact_subnational_v1.csv"
df = pd.read_csv(url)

# 2. Filter for U.S. and fix the Date format
usa_df = df[df['CountryName'] == 'United States'].copy()
usa_df['Date'] = pd.to_datetime(usa_df['Date'], format='%Y%m%d')

# 3. SET THE DATE AS THE INDEX (This is why the averaging wasn't working before!)
usa_df = usa_df.set_index('Date')

# 4. AVERAGE BY MONTH 
# This shrinks the data so it matches your FRED/Consumer Sentiment data
monthly_data = usa_df['StringencyIndex_Average'].resample('MS').mean().reset_index()

# 5. CREATE THE DUMMY (The "Block" variable for your regression)
# If monthly avg is > 50, it's a 1. Otherwise, it's a 0.
monthly_data['lockdown_dummy'] = (monthly_data['StringencyIndex_Average'] > 50).astype(int)

# 6. SAVE TO A TOTALLY NEW FILE NAME
monthly_data.to_excel('RESEARCH_READY_DATA.xlsx', index=False)

print("\n--- SCRIPT FINISHED ---")
print(f"I found {len(monthly_data)} months of data for your model.")
print("Check your folder for: RESEARCH_READY_DATA.xlsx")