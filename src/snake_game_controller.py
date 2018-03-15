from snake_game_model import SnakeGameModel as Model
from snake_game_view import SnakeGameView as View
import copy
import snake_game_enum as sg

MOVES = [ sg.UP, sg.RIGHT, sg.DOWN, sg.LEFT ]
#Controller
class SnakeGameController():
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.ai = SnakeGameAI(model)

    def start(self):
        while True:
            self.view.snake = self.model.snake
            self.view.food = self.model.food
	    self.view.score = self.model.score

class AstarPath():
    def __init(self, model, path):
        self.model = copy.deepcopy(model)
        self.path = path
        self.cost = len(self.path) + self.h(self.path)

    def expand(self):
        head = self.model.snake[0]
        exps = []
        for m in MOVES:
            exp = AstarPath(self.model, self.path)
            exp.model.snakeMove = m
            if not exp.model.gameOver():
                exp.model.snakeUpdate
                exps.append(exp)
        return exps

class SnakeGameAI():
    def __init__(self, model):
        self.model = model
        self.inputs = []

    def getInput(self):
        if self.inputs:
            return self.inputs.pop()
        else:
            frontier = [ AStarPath(self.model) ]
            closed = []
            self.astar(frontier, closed)

    def astar(self, frontier, closed):
        pass
