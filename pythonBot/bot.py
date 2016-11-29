import sys

settings = {}
match = {}
players = {'me': {}, 'opponent': {}}

# TODO: Put things in Bot class if we want to do OOD


class Card(object):
    # Ace is considered 14 typically
    # if it is the start of a straight it will count as 1
    def __init__(self, suit, card_str):
        self.suit = suit
        self.number = 'xx23456789TJQKA'.find(card_str)


def main():
    while not sys.stdin.closed:
        try:
            line = sys.stdin.readline()
            if len(line) == 0:
                break

            line = line.strip().split()
            if len(line) == 0:
                continue
            command = line[0].lower()

            if command == 'settings':
                update_settings(line[1:])
                pass
            elif command == 'match':
                update_match(line[1:])
                pass
            elif 'player' in command:
                update_player(line[0], line[1], line[2])
                pass
            elif command == 'action':
                if 'table' not in match:
                    sys.stdout.write(handle_preflop(line[2]) + "\n")
                    sys.stdout.flush()
                    pass
                elif len(match['table']) == 3:
                    sys.stdout.write(handle_flop(line[2]) + "\n")
                    sys.stdout.flush()
                    pass
                elif len(match['table']) == 4:
                    sys.stdout.write(handle_turn(line[2]) + "\n")
                    sys.stdout.flush()
                    pass
                elif len(match['table']) == 5:
                    sys.stdout.write(handle_river(line[2]) + "\n")
                    sys.stdout.flush()
                    pass
            else:
                sys.stderr.write("Unknown command: " + command + "\n")
                sys.stderr.flush()
        except EOFError:
            return


def update_settings(update):
    key, val = update
    if key == 'starting_stack':
        players['me']['stack'] = players['opponent']['stack'] = int(val)
    else:
        settings[key] = val


def update_match(update):
    key, val = update
    if key == 'table':
        match[key] = parse_cards(val)
    else:
        match[key] = val


def update_player(name, key, val):
    player = players['me'] if name == settings['your_bot'] else players['opponent']

    if key == 'stack':
        player['stack'] = int(val)
    elif key == 'post':
        player['stack'] -= int(val)
    elif key == 'hand':
        player['pocket'] = parse_cards(val)
    elif key == 'wins':
        if 'table' in match:
            del match['table']
    else:
        sys.stderr.write('Unknown command: %s\n' % (key))


def handle_preflop(timeout):
    return 'check 0'


def handle_flop(timeout):
    return 'check 0'


def handle_turn(timeout):
    return 'check 0'


def handle_river(timeout):
    return 'check 0'


def parse_cards(cards_str):
    cards = cards_str[1:-1].split(',')
    return [Card(card[1], card[0]) for card in cards]


def hand_rank(cards):
        hand = sorted([card.number for card in cards])

        is_straight = all([hand[i] + 1 == hand[i+1] for i in range(4)])
        if not is_straight and hand[0] == 14:  # could be A 2 3 4 5
            is_straight = all(hand[i] + 1 == hand[i + 1] for i in range(1, 4))

        is_flush = all([card.suit == cards[0].suit for card in cards])

        num_counts = {card_num: hand.count(card_num) for card_num in hand}
        multiples = sorted([(num_count[card_num], card_num) for card_num in num_counts], reverse=True)
        rank = '0'

        # Royal flush
        if is_straight and is_flush and hand[0] == 10:
            return ['9'] + [num_to_str(card_num) for card_num in hand]
        # Straight flush
        elif is_straight and is_flush:
            rank = '8'
        # Four of a kind
        elif multiples[0][0] == 4:
            rank = '7'
        # Full house
        elif multiples[0][0] == 3 and multiples[1][0] == 2:
            rank = '6'
        # Flush
        elif is_flush:
            rank = '5'
        # Straight
        elif is_straight:
            rank = '4'
        # Three of a kind
        elif multiples[0][0] == 3:
            rank = '3'
        # Two pair
        elif multiples[0][0] == 2 and multiples[1][0] == 2:
            rank = '2'
        # Pair
        elif kinds[0] == 2:
            rank = '1'
        # No pair
        return [rank] + [num_to_str(multiple[1]) for multiple in multiples]


def num_to_str(number):
    return 'xx23456789TJQKA'[number]

if __name__ == '__main__':
    main()
