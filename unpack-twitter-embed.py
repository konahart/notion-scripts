import tweepy
from notion.client import NotionClient
from notion.block import ImageBlock

from creds import NOTION, TWITTER


def get_tweet_id_from_url(tweet_url):
    return tweet_url.split('/photo')[0].split('/')[-1].split('?')[0]


def get_tweet_image_urls(twitter_client, tweet_url):
    tweet_id = get_tweet_id_from_url(tweet_url)
    print(f"{tweet_url} - {tweet_id}")
    tweet = twitter_client.get_status(tweet_id)
    entities = getattr(tweet, "extended_entities", None) or getattr(
        tweet, "entities", None)
    media = entities.get('media')
    urls = []
    if media:
        for image in media:
            urls.append(image['media_url_https'])
    return urls


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
            image_urls = get_tweet_image_urls(twitter, types['tweet'].source)
            for url in image_urls:
                newchild = row.children.add_new(ImageBlock)
                newchild.set_source_url(url)


if __name__ == "__main__":
    main(NOTION["default_page_url"], NOTION["default_page_title"])
