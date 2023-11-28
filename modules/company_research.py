from modules.submodules.gui import * 
from modules.submodules.data_download import * 
from modules.submodules.data_analysis import * 

class CompanyResearch():
    def __init__(self):
        print("[INFO] {:.2f}...initializing company research module".format(
            time.time()-start_time
        ))
        
        self.gui = GUI()
        self.downloads = DataDownload()
        self.analysis = DataAnalysis()
        
        header = html.Div(
            "COMPANY RESEARCH",
            style=GlobalLayouts.header_style
        )
        
        self.gui.layout()
        
        tabs = dcc.Tabs(
            [
                self.gui.tab
            ]
        )
        
        self.app = dash.Dash(
            __name__,
            external_stylesheets=[
                dbc.themes.BOOTSTRAP,
            ],
            prevent_initial_callbacks=True
        )

        self.app.layout = html.Div(
            [
                header,
                tabs
            ],
        )
        
        webbrowser.open_new("http://127.0.0.1:8050")
        
        @self.app.callback(
            Output("sector text", "children"),
            Output("industry text", "children"),
            Output("business summary text", "value"),
#            Output("market data graph", "figure"),
            Output("earnings call graph", "figure"),
            Output("insider sentiment graph", "figure"),
#            Output("earnings surprises graph", "figure"),
            Output("yahoo news graph", "figure"),
            Input("ticker dropdown", "value")
        )
        def _update_company_research(ticker):
#            self.downloads.ticker = ticker.upper()
#            self.downloads.run()
            
#            self.analysis.ticker = ticker.upper()
#            self.analysis.data_analysis()
            
            self.gui.ticker = ticker.upper()
            self.gui.create_screen()
            
            return self.gui.sector, self.gui.industry, self.gui.business_summary, \
                self.gui.earnings_calls_graph, self.gui.insider_sentiments, \
                    self.gui.yahoo_news