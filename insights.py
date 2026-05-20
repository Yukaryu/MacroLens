
def generate_market_insights(
    selected_market,
    comparison_market,
    latest_price,
    latest_50_ma,
    latest_200_ma,
    latest_volatility,
    primary_performance,
    comparison_performance
):
    insights = []

    if latest_price > latest_200_ma:
        insights.append(
            f"{selected_market} is trading above its 200-day moving average."
        )
    else:
        insights.append(
            f"{selected_market} is trading below its 200-day moving average."
        )

    if latest_50_ma > latest_200_ma:
        insights.append(
            "A bullish Golden Cross structure is currently present."
        )
    else:
        insights.append(
            "A bearish Death Cross structure is currently present."
        )

    if latest_volatility > 2:
        insights.append(
            "Market volatility is currently elevated."
        )
    else:
        insights.append(
            "Market volatility is relatively moderate."
        )

    if primary_performance > comparison_performance:
        insights.append(
            f"{selected_market} has outperformed {comparison_market} over the selected period."
        )
    else:
        insights.append(
            f"{comparison_market} has outperformed {selected_market} over the selected period."
        )

    return insights