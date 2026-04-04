import os
import glob
import torch
import ast
import numpy as np
import pandas as pd
from tqdm import tqdm, trange
from torch.utils.data import Dataset, DataLoader, IterableDataset

class KoBARTSummaryDataset(Dataset):
    def __init__(self, file, tok, max_len, pad_index = 0, ignore_index=-100):
        super().__init__()
        self.tok = tok
        self.max_len = max_len
        self.docs = pd.read_csv(file, sep='\t') # load data
        self.len = self.docs.shape[0]
        self.pad_index = pad_index
        self.ignore_index = ignore_index

    # making all sequences same length (padding) for the NN
    def add_padding_data(self, inputs):
        if len(inputs) < self.max_len:
            pad = np.array([self.pad_index] *(self.max_len - len(inputs)))
            inputs = np.concatenate([inputs, pad])
        else:
            inputs = inputs[:self.max_len]

        return inputs
    
    # for positions expected to have paddings in label_ids, use -100 so that they are ignored when computing loss
    def add_ignored_data(self, inputs):
        if len(inputs) < self.max_len:
            pad = np.array([self.ignore_index] *(self.max_len - len(inputs)))
            inputs = np.concatenate([inputs, pad])
        else:
            inputs = inputs[:self.max_len]

        return inputs
    
    def __getitem__(self, idx):
        instance = self.docs.iloc[idx] # instance: the sentence pair at the idx-th row
        
        # encoder input (source sentence)
        # e.g., 나는 래일이 좋다
        input_ids = self.tok.encode(instance['nk']) # convert NK sentence into token IDs
        input_ids = self.add_padding_data(input_ids) # add padding to match maximum length (e.g, 8)
        # e.g., [T1, T2, T4, 0, 0, 0, 0, 0]
        
        # labels (target sentence)
        # e.g., 나는 내일이 좋다
        label_ids = self.tok.encode(instance['sk']) # convert SK sentence into token IDs
        label_ids.append(self.tok.eos_token_id) # append EOS token to token IDs
        # e.g., [T1, T3, T4, <EOS>]

        # decoder input (shifted target sentence)
        # teaches the model what has been generated so far, so it can learn to predict the next token
        dec_input_ids = [self.pad_index] # start off with padding index
        dec_input_ids += label_ids[:-1] # padding index + label_ids without the last token
        # e.g., [0, T1, T3, T4]
        dec_input_ids = self.add_padding_data(dec_input_ids) # add padding to match maximum length (e.g, 8)
        # e.g., [0, T1, T3, T4, 0, 0, 0, 0]
        
        label_ids = self.add_ignored_data(label_ids) # pad labels to match maximum length (e.g, 8)
        # e.g., [T1, T3, T4, <EOS>, -100, -100, -100, -100]
        
        return {
            'input_ids': torch.tensor(input_ids, dtype=torch.long),
            'decoder_input_ids': torch.tensor(dec_input_ids, dtype=torch.long),
            'labels': torch.tensor(label_ids, dtype=torch.long)
        }
    def __len__(self):
        return self.len