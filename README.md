# LING-451 Project

Back-translation for Low-Resource North to South Korean NMT: A Dialect-Aware Evaluation

Hannah Chun

## Overview

This project investigates whether incorporating synthetic North-South Korean bililngual data via back-translation(BT) improves the performance of North-to-South Korean(NKtoSK) neural machine translation(NMT).

First, a baseline NKtoSK model is trained by fine-tuning the South Korean pretrained model, [KoBART](https://github.com/seujung/KoBART-translation) using the existing [North-South Korean bilingual dataset](https://github.com/nth221/KoreanUnificationParallelCorpus). The same bilingual dataset is used to train a South-to-North Korean(SKtoNK) model for BT. 

Second, South Korean monolingual data, sourced from classic novels is translated into North Korean using the SKtoNK model, producing synthetic North-South Korean sentence pairs. These synthetic data are then combined with the original parallel corpus to train the final NKtoSK model.

Thrid, the translation performance of the baseline model and the BT model is compared. Character n-gram F-score (chrF) is used to take into account the morphological and inflectional variation in Korean. 

In addition to chrF3, BERTScore is used as a complementary evaluation metric to assess semantic similarity between the generated translations and the references. The purpose of this comparison is to figure out the extent to which semantically adequate translations exhibit low surface overlap, as well as cases where high semantic similarity does not necessarily reflect accurate dialectal transformation.

Additionally, a logistic regression classifier is trained on the North-South Korean bilingual test dataset to assess whether the generated translations from each model show linguistic characteristics specific to South Korean (SK) Korean.

A qualitative analysis was conducted on the translations from each model to examine which lexical and morphosyntactic differences between North and South Korean were successfully captured.

<sub> cf. To ensure domain consistency with the North–South Korean bilingual dataset, sentences for the South Korean monolingual data were selected from classic novels. To avoid copyright issues and reduce time and labor costs, public-domain English novels ([Project Gutenberg](https://www.gutenberg.org/)) were translated into South Korean using the [GPT-4o mini API](https://developers.openai.com/api/docs/models/gpt-4o-mini).</sub>

## File Structure
```sh
.
├── README.md
├── ProgressNotes.md
├── requirements.txt
├── .gitignore
├── data
│   ├── bilingual
│       ├── original
│           └── original_bilingual.tsv
│           └── train.tsv
│           └── test.tsv
│           └── val.tsv
│       ├── filtered
│           └── train_filtered.tsv
│           └── train_filtered_ratio.tsv
│           └── test_filtered.tsv
│           └── test_filtered_ratio.tsv
│           └── val_filtered.tsv
│           └── val_filtered_ratio.tsv
│       ├── augmented
│           └── train_augmented_0.5x.tsv
│           └── train_augmented_1.0x.tsv
│           └── train_augmented_1.5x.tsv
│           └── train_augmented_2.0x.tsv
│           └── train_augmented_2.5x.tsv
│           └── train_augmented_3.0x.tsv
│           └── train_augmented_3.5x.tsv
│           └── train_augmented_4.0x.tsv
│           └── train_augmented_4.5x.tsv
│   ├── monolingual
│       ├── SK
│           ├── original
│               └── original_monolingual_sk_shuffled.tsv
│               └── original_monolingual.xlsx
│   ├── synthetic
│       └── synthetic_sk_to_nk.tsv
│       ├── subsets
│           └── synthetic_sk_to_nk_subset_0.5x.tsv
│           └── synthetic_sk_to_nk_subset_1.0x.tsv
│           └── synthetic_sk_to_nk_subset_1.5x.tsv
│           └── synthetic_sk_to_nk_subset_2.0x.tsv
│           └── synthetic_sk_to_nk_subset_2.5x.tsv
│           └── synthetic_sk_to_nk_subset_3.0x.tsv
│           └── synthetic_sk_to_nk_subset_3.5x.tsv
│           └── synthetic_sk_to_nk_subset_4.0x.tsv
│           └── synthetic_sk_to_nk_subset_4.5x.tsv
│   ├── translation_results
│       └── aug_1.0x_nk_to_sk_test.tsv
│       └── aug_2.0x_nk_to_sk_test.tsv
│       └── aug_3.0x_nk_to_sk_test.tsv
│       └── aug_4.0x_nk_to_sk_test.tsv
│       └── baseline_nk_to_sk_test.tsv
│   ├── classifier_results
│       └── classifier_summary.csv
│       └── 1.0x_classifier_scores.tsv
│       └── 2.0x_classifier_scores.tsv
│       └── 3.0x_classifier_scores.tsv
│       └── 4.0x_classifier_scores.tsv
│       └── baseline_classifier_scores.tsv
│       └── baseline_high_confidence.tsv
│       └── baseline_low_confidence.tsv
│   ├── qualitative_analysis
│       └── aug_1.0x_nk_to_sk_selected_test.tsv
│       └── aug_2.0x_nk_to_sk_selected_test.tsv
│       └── aug_3.0x_nk_to_sk_selected_test.tsv
│       └── aug_4.0x_nk_to_sk_selected_test.tsv
│       └── baseline_nk_to_sk_selected_test.tsv
│       └── selected_test.tsv
└── src
│   └── dataset.py
│   └── get_model_binary.py
│   └── train.py
│   └── back_translate.py
│   └── translate_test.py
│   └── CHRF.py
│   └── logistic_classifier.ipynb
├── scripts
│   └──bilingual_filter.ipynb
│   └──train_val_split.py
│   └──prepare.sh
│   └──run_train.sh
│   └──GPT_translate_final.py
│   └──syntheticData_subsets.ipynb
│   └──back_translate.sh
│   └──run_aug_train.sh
│   └──translate_test_baseline.sh
│   └──translate_test_aug.sh
│   └──bertscore.sh
│   └──translate_selected_test_baseline.sh
│   └──translate_selected_test_aug.sh
├── output
│   ├── NKtoSK
│       ├── augmented_bilingual
│           ├── aug_1.0x
│               ├── kobart_translation-model_final
│                   └── config.json
│                   └── pytorch_model.bin
│           ├── aug_2.0x
│               ├── kobart_translation-model_final
│                   └── config.json
│                   └── pytorch_model.bin
│           ├── aug_3.0x
│               ├── kobart_translation-model_final
│                   └── config.json
│                   └── pytorch_model.bin
│           ├── aug_4.0x
│               ├── kobart_translation-model_final
│                   └── config.json
│                   └── pytorch_model.bin
│       ├── filtered_bilingual
│           ├── kobart_translation-model_final
│               └── config.json
│               └── pytorch_model.bin
│   ├── SKtoNK
│       ├── filtered_bilingual
│           ├── kobart_translation-model_final
│               └── config.json
│               └── pytorch_model.bin


Note: output directory also includes additional training artifacts such as checkpoint files (e.g., .ckpt) and configuration files (e.g., .yaml), which are omitted for brevity.
```

## Set up the environment

If you run the repo on BlueHive you can directly run `scripts/prepare.sh` to use the installed environment under the path.
To train the translation model, run `scripts/run_train.sh`.

## Obtaining bilingual data
* [North-South Korean bilingual dataset](https://github.com/nth221/KoreanUnificationParallelCorpus)
