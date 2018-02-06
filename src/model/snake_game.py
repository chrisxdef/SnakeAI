from time import sleep
from random import randint
import numpy as np


class SnakeGame:
    UP=0
    RIGHT=1
    DOWN=2
    LEFT=3
    def __init__(self):
        self.width = 20
        self.height = 20
        self.board = 20*20*[0]
        self.head = 22
        self.snake = [self.head,self.head+self.width,self.head+(2*self.width)]
        self.food = [10]
        self.on = False
        
    def update(self,cmd):
        print(cmd)
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
            self.food.remove(self.head)
            r = randint(0,399)
            self.food.append(r)
            print("food"+str(r))
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
        if path == None:
            return None
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
        
        
                
    def astar(self,frontier,closed):
        if not frontier:
            return None
        #Explore frontier for shortest path
        shortest = frontier[0]
        for p in frontier:
            if p[0] < shortest[0]:
                shortest = p
        frontier.remove(shortest)
        #Expand upon the shortest path
        #Do not include paths that lead into a wall, snake or indexes in closed
        #When a possible path is found update its score and add it to the frontier
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
                up[0] = len(up) + self.h(n-self.width)
                up.append(n-self.width)
                frontier.append(up)
            #DOWN
            if n<(self.width-1)*self.height-1 and not n+self.width in self.snake and not n+self.width in closed:
                down = shortest[:]
                down[0] = len(down) + self.h(n+self.width)
                down.append(n+self.width)
                frontier.append(down)
            #LEFT
            if n%self.width!=0 and not n-1 in self.snake and not n-1 in closed:
                left = shortest[:]
                left[0] = len(left) + self.h(n-1)
                left.append(n-1)
                frontier.append(left)
            #RIGHT
            if n%self.width!=self.width-1 and not n+1 in self.snake and not n+1 in closed:
                right = shortest[:]
                right[0] = len(right) + self.h(n+1)
                right.append(n+1)
                frontier.append(right)
            #END
        return self.astar(frontier,closed)

        
    def h(self, n):
        h_rows = self.height*self.width
        h_cols = self.height*self.width
        for f in self.food:
            #number of rows from n to f
            rows = abs(n/self.width-f/self.width)
            if rows<h_rows:
                h_rows = rows
            #' ' cols ' ' ' '
            cols = abs(n%self.width-f%self.width)
            if cols<h_cols:
                h_cols = cols
        return h_cols + h_rows  
        
                
    def gameover(self):
        print("Game Over")
        self.on = False

    def paint(self):
        BLACK = [0,0,0]
        WHITE = [255,255,255]
        data = np.zeroes((WIDTH,HEIGHT),dtype=np.uint8)

        data[0,WIDTH*HEIGHT-1] = WHITE
        for i in this.snake:
            data[i,i] = BLACK
        for i in this.food:
            data[i,i] = BLACK
            

        img = smp.toimage(data)
        img.show()

        

if __name__ == '__main__':
    game = SnakeGame()
    move = None
    game.on = True
    while(game.on):
        a_move = game.ai()
        if(not a_move is None):
            move = a_move
        game.update(move)
        game.paint()
        print(game.snake)
        sleep(0.5)
