from google.cloud import bigquery

client = bigquery.Client()


def calculate_visa(visa):

    visa = (
        visa.groupby(["year"])
        .agg({"cardholders": "mean", "spend": "sum", "transactions": "sum"})
        .round(0)
        .reset_index()
    )

    return visa


def calculate_uk_finance(uk_finance):

    n_cards = 1000
    n_spend = 1e6
    n_debit_trans = 1e6
    n_credit_trans = 1e3

    # cardholders
    uk_finance["debit cards"] = uk_finance["debit cards"] * n_cards
    uk_finance["credit cards"] = uk_finance["credit cards"] * n_cards
    uk_finance["cardholders"] = uk_finance["debit cards"] + uk_finance["credit cards"]

    uk_finance["prop debit cards"] = (
        uk_finance["debit cards"] / uk_finance["cardholders"]
    ) * 100
    uk_finance["prop credit cards"] = (
        uk_finance["credit cards"] / uk_finance["cardholders"]
    ) * 100

    # spend
    uk_finance["debit value of purchases"] = (
        uk_finance["debit value of purchases"] * n_spend
    )
    uk_finance["debit of which inside the UK"] = (
        uk_finance["debit of which inside the UK"] * n_spend
    )
    uk_finance["credit of which purchases"] = (
        uk_finance["credit of which purchases"] * n_spend
    )
    uk_finance["total value of purchases"] = (
        uk_finance["debit value of purchases"] + uk_finance["credit of which purchases"]
    )

    # transactions
    uk_finance["debit volume of purchases"] = (
        uk_finance["debit volume of purchases"] * n_debit_trans
    )
    uk_finance["debit of which inside the UK"] = (
        uk_finance["debit of which inside the UK"] * n_debit_trans
    )
    uk_finance["credit volume of which purchases"] = (
        uk_finance["credit volume of which purchases"] * n_credit_trans
    )
    uk_finance["total volume of purchases"] = (
        uk_finance["debit volume of purchases"]
        + uk_finance["credit volume of which purchases"]
    )

    # uk_finance.rename(columns={'total value of purchases':'spend'}, inplace=True)

    uk_finance = uk_finance[
        [
            "year",
            "debit cards",
            "credit cards",
            "cardholders",
            "debit value of purchases",
            "credit of which purchases",
            "total value of purchases",
            "debit volume of purchases",
            "credit volume of which purchases",
            "total volume of purchases",
        ]
    ]

    return uk_finance


def days_in_year(year):
    # Leap year check:
    # divisible by 4, but not divisible by 100 unless also divisible by 400
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return 366
    else:
        return 365


def calculate_boe(boe):

    n_spend = 1e6

    boe["days_in_year"] = boe["year"].apply(days_in_year)

    boe["Mastercard values"] = (
        boe["Mastercard values (mn)"] * n_spend * boe["days_in_year"]
    )
    boe["Visa Europe values"] = (
        boe["Visa Europe net values (mn)"] * n_spend * boe["days_in_year"]
    )

    boe["Mastercard and Visa values"] = (
        boe["Mastercard values"] + boe["Visa Europe values"]
    )
    boe["Visa proportion"] = (
        boe["Visa Europe values"] / boe["Mastercard and Visa values"] * 100
    )

    boe = boe[
        [
            "year",
            "Mastercard values",
            "Visa Europe values",
            "Mastercard and Visa values",
            "Visa proportion",
        ]
    ]

    return boe


def calculate_global(global_df, card_spend):

    n_cards = 1e6
    n_spend = 1e9

    if card_spend == "card":
        global_df.iloc[:, 1:5] *= n_cards
    elif card_spend == "spend":
        global_df.iloc[:, 1:5] *= n_spend
    else:
        raise ValueError("Argument card_spend must be one of 'card' or 'spend'")

    global_df["visa_marketshare"] = global_df["visa_total"] / global_df["total"] * 100

    return global_df


def calculate_index(df):

    df = df.sort_values("year").reset_index(drop=True)

    df["index"] = df.groupby(["Data source"])["value"].transform(
        lambda x: (x / x.iloc[0] * 100)
    )

    df = df.sort_values(["Data source", "year"]).reset_index(drop=True)

    return df
