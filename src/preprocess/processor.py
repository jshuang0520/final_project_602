import chardet
import glob
import os
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder


# Data Preprocessing Class for the Overview DataFrame
class DataPreprocessor:
    def __init__(self, df):
        self.df = df.copy()

    def drop_columns(self, columns):
        self.df.drop(columns=columns, inplace=True, errors='ignore')
        return self

    def rename_columns(self, columns_map):
        self.df.rename(columns=columns_map, inplace=True)
        return self

    def clean_data(self):
        self.df.dropna(how="any", inplace=True)
        self.df.reset_index(drop=True, inplace=True)
        return self

    def drop_rows(self, condition):
        self.df = self.df[~condition]
        return self

    # def encode_categorical_columns(self, columns):
    #     encoder = OneHotEncoder(sparse=False, drop='first', dtype=int)
    #     encoded_data = pd.DataFrame(encoder.fit_transform(self.df[columns]),
    #                                 columns=encoder.get_feature_names_out(columns))
    #     self.df = pd.concat([self.df.drop(columns, axis=1), encoded_data], axis=1)
    #     return self
    
    def encode_categorical_columns(self, columns):
        encoder = OneHotEncoder(drop='first', dtype=int)
        encoded_array = encoder.fit_transform(self.df[columns])

        # Convert sparse matrix to dense if necessary
        if hasattr(encoded_array, 'toarray'):
            encoded_array = encoded_array.toarray()

        # Get feature names (compatible with both old and new versions)
        if hasattr(encoder, 'get_feature_names_out'):
            feature_names = encoder.get_feature_names_out(columns)
        else:
            feature_names = encoder.get_feature_names(columns)

        encoded_data = pd.DataFrame(encoded_array, columns=feature_names, index=self.df.index)
        self.df = pd.concat([self.df.drop(columns, axis=1), encoded_data], axis=1)
        return self

    def define_features_and_target(self, target_column):
        X = self.df.drop(target_column, axis=1)
        y = self.df[target_column]
        return X, y

    def split_data(self, X, y, test_size=0.2, random_state=42):
        return train_test_split(X, y, test_size=test_size, random_state=random_state)


# Trip Data Processing Class for Individual Trip CSV Files
class TripDataProcessor:
    def __init__(self, trip_df):
        self.trip_df = trip_df.copy()

    def extract_soc_values(self):
        soc_series = self.trip_df['SoC [%]'].dropna()
        first_soc, last_soc = soc_series.iloc[0], soc_series.iloc[-1]
        return first_soc, last_soc

    def calculate_mean_battery_temp(self):
        return self.trip_df['Battery Temperature [°C]'].mean()


# Class for Creating and Managing Metadata from Trip Data
class TripMetadataCreator:
    def __init__(self, trip_folder):
        self.trip_folder = trip_folder
        self.metadata = pd.DataFrame()
        
    def create_metadata(self):
        """Create a consolidated metadata file from all trip CSV files."""
        all_trip_data = []

        # Use a more specific pattern to match only TripA and TripB files
        file_pattern = os.path.join(self.trip_folder, 'Trip[AB]*.csv')

        # Get the list of files first
        files = glob.glob(file_pattern)
        total_files = len(files)

        for index, file_name in enumerate(files, start=1):
            # Extract trip identifier using regex
            match = re.match(r'Trip[AB]\d+', os.path.basename(file_name))
            if match:
                trip_identifier = match.group()
            else:
                print(f'Skipping file {index}/{total_files}: {os.path.basename(file_name)} (Does not match expected pattern)')
                continue  # Skip files that don't match the expected pattern

            with open(file_name, 'rb') as rawdata:
                charenc = chardet.detect(rawdata.read())['encoding']

            # Read the CSV into a DataFrame
            trip_df = pd.read_csv(file_name, sep=';', encoding=charenc)

            # Add trip identifier to each row
            trip_df['Trip'] = trip_identifier

            # Append this trip data to the overall list
            all_trip_data.append(trip_df)

            # Print progress and finished message
            print(f'{index}/{total_files} - Finished processing: {trip_identifier}')

        # Combine all trips into a single metadata DataFrame
        self.metadata = pd.concat(all_trip_data, ignore_index=True)

        print(f"\nMetadata created with {len(self.metadata)} rows from {len(all_trip_data)} trip files.")

    def save_metadata(self, output_file='metadata.csv'):
        """Save the metadata to a CSV file for future use."""
        self.metadata.to_csv(output_file, index=False)
        print(f"Metadata saved to {output_file}")

    def load_metadata(self, file_path):
        """Load existing metadata from a file."""
        self.metadata = pd.read_csv(file_path)
        print(f"Metadata loaded from {file_path} with {len(self.metadata)} rows.")
        return self.metadata

    def process_metadata(self):
        """Extract useful features and statistics from the metadata."""
        self.metadata['First SoC'] = self.metadata.groupby('Trip')['SoC [%]'].transform('first')
        self.metadata['Last SoC'] = self.metadata.groupby('Trip')['SoC [%]'].transform('last')
        self.metadata['Mean Battery Temp'] = self.metadata.groupby('Trip')['Battery Temperature [°C]'].transform('mean')
        return self.metadata


class OverviewDataProcessor(DataPreprocessor):
    def __init__(self, df):
        super().__init__(df)

    def merge_with_metadata(self, metadata):
        """
        Merge the overview dataframe with the processed metadata based on the 'Trip' identifier.
        """
        # Merge overview dataframe with metadata
        self.df = pd.merge(self.df, metadata, on='Trip', how='left')
        return self

    def calculate_soc_difference(self):
        """
        Calculate the difference in SoC between start and end values.
        """
        self.df['SoC Difference'] = self.df['First SoC'] - self.df['Last SoC']
        return self
    
    def encode_season(self):
        """Encodes 'Season' based on the month of the specified date column."""
        def get_season(date_string):
            try:
                # Extract the date part and convert to datetime
                date = pd.to_datetime(date_string.split('_')[0])
                month = date.month
                if 3 <= month <= 5:
                    return 'spring'
                elif 6 <= month <= 8:
                    return 'summer'
                elif 9 <= month <= 11:
                    return 'autumn'
                else:
                    return 'winter'
            except:
                return 'unknown'

        self.df['Season'] = self.df['Date'].apply(get_season)
        return self
