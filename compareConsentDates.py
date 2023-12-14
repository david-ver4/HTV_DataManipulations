import pandas as pd

def compare_ids(csv_file_path, excel_file_path):
    # Read the CSV file into a DataFrame
    df_csv = pd.read_csv(csv_file_path)

    # Read the Excel file into a DataFrame
    df_excel = pd.read_excel(excel_file_path)

    # Extract lists of unique IDs from both DataFrames
    ids_csv = set(df_csv['Id'])
    ids_excel = set(df_excel['ID'])

    # Find IDs that are in one list but not in the other
    ids_only_in_csv = ids_csv - ids_excel
    ids_only_in_excel = ids_excel - ids_csv

    return ids_only_in_csv, ids_only_in_excel

# Replace with 'your_excel_file_path/Fall_23_consent_dates.xlsx'
# with the actual paths to your CSV and Excel files
csv_file_path = 'fitbitWearTimeViaHR_merged.csv'
excel_file_path = 'Fall23_consent_dates.xlsx'

try:
    ids_only_in_csv, ids_only_in_excel = compare_ids(csv_file_path, excel_file_path)

    print('IDs present only in the CSV file:')
    print(ids_only_in_csv)

    print('\nIDs present only in the Excel file:')
    print(ids_only_in_excel)

except FileNotFoundError as e:
    print(f'File not found: {e.filename}')
except Exception as e:
    print(f'An error occurred: {e}')
