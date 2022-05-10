import json
import re
import string
from twitter_connector import get_tweets


def de_emojify(sentence):
    # Remove emojis from the input string using regex
    regrex_pattern = re.compile(pattern="["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'', sentence)


def tokenize(sentence) -> list:
    # Tokenize the input string
    return de_emojify(sentence) \
        .lower() \
        .strip() \
        .replace("\n", " ") \
        .translate(str.maketrans(" ", " ", string.punctuation)) \
        .split(" ")


def calc_scores(response):
    pos, neg = [], []

    # The afinn wordlist contains words with a score from -5 to 5 based on sentiment
    json_path = 'data/afinn.json'
    with open(json_path) as f:
        afinn = json.load(f)

    for item in response:
        tokenized = tokenize(item["text"])

        for token in tokenized:
            dict = {"text": "", "words":[], "score": 0}
            # If there is a match in the afinn wordlist
            if token in afinn:
                # Negative hit
                if afinn[token] < 0:
                    if len(list(filter(lambda res: res['text'] == item["text"], neg))) > 0:
                        dict["words"].append(token)
                        dict["score"] += afinn[token]
                    else:
                        dict["text"] = item["text"]
                        dict["words"] = [token]
                        dict["score"] = afinn[token]
                # Positive hit
                elif afinn[token] > 0:
                    if len(list(filter(lambda res: res['text'] == item["text"], pos))) > 0:
                        dict["words"].append(token)
                        dict["score"] += afinn[token]
                    else:
                        dict["text"] = item["text"]
                        dict["words"] = [token]
                        dict["score"] = afinn[token]

            if dict["score"] > 0:
                pos.append(dict)
            elif dict["score"] < 0:
                neg.append(dict)

    return pos, neg


def do_analysis(scores):
    pos, neg = calc_scores(scores)

    print(f"\nPositive scores:\n{pos}\n")
    print(f"\nNegative scores:\n{neg}")


def main():
    tweets = get_tweets()
    do_analysis(tweets)


if __name__ == "__main__":
    main()
