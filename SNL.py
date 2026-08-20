import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Island Cruises - Forecast P&L",
    page_icon="⛵",
    layout="wide"
)

st.title("⛵ Dashboard Forecast P&L - Island Cruises")


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Forecast Simulation")


# ============================================================
# SEASON
# ============================================================

st.sidebar.subheader("📅 Season")

date_debut = st.sidebar.date_input(
    "Season Start",
    value=date(2027, 5, 1)
)

date_fin = st.sidebar.date_input(
    "End of season",
    value=date(2027, 9, 30)
)


# ============================================================
# CALENDAR VALIDATION
# ============================================================

if date_fin <= date_debut:

    st.error(
        "Ending date must be superior than starting date."
    )

    st.stop()


# ============================================================
# CALENDAR CREATION
# ============================================================

dates = pd.date_range(
    start=date_debut,
    end=date_fin,
    freq="D"
)

df = pd.DataFrame({
    "date": dates
})

df["month"] = df["date"].dt.month
df["year"] = df["date"].dt.year
df["month_name"] = df["date"].dt.strftime("%B")

# Gestion d'une saison sur plusieurs années

df["year_month"] = df["date"].dt.to_period("M")


# ============================================================
# MONTHS PRESENT IN THE SEASON
# ============================================================

months_in_season = (
    df[["year_month"]]
    .drop_duplicates()
    .sort_values("year_month")
)


# ============================================================
# DEFAULT MONTHLY PARAMETERS
# ============================================================

default_parameters = {

    1: {
        "people_per_cruise": 5,
        "price": 100.0,
        "cruises_per_day": 2.0,
        "filling_rate": 60
    },

    2: {
        "people_per_cruise": 5,
        "price": 100.0,
        "cruises_per_day": 2.0,
        "filling_rate": 60
    },

    3: {
        "people_per_cruise": 5,
        "price": 110.0,
        "cruises_per_day": 2.5,
        "filling_rate": 65
    },

    4: {
        "people_per_cruise": 5,
        "price": 120.0,
        "cruises_per_day": 3.0,
        "filling_rate": 70
    },

    5: {
        "people_per_cruise": 5,
        "price": 110.0,
        "cruises_per_day": 2.5,
        "filling_rate": 70
    },

    6: {
        "people_per_cruise": 5,
        "price": 125.0,
        "cruises_per_day": 3.0,
        "filling_rate": 75
    },

    7: {
        "people_per_cruise": 5,
        "price": 140.0,
        "cruises_per_day": 4.0,
        "filling_rate": 90
    },

    8: {
        "people_per_cruise": 5,
        "price": 150.0,
        "cruises_per_day": 4.5,
        "filling_rate": 95
    },

    9: {
        "people_per_cruise": 5,
        "price": 120.0,
        "cruises_per_day": 3.0,
        "filling_rate": 75
    },

    10: {
        "people_per_cruise": 5,
        "price": 110.0,
        "cruises_per_day": 2.5,
        "filling_rate": 70
    },

    11: {
        "people_per_cruise": 5,
        "price": 100.0,
        "cruises_per_day": 2.0,
        "filling_rate": 60
    },

    12: {
        "people_per_cruise": 5,
        "price": 100.0,
        "cruises_per_day": 2.0,
        "filling_rate": 60
    }
}


# ============================================================
# MONTHLY ASSUMPTIONS
# ============================================================

st.sidebar.subheader("📊 Monthly Assumptions")

monthly_parameters = {}


for _, row in months_in_season.iterrows():

    year_month = row["year_month"]

    month_number = year_month.month

    month_name = year_month.strftime("%B %Y")

    defaults = default_parameters[month_number]


    # --------------------------------------------------------
    # MONTH EXPANDER
    # --------------------------------------------------------

    with st.sidebar.expander(
        f"📅 {month_name}",
        expanded=False
    ):


        # ----------------------------------------------------
        # PEOPLE PER CRUISE
        # ----------------------------------------------------

        people_per_cruise = st.number_input(

            "People / cruise",

            min_value=1,

            max_value=13,

            value=int(
                defaults["people_per_cruise"]
            ),

            step=1,

            key=f"people_{year_month}"
        )


        # ----------------------------------------------------
        # PRICE PER PERSON
        # ----------------------------------------------------

        price = st.number_input(

            "Price / person (€)",

            min_value=0.0,

            value=float(
                defaults["price"]
            ),

            step=5.0,

            key=f"price_{year_month}"
        )


        # ----------------------------------------------------
        # CRUISES PER DAY
        # ----------------------------------------------------

        cruises_per_day = st.number_input(

            "Cruises / day",

            min_value=0.0,

            max_value=20.0,

            value=float(
                defaults["cruises_per_day"]
            ),

            step=0.5,

            key=f"cruises_{year_month}"
        )


        # ----------------------------------------------------
        # FILLING RATE
        # ----------------------------------------------------

        filling_rate = st.slider(

            "Filling rate (%)",

            min_value=0,

            max_value=100,

            value=int(
                defaults["filling_rate"]
            ),

            step=5,

            key=f"filling_{year_month}"
        )


        # ----------------------------------------------------
        # STORE PARAMETERS
        # ----------------------------------------------------

        monthly_parameters[year_month] = {

            "people_per_cruise": people_per_cruise,

            "price": price,

            "cruises_per_day": cruises_per_day,

            "filling_rate": filling_rate / 100

        }


# ============================================================
# UPSELLS
# ============================================================

st.sidebar.subheader("🍹 Upsells")


# ------------------------------------------------------------
# DRINKS
# ------------------------------------------------------------

boissons_prix = st.sidebar.number_input(

    "Drinks - Price (€)",

    min_value=0.0,

    value=6.0,

    step=0.25
)


boisson_taux = st.sidebar.slider(

    "Drinks - Purchase rate",

    min_value=0,

    max_value=100,

    value=60,

    step=5

) / 100


# ------------------------------------------------------------
# APPETIZER
# ------------------------------------------------------------

apero_prix = st.sidebar.number_input(

    "Appetizer - Price (€)",

    min_value=0.0,

    value=15.0,

    step=1.0
)


apero_taux = st.sidebar.slider(

    "Appetizer - Purchase rate",

    min_value=0,

    max_value=100,

    value=40,

    step=5

) / 100


# ------------------------------------------------------------
# MEALS
# ------------------------------------------------------------

repas_prix = st.sidebar.number_input(

    "Meals - Price (€)",

    min_value=0.0,

    value=30.0,

    step=1.0
)


repas_taux = st.sidebar.slider(

    "Meals - Purchase rate",

    min_value=0,

    max_value=100,

    value=50,

    step=5

) / 100


# ============================================================
# AVERAGE UPSELL CALCULATION
# ============================================================

upsell_boissons = (
    boissons_prix
    * boisson_taux
)


upsell_apero = (
    apero_prix
    * apero_taux
)


upsell_repas = (
    repas_prix
    * repas_taux
)


upsell_moyen = (

    upsell_boissons

    + upsell_apero

    + upsell_repas
)


# ============================================================
# APPLY MONTHLY PARAMETERS TO DATAFRAME
# ============================================================


# ------------------------------------------------------------
# PEOPLE PER CRUISE
# ------------------------------------------------------------

df["people_per_cruise"] = df["year_month"].map(

    {
        month: monthly_parameters[month]["people_per_cruise"]

        for month in monthly_parameters
    }

)


# ------------------------------------------------------------
# PRICE PER PERSON
# ------------------------------------------------------------

df["prix_personne"] = df["year_month"].map(

    {
        month: monthly_parameters[month]["price"]

        for month in monthly_parameters
    }

)


# ------------------------------------------------------------
# CRUISES PER DAY
# ------------------------------------------------------------

df["cruises_per_day"] = df["year_month"].map(

    {
        month: monthly_parameters[month]["cruises_per_day"]

        for month in monthly_parameters
    }

)


# ------------------------------------------------------------
# FILLING RATE
# ------------------------------------------------------------

df["filling_rate"] = df["year_month"].map(

    {
        month: monthly_parameters[month]["filling_rate"]

        for month in monthly_parameters
    }

)


# ============================================================
# CUSTOMERS & CRUISES CALCULATION
# ============================================================


# Daily cruises

df["cruises"] = df["cruises_per_day"]


# Daily customers

df["customers"] = (

    df["cruises"]

    * df["people_per_cruise"]

    * df["filling_rate"]

)


# ============================================================
# P&L CALCULATION
# ============================================================


# Cruise revenue

df["P&L_cruises"] = (

    df["customers"]

    * df["prix_personne"]

)


# Upsells revenue

df["P&L_upsell"] = (

    df["customers"]

    * upsell_moyen

)


# Total revenue

df["P&L_global"] = (

    df["P&L_cruises"]

    + df["P&L_upsell"]

)


# ============================================================
# MONTHLY AGGREGATE
# ============================================================

df_mensuel = (

    df

    .groupby(
        "year_month",
        as_index=False
    )

    .agg(

        Cruises=(
            "cruises",
            "sum"
        ),

        Customers=(
            "customers",
            "sum"
        ),

        Revenue_Cruises=(
            "P&L_cruises",
            "sum"
        ),

        Revenue_Upsells=(
            "P&L_upsell",
            "sum"
        ),

        Revenue_Global=(
            "P&L_global",
            "sum"
        ),

        People_per_Cruise=(
            "people_per_cruise",
            "mean"
        ),

        Price_per_Person=(
            "prix_personne",
            "mean"
        ),

        Cruises_per_Day=(
            "cruises_per_day",
            "mean"
        ),

        Filling_Rate=(
            "filling_rate",
            "mean"
        )

    )

)


# ============================================================
# MONTH DISPLAY
# ============================================================

df_mensuel["Month"] = (

    df_mensuel["year_month"]

    .dt.strftime("%B %Y")

)


# ============================================================
# KPI CALCULATIONS
# ============================================================

CAForecast = df["P&L_global"].sum()

CAUpsells = df["P&L_upsell"].sum()

CACruises = df["P&L_cruises"].sum()

Customers_Global = df["customers"].sum()

Cruises_Global = df["cruises"].sum()


panier_moyen = (

    CAForecast / Customers_Global

    if Customers_Global > 0

    else 0
)


# ============================================================
# DISPLAY KPI
# ============================================================

st.subheader("📊 Forecast")


col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "Forecast",
    f"{CAForecast:,.0f} €"
)


col2.metric(
    "Customers",
    f"{Customers_Global:,.0f}"
)


col3.metric(
    "Cruises",
    f"{Cruises_Global:,.0f}"
)


col4.metric(
    "Average Basket",
    f"{panier_moyen:,.0f} €"
)


col5.metric(
    "Upsells",
    f"{CAUpsells:,.0f} €"
)


# ============================================================
# SALES BREAKDOWN
# ============================================================

st.subheader("💰 Breakdown of Sales")


col1, col2, col3 = st.columns(3)


col1.metric(
    "Revenue Cruises",
    f"{CACruises:,.0f} €"
)


col2.metric(
    "Revenue Upsells",
    f"{CAUpsells:,.0f} €"
)


col3.metric(
    "Upsells / Customer",
    f"{upsell_moyen:,.2f} €"
)


# ============================================================
# MONTHLY FORECAST GRAPH
# ============================================================

st.subheader("📈 Monthly Forecast")


fig = go.Figure()


fig.add_trace(

    go.Bar(

        x=df_mensuel["Month"],

        y=df_mensuel["Revenue_Cruises"],

        name="Cruises Revenue"

    )

)


fig.add_trace(

    go.Bar(

        x=df_mensuel["Month"],

        y=df_mensuel["Revenue_Upsells"],

        name="Upsells Revenue"

    )

)


fig.update_layout(

    barmode="stack",

    yaxis_title="Revenue (€)",

    xaxis_title="Month",

    hovermode="x unified"

)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# SCHEDULED CRUISES GRAPH
# ============================================================

st.subheader("🚢 Scheduled Cruises")


fig2 = go.Figure()


fig2.add_trace(

    go.Scatter(

        x=df_mensuel["Month"],

        y=df_mensuel["Cruises"],

        mode="lines+markers",

        name="Total Cruises"

    )

)


fig2.update_layout(

    yaxis_title="Total Cruises",

    xaxis_title="Month",

    hovermode="x unified"

)


st.plotly_chart(
    fig2,
    use_container_width=True
)


# ============================================================
# MONTHLY DETAILS TABLE
# ============================================================

st.subheader("📋 Monthly Details")


tableau = df_mensuel.copy()


# ------------------------------------------------------------
# FORMATTING
# ------------------------------------------------------------

tableau["People_per_Cruise"] = (
    tableau["People_per_Cruise"].round(0)
)

tableau["Price_per_Person"] = (
    tableau["Price_per_Person"].round(2)
)

tableau["Cruises_per_Day"] = (
    tableau["Cruises_per_Day"].round(2)
)

tableau["Filling_Rate"] = (
    tableau["Filling_Rate"]
    * 100
).round(0)

tableau["Cruises"] = (
    tableau["Cruises"].round(0)
)

tableau["Customers"] = (
    tableau["Customers"].round(0)
)

tableau["Revenue_Cruises"] = (
    tableau["Revenue_Cruises"].round(0)
)

tableau["Revenue_Upsells"] = (
    tableau["Revenue_Upsells"].round(0)
)

tableau["Revenue_Global"] = (
    tableau["Revenue_Global"].round(0)
)


# ------------------------------------------------------------
# SELECT COLUMNS
# ------------------------------------------------------------

tableau = tableau[

    [

        "Month",

        "People_per_Cruise",

        "Price_per_Person",

        "Cruises_per_Day",

        "Filling_Rate",

        "Cruises",

        "Customers",

        "Revenue_Cruises",

        "Revenue_Upsells",

        "Revenue_Global"

    ]

]


# ------------------------------------------------------------
# RENAME COLUMNS
# ------------------------------------------------------------

tableau.columns = [

    "Month",

    "People / Cruise",

    "Price / Person (€)",

    "Cruises / Day",

    "Filling Rate (%)",

    "Total Cruises",

    "Customers",

    "Revenue Cruises (€)",

    "Revenue Upsells (€)",

    "Revenue Global (€)"

]


# ============================================================
# DISPLAY TABLE
# ============================================================

st.dataframe(

    tableau,

    use_container_width=True,

    hide_index=True

)