import os
import json
import requests

bearer_token = os.getenv("BEARER_TOKEN")


def create_url():
    # Adjustable fields which will be returned such as created_at and language
    tweet_fields = "tweet.fields=created_at,lang"

    # Create a query which can for example check for keywords or/and a specified language
    query = "query=(@RockstarGames OR Rockstar Games)(lang:en)"

    # Set max results
    max_results = "max_results=10"

    url = "https://api.twitter.com/2/tweets/search/recent?{}&{}&{}".format(tweet_fields, query, max_results)
    return url


def bearer_oauth(request):
    request.headers["Authorization"] = f"Bearer {bearer_token}"
    request.headers["User-Agent"] = "v2TweetLookupPython"
    return request


def get_response(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    url = create_url()
    json_response = get_response(url)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
