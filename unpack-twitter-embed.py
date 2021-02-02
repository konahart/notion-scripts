import tweepy
from notion.client import NotionClient

from creds import NOTION, TWITTER


def main(page_url, page_title):
    # set up clients for notion and twitter
    notion = NotionClient(token_v2=NOTION['token'])
    twitter_auth = tweepy.OAuthHandler(
        TWITTER['consumer_key'], TWITTER['consumer_secret'])
    twitter_auth.set_access_token(
        TWITTER['access_key'], TWITTER['access_secret'])
    twitter = tweepy.API(twitter_auth)

    page = notion.get_block(page_url)
    if page.title != page_title:
        print(f"sanity check: {page.title} does not expected title: "
              "{page_title}")
        return
    rows = page.collection.get_rows()
    print(f"found {len(rows)} records")
    for row in rows:
        types = {child.type: child for child in row.children}
        if "tweet" in types and "image" not in types:
            print(f"tweet: {types['tweet'].source}")


if __name__ == "__main__":
    main(NOTION["default_page_url"], NOTION["default_page_title"])
