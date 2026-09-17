"""
Fonctions et constantes partagées entre les pages du dashboard.
"""

import pandas as pd
import streamlit as st

PERIOD_ORDER = ["Heures creuses", "Pointe matin (7h-10h)", "Pointe soir (16h-19h)"]


def bucket_period(hour: int) -> str:
    if 7 <= hour < 10:
        return "Pointe matin (7h-10h)"
    if 16 <= hour < 19:
        return "Pointe soir (16h-19h)"
    return "Heures creuses"


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("data/taxis.csv", parse_dates=["pickup", "dropoff"])
    df = df[df["distance"] > 0].copy()
    df["duration_min"] = (df["dropoff"] - df["pickup"]).dt.total_seconds() / 60
    df = df[df["duration_min"] > 0]

    df["fare_per_mile"] = df["fare"] / df["distance"]
    df["pace_min_per_mile"] = df["duration_min"] / df["distance"]
    df["pickup_hour"] = df["pickup"].dt.hour
    df["periode"] = df["pickup_hour"].apply(bucket_period)
    df["periode"] = pd.Categorical(df["periode"], categories=PERIOD_ORDER, ordered=True)

    df["pickup_borough"] = df["pickup_borough"].fillna("Inconnu")

    return df


def period_filter_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    """Affiche les filtres période et arrondissement puis renvoie le dataframe filtré."""
    st.sidebar.header("🔎 Filtre")
    selected_period = st.sidebar.multiselect(
        "Période de la journée", options=PERIOD_ORDER, default=PERIOD_ORDER
    )
    borough_options = sorted(df["pickup_borough"].dropna().unique())
    selected_boroughs = st.sidebar.multiselect(
        "Arrondissement de départ", options=borough_options, default=borough_options
    )
    filtered = df[
        df["periode"].isin(selected_period)
        & df["pickup_borough"].isin(selected_boroughs)
    ]
    st.sidebar.markdown(
        f"**{len(filtered):,}** courses sélectionnées sur {len(df):,}".replace(",", " ")
    )
    if filtered.empty:
        st.warning("Aucune course ne correspond au filtre sélectionné. Élargissez la sélection.")
        st.stop()
    return filtered
