from google.cloud import bigquery
import pandas as pd
from fintrans_toolbox.src import table_utils as t

client = bigquery.Client()


def read_visa(cardholder_origin, cardholders_location, spend_location):
    """
    \n
    \n
    Description:
    Function allows you to read in data from
    spend_merchant_location. \
    This function uses read_spend_merchant_location
    \n
        Args:
        - cardholder_origin: string.
        (cardholder_origin = "uk" or cardholder_origin = "all")
        - cardholders: string.
        (cardholder = "uk" or cardholers = "all")
        - spend: string.
        (spend = "uk" or spend = "all")
    \n
        - cardholder_location and spend_location are independent of each other\
        To ensure cardholder_location and spend_location are \
        comparable select the same "uk" or "all" for both
        if cardholder ='all' then the number of cardholders is likely to be larger\
        than the true value

    Returns:
       Spend Origin and Channel, grouped by year
    """

    if cardholder_origin == "uk":
        origin = "UNITED KINGDOM"
    elif cardholder_origin == "all":
        origin = "All"

    if cardholders_location == "all" and spend_location == "all":
        print(f"""{origin} cardholder, spend and transactions values""")

        spoc = t.read_spend_origin_and_channel(
            client,
            time_period="Month",
            cardholder_origin=origin,
            cardholder_origin_country="All",
            mcg="All",
            merchant_channel="All",
            mcc="All",
            cardholder_location="",
        )

    elif cardholders_location == "uk" and spend_location == "uk":
        print(
            f"""{origin} cardholders and spend in the UK only
             \n"""
        )
        spoc = t.read_spend_origin_and_channel(
            client,
            time_period="Month",
            cardholder_origin=origin,
            cardholder_origin_country="All",
            mcg="All",
            merchant_channel="All",
            mcc="All",
            cardholder_location="",
            destination_country="'UNITED KINGDOM'",
        )

    elif cardholders_location == "uk" and spend_location == "all":
        print(
            f"""{origin} cardholders in the UK\
spend and transaction values \
in the UK and internationally (when spend == "all")
        \n"""
        )
        spoc_cardholders = t.read_spend_origin_and_channel(
            client,
            time_period="Month",
            cardholder_origin=origin,
            cardholder_origin_country="All",
            mcg="All",
            merchant_channel="All",
            mcc="All",
            cardholder_location="",
            destination_country="'UNITED KINGDOM'",
        )
        spoc_cardholders = spoc_cardholders.drop(
            ["dist_merchants", "pct_repeat_pan_cnt", "destination_country"], axis=1
        )
        spoc_cardholders = spoc_cardholders.drop(["spend", "transactions"], axis=1)

        spoc_spend_trans = t.read_spend_origin_and_channel(
            client,
            time_period="Month",
            cardholder_origin=origin,
            cardholder_origin_country="All",
            mcg="All",
            merchant_channel="All",
            mcc="All",
            cardholder_location="",
        )
        spoc_spend_trans = spoc_spend_trans.drop(
            ["dist_merchants", "pct_repeat_pan_cnt", "destination_country"], axis=1
        )
        spoc_spend_trans = spoc_spend_trans.drop(["cardholders"], axis=1)

        # merge cardholders and spend_transactions df
        # get cardholder numbers of UK only but include international spending
        spoc_columns = list(spoc_cardholders)
        spoc_columns.remove("cardholders")

        # Group all destination countries together
        spoc_spend_trans = spoc_spend_trans.groupby(spoc_columns).agg(
            {
                "spend": "sum",
                "transactions": "sum",
            }
        )

        spoc = spoc_cardholders.merge(spoc_spend_trans, how="inner", on=spoc_columns)

    else:
        raise ValueError(
            """Arguments need to be a combination of the follow:/
            cardholder_origin: 'uk' or 'all' /
            cardholder_location: 'uk' "all' /
            spend_location: 'uk' or 'all'"""
        )

    spoc = t.create_date_time(spoc)
    spoc = spoc.groupby(["date_time", "year"]).agg(
        {
            "cardholders": "sum",
            "spend": "sum",
            "transactions": "sum",
        }
    )
    print("")

    return spoc


def read_f2f_online(cardholder_origin, f2f, online):
    """
    \n
    \n
    Description:
    Function allows you to read in data from \
    spend_merchant_location. \
    This function uses read_spend_merchant_location
    \n
        Args:
        - cardholder_origin: string.
        (cardholder_origin = "uk" or cardholder_origin = "all")
        - f2f: string.
        (f2f = "uk" or f2f = "all")
        - online: string.
        (online = "uk" or online = "all")
        \n
        - f2f and online are independent of each other\
        The number of cardholders is likely to be larger\
        than the true value due to double counting

    Returns:
       Spend Origin and Channel, grouped by year
    """

    if cardholder_origin == "uk":
        origin = "UNITED KINGDOM"
    elif cardholder_origin == "all":
        origin = "All"

    if f2f == "all":
        f2f = t.read_spend_origin_and_channel(
            client,
            time_period="Month",
            cardholder_origin=origin,
            cardholder_origin_country="All",
            mcg="All",
            merchant_channel="Face to Face",
            mcc="All",
            cardholder_location="",
        )

    elif f2f == "uk":
        f2f = t.read_spend_origin_and_channel(
            client,
            time_period="Month",
            cardholder_origin=origin,
            cardholder_origin_country="All",
            mcg="All",
            merchant_channel="Face to Face",
            mcc="All",
            cardholder_location="",
            destination_country="'UNITED KINGDOM'",
        )

    if online == "all":
        online = t.read_spend_origin_and_channel(
            client,
            time_period="Month",
            cardholder_origin=origin,
            cardholder_origin_country="All",
            mcg="All",
            merchant_channel="Online",
            mcc="All",
            cardholder_location="",
        )

    elif online == "uk":
        online = t.read_spend_origin_and_channel(
            client,
            time_period="Month",
            cardholder_origin=origin,
            cardholder_origin_country="All",
            mcg="All",
            merchant_channel="Online",
            mcc="All",
            cardholder_location="",
            destination_country="'UNITED KINGDOM'",
        )

    f2f_online = pd.concat([f2f, online])
    f2f_online = t.create_date_time(f2f_online)
    f2f_online = f2f_online.groupby(["date_time", "year"]).agg(
        {
            "cardholders": "sum",
            "spend": "sum",
            "transactions": "sum",
        }
    )

    return f2f_online


def read_global_cards():

    global_cards = pd.read_csv(
        "/home/jupyter/ft_marketshare/data/raw/Global_data_cards.csv"
    )

    return global_cards


def read_global_spend():

    global_spend = pd.read_csv(
        "/home/jupyter/ft_marketshare/data/raw/Global_data_spend.csv"
    )

    return global_spend


def read_uk_finance():

    uk_finance = pd.read_csv("/home/jupyter/ft_marketshare/data/raw/uk_finance.csv")

    uk_finance["date"] = uk_finance["date"].astype("datetime64[ns]")

    return uk_finance


def read_boe():

    boe = pd.read_csv(
        "/home/jupyter/ft_marketshare/data/raw/Average_daily_RTGS_settlement_BoE.csv"
    )
    boe = boe.melt("Values_Volumes", var_name="year", ignore_index=False)
    boe = (
        boe.pivot(index="year", columns="Values_Volumes", values="value")
        .rename_axis(columns=None)
        .reset_index()
    )

    return boe


def read_link():

    link = pd.read_csv(
        "/home/jupyter/ft_marketshare/data/raw/Total_Cash_Withdrawal_Volume_Link.csv"
    )

    return link
