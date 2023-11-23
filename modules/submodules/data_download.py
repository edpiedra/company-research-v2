from modules.submodules.download_modules.finnhub_data import * 
from modules.submodules.download_modules.finnlp_data import * 
from modules.submodules.download_modules.yahoo_data import * 
from modules.submodules.download_modules.seekingalpha_data import * 

class DataDownload():
    def __init__(self):
        print("[INFO] {:.2f}...initializing data download module".format(
            time.time()-start_time
        ))
        
        self.ticker = None 
        self.start_date = (dt.datetime.now() - relativedelta(years=1)).strftime("%Y-%m-%d")
        self.start_date_long = (dt.datetime.now() - relativedelta(years=5)).strftime("%Y-%m-%d")
        self.end_date = dt.datetime.now().strftime("%Y-%m-%d")
        
        self.finnhub_downloads = FinnHubDownloads()
        self.finnlp_downloads = FinNLPDownloads()
        self.yahoo_downloads = YahooDownloads()
        self.seekingalpha_downloads = SeekingAlphaDownloads()
        
    def run(self):
        print("[INFO] {:.2f}...running data download module".format(
            time.time()-start_time
        ))
        
        self.finnhub_downloads.ticker           = self.ticker 
        self.finnhub_downloads.start_date       = self.start_date 
        self.finnhub_downloads.start_date_long  = self.start_date_long 
        self.finnhub_downloads.end_date         = self.end_date
        
        self.finnhub_downloads.get_company_info()
        
        self.finnlp_downloads.ticker = self.ticker 
        self.finnlp_downloads.start_date = self.start_date 
        self.finnlp_downloads.start_date_long = self.start_date_long 
        self.finnlp_downloads.end_date = self.end_date 
        
        self.finnlp_downloads.get_company_info()
        
        self.yahoo_downloads.start_date = self.start_date
        self.yahoo_downloads.start_date_long = self.start_date_long 
        self.yahoo_downloads.end_date = self.end_date 
        self.yahoo_downloads.ticker = self.ticker 
        
        self.yahoo_downloads.get_company_info()
        
        self.seekingalpha_downloads.ticker = self.ticker
        self.seekingalpha_downloads.start_date_long = self.start_date
        self.seekingalpha_downloads.end_date = self.end_date
        
        self.seekingalpha_downloads.get_company_info()