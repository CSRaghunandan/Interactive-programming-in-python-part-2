# implementation of card game - Memory

import simplegui
import random

deck = list(range(0, 8) + range(0, 8))
exposed = [False] * 16
turns, state = 0, 0
index1, index2 = 999, 999

# helper function to initialize globals
def new_game():
    global turns, deck, state, exposed
    random.shuffle(deck)  
    turns, state = 0, 0
    label.set_text("Turns = " + str(turns))
    index1, index2 = 999, 999
    exposed = [False] * 16
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, index1, index2, turns
    index = pos[0] // 50
    
    if state == 0:
        exposed[index] = True
        index1 = index
        state = 1
    elif state == 1:    
        if exposed[index] == True:
            return
        else:
            exposed[index] = True
            turns += 1
            label.set_text("Turns = " + str(turns))
            index2 = index
            state = 2
    else:
        if exposed[index] == True:
            return
        else:
            exposed[index] = True
                     
        if deck[index1] == deck[index2]:
            pass
        else:
            exposed[index1], exposed[index2] = False, False
        index1 = index
        state = 1
                           
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(len(deck)):
        if exposed[i]:
            canvas.draw_text(str(deck[i]), [(i*50) + 5,80],90,"Red")
        else:
            canvas.draw_polygon([[50*i, 0], [50*(i+1), 0], [50*(i+1), 100], [50*i, 100]],2, "cyan","green")
    

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = " + str(turns))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric
