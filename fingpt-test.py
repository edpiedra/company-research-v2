from modules.submodules.analysis_modules._fingpt_analysis import * 

fingpt = FinGPT()

news = pd.read_csv(
    "./downloads/AAPL/finnlp/yahoo news.csv"
)

data = {
    "datetime"  : [],
    "headline"  : [],
    "source"    : [],
    "summary"   : [],
}

results = {
    "fingpt_sentiment"  : [],
}

for i, article in news.iterrows():
    summary = article["summary"]
    
    try:
        for field in data:
            data[field].append(article[field])
        
        file_contents = summary
        
        fingpt.file_contents = file_contents 
        fingpt.get_sentiment()
        
        results["fingpt_sentiment"].append(fingpt.sentiment)
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
).dt.strftime("%Y%m%d")

df.to_csv("./results/AAPL/yahoo company news fingpt.csv")