import tkinter as tk
import tkinter.ttk as ttk
import time
import random
import sys
n = 200
infectedX = []
timeY = []

class Person(object):
    # Constructor: creates a new person/agent
    def __init__(self, canvas, x, y, fill, timeInfected=0):
        # Calculate parameters for the oval/circle to be drawn
        r = 4 
        x0 = x-r
        y0 = y-r
        x1 = x+r
        y1 = y+r

        # Initialize the agents attributrs
        self.timeInfected = timeInfected
        self.x = x
        self.y = y
        self.infected = False
        self.Immune = False
        self.Dead = False

        self.canvas = canvas
        self.id = canvas.create_oval(x0,y0,x1,y1, fill=fill, outline='')


    def move(self):
        Move = 4
        x1, y1, x2, y2 = self.canvas.bbox(self.id)
        dx = random.choice([-Move, Move])
        dy = random.choice([-Move, Move])

        if self.timeInfected > 70/3:
            self.canvas.move(self.id, dx/2, dy/2)
            self.x = self.x + dx/2
            self.y = self.y + dy/2
            
        elif self.Dead == True:
            self.canvas.move(self.id, dx*0, dy*0)
            self.x = self.x + dx*0
            self.y = self.y + dy*0
        
        else:
            self.canvas.move(self.id, dx, dy)
            self.x = self.x + dx
            self.y = self.y + dy

        if self.infected == True:
            self.timeInfected += 1


    def check_infected(self, persons):
        for person in persons:
            d = ((self.x - person.x)**2 + (self.y - person.y)**2)**(1/2)

            if d < 20 and person.infected == True and person.Immune == False and person.Dead == False:
                self.infect()
                
            if self.timeInfected > 70:
                lucky = 1
                lucky = random.choice([1, 2, 3, 4, 5, 0])
                    
                if lucky == 0:
                    self.kill()
                else:
                    self.immune()

            


    def infect(self):
        self.infected = True
        self.canvas.itemconfig(self.id, fill='red')

    def immune(self):
        self.Immune = True
        self.infected = False
        self.canvas.itemconfig(self.id, fill='blue')
        self.timeInfected = 0

    def kill(self):
        self.Dead = True
        self.infected = False
        self.canvas.itemconfig(self.id, fill='black')
        self.timeInfected = 0



class App(object):
    def __init__(self, master, **kwargs):

        # Create the canvas on which the agents are drawn
        self.master = master
        self.canvas = tk.Canvas(self.master, width=700, height=700,background='white')
        self.canvas.pack()

        # Create a reset button for the simulation
        self.but_reset = ttk.Button(master, text = "Reset", command=self.init_sim)
        self.but_reset.pack(side=tk.BOTTOM)

        # Start / init the simulation
        self.init_sim()

        self.master.after(0, self.update)
        self.frame=0

    def update(self):

        # Update / move each agent
        for person in self.persons:
            person.move()
            person.check_infected(self.persons)

        # Count number of infected persons
        ni = 0
        for p in self.persons:
            if p.infected:
                ni += 1
        infectedX.append(ni)
        print("Number of infected persons:", ni)



        self.master.after(100, self.update)
        self.frame += 1
        timeY.append(self.frame)


    # Start / init simulation (clear all agents and create new ones)
    def init_sim(self):
        self.canvas.delete('all')
        self.persons = []

        for i in range(n):
            x = random.randint(50,650)
            y = random.randint(50,650)
            p = Person(self.canvas, x, y, 'green')
            if random.uniform(0,1) < 0.05:
                p.infect()

            self.persons.append(p)

        self.canvas.pack()

        
# Create the Tkinter application and run it
root = tk.Tk()
app = App(root)
start=time.time()
root.mainloop()
end=time.time()
print("Frames:",app.frame)
print("Runtime:",end-start)
print("Framerate:", app.frame/(end-start))
