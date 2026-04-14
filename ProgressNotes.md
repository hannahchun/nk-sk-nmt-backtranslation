# Progress Notes
The purpose of these notes is to break my bad habit of working on whatever comes up and to keep a record of mistakes I made & how I addressed them.

## 4/6-4/7

### Bilingual Data Filtering Process Modfied + Train/Test/Val dataset changed

Originally, Levenshtein-based filtering was applied to the 130,738 sentence pairs to reduce near-identical and heavily paraphrased pairs. Then the dataset was split into a train:test:val dataset in an 8:1:1 ratio. 

To prevent overlap of North Korean sentences across splits, especially in cases where the same North Korean sentence was aligned with multiple South Korean translations from different publishers of the same novel, I found it more reasonable to utilize the original train–test split (9:1) from prior work. One drawback of the prior work was the use of the same dataset for the test and validation. This project addressed this issue by means of extracting 10% of the data from the training data for validation data, resulting in the train-test-val having a ratio of 8:1:1. 
Then, Levenshtein-based filtering was applied to the new train, test, and validation datasets. Experimented with multiple edit-distance ratio thresholds, and all three options retained the original 8:1:1 ratio. Qualitative inspection of representative examples was done for each threshold option. Threshold 0.25~0.75 was chosen because it seemed to remove needless identical sentence pairs the most, likely to reflect linguistic differences between the two languages, while also retaining the most total sentence pairs. 

| Split | Original | 0.15–0.65 | 0.1–0.7 | 0.25–0.75 |
|------|----------|---------------------|-------------------|--------------------------|
| Train | 107,493 | 61,359 | 77,158 | 84,376 |
| Val   | 11,996  | 6,833  | 8,627  | 9,400  |
| Test  | 11,249  | 6,678  | 8,263  | 8,703  |
| Total | 130,738 | 74,870 | 94,048 | 102,479 |

### Trained NK -> SK Baseline model with new dataset

Wrote up a detailed step-by-step process in the link below. <br>
https://hannahchun.tistory.com/133 

### Trained SK -> NK Baseline model with new dataset

To generate synthetic NK-SK sentence pairs using the South Korean monolingual data, a SK -> NK baseline model was needed. Using the same method as the previous step (with only the input_ids and label_ids switched) a South Korean -> North Korean translation model was fine-tuned. 

## 4/10-4/13

### Creating synthetic North-South Korean sentence pairs using South Korean monolingual data

For back-translation experiments, a total of 395,622 South Korean monolingual sentences from 38 novels were obtained and shuffled to ensure randomness and avoid any ordering bias by book or author.

The monolingual sentences were machine-translated into North Korean using the SK -> NK model, creating synthetic North-South Korean sentence pairs.

### Creating multiple subsets of the synthetic North-South Korean sentence pairs

The synthetic dataset was subsampled into multiple scaled subsets based on the size of the filtered training set (84,376 sentence pairs) to investigate the effect of synthetic data size on NK -> SK translation performance. Subsets corresponding to different proportions of the training data (e.g., 0.5x, 1×, 1.5x, 2×, 2.5x, 3×, 3.5x, 4x, 4.5x) were constructed using random sampling with a fixed seed to ensure reproducibility.

Each corresponding synthetic subset was concatenated with the filtered bilingual training set to create an augmented training set. The validation and test sets were kept fixed across all experiments so that performance differences could be attributed solely to the amount of synthetic training data.