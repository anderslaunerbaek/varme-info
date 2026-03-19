import plotly.express as px
from sqlalchemy import Engine, create_engine

import dash
from dash import Input, Output, State, dcc, html
from src import Config
from src.dash.dummy import build_dataframe, generate_sample_data
from src.dash.style import (
    _all_option,
    _hidden,
    _login_visible,
    style_login_fields,
    style_login_label,
)
from src.data import HeatUnit, HeatUnitType, SensorRecord, SensorRecordType
from src.functions import verify_login

heat_units, sensor_records = generate_sample_data()
df = build_dataframe(heat_units, sensor_records)


config = Config()
engine: Engine = create_engine(config.database_url)

# --- Dash app ---

app = dash.Dash(__name__, title="Heat Unit Dashboard")


# --- Layout (both sections always in DOM) ---

app.layout = html.Div(
    [
        dcc.Store(id="auth-store", storage_type="session"),
        # Login section
        html.Div(
            id="login-section",
            style=_login_visible,
            children=[
                html.Div(
                    style={
                        "backgroundColor": "white",
                        "padding": "40px",
                        "borderRadius": "8px",
                        "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
                        "width": "320px",
                    },
                    children=[
                        html.H2(
                            "Heat Unit Dashboard",
                            style={"textAlign": "center", "marginBottom": "8px"},
                        ),
                        html.P(
                            "Sign in to continue",
                            style={
                                "textAlign": "center",
                                "color": "#666",
                                "marginBottom": "24px",
                            },
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Username",
                                    style=style_login_label,
                                ),
                                dcc.Input(
                                    id="login-username",
                                    type="text",
                                    placeholder="Enter username",
                                    style=style_login_fields,
                                    n_submit=0,
                                ),
                            ],
                            style={"marginBottom": "16px"},
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Password",
                                    style=style_login_label,
                                ),
                                dcc.Input(
                                    id="login-password",
                                    type="password",
                                    placeholder="Enter password",
                                    style=style_login_fields,
                                    n_submit=0,
                                ),
                            ],
                            style={"marginBottom": "16px"},
                        ),
                        html.Div(
                            id="login-error",
                            style={
                                "color": "red",
                                "marginBottom": "12px",
                                "fontSize": "0.9em",
                            },
                        ),
                        html.Button(
                            "Sign In",
                            id="login-button",
                            n_clicks=0,
                            style={
                                "width": "100%",
                                "padding": "10px",
                                "backgroundColor": "#1a73e8",
                                "color": "white",
                                "border": "none",
                                "borderRadius": "4px",
                                "cursor": "pointer",
                                "fontSize": "1em",
                            },
                        ),
                    ],
                )
            ],
        ),
        # Dashboard section
        html.Div(
            id="dashboard-section",
            style=_hidden,
            children=[
                html.Div(
                    style={
                        "fontFamily": "sans-serif",
                        "maxWidth": "1200px",
                        "margin": "0 auto",
                        "padding": "20px",
                    },
                    children=[
                        html.Div(
                            style={
                                "display": "flex",
                                "justifyContent": "space-between",
                                "alignItems": "center",
                                "marginBottom": "8px",
                            },
                            children=[
                                html.H1(
                                    "Heat Unit Sensor Dashboard", style={"margin": "0"}
                                ),
                                html.Button(
                                    "Logout",
                                    id="logout-button",
                                    n_clicks=0,
                                    style={
                                        "padding": "8px 16px",
                                        "backgroundColor": "#e53935",
                                        "color": "white",
                                        "border": "none",
                                        "borderRadius": "4px",
                                        "cursor": "pointer",
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            style={
                                "display": "grid",
                                "gridTemplateColumns": "1fr 1fr 2fr",
                                "gap": "16px",
                                "marginBottom": "20px",
                            },
                            children=[
                                html.Div(
                                    [
                                        html.Label(
                                            "Heat Unit Type",
                                            style={"fontWeight": "bold"},
                                        ),
                                        dcc.Dropdown(
                                            id="heat-unit-type-filter",
                                            options=[_all_option]
                                            + [
                                                {"label": str(t), "value": str(t)}
                                                for t in HeatUnitType
                                            ],
                                            value="All",
                                            clearable=False,
                                        ),
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.Label(
                                            "Sensor Record Type",
                                            style={"fontWeight": "bold"},
                                        ),
                                        dcc.Dropdown(
                                            id="sensor-type-filter",
                                            options=[_all_option]
                                            + [
                                                {"label": str(t), "value": str(t)}
                                                for t in SensorRecordType
                                            ],
                                            value="All",
                                            clearable=False,
                                        ),
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.Label(
                                            "Heat Units", style={"fontWeight": "bold"}
                                        ),
                                        dcc.Dropdown(
                                            id="heat-unit-filter",
                                            options=[
                                                {"label": u.name, "value": u.id}
                                                for u in heat_units
                                            ],
                                            value=[u.id for u in heat_units],
                                            multi=True,
                                            placeholder="Select heat units...",
                                        ),
                                    ]
                                ),
                            ],
                        ),
                        dcc.Graph(id="time-series-chart", style={"height": "500px"}),
                        html.Div(
                            id="record-count",
                            style={
                                "color": "#666",
                                "marginTop": "8px",
                                "fontSize": "0.9em",
                            },
                        ),
                    ],
                )
            ],
        ),
    ]
)


@app.callback(
    Output("auth-store", "data"),
    Output("login-error", "children"),
    Input("login-button", "n_clicks"),
    Input("logout-button", "n_clicks"),
    Input("login-username", "n_submit"),
    Input("login-password", "n_submit"),
    State("login-username", "value"),
    State("login-password", "value"),
    State("auth-store", "data"),
    prevent_initial_call=True,
)
def handle_auth(
    login_clicks,
    logout_clicks,
    username_submit,
    password_submit,
    username,
    password,
    auth_data,
):
    triggered_id = dash.ctx.triggered_id

    if triggered_id == "logout-button":
        return None, ""

    if triggered_id in ("login-button", "login-username", "login-password"):
        if username and password:
            is_valid, user = verify_login(engine, username, password)
        else:
            is_valid = False
        if is_valid:
            return {"authenticated": True, "user_id": user.id}, ""
        return auth_data, "Invalid username or password."

    return dash.no_update, dash.no_update


@app.callback(
    Output("login-section", "style"),
    Output("dashboard-section", "style"),
    Input("auth-store", "data"),
)
def toggle_sections(auth_data):
    if auth_data and auth_data.get("authenticated"):
        return _hidden, {"display": "block"}
    return _login_visible, _hidden


@app.callback(
    Output("time-series-chart", "figure"),
    Output("record-count", "children"),
    Input("heat-unit-type-filter", "value"),
    Input("sensor-type-filter", "value"),
    Input("heat-unit-filter", "value"),
)
def update_chart(heat_unit_type: str, sensor_type: str, selected_unit_ids: list[str]):
    filtered = df.copy()

    if heat_unit_type != "All":
        filtered = filtered[filtered["heat_unit_type"] == heat_unit_type]

    if sensor_type != "All":
        filtered = filtered[filtered["sensor_type"] == sensor_type]

    if selected_unit_ids:
        filtered = filtered[filtered["heat_unit_id"].isin(selected_unit_ids)]

    count_text = f"Showing {len(filtered):,} records"

    if filtered.empty:
        fig = px.line(title="No data for selected filters")
        fig.update_layout(paper_bgcolor="#fafafa")
        return fig, count_text

    filtered = filtered.sort_values("time_stamp")

    fig = px.line(
        filtered,
        x="time_stamp",
        y="value",
        color="heat_unit_name",
        line_dash="sensor_type",
        title="Sensor Readings Over Time",
        labels={
            "time_stamp": "Time",
            "value": "Value",
            "heat_unit_name": "Heat Unit",
            "sensor_type": "Sensor Type",
        },
    )
    fig.update_layout(
        legend_title_text="Heat Unit / Sensor Type",
        hovermode="x unified",
    )

    return fig, count_text


server = app.server

if __name__ == "__main__":
    app.run(debug=config.app_debug, port=config.app_port, host=config.app_host)
