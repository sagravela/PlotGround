from tkinter import *
import numpy as np
from tkinter import messagebox
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import copy


class App:
    def __init__(self, frame, figure):
        self.frame = frame
        self.figure = figure
        self.ax = False
        
        # Define animation method
        self.ani = animation.FuncAnimation(figure, self.animate, interval=1000)
        
        # Range and sampling interval of x and y for default
        self.ranx = [1, 10]
        self.rany = [1, 10]
        self.int_muestreo = 0.01
        self.x = np.arange(self.ranx[0], self.ranx[1], self.int_muestreo)
        self.y = np.arange(self.rany[0], self.rany[1], self.int_muestreo)

        # Boolean control var for clear figure and function data
        self.gc = False
        self.graph_data = False
        self.last_plot = None

        # Conversion of functions from user input to numpy form
        self.funciones = {"sin":"np.sin", "cos":"np.cos", "tan": "np.tan", "log": "np.log", "pi": "np.pi",
"sqrt": "np.sqrt", "e": "np.e"}
        
        # Define a custom color cycle
        self.custom_colors = ['black', 'red', 'green', 'blue', 'orange', 'yellow']

        # WIDGETS SET

        # Sampling Interval
        self.etiqim= Label(self.frame, text="Sample Range: ")
        self.enterint_muestreo= Entry(self.frame, width=5)

        # Function
        self.etiqf=Label(self.frame, text="Function to plot: ")
        self.enterfunction= Entry(self.frame, width=60)
        self.enterfunction.config(bg="gray87",justify="left")

        # X range
        self.etiqr=Label(self.frame, text="X range: ")
        self.enterrange= Entry(self.frame, width=10)

        # Y range
        self.etiqry=Label(self.frame, text="Y range: ")
        self.enterrangey= Entry(self.frame, width=10)

        # Graphic and axis titles
        self.label3d = Label(self.frame, text="Optionally parameters for 3D graphic")
        self.labeltitle= Label(self.frame, text="Graphic name: ")
        self.labelx=Label(self.frame, text="X-axis name: ")
        self.labely=Label(self.frame, text="Y-axis name: ")
        self.labelz=Label(self.frame, text="Z-axis name: ")
        self.xentry= Entry(self.frame)
        self.yentry= Entry(self.frame)
        self.zentry= Entry(self.frame)
        self.titleentry=Entry(self.frame)

        # Buttons
        self.button= Button(self.frame, text="PLOT", bg="white", command=self.represent)
        self.clear_graphs= Button(self.frame, text="CG", bg="white", command=self.graphs_clear)
        self.clear= Button(self.frame, text="C", bg="white", command=self.fields_clear)

        # WIDGETS LOCATION AND PADDING

        self.etiqf.grid(row=0, column=0, padx=10)
        self.enterfunction.grid(row=1, column=0, padx=5)
        self.button.grid(row=2, column=0)
        self.clear.grid(row=3, column=0, pady=5)
        self.clear_graphs.grid(row=4, column=0)
        self.etiqr.grid(row=0, column=1, padx=10)
        self.enterrange.grid(row=0, column=2, padx=10)
        self.labeltitle.grid(row=0, column=3)
        self.labelx.grid(row=1, column=3)
        self.labely.grid(row=2, column=3)
        self.xentry.grid(row=1, column=4)
        self.yentry.grid(row=2, column=4)
        self.titleentry.grid(row=0, column=4)
        self.etiqim.grid(row=1 , column=1, padx=5, pady=5)
        self.enterint_muestreo.grid(row=1 , column=2, padx=5, pady=5)
        self.label3d.grid(row=3, column=3)
        self.etiqry.grid(row=4, column=1, padx=10)
        self.enterrangey.grid(row=4, column=2, padx=10)
        self.labelz.grid(row=4, column=3, padx=10)
        self.zentry.grid(row=4, column=4, padx=10)


            
    def animate(self, frame):
        xtitle= self.xentry.get()
        ytitle= self.yentry.get()
        ztitle= self.zentry.get()
        titlegraph= self.titleentry.get()

        # Clear figure and return
        if self.gc and self.ax:
            self.figure.delaxes(self.ax)
            self.ax = False
            self.gc = False
            self.last_plot = None
            self.ani.event_source.stop()
            return

        if self.graph_data:
            if 'y' in self.graph_data:
                # if tha last plot wasn't a 3d plot so remove axis and create a new one
                if self.last_plot and 'y' not in self.last_plot:
                    self.figure.delaxes(self.ax)
                    self.ax = False
                if not self.ax:
                    self.ax = self.figure.add_subplot(111, projection='3d')
                try:
                    # First try to plot in 3D
                    x, y = np.meshgrid(self.x,self.y)
                    solo=eval(self.graph_data)
                    self.ax.plot_surface(x, y, solo, cmap='viridis')
                except:
                    messagebox.showwarning("ERROR", '''Not possible to plot in 3D''')
            else:
                # if the last plot wasn't a 2d plot so remove it and create a new one
                if self.last_plot and 'y' in self.last_plot:
                    self.figure.delaxes(self.ax)
                    self.ax = False
                if not self.ax:
                    self.ax = self.figure.add_subplot()

                    # Set the custom color cycle as the new default
                    self.ax.set_prop_cycle(color=self.custom_colors)
                try:
                    x = copy.deepcopy(self.x)
                    # Then try to plot in 2D
                    solo=eval(self.graph_data)
                    self.ax.plot(x, solo)
                except:
                    messagebox.showwarning("ERROR", '''Not possible to plot''')
                
            # save last plot
            self.last_plot = copy.deepcopy(self.graph_data)
        
        plt.show()

        if self.ax:
            self.ax.set_ylabel(ytitle)
            self.ax.set_xlabel(xtitle)
            try:
                self.ax.set_zlabel(ztitle)
            except:
                pass
            self.ax.set(title=titlegraph)
            
            self.ax.axhline(0, color="gray")
            self.ax.axvline(0, color="gray")

        self.ani.event_source.stop() # Stop Animation

    def represent(self):
        if not self.gc:
            function= self.enterfunction.get() 
            ranx= self.enterrange.get()
            rany= self.enterrangey.get()

            if self.enterint_muestreo.get():
                try:
                    self.int_muestreo=float(self.enterint_muestreo.get())
                except:
                    messagebox.showwarning("ERROR", '''You should insert a valid number''')

            if ranx:
                try:
                    self.ranx= ranx.split(",")
                    self.x = np.arange(float(self.ranx[0]), float(self.ranx[1]), self.int_muestreo)
                except:
                    messagebox.showwarning("ERROR","Insert values on X range separated with comma")
                    self.enterrange.delete(0, END)
           
            if rany:           
                try:
                    self.rany= rany.split(",")
                    self.y = np.arange(float(self.rany[0]), float(self.rany[1]), self.int_muestreo)
                except:
                    messagebox.showwarning("ERROR","Insert values on Y range separated with comma")
                    self.enterrangey.delete(0, END)

            for i in self.funciones:
                if i in function:
                    function=function.replace(i, self.funciones[i])
            
            self.graph_data=function.lower()

        self.ani.event_source.start() # Start Animation

    def graphs_clear(self):
        self.gc = True
        self.represent()

    def fields_clear(self):
        self.enterint_muestreo.delete(0, END)
        self.enterfunction.delete(0, END)
        self.enterrange.delete(0, END)
        self.enterrangey.delete(0, END)
        self.xentry.delete(0, END)
        self.yentry.delete(0, END)
        self.zentry.delete(0, END)
        self.titleentry.delete(0, END)

        # reset variables after clear
        self.ranx = [1, 10]
        self.rany = [1, 10]
        self.int_muestreo = 0.01
        self.x = np.arange(self.ranx[0], self.ranx[1], self.int_muestreo)
        self.y = np.arange(self.rany[0], self.rany[1], self.int_muestreo)

