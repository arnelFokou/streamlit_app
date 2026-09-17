"""Page 1 — Tendance horaire du volume de courses."""

import plotly.express as px
import streamlit as st

from utils import load_data, period_filter_sidebar

st.set_page_config(page_title="Tendance horaire — Demande", page_icon="📈", layout="wide")

df = load_data()
filtered = period_filter_sidebar(df)

# ----------------------------------------------------------------------------
# Titre — porte le message de CETTE page
# ----------------------------------------------------------------------------
st.title("📈 La demande de courses varie fortement selon l'heure")

# ----------------------------------------------------------------------------
# Données horaires (calculées une seule fois, utilisées par le KPI et le graphique)
# ----------------------------------------------------------------------------
hourly_volume = (
    filtered.groupby("pickup_hour")
    .size()
    .reindex(range(24), fill_value=0)
    .rename("course_count")
    .reset_index()
)
peak_row = hourly_volume.loc[hourly_volume["course_count"].idxmax()]
trough_row = hourly_volume.loc[hourly_volume["course_count"].idxmin()]
peak_share = peak_row["course_count"] / len(filtered) * 100

# ----------------------------------------------------------------------------
# KPIs — uniquement ceux qui concernent CETTE visualisation
# ----------------------------------------------------------------------------
col1, col2, col3 = st.columns(3)
col1.metric(
    "Heure avec le plus de courses",
    f"{int(peak_row['pickup_hour'])}h",
    delta=f"{int(peak_row['course_count']):,} courses".replace(",", " "),
)
col2.metric(
    "Heure avec le moins de courses",
    f"{int(trough_row['pickup_hour'])}h",
    delta=f"{int(trough_row['course_count']):,} courses".replace(",", " "),
)
col3.metric(
    "Part des courses à l'heure de pointe",
    f"{peak_share:,.1f} %".replace(",", " "),
    help="Part des courses filtrées concentrée sur l'heure qui en compte le plus.",
)

st.divider()

# ----------------------------------------------------------------------------
# Visuel unique de cette page
# ----------------------------------------------------------------------------
st.subheader("Nombre de courses par heure (0h-23h)")

fig_line = px.bar(
    hourly_volume,
    x="pickup_hour",
    y="course_count",
    labels={"pickup_hour": "Heure de la journée", "course_count": "Nombre de courses"},
)
fig_line.update_traces(
    marker_color="#c94c4c",
    hovertemplate="%{x}h — %{y} courses<extra></extra>",
)
fig_line.add_vrect(
    x0=16, x1=19, fillcolor="#c94c4c", opacity=0.10, line_width=0,
    annotation_text="Pointe soir", annotation_position="top left",
    annotation_font_color="#c94c4c", annotation_font_size=12,
)
fig_line.add_annotation(
    x=peak_row["pickup_hour"], y=peak_row["course_count"],
    text=f"Pic : {int(peak_row['course_count'])} courses à {int(peak_row['pickup_hour'])}h",
    showarrow=True, arrowhead=2, arrowcolor="#c94c4c",
    ax=0, ay=-40, font=dict(color="#c94c4c", size=13, family="Arial Black"),
)
fig_line.update_layout(
    height=480,
    xaxis=dict(dtick=2, title="Heure de la journée", showgrid=False),
    yaxis=dict(title="Nombre de courses", gridcolor="rgba(0,0,0,0.06)"),
    plot_bgcolor="white",
    margin=dict(t=60),
)
st.plotly_chart(fig_line, use_container_width=True)

st.markdown(
    "**Ce que ce visuel communique :** la demande n'est pas répartie uniformément dans la "
    "journée. Cette lecture du volume complète la page « Prix par période », qui mesure "
    "la rentabilité moyenne au mile."
)
