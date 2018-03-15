import thread
from snake_game_model import SnakeGameModel as Model
from snake_game_controller import SnakeGameController as Controller
from snake_game_view import SnakeGameView as View

model = Model()
view = View(model.width, model.height)
controller = Controller(model, view)
print("Controller Thread")
thread.start_new_thread(controller.start, ())
print("Model Thread")
thread.start_new_thread(model.mainloop, ())
print("View Thread")
view.mainloop()
