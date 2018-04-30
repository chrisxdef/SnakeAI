from random import randint
from snake_enum import Direction
from snake_algo import SnakeAlgo, NoPath
from snake_game_viewer import SnakeGameViewer

class SnakeGameModel():
    def __init__(self):
        self.width = 25
        self.height = 25
        self.snake = [370, 370+self.width, 370+(2*self.width), 370+(3*self.width), 370+(4*self.width), 370+(5*self.width)]
        self.score = 0
        self.n_turns = 0
        self.boundaries = []
        self.set_boundaries()
        self.food = []
        self.food_limit = 1
        self.spawn_food()
        self.snake_direction = Direction.UP
        self.ai = SnakeAlgo(self.config_dictionary())
        self.viewer = SnakeGameViewer(self.config_dictionary())
        self.game_data = None

    def resolve_direction(self):
        if self.snake_direction == Direction.UP:
            return -self.width
        elif self.snake_direction == Direction.RIGHT:
            return 1
        elif self.snake_direction == Direction.DOWN:
            return self.width
        else:
            return -1

    def set_boundaries(self):
        right_inc = self.width - 1
        for i in range(0,self.width):
            # Left
            self.boundaries.append(i*self.width)
            # Right
            self.boundaries.append(i*self.width + right_inc)
        bottom_inc = self.width*(self.height-1) 
        for i in range(1,self.width-1):
            # Top
            self.boundaries.append(i)
            # Bottom
            self.boundaries.append(i+bottom_inc)

    def spawn_food(self):
        if len(self.food) >= self.food_limit:
            return 0
        food = randint(self.width, self.width*(self.height-1))
        while food in self.boundaries or food in self.snake:
            food = randint(self.width, self.width*(self.height-1))
        self.food.append(food)
        return 1

    def config_dictionary(self):
        model = { }
        model [ 'height' ]      = self.height
        model [ 'width' ]       = self.width
        model [ 'boundary' ]    = self.boundaries
        model [ 'food_limit' ]  = self.food_limit
        return model

    def game_state_dictionary(self):
        model = { }
        model [ 'head' ]        = self.snake[0]
        model [ 'tail' ]        = self.snake[len(self.snake)-1]
        model [ 'snake' ]       = self.snake
        model [ 'food' ]        = self.food
        model [ 'n_turns' ]     = self.n_turns
        model [ 'score' ]       = self.score
        return model

    def game_over(self):
        head = self.snake[0]
        return head in self.snake[1:] or head in self.boundaries

    def update_snake(self):
        # Apply new head
        head = self.snake[0] + self.resolve_direction()
        self.snake.insert(0, head)
        # Update snake body as required
        # If we are collecting food leave snake as is
        if not self.collect_food():
            # When we do not collect food, simply remove the tail of the list
            self.snake.pop()

    # Currently calls spawn food as food is collected
    def collect_food(self):
        if self.snake[0] in self.food:
            self.food.remove(self.snake[0])
            self.score += 1
            self.spawn_food()
            return True
        return False

    def main(self):
        try:
            while True:
                self.snake_direction = self.ai.pick_a_direction(self.game_state_dictionary())
                self.update_snake()
                self.viewer.update(self.game_state_dictionary())
                if self.game_over():
                    print 'Game Over\n\n'
                    return 1
                self.n_turns += 1
        except KeyboardInterrupt:
            print "Keyboard Interrupt - Exiting game"
            return 0
        except NoPath:
            print 'No Path'
            return 0

if __name__ == '__main__':
    game = SnakeGameModel()
    main_loop = 1
    while main_loop:
        print '\n\nNew Game\n\n'
        main_loop = game.main()
        print game.game_state_dictionary()
        game = SnakeGameModel()

