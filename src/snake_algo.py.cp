from snake_enum import Direction
import time
import numpy as np
import codecs, json

class SnakeAlgo():
    def __init__(self, config_dict):
        self.size_of_boundary   = len(config_dict[ 'boundary' ])
        self.bounds             = config_dict[ 'boundary' ] 
        self.width              = config_dict[ 'width' ]
        self.height             = config_dict[ 'height' ]
        self.food_limit         = config_dict[ 'food_limit' ]

        # Matrices
        #Create boundary marix
        b_list = []
        for index in self.bounds:
            x, y = self.index_to_coord(index) 
            b_list.append([ x, y])
        self.b_mat = np.mat( b_list, dtype=float)
    
        # snake body matrix
        self.s_w = np.transpose(np.random.rand(400, 2))
        # boundary matrix
        self.b_w = np.random.rand(self.size_of_boundary, 2)
        # food matrix

        self.models_list = {}
        self.load_models()

    def save_models(self):
        f = open('./memory/N_weights.json', 'w')
        f.write(json.dumps(self.models_list))
        f.close()
    
    def load_models(self):
        f = codecs.open('./memory/N_weights.json', 'r', encoding='utf8')
        models = json.loads(f.read())
        self.models_list = models
        f.close()
        return len(self.models_list)

    def save_model(self, value=None):
        i = len(self.models_list) + 1
        name = "N-weight-%d" % i
        for k in self.models_list:
            if k == name and value['score'] < models_list[k]['value']['score']:
                return 0
        model                       = { }
        model[ 'N-weight' ]         = self.s_w.tolist() 
        model[ 'value'  ]           = value 
        self.models_list[ name ]    = model
    
    def load_model(self, i):
        name  = "N-weight-%d" % i
        model = self.models_list[ name ]
        self.s_w = np.array(model)

    def random_model(self):
        self.s_w = np.transpose(np.random.rand(400, 2))

    def learn_model(self, model1, model2):
        pass

    def index_to_coord(self, index):
        x = index % self.width
        y = index / self.width
        return ( x, y )
    

    def pick_a_direction(self, game_state):
        # performance timer
        start = time.time()
        
        # Retreive Head and Food location, convert to x,y and build a matrix
        head = game_state[ 'head' ]
        food = game_state[ 'food' ][0]
        
        head_x, head_y = self.index_to_coord(head)
        food_x, food_y = self.index_to_coord(food)
        x_diff = head_x - food_x
        y_diff = head_y - food_y

        # build a base direction confidence matrix
        if x_diff == 0:
            left    = 1
            right   = 1
        elif x_diff > 0:
            left    = 2
            right   = 1
        else:
            left    = 1
            right   = 2

        if y_diff == 0:
            up      = 1
            down    = 1
        elif y_diff > 0:
            up      = 2
            down    = 1
        else:
            up      = 1
            down    = 2

        base_direction_mat = np.mat( [ [ left, right ] , [ down, up ] ] )
        base_direction_norm = base_direction_mat / np.linalg.norm(base_direction_mat)
        print base_direction_norm
        # A direction matrix based simply on the distance from food in the x,y space
        # this matrix's values are to be adjusted by the state of the snakes body and game boundary

        # BEGIN SNAKE BODY WEIGHTS
        head_mat = np.mat( [ [ head_x, 0], [0, head_y] ], dtype=float )
        snake = game_state[ 'snake' ]
        n = len(snake)
        # Split the snake weight into the portion we need, by cutting off the matrix at row n
        s_w_split = np.delete(self.s_w, range(n, 400), axis=1) 
        # build snake body matrix
        s_list = []
        for index in snake:
            x, y = self.index_to_coord(index) 
            s_list.append([ x, y ])
        snake_mat = np.mat( s_list, dtype=float )

        # dot the snake_mat and s_w_split matrix, then dot that result with head_mat
        snake_body_w = np.dot(s_w_split, snake_mat)
        snake_body_norm = snake_body_w / np.linalg.norm(snake_body_w)
        print snake_body_norm
        # END SNAKE BODY
        
        # calculate final direction matrix

        direction_mat = np.multiply(base_direction_norm, snake_body_norm)
        print direction_mat 
        # performace timer
        print 'pick a direction executed in %d' % (start - time.time())

        return Direction(np.argmax(direction_mat))

