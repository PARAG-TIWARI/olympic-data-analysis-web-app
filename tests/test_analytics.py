import pandas as pd

import helper
from preprocessor import preprocess


def sample_raw_data():
    return pd.DataFrame(
        [
            {
                "Name": "Athlete A", "Sex": "M", "Age": 22, "Height": 180,
                "Weight": 75, "Team": "USA", "NOC": "USA", "Games": "2012 Summer",
                "Year": 2012, "Season": "Summer", "City": "London",
                "Sport": "Athletics", "Event": "100m", "Medal": "Gold",
            },
            {
                "Name": "Athlete B", "Sex": "F", "Age": 24, "Height": 170,
                "Weight": 60, "Team": "USA", "NOC": "USA", "Games": "2012 Summer",
                "Year": 2012, "Season": "Summer", "City": "London",
                "Sport": "Swimming", "Event": "200m", "Medal": "Silver",
            },
            {
                "Name": "Athlete A", "Sex": "M", "Age": 26, "Height": 180,
                "Weight": 75, "Team": "USA", "NOC": "USA", "Games": "2016 Summer",
                "Year": 2016, "Season": "Summer", "City": "Rio",
                "Sport": "Athletics", "Event": "200m", "Medal": None,
            },
            {
                "Name": "Athlete C", "Sex": "F", "Age": 23, "Height": 165,
                "Weight": 55, "Team": "CAN", "NOC": "CAN", "Games": "2014 Winter",
                "Year": 2014, "Season": "Winter", "City": "Sochi",
                "Sport": "Skiing", "Event": "Slalom", "Medal": "Bronze",
            },
        ]
    )


def sample_regions():
    return pd.DataFrame(
        [
            {"NOC": "USA", "region": "United States", "notes": None},
            {"NOC": "CAN", "region": "Canada", "notes": None},
        ]
    )


def test_preprocess_filters_winter_games_and_maps_regions():
    result = preprocess(sample_raw_data(), sample_regions())

    assert len(result) == 3
    assert set(result["region"]) == {"United States"}
    assert {"Gold", "Silver"}.issubset(result.columns)


def test_country_year_list_inserts_overall_first():
    processed = preprocess(sample_raw_data(), sample_regions())
    years, countries = helper.country_year_list(processed)

    assert years[0] == "Overall"
    assert years[1:] == [2012, 2016]
    assert countries == ["Overall", "United States"]


def test_fetch_medal_tally_counts_distinct_medals():
    processed = preprocess(sample_raw_data(), sample_regions())
    tally = helper.fetch_medal_tally(processed, 2012, "Overall")

    assert tally.loc[0, "region"] == "United States"
    assert tally.loc[0, "Gold"] == 1
    assert tally.loc[0, "Silver"] == 1
    assert tally.loc[0, "total"] == 2


def test_data_over_time_counts_unique_names_per_year():
    processed = preprocess(sample_raw_data(), sample_regions())
    result = helper.data_over_time(processed, "Name").set_index("Edition")

    assert result.loc[2012, "Name"] == 2
    assert result.loc[2016, "Name"] == 1


def test_men_and_women_participation_counts_each_athlete_each_year():
    processed = preprocess(sample_raw_data(), sample_regions())
    result = helper.men_vs_women(processed).set_index("Year")

    assert result.loc[2012, "Male"] == 1
    assert result.loc[2012, "Female"] == 1
    assert result.loc[2016, "Male"] == 1
    assert result.loc[2016, "Female"] == 0


def test_weight_height_helper_does_not_mutate_original_dataframe():
    processed = preprocess(sample_raw_data(), sample_regions())
    original = processed.copy(deep=True)

    result = helper.weight_v_height(processed, "Overall")

    assert result["Medal"].eq("No Medal").any()
    pd.testing.assert_frame_equal(processed, original)
