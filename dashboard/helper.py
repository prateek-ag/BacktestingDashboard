from multiprocessing.sharedctypes import Value
from yahooquery import Ticker
import yfinance as yf
import pandas as pd
import plotly.express as px
from plotly.graph_objs import *
import plotly.graph_objects as go

def get_symbol(symbol):
    name = Ticker(symbol).get_modules("quoteType")[symbol]["longName"]
    if name: return name
    raise ValueError("Could not find ticker")

def compress_legend(fig):
   group1_base, group2_base  = fig.data[0].name.split(",")
   lines_marker_name = []
   for i, trace in enumerate(fig.data):
       part1,part2 = trace.name.split(',')
       if part1 == group1_base:
           lines_marker_name.append({"line": trace.line.to_plotly_json(), "marker": trace.marker.to_plotly_json(), "mode": trace.mode, "name": part2.lstrip(" ")})
       if part2 != group2_base:
           trace['name'] = ''
           trace['showlegend']=False
       else:
           trace['name'] = part1
   
   ## Add the line/markers for the 2nd group
   for lmn in lines_marker_name:
       lmn["line"]["color"] = "white"
       lmn["marker"]["color"] = "white"
       fig.add_trace(go.Scatter(y=[None], **lmn))

   fig.update_layout(legend_title_text='', 
                     legend_itemclick=False,
                     legend_itemdoubleclick= False)

def get_data(ticker, existing_data):
    if not existing_data: existing_data = dict()
    temp_df = yf.Ticker(ticker).history(period="max")
    temp_df.index.names = ['Date']
    existing_data[ticker] = temp_df

    return existing_data

def get_stock_information_chart(tickers, value_vars, data):
    total_df = get_total_stock_information(tickers, data)
    total_df = pd.melt(total_df, value_vars=value_vars, id_vars=['Date', 'Ticker'])
    fig =  px.line(total_df, x="Date", y="value", color="Ticker", line_dash="variable")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', font = {'color':'#FFFFFF'})
    compress_legend(fig)
    return fig

def get_total_stock_information(tickers, data):
    to_return = pd.DataFrame()
    for ticker in tickers:
        to_return = to_return.append(data[ticker].reset_index().assign(Ticker=ticker))

    return to_return

def get_columns_from_data(tickers, data):
    all_cols = [data[i].columns for i in tickers]
    return list(set.intersection(*map(set,all_cols)))