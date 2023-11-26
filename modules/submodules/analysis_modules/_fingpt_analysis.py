from variables.variables import *

class FinGPT():
    def __init__(self):
        print("[INFO] {:.2f}...initializing fingpt module".format(
            time.time()-start_time
        ))
        
        base_model = "THUDM/chatglm2-6b"
        peft_model = "oliverwang15/FinGPT_ChatGLM2_Sentiment_instruction_LoRA_FT"
        
        self.tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
        model = AutoModel.from_pretrained(base_model, trust_remote_code=True, device_map="cpu", torch_dtype=torch.float32)
        model = PeftModel.from_pretrained(model, peft_model)
        self.model = model.eval()
        
        self.file_contents = None 
        
    def get_sentiment(self):
        prompt = [
            '''
            Instruction: What is the sentiment of this news? Please choose an answer from negative/neutral/positive.
            Input: {}
            Answer: 
            '''.format(self.file_contents)
        ]
        
        tokens = self.tokenizer(
            prompt, return_tensors='pt', padding=True
        )
        
        res = self.model.generate(**tokens, max_length=512)
        res_sentences = [self.tokenizer.decode(i) for i in res]
        out_text = [o.split("Answer: ")[1] for o in res_sentences]
        
        self.sentiment = out_text[0]