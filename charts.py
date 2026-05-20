import plotly.express as px
# create line chart function
def create_line_chart(df, y_columns, title, y_axis_title, line_color="#1f77b4"):
    fig = px.line(
        df,
        x=df.index,
        y=y_columns,
        title=title,
        height=500,
        color_discrete_sequence=None if isinstance(y_columns, list)
        else [line_color]
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=y_axis_title,
        hovermode="x unified"
    )
    return fig