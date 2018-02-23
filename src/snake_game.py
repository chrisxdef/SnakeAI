from time import sleep
from random import randint
from random import choice
from Tkinter import *

class SnakeGame(Tk):
    UP=-20
    RIGHT=1
    DOWN=20
    LEFT=-1
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.width = 20
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
        self.redraw(5)

    def update(self,cmd):
        if cmd == None:
            cmd = self.last_input
        self.last_input = cmd
        #Update head location and check for wall collision
        if cmd==SnakeGame.UP and self.head>self.width-1:
            self.head+=SnakeGame.UP
        elif cmd==SnakeGame.RIGHT and self.head%self.width!=self.width-1:
            self.head+=SnakeGame.RIGHT
        elif cmd==SnakeGame.DOWN and self.head/self.width!=self.height-1:
            self.head+=SnakeGame.DOWN
        elif cmd==SnakeGame.LEFT and self.head%self.width!=0:
            self.head+=SnakeGame.LEFT
        else:
            self.gameover()
            return
        #Update Snake location
        #By removing the last location the array now represent the new location of
        #the snake body without the new head locaiton
        #If the snake head is on a food tile then retain the end of the snake body
        #and removee the food from the board
        if self.head in self.food:
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

    def getAdjacent(self, n, snake=None):
        if snake == None:
            snake = self.snake
        adj = []
        #Up
        up = n+SnakeGame.UP
        if not up<0 and not up in snake:
            adj.append(up)
        #Down
        down = n+SnakeGame.DOWN
        if not down>=self.width*self.height and not down in snake:
            adj.append(down)
        #Left
        left = n+SnakeGame.LEFT
        if not left%self.width==self.width-1 and not left in snake:
            adj.append(left)
        #Right
        right = n+SnakeGame.RIGHT
        if not right%self.width==0 and not right in snake:
            adj.append(right)
        return adj

    def getAllAdjacent(self, n, snake=None):
        if snake == None:
            snake = self.snake
        frontier = [n]
        closed = []
        while frontier:
            if len(closed) > len(snake)*2:
                return closed
            k = frontier.pop()
            closed.append(k)
            adj = self.getAdjacent(k, snake)
            for i in adj:
                if not i in closed:
                    frontier.append(i)
        return closed

    def countAdjacent(self, n, snake=None):
        if snake == None:
            snake = self.snake
        return len(self.getAllAdjacent(n, snake))
        

    def ai(self):
        frontier = [[9999,self.head]]
        closed = []
        path = self.astar(frontier,closed)
        if path == None or len(path)<3:
            print(len(path))
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
        return diff
        
    def idle(self):            
        h = self.head
        print("idle")
        moves = []
        #UP
        if h>=self.width and not h+SnakeGame.UP in self.snake:
                moves.append(SnakeGame.UP)
        #RIGHT
        if h%self.width!=self.width-1 and not h+SnakeGame.RIGHT in self.snake:
                moves.append(SnakeGame.RIGHT)
        #DOWN
        if h/self.width!=self.height-1 and not h+SnakeGame.DOWN in self.snake:
                moves.append(SnakeGame.DOWN)
        #LEFT
        if h%self.width!=0 and not h+SnakeGame.LEFT in self.snake:
                moves.append(SnakeGame.LEFT)
        if not moves:
                return None
        best = 9998
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
        elif shortest[0]-len(shortest) < best[0]-len(best):
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
        return self.astar(frontier,closed,best)

        
    def h(self, n, snake=None):
        if len(self.getAdjacent(n, snake))==0:
            return 9999
        if snake == None:
            snake = self.snake
        #Implement a heuristic that uses the position of the snake
        #Build rectangle around snake and find rect's area
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

       #get the number of cols away head is from rect
        m = snake[0]%self.width
        m_cols = abs(max_col - m)
        if m_cols < abs(min_col - m):
            m_cols = abs(min_col - m)
        #and rows
        m_rows = abs(max_row - m)
        if m_rows < abs(min_row - m):
            m_rows = abs(min_row - m)
        h_edge = m_rows + m_cols


        #distance to food
        h_rows = self.height*self.width
        h_cols = self.height*self.width
        if not food:
            h_rows = 0
            h_cols = 0
        for f in self.food:
            #number of rows from n to f
            rows = abs(n/self.width-f/self.width)
            #' ' cols ' ' ' '
            cols = abs(n%self.width-f%self.width)
            if rows<h_rows and cols<h_cols:
                h_rows = rows
                h_cols = cols

        #Count all tiles adjacent to this tile and adjacent to those
        h_adj = self.countAdjacent(n, snake)

        
        
        return (h_cols + h_rows) + ((rect_a-len(snake)) + (len(snake) - h_adj) + h_edge)*2

    def gameover(self):
        print("Game Over")
        print(self.last_input)
        self.on = False

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

if __name__ == '__main__':
    game = SnakeGame()
    game.mainloop()
