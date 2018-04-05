import subprocess as sp
from sys import stdout

class SnakeGameViewer():
    def __init__(self, config):
        self.height     = config['height']
        self.width      = config['width']
        self.bounds     = config['boundary']
    
    def update(self, update):
        snake      = update['snake']
        food       = update['food']
        score      = update['score']
        # clear screen
        sp.call('clear', shell=True)
        for i in range(self.width*self.height):
            if i == snake[0]:
                stdout.write(' %')
            elif i == snake[len(snake)-1]:
                stdout.write(' #')
            elif i in self.bounds or i in snake:
                stdout.write(' @')
            elif i in food:
                stdout.write(' $')
            else:
                stdout.write('  ')
            if i % self.width == self.width-1:
                stdout.write('\n')

        stdout.flush()

        print score
