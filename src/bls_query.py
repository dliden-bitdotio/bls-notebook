import pandas as pd
import requests
import json


def get_state_fips_codes():
    """
    Returns dataframe of state FIPS codes and state names
    from the BLS JT series reference
    """
    url = "https://download.bls.gov/pub/time.series/jt/jt.state"
    data = requests.get(url)
    data_fmt = data.content.decode("utf-8").split("\r\n")
    df = (
        pd.DataFrame(
            [x.split("\t") for x in data_fmt[1:-1]],
            columns=data_fmt[0].split("\t"),
        )
        .loc[:, ["state_code", "state_text"]]
    )

    return df
