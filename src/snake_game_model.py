from time import sleep
from random import randint
import snake_game_enum as sg
#Model
class SnakeGameModel():
    def __init__(self):
        self.width = 20
        self.height = 20
        self.score = 0
        self.snake = [22,22+self.width,22+(2*self.width)]
        self.food = [randint(0, self.width*self.height-1)]
        self.snakeInput = sg.NO_INPUT
	self.snakeMove = sg.UP

    def mainloop(self):
        on = True
	sleep(10)
        while on:
            print(self.snake)
            #Grab and input every 0.5 seconds
            sleep(0.5)
            if self.snakeInput != sg.NO_INPUT:
                self.snakeMove = self.snakeInput
		self.snakeInput = sg.NO_INPUT
            if self.gameOver():
		print("Game Over")
                on = False
            else:
                self.snakeUpdate()

    def snakeUpdate(self):
        head = self.snake[0] + self.snakeMove
        self.snake.insert(0, head)
        if head in self.food:
            self.food.remove(head)
            self.score += 1
            self.food.append(randint(0, self.width*self.height-1))
        else:
            self.snake.pop()
            
    def gameOver(self):
        head = self.snake[0]
        move = self.snakeMove
        return move==sg.UP and head/self.height==0 or \
               move==sg.RIGHT and head%self.width==self.width-1 or \
               move==sg.DOWN and head/self.height==self.height-1 or \
               move==sg.LEFT and head%self.width==0 or \
               head + move in self.snake
