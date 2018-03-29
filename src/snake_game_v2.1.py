from time import sleep
from random import randint
from random import choice
from Tkinter import *
import threading
from Queue import Queue, PriorityQueue
from copy import deepcopy

# Globals
# Inputs
UP = -20
RIGHT = 1
DOWN = 20
LEFT = -1
MOVES = [UP, RIGHT, DOWN, LEFT]
# Queue shared by Controller and Model for updating game
INPUT_QUEUE = Queue()
# Game state queue
STATE_QUEUE = Queue(1)
# Parameters for game
HEIGHT = 20
WIDTH = 20

ON = True

#Game Data Model
class SnakeGameModel():
    def __init__(self):
        self.score = 0
        self.snake = [42,42+WIDTH,42+(2*WIDTH)]
        self.food = [randint(0, WIDTH*HEIGHT-1)]
        self.snakeDirection = UP

    def getInputQueue(self):
        snakeMove = self.snakeDirection if INPUT_QUEUE.empty() else INPUT_QUEUE.get()
        self.snakeDirection = snakeMove
        return snakeMove
        
    def update(self, snakeMove=None):
        #Grab and input every 0.5 seconds
        sleep(0.5)
        if snakeMove == None:
            snakeMove = self.getInputQueue()
        if self.gameOver():
            return False
        else:
            head = self.snake[0] + self.snakeDirection()
            self.snake.insert(0, head)
            if head in self.food:
                food.remove(food)
                score += 1
                food.append(randint(0, WIDTH*HEIGHT-1))
            else:
                self.snake.pop()

        return True
    
    def gameOver(self):
        head = self.snake[0]
        move = self.snakeDirection
        return move==UP and head/HEIGHT==0 or \
               move==RIGHT and head%WIDTH==WIDTH-1 or \
               move==DOWN and head/HEIGHT==HEIGHT-1 or \
               move==LEFT and head%WIDTH==0

    def clone(self):
        gm = SnakeGameModel()
        gm.score = self.score
        gm.snake = list(self.snake)
        gm.food = list(self.food)
        return gm
#Game Controller (Input Handler / AI)
class SnakeGameController():
    def __init__(self):
        pass
        
    def closed(self,path,closed):
        threshold = 10
        #entry[0] the heuristic score
        #entry[1] the end of path
        head = path[1].state.snake[0]
        for entry in closed:
            if entry[1] == head:
                return abs(entry[0] - path[0]) > threshold
        closed.append((path[0], head))
        return False
            
    #Frontier is a priority queue (h_value, SnakePath)
    def astar(self,frontier,closed,score):
        first = frontier.get()
        print len(first[1].path)
        if first[1].state.score > score:
            return first[1]
        #Add to close
        if not self.closed(first,closed):
            print("closed")
            expansion = first[1].expand()
            print("expansion")
            for path in expansion:
                frontier.put((path.h(), path))
            print("puts")
        return self.astar(frontier,closed,score)

    def main(self):
        while ON:
            if INPUT_QUEUE.empty:
                game_state = STATE_QUEUE.get()
                frontier = PriorityQueue()
                frontier.put((9999, SnakePath([], game_state)))
                path = self.astar(frontier, [], game_state.score)
                for i in path.path:
                    INPUT_QUEUE.put(i)
            
class SnakePath():
    def __init__(self, path, game_state):
        self.path = path
        self.state = game_state
        self.h_value = None

    def simulate(self, move):
        #copy game state
        new_state = self.state.clone()
        if new_state.update(snakeMove=move):
            path = list(self.path)
            path.append(move)
            return SnakePath(path, new_state)
        return None

    def expand(self):
        paths = []
        for move in MOVES:
            p = self.simulate(move)
            if not p == None:
                paths.append(p)
        return paths

    def h(self):
        n = self.state.snake[0]
        if not self.h_value == None:
            return self.h_value
        snake = self.state.snake
        food = self.state.food
        #Implement a heuristic that uses the position of the snake
        #Build rectangle around snake and find rect's area
        #min_row = HEIGHT
        #max_row = 0
        #min_col = WIDTH
        #max_col = 0
        #for i in snake:
        #    row = i/WIDTH
##            col = i%WIDTH
##            if row > max_row:
##                max_row = row
##            if row < min_row:
##                min_row = row
##            if col > max_col:
##                max_col = col
##            if col < min_col:
##                min_col = col
##        rect_w = max_col + min_col + 1
##        rect_h = max_row + min_row + 1
##        rect_a = rect_w * rect_h
##
##       #get the number of cols away head is from rect
##        m = snake[0]%WIDTH
##        m_cols = abs(max_col - m)
##        if m_cols < abs(min_col - m):
##            m_cols = abs(min_col - m)
##        #and rows
##        m_rows = abs(max_row - m)
##        if m_rows < abs(min_row - m):
##            m_rows = abs(min_row - m)
##        h_edge = m_rows + m_cols


        #distance to food
        h_rows = HEIGHT*WIDTH
        h_cols = HEIGHT*WIDTH
        for f in food:
            #number of rows from n to f
            rows = abs(n/WIDTH-f/WIDTH)
            #' ' cols ' ' ' '
            cols = abs(n%WIDTH-f%WIDTH)
            if rows<h_rows and cols<h_cols:
                h_rows = rows
                h_cols = cols


        self.h_value = h_cols + h_rows
       # self.h_value = (h_cols + h_rows) + ((rect_a-len(snake)*2) + h_edge*2)*2
        return self.h_value
    
#Application
class SnakeGameApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        #Create Game Model
        self.game_model = SnakeGameModel()
        #Where we put the scoreboard
        self.title("SnA*ke")
        self.sidebar = Frame(self, width=200, bg='white', height=500, relief='sunken', borderwidth=2)
        self.sidebar.pack(expand=True, fill='y', side='left', anchor='nw')  
        #Where we draw our canvas
        self.mainarea = Frame(self, bg='#CCC', width=500, height=500)
        self.mainarea.pack(expand=True, fill='both', side='right')
        #Where we draw our model data
        self.scale = 16
        self.w = Canvas(self.mainarea, width=WIDTH*self.scale, height=HEIGHT*self.scale)
        self.w.pack()
        #Create each grid box and store them in a list
        self.grid = []
        for i in range(WIDTH*HEIGHT):
            x= (i%WIDTH)*self.scale
            y= (i/WIDTH)*self.scale
            self.grid.append(self.w.create_rectangle(x,y,x+self.scale,y+self.scale, fill="white"))
        #Dynamic text box to update score
        self.scoreboard = Label(self.sidebar, text="0")
        self.scoreboard.pack()
        self.counter = 200
        self.redraw(5)
        
    def redraw(self, delay):
        global ON
        if self.counter == 0:
            ON = self.game_model.update()
            if STATE_QUEUE.full():
                STATE_QUEUE.get()
            STATE_QUEUE.put(self.game_model)
        self.counter = (self.counter+1) % 200
        if not ON:
            print "Game Over"
            return
        #Update scoreboard
        self.scoreboard.configure(text=str(self.game_model.score))
        #Update grid
        for i in range(WIDTH*HEIGHT):
            color = "white"
            if i in self.game_model.snake:
                color = "black"
            elif i in self.game_model.food:
                color = "gray"
            self.w.itemconfig(self.grid[i], fill=color)

        self.after(delay, lambda: self.redraw(delay))

game = SnakeGameApp()
#Create Game Controller
game_controller = SnakeGameController()
controller = threading.Thread(target=game_controller.main)
controller.start()
game.mainloop()
