# The train and test dataset of the bilingual corpus could already be obtained from https://github.com/nth221/KoreanUnificationParallelCorpus 
# Therefore, a certain portion of sentence pairs was extracted from the train dataset to create a validation dataset. 
# The final ratio of train : test : val dataset is 8 : 1 : 1.

import pandas as pd
from sklearn.model_selection import train_test_split

# load original bilingual train dataset
df = pd.read_csv('../data/bilingual/kpc-train.tsv', sep='\t')

# get unique NK sentences
unique_nk = df['nk'].unique()

# split NK sentences
nk_train, nk_val = train_test_split(
    unique_nk,
    test_size=0.1,  # ≈ 10% of total gives 8:1:1 overall
    random_state=42
)

#  assign rows based on NK
train_df = df[df['nk'].isin(nk_train)]
val_df   = df[df['nk'].isin(nk_val)]

# save files
train_df.to_csv('../data/bilingual/train.tsv', sep='\t', index=False)
val_df.to_csv('../data/bilingual/val.tsv', sep='\t', index=False)

print(f"Train size: {len(train_df)}") # Train size: 107493
print(f"Val size: {len(val_df)}") # Val size: 11996