from google.cloud import bigquery
import plotly.express as px
import numpy as np

client = bigquery.Client()

# colours
visa_big_col = "#ff0000"
uk_finance_col = "#0000ff"
global_col = "#00ff00"
boe_col = "#000000"

visa_global_col = "#ffff00"
visa_uk_finance_col = "#ff00ff"
visa_boe_col = "#A52A2A"


def plot_total_cardholders(df):

    metrics = ["cardholders_uk_finance", "total_cards_global"]
    legend_name = ["UK Finance", "Global Data"]
    legend_colours = [uk_finance_col, global_col]

    df = df[df["Data source"].isin(metrics)]

    # change legend titles
    df = df.copy()
    df["Data source"] = np.where(
        df["Data source"] == metrics[0], legend_name[0], df["Data source"]
    )
    df = df.copy()
    df["Data source"] = np.where(
        df["Data source"] == metrics[1], legend_name[1], df["Data source"]
    )

    # order df
    df = df.set_index("Data source")
    df = df.loc[legend_name].reset_index()

    scale = 1e6
    df["value"] = df["value"] / scale

    fig = px.line(
        df,
        x="year",
        y="value",
        color="Data source",
        title="Total number of cards in circulation",
    ).update_layout(
        yaxis_title="Number of cardholders (millions) ",
    )

    fig.update_yaxes(range=[0, 180])

    fig["data"][0]["line"]["color"] = legend_colours[0]
    fig["data"][1]["line"]["color"] = legend_colours[1]

    fig.show()


def plot_visa_cardholders(df):

    metrics = ["cardholders_spoc", "visa_total_cards_global"]
    legend_name = ["Visa big data", "Global Data"]
    legend_colours = [visa_big_col, global_col]

    df = df[df["Data source"].isin(metrics)]

    # change legend titles
    df = df.copy()
    df["Data source"] = np.where(
        df["Data source"] == metrics[0], legend_name[0], df["Data source"]
    )
    df = df.copy()
    df["Data source"] = np.where(
        df["Data source"] == metrics[1], legend_name[1], df["Data source"]
    )

    # order df
    df = df.set_index("Data source")
    df = df.loc[legend_name].reset_index()

    scale = 1e6
    df["value"] = df["value"] / scale

    fig = px.line(
        df,
        x="year",
        y="value",
        color="Data source",
        title="Number of Visa card's in circulation",
    ).update_layout(
        yaxis_title="Number of cardholders (millions)",
    )

    fig.update_yaxes(range=[0, 180])

    fig["data"][0]["line"]["color"] = legend_colours[0]
    fig["data"][1]["line"]["color"] = legend_colours[1]

    fig.show()


def plot_marketshare_cardholders(df):

    metrics = [
        "visa_marketshare_cards_global",
        "uk_finance_marketshare",
        "global_marketshare",
    ]
    df = df[df["Data source"].isin(metrics)].reset_index(drop=True)

    # change legend titles
    df = df.copy()
    df["Data source"] = np.where(
        df["Data source"] == "visa_marketshare_cards_global",
        "Global",
        df["Data source"],
    )
    df = df.copy()
    df["Data source"] = np.where(
        df["Data source"] == "uk_finance_marketshare",
        "Visa big data / UK Finance",
        df["Data source"],
    )
    df = df.copy()
    df["Data source"] = np.where(
        df["Data source"] == "global_marketshare",
        "Visa big data / Global",
        df["Data source"],
    )

    # plot value
    fig = px.line(
        df,
        x="year",
        y="value",
        color="Data source",
        title="Visa's Marketshare (Cardholders)",
    ).update_layout(
        yaxis_title="%",
    )

    fig.update_yaxes(range=[0, 100])

    fig["data"][0]["line"]["color"] = visa_global_col
    fig["data"][1]["line"]["color"] = visa_uk_finance_col
    fig["data"][2]["line"]["color"] = global_col

    fig.show()

    # plot index
    fig = px.line(
        df,
        x="year",
        y="index",
        color="Data source",
        title="Index of Visa's Marketshare (Cardholders)",
    )

    fig["data"][0]["line"]["color"] = visa_global_col
    fig["data"][1]["line"]["color"] = visa_uk_finance_col
    fig["data"][2]["line"]["color"] = global_col

    fig.show()


def plot_total_spend(df):

    metrics = [
        "total value of purchases_uk_finance",
        "total_spend_global",
        "Mastercard and Visa values_boe",
    ]
    legend_name = ["UK Finance", "Global Data", "Bank of England"]
    legend_colours = [uk_finance_col, global_col, boe_col]

    df = df[df["Data source"].isin(metrics)]

    # change legend titles
    df = df.copy()
    df["Data source"] = np.where(
        df["Data source"] == metrics[0], legend_name[0], df["Data source"]
    )
    df = df.copy()
    df["Data source"] = np.where(
        df["Data source"] == metrics[1], legend_name[1], df["Data source"]
    )
    df = df.copy()
    df["Data source"] = np.where(
        df["Data source"] == metrics[2], legend_name[2], df["Data source"]
    )

    # order df
    df = df.set_index("Data source")
    df = df.loc[legend_name].reset_index()

    scale = 1e9
    df["value"] = df["value"] / scale

    # plot df
    fig = px.line(
        df,
        x="year",
        y="value",
        color="Data source",
        title="Total value of transactions",
    ).update_layout(
        yaxis_title="£ (billions)",
    )

    fig.update_yaxes(range=[0, 1500])

    fig["data"][0]["line"]["color"] = legend_colours[0]
    fig["data"][1]["line"]["color"] = legend_colours[1]
    fig["data"][2]["line"]["color"] = legend_colours[2]

    fig.show()

    # plot df
    fig = px.line(
        df,
        x="year",
        y="index",
        color="Data source",
        title="Index total value of UK transactions",
    ).update_layout(
        yaxis_title=" Index",
    )

    fig["data"][0]["line"]["color"] = legend_colours[0]
    fig["data"][1]["line"]["color"] = legend_colours[1]
    fig["data"][2]["line"]["color"] = legend_colours[2]

    fig.show()


def plot_visa_spend(df):

    metrics = ["spend_spoc", "visa_total_spend_global", "Visa Europe values_boe"]
    legend_name = ["Visa big data", "Global Data", "Bank of England"]
    legend_colours = [visa_big_col, global_col, boe_col]

    df = df[df["Data source"].isin(metrics)]

    # change legend titles
    df = df.copy()
    df["Data source"] = np.where(
        df["Data source"] == metrics[0], legend_name[0], df["Data source"]
    )
    df = df.copy()
    df["Data source"] = np.where(
        df["Data source"] == metrics[1], legend_name[1], df["Data source"]
    )
    df = df.copy()
    df["Data source"] = np.where(
        df["Data source"] == metrics[2], legend_name[2], df["Data source"]
    )

    # order df
    df = df.set_index("Data source")
    df = df.loc[legend_name].reset_index()

    scale = 1e9
    df["value"] = df["value"] / scale

    # plot df
    fig = px.line(
        df,
        x="year",
        y="value",
        color="Data source",
        title="Total value of Visa transactions",
    ).update_layout(
        yaxis_title="£ (billions)",
    )

    fig.update_yaxes(range=[0, 1500])

    fig["data"][0]["line"]["color"] = legend_colours[0]
    fig["data"][1]["line"]["color"] = legend_colours[1]
    fig["data"][2]["line"]["color"] = legend_colours[2]

    fig.show()

    # plot index
    fig = px.line(
        df,
        x="year",
        y="index",
        color="Data source",
        title="Index total value of Visa transactions",
    ).update_layout(
        yaxis_title="Index",
    )

    fig["data"][0]["line"]["color"] = legend_colours[0]
    fig["data"][1]["line"]["color"] = legend_colours[1]
    fig["data"][2]["line"]["color"] = legend_colours[2]

    fig.show()


def plot_marketshare_spend(df):

    metrics = [
        "visa_marketshare_spend_global",
        "uk_finance_marketshare",
        "global_marketshare",
        "boe_marketshare",
        "Visa proportion_boe",
    ]
    legend_name = [
        "Global Data",
        "Visa big data / UK Finance",
        "Visa big data / Global",
        "Visa big data / Bank of England",
        "Bank of England",
    ]
    legend_colours = [
        global_col,
        visa_uk_finance_col,
        visa_global_col,
        visa_boe_col,
        boe_col,
    ]

    df = df[df["Data source"].isin(metrics)].reset_index(drop=True)

    # change legend titles
    df = df.copy()
    df["Data source"] = np.where(
        df["Data source"] == metrics[0], legend_name[0], df["Data source"]
    )
    df = df.copy()
    df["Data source"] = np.where(
        df["Data source"] == metrics[1], legend_name[1], df["Data source"]
    )
    df = df.copy()
    df["Data source"] = np.where(
        df["Data source"] == metrics[2], legend_name[2], df["Data source"]
    )
    df = df.copy()
    df["Data source"] = np.where(
        df["Data source"] == metrics[3], legend_name[3], df["Data source"]
    )
    df = df.copy()
    df["Data source"] = np.where(
        df["Data source"] == metrics[4], legend_name[4], df["Data source"]
    )

    # order df
    df = df.set_index("Data source")
    df = df.loc[legend_name].reset_index()

    # plot df
    fig = px.line(
        df,
        x="year",
        y="value",
        color="Data source",
        title="Visa's Marketshare (Spend)",
    ).update_layout(
        yaxis_title="%",
    )

    fig.update_yaxes(range=[0, 100])

    fig["data"][0]["line"]["color"] = legend_colours[0]
    fig["data"][1]["line"]["color"] = legend_colours[1]
    fig["data"][2]["line"]["color"] = legend_colours[2]
    fig["data"][3]["line"]["color"] = legend_colours[3]
    fig["data"][4]["line"]["color"] = legend_colours[4]

    fig.show()

    # plot index
    fig = px.line(
        df,
        x="year",
        y="index",
        color="Data source",
        title="Index of Visa' Marketshare (Spend)",
    )

    fig["data"][0]["line"]["color"] = legend_colours[0]
    fig["data"][1]["line"]["color"] = legend_colours[1]
    fig["data"][2]["line"]["color"] = legend_colours[2]
    fig["data"][3]["line"]["color"] = legend_colours[3]
    fig["data"][4]["line"]["color"] = legend_colours[4]

    fig.show()


def plot_marketshare_trans(df):

    metrics = [
        "uk_finance_trans_marketshare",
    ]
    legend_name = [
        "Visa big data / UK Finance",
    ]
    legend_colours = [
        visa_uk_finance_col,
    ]

    df = df[df["Data source"].isin(metrics)].reset_index(drop=True)

    # change legend titles
    df = df.copy()
    df["Data source"] = np.where(
        df["Data source"] == metrics[0], legend_name[0], df["Data source"]
    )

    # order df
    df = df.set_index("Data source")
    df = df.loc[legend_name].reset_index()

    # plot df
    fig = px.line(
        df,
        x="year",
        y="value",
        color="Data source",
        title="Visa's Marketshare (Transactions)",
    ).update_layout(
        yaxis_title="%",
    )

    fig.update_yaxes(range=[0, 100])

    fig["data"][0]["line"]["color"] = legend_colours[0]

    fig.show()

    # plot index
    fig = px.line(
        df,
        x="year",
        y="index",
        color="Data source",
        title="Index of Visa's Marketshare (Transactions)",
    )

    fig["data"][0]["line"]["color"] = legend_colours[0]

    fig.show()


def plot_adjusted_visa(df, y_value):

    if y_value == "value":
        scaling_factor = 1e9
        y_title = "£ (billions)"
    else:
        scaling_factor = 1
        y_title = "index"

    df[y_value] = df[y_value] / scaling_factor

    df = df.sort_values(["year", "Data source"])
    df["year"] = df["year"].astype(str)
    fig = px.line(
        df,
        x="year",
        y=y_value,
        color="Data source",
        title="Accounting for Visas marketshare in spoc",
    ).update_layout(
        yaxis_title=y_title,
    )

    fig.show()
