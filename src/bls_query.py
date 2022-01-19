import json

import numpy as np
import pandas as pd
import requests


def get_state_fips_codes():
    """
    Returns dataframe of state FIPS codes and state names
    from the BLS JT series reference
    """
    url = "https://download.bls.gov/pub/time.series/jt/jt.state"
    data = requests.get(url)
    data_fmt = data.content.decode("utf-8").split("\r\n")
    df = pd.DataFrame(
        [x.split("\t") for x in data_fmt[1:-1]],
        columns=data_fmt[0].split("\t"),
    ).loc[:, ["state_code", "state_text"]]

    return df


def construct_jolts_id(
    prefix="JT",
    sa="S",
    industry="000000",
    state="00",
    area="00000",
    size_class="00",
    element="QU",
    rate_level="R",
):
    """Helper function for constructing a JOLTS ID for API requests"""
    return (
        prefix
        + sa
        + industry
        + state
        + area
        + size_class
        + element
        + rate_level
    )


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx : min(ndx + n, l)]


def build_jolts_dataframe(
    registration_key,
    element="QU",
    rate_level="R",
    sa="S",
    industry="000000",
    start_year=2018,
    end_year=2022,
    name="Quit Rate (Seasonally Adjusted)",
    annual=True,
):
    """Download JOLTS Data from the BLS API

    Parameters
    ----------
    registration_key : str
        BLS API registration key
    element : str
        Element of JOLTS Survey to download
    rate_level : str
        Rate ("R") or Level ("L")
    sa : str
        Seasonally Adjusted ("S") or not ("U")
    industry : str
        Industry code (e.g. "000000" for all industries)
    start_year : int
        Starting year of JOLTS data to download
    end_year : int
        Ending year of JOLTS data to download
    name : str
        Name to give to the downloaded series
    annual : bool
        If true, include annual estimates

    Returns
    -------
    pandas.DaraFrame
        DataFrame of specified JOLTS series with columns for
        FIPS code, state name, year, date, name, footnotes, series id
    """
    fips = get_state_fips_codes()
    codes = [
        construct_jolts_id(
            state=x,
            element=element,
            rate_level=rate_level,
            sa=sa,
            industry=industry,
        )
        for x in fips["state_code"]
    ]
    codes_iter = batch(codes, n=20)
    # API Call to BLS
    response_series = []
    for z in codes_iter:
        headers = {"Content-type": "application/json"}
        payload = {
            "seriesid": z,
            "startyear": f"{start_year}",
            "endyear": f"{end_year}",
        }
        payload.update({"registrationKey": registration_key})
        if annual:
            payload.update({"annualaverage": "true"})
        payload = json.dumps(payload)
        response = requests.post(
            "https://api.bls.gov/publicAPI/v2/timeseries/data/",
            data=payload,
            headers=headers,
        )
        response.raise_for_status()
        response_series.extend(response.json()["Results"]["series"])

    # Parse Response into DataFrame
    dfs = []
    # Build a pandas series from the API results, bls_series
    for s in response_series:
        series_id = s["seriesID"]
        data = s["data"]
        data = pd.DataFrame(data)
        data["series"] = series_id
        dfs.append(data)
    df_full = pd.concat(dfs)

    # parse dates
    df_full["month"] = df_full["period"].str.extract("M(\d+)").astype(int)
    df_full.loc[df_full["period"] == "M13", "month"] = 1
    df_full["date"] = pd.to_datetime(df_full[["year", "month"]].assign(day=1))
    df_full["name"] = name
    df_full["footnotes"] = df_full["footnotes"].apply(
        lambda x: x[0].setdefault("text", np.nan)
    )
    df_full["seasonally_adjusted"] = sa
    # df_full['footnotes'] = df_full['footnotes'].apply(lambda x: x[0]['text'])
    df_full.loc[df_full["period"] == "M13", "date"] = None
    # parse geography
    df_full["state_code"] = df_full["series"].str.slice(start=9, stop=11)
    fips_map = {x: y for x, y in zip(fips["state_code"], fips["state_text"])}
    df_full["state"] = df_full["state_code"].map(fips_map)

    # Specify Types
    df_full = df_full.astype(
        {
            "series": "str",
            "state_code": "str",
            "state": "str",
            "year": "int",
            "date": "datetime64[D]",
            "name": "str",
            "footnotes": "str",
            "seasonally_adjusted": "str",
            "value": "float",
        }
    )
    df_full["month"] = df_full["date"].dt.month

    return df_full.loc[
        :,
        [
            "series",
            "name",
            "year",
            "month",
            "date",
            "state",
            "state_code",
            "seasonally_adjusted",
            "value",
            "footnotes",
        ],
    ]


def jolts_national_by_industry(
    registration_key,
    element,
    rate_level,
    sa,
    name,
    fips="00",
    start_year=2018,
    end_year=2022,
    annual=True,
    ):
    """Download national JOLTS data by industry"""

    industry_codes = {"110000": "Agriculture, Forestry, Fishing and Hunting",
                      "210000": "Mining, Quarrying, and Oil and Gas Extraction",
                        "220000": "Utilities",
                        "230000": "Construction",
                        "310000": "Manufacturing",
                        "320000": "Manufacturing",
                        "330000": "Manufacturing",
                        "420000": "Wholesale Trade",
                        "440000": "Retail Trade",
                        "450000": "Retail Trade",
                        "480000": "Transportation and Warehousing",
                        "490000": "Transportation and Warehousing",
                        "510000": "Information",
                        "520000": "Finance and Insurance",
                        "530000": "Real Estate and Rental and Leasing",
                        "540000": "Professional, Scientific, and Technical Services",
                        "550000": "Management of Companies and Enterprises",
                        "560000": "Administrative and Support and Waste Management and Remediation Services",
                        "610000": "Educational Services",
                        "620000": "Health Care and Social Assistance",
                        "710000": "Arts, Entertainment, and Recreation",
                        "720000": "Accommodation and Food Services",
                        "810000": "Other Services (except Public Administration)",
                        "820000": "Public Administration",
                        }


    code_list = industry_codes.keys()

    codes = [
        construct_jolts_id(
            element=element,
            rate_level=rate_level,
            sa=sa,
            industry=c,
            state=fips,
        )
        for c in code_list
    ]

    codes_iter = batch(codes, n=20)
    # API Call to BLS
    response_series = []
    for z in codes_iter:
        headers = {"Content-type": "application/json"}
        payload = {
            "seriesid": z,
            "startyear": f"{start_year}",
            "endyear": f"{end_year}",
        }
        payload.update({"registrationKey": registration_key})
        if annual:
            payload.update({"annualaverage": "true"})
        payload = json.dumps(payload)
        response = requests.post(
            "https://api.bls.gov/publicAPI/v2/timeseries/data/",
            data=payload,
            headers=headers,
        )
        response.raise_for_status()
        response_series.extend(response.json()["Results"]["series"])

    # Parse Response into DataFrame
    dfs = []
    # Build a pandas series from the API results, bls_series
    for s in response_series:
        series_id = s["seriesID"]
        data = s["data"]
        data = pd.DataFrame(data)
        data["series"] = series_id
        dfs.append(data)
    df_full = pd.concat(dfs)

    # parse dates
    df_full["month"] = df_full["period"].str.extract("M(\d+)").astype(int)
    df_full.loc[df_full["period"] == "M13", "month"] = 1
    df_full["date"] = pd.to_datetime(df_full[["year", "month"]].assign(day=1))
    df_full["name"] = name
    df_full["footnotes"] = df_full["footnotes"].apply(
        lambda x: x[0].setdefault("text", np.nan)
    )
    df_full["seasonally_adjusted"] = sa
    # df_full['footnotes'] = df_full['footnotes'].apply(lambda x: x[0]['text'])
    df_full.loc[df_full["period"] == "M13", "date"] = None
    # parse geography
    df_full["state_code"] = df_full["series"].str.slice(start=9, stop=11)

    # extract industry
    df_full["industry_code"] = df_full["series"].str.slice(start=3, stop=9)
    df_full["industry"] = df_full["industry_code"].map(industry_codes)


    # Specify Types
    df_full = df_full.astype(
        {
            "series": "str",
            "state_code": "str",
            "year": "int",
            "date": "datetime64[D]",
            "name": "str",
            "footnotes": "str",
            "seasonally_adjusted": "str",
            "industry_code": "str",
            "industry": "str",
            "value": "float",
        }
    )
    df_full["month"] = df_full["date"].dt.month

    return df_full.loc[
        :,
        [
            "series",
            "name",
            "year",
            "month",
            "date",
            "state_code",
            "seasonally_adjusted",
            "industry_code",
            "industry",
            "value",
            "footnotes",
        ],
    ]


def get_recessions_fred(
    api_key, start_date="2003-01-01", end_date="2022-01-11"
):
    """Get recessions indicators from St. Louis FRED API"""
    url = "https://api.stlouisfed.org/fred/series/observations"
    payload = {
        "series_id": "USRECM",
        "api_key": api_key,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": end_date,
    }
    response = requests.get(url, params=payload)
    return pd.read_json(json.dumps(response.json()["observations"])).loc[
        :, ["date", "value"]
    ]


def monthly_national_sub(bls_series, sa="S"):
    monthly = bls_series[bls_series.date.notnull()]
    monthly_national = monthly.loc[
        (monthly["state"] == "Total US")
        & (monthly["seasonally_adjusted"] == sa),
        :,
    ]
    return monthly_national
