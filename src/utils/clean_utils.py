from google.cloud import bigquery
import pandas as pd


client = bigquery.Client()


def clean_uk_finance(uk_finance):

    uk_finance["year"] = uk_finance["date"].dt.year
    uk_finance = (
        uk_finance.groupby(["year"])
        .agg(
            {
                "debit cards": "mean",
                "credit cards": "mean",
                "debit value of purchases": "sum",
                "debit of which inside the UK": "sum",
                "credit of which purchases": "sum",
                "debit volume of purchases": "sum",
                "debit volume of which inside the UK": "sum",
                "credit volume of which purchases": "sum",
            }
        )
        .round(0)
        .reset_index()
    )
    return uk_finance


def clean_boe(boe):

    # days_23 = [90, 91, 92, 92]
    quarters_23 = ["Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023"]
    quarters_24 = ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"]

    boe_23 = boe.loc[boe["year"].isin(quarters_23)]
    boe_23 = boe_23.copy()
    boe_23["year"] = "2023"

    boe_23 = boe_23.groupby(["year"]).mean().round(0).reset_index()

    boe = boe[~boe["year"].isin(quarters_23)]
    boe = boe[~boe["year"].isin(quarters_24)]

    boe = pd.concat([boe, boe_23])

    boe["year"] = boe["year"].replace("YTD 2024", "2024")
    boe["year"] = boe["year"].astype(int)

    boe = boe[boe["year"] >= 2019]
    boe = boe.sort_values("year").reset_index(drop=True)

    return boe


def clean_global(global_df):

    global_df["total"] = (
        global_df["Visa_debit"]
        + global_df["Mastercard_debit"]
        + global_df["Mastercard_credit"]
        + global_df["Visa_credit"]
        + global_df["American Express_credit"]
    )

    global_df["visa_total"] = global_df["Visa_debit"] + global_df["Visa_credit"]

    global_df["debit"] = global_df["Visa_debit"] + global_df["Mastercard_debit"]

    global_df["credit"] = (
        global_df["Mastercard_credit"]
        + global_df["Visa_credit"]
        + global_df["American Express_credit"]
    )

    global_df = global_df[["year", "debit", "credit", "visa_total", "total"]]

    return global_df


def rename_columns(df, suffix):
    cols = df.columns[1:]
    df = df.rename(columns={c: c + suffix for c in df.columns if c in cols})
    return df
