import pandas as pd
from sacrebleu.metrics import CHRF

def compute_chrf(file_path):
    # load data
    df = pd.read_csv(file_path, sep="\t")

    # extract lists
    references = df["ref_sk"].tolist()
    hypotheses = df["hyp_sk"].tolist()

    # Initialize chrF (character-level, recall-weighted)
    chrf = CHRF(word_order=0, beta=3)

    # compute score
    score = chrf.corpus_score(hypotheses, [references])

    return score.score

if __name__ == "__main__":
    file_path = "../data/translation_results/aug_4.0x_nk_to_sk_test.tsv"
    
    score = compute_chrf(file_path)
    
    print(f"chrF3: {score:.2f}")