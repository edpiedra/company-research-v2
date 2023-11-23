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
            Output("description", "value"),
#            Output("historical graph", "figure"),
            Input("ticker dropdown", "value")
        )
        def _update_company_research(ticker):
            self.downloads.ticker = ticker.upper()
            self.downloads.run()
            
            self.analysis.ticker = ticker.upper()
            self.analysis.data_analysis()
            
            return "description"