from variables.variables import * 
from modules.submodules.download_modules.finnhub_data import * 

class GUI():
    def __init__(self):
        print("[INFO] {:.2f}...initializing gui module".format(
            time.time()-start_time
        ))
        
        self.finnhub = FinnHubDownloads()
        self.finnhub.get_stock_symbols()
        
    def layout(self):
        print("[INFO] {:.2f}...creating layout".format(
            time.time()-start_time
        ))
        
        ticker_label = html.Div(
            "ticker",
            style=GlobalLayouts.container_style
        )
        
        ticker_dropdown = dcc.Dropdown(
            options=[
                {
                    "label": t, "value": t
                } for t in self.finnhub.tickers
            ],
            id="ticker dropdown",
            style=GlobalLayouts.dropdown_style
        )
        
        ticker_input_cont = html.Div(
            [
                ticker_label,
                ticker_dropdown
            ],
            style=GlobalLayouts.container_style
        )
        
        description_label = html.Div(
            "description",
            style=GlobalLayouts.container_style
        )
        
        description = dcc.Textarea(
            id="description",
            wrap=True,
            style=GlobalLayouts.input_style
        )
        
        description_cont = html.Div(
            [
                description_label,
                description
            ],
            style=GlobalLayouts.container_style
        )
        
        historical_graph = dcc.Graph(
            id="historical graph",
        )
        
        historical_graph_cont = html.Div(
            [
                historical_graph
            ],
            style=GlobalLayouts.container_style
        )
        
        tab_cont = html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(ticker_input_cont, width=3),
                        dbc.Col(description_cont)
                    ]
                ),
                dbc.Row(
                    [
                        historical_graph_cont
                    ]
                )
            ],
            style=GlobalLayouts.container_style 
        )
        
        self.tab = dcc.Tab(
            children=tab_cont,
            style=GlobalLayouts.tab_style,
            selected_style=GlobalLayouts.tab_selected_style     
        )