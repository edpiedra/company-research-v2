from variables.variables import * 

class NLTKAnalysis():
    def __init__(self):
        print("[INFO] {:.2f}...initializing nltk analysis module".format(
            time.time()-start_time
        ))
        
        self.file_contents = None 
        self.sid = SentimentIntensityAnalyzer()
        
    def get_sentiment_score(self):
        sentences = [
            " ".join(sent.split()).strip() for sent in self.file_contents.split(". ")
        ]
        
        df = pd.DataFrame(sentences, columns=["content"])
        
        def _get_wordnet_pos(pos_tag):
            if pos_tag.startswith("J"):
                return wordnet.ADJ 
            elif pos_tag.startswith('V'):
                return wordnet.VERB
            elif pos_tag.startswith('N'):
                return wordnet.NOUN
            elif pos_tag.startswith('R'):
                return wordnet.ADV
            else:
                return wordnet.NOUN
            
        def _clean_text(
            text, digits=False, stop_words=False, lemmatize=False, only_noun=False
        ):
            text = str(text).lower()
            text = [word.strip(string.punctuation) for word in text.split(" ")]
            
            if digits:
                text = [word for word in text if not any(c.isdigit() for c in word)] 
                
            if stop_words:
                stop = stopwords.words("english")
                text = [x for x in text if x not in stop] 
                
            text = [t for t in text if len(t) > 0]
            
            if lemmatize:
                pos_tags = pos_tag(text) 
                
                text = [
                    WordNetLemmatizer().lemmatize(t[0], _get_wordnet_pos(t[1])) for t in pos_tags
                ]
                
            if only_noun:
                is_noun = lambda pos: pos[:2] == "NN" 
                
                text = [
                    word for (word, pos) in pos_tag(text) if is_noun(pos)
                ]
                
            text = [t for t in text if len(t) > 1]
            text = " ".join(text)
            
            return (text)
        
        df["content_clean"] = df["content"].apply(lambda x: _clean_text(x, digits=True, stop_words=True, lemmatize=True))
        
        df["sentiment"] = df["content_clean"].apply(lambda x: self.sid.polarity_scores(x))
        
        df = pd.concat(
            [
                df.drop(["sentiment"], axis=1), 
                df["sentiment"].apply(pd.Series)
            ],
            axis=1
        )
        
        df.rename(
            columns={
                "neu"   : "NEUTRAL", 
                "neg"   : "NEGATIVE", 
                "pos"   : "POSITIVE"
            },
            inplace=True
        )
        
        df["CONFIDENCE"] = df[
            [
                "NEGATIVE", "NEUTRAL", "POSITIVE"
            ]
        ].max(axis=1)
        
        df["SENTIMENT"] = df[
            [
                "NEGATIVE", "NEUTRAL", "POSITIVE"
            ]
        ].idxmax(axis=1)
        
        sentiment_ratio = df["SENTIMENT"].value_counts(normalize=True).to_dict()
        
        for key in [
            "NEGATIVE", "NEUTRAL", "POSITIVE"
        ]:
            if key not in sentiment_ratio:
                sentiment_ratio[key] = 0.0
                
        sentiment_ratio["SENTIMENT_SCORE"] = (sentiment_ratio["NEUTRAL"] + sentiment_ratio["POSITIVE"]) - sentiment_ratio["NEGATIVE"]
        
        self.sentiment_ratio = {}
        
        for sentiment in sentiment_ratio:
            self.sentiment_ratio[sentiment + "_NLTK"] = sentiment_ratio[sentiment]