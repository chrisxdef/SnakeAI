from snake_enum import Direction
import time
from copy import deepcopy
from Queue import PriorityQueue

class SnakeAlgo():
    Width = 0
    Height = 0
    def __init__(self, config_dict):
        self.bounds             = config_dict[ 'boundary' ] 
        SnakeAlgo.Width         = config_dict[ 'width' ]
        SnakeAlgo.Height        = config_dict[ 'height' ]
        self.food_limit         = config_dict[ 'food_limit' ]
        self.path               = []

    def index_to_coord(self, index):
        x = index % SnakeAlgo.Width
        y = index / SnakeAlgo.Width
        return ( x, y ) 

    def pick_a_direction(self, game_state):
        if self.path:
            return self.path.pop(0)
        # performance timer
        start   = time.time()
        
        self.path = self.astar(game_state['snake'], game_state['food'])

        # performace timer
        print 'pick a direction executed in %d' % (start - time.time())
        return self.path.pop(0)

    def astar(self, snake, food):
        starting_path    = SnakePathModel(deepcopy(snake), food, self.bounds, [ ] ) 
        frontier    = PriorityQueue()
        frontier.put( ( self.h(starting_path), starting_path  ) )
        closed      = [ ]
        best_so_far = ( -999, [ Direction.UP ] )
        while True:
            print frontier.qsize()
            # Pick best path from list
            best_path = frontier.get(block=False)
            best_path = best_path[1]
            # Check if this is a solution
            if best_path.check_for_food():
                print best_path.path
                return best_path.path
            # Check if this path has been closed
            if not best_path.snake[0] in closed:
                # close the current location
                closed.append(best_path.snake[0])
                # Expand the best path
                expanded_list = best_path.expand()
                for path in expanded_list:
                    frontier.put( ( self.h(path), path ) )

    def h(self, path):
        head    = path.snake[0]
        food    = path.food[0]
        snake   = path.snake
        bounds  = self.bounds
        width   = SnakeAlgo.Width
        height  = SnakeAlgo.Height

        # distance too food
        head_x, head_y = self.index_to_coord(head)
        food_x, food_y = self.index_to_coord(food)
        x_diff = (head_x - food_x) ** 2
        y_diff = (head_y - food_y) ** 2
        h_diff = -1 * (x_diff + y_diff)

        min_row = height
        max_row = 0
        min_col = width
        max_col = 0
        for i in snake:
            row = i/width
            col = i%width
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

        return h_diff + rect_a

class SnakePathModel():
    def __init__(self, snake, food, bounds, path):
        self.snake  = snake
        self.food   = food
        self.bounds = bounds
        self.path   = path

    def copy(self):
        return SnakePathModel(deepcopy(self.snake), self.food, self.bounds, deepcopy(self.path))

    def resolve_direction(self, direction):
        if direction == Direction.UP:
            return -SnakeAlgo.Width
        elif direction == Direction.RIGHT:
            return 1
        elif direction == Direction.DOWN:
            return SnakeAlgo.Width
        else:
            return -1
    
    def game_over(self):
        head = self.snake[0]
        return head in self.snake[1:] or head in self.bounds or head < 0 or head >= SnakeAlgo.Width * SnakeAlgo.Height

    def update_snake(self, direction):
        # Apply new head
        head = self.snake[0] + self.resolve_direction(direction)
        self.snake.insert(0, head)
        # Update snake body as required
        # If we are collecting food leave snake as is
        if not self.snake[0] in self.food:
            # When we do not collect food, simply remove the tail of the list
            self.snake.pop()
        if self.game_over():
            return False
        self.path.append(direction)
        return True

    def expand(self):
        new_paths = [ ]
        # Up
        path = self.copy()
        if self.update_snake(Direction.UP):
            new_paths.append(path)
        # Right
        path = self.copy()
        if self.update_snake(Direction.RIGHT):
            new_paths.append(path)
        # Down 
        path = self.copy()
        if self.update_snake(Direction.DOWN):
            new_paths.append(path)
        # Left 
        path = self.copy()
        if self.update_snake(Direction.LEFT):
            new_paths.append(path)
        return new_paths

    def check_for_food(self):
        return self.snake[0] in self.food

