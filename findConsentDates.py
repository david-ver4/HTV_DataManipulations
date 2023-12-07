import pandas as pd

# Read the input CSV file
input_file_path = 'dailyActivity_merged.csv'
df = pd.read_csv(input_file_path)

# Convert 'ActivityDate' column to datetime format
df['ActivityDate'] = pd.to_datetime(df['ActivityDate'], errors='coerce')

# Drop rows with missing or invalid dates
df = df.dropna(subset=['ActivityDate'])

# Group by ID and get the first ActivityDate for each group
consent_dates = df.groupby('Id')['ActivityDate'].min().reset_index()

# Set the date format for the 'ActivityDate' column
consent_dates['ActivityDate'] = consent_dates['ActivityDate'].dt.strftime('%m/%d/%Y')

# Save the results to a new Excel file
output_file_path = 'Fall23_consent_dates.xlsx'
consent_dates.to_excel(output_file_path, index=False)

print(f"Consent dates have been saved to {output_file_path}")
