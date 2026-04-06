# LING-451 Project

Back-translation for Low-Resource North to South Korean NMT: A Dialect-Aware Evaluation

Hannah Chun

## Overview

This project investigates whether incorporating synthetic North-South Korean bililngual data via back-translation(BT) improves the performance of North-to-South Korean(NKtoSK) neural machine translation(NMT).

First, a baseline NKtoSK model is trained by fine-tuning the South Korean pretrained model, [KoBART](https://github.com/seujung/KoBART-translation) using the existing [North-South Korean bilingual dataset](https://github.com/nth221/KoreanUnificationParallelCorpus). The same bilingual dataset is used to train a South-to-North Korean(SKtoNK) model for BT. 

Second, South Korean monolingual data, sourced from classic novels is translated into North Korean using the SKtoNK model, producing synthetic North-South Korean sentence pairs. These synthetic data are then combined with the original parallel corpus to train the final NKtoSK model.

Thrid, the translation performance of the baseline model and the BT model is compared. Character n-gram F-score (chrF) is used to take into account the morphological and inflectional variation in Korean. Additionally, a logistic regression classifier is trained on the North-South Korean bilingual dataset to evaluate whether the model correctly performs dialect-aware translation.

<sub> cf. To ensure domain consistency with the North–South Korean bilingual dataset, sentences for the South Korean monolingual data were selected from classic novels. To avoid copyright issues and reduce time and labor costs, public-domain English novels ([Project Gutenberg](https://www.gutenberg.org/)) were translated into South Korean using the [GPT-4o mini API](https://developers.openai.com/api/docs/models/gpt-4o-mini).</sub>

## File Structure
```sh
.
├── README.md
├── requirements.txt
├── .gitignore
├── data
│   ├── bilingual
│       └── original_bilingual.csv
│       └── original_bilingual_filtered.csv
│       └── train.tsv
│       └── test.tsv
│       └── val.tsv
│   ├── monolingual
└── src
│   └── dataset.py
│   └── get_model_binary.py
│   └── train.py
├── scripts
│   └──bilingual_filter.ipynb
│   └──train_test_val_split.ipynb
│   └──prepare.sh
│   └──run_train.sh
├── output
│   ├── NKtoSK
│       ├── kobart_translation-model_final
│           └── config.json
│           └── pytorch_model.bin
│       ├── kobart_translation-model_chp
│           └── epoch=00-val_loss=2.113.ckpt
│           └── epoch=01-val_loss=1.982.ckpt
│           └── epoch=02-val_loss=1.962.ckpt
│           └── epoch=03-val_loss=2.012.ckpt
│           └── epoch=04-val_loss=2.054.ckpt
│       ├── tb_logs
│           ├── default
│               ├── version_0
│                   └── hparams.yaml
│       ├── logs
│           └── train_974291.err
│           └── train_974291.out
│       └── kobart_translation-last.ckpt
│  ├── SKtoNK
│       ├── kobart_translation-model_final
│           └── config.json
│           └── pytorch_model.bin
│       ├── kobart_translation-model_chp
│           └── epoch=00-val_loss=2.193.ckpt
│           └── epoch=01-val_loss=1.868.ckpt
│           └── epoch=02-val_loss=1.773.ckpt
│           └── epoch=03-val_loss=1.735.ckpt
│           └── epoch=04-val_loss=1.755.ckpt
│       ├── tb_logs
│           ├── default
│               ├── version_0
│                   └── hparams.yaml
│       ├── logs
│           └── train_975812.err
│           └── train_975812.out
│       └── kobart_translation-last.ckpt

```

## Set up the environment

If you run the repo on BlueHive you can directly run `scripts/prepare.sh` to use the installed environment under the path.
To train the translation model, run `scripts/run_train.sh`.

## Obtaining data
* [North-South Korean bilingual dataset](https://github.com/nth221/KoreanUnificationParallelCorpus)
* South Korean monolingual dataset
