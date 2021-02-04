import csv
from notion.client import NotionClient
from py3pin.Pinterest import Pinterest

from creds import NOTION, PINTEREST


def get_board_pins(pinterest, board_id):
    board_feed = []
    feed_batch = pinterest.board_feed(board_id=board_id)
    while len(feed_batch) > 0:
        board_feed += feed_batch
        feed_batch = pinterest.board_feed(board_id=board_id)
    return board_feed


def clean_pins(board):
    """
        id : {pin}
    """
    pins = {}
    num = len(board) - 1
    for pin in board:
        pin = pin_to_row(pin, num)
        if pin:
            pins[pin['id']] = pin
        num -= 1
    return pins


def pin_to_row(row, num):
    pin = {}
    pin['title'] = row.get('grid_title')
    pin['url'] = row.get('link')
    pin['id'] = row.get('id')
    if pin['id']:
        pin['pin_url'] = f"https://www.pinterest.com/pin/{pin['id']}/"
    pin['description'] = row.get('description')
    images = row.get('images')
    if images:
        img = images.get('orig')
        if img:
            pin['img_url'] = img.get('url')
    pin['created_at'] = num
    if pin.get('title') or pin.get('url') or pin.get('description') or \
            pin.get('img_url'):
        return pin
    return None


def export_csv(board_name, pins):
    with open(f'{board_name}.csv', 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(pins[0].keys())
        for pin in pins:
            csv_writer.writerow(pin.values())
    print(f"Wrote pins to {board_name}.csv")


def main(board_id, board_name, page_url, page_title):
    # set up clients for notion and twitter
    notion = NotionClient(token_v2=NOTION['token'])
    pinterest = Pinterest(email=PINTEREST['email'],
                          password=PINTEREST['password'],
                          username=PINTEREST['username'])
    pinterest.login()

    # get pins from board
    pins = get_board_pins(pinterest, board_id)
    pins = clean_pins(pins)
    print(f"Fetched {len(pins)} pins from board")

    # get notion pin collection
    page = notion.get_collection_view(page_url)
    if page.parent.title != page_title:
        print(f"sanity check: {page.parent.title} does not expected title: "
              f"{page_title}")
        return
    rows = page.collection.get_rows()
    print(f"found {len(rows)} records")
    pins_in_notion = {row.get_property('id') for row in rows}

    # for any pin not already in notion collection, create a new row
    for pin_id, pin in pins.items():
        if pin_id not in pins_in_notion:
            print(f"{pin_id} {pin['pin_url']}")
            row = page.collection.add_row()
            for key, value in pin.items():
                row.set_property(key, value)


if __name__ == "__main__":
    main(PINTEREST["default_board_id"], PINTEREST["default_board_name"],
         NOTION["default_page_url"], NOTION["default_page_title"])
