import matplotlib.pyplot as plt
import pandas as pd


def plot_route_summary(summary: pd.DataFrame, limit: int = 15) -> None:
    """Plot the routes with the most scheduled trips."""
    selected = summary.head(limit).sort_values("trip_count")
    labels = selected["route_short_name"].fillna(selected["route_id"])
    selected.assign(route=labels).plot.barh(x="route", y="trip_count", legend=False)
    plt.xlabel("Nombre de trajets")
    plt.ylabel("Ligne")
    plt.title("Lignes avec le plus de trajets")
    plt.tight_layout()
    plt.show()
