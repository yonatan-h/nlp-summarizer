import spacy
from collections import Counter, defaultdict
from heapq import nlargest
from spacy.lang.en.stop_words import STOP_WORDS as stop_words
from string import punctuation

with open("text.txt", "r") as file:
    text = file.read()
# print(text)
nlp = spacy.load("en_core_web_sm")

def sanitize(text):
    sanitized = []
    punctuations = set(list(punctuation+'\n'))

    for letter in text:
        if letter not in punctuations:
            sanitized.append(letter)

    return "".join(sanitized)

def get_tokens(doc, sanitize):
    tokens = []
    for token in doc:
        text = token.text.lower().strip()
        if text in stop_words: continue
        sanitized = sanitize(text)
        if sanitized: tokens.append(sanitized)

    return tokens

#get tokens

#get frequecies
def get_normalized_freq(tokens):
    counts = Counter(tokens)
    freqs = defaultdict(lambda: 0.0)
    max_freq = max(counts.values())

    for token in counts:
        freqs[token] = counts[token]/max_freq

    return freqs


#get sentence scores
def get_sentence_scores(doc, freqs, sanitize):
    sentence_scores = defaultdict(lambda: 0.0)

    for sentence in doc.sents:
        for token in sentence:
            text = sanitize(token.text)
            sentence_scores[sentence.text] += freqs[text]

    return sentence_scores


def get_summary(sentence_scores, n):
    summary = nlargest(n, sentence_scores, key=sentence_scores.get)
    return "".join(summary)


def handle_summary(text):
    print("summarizing:",text)
    doc = nlp(text)
    tokens = get_tokens(doc, sanitize)
    freqs = get_normalized_freq(tokens)
    sentence_scores = get_sentence_scores(doc, freqs, sanitize)
    num_sentences = max(1, len(sentence_scores) // 3)
    summary = get_summary(sentence_scores, num_sentences)
    print("summarized:", summary)
    return summary

# handle_summary(text)


