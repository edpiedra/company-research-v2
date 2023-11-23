from variables.variables import * 

class TextblobAnalysis():
    def __init__(self):
        print("[INFO] {:.2f}...initializing textblob analysis module".format(
            time.time()-start_time
        ))
        
        self.file_contents = None 
        
    def get_properties(self):
        self.blob = textblob.TextBlob(self.file_contents) 
        
        self._get_polarity()
        self._get_subjectivity()
        
    def _get_polarity(self):
        self.polarity = self.blob.polarity 
        
    def _get_subjectivity(self):
        self.subjectivity = self.blob.subjectivity 