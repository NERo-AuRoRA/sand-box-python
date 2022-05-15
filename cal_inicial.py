import numpy as np
import threading
import cv2
from tkinter import Tk, Button, messagebox
from openni import openni2

janela = Tk()
janela.geometry("700x300")
janela.title("Interface em desenvolvimento")






pts = []

def cal_inicial():
    global pts
    messagebox.showinfo("Info", "Clique sobre o vértice superior esquerdo da caixa, depois sobre o vértice inferior direito da caixa.")
    if len(pts) !=  0:
        pts = []
    openni2.initialize()
    dev = openni2.Device.open_any()

   
  
    def onMouse1(event, x, y, flags, param):
        
        if event == cv2.EVENT_LBUTTONDOWN:
            pts.append(x)
            pts.append(y)

    cv2.namedWindow("Canvas", cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("Canvas", onMouse1)   

    while (True):
        color_stream = dev.create_color_stream()
        color_stream.start()
    # show
        cframe = color_stream.read_frame()
        cframe_data = np.array(cframe.get_buffer_as_triplet()).reshape([480, 640, 3])
        R = cframe_data[:, :, 0]
        G = cframe_data[:, :, 1]
        B = cframe_data[:, :, 2]
        cframe_data = np.transpose(np.array([B, G, R]), [1, 2, 0])
  
 
        cv2.imshow("Canvas", cframe_data)
        cv2.waitKey(34)
        if (cv2.getWindowProperty("Canvas", cv2.WND_PROP_VISIBLE) <1):
            if (len(pts) != 4):
                messagebox.showinfo("Info", "calibre a área da caixa")
                pts = []
                break
        
            
            
        if (len(pts) == 4) :
            if (pts[0] >= pts[2]) or (pts[1] >= pts[3]):
                messagebox.showinfo("Info", "Clique sobre o vértice superior esquerdo da caixa, depois sobre o vértice inferior direito. Calibre novamente")
                pts = []
                break
            else:
                break
    cv2.destroyAllWindows()




botao4 = Button(janela, text="Aplicar", command= lambda: threading.Thread(target=cal_inicial()).start())
botao4.pack()

janela.mainloop()