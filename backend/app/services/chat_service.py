from app.services.analytics_service import (
    get_top_states_by_median_aqi,
    get_worst_counties_by_max_aqi,
    get_most_unhealthy_counties,
    get_pollutant_summary,
    compare_states
)

from app.services.llm_service import generate_explanation


def build_response(question: str, intent: str, data, chart=None):
    """
    Builds final response using Gemini explanation + calculated data + chart metadata.
    """
    explanation = generate_explanation(question, intent, data)

    return {
        "answer": explanation,
        "intent": intent,
        "data": data,
        "chart": chart
    }


def answer_question(question: str):
    """
    Maps user questions to trusted pandas calculations.
    Gemini explains the result, but pandas produces the actual numbers.
    """

    q = question.lower()

    if (
        "top state" in q
        or "top states" in q
        or "worst state" in q
        or "highest median" in q
        or "median aqi" in q
    ):
        data = get_top_states_by_median_aqi(limit=10)

        chart = {
            "type": "bar",
            "x_key": "State",
            "y_key": "Median AQI",
            "title": "Top States by Average Median AQI"
        }

        return build_response(question, "top_states_by_median_aqi", data, chart)

    elif "worst count" in q or "max aqi" in q or "highest max" in q:
        data = get_worst_counties_by_max_aqi(limit=10)

        chart = {
            "type": "bar",
            "x_key": "County",
            "y_key": "Max AQI",
            "title": "Worst Counties by Max AQI"
        }

        return build_response(question, "worst_counties_by_max_aqi", data, chart)

    elif "unhealthy" in q:
        data = get_most_unhealthy_counties(limit=10)

        chart = {
            "type": "bar",
            "x_key": "County",
            "y_key": "Total Unhealthy Days",
            "title": "Counties with Most Unhealthy Days"
        }

        return build_response(question, "most_unhealthy_counties", data, chart)

    elif (
        "pollutant" in q
        or "pm2.5" in q
        or "ozone" in q
        or "co" in q
        or "no2" in q
        or "pm10" in q
    ):
        data = get_pollutant_summary()

        chart = {
            "type": "bar",
            "x_key": "pollutant",
            "y_key": "days",
            "title": "AQI Days by Dominant Pollutant"
        }

        return build_response(question, "pollutant_summary", data, chart)

    elif "compare" in q and "california" in q and "texas" in q:
        data = compare_states("California", "Texas")

        chart = {
            "type": "bar",
            "x_key": "State",
            "y_key": "Median AQI",
            "title": "California vs Texas: Average Median AQI"
        }

        return build_response(question, "compare_california_texas", data, chart)

    else:
        return {
            "answer": (
                "I can answer questions about top states by Median AQI, worst counties by Max AQI, "
                "unhealthy air-quality days, pollutant summary, and California vs Texas comparison."
            ),
            "intent": "unknown",
            "data": None,
            "chart": None
        }
