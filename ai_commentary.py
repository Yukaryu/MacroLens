import os

from google import genai


def generate_ai_commentary(
    selected_market,
    comparison_market,
    selected_economic_indicator,
    latest_price,
    latest_return,
    latest_30_day_return,
    latest_volatility,
    latest_drawdown,
    economic_trend,
    insights
):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "AI commentary is unavailable because no Gemini API key was found."

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are writing concise macro-financial commentary for a student-built dashboard.

    Write 1 short paragraph, around 80-120 words.
    Do not give investment advice.
    Do not predict exact future prices.
    Be analytical, clear, and cautious.

    Dashboard data:
    - Selected market: {selected_market}
    - Comparison market: {comparison_market}
    - Economic indicator: {selected_economic_indicator}
    - Latest price: {latest_price}
    - Latest daily return: {latest_return:.2f}%
    - 30-day return: {latest_30_day_return:.2f}%
    - 30-day volatility: {latest_volatility:.2f}%
    - Current drawdown: {latest_drawdown:.2f}%
    - Economic trend: {economic_trend}
    - Rule-based insights: {insights}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        error_message = str(e)
        if "429" in error_message:
            return """
        AI commentary is temporarily unavailable because the free API quota has been exceeded.
        Please wait a few moments and try again.
        """
        elif "503" in error_message:
            return """
        The AI service is currently experiencing high demand.
        Please try again shortly.
        """
        else:
            return """
        An unexpected AI error occurred.
        Please try again later.
        """