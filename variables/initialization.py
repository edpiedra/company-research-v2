import time 
start_time = time.time()

print("[INFO] {:.2f}...loading libraries".format(
    time.time()-start_time
))

import pandas as pd 
import numpy as np
import json, os 
import datetime as dt 
from dateutil.relativedelta import relativedelta 

#NLTK LIBRARIES
import string 
from nltk.sentiment.vader import SentimentIntensityAnalyzer 
from nltk.corpus import wordnet, stopwords 
from nltk import pos_tag 
from nltk.stem import WordNetLemmatizer

#SPACY LM LIBRARIES
import spacy 
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

#TEXTBLOB LIBRARIES
import textblob

#FINNHUB LIBRARIES
import finnhub

#FINNLP LIBRARIES
from finnlp.data_sources.social_media.stocktwits_streaming import Stocktwits_Streaming
from finnlp.data_sources.news.cnbc_streaming import CNBC_Streaming
from finnlp.data_sources.news.marketwatch_date_range import MarketWatch_Date_Range
from finnlp.data_sources.news.seekingalpha_date_range import SeekingAlpha_Date_Range
from finnlp.data_sources.news.yahoo_streaming import Yahoo_Date_Range

#YAHOO FINANCE LIBRARIES
import yfinance as yf 

#SEEKINGALPHA LIBRARIES
from selenium import webdriver
import re 
from bs4 import BeautifulSoup 
from furl import furl
from urllib.parse import urljoin 

#GUI LIBRARIES
import dash, webbrowser 
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

#FINGPT LIBRARIES

os.environ["TRANSFORMERS_CACHE"] = "u:/huggingface/cache/"

from transformers import AutoModel, AutoTokenizer 
from peft import PeftModel 
import torch 