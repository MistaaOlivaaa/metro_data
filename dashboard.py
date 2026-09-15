from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIRECTORY = PROJECT_ROOT / "data" / "processed"


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    routes = pd.read_csv(DATA_DIRECTORY / "routes_clean.csv", dtype=str)
    trips = pd.read_csv(DATA_DIRECTORY / "trips_clean.csv", dtype=str)
    stops = pd.read_csv(DATA_DIRECTORY / "stops_clean.csv", dtype=str)
    stop_times = pd.read_csv(DATA_DIRECTORY / "stop_times_clean.csv", dtype=str)
    return routes, trips, stops, stop_times


st.set_page_config(page_title="Ilevia Dashboard", page_icon="I", layout="wide")
st.title("Ilevia Dashboard")
st.caption("Exploration des lignes, trajets et arrets du reseau Ilevia")

routes, trips, stops, stop_times = load_data()

route_counts = trips.groupby("route_id").size().rename("trip_count").reset_index()
route_table = routes.merge(route_counts, on="route_id", how="left").fillna({"trip_count": 0})
route_table["trip_count"] = route_table["trip_count"].astype(int)

route_options = route_table.sort_values("route_short_name")[
    ["route_id", "route_short_name", "route_long_name"]
].drop_duplicates()
route_labels = {
    row.route_id: f"{row.route_short_name} - {row.route_long_name}"
    for row in route_options.itertuples()
}

with st.sidebar:
    st.header("Filtres")
    selected_route = st.selectbox(
        "Ligne",
        options=["Toutes les lignes", *route_options["route_id"].tolist()],
        format_func=lambda route_id: route_id
        if route_id == "Toutes les lignes"
        else route_labels[route_id],
    )

filtered_trips = trips
if selected_route != "Toutes les lignes":
    filtered_trips = trips[trips["route_id"] == selected_route]

metric_columns = st.columns(4)
metric_columns[0].metric("Lignes", f"{len(route_table):,}".replace(",", " "))
metric_columns[1].metric("Arrets", f"{len(stops):,}".replace(",", " "))
metric_columns[2].metric("Trajets", f"{len(filtered_trips):,}".replace(",", " "))
metric_columns[3].metric(
    "Horaires", f"{len(stop_times):,}".replace(",", " ")
)

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Trajets par ligne")
    chart_data = route_table.sort_values("trip_count", ascending=False).head(20)
    st.bar_chart(chart_data.set_index("route_short_name")["trip_count"])

with right_column:
    st.subheader("Lignes selectionnees")
    visible_routes = route_table
    if selected_route != "Toutes les lignes":
        visible_routes = visible_routes[visible_routes["route_id"] == selected_route]
    st.dataframe(
        visible_routes[
            ["route_short_name", "route_long_name", "route_type", "trip_count"]
        ].sort_values("trip_count", ascending=False),
        hide_index=True,
        use_container_width=True,
    )

st.subheader("Carte des arrets")
map_data = stops[["stop_name", "stop_lat", "stop_lon"]].copy()
map_data["lat"] = pd.to_numeric(map_data["stop_lat"], errors="coerce")
map_data["lon"] = pd.to_numeric(map_data["stop_lon"], errors="coerce")
map_data = map_data.dropna(subset=["lat", "lon"])[["lat", "lon"]]
st.map(map_data)

st.subheader("Apercu des trajets")
st.dataframe(filtered_trips.head(100), hide_index=True, use_container_width=True)
