import plotly.express as px

def create_chart(df, chart_type, x_col, y_col):
    """User ki choice ke hisab se Plotly chart banata hai."""
    title = f"{x_col} vs {y_col}"
    if chart_type == "Bar Chart":
        return px.bar(df, x=x_col, y=y_col, title=title)
    elif chart_type == "Line Chart":
        return px.line(df, x=x_col, y=y_col, title=title)
    elif chart_type == "Scatter Plot":
        return px.scatter(df, x=x_col, y=y_col, title=title)
    return None
