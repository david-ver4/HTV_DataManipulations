import pandas as pd

# Load the Excel file
file_path = "SP23_dayTimeWearing.xlsx"
xls = pd.ExcelFile(file_path)

# Read data from "TotalMinutesWearTime" sheet and "TotalTimeInBed" sheet
minutes_wear_time = xls.parse("TotalMinutesWearTime", index_col=0)
time_in_bed = xls.parse("TotalTimeInBed", index_col=0)

# Subtract the data and store it in a new DataFrame
total_day_time_wear_time = minutes_wear_time.sub(time_in_bed, fill_value=0)

# Create a new Excel writer object
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
    # Write the result to a new sheet named "TotalDayTimeWearTime"
    total_day_time_wear_time.to_excel(writer, sheet_name="TotalDayTimeWearTime")

print("Subtraction completed and saved to TotalDayTimeWearTime sheet.")
