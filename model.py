"""
Created on Fri Apr 15 17:20:16 2022
@author: seoann
"""
import itertools
from utils import clean_text, LoadDataset, find_label
import torch
from train_ml import Deserialization, evaluate
from transformers import ElectraTokenizerFast
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

class ModelHandler:
    def __init__(self):
        super().__init__()
    
    def initialize(self):
        # De-serializing model and load tokenizer
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        Deserialization()
        print('De-Serialization clear')
        self.tokenizer = ElectraTokenizerFast.from_pretrained("kykim/electra-kor-base")
        token = pd.read_csv('electra_training/src/words/token.txt')
        self.tokenizer.add_tokens(str(token.columns[:]))
        print('tokenizer initialized')

    def preprocess(self, text):
        # cleansing raw text
        input = clean_text(text, self.tokenizer)
        # vectorizing cleaned text
        return input

    def inference(self, data):
        # get predictions from model as probabilities
        output = evaluate(data)
        return output

    def postprocess(self, data):
        # process predictions to predicted label and output format
        message = find_label(data)
        return message

    def handle(self, data):
        # do above processes
        model_input = self.preprocess(data)
        model_output = self.inference(model_input)
        print(self.postprocess(model_output))
        return self.postprocess(model_output)

 
