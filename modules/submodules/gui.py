from variables.variables import * 
from modules.submodules.download_modules.finnhub_data import * 

class GUI():
    def __init__(self):
        print("[INFO] {:.2f}...initializing gui module".format(
            time.time()-start_time
        ))
        
        self.finnhub = FinnHubDownloads()
        self.finnhub.get_stock_symbols()
        
        self.ticker = None 
        self.sector = None 
        self.industry = None 
        self.business_summary = None 
        
    def create_screen(self):
        self.downloads_folder = f'./downloads/{self.ticker}'
        self.results_folder = f'./results/{self.ticker}'
        
        self._load_market_data()
        self._load_company_info()
        self._load_earnings_calls()
        self._load_insider_sentiments()
        self._load_yahoo_company_news()
        
    def _load_market_data(self):
        print("[INFO] {:.2f}...loading market data".format(
            time.time()-start_time
        ))
        
        df = pd.read_csv(
            self.downloads_folder + "/yahoo/market data.csv",
            usecols=[
                "Date", "Close"
            ]
        )
        
        df["period"] = pd.to_datetime(
            df["Date"],
            errors="coerce",
            format="%Y-%m-%d %H:%M:%S%z",
            utc=True
        )
        
        df["period"] = pd.to_datetime(
            df["period"],
            errors="coerce",
            format="%Y-%m-%d %H:%M:%S%z",
            utc=True
        ).dt.strftime("%Y%m%d")
        
        df.drop(
            "Date",
            axis=1,
            inplace=True
        )
        
        self.market_data = df.copy()
        
    def _load_company_info(self):
        print("[INFO] {:.2f}...loading company info".format(
            time.time()-start_time
        ))
        
        df = pd.read_csv(
            self.downloads_folder + "./yahoo/company info.csv",
            index_col=[0]
        )
        
        self.sector = df.loc["sector"][0]
        self.industry = df.loc["industry"][0]
        self.business_summary = df.loc["longBusinessSummary"][0]
         
    def _load_earnings_calls(self):
        print("[INFO] {:.2f} loading earnings calls".format(
            time.time()-start_time
        ))
        
        df = pd.read_csv(
            self.results_folder + "/earnings calls.csv",
            usecols=[
                "period", "textblob_polarity", "textblob_subjectivity",
                "SENTIMENT_SCORE_NLTK", "negative_WGT_LM"
            ]
        )
                
        df["period"] = df["period"].astype("unicode")
        
        df = self.market_data.merge(
            right=df,
            how="left",
            on="period"
        )
        
        df["period"] = pd.to_datetime(
            df["period"],
            errors="coerce",
            format="%Y%m%d"
        )
        
        df = df.set_index("period")
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.update_layout(
            {
                "paper_bgcolor": GlobalLayouts.LIGHT_COLOR,
                "plot_bgcolor": GlobalLayouts.LIGHT_COLOR,
                "title": {
                    "font": {
                        "family": "Courier New",
                        "size": 30
                    },
                    "text": "<b>Historical Earnings Calls",
                },
                "legend": {
                    "orientation": "h",
                }
            }
        )
        
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["Close"],
                connectgaps=True,
                name="Close",
            ),
            secondary_y=False
        )
    
        for col in df.columns:
            if col!="Close":
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df[col],
                        connectgaps=True,
                        yaxis="y2",
                        name=col
                    ),
                    secondary_y=True
                )
            
        self.earnings_calls_graph = fig
        
    def _load_insider_sentiments(self):
        print("[INFO] {:.2f}...loading insider sentiments".format(
            time.time()-start_time
        ))
        
        df = pd.read_csv(
            self.results_folder + "/insider sentiments.csv",
            usecols=[
                "year", "month", "mspr"
            ]
        )
        
        df["day"] = 1
        df["period"] = pd.to_datetime(df[["year", "month", "day"]]) + \
            pd.offsets.MonthEnd(0)
            
        df["period"] = df["period"].dt.strftime("%Y%m%d")
        
        df = self.market_data.merge(
            right=df,
            how="left",
            on="period"
        )
        
        df["period"] = pd.to_datetime(
            df["period"],
            errors="coerce",
            format="%Y%m%d"
        )
        
        df = df.set_index("period")
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.update_layout(
            {
                "paper_bgcolor": GlobalLayouts.LIGHT_COLOR,
                "plot_bgcolor": GlobalLayouts.LIGHT_COLOR,
                "title": {
                    "font": {
                        "family": "Courier New",
                        "size": 30
                    },
                    "text": "<b>Insider Sentiments",
                },
                "legend": {
                    "orientation": "h",
                }
            }
        )
        
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["Close"],
                connectgaps=True,
                name="Close",
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["mspr"],
                connectgaps=True,
                name="mspr",
            ),
            secondary_y=True
        )
        
        self.insider_sentiments = fig 
    
    def _load_yahoo_company_news(self):
        print("[INFO] {:.2f}...loading yahoo company news".format(
            time.time()-start_time
        ))
        
        df = pd.read_csv(
            self.results_folder + "/yahoo company news.csv",
            usecols=[
                "datetime", "textblob_polarity", "textblob_subjectivity",
                "SENTIMENT_SCORE_NLTK", "negative_WGT_LM"
            ]
        )
        
        df["period"] = pd.to_datetime(
            df["datetime"],
            errors="coerce",
            format="%Y-%m-%d %H:%M:%S"
        ).dt.strftime("%Y%m%d")
        
        df.drop(
            ["datetime"],
            axis=1,
            inplace=True,
        )
        
        df = df.groupby("period").sum().reset_index()
        
        df = self.market_data.merge(
            right=df,
            how="left",
            on="period"
        )
        
        df = df.set_index("period")
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.update_layout(
            {
                "paper_bgcolor": GlobalLayouts.LIGHT_COLOR,
                "plot_bgcolor": GlobalLayouts.LIGHT_COLOR,
                "title": {
                    "font": {
                        "family": "Courier New",
                        "size": 30
                    },
                    "text": "<b>Historical Yahoo News",
                },
                "legend": {
                    "orientation": "h",
                }
            }
        )
        
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["Close"],
                connectgaps=True,
                showlegend=True,
                name="Close"
            ),
            secondary_y=False
        )
    
        for col in df.columns:
            if col!="Close":
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df[col],
                        connectgaps=True,
                        showlegend=True,
                        name=col
                    ),
                    secondary_y=True
                )
            
        self.yahoo_news = fig 
        
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
        
        sector_label = html.Div(
            "sector",
            style=GlobalLayouts.container_style
        )
        
        sector_text = html.Div(
            id="sector text",
            style=GlobalLayouts.container_style
        )
        
        sector_cont = html.Div(
            [
                sector_label,
                sector_text
            ],
            style=GlobalLayouts.container_style
        )
        
        industry_label = html.Div(
            "industry",
            style=GlobalLayouts.container_style
        )
        
        industry_text = html.Div(
            id="industry text",
            style=GlobalLayouts.container_style
        )
        
        industry_cont = html.Div(
            [
                industry_label,
                industry_text
            ],
            style=GlobalLayouts.container_style
        )
        
        business_summary_text = dcc.Textarea(
            id="business summary text",
            wrap=True,
            style=GlobalLayouts.input_style | {
                "width"     : "100%",
                "height"    : 250
            }
        )
        
        business_summary_cont = html.Div(
            [
                business_summary_text
            ],
            style=GlobalLayouts.container_style
        )
        
        earnings_call_graph = dcc.Graph(
            id="earnings call graph"
        )
        
        earnings_call_cont = html.Div(
            [
                earnings_call_graph
            ],
            style=GlobalLayouts.container_style
        )
        
        insider_sentiment_graph = dcc.Graph(
            id="insider sentiment graph"
        )
        
        insider_sentiment_cont = html.Div(
            [
                insider_sentiment_graph
            ],
            style=GlobalLayouts.container_style
        )
        
        yahoo_news_graph = dcc.Graph(
            "yahoo news graph"
        )
        
        yahoo_news_cont = html.Div(
            [
                yahoo_news_graph
            ],
            style=GlobalLayouts.container_style
        )
        
        tab_cont = html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row(ticker_input_cont),
                                dbc.Row(sector_cont),
                                dbc.Row(industry_cont),
                            ],
                            width=2
                        ),
                        dbc.Col(business_summary_cont)
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(earnings_call_cont, width=6),
                        dbc.Col(insider_sentiment_cont)
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(yahoo_news_cont, width=6),
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