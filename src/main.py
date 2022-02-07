import datetime
import os

from dotenv import load_dotenv

from bls_query import build_jolts_dataframe, jolts_national_by_industry
from upload_download_bitdotio import upload_table

if __name__ == "__main__":
    load_dotenv()
    BLS_KEY = os.environ.get("BLS_API_KEY")
    PG_STRING = os.environ.get("BITIO_PG_STRING")
    BITIO_REPO = os.environ.get("BITIO_REPO")
    CURRENTYEAR = datetime.datetime.today().year
    QUIT_RATE_TABLE = "quit_rate"
    HIRE_RATE_TABLE = "hire_rate"
    LD_TABLE="layoffs_discharges_rate"
    OPENINGS_TABLE="job_openings_rate"

    # Download Updated JOLTS Data For Each Table Needed
    ## Seasonally Adjusted Quit Rate (for Monthly estimates)
    quitrate_sa = build_jolts_dataframe(
        element="QU",
        rate_level="R",
        sa="S",
        start_year=2003,
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
        start_year=2003,
        end_year=CURRENTYEAR,
        annual=True,
        registration_key=BLS_KEY,
        name="Quit Rate",
    )
    quitrate_u["seasonal_adjustment"] = "U"

    ## Combined Quit Rate (adjusted and unadjusted)
    quitrate_combined = quitrate_sa.append(quitrate_u)

    ## layoffs & discharges (SA)
    ld_sa = build_jolts_dataframe(
            element="LD",
            rate_level="R",
            sa="S",
            start_year=2003,
            end_year=CURRENTYEAR,
            annual=False,
            registration_key=BLS_KEY,
            name="Layoffs and Discharges Rate",
        )
    ld_sa["seasonal_adjustment"] = "S"
    ## layoffs & discharges (U)
    ld_u = build_jolts_dataframe(
            element="LD",
            rate_level="R",
            sa="U",
            start_year=2003,
            end_year=CURRENTYEAR,
            annual=False,
            registration_key=BLS_KEY,
            name="Layoffs and Discharges Rate",
        )
    ld_u["seasonal_adjustment"] = "U"

    ## Combined Layoffs & Discharges
    ld_combined = ld_sa.append(ld_u)

    ## Job Openings (SA)
    openings_sa = build_jolts_dataframe(
            element="JO",
            rate_level="R",
            sa="S",
            start_year=2003,
            end_year=CURRENTYEAR,
            annual=False,
            registration_key=BLS_KEY,
            name="Job Openings",
        )
    openings_sa["seasonal_adjustment"] = "S"
    ## Job Openings (U)
    openings_u = build_jolts_dataframe(
            element="JO",
            rate_level="R",
            sa="U",
            start_year=2003,
            end_year=CURRENTYEAR,
            annual=False,
            registration_key=BLS_KEY,
            name="Job Openings",
        )
    openings_u["seasonal_adjustment"] = "U"

    ## Combined Layoffs & Discharges
    openings_combined = openings_sa.append(openings_u)

    ## Hire Rate (SA)
    hires_sa = build_jolts_dataframe(
            element="HI",
            rate_level="R",
            sa="S",
            start_year=2003,
            end_year=CURRENTYEAR,
            annual=False,
            registration_key=BLS_KEY,
            name="Hire Rate",
        )
    hires_sa["seasonal_adjustment"] = "S"
    ## Hire Rate (U)
    hires_u = build_jolts_dataframe(
            element="HI",
            rate_level="R",
            sa="U",
            start_year=2003,
            end_year=CURRENTYEAR,
            annual=True,
            registration_key=BLS_KEY,
            name="Hire Rate",
        )
    hires_u["seasonal_adjustment"] = "U"

    ## Combined Hire Rate
    hires_combined = hires_sa.append(hires_u)
    

    # Upload to bit.io
    upload_table(df=quitrate_combined, upload_schema=BITIO_REPO, upload_table=QUIT_RATE_TABLE, bitio_pg_string=PG_STRING)
    upload_table(df=ld_combined, upload_schema=BITIO_REPO, upload_table=LD_TABLE, bitio_pg_string=PG_STRING)
    upload_table(df=openings_combined, upload_schema=BITIO_REPO, upload_table=OPENINGS_TABLE, bitio_pg_string=PG_STRING)
    upload_table(df=hires_combined, upload_schema=BITIO_REPO, upload_table=HIRE_RATE_TABLE, bitio_pg_string=PG_STRING)

    # Industry Level Data
    ## quit rates
    industry_quits_sa = jolts_national_by_industry(
        element="QU",
        rate_level="R",
        sa="S",
        start_year=2003,
        end_year=CURRENTYEAR,
        annual=False,
        registration_key=BLS_KEY,
        name="Quit Rate by Industry",
    )
    industry_quits_sa["seasonal_adjustment"] = "S"

    industry_quits_u = jolts_national_by_industry(
        element="QU",
        rate_level="R",
        sa="U",
        start_year=2003,
        end_year=CURRENTYEAR,
        annual=True,
        registration_key=BLS_KEY,
        name="Quit Rate by Industry",
    )
    industry_quits_u["seasonal_adjustment"] = "U"

    industry_quits_combined = industry_quits_sa.append(industry_quits_u)

    ## layoffs & discharges
    industry_ld_sa = jolts_national_by_industry(
        element="LD",
        rate_level="R",
        sa="S",
        start_year=2003,
        end_year=CURRENTYEAR,
        annual=False,
        registration_key=BLS_KEY,
        name="Layoffs and Discharges by Industry",
    )
    industry_ld_sa["seasonal_adjustment"] = "S"

    industry_ld_u = jolts_national_by_industry(
        element="LD",
        rate_level="R",
        sa="U",
        start_year=2003,
        end_year=CURRENTYEAR,
        annual=True,
        registration_key=BLS_KEY,
        name="Layoffs and Discharges by Industry",
    )
    industry_ld_u["seasonal_adjustment"] = "U"

    industry_ld_combined = industry_ld_sa.append(industry_ld_u)

    ## openings
    industry_openings_sa = jolts_national_by_industry(
        element="JO",
        rate_level="R",
        sa="S",
        start_year=2003,
        end_year=CURRENTYEAR,
        annual=False,
        registration_key=BLS_KEY,
        name="Job Openings by Industry",
    )
    industry_openings_sa["seasonal_adjustment"] = "S"

    industry_openings_u = jolts_national_by_industry(
        element="JO",
        rate_level="R",
        sa="U",
        start_year=2003,
        end_year=CURRENTYEAR,
        annual=True,
        registration_key=BLS_KEY,
        name="Job Openings by Industry",
    )
    industry_openings_u["seasonal_adjustment"] = "U"

    industry_openings_combined = industry_openings_sa.append(industry_openings_u)

    # quit level
    quitlevel_sa = build_jolts_dataframe(
        element="QU",
        rate_level="L",
        sa="S",
        start_year=2003,
        end_year=CURRENTYEAR,
        annual=False,
        registration_key=BLS_KEY,
        name="Quit Level",
    )
    quitlevel_sa["seasonal_adjustment"] = "S"

    ## Non Seasonally Adjusted Quit Rate (for Annual estimates)
    quitlevel_u = build_jolts_dataframe(
        element="QU",
        rate_level="L",
        sa="U",
        start_year=2003,
        end_year=CURRENTYEAR,
        annual=True,
        registration_key=BLS_KEY,
        name="Quit Level",
    )
    quitlevel_u["seasonal_adjustment"] = "U"

    ## Combined Quit Rate (adjusted and unadjusted)
    quitlevel_combined = quitlevel_sa.append(quitlevel_u)

    ## Hire Level (SA)
    hirelevel_sa = build_jolts_dataframe(
            element="HI",
            rate_level="L",
            sa="S",
            start_year=2003,
            end_year=CURRENTYEAR,
            annual=False,
            registration_key=BLS_KEY,
            name="Hire Level",
        )
    hirelevel_sa["seasonal_adjustment"] = "S"
    ## Hire Rate (U)
    hirelevel_u = build_jolts_dataframe(
            element="HI",
            rate_level="L",
            sa="U",
            start_year=2003,
            end_year=CURRENTYEAR,
            annual=True,
            registration_key=BLS_KEY,
            name="Hire Level",
        )
    hirelevel_u["seasonal_adjustment"] = "U"

    ## Combined Hire Rate
    hirelevel_combined = hirelevel_sa.append(hirelevel_u)


    upload_table(df=industry_quits_combined, upload_schema=BITIO_REPO, upload_table="industry_quit_rate", bitio_pg_string=PG_STRING)
    upload_table(df=industry_ld_combined, upload_schema=BITIO_REPO, upload_table="industry_ld_rate", bitio_pg_string=PG_STRING)
    upload_table(df=industry_openings_combined, upload_schema=BITIO_REPO, upload_table="industry_openings_rate", bitio_pg_string=PG_STRING)
    upload_table(df=quitlevel_combined, upload_schema=BITIO_REPO, upload_table="quit_level", bitio_pg_string=PG_STRING)
    upload_table(df=hirelevel_combined, upload_schema=BITIO_REPO, upload_table="hire_level", bitio_pg_string=PG_STRING)

## separation Rate (SA)
    separations_sa = build_jolts_dataframe(
            element="TS",
            rate_level="R",
            sa="S",
            start_year=2003,
            end_year=CURRENTYEAR,
            annual=False,
            registration_key=BLS_KEY,
            name="Total Separation Rate",
        )
    separations_sa["seasonal_adjustment"] = "S"
    ## separation Rate (U)
    separations_u = build_jolts_dataframe(
            element="TS",
            rate_level="R",
            sa="U",
            start_year=2003,
            end_year=CURRENTYEAR,
            annual=True,
            registration_key=BLS_KEY,
            name="Total Separation Rate",
        )
    separations_u["seasonal_adjustment"] = "U"

    ## Combined separation Rate
    separations_combined = separations_sa.append(separations_u)


## separation Level (SA)
    separationlevel_sa = build_jolts_dataframe(
            element="TS",
            rate_level="L",
            sa="S",
            start_year=2003,
            end_year=CURRENTYEAR,
            annual=False,
            registration_key=BLS_KEY,
            name="Total Separation Level",
        )
    separationlevel_sa["seasonal_adjustment"] = "S"
    ## separation Rate (U)
    separationlevel_u = build_jolts_dataframe(
            element="TS",
            rate_level="L",
            sa="U",
            start_year=2003,
            end_year=CURRENTYEAR,
            annual=True,
            registration_key=BLS_KEY,
            name="Total Separation Level",
        )
    separationlevel_u["seasonal_adjustment"] = "U"

    ## Combined separation Rate
    separationlevel_combined = separationlevel_sa.append(separationlevel_u)

    upload_table(df=separations_combined, upload_schema=BITIO_REPO, upload_table="separation_rate", bitio_pg_string=PG_STRING)
    upload_table(df=separationlevel_combined, upload_schema=BITIO_REPO, upload_table="separation_level", bitio_pg_string=PG_STRING)

    # Other Industry Data
    ## Separation Rate
    industry_separations_sa = jolts_national_by_industry(
        element="TS",
        rate_level="R",
        sa="S",
        start_year=2003,
        end_year=CURRENTYEAR,
        annual=False,
        registration_key=BLS_KEY,
        name="Job Separation Rate by Industry",
    )
    industry_separations_sa["seasonal_adjustment"] = "S"

    industry_separations_u = jolts_national_by_industry(
        element="TS",
        rate_level="R",
        sa="U",
        start_year=2003,
        end_year=CURRENTYEAR,
        annual=True,
        registration_key=BLS_KEY,
        name="Job Separation Rate by Industry",
    )
    industry_separations_u["seasonal_adjustment"] = "U"

    industry_separations_combined = industry_separations_sa.append(industry_separations_u)

    ## Separation Level
    industry_separationslevel_sa = jolts_national_by_industry(
        element="TS",
        rate_level="L",
        sa="S",
        start_year=2003,
        end_year=CURRENTYEAR,
        annual=False,
        registration_key=BLS_KEY,
        name="Job Separation Level by Industry",
    )
    industry_separationslevel_sa["seasonal_adjustment"] = "S"

    industry_separationslevel_u = jolts_national_by_industry(
        element="TS",
        rate_level="L",
        sa="U",
        start_year=2003,
        end_year=CURRENTYEAR,
        annual=True,
        registration_key=BLS_KEY,
        name="Job Separation Level by Industry",
    )
    industry_separationslevel_u["seasonal_adjustment"] = "U"

    industry_separationslevel_combined = industry_separationslevel_sa.append(industry_separationslevel_u)

    ## hires by industry
    industry_hires_sa = jolts_national_by_industry(
        element="HI",
        rate_level="R",
        sa="S",
        start_year=2003,
        end_year=CURRENTYEAR,
        annual=False,
        registration_key=BLS_KEY,
        name="Hire Rate by Industry",
    )
    industry_hires_sa["seasonal_adjustment"] = "S"

    industry_hires_u = jolts_national_by_industry(
        element="HI",
        rate_level="R",
        sa="U",
        start_year=2003,
        end_year=CURRENTYEAR,
        annual=True,
        registration_key=BLS_KEY,
        name="Hire Rate by Industry",
    )
    industry_hires_u["seasonal_adjustment"] = "U"

    industry_hires_combined = industry_hires_sa.append(industry_hires_u)

## hire level by industry
    industry_hires_sa = jolts_national_by_industry(
        element="HI",
        rate_level="R",
        sa="S",
        start_year=2003,
        end_year=CURRENTYEAR,
        annual=False,
        registration_key=BLS_KEY,
        name="Hire Rate by Industry",
    )
    industry_hires_sa["seasonal_adjustment"] = "S"

    industry_hires_u = jolts_national_by_industry(
        element="HI",
        rate_level="R",
        sa="U",
        start_year=2003,
        end_year=CURRENTYEAR,
        annual=True,
        registration_key=BLS_KEY,
        name="Hire Rate by Industry",
    )
    industry_hires_u["seasonal_adjustment"] = "U"

    industry_hires_combined = industry_hires_sa.append(industry_hires_u)

    ## hire level by industry
    industry_hirelevel_sa = jolts_national_by_industry(
        element="HI",
        rate_level="L",
        sa="S",
        start_year=2003,
        end_year=CURRENTYEAR,
        annual=False,
        registration_key=BLS_KEY,
        name="Hire Level by Industry",
    )
    industry_hirelevel_sa["seasonal_adjustment"] = "S"

    industry_hirelevel_u = jolts_national_by_industry(
        element="HI",
        rate_level="L",
        sa="U",
        start_year=2003,
        end_year=CURRENTYEAR,
        annual=True,
        registration_key=BLS_KEY,
        name="Hire Level by Industry",
    )
    industry_hirelevel_u["seasonal_adjustment"] = "U"

    industry_hirelevel_combined = industry_hirelevel_sa.append(industry_hirelevel_u)

        ## quit levels
    industry_quitlevel_sa = jolts_national_by_industry(
        element="QU",
        rate_level="L",
        sa="S",
        start_year=2003,
        end_year=CURRENTYEAR,
        annual=False,
        registration_key=BLS_KEY,
        name="Quit Level by Industry",
    )
    industry_quitlevel_sa["seasonal_adjustment"] = "S"

    industry_quitlevel_u = jolts_national_by_industry(
        element="QU",
        rate_level="L",
        sa="U",
        start_year=2003,
        end_year=CURRENTYEAR,
        annual=True,
        registration_key=BLS_KEY,
        name="Quit Level by Industry",
    )
    industry_quitlevel_u["seasonal_adjustment"] = "U"

    industry_quitlevel_combined = industry_quitlevel_sa.append(industry_quitlevel_u)

    upload_table(df=industry_separations_combined, upload_schema=BITIO_REPO, upload_table="industry_separation_rate", bitio_pg_string=PG_STRING)
    upload_table(df=industry_separationslevel_combined, upload_schema=BITIO_REPO, upload_table="industry_separation_level", bitio_pg_string=PG_STRING)
    upload_table(df=industry_hires_combined, upload_schema=BITIO_REPO, upload_table="industry_hire_rate", bitio_pg_string=PG_STRING)
    upload_table(df=industry_hirelevel_combined, upload_schema=BITIO_REPO, upload_table="industry_hire_level", bitio_pg_string=PG_STRING)
    upload_table(df=industry_quitlevel_combined, upload_schema=BITIO_REPO, upload_table="industry_quit_level", bitio_pg_string=PG_STRING)

    # layoffs and discharges level
    layoffs_discharges_sa = build_jolts_dataframe(
            element="LD",
            rate_level="L",
            sa="S",
            start_year=2003,
            end_year=CURRENTYEAR,
            annual=False,
            registration_key=BLS_KEY,
            name="Layoffs and Discharges Level",
        )
    layoffs_discharges_sa["seasonal_adjustment"] = "S"
    ## separation Rate (U)
    layoffs_discharges_u = build_jolts_dataframe(
            element="LD",
            rate_level="L",
            sa="U",
            start_year=2003,
            end_year=CURRENTYEAR,
            annual=True,
            registration_key=BLS_KEY,
            name="Layoffs and Discharges Level",
        )
    layoffs_discharges_u["seasonal_adjustment"] = "U"

    ## Combined separation Rate
    layoffs_discharges_combined = layoffs_discharges_sa.append(layoffs_discharges_u)

    upload_table(df=layoffs_discharges_combined, upload_schema=BITIO_REPO, upload_table="layoffs_discharges_level", bitio_pg_string=PG_STRING)