# HTV_DataManipulations README

This repository contains code files for data cleaning and analysis related to Happy Teacher Study.

## Data Cleaning Scripts

### 1. Data_Cleaning_v03_RC(1).ipynb

- **Purpose:** Designed to turn raw files into usable clean datasets.
- **Usage:**
  - Use raw datasets directly exported from fitabase.
  - In the second box, uncomment to filter and produce a new weartime file with 0s allocated to invalid datapoints.
  - Use cleaned weartime dataset generated from normal running and file generating made using this script.

### 2. compareConsentDates.py

- **Purpose:** Optional tool to compare consent dates between raw consent date and raw dataset to identify potential inequivalencies.
- **Usage:**
  - Use consent date file and the raw dataset.

### 3. findConsentDates.py

- **Purpose:** Optional tool to identify and make a consent date file for beta testing.

### 4. zeroAllocate.py

- **Purpose:** Based on Wear Time threshold 10-hour invalid limit, allocate zeros to another dataset.
- **Usage:**
  - Use cleaned and filtered threshold weartime dataset as the base to allocate 0s to another non-weartime dataset.

## WeekendWeekdayAligning Scripts

### 1. DATESHIFTERfinal.py

- **Purpose:** Using the earliest consent date as the reference date, this is designed to alter the cleaned data sets in a way where constant dates are established instead of numbered days for the first row and every data point aligns with its corresponding date for each participant.
- **Usage:**
  - Use clean and filtered threshold datasets.

### 2. aligner.py

- **Purpose:** Optional tool to print out differences between reference date and first dates of each participant.

### 3. daytimesubtract.py

- **Purpose:** Create another variable and Excel sheet called TotalDayTimeWearTime.
- **Usage:**
  - Takes the difference between TotalMinutesWearTime and TotalTimeInBed.

### 4. weekendHighlights.py

- **Purpose:** Optional tool to highlight data points that align on weekend dates.

### 5. weeklyaverages.py

- **Purpose:** Generate a new file consisting of weekday and weekend averages for each participant.
- **Usage:**
  - Use file generated from DATESHIFTERfinal.py script.

## Data Analysis Code

### 1. Data_Cleaning_Analysis.py

- **Purpose:** Generate average and standard deviations of first and last consecutive 5-day spans with inclusion of number of days statistics related to study.
- **Usage:**
  - Use clean and filtered threshold datasets.
