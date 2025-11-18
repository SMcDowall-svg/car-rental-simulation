import pandas as pd
from dash import Dash, dcc, html, dash_table, Input, Output

# Load data
data = pd.read_csv("profitable_rides.csv")
df = pd.DataFrame(data)

# Reformat datetime columns 
df["Start"] = pd.to_datetime(df["Start"]).dt.strftime("%Y-%m-%d")
df["End"] = pd.to_datetime(df["End"]).dt.strftime("%Y-%m-%d")

df = df.drop(columns=["revenue_minute", "revenue_km", "Rental_state"], errors="ignore")
df = df.round(0)

# Rename columns
df = df.rename(columns={
    "duration_minute": "Ride Duration (Minutes)",
    "car_id": "Car ID",
    "battery_left": "Remaining Battery",
    "profitable_minutes": "Profitable Minutes",
    "Incentive20": "Free 20mins",
    "Incentive15": "Free 15mins",
    "Incentive10": "Free 10mins",
    "Incentive5": "Free 5mins"
})
# App setup
app = Dash(__name__)

app.layout = html.Div([
    html.H2("Ride Incentives Suggestions"),

    # Filters
    html.Div([
        html.Label("Select Car ID:", style={"marginRight": "10px", "fontWeight": "bold"}),
        dcc.Dropdown(
            id="car-filter",
            options=[{"label": str(cid), "value": cid} for cid in df["Car ID"].unique()],
            value=df["Car ID"].unique()[0],
            clearable=False,
            style={"width": "200px"}
        ),

        html.Label("Select Start Date:", style={"marginLeft": "30px", "marginRight": "10px", "fontWeight": "bold"}),
        dcc.Dropdown(
            id="date-filter",
            options=[{"label": date, "value": date} for date in sorted(df["Start"].unique())],
            value=None,  
            placeholder="All Dates",
            clearable=True,
            style={"width": "200px"}
        )
    ], style={"marginBottom": "20px", "display": "flex", "alignItems": "center"}),

    dash_table.DataTable(
        id="rental-table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        filter_action="native",
        sort_action="native",
        page_size=10,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "center", "padding": "5px"},
        style_header={"backgroundColor": "#f4f4f4", "fontWeight": "bold"}
    )
])

@app.callback(
    Output("rental-table", "data"),
    Input("car-filter", "value"),
    Input("date-filter", "value")
)
def update_table(selected_car, selected_date):
    filtered_df = df[df["Car ID"] == selected_car]
    if selected_date:
        filtered_df = filtered_df[filtered_df["Start"] == selected_date]
    return filtered_df.to_dict("records")

if __name__ == "__main__":
    app.run(debug=True)