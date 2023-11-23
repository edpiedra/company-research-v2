from variables.variables import * 

class SeekingAlphaDownloads():
    def __init__(self):
        print("[INFO] {:.2f}...initializing seeking alpha downloads module".format(
            time.time()-start_time
        ))
        
        self.ticker = None
        self.start_date = None 
        self.start_date_long = None 
        self.end_date = None 
        
        
    def get_company_info(self):
        print("[INFO] {:.2f}...running seekingalpha download module".format(
            time.time()-start_time
        ))    
        self.folder = f'./downloads/{self.ticker}/seekingalpha'

        if not(os.path.exists(self.folder)):
            os.makedirs(self.folder)
            
        self.driver = webdriver.Firefox()
        self._download_earnings_calls()
        
    
    def _download_earnings_calls(self):
        print("[INFO] {:.2f}...downloading earnings calls from seeking alpha".format(
            time.time()-start_time
        ))
        
        transcript_folder = self.folder + "/transcripts"
        
        if not(os.path.exists(transcript_folder)):
            os.makedirs(transcript_folder)
            
        SA_URL = "https://seekingalpha.com/"
        TRANSCRIPT = re.compile("Earnings Call Transcript")
        
        url = f'{SA_URL}symbol/{self.ticker}/earnings/transcripts'
        self.driver.get(url)
        time.sleep(2)
        response = self.driver.page_source 
        soup = BeautifulSoup(response, "lxml")
        links = soup.find_all(name="a", string=TRANSCRIPT)
        
        for link in links:
            transcript_url = link.attrs.get("href")
            article_url = furl(urljoin(SA_URL, transcript_url)).add({"part": "single"})
            self.driver.get(article_url.url)
            html = self.driver.page_source 
            soup = BeautifulSoup(html, "lxml")
            content = []
            headline = soup.find("head").text 
            
            try:
                period = re.search(r' Q\d \d+', headline).group().strip()
                
                quarter = int(period[1])
                year = int(period[-4:])
                _date = dt.datetime(year, quarter*3-2, 1).strftime("%Y-%m-%d")
                _date = pd.Timestamp(_date) + pd.offsets.MonthEnd(n=1)
                
                if (_date < dt.datetime.strptime(self.start_date_long, "%Y-%m-%d")):
                    break

                print("[INFO] {:.2f}...downloading {} transcripts for {}".format(
                    time.time()-start_time, self.ticker, period
                ))
                
                for header in [p.parent for p in soup.find_all("strong")]:
                    text = header.text.strip()
                    
                    if text.lower().startswith('copyright'):
                        continue 
                    elif text.lower().startswith('question-and'):
                        break 
                    elif "participant" in text.lower():
                        continue 
                    else:
                        p = []
                        
                        for participant in header.find_next_siblings('p'):
                            if participant.find("strong"):
                                break
                            else:
                                p.append(participant.text)
                                
                        content.append(['\n'.join(p)])
                filename = transcript_folder + f'/{period}.json'
                json.dump(content, open(filename, "w"))
            except:
                continue