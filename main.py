#==========================================================================================

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

#==========================================================================================
    #Inicializando kinect
#==========================================================================================

dist = 0


openni2.initialize()
dev = openni2.Device.open_any()
depth_stream = dev.create_depth_stream()
depth_stream.start()


#==========================================================================================
    #Definindo função para vizualização das curvas de nível
#==========================================================================================

def exibe_curvas_de_nivel(depth_stream, n_curvas_de_nivel=40, x_label=np.arange(80, 640, 1),
                          y_label=np.arange(10, 480, 1)):
    """
    Função para definir a exibição das curvas de nível na imagem.
    :param depth_stream:
    :param n_curvas_de_nivel:
    :param x_label:
    :param y_label:
    :return:
    """
    x_label, y_label = np.meshgrid(x_label, y_label)
    frame = depth_stream.read_frame()
    frame_data = frame.get_buffer_as_uint16()

    img = np.frombuffer(frame_data, dtype=np.uint16)

    z_label = np.reshape(img, (480, 640))[10:480, 80:]
    z_label = np.rot90(z_label, 2)

    fig, ax = plt.subplots()
    CS = ax.contour(x_label, y_label, z_label, n_curvas_de_nivel)
    ax.clabel(CS, fontsize=9, inline=True)
    ax.set_title('Curva de nível')
    plt.show()
#==========================================================================================
    #Definindo função para vizualização em 3D
#==========================================================================================

def exibe_3d(depth_stream, x_label=np.arange(80, 640, 1), y_label=np.arange(10, 480, 1), cmap=cm.coolwarm, linewidth=0,
             antialised=True):
    """
    Função para fazer a exibição da imagem em três dimensões
    :param depth_stream:
    :param x_label:
    :param y_label:
    :param cmap:
    :param linewidth:
    :param antialised:
    :return:
    """
    x_label, y_label = np.meshgrid(x_label, y_label)

    frame = depth_stream.read_frame()
    frame_data = frame.get_buffer_as_uint16()

    img = np.frombuffer(frame_data, dtype=np.uint16)

    z_label = np.reshape(img, (480, 640))[10:480, 80:]
    z_label = np.fliplr(z_label)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    surf = ax.plot_surface(x_label, y_label, z_label, cmap=cmap, linewidth=linewidth, antialiased=antialised)
    ax.zaxis.set_major_formatter('{x:.02f}')
    fig.colorbar(surf, shrink=0.5, aspect=5)  
    plt.show()
    


def exib_TR(depth_stream, mapoption = cv2.COLORMAP_JET, walloption=1, curv = 1, n=5, thicknesscurv= 2, siz = 10):
    
    def onMouse(event, x, y, flags, param):
        global dist   
        if event == cv2.EVENT_MOUSEMOVE:
            dist = (val1/val2)*imgray[y, x]
    def resolu(siz):        
        if siz == 10:
            res = [0,0]
        elif siz == 0:
            res = [640,480]
        elif siz == 1:
            res = [720, 640]
        elif siz == 2:
            res = [1280, 720]
        return res
    
    res = resolu(siz)
   
    cv2.namedWindow("Curvas em tempo real com mapa de cores", cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("Curvas em tempo real com mapa de cores", onMouse)            
    while(True):
        
        frame = depth_stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()
        img = np.frombuffer(frame_data, dtype=np.uint16)

        img.shape = (1, 480, 640)
        img = np.fliplr(img)    
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 0, 1)
        img = img[10:480, 80:]

        val1 = np.amax(img)

        img = cv2.convertScaleAbs(img, alpha=0.1) 
        img = cv2.rotate(img, cv2.ROTATE_180) 
        
        im_color = cv2.applyColorMap(img, mapoption) 
        im_color = cv2.medianBlur(im_color, 21)
        im_color1 = cv2.applyColorMap(img, cv2.COLORMAP_BONE)
        
        if (siz != 10):
            im_color = cv2.resize(im_color, res, interpolation=cv2.INTER_LINEAR)
            im_color1 = cv2.resize(im_color1, res, interpolation=cv2.INTER_LINEAR)    
        
        imgray = cv2.medianBlur(cv2.cvtColor (im_color1, cv2.COLOR_BGR2GRAY), 43)

        val2 = np.amax(imgray)
        
        whitewall = (np.ones(im_color.shape))*255
        if walloption == 0: wall = whitewall
        elif walloption == 1: wall = im_color
        if curv == 1:
            for i in range(255):     
                ret, thresh = cv2.threshold (imgray, (n*i), 255, cv2.THRESH_BINARY)
                contours, his  = cv2.findContours (thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                cv2.drawContours(wall, contours, -1, (0,0,0), thicknesscurv)
        if type(dist) == np.float32:
            cv2.putText(wall,str(int(dist)),(10,((np.size(wall,0))-30)),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),1)
            
        cv2.imshow("Curvas em tempo real com mapa de cores", (wall))    
          
        cv2.waitKey(34)
      
        if cv2.getWindowProperty("Curvas em tempo real com mapa de cores", cv2.WND_PROP_VISIBLE) <1:
            break


#==========================================================================================
    #adicionando thread
#==========================================================================================

def m1():
    if ((thickness_curv.current() != -1) & (siz.current() != -1 )
                                     & (numbers_curv.current() != -1)
                                     & (gradi.current() != -1)):
                                     x = threading.Thread(target=exib_TR(depth_stream, 
                                       gradi.current(),var1.get(),var2.get(),var3.get(),var4.get(), siz.current()))
                                     x.start()
    else:
        tk.messagebox.showerror("Erro", "Defina todos os paramêtros")

def m4():
    x = threading.Thread(target= exibe_curvas_de_nivel(depth_stream, n_curvas_de_nivel=40,
                         x_label=np.arange(80, 640, 1), y_label=np.arange(10, 480, 1)))
    x.start()

def m5():
    x = threading.Thread(target=exibe_3d(depth_stream, x_label=np.arange(80, 640, 1),
                      y_label=np.arange(10, 480, 1), cmap=cm.coolwarm, linewidth=0, antialised=True))
    x.start()
#==========================================================================================
    #Criando interface gráfica
#==========================================================================================


janela = tk.Tk()
janela.geometry("700x300")
janela.title("Interface em desenvolvimento")

a = 10
b = 30
c = 10

botao1 = ttk.Button(janela, text="Exibir", command= m1 )
botao1.place(height=20, width=50, x=a, y=(c + 4*b))

texto = ttk.Label(janela, text="Escolha modo de exibição do frame capturado:")
texto.place(height=20, width=250, x=a, y=(c + 5*b))

texto2 = ttk.Label(janela, text="Defina os parâmetros para exibição em tempo real:")
texto2.place(height=20, width=300, x=a, y=(c + 2*b))

botao4 = ttk.Button(janela, text="Exibir curvas", command= m4)
botao4.place(height=20, width=80,x=a, y=(c + 6*b))

botao5 = ttk.Button(janela, text="Exibir superficie", command=m5)
botao5.place(height=20, width=100, x=a, y=(c + 7*b))

var1 = tk.IntVar()
check2 = ttk.Checkbutton(janela, text='Cores', variable= var1)
check2.place(height=20, width=100, x=a, y=(c + 3*b))

var2 = tk.IntVar()
check2 = ttk.Checkbutton(janela, text='Curvas', variable= var2)
check2.place(height=20, width=100, x=27*a, y=(c + 3*b))

selected_gradient = tk.StringVar()
lt =  ['COLORMAP_AUTUMN','COLORMAP_BONE' ,
                       'COLORMAP_JET(PADRÃO)' ,
                       'COLORMAP_WINTER' ,
                       'COLORMAP_RAINBOW' ,
                       'COLORMAP_OCEAN',
                       'COLORMAP_SUMMER',
                       'COLORMAP_SPRING',
                       'COLORMAP_COOL',
                       'COLORMAP_HSV',
                       'COLORMAP_PINK',
                       'COLORMAP_HOT',
                       'COLORMAP_PARULA',
                       'COLORMAP_MAGMA',
                       'COLORMAP_INFERNO',
                       'COLORMAP_PLASMA',
                       'COLORMAP_VIRIDIS',
                       'COLORMAP_CIVIDIS',
                       'COLORMAP_TWILIGHT',
                       'COLORMAP_TWILIGHT_SHIFTED',
                       'COLORMAP_TURBO',
                       'COLORMAP_DEEPGREEN']
gradi = ttk.Combobox(janela, values = lt, textvariable= selected_gradient)
gradi.set('Mapa de cor')
gradi['state'] = 'readonly'
gradi.place(height=20, width=195, x=7*a, y=(c + 3*b))

var3 = tk.IntVar()
list_numbers_curv= [1,3,5,8,10,15,20,30]
numbers_curv = ttk.Combobox(janela, values = list_numbers_curv, textvariable= var3)
numbers_curv.set('Distância entre curvas')
numbers_curv['state'] = 'readonly'
numbers_curv.place(height=20, width=140, x=33*a, y=(c + 3*b))


var4 = tk.IntVar()
list_thickness_curv = [1,2,3,4,5,6,7,8]
thickness_curv = ttk.Combobox(janela, values =list_thickness_curv, textvariable= var4)
thickness_curv.set('Espessura')
thickness_curv['state'] = 'readonly'
thickness_curv.place(height=20, width=100, x=48*a, y=(c + 3*b))

var5 = tk.StringVar()
sizlist = ['640x480','720x640','1280x720']
siz = ttk.Combobox(janela, values = sizlist, textvariable= var5)
siz.set('Resolução')
siz['state'] = 'readonly'
siz.place(height=20, width=100, x=59*a, y=(c + 3*b))



janela.mainloop()