from dash import html, dcc
import dash
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import components, helper
import yfinance as yf

from dash_extensions.enrich import Dash, ServersideOutput, Trigger, Output, Input, State


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://use.fontawesome.com/releases/v5.8.1/css/all.css'])

app.layout = html.Div(
    [
        dbc.Row([
            dbc.Col(width=3, style=components.left_sidebar_style, children=components.left_sidebar),
            dbc.Col(width=9, children=[
                dcc.Tabs(
                    [dcc.Tab(label="Stock Information", style={'backgroundColor': 'black', 'borderColor': 'Grey'}, value="stock_information"),
                    dcc.Tab(label="Strategy Performance Results",style={'backgroundColor': 'black', 'borderColor': 'grey'}, value="performance_result"),
                    dcc.Tab(label="Strategy Specific Data", style={'backgroundColor': 'black', 'borderColor': 'grey'}, value="strategy_data")],
                    style={'width': '101%', 'margin': '-1%', 'height': '5%', 'color': 'white', 'font-size': '90%'}, id="main_tab"
                ),
                html.Div(style={"backgroundColor": "black", "height": "85%", "margin": "3%", "borderRadius": "35px", 'padding': '0.8% 2%'}, id="content", children = components.main_content)
            ], style={})
        ], style={'height': '100%'}),

        dcc.Store(id="data_store_1", data=dict()),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Error")),
                dbc.ModalBody("This is the content of the modal"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="error_modal",
            is_open=False,
        )
    ], 
    style={'height': '100vh', 'backgroundColor': ' #383838'}
)

@app.callback(
    [Output("stock_information_tab", "style"),
    Output("performance_result_tab", "style"),
    Output("strategy_data_tab", "style")],
    [Input("main_tab", "value")]
)
def render_tab(tab):
    to_return = [{"display": "none"}] * 3

    if tab == "stock_information":
        to_return[0] = {"display": "block"}
    if tab == "performance_result":
        to_return[1] = {"display": "block"}
    if tab == "strategy_data":
        to_return[2] = {"display": "block"}

    return to_return

@app.callback(
    [Output("ticker_checklist", "options"),
    Output("ticker_checklist", "value"),
    ServersideOutput("data_store_1", "data"),
    Output("ticker_input", "value")],
    [Input("ticker_input", "value")],
    [State("ticker_checklist", "options"),
    State("ticker_checklist", "value"),
    State("data_store_1", "data")]
)
def search_tickers(ticker_name, options, value, existing_data):
    if not ticker_name or ticker_name == '': raise PreventUpdate

    all_tickers = [i['value'] for i in options]
    if ticker_name in all_tickers: raise PreventUpdate

    try:
        name = helper.get_symbol(ticker_name)
        options.append({"label": name, "value": ticker_name})
    except:
        print("Could not find given ticker")
        raise PreventUpdate
    else:
        value.append(ticker_name)
        data = helper.get_data(ticker_name, existing_data)
        return options, value, data, ""


@app.callback(
    [Output("stock_info_chart_col_picker", "options"),
    Output("stock_info_chart_col_picker", "value")],
    [Input("execute_button", "n_clicks")],
    [State("ticker_checklist", "value"),
    State("data_store_1", "data")]
)
def update_stock_information_column_picker(n_clicks, tickers, data):
    if n_clicks and data and tickers:
        columns = helper.get_columns_from_data(tickers, data)
        print(columns)
        options = [{'label': i, 'value': i} for i in columns]
        value = [i for i in ["Open", "High", "Low"] if i in columns]

        return options, value
    
    raise PreventUpdate


@app.callback(
    Output("stock_information_chart", "figure"),
    [Input("execute_button", "n_clicks"),
    Input("stock_info_chart_col_picker", "value")],
    [State("ticker_checklist", "value"),
    State("data_store_1", "data")]
)
def update_stock_information(n_clicks, columns, tickers, data):
    if n_clicks and data:
        return helper.get_stock_information_chart(tickers, columns, data)
    raise PreventUpdate

@app.callback(
    Output("ticker_checklist", "value"),
    [Input("testing_area", "n_blur")],
    State("testing_area", "value")
)
def test(n_blur, text):
    if n_blur:
        print(text.splitlines())
    raise PreventUpdate


# @app.callback(
#     [Output("data_store_1", "data"),
#     Output("ticker_checklist", "options"),
#     Output("ticker_checklist", "value")],
#     [Input("data_upload", "contents"),
#     Input("data_upload", "filename")]
# )
# def add_uploaded_data(contents, filenames):
#     if contents:
#         for i in range(len(contents)):
#             name = filenames[i]
#             content = contents[i]

#             ticker, extension = filenames.split('.')
#             if extension != "csv":
#                 return None



if __name__ == '__main__':
    app.run_server(debug=True)
