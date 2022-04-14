
import tkinter as tk
from tkinter import ttk

import numpy as np
import cv2
from openni import openni2

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np

import threading

janela = tk.Tk()
janela.geometry("700x300")
janela.title("Interface em desenvolvimento")

h = janela.winfo_screenheight()
w = janela.winfo_screenwidth()

v1 = tk.IntVar()
s1 = ttk.Scale( janela, variable = v1, 
           from_ = 1, to = 800, 
           orient = "horizontal") 
s1.set(400)
s1.pack(anchor = "center") 


v2 = tk.IntVar()
s2 = ttk.Scale( janela, variable = v2, 
           from_ = 1, to = 800, 
           orient = "horizontal") 
s2.set(400)
s2.pack(anchor = "center") 

v3 = tk.IntVar()
s3 = ttk.Scale( janela, variable = v3, 
           from_ = -180, to = 180, 
           orient = "horizontal") 
s3.set(0)
s3.pack(anchor = "center") 

v4 = tk.IntVar()
s4 = ttk.Scale( janela, variable = v4, 
           from_ = -180, to = 180, 
           orient = "horizontal") 
s4.set(0)
s4.pack(anchor = "center") 

v5 = tk.IntVar()
s5 = ttk.Scale( janela, variable = v5, 
           from_ = -180, to = 180, 
           orient = "horizontal") 
s5.set(0)
s5.pack(anchor = "center") 

botao4 = ttk.Button(janela, text="Aplicar", command= lambda: threading.Thread(target=f, args= (h, w)).start())                                 
botao4.pack()
                           

def cal_final(h= 100, w = 100):
   
    x = 0
    y = 0
    while (True):
        
        x = v1.get()
        y = v2.get()
        center = [w/2 + v4.get() , h/2 + v5.get()]
        rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=v3.get(), scale=1)

        x1 = int((w/2)-(x/2)) + v4.get()
        y1 = int((h/2)-(y/2)) + v5.get()
        x2 = int((w/2)+(x/2)) + v4.get()
        y2 = int((h/2)+(y/2)) + v5.get()
        canvas = np.ones((h, w, 3))*0
        vermelho = (0, 0, 255)
        cv2.rectangle(canvas, (x1, y1), (x2, y2), vermelho, -1)
        canvas = cv2.warpAffine(src=canvas, M=rotate_matrix, dsize=(w, h))
    
        cv2.imshow("Canvas", canvas)
        cv2.waitKey(34)   
        if (cv2.getWindowProperty("Canvas", cv2.WND_PROP_VISIBLE) <1) :
            break


janela.mainloop()