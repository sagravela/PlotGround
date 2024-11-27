from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import style
from math import *
from app import *

def main():
    
    # initialize root
    root = Tk()
    root.wm_title("PlotGround")
    style.use('fast')

    frame= Frame(root)
    frame.pack()

    # set figure
    figure = Figure(figsize=(12, 8))

    canvas = FigureCanvasTkAgg(figure, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)# barra de iconos
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    
    # Frame where are inputs from user
    frame2= Frame(root)
    frame2.pack()
    
    App(frame2, figure)
    
    root.mainloop()


if __name__=="__main__":
    main()
    