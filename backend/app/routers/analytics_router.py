from fastapi import APIRouter, Query

from app.services.data_service import get_dataset_summary
from app.services.analytics_service import (
    get_top_states_by_median_aqi,
    get_worst_counties_by_max_aqi,
    get_most_unhealthy_counties,
    get_pollutant_summary,
    compare_states
)

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/summary")
def dataset_summary():
    return get_dataset_summary()


@router.get("/top-states")
def top_states(limit: int = Query(default=10, ge=1, le=50)):
    return get_top_states_by_median_aqi(limit)


@router.get("/worst-counties")
def worst_counties(limit: int = Query(default=10, ge=1, le=50)):
    return get_worst_counties_by_max_aqi(limit)


@router.get("/unhealthy-counties")
def unhealthy_counties(limit: int = Query(default=10, ge=1, le=50)):
    return get_most_unhealthy_counties(limit)


@router.get("/pollutants")
def pollutants():
    return get_pollutant_summary()


@router.get("/compare-states")
def compare_two_states(state1: str, state2: str):
    return compare_states(state1, state2)
