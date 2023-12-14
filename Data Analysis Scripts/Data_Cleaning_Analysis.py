import pandas as pd
import os

# Load data from the Excel files
file_path_Steps = 'SP23_physicalActivityV3.xlsx'
sheet_name_Steps = 'RestingHeartRate'
file_path_consent = 'Sp23_consent_dates.xlsx'

# Load the data from the specified sheets
df_Steps = pd.read_excel(file_path_Steps, sheet_name=sheet_name_Steps)
df_consent = pd.read_excel(file_path_consent)

# Initialize lists to store valid and invalid participant IDs
valid_participant_ids = []
invalid_participant_ids = []

# Define the threshold for inconsistent consecutive dates (e.g., 3 days)
inconsistent_threshold = 11

# Define the threshold for invalid data (e.g., a large gap between non-zero values)
invalid_threshold = 1000  # Adjust this threshold as needed

# Define the additional conditions
consecutive_no_data_threshold = 11  # Number of consecutive no data days to consider
max_allowed_gaps = 4  # Number of 4+ days no data gaps to consider

# Loop through each participant in the physical activity data
for col_num in range(1, df_Steps.shape[1]):
    participant_data = df_Steps.iloc[:, col_num]

    # Filter out days with no data (assuming '0' represents missing data)
    non_zero_data = participant_data[participant_data != 0]

    # Check if the participant has at least 3 non-zero data points (change as needed)
    if len(non_zero_data) >= 3:
        # Identify gaps of inconsistent data and invalid data
        is_inconsistent = False
        is_invalid = False
        consecutive_zeros = 0
        prev_non_zero_index = None
        max_no_data_gap = 0
        no_data_gap_count = 0
        for index in non_zero_data.index:
            value = non_zero_data[index]
            if prev_non_zero_index is not None:
                gap = index - prev_non_zero_index - 1
                if gap > inconsistent_threshold:
                    is_inconsistent = True
                if gap > invalid_threshold:
                    is_invalid = True
                if gap > 0:
                    consecutive_zeros = 0
                elif consecutive_zeros >= consecutive_no_data_threshold:
                    no_data_gap_count += 1
                consecutive_zeros += 1
                if consecutive_zeros > max_no_data_gap:
                    max_no_data_gap = consecutive_zeros
            prev_non_zero_index = index

        if not is_inconsistent and (not is_invalid or no_data_gap_count > max_allowed_gaps):
            valid_participant_ids.append(df_Steps.columns[col_num])
        else:
            invalid_participant_ids.append(df_Steps.columns[col_num])
    else:
        invalid_participant_ids.append(df_Steps.columns[col_num])

# Create a new DataFrame to store the results
result_data = []

# Loop through each participant in the consent data
for col_num in range(1, df_Steps.shape[1]):
    participant_id = df_Steps.columns[col_num]

    # Filter consent data for the current participant
    consent_data = df_consent[df_consent['ID'] == participant_id]
    consent_date = pd.to_datetime(consent_data.iloc[0]['Consent Date']) if not consent_data.empty else None

    # Filter out days with no data (assuming '0' represents missing data)
    participant_data1 = df_Steps.iloc[:, [0, col_num]].copy()
    participant_data = participant_data1[participant_data1.iloc[:, 1] != 0]

    # Calculate the mean and standard deviation for the first and last five days
    # Calculate the "First Consecutive 5 day mean" and "First Consecutive 5 day standard deviation"

    # Calculate the "Last Consecutive 5 day mean (<day 70)" and "Last Consecutive 5 day standard deviation"
    if len(participant_data) >= 70:
        consecutive_mean_last = df_Steps.iloc[66:71, col_num].mean()
        consecutive_std_last = df_Steps.iloc[66:71, col_num].std()
    else:
        consecutive_mean_last = participant_data.iloc[-5:, 1].mean()
        consecutive_std_last = participant_data.iloc[-5:, 1].std()
    if len(participant_data) >= 5:
        consecutive_mean_first = participant_data.iloc[:5, 1].mean()
        consecutive_std_first = participant_data.iloc[:5, 1].std()
    else:
        consecutive_mean_first = consecutive_std_first = "Not sufficient"

    # Calculate the "First date of Fitbit use" and "Last date of Fitbit use"
    first_date_fitbit1 = int(participant_data.iloc[0, 0] if len(participant_data) > 0 else 0)
    last_date_fitbit2 = int(participant_data.iloc[-1, 0] if len(participant_data) > 0 else 0)

    # Calculate the number of non-zero data points
    num_recorded_data = len(participant_data)

    # Append the results to the result_data list
    result_data.append([participant_id, consent_date, first_date_fitbit1,
                        last_date_fitbit2,num_recorded_data,
                        consecutive_mean_first, consecutive_std_first,
                        consecutive_mean_last, consecutive_std_last])

# Create a new DataFrame from the result_data list with appropriate column names
result_df = pd.DataFrame(result_data, columns=['Participant ID', 'Start Date of Intervention',
                                               '#DaysAfterConsent', '#DaysOfIntervention','#DaysOfRecordedData',
                                               'First Consecutive 5 day mean', 'First Consecutive 5 day std',
                                               'Last Consecutive 5 day mean (<day 70)', 'Last Consecutive 5 day std'])

# Calculate the maximum width of values in each column
column_widths = {
    column: max(result_df[column].astype(str).apply(len).max(), len(column)) for column in result_df.columns
}

# Export the results to a new Excel file with stretched columns
output_file_path = 'SP23RestingHeartRateAnalysisV3.xlsx'
# Check if the file exists
if os.path.isfile(output_file_path):
    # Read the existing file
    existing_data = pd.read_excel(output_file_path)

    # Combine the existing data with the new data (assuming combined_df is your new data)
    combined_df = pd.concat([existing_data, result_df], ignore_index=True)
else:
    combined_df = result_df  # If the file doesn't exist, use only the new data

# Save the combined data to the Excel file
with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
    combined_df.to_excel(writer, sheet_name='RestingHeartRate', index=False)
    worksheet = writer.sheets['RestingHeartRate']
    for i, width in enumerate(column_widths.values()):
        worksheet.set_column(i, i, width)

print("Valid Participant IDs:")
print(valid_participant_ids)

print("\nInvalid Participant IDs (Not sufficient data or inconsistent dates or invalid data or too many gaps):")
print(invalid_participant_ids)
print(f'Results saved to {output_file_path}')







