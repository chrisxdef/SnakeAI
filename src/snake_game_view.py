from Tkinter import *
class SnakeGameView(Tk):
    def __init__(self, width, height, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.width = width
        self.height = height
        self.snake = []
        self.food = []
	self.score = 0
        self.scale = 16
        #Where we put the scoreboard
        self.title("SnA*ke")
        self.sidebar = Frame(self, width=200, bg='white', height=500, relief='sunken', borderwidth=2)
        self.sidebar.pack(expand=True, fill='y', side='left', anchor='nw')  
        #Where we draw our canvas
        self.mainarea = Frame(self, bg='#CCC', width=500, height=500)
        self.mainarea.pack(expand=True, fill='both', side='right')
        #Where we draw our model data
        self.w = Canvas(self.mainarea, width=self.width*self.scale, height=self.height*self.scale)
        self.w.pack()
        #Create each grid box and store them in a list
        self.grid = []
        for i in range(self.width*self.height):
            x= (i%self.width)*self.scale
            y= (i/self.width)*self.scale
            self.grid.append(self.w.create_rectangle(x,y,x+self.scale,y+self.scale, fill="white"))
        #Dynamic text box to update score
        self.scoreboard = Label(self.sidebar, text="0")
        self.scoreboard.pack()
	self.redraw(5)       
 
    def redraw(self, delay):
        #Update scoreboard
        self.scoreboard.configure(text=str(self.score))
        for i in range(self.width*self.height):
            color = "white"
            if i in self.snake:
                color = "black"
            elif i in self.food:
                color = "gray"
            self.w.itemconfig(self.grid[i], fill=color)
                    
        self.after(delay, lambda: self.redraw(delay))
