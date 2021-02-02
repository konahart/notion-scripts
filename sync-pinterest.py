import csv
from py3pin.Pinterest import Pinterest

from creds import PINTEREST


def get_board_pins(pinterest, board_id):
    board_feed = []
    feed_batch = pinterest.board_feed(board_id=board_id)
    while len(feed_batch) > 0:
        board_feed += feed_batch
        feed_batch = pinterest.board_feed(board_id=board_id)
    return board_feed


def clean_pins(board):
    pins = []
    num = len(board) - 1
    for pin in board:
        pin = pin_to_row(pin, num)
        if pin:
            pins.append(pin)
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


def main(board_id, board_name):
    pinterest = Pinterest(email=PINTEREST['email'],
                          password=PINTEREST['password'],
                          username=PINTEREST['username'])
    pinterest.login()
    pins = get_board_pins(pinterest, board_id)
    pins = clean_pins(pins)
    print(f"Fetched {len(pins)} pins from board")

    with open(f'{board_name}.csv', 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(pins[0].keys())
        for pin in pins:
            csv_writer.writerow(pin.values())
    print(f"Wrote pins to {board_name}.csv")


if __name__ == "__main__":
    main(PINTEREST["default_board_id"], PINTEREST["default_board_name"])
