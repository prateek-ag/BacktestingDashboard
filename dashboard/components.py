from dash import html, dcc, Input, Output, Dash
import dash_bootstrap_components as dbc

left_sidebar = [
        html.H3("BackTesting Dashboard", style={'color': "white", 'margin-bottom': '10%'}),
        
        html.Div([
            html.P("Pick Strategy", style={'color': 'white', 'margin-bottom': '0%'}),
            dcc.Dropdown(id="strategy_dropdown", style={'width': '87%'})
        ], style={"margin-bottom": "5%"}),
        html.Div([
            html.P("Search for Ticker", style={'color': 'white', 'margin-bottom': '0%'}),
            dcc.Input(id="ticker_input", type="text", placeholder="Press Enter to Search", debounce=True, style={'width': '75%'})]),

        html.Div(dcc.Checklist(id="ticker_checklist", options=[], value=[], labelStyle={"display": "inline-block", 'margin-top':'2%', 'color': 'white', 'padding': '2%'}, 
            inputStyle={"margin-right": "5px"}), style={"overflow": "auto", 'flex-grow': '1'}), 

         dcc.Upload(
            id="data_upload",
            children=html.Div(["Drag and Drop or ", html.A("Select File(s)"), 
                                html.I(id="tooltip-target", className="fas fa-question-circle", style={"float": "right", "margin-right": "2%", 'margin-top': '2%'}),
                                dbc.Tooltip(
                                    ["CSV file(s) containing at least: Date, Open (open price on date)."],
                                    target="tooltip-target",)]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin-bottom": "8%",
                'color': 'white'
            },
            # Allow multiple files to be uploaded
            multiple=True,
        ),
        dbc.Button("Run Backtest", id="execute_button", style={"float": 'right', 'margin-left': 'auto', "background-color": "#79C8FD", 'color': 'black', 'width': '40%', 'margin-bottom': '6%'})
    
]

stock_information_tab = [
    html.Div(dcc.Dropdown(id="stock_info_chart_col_picker", multi=True), style={"width": "40%", "margin": "2% 2% 2% auto"}),
    dcc.Graph(id="stock_information_chart")
]

performance_result_tab = [
    html.H1("performance results", id="performance_result_tab_header"),
    dcc.Textarea(id="testing_area")
]

strategy_data_tab = [
    html.H1("strategy data", id="strategy_data_tab_header") 
]

main_content = [
    html.Div(id = "stock_information_tab", children = stock_information_tab, style={"display": "none"}),
    html.Div(id = "performance_result_tab", children = performance_result_tab, style={"display": "none"}),
    html.Div(id= "strategy_data_tab", children = strategy_data_tab, style={"display":"none"})
]

left_sidebar_style = {'backgroundColor': "black", 'height': '100vh', 'min-height': '100vh', 'padding-left': '2%', 'padding-top': '0.7%', "display": "flex", 'flex-direction': 'column'}