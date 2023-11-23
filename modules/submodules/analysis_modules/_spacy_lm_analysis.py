from variables.variables import * 

class SpacyLMAnalysis():
    def __init__(self):
        print("[INFO] {:.2f}...initializing spacy LM analysis module".format(
            time.time()-start_time
        ))
        
        self.nlp = spacy.load("en_core_web_lg")
        
        self.sentiments     = [
            "negative", "positive", "uncertainty", "litigious", "constraining"
        ]
        
        df = pd.read_csv('./data/Loughran-McDonald_MasterDictionary_1993-2021.csv')
        df.columns = [column.lower() for column in df.columns]
        df = df[self.sentiments + ['word']]
        df[self.sentiments] = df[self.sentiments].astype(bool)
        df = df[(df[self.sentiments]).any(axis=1)]
        word_list = self.nlp(" ".join(df['word'].str.lower()))
        
        word_lemmas = [] 
        for word in word_list:
            word_lemmas.append(word.lemma_)
            
        df.insert(loc=6, column='lemma', value=word_lemmas)
        df = df.drop_duplicates('lemma')
        
        self.sentiment_df   = df.copy()
        
        self.tfidf_vectorizer   = TfidfVectorizer(
            smooth_idf=True, use_idf=True, min_df=0.025
        )
        
        self.sentiment_vectorizer   = CountVectorizer()
        self.file_contents = None 
        
    def get_sentiments(self):
        '''
        the LoughranMcDonald Master Dictionary provides a sentiments category for 80,000 words.
        '''
        doc     = self.nlp(self.file_contents) 
        
        with doc.retokenize() as retokenizer:
            for ent in doc.ents:
                retokenizer.merge(doc[ent.start:ent.end], attrs={"LEMMA": ent.text})
        
        words   = [] 
                
        for word in doc:
            if word.is_alpha and word.is_ascii and not word.is_stop and \
                word.ent_type_ not in [
                    "PERSON", "DATE", "TIME", "ORDINAL", "CARDINAL"
                ]:
                    words.append(word.lemma_.lower()) 
                    
        self.text_sentiments    = {}
        total_words             = 0 
        
        for sentiment in self.sentiments:
            sentiment_words     = self.sentiment_df.loc[self.sentiment_df[sentiment], "lemma"] 
            self.sentiment_vectorizer.fit(sentiment_words) 
            vector  = self.sentiment_vectorizer.transform([" ".join(words)]) 
            
            word_count = np.sum(vector.toarray())
            total_words += word_count 
            self.text_sentiments[sentiment]     = word_count
            
        self.text_sentiments["TOTAL_SENTIMENT_WORDS"] = total_words 
        
        for sentiment in self.sentiments:
            if total_words > 0:
                self.text_sentiments[sentiment + "_WGT"] = self.text_sentiments[sentiment] / total_words  
            else:
                self.text_sentiments[sentiment + "_WGT"] = "" 
            
        for sentiment in self.text_sentiments:
            self.text_sentiments[sentiment + "_LM"] = self.text_sentiments.pop(sentiment) 