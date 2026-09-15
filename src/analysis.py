import pandas as pd


def route_summary(routes: pd.DataFrame, trips: pd.DataFrame) -> pd.DataFrame:
    """Return the number of trips associated with each route."""
    trip_counts = trips.groupby("route_id").size().rename("trip_count")
    columns = ["route_id", "route_short_name", "route_long_name"]
    available = [column for column in columns if column in routes.columns]
    return routes[available].drop_duplicates().merge(
        trip_counts, on="route_id", how="left"
    ).fillna({"trip_count": 0}).sort_values("trip_count", ascending=False)


def stop_usage(stop_times: pd.DataFrame) -> pd.DataFrame:
    """Count scheduled stop-time records for every stop."""
    return (
        stop_times.groupby("stop_id")
        .size()
        .rename("stop_time_count")
        .reset_index()
        .sort_values("stop_time_count", ascending=False)
    )
