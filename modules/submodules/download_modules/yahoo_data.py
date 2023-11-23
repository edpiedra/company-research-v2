from variables.variables import * 

class YahooDownloads():
    def __init__(self):
        print("[INFO] {:.2f}...initializing yahoo downloads module".format(
            time.time()-start_time
        ))
        
        self.ticker = None 
        self.start_date = None 
        self.start_date_long = None 
        self.end_date = None 
        
        
    def _market_data(self):
        print("[INFO] {:.2f}...getting market data from yahoo for {} from {} to {}".format(
            time.time()-start_time, self.ticker, self.start_date_long, self.end_date
        ))
        
        data = self.yf_ticker.history(
            start=self.start_date_long,
            end=self.end_date,
        )
        
        data.to_csv(self.folder + "/market data.csv")
        
    def _company_info(self):
        print("[INFO] {:.2f}...getting company info from yahoo for {}".format(
            time.time()-start_time, self.ticker
        ))
        
        data = pd.Series(self.yf_ticker.info)
        
        data.to_csv(self.folder + "/company info.csv")
        
    def _company_financials(self):
        print("[INFO] {:.2f}...getting financial statement from yahoo for {}".format(
            time.time()-start_time, self.ticker
        ))    
        
        inc = self.yf_ticker.quarterly_income_stmt 
        bs = self.yf_ticker.quarterly_balance_sheet
        cf = self.yf_ticker.quarterly_cash_flow 
        
        inc.to_csv(self.folder + "/income statement.csv")
        
        bs.to_csv(self.folder + "/balance sheet.csv")
        
        cf.to_csv(self.folder + "/cash flow.csv")
        
    def get_company_info(self):
        self.folder = f'./downloads/{self.ticker}/yahoo'

        if not(os.path.exists(self.folder)):
            os.makedirs(self.folder)
    
        self.yf_ticker = yf.Ticker(self.ticker)
        
        self._market_data()
        self._company_info()
        self._company_financials()