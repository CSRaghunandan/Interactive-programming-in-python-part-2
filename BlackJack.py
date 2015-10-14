# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome, message, try_again = "", "hit or stand?", ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.card = []

    def __str__(self):
        result = "Hand Contains "
        for card in self.card:
            result += card.suit  + card.rank + " " 
        return result

    def add_card(self, card):
        self.card.append(Card(card.suit, card.rank))

    def get_value(self):
        contain_aces = False
        hand_value = 0
        
        for card in self.card:
            hand_value += VALUES[card.rank]
            
        for card in self.card:
            if card.rank == 'A':
                contain_aces = True
            
        if not contain_aces:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
            
    def draw(self, canvas, pos):
        for card in self.card:
            card.draw(canvas, pos)
            pos[0] += 30 + CARD_SIZE[0] 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for i in SUITS:
            for j in RANKS:
                self.deck.append(Card(i, j))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
            
    def __str__(self):
        result = "Deck contains "
        for card in self.deck:
            result += card.suit + card.rank + " "
        return result


# globals for deck, dealer, player
deck = Deck()
dealer, player = Hand(), Hand()


#define event handlers for buttons
def deal():
    global outcome, message, in_play, try_again
    global deck, player, dealer, score
     
    # your code goes here
    outcome, message, try_again  = "", "Hit or stand?", ""
    if in_play:
        score -= 1
        try_again = "Dealed in-play. Dealer Wins"
        in_play = False
    
    deck = Deck()
    deck.shuffle()
    dealer, player = Hand(), Hand()
    
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())

    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    
    print "Dealers hand: " + str(dealer)
    print "Players hand: " + str(player)
    
    in_play = True

def hit():
    global  outcome, message, player, try_again
    global score, in_play
    if in_play:
        try_again = ""
        if player.get_value() <= 21:
            player.add_card(deck.deal_card())
            print "Players hand: " + str(player)
            
            if player.get_value() > 21:
                outcome = "Player busted. Dealer Wins"
                message = "New Deal?"
                print outcome
                in_play = False
                score -= 1
    else:
        try_again = "Can't hit when not in play"
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global outcome, message , dealer, try_again
    global score, in_play
    if not in_play:
        try_again = "Can't stand when not in play"
        print outcome
    else:
        try_again = ""
        while dealer.get_value() < 17 and in_play == True:
            dealer.add_card(deck.deal_card())
            print "Dealers Hand: " + str(dealer)
            if dealer.get_value() > 21:
                outcome = "Dealer busted. Player Wins."
                message = "New Deal?"
                in_play = False
                print outcome
                score += 1
                return
        if dealer.get_value() >= player.get_value():
            outcome = "Dealer Wins."
            score -= 1
            print outcome

        else:
            outcome = "Player Wins."
            score += 1
            print outcome
        message = "New Deal?"
        in_play = False        
           
# draw handler    
def draw(canvas):
    canvas.draw_text("Blackjack", [80,120], 50, "Black")
    canvas.draw_text("Score = " + str(score), [350, 120], 50, "Black")
    
    canvas.draw_text("Dealer", [80, 180], 30, "blue")
    canvas.draw_text(outcome, [230, 180], 30, "blue")
    canvas.draw_text(try_again,[80,340], 30, "blue")
    dealer.draw(canvas, [80, 200])
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,[80+36, 200 + 48], CARD_BACK_SIZE)
    canvas.draw_text("Player", [80, 380], 30, "blue")
    canvas.draw_text(message, [230,380], 30, "blue")
    player.draw(canvas, [80, 400])


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


# remember to review the gradic rubric
