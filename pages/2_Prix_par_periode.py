"""
Page 2 — Prix au mile par période de la journée.
Message : la pointe du soir (16h-19h) coûte le plus cher au mile.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from utils import PERIOD_ORDER, load_data, period_filter_sidebar

st.set_page_config(page_title="Prix par période — Prix au mile", page_icon="📊", layout="wide")

df = load_data()
filtered = period_filter_sidebar(df)

# ----------------------------------------------------------------------------
# Titre — porte le message de CETTE page
# ----------------------------------------------------------------------------
st.title("📊 La pointe du soir (16h-19h) coûte le plus cher au mile")

# ----------------------------------------------------------------------------
# Données par période (calculées une seule fois, utilisées par le KPI et le graphique)
# ----------------------------------------------------------------------------
off_peak_fpm = df.loc[df["periode"] == "Heures creuses", "fare_per_mile"].mean()
period_fpm = filtered.groupby("periode", observed=True)["fare_per_mile"].mean()
evening_fpm = period_fpm.get("Pointe soir (16h-19h)", float("nan"))

evening_revenue_share = (
    filtered.loc[filtered["periode"] == "Pointe soir (16h-19h)", "fare"].sum()
    / filtered["fare"].sum()
    * 100
    if filtered["fare"].sum() > 0 else 0
)

# ----------------------------------------------------------------------------
# KPIs — uniquement ceux qui concernent CETTE visualisation
# ----------------------------------------------------------------------------
col1, col2, col3 = st.columns(3)
col1.metric(
    "Prix moyen au mile — pointe soir",
    f"{evening_fpm:,.2f} $/mile" if pd.notna(evening_fpm) else "n/a",
    delta=f"{(evening_fpm - off_peak_fpm):+.2f} $ vs heures creuses" if pd.notna(evening_fpm) else None,
)
col2.metric(
    "Prix moyen au mile — heures creuses",
    f"{off_peak_fpm:,.2f} $/mile" if pd.notna(off_peak_fpm) else "n/a",
)
col3.metric(
    "Part du CA généré en pointe soir",
    f"{evening_revenue_share:,.0f} %",
    help="Part du chiffre d'affaires filtré généré par les seules courses de 16h-19h.",
)

st.divider()

# ----------------------------------------------------------------------------
# Visuel unique de cette page
# ----------------------------------------------------------------------------
st.subheader("La pointe du soir (16h-19h) coûte le plus cher au mile")

period_fpm_df = period_fpm.reindex(PERIOD_ORDER).dropna().reset_index()
period_fpm_df["label"] = period_fpm_df["fare_per_mile"].map(lambda v: f"${v:.2f}")

fig_fpm = px.bar(
    period_fpm_df,
    x="periode",
    y="fare_per_mile",
    color="periode",
    text="label",
    labels={"periode": "Période", "fare_per_mile": "Prix moyen / mile ($)"},
    category_orders={"periode": PERIOD_ORDER},
    color_discrete_map={
        "Heures creuses": "#a8b3c1",
        "Pointe matin (7h-10h)": "#f2a65a",
        "Pointe soir (16h-19h)": "#c94c4c",
    },
)
fig_fpm.update_traces(
    textposition="outside",
    textfont=dict(size=15, family="Arial Black"),
    marker_line_width=0,
    width=0.55,
)
fig_fpm.update_layout(
    height=480,
    showlegend=False,
    xaxis=dict(title=None, showgrid=False),
    yaxis=dict(title="Prix moyen / mile ($)", tickprefix="$", gridcolor="rgba(0,0,0,0.06)"),
    plot_bgcolor="white",
    margin=dict(t=40),
    uniformtext_minsize=12,
)
st.plotly_chart(fig_fpm, use_container_width=True)

st.markdown(
    "**Ce que ce visuel communique :** le prix moyen au mile grimpe nettement en pointe "
    "soir par rapport aux heures creuses — c'est le chiffre central du message : cette "
    "fenêtre horaire est la plus rentable au mile parcouru, et mérite qu'on y concentre "
    "davantage de chauffeurs."
)
