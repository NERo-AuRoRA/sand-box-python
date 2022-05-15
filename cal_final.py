import cv2
import numpy as np
import threading
from tkinter import ttk, Tk, IntVar, Scale, Button


janela = Tk()
janela.geometry("700x300")
janela.title("Interface em desenvolvimento")

h = janela.winfo_screenheight()
w = janela.winfo_screenwidth()

v1 = IntVar()
s1 = Scale( janela, variable = v1,
           from_ = 1, to = 800, 
           orient = "horizontal") 
s1.set(400)
s1.pack(anchor = "center") 


v2 = IntVar()
s2 = Scale( janela, variable = v2,
           from_ = 1, to = 800, 
           orient = "horizontal") 
s2.set(400)
s2.pack(anchor = "center") 

v3 = IntVar()
s3 = Scale( janela, variable = v3,
           from_ = -180, to = 180, 
           orient = "horizontal") 
s3.set(0)
s3.pack(anchor = "center") 

v4 = IntVar()
s4 = Scale( janela, variable = v4,
           from_ = -180, to = 180, 
           orient = "horizontal") 
s4.set(0)
s4.pack(anchor = "center") 

v5 = IntVar()
s5 = Scale( janela, variable = v5,
           from_ = -180, to = 180, 
           orient = "horizontal") 
s5.set(0)
s5.pack(anchor = "center") 

botao4 = Button(janela, text="Aplicar", command= lambda: threading.Thread(target=f, args= (h, w)).start())
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