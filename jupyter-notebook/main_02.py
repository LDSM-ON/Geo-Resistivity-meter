'''
Geo-Resistivity-meter

Hardware and software repository for a geophysical instrument

**Descrição da função e objetivo do código "Geo-Resistivity-Meter":** 

The provided code is a Python program using the Tkinter library to create a graphical user interface (GUI) for a geophysical measurement instrument called "Geo-Resistivity-Meter." This interface consists of multiple tabs, each representing different functionalities and steps related to measuring apparent resistivity of the soil or subsurface in geophysical applications.

**Code Operation:**

1. The GUI is created using Tkinter and divided into several tabs: "Home Page," "Spreadsheet," "Apparent Resistivity," "Fitting an error model," and "Inversion." Each tab represents a specific functionality of the geophysical instrument.

2. The "Home Page" tab displays information about the Geo-Resistivity-Meter instrument, provides links for help, accessing the project's software repository and information, and allows the user to select a path and folder name to store the resistivity measurement data.

The algorithm uses R2 (http://www.es.lancs.ac.uk/people/amb/Freeware/R2/R2.htm), which is a forward/inverse solution for 3D or 2D current flow in a quadrilateral or triangular mesh. The inverse solution is based on a regularized objective function combined with weighted least squares (an 'Occams' type solution) as defined in Binley and Kemna (2005) and Binley (2015). Electrodes can be placed on the ground surface or in boreholes. Topography is easily accounted for in the finite element mesh. A 32-bit and 64-bit version for Intel compatible processors are provided in the download. Executables for other platforms are available from the author. The current (64-bit) version has no problem size limits.

3. When the START button is clicked, the algorithm creates an object of the Project class, named "k." This is the main object we will interact with. The second step is to read data from a survey file. Here, we choose a CSV file that contains only resistivity data. Importantly, when importing survey data, the object automatically searches for reciprocal measurements and calculates a reciprocal error with the found measurements.

4. The "Spreadsheet" tab is related to the processing and display of resistivity measurement data.

5. In the "Apparent Resistivity" tab, the program reads data from the previously created spreadsheet file and displays it on a pseudo-section graph generated using the Matplotlib library and displayed in the interface.

6. In the "Fitting an error model" tab, another graph is created, representing the fitting of an error model to the measurement data.

Different error models are available to be fitted to DC (direct current) data:

- A simple linear model: k.fitErrorLin()
- A power-law model: k.fitErrorPwl()
- A linear mixed-effect model: k.fitErrorLME() (only on Linux with an R kernel installed)

Each of these models will create a new error column in the Survey object, which will be used in the inversion if k.err = True.

7. In the "Inversion" tab, the data is processed, and a graph is generated, showing the results of the resistivity data inversion.

**Results Visualization and Post-processing:**

Results can be shown using k.showResults(). Multiple arguments can be passed to the method to rescale the color bar, view the sensitivity or not, change the attribute, or plot contours. The inversion errors can also be plotted using k.pseudoError() or k.showInvError().

The inversion takes place in the working directory specified by the R2 object when k = R2 is first called. It can be changed later using k.setwd(<newWorkingDirectory>). The inversion parameters are defined in a dictionary in k.param and can be manually changed by the user (e.g., k.param['a_wgt'] = 0.01). All parameters have default values, and their names follow the R2 manual. The .in file is written automatically when the k.invert() method is called.

**Observations:**

1. Some parts of the code are missing or incomplete, such as the definition of the "selectPath()" function and other functions, as well as the import of the "salve" and "calculadora" modules.

2. Some lines of code are commented, indicating that these parts may be under development or adapted from other modules.

3. The GUI allows user interaction to configure measurements and display results.

4. The code is under development and may not be fully functional or optimized.

5. For the code to work correctly, the imported modules must be available in the execution environment, and any other dependencies must be installed.
'''

# Import the required modules
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import time
import customtkinter
import sys
import re
from tkinter import filedialog
from tkinter.ttk import *
from tkinter import *
from PIL import Image, ImageTk
import time
import numpy as np
import pandas as pd
from pandastable import Table
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from time import strftime
import os
from io import StringIO
from datetime import datetime

# Import the askdirectory function from filedialog
from tkinter.filedialog import askdirectory
import tkinter.messagebox

# Import the showinfo function from messagebox
from tkinter.messagebox import showinfo

# Import the webbrowser module
import webbrowser

# Import the platform module
import platform





def run():
    root = Tk()
    root.title('Geo-Resistivity-Meter')
    width_of_window = 1005
    height_of_window = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width/2)-(width_of_window/2)
    y_coordinate = (screen_height/2)-(height_of_window/2)
    root.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))
    root.configure(bg='white')

    icon = PhotoImage(file="figure/energia3.png")#logo
    root.iconphoto(True, icon)
        
    my_font=('arial', 20, 'bold')
    my_font1=('fantasy', 26, 'bold')
    my_font2=('arial', 12, 'bold')
    root.resizable(False,False)
    
    estado_botao = False
    # ==============================================================================
    # ================== ABAS    ===================================================
    # ==============================================================================
    s = ttk.Style()
    s.theme_create('pastel', settings={
            ".": {
                "configure": {
                    "background": '#ffffcc', # All except tabs
                    "font": 'red'
                }
            },
            "TNotebook": {
                "configure": {
                    "background":'#0b8be0', # Your margin color
                    "tabmargins": [2, 5, 0, 0], # margins: left, top, right, separator
                }
            },
            "TNotebook.Tab": {
                "configure": {
                    "background": '#d9ffcc', # tab color when not selected
                    "padding": [10, 2], # [space between text and horizontal tab-button border, space between text and vertical tab_button border]
                    "font":"white"
                },
                "map": {
                    "background": [("selected", '#ccffff')], # Tab color when selected
                    "expand": [("selected", [1, 1, 1, 0])] # text margins
                }
            }
    })
    s.theme_use('pastel')
    s.configure('TNotebook.Tab', font=my_font2 , highlightbackground="#dce6f4")#fonte da abas
    tabsystem = ttk.Notebook(root)

    # Create new tabs using Frame widget
    tab1 = Frame(tabsystem,width=995,height=800,bg='#f0f0f0')
    tabsystem.add(tab1, text='  Home Page  ')
    tabsystem.place(x=5,y=12)
            
    tab2 = Frame(tabsystem,width=995,height=800,bg='#f0f0f0')
    tabsystem.add(tab2, text='  Spreadsheet  ')
    tabsystem.place(x=5,y=12)
            
    tab3 = Frame(tabsystem,width=995,height=800,bg='#f0f0f0')
    tabsystem.add(tab3, text='  Apparent Resistivity  ')
    tabsystem.place(x=5,y=12)
            
    tab4 = Frame(tabsystem,width=995,height=800,bg='#f0f0f0')
    tabsystem.add(tab4, text='  Fitting an error model  ')
    tabsystem.place(x=5,y=12)
            
    tab5 = Frame(tabsystem,width=995,height=800,bg='#f0f0f0')
    tabsystem.add(tab5, text='  Inversion  ')
    tabsystem.place(x=5,y=12)
   
        
    def cria_pasta():

        path = StringVar()   # Receiving user's file_path selection
        folder = StringVar() # Receiving user's folder_name selection

        Label(tab1,text = "Target path:").place(x=50, y= 250)
        Entry(tab1, textvariable = path).place(x=110, y= 250)
        Button(tab1, text = "Path select: ", command = selectPath).place(x=265, y= 250)


        Label(tab1,text = "Folder name:").place(x=50, y= 300)
        Entry(tab1,textvariable = folder).place(x=110, y= 300)
        Button(tab1, text = "Submit: ", command = create_file).place(x=265, y= 300)
        

    logo_image1 = ImageTk.PhotoImage(Image.open("figure/energia3.png"))
    Label(tab1, image=logo_image1).place(x=5, y=5)
    Label(tab1,text = "Geo-Resistivity-Meter",font=my_font1).place(x=90, y= 10)

    Frame(tab1, width=350, height=150, background="#dce6f4", highlightbackground="black", highlightthickness=3).place(x=5, y=80)
    Frame(tab1, width=350, height=280, background="#dce6f4", highlightbackground="black", highlightthickness=3).place(x=5, y=250)
    Frame(tab1, width=616, height=450, background="#dce6f4", highlightbackground="black", highlightthickness=3).place(x=375, y=80)
    Frame(tab1, width=590, height=140, background="white", highlightbackground="black", highlightthickness=2).place(x=390, y=380)

    Label(tab1,text = "Help",font=my_font,bg='#0b8be0',fg="white").place(x=8, y=83)
    Label(tab1,text = "About",font=my_font,bg='#0b8be0',fg="white").place(x=8, y=253)
    Label(tab1,text = "Start",font=my_font,bg='#0b8be0',fg="white").place(x=378, y=83)
        
    def click1():
        webbrowser.open_new(r"https://github.com/LDSM-ON/Geo-Resistivity-meter")
    def click2():
        webbrowser.open_new(r"https://www.gov.br/observatorio/pt-br")
            
    logo_git = ImageTk.PhotoImage(Image.open("figure/git.png"))
    Label(tab1, image=logo_git).place(x=20, y=130)
    logo_caution = ImageTk.PhotoImage(Image.open("fig/caution.png"))
        
        
    Label(tab1,text = "Geo-Resistivity-Meter \n Hardware and software repository \n for a geophysical instrument \n Made at the",bg= "#dce6f4",font=('helvetica', 11)).place(x=65, y=291)
        
    Button(tab1,text = "Help Home",bd=0,bg= "#dce6f4",command=click1,foreground='blue',font=('helvetica', 11, 'underline')).place(x=40, y=125)
    Button(tab1,text = "Report Problems",bd=0,bg= "#dce6f4",command=click1,foreground='blue',font=('helvetica', 11, 'underline')).place(x=40, y=150)

    Button(tab1,text = "Observatório Nacional",bd=0,bg= "#dce6f4",command=click2,foreground='blue',font=('helvetica', 11, 'underline italic')).place(x=100, y=359)
    Label(tab1,text = "with help from the open-source community \n Raspberry Pi and Arduino \n it is free software and you are welcome \n to distribute it under certain conditions see.",bg= "#dce6f4",font=('helvetica', 11)).place(x=30, y=381)
        
    Label(tab1, text = "Software version: 1.0  \n Python version: %s \n " % platform.python_version() + "tkinter version: %d" % tkinter.TkVersion,bg= "#dce6f4",font=('helvetica', 11)).place(x=100, y=450)

    labelframe = LabelFrame(tab1, text="Project Name",bg='#dce6f4',font=my_font2)
    labelframe.place(x=390, y=130)

    labelframe2 = LabelFrame(tab1, text="Settings",bg='#dce6f4',font=my_font2)
    labelframe2.place(x=390, y=225)

    labelframe3 = LabelFrame(tab1, text="Monitoring",bg='#dce6f4',font=my_font2)
    labelframe3.place(x=390, y=295)

    labelframe4 = LabelFrame(tab1, text="Loop",bg='#dce6f4',font=my_font2)
    labelframe4.place(x=390, y=286)

        
    def selectPath():   
        path_ = askdirectory()
        path.set(path_)
            
    def create_file():
        dirs = os.path.join(path.get(), folder.get())
        if not os.path.exists(dirs):
            os.makedirs(dirs)
            tkinter.messagebox.showinfo('Tips:','Pasta criado com sucesso!')
            
    path = StringVar()   # Receiving user's file_path selection
    folder = StringVar() # Receiving user's folder_name selection
    numberChosen2 = IntVar() # Numero de eletrodos
    AB = StringVar()
    na = StringVar()
            
    Name_label = Label(labelframe,text = "Name:",bg='#dce6f4',font=my_font2).grid(row=0,column=0)
    Name_entry = Entry(labelframe,width=68,bd=2, textvariable=folder).grid(row=0,column=1,padx=10,pady=4)
    Path_label = Label(labelframe,text = "Path:",bg='#dce6f4',font=my_font2).grid(row=1,column=0)
    Path_entry = Entry(labelframe,width=68,bd=2, textvariable = path).grid(row=1,column=1,padx=10,pady=4)
    Button(labelframe, text = "Browse ", command = selectPath, width=8, height=1,font=my_font2).grid(row=1,column=2,padx=3,pady=4)
        
    Label(labelframe2,text='Arranjo',bg='#dce6f4',height=0,font=my_font2).grid(row=0,column=8,padx=3,pady=4)
        
    arranjo = ttk.Combobox(labelframe2 ,state="readonly",width=12,height=40,font=('helvetica', 16, 'bold'))
    arranjo['values'] = ["Dipolo-Dipolo", "Wernner", "Schlumberger", "Pólo-Dipolo"]
    arranjo['state'] = 'readonly'
    arranjo.set("")
    arranjo.grid(row=0,column=9,padx=3,pady=4)
  
    # bind the selected value changes
    def arranjo_changed():
        if arranjo.get() == "Schlumberger":
            print("Schlumberger")
            
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  Dipolo-Dipolo  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>        
        if arranjo.get() == "Dipolo-Dipolo":
            
            sys.path.append((os.path.relpath('../src'))) # add here the relative path of the API folder
            testdir = "../src/examples/dc-2d/"
            from resipy import Project
            k = Project(typ='R2') # create a Project object in a working directory (can also set using k.setwd())
            k.createSurvey(testdir + 'root_file.csv', ftype='Syscal') # read the survey file
                    
                    
            # Function to redirect standard output to a text widget in Tkinter
            class StdoutRedirector:
                def __init__(self, text_widget):
                    self.text_widget = text_widget
                    self.output = StringIO()

                def write(self, text):
                    self.output.write(text)
                    self.text_widget.insert(END, text)
                    self.text_widget.see(END)

            # Create Tkinter main window
                    
            # Create a text widget to display the output
            output_text = Text(tab1, width=62, height=8)
            output_text.place(x=392, y=381)
            
 

            sys.stdout = StdoutRedirector(output_text)

    
            now = datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            
            
           
            print("<<<<<<<<<<<<<<<<<<<<  START OF SURVEY   >>>>>>>>>>>>>>>>")
            print("")
            print("<<<<<<<<<<<<<<<<<<<<  "+date_time+"  >>>>>>>>>>>>>>>>>")

            # Function to display the output
       
                
            k.filterUnpaired()
            k.fitErrorLin()        
            k.createMesh(typ='quad') # generate quadrilateral mesh (default for 2D survey)
            k.showMesh()        
            k.param['data_type'] = 1 # using log of resistitivy
            k.err = True # if we want to use the error from the error models fitted before
            k.invert() # this will do the inversion
            
            
            def create_folder_and_save(df, path, folder_name):
                
                global file_path
                # Get the current date and time
                current_time_date = datetime.now().strftime("%d%m%Y_%H%M%S")
                
                folder_path = os.path.join(path, folder_name + "_" + current_time_date)
                os.makedirs(folder_path, exist_ok=True)

                # Save the file inside the folder
                file_path = os.path.join(folder_path, folder_name + "_" + current_time_date + ".csv")
                df.to_csv(file_path, index=False)
                return file_path

            # ...

            # Here should be the path of the root file that contains the measurement data
            
            df = pd.read_csv('root_file.csv')
            
            create_folder_and_save(df, path.get(), folder.get())
            

            
            # delete space at end and beginning of column names
            headers = df.columns#create a worksheet headers list
            if 'Spa.1' in headers:
                    newheaders = list(map(str.strip, headers)) 
                    dico = dict(zip(headers, newheaders))
                    df = df.rename(index=str, columns=dico)
                    df = df.rename(columns={'Spa.1':'a',
                                                    'Spa.2':'b',
                                                    'Spa.3':'m',
                                                    'Spa.4':'n',
                                                    'Rho_a':'Rho_a',
                                                    'In':'I(mA)',
                                                    'Vp':'vp',
                                                    'Dev.':'dev',
                                                    'M':'ip',
                                                    'Sp':'sp'})
                 
            frame = Frame(tab2)
            frame.pack()
                    
            pt = Table(frame, dataframe=df)  
            table = pt = Table(frame, dataframe=df,showtoolbar=True, showstatusbar=True,width=890, height=480)
            pt.show()
                    
            # Create a figure and axis for the chart
            fig, ax = plt.subplots(figsize=(14, 8))

            # Run k.showPseudo() and plot the graph
            k.showPseudo(ax=ax)

            # Create the canvas widget to display the picture
            canvas = FigureCanvasTkAgg(fig, master=tab3)
            canvas.draw()
            canvas.get_tk_widget().pack()
                    
            #=====================================
            # Create a figure and axis for the chart
            fig, ax = plt.subplots(figsize=(14, 8))

            # Run k.showPseudo() and plot the graph
            k.fitErrorLin(ax=ax)

            # Create the canvas widget to display the picture
            canvas = FigureCanvasTkAgg(fig, master=tab4)
            canvas.draw()
            canvas.get_tk_widget().pack()
            
            
            #=====================================
            # Get the current date and time
            current_time_date = datetime.now().strftime("%d%m%Y_%H%M%S")
            
            # Create a figure and axis for the chart
            fig, ax = plt.subplots(figsize=(14, 8))

            # Run k.showPseudo() and plot the graph
            
            k.showResults(attr='Resistivity(ohm.m)', sens=False, contour=True, vmin=30, vmax=100,ax=ax)
        
            # Create the canvas widget to display the picture
            canvas = FigureCanvasTkAgg(fig, master=tab5)
            canvas.draw()
            canvas.get_tk_widget().pack()

            # Full path to image file
            caminho_imagem = os.path.join(file_path, file_path + "_" + current_time_date + ".jpg")  # Replace with the desired file name

            # Save the canvas as a PNG image in the destination folder
            fig.savefig(caminho_imagem)
            print("")
            print(path.get()+"/"+folder.get())
            
  
            
            print("<<<<<<<<<<<<<<<<<<<<  "+date_time+"  >>>>>>>>>>>>>>>>>")
            print("")
            print("<<<<<<<<<<<<<<<<<<<<<<<  END OF SURVEY   >>>>>>>>>>>>>>>>>>>")
           
        
    
        
    numberChosen2 = ttk.Combobox(labelframe2, values=["24","48","72"],state="readonly",width=3,height=40,font=('helvetica', 14, 'bold'))
    numberChosen2.grid(row=0,column=1)
    numberChosen2.set("24")
    
    numberChosen3 = ttk.Combobox(labelframe4, values=["no loop","15 segundos", "30 segundos", "1 horas", "24 horas"],state="readonly",  width=19,height=50,font=('helvetica', 16, 'bold'))
    numberChosen3.set("no loop")
    numberChosen3.grid(row=0,column=0,padx=4,pady=4)

    N_elec_label = Label(labelframe2,text='N_elec: ',bg='#dce6f4',height=0,font=my_font2).grid(row=0,column=0,padx=3,pady=4)
        
    A_label = Label(labelframe2,text='AB: ',bg='#dce6f4',height=0,font=my_font2).grid(row=0,column=2,padx=3,pady=4)
    A_entry = Entry(labelframe2,bd=2,width=3,font=my_font2,textvariable = AB,bg='yellow').grid(row=0,column=3,padx=3,pady=4)
        
    na_label = Label(labelframe2,text='na: ',bg='#dce6f4',height=0,font=my_font2).grid(row=0,column=6,padx=3,pady=4)
    na_entry = Entry(labelframe2,bd=2,width=3,font=my_font2,textvariable = na,bg='yellow').grid(row=0,column=7,padx=3,pady=4)
        
    def rep():
        if numberChosen3.get() == "no loop":
            arranjo_changed()
        if numberChosen3.get() == "15 segundos":
            for i in range(3):
                arranjo_changed()
                time.sleep(15)
        
        
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
       
    Button(labelframe4, text = "TO UPDATE", width=13, height=3).grid(row=0,column=1,padx=5,pady=4)
    Button(labelframe4, text = "XXXXXX ", width=13, height=3).grid(row=0,column=2,padx=5,pady=4)
    Button(labelframe4, text = "START", command =rep,width=13, height=3).grid(row=0,column=3,padx=5,pady=4)
    


        
    root.mainloop()


