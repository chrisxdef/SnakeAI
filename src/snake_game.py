from time import sleep
from random import *
from Tkinter import *
import json
import operator
import math

class SnakeGame(Tk):
    UP=-20
    RIGHT=1
    DOWN=20
    LEFT=-1
    def __init__(self, *args, **kwargs):
	Tk.__init__(self, *args, **kwargs)
        self.width = 20
	self.bias = [1.0, 1.0, 1.0, 1.0]
	self.key = "1.0:1.0:1.0:1.0"
	self.highscores = []
        self.height = 20
        self.board = self.width*self.height*[0]
	self.score = 0
        self.head = 22
        self.snake = [self.head,self.head+self.width,self.head+(2*self.width)]
        self.food = [10]
        self.last_input = None
       	self.scale = 16
	self.title("SnA*ke")
	self.grid = []
	self.sidebar = Frame(self, width=200, bg='white', height=500, relief='sunken', borderwidth=2)
	self.sidebar.pack(expand=True, fill='y', side='left', anchor='nw')	
	self.mainarea = Frame(self, bg='#CCC', width=500, height=500)
	self.mainarea.pack(expand=True, fill='both', side='right')
	self.w = Canvas(self.mainarea, width=self.width*self.scale, height=self.height*self.scale)
	self.w.pack()
	for i in range(self.width*self.height):
	    x= (i%self.width)*self.scale
	    y= (i/self.width)*self.scale
	    self.grid.append(self.w.create_rectangle(x,y,x+self.scale,y+self.scale, fill="white"))
	self.scoreboard = Label(self.sidebar, text="0")
	self.scoreboard.pack()
	self.on = True

	self.population = []
	self.initPopulation()

	self.c = 0
	
	self.redraw(1)

    def update(self,cmd):
	self.c+=1
	if self.c == 400:
	    print("caught in loop")
	    self.gameover()
	    self.c = 0;
 	    return
	if cmd == None:
	    cmd = self.last_input
	self.last_input = cmd
        #Update head location and check for wall collision
        if cmd==SnakeGame.UP and self.head>self.width-1:
            self.head-=self.width
        elif cmd==SnakeGame.RIGHT and self.head%self.width!=self.width-1:
            self.head+=1
        elif cmd==SnakeGame.DOWN and self.head<((self.width-1)*self.height)-1:
            self.head+=self.width
        elif cmd==SnakeGame.LEFT and self.head%self.width!=0:
            self.head-=1
        else:
            self.gameover()
            return
        #Update Snake location
        #By removing the last location the array now represent the new location of
        #the snake body without the new head locaiton
        #If the snake head is on a food tile then retain the end of the snake body
        #and removee the food from the board
        if self.head in self.food:
	    self.c = 0
	    self.score += 1
            self.food.remove(self.head)
            r = randint(0,399)
	    while r in self.snake or r in self.food:
        	r = randint(0,399)
            self.food.append(r)
        else:
            self.snake.pop()
        #Check for Snake on Snake collision
        #If the new head position is already in the snake's
        #collection then there is a collision
        if self.head in self.snake:
            self.gameover()
            return
        #Add the new snake head to the snake
        self.snake.insert(0,self.head)

    def ai(self):
        frontier = [[0,self.head]]
        closed = []
        path = self.astar(frontier,closed)
        if path == None or len(path)<3:
            return self.idle() 
        move = path[2]
        diff = self.head - move
        if diff == self.width:
            return SnakeGame.UP
        if diff == -self.width:
            return SnakeGame.DOWN
        if diff == -1:
            return SnakeGame.RIGHT
        if diff == 1:
            return SnakeGame.LEFT
        return None
        
        
    def idle(self):            
	h = self.head
	moves = []
	if h>=self.width and not h-self.width in self.snake:
		moves.append(SnakeGame.UP)
	if h%self.width!=self.width-1 and not h+1 in self.snake:
		moves.append(SnakeGame.RIGHT)
	if h+self.width<self.height*(self.width-1) and not h+self.width in self.snake:
		moves.append(SnakeGame.DOWN)
	if h%self.width!=0 and not h-1 in self.snake:
		moves.append(SnakeGame.LEFT)
	if not moves:
		return None
	best = 9999
	for i in moves:
		if self.h(i+h) < best:
			best = i
	return best
	

    def astar(self,frontier,closed, best=None):
        if not frontier:
            return best
        #Explore frontier for shortest path
        shortest = frontier[0]
        for p in frontier:
            if p[0] < shortest[0]:
                shortest = p
        frontier.remove(shortest)
	if best == None:
	    best = shortest
	elif shortest[1]-shortest[0] < best[1]-best[0]:
	    best = shortest
        #Expand upon the shortest path
        #Do not include paths that lead into a wall, snake or indexes in closed
        #When a possible path is found update its score and add it to the frontier
	#Update snake
	snake = self.snake[:]
	for i in shortest[2:]:
		snake.pop()
		snake.insert(0, i)
	
        #Expansion of shortest path BEGIN
        #End of shortest path index
        n = shortest[len(shortest)-1]
        #If n is food, we found the shortest path to food
        if n in self.food:
            return shortest
        #close this index
        if not n in closed:
            closed.append(n)
            #UP
            if n>self.width and not n-self.width in self.snake and not n-self.width in closed:
                up = shortest[:]
                up[0] = len(up) + self.h(n-self.width, snake)
                up.append(n-self.width)
                frontier.append(up)
            #DOWN
            if n<(self.width-1)*self.height-1 and not n+self.width in self.snake and not n+self.width in closed:
                down = shortest[:]
                down[0] = len(down) + self.h(n+self.width, snake)
                down.append(n+self.width)
                frontier.append(down)
            #LEFT
            if n%self.width!=0 and not n-1 in self.snake and not n-1 in closed:
                left = shortest[:]
                left[0] = len(left) + self.h(n-1, snake)
                left.append(n-1)
                frontier.append(left)
            #RIGHT
            if n%self.width!=self.width-1 and not n+1 in self.snake and not n+1 in closed:
                right = shortest[:]
                right[0] = len(right) + self.h(n+1, snake)
                right.append(n+1)
                frontier.append(right)
            #END
        return self.astar(frontier,closed, shortest)

        
    def h(self, n, snake=None):
	if snake == None:
	    snake = self.snake
	#Implement a heuristic that uses the position of the snake
	min_row = self.height
	max_row = 0
	min_col = self.width
	max_col = 0
	for i in snake:
	    row = i/self.width
	    col = i%self.width
	    if row > max_row:
		max_row = row
	    if row < min_row:
		min_row = row
	    if col > max_col:
		max_col = col
	    if col < min_col:
		min_col = col
	rect_w = max_col + min_col + 1
	rect_h = max_row + min_row + 1
	rect_a = rect_w * rect_h

        h_rows = self.height*self.width
        h_cols = self.height*self.width
        for f in self.food:
            #number of rows from n to f
            rows = abs(n/self.width-f/self.width)
            #' ' cols ' ' ' '
            cols = abs(n%self.width-f%self.width)
            if rows<h_rows and cols<h_cols:
                h_rows = rows
                h_cols = cols

	#Add 1 if tile is near a wall
	h_wall = 0.0
	if n % self.width == 0:
	    h_wall+=1
	if n % self.width == self.width-1:
	    h_wall+=1
	if n < self.width:
	    h_wall+=1
	if n / self.width == self.height-1:
	    h_wall+=1

	#how much free space around this point
	h_free = 0.0
	sqre = int( math.ceil(math.sqrt(len(self.snake))/2.0) )
	for i in range(n-(sqre)-(sqre*self.width),n+(sqre)+(sqre*self.width)):
		if i in snake or i<n and i%self.width>n%self.width and i%self.width>(n+sqre)%self.width or i>n and i%self.width<n%self.width and i%self.width<(n+sqre)%self.width:
			h_free+=1

        return float(h_cols+h_rows) * self.bias[0] + float(rect_a-len(snake)) * self.bias[1] + h_wall * self.bias[2] + h_free * self.bias[3]
                
    def gameover(self):
	self.c = 0
        print("Game Over")
	self.setHighscore()
        self.setBias(self.population.pop())
	if not self.population:
	    self.nextGeneration()
	self.score = 0
        self.head = 22
        self.snake = [self.head,self.head+self.width,self.head+(2*self.width)]
        self.food = [10]
	    
	

    def redraw(self, delay):
	self.scoreboard.configure(text=str(self.score))
	if self.on:	
		self.update(self.ai())
		for i in range(len(self.board)):
			color = "white"
			if i in self.snake:
			    color = "black"
			elif i in self.food:
			    color = "gray"
			self.w.itemconfig(self.grid[i], fill=color)
					
		self.after(delay, lambda: self.redraw(delay))

    def setBias(self, bias):
	self.bias = bias[:]
	self.key = str(self.bias[0]) + ':' + str(self.bias[1]) + ':' + str(self.bias[2]) + ':' + str(self.bias[3])

   # record a score and sore by best
    def setHighscore(self):
	print("Snake " + self.key)
	with open('./highscores.json', 'r') as hs:
	    data = json.loads(hs.read())
	    hs.close()
	if self.key in data.keys():
	    if data[self.key] >= self.score:
		print("Score " + str(self.score))
		return
	print("Highscore " + str(self.score))
	data[self.key] = self.score
	sorted_data = sorted(data.items(), key=operator.itemgetter(1))
	self.highscores = []
	k = 5
	if len(sorted_data) < k:
		k = len(sorted_data)
	for i in range(k):
		self.highscores.append(sorted_data[i])
	with open('./highscores.json', 'w') as hs:
	    hs.write(str(json.dumps(data)))
	    hs.close()
	
    def getTopN(self, n):
	with open('./highscores.json', 'r') as hs:
	    data = json.loads(hs.read())
	    hs.close()
	sorted_data = sorted(data.items(), key=operator.itemgetter(1))
	self.highscores = []
	if len(sorted_data) < n:
		n = len(sorted_data)
	self.highscores = []
	for i in range(n):
		self.highscores.append(sorted_data[i])
	

    def getHighscore(self, key=None, bias=None):
	if key == None:
	    key = self.key
	if bias == None:
	    bias = self.bias[:]
	with open('./highscores.json', 'r') as hs:
	    data = json.loads(hs.read())
	    hs.close()
	if key in data.keys():
	   return data[key]
	return None


    def initPopulation(self):
	for i in range(1000):
	    bias = []
	    for i in range(len(self.bias)):
		bias.append(random())
	    self.population.append(bias)
		

    def nextGeneration(self):
	print("new Gen")
	pop = []
	top = self.getTopN(500)
	self.population = []
	for i in range(500):
	    pair = []
	    for i in range(10):
		r = choice(top)
		if r[1] > pair[0][1]:
		    pair.insert(0, r)
	    pair = self.nextPop([pair[0][0], pair[1][0]])
	    pop.append(pair[0])
	    pop.append(pair[1])
	    
    def nextPop(self, pair):
	first = pair[0].split(':')
	second = pair[1].split(':')
	pair = [first, second]
	new_bias1 = []
	new_bias2 = []
	for i in range(len(first)):
	    r = nextInt(2)
	    new_bias1.append(float(pair[r][i]))
	    r = (r+1)%2
	    new_bias2.append(float(pair[r][i]))
	if random() < 0.2:
	    new_bias1[randInt(len(new_bias))] = choice(new_bias) * random()
	if random() < 0.2:
	    new_bias2[randInt(len(new_bias))] = choice(new_bias) * random()
	return [new_bias1, new_bias2]
 


if __name__ == '__main__':
    game = SnakeGame()
    game.mainloop()
