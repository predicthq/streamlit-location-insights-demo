import streamlit as st
# import datetime
# import pandas as pd
from utils.predicthq import (
    fetch_features,
    fetch_event_counts,
    calc_sum_of_features,
    calc_sum_of_event_counts,
    ATTENDED_CATEGORIES,
    NON_ATTENDED_CATEGORIES,
    PHQ_ATTENDANCE_FEATURES,
)
from utils.map import show_map


def show_metrics(
    lat, lon, radius, radius_unit, date_from, date_to, suggested_radius, tz="UTC"
):
    # Work out previous date range for delta comparisons
    previous_date_from = date_from - (date_to - date_from)
    previous_date_to = date_from

    # Fetch sum of Predicted Attendance
    phq_attendance_features = fetch_features(
        lat,
        lon,
        radius,
        date_from=date_from,
        date_to=date_to,
        features=PHQ_ATTENDANCE_FEATURES,
        radius_unit=radius_unit,
    )
    phq_attendance_sum = calc_sum_of_features(
        phq_attendance_features, PHQ_ATTENDANCE_FEATURES
    )

    # Fetch previous predicted attendance
    previous_phq_attendance_features = fetch_features(
        lat,
        lon,
        radius,
        date_from=previous_date_from,
        date_to=previous_date_to,
        features=PHQ_ATTENDANCE_FEATURES,
        radius_unit=radius_unit,
    )
    previous_phq_attendance_sum = calc_sum_of_features(
        previous_phq_attendance_features, PHQ_ATTENDANCE_FEATURES
    )

    # Work out average daily predicted attendance
    days = (date_to - date_from).days
    average_daily_attendance = phq_attendance_sum / days
    previous_average_daily_attendance = previous_phq_attendance_sum / days

    # Fetch event counts/stats
    counts = fetch_event_counts(
        lat,
        lon,
        radius,
        date_from=date_from,
        date_to=date_to,
        tz=tz,
        radius_unit=radius_unit,
    )
    attended_events_sum = calc_sum_of_event_counts(counts, ATTENDED_CATEGORIES)
    non_attended_events_sum = calc_sum_of_event_counts(counts, NON_ATTENDED_CATEGORIES)

    # Fetch event counts/stats for previous period
    previous_counts = fetch_event_counts(
        lat,
        lon,
        radius,
        date_from=previous_date_from,
        date_to=previous_date_to,
        tz=tz,
        radius_unit=radius_unit,
    )
    previous_attended_events_sum = calc_sum_of_event_counts(
        previous_counts, ATTENDED_CATEGORIES
    )
    previous_non_attended_events_sum = calc_sum_of_event_counts(
        previous_counts, NON_ATTENDED_CATEGORIES
    )

    # Fetch Demand Surges
    # demand_surges = fetch_demand_surges(
    #     lat,
    #     lon,
    #     radius,
    #     date_from=date_from,
    #     date_to=date_to,
    #     radius_unit=radius_unit,
    # )
    # demand_surges_count = len(demand_surges)

    # previous_demand_surges = fetch_demand_surges(
    #     lat,
    #     lon,
    #     radius,
    #     date_from=previous_date_from,
    #     date_to=previous_date_to,
    #     radius_unit=radius_unit,
    # )
    # previous_demand_surges_count = len(previous_demand_surges)

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    # Display metrics
    col12, col22, col32, col42 = st.columns(4)

    # with col1:
    #     st.metric(
    #         label="Suggested Radius",
    #         value=f"{suggested_radius['radius']}{suggested_radius['radius_unit']}",
    #         help="[Suggested Radius Docs](https://docs.predicthq.com/resources/suggested-radius)",
    #     )

    with col1:
        delta_pct = calc_delta_pct(phq_attendance_sum, previous_phq_attendance_sum)
        st.metric(
            label="**Predicted Attendance**",
            value=f"{phq_attendance_sum:,.0f}",
            delta=f"{delta_pct:,.0f}%",
            help=f"The predicted number of people attending events in the selected date range. Previous period: {previous_phq_attendance_sum:,.0f}.",
        )
    with col12:
        st.caption("Difference to previous 90 day period")

    with col2:
        delta_pct = calc_delta_pct(
            average_daily_attendance, previous_average_daily_attendance
        )
        st.metric(
            label="**Avg Daily Attendance**",
            value=f"{average_daily_attendance:,.0f}",
            delta=f"{delta_pct:,.0f}%",
            help=f"The average daily predicted number of people attending events in the selected date range. Previous period: {previous_average_daily_attendance:,.0f}.",
        )
    
    with col22:
        st.caption("Difference to previous 90 day period")

    with col3:
        delta_pct = calc_delta_pct(attended_events_sum, previous_attended_events_sum)
        st.metric(
            label="**Attended Events**",
            value=attended_events_sum,
            delta=f"{delta_pct:,.0f}%",
            help=f"Total number of attended events in the selected date range. Previous period: {previous_attended_events_sum}.",
        )

    with col32:
        st.caption("Difference to previous 90 day period")

    with col4:
        delta_pct = calc_delta_pct(
            non_attended_events_sum, previous_non_attended_events_sum
        )
        st.metric(
            label="**Holidays & Observances**",
            value=non_attended_events_sum,
            delta=f"{delta_pct:,.0f}%",
            help=f"Total number of non-attended events in the selected date range. Previous period: {previous_non_attended_events_sum}.",
        )
    
    with col42:
        st.caption("Difference to previous 90 day period")

    # with col5:
    #     delta_pct = calc_delta_pct(demand_surges_count, previous_demand_surges_count)
    #     st.metric(
    #         label="Demand Surges",
    #         value=demand_surges_count,
    #         delta=f"{delta_pct:,.0f}%",
    #         help=f"Number of [Demand Surges](https://docs.predicthq.com/resources/demand-surge) in the selected date range. Previous period: {previous_demand_surges_count}.",
    #     )


def calc_delta_pct(current, previous):
    return ((current - previous) / previous * 100) if previous > 0 else 0
