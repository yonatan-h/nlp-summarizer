from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, get_linear_schedule_with_warmup
from torch.optim import AdamW
import torch
import gc
import time

tokenizer = AutoTokenizer.from_pretrained('google/mt5-small')
model = AutoModelForSeq2SeqLM.from_pretrained('yonatan-h/amharic-summarizer')

text_len = 512 #ideally 512 
summary_len = 128 #ideally 128
batch_size = 8 # 64, 24,16, 8 depending on gpu usage
epochs = 30 # 10, 5, 1 depending on time
learning_rate = 2e-5 #2e-5, 1e-4 if not converging quickly
warmup_fraction = 0.05 #5%, 10%

def encode(text, length):
    encoded = tokenizer.encode(
        text, return_tensors='pt', padding="max_length", max_length=length, truncation=True
    )
    return encoded[0]

def decode(encoded):
    decoded = tokenizer.decode(encoded)
    return decoded
    

def summarize(text, max_len=summary_len, model=model, text_len=text_len):
    encoded_in = encode(text, text_len)

    encoded_out = model.generate(
        encoded_in.unsqueeze(0),
        
        min_length=1,  # 10, 20, 30, or experiment based on your dataset
        max_length=max_len,  # 100, 150, 200, or adjust depending on summary length
        no_repeat_ngram_size=2,  # 1, 2, 3 (to avoid repeating n-grams)
        num_beams = 10,
        early_stopping=True
        
)
    decoded = decode(encoded_out[0])
    return decoded

def handle_summary(text):
    return summarize(text)