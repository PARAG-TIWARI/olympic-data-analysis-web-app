"""Preprocessing helpers for the Olympic athlete dataset."""

import pandas as pd


def preprocess(df, region_df):
    """Filter Summer Games, map NOC codes and create medal indicator columns."""
    summer_df = df.loc[df["Season"] == "Summer"].copy()
    merged_df = summer_df.merge(region_df, on="NOC", how="left")
    merged_df = merged_df.drop_duplicates().reset_index(drop=True)

    medal_flags = pd.get_dummies(merged_df["Medal"], dtype="uint8")
    return pd.concat([merged_df, medal_flags], axis=1)
