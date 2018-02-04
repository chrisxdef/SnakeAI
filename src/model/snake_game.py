
class SnakeGame:
    UP=0,RIGHT=1,DOWN=2,LEFT=3
    def __init__(self):
        self.width = 20
        self.height = 20
        self.board = 20*20*[0]
        self.head = 22
        self.snake = [head,head+width,head+(2*width)]
        self.food = []
    def update(self,cmd):
        #Update head location and check for wall collision
        if cmd==UP and this.head>width-1:
            this.head-=height
        elif cmd==RIGHT and this.head%width==width-1:
            this.head+=1
        elif cmd==DOWN and this.head<((width-1)*height):
            this.head+=height
        elif cmd==LEFT and this.head%width==0:
            this.head-=1
        else:
            gameover()
            return
        #Update Snake location
        #By removing the last location the array now represent the new location of
        #the snake body without the new head locaiton
        #If the snake head is on a food tile then retain the end of the snake body
        #and removee the food from the board
        if this.head in food:
            food.remove(this.head)
        else:
            this.snake.pop()
        #Check for Snake on Snake collision
        #If the new head position is already in the snake's
        #collection then there is a collision
        if this.head in this.snake:
            gameover()
            return
        #Add the new snake head to the snake
        this.snake.insert(0,this.head)
                
    
    def gameover(self):
        print("Game Over")


