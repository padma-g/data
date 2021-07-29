'''
Author: Padma Gundapaneni @padma-g
This script will generate a cleaned CDC air quality data file.
Run "python3 parse_air_quality.py.
'''
import sys
import pandas as pd

# Mapping of column names in file to StatVar names.
STATVARS = {
    "DS_PM_pred": "Mean_Concentration_AirPollutant_PM2.5",
    "DS_O3_pred": "Mean_Concentration_AirPollutant_Ozone",
    "PM25_max_pred": "Max_Concentration_AirPollutant_PM2.5",
    "PM25_med_pred": "Median_Concentration_AirPollutant_PM2.5",
    "PM25_mean_pred": "Mean_Concentration_AirPollutant_PM2.5",
    "PM25_pop_pred": "PopulationWeighted_Concentration_AirPollutant_PM2.5",
    "O3_max_pred": "Max_Concentration_AirPollutant_Ozone",
    "O3_med_pred": "Median_Concentration_AirPollutant_Ozone",
    "O3_mean_pred": "Mean_Concentration_AirPollutant_Ozone",
    "O3_pop_pred": "PopulationWeighted_Concentration_AirPollutant_Ozone"
}

# Mapping of month abbreviations to month numbers.
MONTH_MAP = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12
}


def main():
    """Main function to generate the cleaned csv file."""
    file_path = sys.argv[1]
    output_file = sys.argv[2]
    clean_air_quality_data(file_path, output_file)


def clean_air_quality_data(file_path, output_file):
    """
    Args:
        file_path: path to a comma-separated CDC air quality data file
        output_file: path for the cleaned csv to be stored
    Returns:
        a cleaned csv file
    """
    print("Cleaning file...")
    data = pd.read_csv(file_path)
    if "Ozone" in file_path and "County" in file_path:
        data["Month"] = data["Month"].map(MONTH_MAP)
        data["date"] = pd.to_datetime(data[["Year", "Month", "Day"]],
                                      yearfirst=True)
    else:
        data["date"] = pd.to_datetime(data["date"], yearfirst=True)
    if "PM2.5" in file_path:
        census_tract = "DS_PM"
    elif "Ozone" in file_path:
        census_tract = "DS_O3"
    if "Census" in file_path:
        data = pd.melt(data,
                       id_vars=[
                           'year', 'date', 'statefips', 'countyfips', 'ctfips',
                           'latitude', 'longitude', census_tract + '_stdd'
                       ],
                       value_vars=[str(census_tract + '_pred')],
                       var_name='StatisticalVariable',
                       value_name='Value')
        data.rename(columns={census_tract + '_stdd': 'Error'}, inplace=True)
        data["dcid"] = "geoId/" + data["ctfips"].astype(str)
        data['StatisticalVariable'] = data['StatisticalVariable'].map(STATVARS)
    elif "County" in file_path and "PM" in file_path:
        data["countyfips"] = "1200" + data["countyfips"].astype(str)
        data["dcid"] = "geoId/" + data["countyfips"].astype(str)
    elif "County" in file_path and "Ozone" in file_path:
        data["countyfips"] = "1200" + data["countyfips"].astype(str)
        data["dcid"] = "geoId/" + data["countyfips"].astype(str)
    data.to_csv(output_file)
    print("Finished cleaning file!")


if __name__ == "__main__":
    main()