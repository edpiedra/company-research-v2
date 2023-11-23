from modules.submodules.analysis_modules._nltk_analysis import * 
from modules.submodules.analysis_modules._spacy_lm_analysis import * 
from modules.submodules.analysis_modules._textblob_analysis import * 

class DataAnalysis():
    def __init__(self):
        print("[INFO] {:.2f}...initializing data analysis module".format(
            time.time()-start_time
        ))
        
        self.ticker = None 
        self.file_contents = None 
        
        self.textblob = TextblobAnalysis()
        self.spacy = SpacyLMAnalysis()
        self.nltk = NLTKAnalysis()
        
    def _run_through_nlp_models(self):
        self.textblob.file_contents = self.file_contents 
        self.textblob.get_properties()
        
        self.spacy.file_contents = self.file_contents 
        self.spacy.get_sentiments()
        
        self.nltk.file_contents = self.file_contents 
        self.nltk.get_sentiment_score()
        
    def _finnhub_company_news(self):
        print("[INFO] {:.2f}...analyzing finnhub company news".format(
            time.time()-start_time
        ))
        
        news = json.load(open(self.folder + "/company news.json", "r"))
        
        data = {
            "datetime"  : [],
            "headline"  : [],
            "source"    : [],
            "summary"   : [],
        }
        
        results = {
            "textblob_polarity" : [],
            "textblob_subjectivity" : [],
            "NEGATIVE_NLTK" : [],
            "NEUTRAL_NLTK"  : [],
            "POSITIVE_NLTK" : [],
            "SENTIMENT_SCORE_NLTK"  : [],
        }
        
        for article in news:
            summary = article["summary"]
            
            if summary.startswith("Looking for stock market analysis"):
                continue 
            
            for field in data:
                data[field].append(article[field])
            
                
            self.file_contents = article["summary"]
            self._run_through_nlp_models()
            
            results["textblob_polarity"].append(self.textblob.polarity) 
            results["textblob_subjectivity"].append(self.textblob.subjectivity) 
            results["NEGATIVE_NLTK"].append(self.nltk.sentiment_ratio["NEGATIVE_NLTK"])
            results["NEUTRAL_NLTK"].append(self.nltk.sentiment_ratio["NEUTRAL_NLTK"])
            results["POSITIVE_NLTK"].append(self.nltk.sentiment_ratio["POSITIVE_NLTK"])
            results["SENTIMENT_SCORE_NLTK"].append(self.nltk.sentiment_ratio["SENTIMENT_SCORE_NLTK"])
            
            for sentiment in self.spacy.text_sentiments:
                if sentiment in results:
                    results[sentiment].append(self.spacy.text_sentiments[sentiment])
                else:
                    results[sentiment] = [self.spacy.text_sentiments[sentiment]]
        
        df_data = pd.DataFrame(data=data)
        df_results = pd.DataFrame(data=results)
        
        df = pd.concat(
            [
                df_data, df_results
            ],
            axis=1
        )
        
        df["period"] = pd.to_datetime(
            df["datetime"],
            errors="coerce",
            unit="s"
        ).dt.strftime("%Y%m%d"
                      )
        df.to_csv(self.target + "/finnhub company news.csv")
        
    def _earnings_surprises(self):
        print("[INFO] {:.2f}...analyzing earnings surprises".format(
            time.time()-start_time
        ))        
        
        earnings = json.load(open(self.folder + "/earnings surprises.json", "r"))
        
        data = {
            "period"    : [],
            "surprisePercent"   : [],
        }
        
        for earning in earnings:
            for field in data:
                data[field].append(earning[field])
                
        df = pd.DataFrame(data=data)
        
        df["period"] = pd.to_datetime(
            df["period"],
            errors="coerce",
            format="%Y-%m-%d"
        ).dt.strftime("%Y%m%d")
        
        df.to_csv(self.target + "/earnings surprises.csv")
        
    def _insider_sentiments(self):
        print("[INFO] {:.2f}...analyzing insider sentiments".format(
            time.time()-start_time
        ))    
        
        insiders = json.load(open(self.folder + "/insider sentiments.json", "r"))["data"]
        
        data = {
            "year"  : [],
            "month" : [],
            "mspr"  : [],
        }
        
        for insider in insiders:
            for field in data:
                data[field].append(insider[field])
                
        df = pd.DataFrame(
            data=data
        )
        
        df["period"] = df["year"].astype(str) + df["month"].astype(str)
        
        df["period"] = pd.to_datetime(
            df["period"],
            errors="coerce",
            format="%Y%m"
        ) + pd.offsets.QuarterEnd(0)
        
        df["period"] = df["period"].dt.strftime("%Y%m%d")
        
        df.to_csv(self.target + "/insider sentiments.csv")
        
    def _recommendation_trends(self):
        print("[INFO] {:.2f}...analyzing recommendation trends".format(
            time.time()-start_time
        ))
        
        recommendations = json.load(open(self.folder + "/recommendation trends.json", "r"))
        
        data = {
            "buy"   : [],
            "hold"  : [],
            "period"    : [],
            "sell"  : [],
            "strongBuy" : [],
            "strongSell"    : [],
        }
        
        for recommendation in recommendations:
            for field in data:
                data[field].append(recommendation[field])
                
        df = pd.DataFrame(data=data)
        
        df["period"] = pd.to_datetime(
            df["period"],
            errors="coerce",
            format="%Y-%m-%d"
        ).dt.strftime("%Y%m%d")
        
        df.to_csv(self.target + "/recommendation trends.csv")
        
    def _stocktwits(self):
        print("[INFO] {:.2f}...analyzing stocktwits".format(
            time.time()-start_time
        ))    
        
        stocktwits = pd.read_csv(self.folder + "/stocktwits.csv")
        
        data = {
            "created_at"    : [],
            "sentiment"     : [],
        }
        
        for _, twit in stocktwits.iterrows():
            entities = twit["entities"].replace("\'", '\"')
            entities = entities.replace("None", '\"None\"')
            sentiment = json.loads(entities)
            sentiment = sentiment["sentiment"]
            
            if sentiment != "None":
                sentiment = sentiment["basic"]
                data["created_at"].append(twit["created_at"])
                data["sentiment"].append(sentiment)
                
        df = pd.DataFrame(data=data)
        
        df["period"] = pd.to_datetime(
            df["created_at"],
            errors="coerce",
            format="%Y-%m-%dT%H:%M:%SZ"
        ).dt.strftime("%Y%m%d")
        
        df.to_csv(self.target + "/stocktwits.csv")
    
    def _yahoo_news(self):
        print("[INFO] {:.2f}...analyzing yahoo news".format(
            time.time()-start_time
        ))    
        
        news = pd.read_csv(self.folder + "/yahoo news.csv")
        
        data = {
            "datetime"  : [],
            "headline"  : [],
            "source"    : [],
            "summary"   : [],
        }
        
        results = {
            "textblob_polarity" : [],
            "textblob_subjectivity" : [],
            "NEGATIVE_NLTK" : [],
            "NEUTRAL_NLTK"  : [],
            "POSITIVE_NLTK" : [],
            "SENTIMENT_SCORE_NLTK"  : [],
        }
        
        for i, article in news.iterrows():
            summary = article["summary"]
            
            try:
                for field in data:
                    data[field].append(article[field])
                
                self.file_contents = article["summary"]
                self._run_through_nlp_models()
                
                results["textblob_polarity"].append(self.textblob.polarity) 
                results["textblob_subjectivity"].append(self.textblob.subjectivity) 
                results["NEGATIVE_NLTK"].append(self.nltk.sentiment_ratio["NEGATIVE_NLTK"])
                results["NEUTRAL_NLTK"].append(self.nltk.sentiment_ratio["NEUTRAL_NLTK"])
                results["POSITIVE_NLTK"].append(self.nltk.sentiment_ratio["POSITIVE_NLTK"])
                results["SENTIMENT_SCORE_NLTK"].append(self.nltk.sentiment_ratio["SENTIMENT_SCORE_NLTK"])
                
                for sentiment in self.spacy.text_sentiments:
                    if sentiment in results:
                        results[sentiment].append(self.spacy.text_sentiments[sentiment])
                    else:
                        results[sentiment] = [self.spacy.text_sentiments[sentiment]]
            except:
                continue
        
        df_data = pd.DataFrame(data=data)
        df_results = pd.DataFrame(data=results)
        
        df = pd.concat(
            [
                df_data, df_results
            ],
            axis=1
        )
        
        df["period"] = pd.to_datetime(
            df["datetime"],
            errors="coerce",
            unit="s"
        ).dt.strftime("%Y%m%d"
                      )
        df.to_csv(self.target + "/yahoo company news.csv")
        
    def _earnings_calls(self):
        print("[INFO] {:.2f}...analyzing earnings calls".format(
            time.time()-start_time
        ))
        
        final = {
            "period"        : [],
            "textblob_polarity" : [],
            "textblob_subjectivity" : [],
            "NEGATIVE_NLTK" : [],
            "NEUTRAL_NLTK"  : [],
            "POSITIVE_NLTK" : [],
            "SENTIMENT_SCORE_NLTK"  : [],
        }
        
        for filename in os.listdir(self.folder):
            print("[INFO] {:.2f}...analyzing {}".format(
                time.time()-start_time, filename
            ))
            
            transcript = json.load(
                open(os.path.join(self.folder, filename), "r")
            )

            if len(transcript) > 0:
                results = {
                    "textblob_polarity" : [],
                    "textblob_subjectivity" : [],
                    "NEGATIVE_NLTK" : [],
                    "NEUTRAL_NLTK"  : [],
                    "POSITIVE_NLTK" : [],
                    "SENTIMENT_SCORE_NLTK"  : [],
                }
                            
                for speaker in transcript:
                    self.file_contents = speaker[0].replace("\n", "")
                    self._run_through_nlp_models()
                    
                    results["textblob_polarity"].append(self.textblob.polarity) 
                    results["textblob_subjectivity"].append(self.textblob.subjectivity) 
                    results["NEGATIVE_NLTK"].append(self.nltk.sentiment_ratio["NEGATIVE_NLTK"])
                    results["NEUTRAL_NLTK"].append(self.nltk.sentiment_ratio["NEUTRAL_NLTK"])
                    results["POSITIVE_NLTK"].append(self.nltk.sentiment_ratio["POSITIVE_NLTK"])
                    results["SENTIMENT_SCORE_NLTK"].append(self.nltk.sentiment_ratio["SENTIMENT_SCORE_NLTK"])
                    
                    for sentiment in self.spacy.text_sentiments:
                        if sentiment in results:
                            results[sentiment].append(self.spacy.text_sentiments[sentiment])
                        else:
                            results[sentiment] = [self.spacy.text_sentiments[sentiment]]
                            
                df = pd.DataFrame(data=results)
                
                final["textblob_polarity"].append(df["textblob_polarity"].mean())
                final["textblob_subjectivity"].append(df["textblob_subjectivity"].mean())
                final["NEGATIVE_NLTK"].append(df["NEGATIVE_NLTK"].sum())
                final["NEUTRAL_NLTK"].append(df["NEUTRAL_NLTK"].sum())
                final["POSITIVE_NLTK"].append(df["POSITIVE_NLTK"].sum())
                final["SENTIMENT_SCORE_NLTK"].append(df["SENTIMENT_SCORE_NLTK"].sum())
                final["period"].append(filename.split(".")[0])
                
                for sentiment in self.spacy.text_sentiments:
                    if "WGT" not in sentiment:
                        if sentiment in final:
                            final[sentiment].append(df[sentiment].sum())
                        else:
                            final[sentiment] = [df[sentiment].sum()]
                        
        df = pd.DataFrame(data=final)
        
        for sentiment in self.spacy.text_sentiments:
            if "WGT" in sentiment:
                calc_field = sentiment.replace("_WGT", "")
                df[sentiment] = df[calc_field].divide(df["TOTAL_SENTIMENT_WORDS_LM"])
        
        df[["quarter", "year"]] = df["period"].str.split(" ", n=1, expand=True)
        df["quarter"] = df["quarter"].str.replace("Q", "")
        df["period"] = (df["quarter"].astype(int).multiply(3)).astype(str) + df["year"]
        
        df["period"] = pd.to_datetime(
            df["period"],
            errors="coerce",
            format="%m%Y"
        ) + pd.offsets.QuarterEnd(0)
        
        df["period"] = df["period"].dt.strftime("%Y%m%d")
        
        df.to_csv(self.target + "/earnings calls.csv")
        
    def data_analysis(self):
        self.target = f'./results/{self.ticker}'
        
        if not(os.path.exists(self.target)):
            os.makedirs(self.target)
            
        self.folder = f'./downloads/{self.ticker}/finnhub'
        
        if (os.path.exists(self.folder)):
            self._finnhub_company_news()  
            self._earnings_surprises()  
            self._insider_sentiments()
            self._recommendation_trends()
            
        self.folder = f'./downloads/{self.ticker}/finnlp'
        
        if (os.path.exists(self.folder)):
            self._stocktwits()
            self._yahoo_news()
            
        self.folder = f'./downloads/{self.ticker}/seekingalpha/transcripts'
        
        if (os.path.exists(self.folder)):
            self._earnings_calls()