import pandas as pd
import glob
import chardet
import numpy as np

# Function to load all trip data files into a single "meta" DataFrame
def load_meta_trip_data(directory_path):
    trip_data_list = []
    for file_name in glob.glob(directory_path + 'Trip*.csv'):
        with open(file_name, 'rb') as file:
            result = chardet.detect(file.read())
            encoding = result['encoding']
        try:
            # Read each CSV file
            df = pd.read_csv(file_name, encoding=encoding, sep=';')
            df['File Name'] = file_name  # Add a column for the file name to keep track
            trip_data_list.append(df)   # Append each DataFrame to the list
        except Exception as e:
            print(f"Error reading {file_name}: {e}")
    
    # Concatenate all individual trip DataFrames into a single DataFrame
    meta_trip_df = pd.concat(trip_data_list, ignore_index=True)
    return meta_trip_df

# Process the meta DataFrame to extract last SoC [%] and mean Battery Temperature [°C]
def process_meta_trip_data(meta_trip_df):
    soc_and_temp_summary = []
    # Group by file name to process each trip individually
    for file_name, group_df in meta_trip_df.groupby('File Name'):
        # Last 'SoC [%]' value, handling NaNs
        last_soc_value = group_df['SoC [%]'].iloc[-1]
        if pd.isna(last_soc_value) and len(group_df['SoC [%]']) > 1:
            last_soc_value = group_df['SoC [%]'].iloc[-2]
            if pd.isna(last_soc_value) and len(group_df['SoC [%]']) > 2:
                last_soc_value = group_df['SoC [%]'].iloc[-3]
        
        # Mean of 'Battery Temperature [°C]', ignoring NaNs
        mean_battery_temp = group_df['Battery Temperature [°C]'].mean(skipna=True)
        
        # Append results for each trip
        soc_and_temp_summary.append((file_name, last_soc_value, mean_battery_temp))
    
    # Convert the list to a DataFrame for summary output
    summary_df = pd.DataFrame(soc_and_temp_summary, columns=['File Name', 'Last SoC [%] Value', 'Mean Battery Temperature [°C]'])
    return summary_df

# Function to process the overview data
def process_overview_data(file_path):
    df = pd.read_excel(file_path)
    df = df.drop(['Unnamed: 8', 'Unnamed: 13', 'Note'], axis=1)
    df = df.drop(index=[32,33]).reset_index(drop=True)
    return df

# Main function to combine and finalize the dataset
def create_final_dataset(overview_path, directory_path):
    # Load and process trip data
    meta_trip_df = load_meta_trip_data(directory_path)
    soc_temp_df = process_meta_trip_data(meta_trip_df)
    overview_df = process_overview_data(overview_path)
    
    # Check and align SoC data
    soc_overview = overview_df['Battery State of Charge (End)'].apply(lambda x: round(x * 100, 1))
    soc_compare = pd.concat([soc_overview, soc_temp_df['Last SoC [%] Value']], axis=1)
    
    # Fill NaN or 0 values in 'Last SoC [%] Value'
    for i in range(len(soc_compare)):
        if pd.isna(soc_compare['Last SoC [%] Value'].iloc[i]) or soc_compare['Last SoC [%] Value'].iloc[i] == 0:
            soc_compare['Last SoC [%] Value'].iloc[i] = soc_compare['Battery State of Charge (End)'].iloc[i]

    # Align Battery State of Charge (End)
    for i in range(len(soc_compare)):
        if soc_compare['Last SoC [%] Value'].iloc[i] != soc_compare['Battery State of Charge (End)'].iloc[i]:
            soc_compare['Battery State of Charge (End)'].iloc[i] = soc_compare['Last SoC [%] Value'].iloc[i]

    # Add necessary columns to overview
    overview_df['Mean Battery Temperature [°C]'] = soc_temp_df['Mean Battery Temperature [°C]'].apply(lambda x: round(x, 4))
    overview_df['Battery State of Charge (End)'] = soc_compare['Battery State of Charge (End)'].apply(lambda x: x / 100)
    overview_df.loc[35, 'Battery State of Charge (Start)'] = 0.854
    overview_df['Battery_consuming'] = overview_df['Battery State of Charge (Start)'] - overview_df['Battery State of Charge (End)']
    
    # Transform into the final data frame
    final_df = overview_df.drop(['Trip', 'Date', 'Battery Temperature (Start) [°C]', 'Battery Temperature (End)',
                                 'Battery State of Charge (Start)', 'Battery State of Charge (End)', 'Fan'], axis=1)
    object_cols = final_df.select_dtypes(include=['object']).columns
    final_df = pd.get_dummies(final_df, columns=object_cols, dtype=int)
    final_df = final_df.rename(columns={'Battery_consuming': 'SOC'})
    
    return final_df
