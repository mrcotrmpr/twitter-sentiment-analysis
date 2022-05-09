import os
import requests
from nltk.sentiment import SentimentIntensityAnalyzer

bearer_token = os.getenv("BEARER_TOKEN")


def create_url() -> str:
    # Adjustable fields which will be returned such as created_at and language
    tweet_fields = "tweet.fields=created_at,lang"

    # Create a query which can for example check for keywords or/and a specified language
    query = "query=(@RockstarGames)(lang:en)"

    # Set max results between 10 and 100
    max_results = "max_results=100"

    url = "https://api.twitter.com/2/tweets/search/recent?{}&{}&{}".format(tweet_fields, query, max_results)
    return url


def bearer_oauth(request) -> dict:
    request.headers["Authorization"] = f"Bearer {bearer_token}"
    request.headers["User-Agent"] = "v2TweetLookupPython"
    return request


def get_response(url) -> dict:
    response = requests.request("GET", url, auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def do_analysis(response):
    sia = SentimentIntensityAnalyzer()

    pos = [item["text"] for item in response if sia.polarity_scores(item["text"])['pos'] > 0.5]
    neg = [item["text"] for item in response if sia.polarity_scores(item["text"])['neg'] > 0.5]

    return pos, neg


def main():
    url = create_url()
    response = get_response(url)["data"]

    pos, neg = do_analysis(response)

    print(f"Positive tweets: \n{pos}\n")
    print(f"Negative tweets: \n{neg}")


if __name__ == "__main__":
    main()
