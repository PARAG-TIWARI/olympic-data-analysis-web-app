"""Reusable analytics helpers for the Olympic data dashboard."""

import numpy as np


MEDAL_COLUMNS = ["Gold", "Silver", "Bronze"]
MEDAL_DEDUP_COLUMNS = [
    "Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"
]


def fetch_medal_tally(df, year, country):
    """Return medal counts by region, or year for a selected country."""
    medal_df = df.drop_duplicates(subset=MEDAL_DEDUP_COLUMNS).copy()

    if year != "Overall":
        medal_df = medal_df[medal_df["Year"] == int(year)]

    if country != "Overall":
        medal_df = medal_df[medal_df["region"] == country]
        group_column = "Year" if year == "Overall" else "region"
    else:
        group_column = "region"

    result = (
        medal_df.groupby(group_column, as_index=False)[MEDAL_COLUMNS]
        .sum()
    )

    if group_column == "Year":
        result = result.sort_values("Year")
    else:
        result = result.sort_values("Gold", ascending=False)

    result["total"] = result[MEDAL_COLUMNS].sum(axis=1)
    for column in MEDAL_COLUMNS + ["total"]:
        result[column] = result[column].astype(int)

    return result.reset_index(drop=True)


def country_year_list(df):
    """Return sorted Olympic years and country/region names with Overall first."""
    years = sorted(df["Year"].dropna().unique().tolist())
    countries = np.unique(df["region"].dropna().values).tolist()
    countries.sort()
    return ["Overall", *years], ["Overall", *countries]


def data_over_time(df, column):
    """Count unique values of a column for each Olympic year."""
    temp = df.drop_duplicates(["Year", column])
    result = temp.groupby("Year").size().reset_index(name=column)
    return result.rename(columns={"Year": "Edition"})


def most_successful(df, sport):
    """Return the athletes with the highest medal counts overall or by sport."""
    medal_df = df.dropna(subset=["Medal"]).copy()
    if sport != "Overall":
        medal_df = medal_df[medal_df["Sport"] == sport]

    counts = medal_df["Name"].value_counts().head(15).rename_axis("Name").reset_index(name="Medals")
    athlete_info = medal_df[["Name", "Sport", "region"]].drop_duplicates("Name")
    return counts.merge(athlete_info, on="Name", how="left")


def yearwise_medal_tally(df, country):
    """Count distinct medal-awarded events for a country by year."""
    medal_df = df.dropna(subset=["Medal"]).copy()
    medal_df = medal_df.drop_duplicates(subset=MEDAL_DEDUP_COLUMNS)
    country_df = medal_df[medal_df["region"] == country]
    return (
        country_df.groupby("Year")["Medal"]
        .count()
        .reset_index(name="Medal")
        .sort_values("Year")
    )


def country_event_heatmap(df, country):
    """Build a sport-by-year medal-event count table for a selected country."""
    medal_df = df.dropna(subset=["Medal"]).copy()
    medal_df = medal_df.drop_duplicates(subset=MEDAL_DEDUP_COLUMNS)
    country_df = medal_df[medal_df["region"] == country]

    return country_df.pivot_table(
        index="Sport",
        columns="Year",
        values="Medal",
        aggfunc="count",
    ).fillna(0)


def most_successful_countrywise(df, country):
    """Return the top ten medal-winning athletes for a selected country."""
    medal_df = df.dropna(subset=["Medal"]).copy()
    country_df = medal_df[medal_df["region"] == country]

    counts = country_df["Name"].value_counts().head(10).rename_axis("Name").reset_index(name="Medals")
    athlete_info = country_df[["Name", "Sport"]].drop_duplicates("Name")
    return counts.merge(athlete_info, on="Name", how="left")


def weight_v_height(df, sport):
    """Return one athlete record per name/region for the selected sport."""
    athlete_df = df.drop_duplicates(subset=["Name", "region"]).copy()
    athlete_df["Medal"] = athlete_df["Medal"].fillna("No Medal")

    if sport != "Overall":
        athlete_df = athlete_df[athlete_df["Sport"] == sport]

    return athlete_df


def men_vs_women(df):
    """Count unique athletes by sex and Olympic year (not once per whole career)."""
    athlete_df = df.drop_duplicates(subset=["Name", "region", "Year"])

    men = (
        athlete_df[athlete_df["Sex"] == "M"]
        .groupby("Year")["Name"]
        .nunique()
        .rename("Male")
    )
    women = (
        athlete_df[athlete_df["Sex"] == "F"]
        .groupby("Year")["Name"]
        .nunique()
        .rename("Female")
    )

    result = men.to_frame().join(women, how="outer").fillna(0).astype(int)
    return result.reset_index().sort_values("Year")
