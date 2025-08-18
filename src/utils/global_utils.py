import pandas as pd
import plotly.express as px


def debit():
    debit_data = {
        "year": ["2019", "2020", "2021", "2022", "2023"],
        "percentage_cards": [96.1, 94.2, 88.4, 72.5, 68.5],
        "percentage_value": [96.6, 96.3, 91.7, 77.6, 68.8],
    }
    debit_df = pd.DataFrame(debit_data)
    return debit_df


def credit():
    credit_data = {
        "year": ["2019", "2020", "2021", "2022", "2023"],
        "percentage_cards": [34.7, 33.8, 31, 29.6, 28.3],
        "percentage_value": [29.8, 26.7, 25.5, 23.2, 21.8],
    }
    credit_df = pd.DataFrame(credit_data)
    return credit_df


def debit_credit():
    debit_credit_data = {
        "year": ["2019", "2020", "2021", "2022", "2023"],
        "percentage_cards": [72.8, 71.1, 67.1, 56.9, 54],
        "percentage_value": [83.8, 84.7, 80.4, 67.1, 59.3],
    }
    debit_credit_df = pd.DataFrame(debit_credit_data)
    return debit_credit_df


def debit_credit_exc_cash():
    debit_credit_ex_cash_data = {
        "year": ["2019", "2020", "2021", "2022", "2023"],
        "percentage_cards": [100, 100, 100, 100, 100],  # needs to be calculated
        "percentage_value": [81.4, 83.1, 79.1, 66.0, 58.3],
    }
    debit_credit_ex_cash_df = pd.DataFrame(debit_credit_ex_cash_data)
    return debit_credit_ex_cash_df


def get_marketshare():
    marketshare_debit = debit()
    marketshare_credit = credit()
    marketshare_debit_credit = debit_credit()
    marketshare_debit_credit_ex_cash = debit_credit_exc_cash()

    marketshare_total_1 = marketshare_debit.merge(
        marketshare_credit, how="inner", on="year", suffixes=("_debit", "_credit")
    )

    marketshare_total_2 = marketshare_debit_credit.merge(
        marketshare_debit_credit_ex_cash,
        how="inner",
        on="year",
        suffixes=("_debit_credit", "_debit_credit_exc_cash"),
    )

    marketshare_total = marketshare_total_1.merge(
        marketshare_total_2, how="inner", on="year"
    )

    marketshare_total = marketshare_total.drop(
        "percentage_cards_debit_credit_exc_cash", axis=1
    )
    marketshare_total = marketshare_total.drop(
        "percentage_value_debit_credit_exc_cash", axis=1
    )

    return marketshare_total


def plot_marketshare(df, yaxis_variable):

    if yaxis_variable.columns[1] == "percentage_cards_debit":
        title = "Market Share of cards in circulation by Card Type (Percentage)"
        new_names = {
            "percentage_cards_debit": "Debit",
            "percentage_cards_credit": "Credit",
            "percentage_cards_debit_credit": "Debit and Credit",
        }

    elif yaxis_variable.columns[1] == "percentage_value_debit":
        title = "Visa Market Share of Transactional Value by Card Type (Percentage)"
        new_names = {
            "percentage_value_debit": "Debit",
            "percentage_value_credit": "Credit",
            "percentage_value_debit_credit": "Debit and Credit",
        }
    else:
        title = "Error"

    fig = px.line(
        df,
        x="year",
        y=yaxis_variable.columns[1:5],
        labels={"year": "Year", "value": "", "variable": "Card type"},
    )
    fig.update_yaxes(range=[0, 100])
    fig.update_layout(
        title={
            "text": title,
            "x": 0.5,  # Center the title horizontally
            "xanchor": "center",  # Anchor the title at the center
        }
    )

    fig.for_each_trace(
        lambda t: t.update(
            name=new_names[t.name],
            legendgroup=new_names[t.name],
            hovertemplate=t.hovertemplate.replace(t.name, new_names[t.name]),
        )
    )
    fig.show()


def merge_marketshare(df):
    marketshare_debit = debit()
    marketshare_debit_credit = debit_credit()
    # marketshare_debit_credit_ex_cash = debit_credit_exc_cash()

    df = df.merge(marketshare_debit, how="left", on="year")
    df = df.merge(
        marketshare_debit_credit,
        how="left",
        on="year",
        suffixes=("_debit", "_debit_credit"),
    )
    return df


def calculate_spend_marketshare(df):
    df["spend_per_millions"] = df["value"] / 1e6
    df["adj_debit_spend"] = (
        df["spend_per_millions"] / df["percentage_value_debit"] * 100
    )
    df["adj_debit_credit_spend"] = (
        df["spend_per_millions"] / df["percentage_value_debit_credit"] * 100
    )
    # df["adj_debit_credit_exc_cash_spend"] = (
    #     df["spend_per_millions"] / df["percentage_value_debit_credit_exc_cash"] * 100
    # )
    return df
