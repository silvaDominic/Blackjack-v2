import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_backs = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# used for drawing hands
DEALER_HAND_LOC = [100, 100]
PLAYER_HAND_LOC = [100, 400]
# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    # create a card object if it is of a valid type
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank
    # return a string representation of a card
    def __str__(self):
        return self.suit + self.rank
    # return the suit of a card
    def get_suit(self):
        return self.suit
    # return the rank of a card
    def get_rank(self):
        return self.rank
    # draw card
    def draw(self, canvas, pos):
        # card location depends on image format (see image url)
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))

        # Ranks and Suits are multiplied by the starting position coordinates
        canvas.draw_image(card_images, card_loc, CARD_SIZE,
                          [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []

    def __str__(self):
        # return a string representation of a hand
        s = ""
        for i in range(len(self.hand)):
            s += " " + str(self.hand[i])
        return "Hand contains: " + s

    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        hand_total = 0
        has_Ace = False
        for card in self.hand:
            hand_total += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                has_Ace = True

        if has_Ace == False:
            return hand_total
        else:
            if hand_total + 10 <= 21:
                return hand_total + 10
            else:
                return hand_total

    def draw(self, canvas, pos):
        # draw a hand on the canvas, uses draw method for cards
        # spacing is one card width
        spacing = 76
        for card in self.hand:
            card.draw(canvas, [pos[0] + spacing, pos[1]])
            spacing += 76


# define deck class
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()

    def __str__(self):
        # return a string representing the deck
        s = ""
        for i in range(len(self.deck)):
            s += str(self.deck[i])
        return "" + s

# define event handlers for buttons
def deal():
    # initialize globals
    global outcome, in_play, player_hand, dealer_hand, game_deck, score, is_bust

    is_bust = False
    # penalize player if resets hand in middle of a turn
    if in_play == True:
        score -= 1

        # create players and deck, shuffle deck
    dealer_hand = Hand()
    player_hand = Hand()
    game_deck = Deck()
    game_deck.shuffle()

        # deal cards to players
    for i in range(2):
        player_hand.add_card(game_deck.deal_card())
        dealer_hand.add_card(game_deck.deal_card())

    # controls whether player is still active
    in_play = True

def hit():
    #initialize globals
    global score, outcome, is_bust, in_play

    # as long as player is still active and has not busted, evaluated hand
    if in_play == True and is_bust == False:
        player_hand.add_card(game_deck.deal_card())
        if player_hand.get_value() > 21:
            in_play = False
            is_bust = True
            outcome = "You busted!"
            score -= 1
        elif player_hand.get_value() == 21:
            stand()

def stand():
    # initialize globals
    global score, outcome, in_play

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play == True:
        while dealer_hand.get_value() < 17:
            print "Dealer hits.."
            dealer_hand.add_card(game_deck.deal_card())
            outcome = "Dealer's: " + str(dealer_hand) + " " + str(dealer_hand.get_value())

        # other conditions
        if dealer_hand.get_value() <= 21:
            if dealer_hand.get_value() == player_hand.get_value():
                score -= 1
                outcome = "Tie! Dealer wins!"

            elif dealer_hand.get_value() > player_hand.get_value():
                score -= 1
                outcome = "Dealer wins!"
            else:
                score += 1
                outcome = "You win!"
        else:
            score += 1
            outcome = "Dealer busts! You win!"

    # game has ended
    in_play = False

# draw handler
def draw(canvas):

    # useful display information
    canvas.draw_text(str(player_hand.get_value()), (250, 550), 25, 'White')
    canvas.draw_text('Score: ' + str(score), (400, 550), 25, 'White')
    player_hand.draw(canvas, PLAYER_HAND_LOC)
    dealer_hand.draw(canvas, DEALER_HAND_LOC)

    # draw back image over 'hole' card until game is over
    if in_play == True:
        canvas.draw_image(card_backs, CARD_BACK_CENTER, CARD_SIZE,
                          [DEALER_HAND_LOC[0] + 76 + CARD_BACK_CENTER[0],
                           DEALER_HAND_LOC[1] + CARD_BACK_CENTER[1]] , CARD_SIZE)

    #display outcome and dealer's final score
    else:
        canvas.draw_text(outcome, (225, 300), 25, 'Red')
        canvas.draw_text(str(dealer_hand.get_value()), (250, 50), 25, 'White')

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()