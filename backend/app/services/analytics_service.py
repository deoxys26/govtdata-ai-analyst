from app.services.data_service import load_aqi_data


def get_top_states_by_median_aqi(limit: int = 10):
    """
    Finds states with highest average Median AQI.
    Higher AQI means worse air quality.
    """
    df = load_aqi_data()

    result = (
        df.groupby("State")["Median AQI"]
        .mean()
        .sort_values(ascending=False)
        .head(limit)
        .reset_index()
    )

    result["Median AQI"] = result["Median AQI"].round(2)

    return result.to_dict(orient="records")


def get_worst_counties_by_max_aqi(limit: int = 10):
    """
    Finds counties with highest Max AQI.
    """
    df = load_aqi_data()

    result = (
        df[["State", "County", "Max AQI"]]
        .sort_values(by="Max AQI", ascending=False)
        .head(limit)
    )

    return result.to_dict(orient="records")


def get_most_unhealthy_counties(limit: int = 10):
    """
    Finds counties with most unhealthy air quality days.
    Combines multiple unhealthy categories.
    """
    df = load_aqi_data()

    df["Total Unhealthy Days"] = (
        df["Unhealthy for Sensitive Groups Days"]
        + df["Unhealthy Days"]
        + df["Very Unhealthy Days"]
        + df["Hazardous Days"]
    )

    result = (
        df[["State", "County", "Total Unhealthy Days"]]
        .sort_values(by="Total Unhealthy Days", ascending=False)
        .head(limit)
    )

    return result.to_dict(orient="records")


def get_pollutant_summary():
    """
    Shows how many AQI days were dominated by each pollutant.
    """
    df = load_aqi_data()

    pollutant_columns = [
        "Days CO",
        "Days NO2",
        "Days Ozone",
        "Days PM2.5",
        "Days PM10"
    ]

    summary = []

    for col in pollutant_columns:
        summary.append({
            "pollutant": col.replace("Days ", ""),
            "days": int(df[col].sum())
        })

    summary = sorted(summary, key=lambda x: x["days"], reverse=True)

    return summary


def compare_states(state1: str, state2: str):
    """
    Compares two states using AQI metrics.
    """
    df = load_aqi_data()

    filtered = df[df["State"].isin([state1, state2])]

    result = (
        filtered.groupby("State")
        .agg({
            "Good Days": "sum",
            "Moderate Days": "sum",
            "Unhealthy Days": "sum",
            "Max AQI": "max",
            "Median AQI": "mean"
        })
        .reset_index()
    )

    result["Median AQI"] = result["Median AQI"].round(2)

    return result.to_dict(orient="records")
