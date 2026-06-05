import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "annual_aqi_by_county_2024.csv"

VALID_US_STATES = {
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "District Of Columbia", "Florida", "Georgia",
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota",
    "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island",
    "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
}


def load_aqi_data():
    """
    Loads and cleans the EPA AQI CSV dataset.
    """
    df = pd.read_csv(DATA_PATH)

    # Clean column names and text values
    df.columns = df.columns.str.strip()
    df["State"] = df["State"].astype(str).str.strip()

    # Keep only valid US states + DC
    df = df[df["State"].isin(VALID_US_STATES)]

    return df


def get_dataset_summary():
    df = load_aqi_data()

    return {
        "rows": int(len(df)),
        "columns": list(df.columns),
        "states_count": int(df["State"].nunique()),
        "counties_count": int(df["County"].nunique()),
        "year_min": int(df["Year"].min()),
        "year_max": int(df["Year"].max())
    }
