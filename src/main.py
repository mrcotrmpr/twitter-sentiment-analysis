import os
import json
import requests

bearer_token = os.getenv("BEARER_TOKEN")


def create_url():
    # Adjustable fields which will be retrieved such as created_at and language
    tweet_fields = "tweet.fields=created_at,lang"

    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated ID's
    ids = "ids=1278747501642657792,1255542774432063488"

    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
    return url


def bearer_oauth(request):
    request.headers["Authorization"] = f"Bearer {bearer_token}"
    request.headers["User-Agent"] = "v2TweetLookupPython"
    return request


def connect_to_endpoint(url):
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
    json_response = connect_to_endpoint(url)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()