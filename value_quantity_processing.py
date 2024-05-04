import pandas as pd
from pathlib import Path

def process_files_and_save_prices(folder_path):
    folder_path = Path(folder_path)
    final_data = {}

    # Read and process files for each year
    for year in range(2015, 2022):
        file_path = folder_path / f"{year}.csv"
        
        data = pd.read_csv(file_path, dtype={'Product': str})
        data['Value'] = pd.to_numeric(data['Value'].replace({',': ''}, regex=True), errors='coerce')
        data['First Quantity'] = pd.to_numeric(data['First Quantity'].replace({',': ''}, regex=True), errors='coerce')
        data['Second Quantity'] = pd.to_numeric(data['Second Quantity'].replace({',': ''}, regex=True), errors='coerce')

        data.fillna(0, inplace=True)

        data['HS 6'] = data['Product'].str[:6]
        grouped = data.groupby('HS 6').agg({
            'First Quantity': 'sum',
            'Second Quantity': 'sum',
            'Value': 'sum'
        }).reset_index()

        grouped['Total Quantity'] = grouped['First Quantity'] + grouped['Second Quantity']
        grouped['Price'] = grouped.apply(lambda x: x['Value'] / x['Total Quantity'] if x['Total Quantity'] > 0 else 0, axis=1)

        # Rename the 'Price' column to the year it represents
        grouped.rename(columns={'Price': f'Price_{year}'}, inplace=True)

        # Store the result in the final_data dictionary
        final_data[year] = grouped[['HS 6', f'Price_{year}']]

    # Merge all the dataframes on 'HS 6'
    final_df = pd.DataFrame()
    for year, df in final_data.items():
        if final_df.empty:
            final_df = df
        else:
            final_df = final_df.merge(df, on='HS 6', how='outer')

    # Save the merged dataframe to a single Excel file
    final_df.to_excel(folder_path / "HS6_Prices_All_Years.xlsx", index=False)

    print("Processing complete. The consolidated file has been saved.")
    
def process_files_and_save_values_prices(folder_path):
    folder_path = Path(folder_path)
    final_data = {}

    # Read and process files for each year
    for year in range(2015, 2022):
        file_path = folder_path / f"{year}.csv"
        
        data = pd.read_csv(file_path, dtype={'Product': str})
        data['Value'] = pd.to_numeric(data['Value'].replace({',': ''}, regex=True), errors='coerce')
        data['First Quantity'] = pd.to_numeric(data['First Quantity'].replace({',': ''}, regex=True), errors='coerce')
        data['Second Quantity'] = pd.to_numeric(data['Second Quantity'].replace({',': ''}, regex=True), errors='coerce')

        data.fillna(0, inplace=True)

        data['HS 6'] = data['Product'].str[:6]
        grouped = data.groupby('HS 6').agg({
            'First Quantity': 'sum',
            'Second Quantity': 'sum',
            'Value': 'sum'
        }).reset_index()

        grouped['Total Quantity'] = grouped['First Quantity'] + grouped['Second Quantity']
        grouped['Price'] = grouped.apply(lambda x: x['Value'] / x['Total Quantity'] if x['Total Quantity'] > 0 else 0, axis=1)

        # Save the Value and Price under the respective year columns
        grouped.rename(columns={'Value': f'Value_{year}', 'Price': f'Price_{year}'}, inplace=True)

        # Store the result in the final_data dictionary
        final_data[year] = grouped[['HS 6', f'Value_{year}', f'Price_{year}']]

    # Merge all the dataframes on 'HS 6'
    final_df = pd.DataFrame()
    for year, df in final_data.items():
        if final_df.empty:
            final_df = df
        else:
            final_df = final_df.merge(df, on='HS 6', how='outer')

    # Save the merged dataframe to a single Excel file
    final_df.to_excel(folder_path / "HS6_Values_and_Prices_All_Years.xlsx", index=False)

    print("Processing complete. The consolidated file has been saved.")

# Set the path to the folder containing the Excel files
folder_path = 'Data/Import Value and Quantities from US to China/'

# Call the function with the folder path
process_files_and_save_prices(folder_path)
process_files_and_save_values_prices(folder_path)