import os
import streamlit as st
from fredapi import Fred
from dotenv import load_dotenv

# imports
from config import market_options, economic_options, market_colors
from data_loader import load_market_data, load_economic_data, get_latest_value
from charts import create_line_chart
from insights import generate_market_insights
from ai_commentary import generate_ai_commentary

load_dotenv()


def metric_card(title, value, delta=None):
    if delta is None:
        delta_html = ""
    else:
        is_positive = delta >= 0
        delta_class = "positive" if is_positive else "negative"
        arrow = "↑" if is_positive else "↓"

        delta_html = f"""
        <span class="delta {delta_class}">
            {arrow} {delta:,.2f}
        </span>
        """

    st.iframe(
        f"""
        <style>
        .card {{
            background: #111827;
            border: 1px solid #374151;
            border-radius: 16px;
            padding: 24px;
            height: 130px;
            font-family: "Source Sans Pro", sans-serif;
            display: flex;
            flex-direction: column;
        }}
        
        .title {{
            color: #D1D5DB;
            font-size: 18px;
            font-weight: 600;
        
            height: 50px;
            line-height: 1.2;
        }}
        
        .value {{
            color: white;
            font-size: 27px;
            font-weight: 800;
        }}
        
        .bottom-row {{
            margin-top: auto;
            color: white;           
        }}
        .positive {{
                color: #4ADE80;
                background: rgba(34, 197, 94, 0.18);
            }}
            .negative {{
                color: #F87171;
                background: rgba(239, 68, 68, 0.18);
            }}
        </style>

        <div class="card">
        <div class="title">{title}</div>

        <div class="value">{value}</div>

        <div class="bottom-row">
            {delta_html}
        </div>
        </div>
        """,
        height=200
    )
st.markdown(
    """
    <style>

    /* Entire sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0B1120;
        border-right: 1px solid #1F2937;
    }

    /* Sidebar inner container */
    section[data-testid="stSidebar"] .block-container {
        padding-top: 0.5rem;
        padding-bottom: 1rem;
    }

    /* Remove top whitespace */
    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 0rem;
    }

    /* Selectbox styling */
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #111827;
        border: 1px solid #374151;
        border-radius: 12px;
    }

    /* Selectbox text */
    section[data-testid="stSidebar"] div[data-baseweb="select"] span {
        color: white;
        font-weight: 500;
    }

    /* Expander boxes */
    section[data-testid="stSidebar"] details {
        background-color: #111827;
        border: 1px solid #374151;
        border-radius: 14px;
        padding: 0.2rem 0.4rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)
# CSS
st.set_page_config(
    page_title="MacroLens",
    layout="wide"
)
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1200px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    h1 {
        font-size: 3rem !important;
        font-weight: 700 !important;
    }
    h2 {
        font-size: 2rem !important;
        margin-top: 1rem !important;
    }
    h3 {
        font-size: 1.4rem !important;
        margin-top: 0.5rem !important;
    }
    p {
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>

    [data-testid="stMetricLabel"] {
        font-size: 1.05rem !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 2.4rem !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricDelta"] {
        font-size: 1rem !important;
    }

    button[data-baseweb="tab"] {
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.25rem !important;
    }
    section[data-testid="stSidebar"] {
        padding-top: 1rem;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    section[data-testid="stSidebar"] label {
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetric"] {
        background-color: #111827;
        padding: 1.2rem;
        border-radius: 0.9rem;
        border: 1px solid #374151;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #D1D5DB !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: white !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 1rem !important;
    }
    /* Metric card */
    [data-testid="stMetric"] {
        background-color: #111827;
        padding: 1.2rem;
        border-radius: 0.9rem;
        border: 1px solid #374151;
    }

    /* Metric label */
    [data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #D1D5DB !important;
    }

    /* Metric value */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: white !important;
    }

    /* Move delta badge inline */
    [data-testid="stMetricDelta"] {
        display: inline-flex !important;
        align-items: center;
        margin-left: 0.8rem;
        font-size: 1rem !important;
    }
    /* Put value + delta on same row */
    [data-testid="stMetric"] > div {
        display: flex;
        flex-direction: column;
    }

    [data-testid="stMetric"] label + div {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# beginning headers
st.title("MacroLens")
st.markdown(
    """
    ### Macroeconomic & Market Intelligence Dashboard

    Analyze financial markets, economic indicators, volatility, correlations,
    and comparative asset performance using real-world market data.
    """
)


# sidebar controls
st.sidebar.header("Dashboard Controls")
# Reset button
if st.sidebar.button("Reset Dashboard"):
    st.session_state.clear()
    st.rerun()

with st.sidebar.expander("Market Settings", expanded=True):
    selected_period = st.selectbox(
        "Select Time Period",
        ["1y", "5y", "10y", "max"]
    )
    selected_market = st.selectbox(
        "Select Market Indicator",
        list(market_options.keys())
    )
with st.sidebar.expander("Comparison Settings", expanded=True):
    comparison_market = st.selectbox(
        "Compare With",
        list(market_options.keys()),
        index=1
    )
with st.sidebar.expander("Economic Settings", expanded=True):
    selected_economic_indicator = st.selectbox(
        "Select Economic Indicator",
        list(economic_options.keys())
    )

# Current selection section in sidebar
st.sidebar.divider()
st.sidebar.subheader("Current Selection")
st.sidebar.write(f"Market: {selected_market}")
st.sidebar.write(f"Comparison: {comparison_market}")
st.sidebar.write(
    f"Economic Indicator: {selected_economic_indicator}"
)

# About MacroLens section in Sidebar
st.sidebar.divider()
with st.sidebar.expander("About MacroLens"):
    st.write(
        """
        MacroLens is an interactive macroeconomic and financial analytics dashboard 
        built using Python, Streamlit, Plotly, yfinance, and FRED data.

        Features include:
        - Market trend analysis
        - Moving averages
        - Volatility tracking
        - Economic indicator monitoring
        - Relative asset performance
        - Rolling correlation analysis
        - Automated macro insights
        """
    )

# adding sidebar tabs
market_tab, econ_tab, comparison_tab = st.tabs(
    ["Markets", "Economy", "Comparison"]
)

# getting the tickers of selected market options
ticker = market_options[selected_market]
comparison_ticker = market_options[comparison_market]

# getting economic data
fred_api_key = os.getenv("FRED_API_KEY")
fred = Fred(api_key=fred_api_key)
economic_series_code = economic_options[selected_economic_indicator]["code"]
economic_unit = economic_options[selected_economic_indicator]["unit"]

# getting data and comparison_data, spinner shows when loading
try:
    with st.spinner("Loading market data..."):
        data = load_market_data(ticker, selected_period)

        comparison_data = load_market_data(
            comparison_ticker,
            selected_period
        )
    with st.spinner("Loading economic data..."):
        economic_data = load_economic_data(
            fred,
            economic_series_code
        )
except Exception as e:
    st.error("Something went wrong while loading the data.")
    st.write(e)
    st.stop()

# in case yfinance fails/ returns empty
if data.empty or "Close" not in data.columns:
    st.error(
        "Market data could not be loaded right now because the data provider is rate-limiting requests. Please refresh after a few minutes."
    )
    st.stop()

if comparison_data.empty or "Close" not in comparison_data.columns:
    st.error(
        "Comparison market data could not be loaded right now because the data provider is rate-limiting requests. Please refresh after a few minutes."
    )
    st.stop()

# in case fred api fails
if economic_data.empty:
    st.warning(
        "Economic data could not be loaded right now."
    )

# getting the latest data
latest_price = get_latest_value(data["Close"])
latest_return = get_latest_value(data["Daily Return"])
latest_30_day_return = get_latest_value(data["30 Day Return"])
latest_volatility = get_latest_value(data["30 Day Volatility"])
latest_drawdown = get_latest_value(data["Drawdown"])
max_drawdown = data["Drawdown"].min().item()
latest_sharpe = get_latest_value(data["Rolling Sharpe Ratio"])
latest_annualized_volatility = get_latest_value(data["Annualized Volatility"])
# Normalize prices for comparison
data["Normalized"] = (
       data["Close"] / data["Close"].iloc[0]
   ) * 100
comparison_data["Normalized"] = (
       comparison_data["Close"] / comparison_data["Close"].iloc[0]
   ) * 100
# -----------------------------
# intelligence section
# -----------------------------
latest_50_ma = data["50 Day MA"].dropna().iloc[-1].item()
latest_200_ma = data["200 Day MA"].dropna().iloc[-1].item()

primary_performance = data["Normalized"].dropna().iloc[-1].item()
comparison_performance = comparison_data["Normalized"].dropna().iloc[-1].item()

insights = generate_market_insights(
    selected_market,
    comparison_market,
    latest_price,
    latest_50_ma,
    latest_200_ma,
    latest_volatility,
    primary_performance,
    comparison_performance
)
# MARKET TAB
with market_tab:
    with st.container():
        st.caption(
            "This section shows price trends, moving averages, daily returns, and volatility for the selected market."
        )

        st.divider()

        # getting the market change trend
        market_change = latest_price - data["Close"].dropna().iloc[-2].item()
        if market_change > 0:
            market_trend = "rising"
        elif market_change < 0:
            market_trend = "falling"
        else:
            market_trend = "flat"

        # creates dashboard-style metric cards for the latest data
        metric_row1 = st.columns(4)

        with metric_row1[0]:
            metric_card(
                "Latest Price",
                f"${latest_price:,.2f}",
                market_change
            )

        with metric_row1[1]:
            metric_card(
                "Daily Return",
                f"{latest_return:.2f}%"
            )

        with metric_row1[2]:
            metric_card(
                "30-Day Return",
                f"{latest_30_day_return:.2f}%"
            )

        with metric_row1[3]:
            metric_card(
                "30-Day Sharpe",
                f"{latest_sharpe:.2f}"
            )

        metric_row2 = st.columns(4)
        with metric_row2[0]:
            metric_card(
            "30-Day Volatility",
            f"{latest_volatility:.2f}%"
        )
        with metric_row2[1]:
            metric_card(
            "Annualized Volatility",
            f"{latest_annualized_volatility:.2f}%"
        )
        with metric_row2[2]:
            metric_card(
            "Current Drawdown",
            f"{latest_drawdown:.2f}%"
        )
        with metric_row2[3]:
            metric_card(
            "Max Drawdown",
            f"{max_drawdown:.2f}%"
        )
        st.divider()

        # Market index chart
        st.subheader(f"{selected_market} - {selected_period}")
        fig = create_line_chart(
            data,
            ["Close", "50 Day MA", "200 Day MA"],
            f"{selected_market} Price & Moving Averages",
            "Price",
            market_colors[selected_market]
        )
        fig.data[0].line.color = market_colors[selected_market]
        fig.data[1].line.color = "#7FB3D5"
        fig.data[2].line.color = "#F5B7B1"
        st.plotly_chart(fig)

        st.divider()


        # Daily Returns Chart
        st.subheader("Daily Returns (%)")
        fig_returns = create_line_chart(
            data,
            "Daily Return",
            f"{selected_market} Daily Returns",
            "Daily Return (%)",
            market_colors[selected_market]
        )
        st.plotly_chart(fig_returns)

        st.divider()

        # 30-day Volatility Chart
        st.subheader("30-Day Rolling Volatility")
        fig_volatility = create_line_chart(
            data,
            "30 Day Volatility",
            f"{selected_market} 30-Day Rolling Volatility",
            "Volatility",
            market_colors[selected_market]
        )
        st.plotly_chart(fig_volatility)
        st.divider()

        # drawdown chart
        fig_drawdown = create_line_chart(
            data,
            "Drawdown",
            f"{selected_market} Drawdown",
            "Drawdown (%)",
            market_colors[selected_market]
        )
        st.plotly_chart(fig_drawdown)
        st.divider()
        # 30 day rolling chart
        fig_30_return = create_line_chart(
            data,
            "30 Day Return",
            f"{selected_market} 30-Day Rolling Return",
            "30-Day Return (%)",
            market_colors[selected_market]
        )
        st.plotly_chart(fig_30_return)
        st.divider()

        # Sharpe chart
        fig_sharpe = create_line_chart(
            data,
            "Rolling Sharpe Ratio",
            f"{selected_market} 30-Day Rolling Sharpe Ratio",
            "Sharpe Ratio",
            market_colors[selected_market]
        )
        st.plotly_chart(fig_sharpe)

        st.divider()
        # annualized volatility figure
        fig_annualized_volatility = create_line_chart(
            data,
            "Annualized Volatility",
            f"{selected_market} Annualized Volatility",
            "Annualized Volatility (%)",
            market_colors[selected_market]
        )
        st.plotly_chart(fig_annualized_volatility)

        # preview last 5 rows
        with st.expander("Preview Market Data"):
            st.dataframe(data.tail())

        # download data button
        csv_market = data.to_csv().encode("utf-8")
        st.download_button(
            label="Download Market Data CSV",
            data=csv_market,
            file_name="market_data.csv",
            mime="text/csv"
        )
        st.divider()

        st.caption("Source: Yahoo Finance via yfinance.")

# -------------------------
# Economic Data
# -------------------------

# get economic data, spinner shows when loading
with st.spinner("Loading economic data..."):
    economic_data = load_economic_data(
        fred,
        economic_series_code
    )

# join tables
combined_data = data[["Close"]].join(
    economic_data,
    how="inner"
)
# calculate rolling correlation
combined_data["Rolling Correlation"] = (
    combined_data["Close"]
    .rolling(window=30)
    .corr(combined_data["Economic Indicator"])
)

# deciding economic change trend
clean_economic_data = economic_data["Economic Indicator"].dropna()
latest_economic_value = clean_economic_data.iloc[-1].item()
previous_economic_value = clean_economic_data.iloc[-2].item()
economic_change = latest_economic_value - previous_economic_value
if economic_change > 0:
    trend = "Rising"
elif economic_change < 0:
    trend = "Falling"
else:
    trend = "Flat"

# ECON TAB
with econ_tab:
    with st.container():
        st.caption(
            "This section tracks the selected macroeconomic indicator using FRED data."
        )

        st.divider()

        st.subheader(selected_economic_indicator)
        # metric cards for latest data change
        econ_col1, econ_col2, econ_col3 = st.columns(3)
        econ_col1.metric(
            f"Latest Value ({economic_unit})",
            f"{latest_economic_value:.2f}"
        )
        econ_col2.metric(
            "Latest Change",
            f"{economic_change:.2f}"
        )
        econ_col3.metric(
            "Trend",
            trend
        )

        st.divider()

        # Macro Snapshot section
        st.subheader("Macro Snapshot")
        snapshot = (
            f"{selected_economic_indicator} is {trend.lower()} based on the latest available data. "
            f"Meanwhile, {selected_market} is currently {market_trend} based on the latest closing price."
        )
        st.info(snapshot)

        st.divider()

        # Insight Section
        st.subheader("Key Insights")
        for insight in insights:
            st.write(f"• {insight}")

        st.divider()
        # AI Commentary button
        st.subheader("AI Macro Commentary")
        if st.button("Generate AI Commentary"):
            with st.spinner("Generating AI commentary..."):
                commentary = generate_ai_commentary(
                    selected_market,
                    comparison_market,
                    selected_economic_indicator,
                    latest_price,
                    latest_return,
                    latest_30_day_return,
                    latest_volatility,
                    latest_drawdown,
                    trend,
                    insights
                )
            with st.container():
                st.markdown("### AI Market Commentary")
                st.write(commentary)
                st.caption(
                    "AI commentary is generated from dashboard metrics and is for educational purposes only. It should not be interpreted as financial advice."
                )

        st.divider()

        # drawing the chart
        fig_economic = create_line_chart(
            economic_data,
            "Economic Indicator",
            selected_economic_indicator,
            economic_unit
        )
        st.plotly_chart(fig_economic)

        st.divider()

        # preview last 5 rows
        with st.expander("Preview Economic Data"):
            st.dataframe(economic_data.tail())
        st.caption("Source: FRED Federal Reserve Economic Data.")

        # download economic data
        csv_economic = economic_data.to_csv().encode("utf-8")
        st.download_button(
            label="Download Economic Data CSV",
            data=csv_economic,
            file_name="economic_data.csv",
            mime="text/csv"
        )
# -------------------------
# Comparison Data
# -------------------------

with comparison_tab:
    with st.container():
        st.caption(
            "This section compares normalized performance between two selected assets. Both series start at 100."
        )

        st.divider()

        if selected_market == comparison_market:
            st.warning("Please select two different markets for comparison.")
            st.stop()

        # Comparison charts
        comparison_df = data[["Normalized"]].rename(
            columns={"Normalized": selected_market}
        ).join(
            comparison_data[["Normalized"]].rename(
                columns={"Normalized": comparison_market}
            ),
            how="inner"
        )

        comparison_fig = create_line_chart(
            comparison_df,
            [selected_market, comparison_market],
            f"{selected_market} vs {comparison_market}",
            "Normalized Value"
        )
        comparison_fig.data[0].line.color = market_colors[selected_market]
        comparison_fig.data[1].line.color = market_colors[comparison_market]
        st.plotly_chart(comparison_fig)

        st.divider()

        # Correlation section
        st.subheader("Rolling Correlation Analysis")
        st.info(
            """
            Correlation ranges from -1 to +1. 
            A positive value means the market and economic indicator tend to move together, 
            while a negative value means they tend to move in opposite directions. 
            Correlation does not imply causation.
            """
        )
        # correlation fig
        correlation_fig = create_line_chart(
            combined_data,
            "Rolling Correlation",
            f"{selected_market} vs {selected_economic_indicator}",
            "Correlation"
        )
        st.plotly_chart(correlation_fig)

        st.divider()

        # preview last 5 rows
        with st.expander("Preview Comparison Data"):
            st.dataframe(comparison_df.tail())

        csv_comparison = comparison_df.to_csv().encode("utf-8")

        # download comparison data
        st.download_button(
            label="Download Comparison Data CSV",
            data=csv_comparison,
            file_name="comparison_data.csv",
            mime="text/csv"
        )

        st.divider()

        st.caption("Source: Yahoo Finance via yfinance.")






# Footer at very bottom of web app
st.divider()
st.caption(
    "Data Sources: Yahoo Finance (market data) and FRED Federal Reserve Economic Data."
)
st.caption(
    "MacroLens is an educational analytics dashboard and should not be interpreted as financial advice."
)