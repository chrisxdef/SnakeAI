from snake_enum import Direction
from copy import deepcopy
from Queue import PriorityQueue, Empty
from time import sleep

class NoPath(Exception):
    pass

class SnakeAlgo():
    Width = 0
    Height = 0
    Game_Size = 0
    Bounds = []
    def __init__(self, config_dict):
        SnakeAlgo.Bounds        = config_dict[ 'boundary' ] 
        SnakeAlgo.Width         = config_dict[ 'width' ]
        SnakeAlgo.Height        = config_dict[ 'height' ]
        SnakeAlgo.Game_Size     = (SnakeAlgo.Width) * (SnakeAlgo.Height)
        self.food_limit         = config_dict[ 'food_limit' ]
        self.path               = []

    @staticmethod
    def index_to_coord(index):
        x = index % SnakeAlgo.Width
        y = index / SnakeAlgo.Width
        return ( x, y ) 

    def pick_a_direction(self, game_state):
        if self.path:
            return self.path.pop(0)
        self.path = self.astar(game_state['snake'], game_state['food'])
        return self.path.pop(0)

    def astar(self, snake, food):
        starting_path   = SnakePathModel(deepcopy(snake), food, [ ] ) 
        expanded_start  = starting_path.expand()
        frontier    = PriorityQueue()
        best_seen = None
        for path in expanded_start:
            t_path = ( self.h(path), path )
            frontier.put( t_path )
            if best_seen == None:
                best_seen = t_path
            elif t_path[0] < best_seen[0]:
                best_seen = t_path
        closed      = [ ]
        search_depth = 0
        max_search = 3000
        while True:
            search_depth += 1
            # Pick best path from list
            try:
                best_path = frontier.get(block=False)
            except Empty:
                if best_seen != None:
                    print 'short path'
                    return best_seen[1].path
                print 'No Path Found'
                print 'Game Over'
                raise NoPath()
            # Check if this is a solution
            if best_path[1].check_for_food():
                return best_path[1].path
            if search_depth >= max_search:
                return best_seen[1].path
            # update best seen
            if best_path[0] < best_seen[0]:
                best_seen = best_path
            # Check if this path has been closed
            to_close = (best_path[0], best_path[1].snake[0])
            #to_close = best_path[1].snake[0]
            already_closed = False
            for c in closed:
                if to_close[1] == c[1]:
                    if to_close[0] < c[0]:
                        closed.remove(c)
                        closed.append(to_close)
                    else:
                        already_closed = True
                    break
            if not already_closed:
                closed.append(to_close)
                # Expand the best path
                expanded_list = best_path[1].expand()
                for path in expanded_list:
                    frontier.put( ( self.h(path), path ) )

    def h(self, path):
        head    = path.snake[0]
        tail    = path.snake[len(path.snake)-1]
        food    = path.food
        snake   = path.snake
        #bounds  = SnakeAlgo.Bounds

        # distance to food
        head_x, head_y = SnakeAlgo.index_to_coord(head)
        #h_greedy = 999
        target_food = food[0]
        #for f in food:
        #    food_x, food_y = SnakeAlgo.index_to_coord(f)
        #    diff = ( abs(head_x - food_x) + abs(head_y - food_y) )
        #    if diff < h_greedy:
        #        h_greedy = diff
        #        target_food = f
        # distance from head to tail
        tail_x, tail_y = SnakeAlgo.index_to_coord(tail)
        h_tail = ( abs(head_x - tail_x) + abs(head_y - tail_y) )
        # distance from tail to target food
        food_x, food_y = SnakeAlgo.index_to_coord(target_food)
        h_tail_food = ( abs(food_x - tail_x) + abs(food_y - tail_y) )
        h_turns = 0
        if len(path.path) > 1:
            last_move = path.path[0]
            for i in range(1, len(path.path)):
                if last_move != path.path[i]:
                    h_turns += 1
                last_move = path.path[i]

        # how many open tiles are adjacnet to the head, tail and food
        #h_adj_head = path.count_adjacent(head)
        #h_adj_tail = 4 - path.count_adjacent(tail)
        #h_adj_food = 4 - path.count_adjacent(target_food)
        #h_adj = h_adj_head**4 + h_adj_tail + h_adj_food

        # number of empty reachable tiles or tail is adjacent to free tiles
        h_free = path.h_count_free_tiles()

        #return ( h_free )**4 + h_tail**3 + h_tail_food**4
        return h_tail_food**6 + h_tail**6 + h_free**6 + h_turns**2

class SnakePathModel():
    def __init__(self, snake, food, path):
        self.snake  = snake
        self.food   = food
        self.path   = path

    def copy(self):
        return SnakePathModel(deepcopy(self.snake), self.food, deepcopy(self.path))

    def resolve_direction(self, direction):
        if direction == Direction.UP:
            return -SnakeAlgo.Width
        elif direction == Direction.RIGHT:
            return 1
        elif direction == Direction.DOWN:
            return SnakeAlgo.Width
        elif direction == Direction.LEFT:
            return -1
        return None
    
    def game_over(self):
        head = self.snake[0]
        return head in self.snake[1:] or head in SnakeAlgo.Bounds or head < 0 or head >= SnakeAlgo.Game_Size

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
        new_paths = [] 
        # Up
        path = self.copy()
        if path.update_snake(Direction.UP):
            new_paths.append(path)
        # Right
        path = self.copy()
        if path.update_snake(Direction.RIGHT):
            new_paths.append(path)
        # Down 
        path = self.copy()
        if path.update_snake(Direction.DOWN):
            new_paths.append(path)
        # Left 
        path = self.copy()
        if path.update_snake(Direction.LEFT):
            new_paths.append(path)
        return new_paths

    def check_for_food(self):
        return self.snake[0] in self.food
    
    def get_adjacent(self, n):
        moves = [ self.resolve_direction(Direction.UP), self.resolve_direction(Direction.RIGHT), self.resolve_direction(Direction.DOWN), self.resolve_direction(Direction.LEFT) ]
        adj = []
        for move in moves:
            m = n + move
            if m < SnakeAlgo.Game_Size and  m >= 0 and not m in self.snake and not m in SnakeAlgo.Bounds:
                adj.append(m)
        return adj
    
    def count_adjacent(self, n):
        moves = [ self.resolve_direction(Direction.UP), self.resolve_direction(Direction.RIGHT), self.resolve_direction(Direction.DOWN), self.resolve_direction(Direction.LEFT) ]
        adj = 0
        for move in moves:
            m = n + move
            if m < SnakeAlgo.Game_Size and  m >= 0 and not m in self.snake and not m in SnakeAlgo.Bounds:
                adj += 1
        return adj
 
    def h_count_free_tiles(self):
        head = self.snake[0]
        tail_adj = self.get_adjacent(self.snake[len(self.snake)-1])
        expand = self.get_adjacent(head)
        adj = []
        max_search = len(self.snake)
        while expand:
            n = expand.pop()
            adj.append(n)
            if n in tail_adj:
                return 0
            if len(adj) >= max_search:
                return 2
            adjs = self.get_adjacent(n)
            for m in adjs:
                if not m in adj:
                    expand.append(m)
        return max_search - len(adj)


