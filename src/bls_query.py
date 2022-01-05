import pandas as pd
import requests
import json


def get_state_fips_codes():
    """
    Returns a dataframe of state FIPS codes and corresponding names and
    abbreviations from the U.S. Census Bureau.
    """
    url = "https://www2.census.gov/geo/docs/reference/state.txt"
    data = requests.get(url)
    data_fmt = data.content.decode("utf-8").split("\n")
    df = (
        pd.DataFrame(
            [x.split("|") for x in data_fmt[1:-1]],
            columns=data_fmt[0].split("|"),
        )
        .loc[:, ["STATE", "STUSAB", "STATE_NAME"]]
        .rename(
            columns={"STATE": "fips", "STUSAB": "abbrev", "STATE_NAME": "state"}
        )
    )
    return df
