import torch
import pandas as pd
from tqdm import tqdm
import argparse
from kobart import get_kobart_tokenizer
from transformers.models.bart import BartForConditionalGeneration

# argument parsing
parser = argparse.ArgumentParser()

parser.add_argument("--input_file", type=str, required=True)
parser.add_argument("--output_file", type=str, required=True)
parser.add_argument("--model_path", type=str, required=True)

parser.add_argument("--batch_size", type=int, default=16)
parser.add_argument("--max_length", type=int, default=128)
parser.add_argument("--num_beams", type=int, default=5)

args = parser.parse_args()

# load SK -> NK model
print("Loading model from:", args.model_path)

model = BartForConditionalGeneration.from_pretrained(args.model_path)
tokenizer = get_kobart_tokenizer()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

model.to(device)
model.eval()

# load data
print("Loading data from:", args.input_file)

df = pd.read_csv(args.input_file, sep="\t")

# drop invalid rows just in case
df = df.dropna(subset=["sk"])
df["sk"] = df["sk"].astype(str).str.strip()

print("Total sentences:", len(df))

# translate in batches
batch_size = args.batch_size
results = []

for i in tqdm(range(0, len(df), batch_size)):
    # extract batch
    batch = df["sk"].iloc[i:i+batch_size].tolist()
    
    # tokenize
    inputs = tokenizer(
        batch, 
        return_tensors="pt", 
        padding=True, 
        truncation=True, 
        max_length=args.max_length
    )
    input_ids = inputs["input_ids"].to(device)
    
    # generate
    with torch.no_grad(): # no gradients needed : faster + less memory
        outputs = model.generate(
            input_ids,
            max_length=args.max_length, # prevents infinite generation
            num_beams=args.num_beams, # keeps top 5 candidates and chooses best sequence overall
            eos_token_id=1 # stop when EOS token appears
        )
    
    # decode output
    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    results.extend(decoded)

# sanity check
print("Input size:", len(df))
print("Output size:", len(results))

assert len(df) == len(results), "Mismatch between input and output!"

# save as parallel corpus (nk, sk)
output_df = pd.DataFrame({
    "nk": results,
    "sk": df["sk"].tolist()
})

output_df.to_csv(args.output_file, sep="\t", index=False)

print("Saved to:", args.output_file)