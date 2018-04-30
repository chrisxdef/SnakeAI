from snake_enum import Direction
from copy import deepcopy
from Queue import PriorityQueue, Empty
from time import sleep, time
import math

class NoPath(Exception):
    pass

class SnakeAlgo():
    Width = 0
    Height = 0
    Game_Size = 0
    Moves  = []
    Bounds = []
    def __init__(self, config_dict):
        SnakeAlgo.Bounds        = config_dict[ 'boundary' ] 
        SnakeAlgo.Width         = config_dict[ 'width' ]
        SnakeAlgo.Height        = config_dict[ 'height' ]
        SnakeAlgo.Game_Size     = (SnakeAlgo.Width) * (SnakeAlgo.Height)
        SnakeAlgo.Moves         = [ Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT ]
        for i in range(len(SnakeAlgo.Moves)):
            SnakeAlgo.Moves[i] = SnakeAlgo.resolve_direction(SnakeAlgo.Moves[i])
        self.food_limit         = config_dict[ 'food_limit' ]
        self.path               = []

    @staticmethod
    def resolve_direction(direction):
        if direction == Direction.UP:
            return -SnakeAlgo.Width
        elif direction == Direction.RIGHT:
            return 1
        elif direction == Direction.DOWN:
            return SnakeAlgo.Width
        elif direction == Direction.LEFT:
            return -1
        return None
    
    @staticmethod
    def index_to_coord(index):
        x = index % SnakeAlgo.Width
        y = index / SnakeAlgo.Width
        return ( x, y ) 

    @staticmethod
    def diff(p1, p2):
        p1_x, p1_y = SnakeAlgo.index_to_coord(p1)
        p2_x, p2_y = SnakeAlgo.index_to_coord(p2)
        return abs(p1_x - p2_x), abs(p1_y - p2_y)

    def pick_a_direction(self, game_state):
        if self.path:
            return self.path.pop(0)
        snake   = game_state['snake']
        food    = game_state['food']
        path_model = SnakePathModel( snake, food, [ ] )
        self.path = SnakeAlgo.astar( path_model )
        return self.path.pop(0)

    @staticmethod
    def astar( origin_path_model ):
        # Initialize
        expanded_start  = origin_path_model.expand()
        frontier    = PriorityQueue()
        closed      = [ ]
        food        = origin_path_model.food

        best_seen = None
        for path in expanded_start:
            if path.h_expand()<4:
                t_path = ( path.h(), path )
                frontier.put( t_path )
                if ( best_seen == None or t_path[0] < best_seen[0] ):
                    best_seen = (t_path[0], t_path[1].path)
        if best_seen == None:
            raise NoPath()

        while not frontier.empty():
            best_path = frontier.get(block=False)
            # Check if this is a solution
            # update best seen
            if best_path[1].check_for_food():
                if best_path[1].astar_tail():
                    return best_path[1].path
            else:
                if best_path[0] < best_seen[0]:
                   best_seen = (best_path[0], best_path[1].path)
                # Check if this path has been closed
                to_close = ( best_path[0], best_path[1].snake[0] )
                expand = True
                for c in closed:
                    if to_close[1] == c[1]:
                        if to_close[0] < c[0]:
                            closed.remove(c)
                        else:
                            expand = False
                        break
                if expand:
                    closed.append(to_close)
                    # Expand the best path
                    expanded_list = best_path[1].expand()
                    for path in expanded_list:
                        if path.h_expand()<4:
                            frontier.put( ( path.h(), path ) )

        return best_seen[1]

class SnakePathModel():
    def __init__(self, snake, food, path):
        self.snake  = deepcopy(snake)
        self.food   = deepcopy(food)
        self.path   = deepcopy(path)

    def copy(self):
        return SnakePathModel( self.snake, self.food, self.path )

    def game_over(self):
        head = self.snake[0]
        return head in self.snake[1:] or head in SnakeAlgo.Bounds or head < 0 or head >= SnakeAlgo.Game_Size

    def update_snake(self, direction):
        # Apply new head
        head = self.snake[0] + SnakeAlgo.resolve_direction(direction)
        self.snake.insert(0, head)
        # Update snake body as required
        # If we are collecting food leave snake as is
        if not head in self.food:
            self.snake.pop()
        if self.game_over():
            return False
        self.path.append(direction)
        return True

    def expand(self):
        new_paths = [] 
        moves = [ Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT ]
        for move in moves:
            path = self.copy()
            if path.update_snake(move):
                new_paths.append(path)
        return new_paths

    def check_for_food(self):
        return self.snake[0] in self.food
   

    def h(self):
        food        = self.food[0]
        h_local_center    = self.h_center(self.local_center())
        h_food_center = self.h_center(food)
        h_rect_a    = self.h_rect()

        h = h_food_center + h_local_center + (h_rect_a - len(self.snake))

        return h

    def h_center(self, center):
        center_x, center_y = SnakeAlgo.index_to_coord(center)
        h_snake = 0
        for i in self.snake[1:]:
            x, y = SnakeAlgo.index_to_coord(i)
            h_snake += math.sqrt( (center_x - x)**2 + (center_y - y)**2 )
        return h_snake


    def local_center(self):
        map_center  = SnakeAlgo.Width / 2 + SnakeAlgo.Height / 2
        diam        = math.sqrt(len(self.snake)) + 2
        rad         = diam / 2

        food        = self.food[0]
        
        valid_tile  = False
        i_move      = 0
        centered_dist = 999
        centered = 0
        center = 0
        i = 1
        while i_move < 4:
            move = SnakeAlgo.Moves[i_move]
            center = food + i*move
            if center in SnakeAlgo.Bounds:
                i_move += 1
                i = 1
            else:
                i += 1
                if i > rad:
                    i_move += 1
                    i = 1
                    center_dist = SnakeAlgo.diff(center, map_center)
                    center_dist = center_dist[0] + center_dist[1]
                    if centered_dist > center_dist:
                        centered_dist = center_dist
                        centered = center
        
        return centered

    def h_box(self):
        len_snake   = len(self.snake)
        opt_r       = (math.sqrt(len_snake)+2) / 2

        h_box       = 0
        diff        = 0

        for index in range(1, len_snake):
            if index % opt_r == 0:
                h_box   += diff
                diff    = 0
            diff += abs( self.snake[ index ] - self.snake[ index-1 ] )
   
        h_box += diff

        return h_box        
                
    def h_rect(self):
        min_row = SnakeAlgo.Height
        max_row = 0
        min_col = SnakeAlgo.Width
        max_col = 0
        for i in self.snake:
            row = i/SnakeAlgo.Width
            col = i%SnakeAlgo.Width
            if row > max_row:
                max_row = row
            if row < min_row:
                min_row = row
            if col > max_col:
                max_col = col
            if col < min_col:
                min_col = col
        rect_w = max_col - min_col + 1
        rect_h = max_row - min_row + 1
        rect_a = rect_w * rect_h
                    
        return rect_a

    def h_expand(self):
        expansion_len = len(self.expand())
        return (4 - expansion_len)

    # astar to locate tail and helper functions
    def h_tail(self, head):
        tail    = self.snake[len(self.snake)-1]

        x_diff, y_diff = SnakeAlgo.diff(head, tail)

        return x_diff + y_diff

    def tail_expand(self, s_head):
        expanded = [] 
        for move in SnakeAlgo.Moves:
            head = s_head + move 
            if not head in self.snake[1:len(self.snake)-1] \
                    and not head in SnakeAlgo.Bounds \
                    and not head < 0 \
                    and not head >= SnakeAlgo.Game_Size:
                expanded.append(head)
        return expanded

    def astar_tail(self):
        frontier = PriorityQueue()
        closed = []
        frontier.put( ( self.h_tail(self.snake[0]), self.snake[0] ) )
        tail = self.snake[len(self.snake)-1]

        while not frontier.empty():
            head = frontier.get(block=False)[1]
            if head == tail:
                return True
            if not head in closed:
                closed.append( head )
                expansion = self.tail_expand(head)
                for n_head in expansion:
                    frontier.put( (self.h_tail(n_head), n_head) )

        return False
