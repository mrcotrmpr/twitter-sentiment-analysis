import json
from main import calc_scores


def evaluate():
    # Analyze test set
    json_path = 'data/sentiment.json'
    with open(json_path) as f:
        test_set = json.load(f)

    pos, neg = calc_scores(test_set)

    # Calc true/ false positives & negatives
    tp, tn, fp, fn = [], [], [], []

    # Positive (sentiment = 1)
    for sentence in pos:
        actual_score = int([item["sentiment"] for item in test_set if item["text"] == sentence["text"]][0])
        if actual_score == 1:
            tp.append(sentence)
        else:
            fp.append(sentence)

    # Negative (sentiment = 0)
    for sentence in neg:
        actual_score = int([item["sentiment"] for item in test_set if item["text"] == sentence["text"]][0])
        if actual_score == 0:
            tn.append(sentence)
        else:
            fn.append(sentence)

    print("Evaluation function:\n")
    print(f"True positives: {len(tp)}")
    print(f"False positives: {len(fp)}")
    print(f"True negatives: {len(tn)}")
    print(f"False negatives: {len(fn)}\n")


def main():
    evaluate()


if __name__ == "__main__":
    main()