import pandas as pd

# Load the Excel file
xls = pd.ExcelFile('../Resources/Seasonally Adjusted.xlsx')

# For each sheet in the Excel file
for sheet_name in xls.sheet_names:
    # Load the sheet to a DataFrame
    df = xls.parse(sheet_name)
    
    # Save the DataFrame to a CSV file
    df.to_csv(f"../Resources/{sheet_name}.csv", index=False)