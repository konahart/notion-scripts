from notion.client import NotionClient

from creds import NOTION_TOKEN


def main(page_url, page_title):
    client = NotionClient(token_v2=NOTION_TOKEN)
    page = client.get_block(page_url)
    if page.title != page_title:
        print(
            f"sanity check: {page.title} does not expected title: {page_title}")
        return
    rows = page.collection.get_rows()
    print(f"found {len(rows)} records")
    for row in rows:
        types = {child.type: child for child in row.children}
        if "tweet" in types and "image" not in types:
            print(f"tweet: {types['tweet'].source}")
