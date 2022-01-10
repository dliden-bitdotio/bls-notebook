import datetime
import os

from dotenv import load_dotenv

from bls_query import build_jolts_dataframe
from upload_download_bitdotio import upload_table

if __name__ == "__main__":
    load_dotenv()
    BLS_KEY = os.environ.get("BLS_API_KEY")
    PG_STRING = os.environ.get("BITIO_PG_STRING")
    CURRENTYEAR = datetime.datetime.today().year
    BITIO_REPO = "bitdotio/bls_quit_rate"
    QUIT_RATE_TABLE = "quit_rate"

    # Download Updated JOLTS Data For Each Table Needed
    ## Seasonally Adjusted Quit Rate (for Monthly estimates)
    quitrate_sa = build_jolts_dataframe(
        element="QU",
        rate_level="R",
        sa="S",
        start_year=2001,
        end_year=CURRENTYEAR,
        annual=False,
        registration_key=BLS_KEY,
        name="Quit Rate",
    )
    quitrate_sa["seasonal_adjustment"] = "S"

    ## Non Seasonally Adjusted Quit Rate (for Annual estimates)
    quitrate_u = build_jolts_dataframe(
        element="QU",
        rate_level="R",
        sa="U",
        start_year=2001,
        end_year=CURRENTYEAR,
        annual=True,
        registration_key=BLS_KEY,
        name="Quit Rate",
    )
    quitrate_u["seasonal_adjustment"] = "U"

    ## Combined Quit Rate (adjusted and unadjusted)
    quitrate_combined = quitrate_sa.append(quitrate_u)

    # Upload to bit.io
    upload_table(df=quitrate_combined, upload_schema=BITIO_REPO, upload_table=QUIT_RATE_TABLE, bitio_pg_string=PG_STRING)
