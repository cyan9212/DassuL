""" written by seoann 04/29/2022 """

from src.utils import tokenizer
from model import get_pretrained_model
from training import train_model
from src.utils import split_data, LoadDataset
from src.tokenizer import get_tokenizer
from evaluation import evaluate
from torch import nn
import pandas as pd
import torch
import torch.nn as nn
import warnings
warnings.filterwarnings(action='ignore')


class run():
    def main():
        tk = get_tokenizer()
        epochs = 300
        batch_size = 64
        PATH = './data/unsmile_data/'
        PATH2 = './data/kakao/'
        
        for category in ['개인지칭','기타혐오','성별','성소수자','악플욕설','연령','인종국적','종교','지역','clean',]:

            electra = get_pretrained_model()
            electra.set_device()

            data = pd.read_csv(PATH + f'{category}.csv')
            data2 = pd.read_csv(PATH2 + f'{category}.csv')

            data = data[['문장', f'{category}']]
            data2 = data2[['text', f'{category}']]
            
            data2.rename(columns = {'text':'문장'},inplace=True)
            data = pd.concat([data,data2], ignore_index=True)

            X_train, X_test = split_data.dataSplit(data, category)
            X_train, X_validation = split_data.dataSplit(X_train, category)

            
            train_set = LoadDataset(X_train, tk.tokenizer, electra.device)
            validation_set = LoadDataset(X_validation, tk.tokenizer, electra.device)
            test_set = LoadDataset(X_test, tk.tokenizer, electra.device)

            train =  train_model(electra.model, epochs, batch_size, train_set, validation_set, category, electra.device)
            eval = evaluate(electra.model, batch_size, test_set, category, electra.device)
            torch.save(electra.model.state_dict(), f'./models/{category}.pth')
    
    
    if __name__ == "__main__":
        main() 
