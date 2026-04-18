# Progress Notes
The purpose of these notes is to break my bad habit of working on whatever comes up and to keep a record of mistakes I made & how I addressed them.

## 4/6-4/7

### Bilingual Data Filtering Process Modfied + Train/Test/Val dataset changed

Originally, Levenshtein-based filtering was applied to the 130,738 sentence pairs to reduce near-identical and heavily paraphrased pairs. Then the dataset was split into a train:test:val dataset in an 8:1:1 ratio. 

To prevent overlap of North Korean sentences across splits, especially in cases where the same North Korean sentence was aligned with multiple South Korean translations from different publishers of the same novel, I found it more reasonable to utilize the original train–test split (9:1) from prior work. One drawback of the prior work was using the same dataset for the test and validation. 

For this project, I addressed this issue by extracting 10% of the data from the training data for validation data, resulting in the train-test-val having a ratio of 8:1:1. 

Then, Levenshtein-based filtering was applied to the new train, test, and validation datasets. I experimented with multiple edit-distance ratio thresholds, and all three options retained the original 8:1:1 ratio. Qualitative inspection was done on a subset of the remaining sentence pairs for each threshold option. The threshold range of 0.25–0.75 was selected because seemed to effectively remove near-identical sentence pairs, thereby better capturing linguistic differences while still retaining a relatively sufficient amount of sentence pairs.

| Split | Original | 0.15–0.65 | 0.1–0.7 | 0.25–0.75 |
|------|----------|---------------------|-------------------|--------------------------|
| Train | 107,493 | 61,359 | 77,158 | 84,376 |
| Val   | 11,996  | 6,833  | 8,627  | 9,400  |
| Test  | 11,249  | 6,678  | 8,263  | 8,703  |
| Total | 130,738 | 74,870 | 94,048 | 102,479 |

<br>

`./scripts/train_val_split.py` <br>
`./scripts/bilingual_filter.ipynb`

input data : <br>
`./data/bilingual/original/` <br>
output data : <br>
`./data/bilingual/filtered/`

### Trained NK -> SK Baseline model with new dataset

Wrote up a detailed step-by-step process in the link below. <br>
https://hannahchun.tistory.com/133 

`./src/train.py` <br>
`./src/dataset.py` <br>

`./scripts/run_train.sh`

input data : <br>
`./data/bilingual/filtered/train_filtered.tsv` <br>
`./data/bilingual/filtered/val_filtered.tsv` <br>

output model stored: <br>
`./output/NKtoSK/filtered_bilingual/`

### Trained SK -> NK Baseline model with new dataset

To generate synthetic NK-SK sentence pairs using the South Korean monolingual data, a SK -> NK baseline model was needed. Using the same method as the previous step (with only the input_ids and label_ids switched) a SK -> NK translation model was fine-tuned. 

`./src/train.py` <br>
`./src/dataset.py` <br>

`./scripts/run_train.sh`

input data : <br>
`./data/bilingual/filtered/train_filtered.tsv` <br>
`./data/bilingual/filtered/val_filtered.tsv` <br>

output model stored: <br>
`./output/SKtoNK/filtered_bilingual/`

## 4/10-4/13

### Created synthetic North-South Korean sentence pairs using South Korean monolingual data

For back-translation experiments, a total of 395,622 South Korean monolingual sentences from 38 novels were obtained and shuffled to ensure randomness and avoid any ordering bias by book or author.

`./scripts/syntheticData_subsets.ipynb` - shuffle monolingual data

input data : <br>
`./data/monolingual/SK/original/original_monolingual.xlsx` <br>
obtained via `./scripts/GPT_translate_final.py`

output data : <br>
`./data/monolingual/SK/original/original_monolingual_sk_shuffled.tsv`

The monolingual sentences were machine-translated into North Korean using the SK -> NK model, creating synthetic North-South Korean sentence pairs.

`./src/back_translate.py` <br><br>
`./scripts/back_translate.sh`

model used: <br>
`./output/SKtoNK/filtered_bilingual/kobart_translation-model_final` <br>

input data : <br>
`./data/monolingual/SK/original/original_monolingual_sk_shuffled.tsv` <br>

output data : <br>
`./data/synthetic/synthetic_sk_to_nk.tsv`

### Created multiple subsets of the synthetic North-South Korean sentence pairs

The synthetic dataset was subsampled into multiple scaled subsets based on the size of the filtered training set (84,376 sentence pairs) to investigate the effect of synthetic data size on NK -> SK translation performance. Subsets corresponding to different proportions of the training data (e.g., 0.5x, 1×, 1.5x, 2×, 2.5x, 3×, 3.5x, 4x, 4.5x) were constructed using random sampling with a fixed seed to ensure reproducibility.

`./scripts/syntheticData_subsets.ipynb` - create subsets of synthetic data <br>

input data : <br>
`./data/synthetic/synthetic_sk_to_nk.tsv` <br>

output data : <br>
`./data/synthetic/subsets/` <br>

Each corresponding synthetic subset was concatenated with the filtered bilingual training set to create an augmented training set. 

`./scripts/syntheticData_subsets.ipynb` - concatenates each synthetic subset with train_filtered.tsv <br>

input data : <br>
`./data/bilingual/filtered/train_filtered.tsv` <br> `./data/synthetic/subsets/` <br>

output data : <br>
`./data/bilingual/augmented/`

## 4/14-4/16

### Train NK -> SK model on the augmented data (1×, 2×, 3×, 4x)
Trained NK -> SK translation models using augmented training dataset : filtered bilingual training data + synthetic sentence pairs at multiple scales (1×, 2×, 3×, 4×). All models were trained under the same configuration to ensure fair comparison across different data sizes. Validation and test sets were kept fixed across all experiments so that performance differences could be attributed solely to the amount of synthetic training data.

`./src/train.py` <br>
`./src/dataset.py`

`./scripts/run_aug_train.sh`

input data : <br>
`./data/bilingual/augmented/train_augmented_1.0x.tsv` `./data/bilingual/augmented/train_augmented_2.0x.tsv` `./data/bilingual/augmented/train_augmented_3.0x.tsv` `./data/bilingual/augmented/train_augmented_4.0x.tsv`

output model : <br>
`./output/NKtoSK/augmented_bilingual/aug_1.0x` `./output/NKtoSK/augmented_bilingual/aug_2.0x` `./output/NKtoSK/augmented_bilingual/aug_3.0x` `./output/NKtoSK/augmented_bilingual/aug_4.0x`

### Generate translations on the test set for evaluation
For evaluation, the test set was translated using each trained model : the baseline and augmented models (1×, 2×, 3×, 4x).

For each model, North Korean input sentences from the test set were used to generate South Korean translations, and the outputs were saved alongside the reference translations in a structured TSV format (nk, ref_sk, hyp_sk).

`./src/translate_test.py` <br><br>
`./scripts/translate_test_aug.sh`
`./scripts/translate_test_baseline.sh`

input data : <br>
`./data/bilingual/filtered/test_filtered.tsv`

model used: <br>
`./output/NKtoSK/augmented_bilingual/aug_1.0x` `./output/NKtoSK/augmented_bilingual/aug_2.0x` `./output/NKtoSK/augmented_bilingual/aug_3.0x` `./output/NKtoSK/augmented_bilingual/aug_4.0x`

output data : <br> 
`./data/translation_results/`