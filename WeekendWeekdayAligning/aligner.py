import pandas as pd

# Load the consent dates data
consent_dates_df = pd.read_excel('Sp23_consent_dates.xlsx')

# Load the test6 data
test6_df = pd.read_excel('test6.xlsx', header=None)  # Assuming you don't have headers

# Create a dictionary to map participant IDs to their consent dates
consent_date_dict = dict(zip(consent_dates_df['ID'], consent_dates_df['Consent Date']))

# Define the reference date (2/15/2023)
reference_date = pd.to_datetime('2/15/2023', format='%m/%d/%Y')
days_difference_dict = {}
# Iterate through the rows of test6 and print participant ID and days difference
for row in range(0, len(consent_dates_df)):
    participant_id = consent_dates_df.iloc[row, 0]
    consent_date = consent_date_dict.get(participant_id, '2/15/2023')
    consent_date = pd.to_datetime(consent_date, format='%m/%d/%Y')
    days_difference = (consent_date - reference_date).days

    days_difference_dict[participant_id] = days_difference

    print(f"Participant ID: {participant_id}, Days Difference: {days_difference}")

print(days_difference_dict)












