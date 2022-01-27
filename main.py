#==========================================================================================
from tkinter import *

import numpy as np
import cv2
from openni import openni2

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
from time import sleep

import threading

#==========================================================================================
    #Inicializando kinect
#==========================================================================================

openni2.initialize()
dev = openni2.Device.open_any()
depth_stream = dev.create_depth_stream()
depth_stream.start()

#==========================================================================================
    #Definindo função para vizualização das curvas de nível
#==========================================================================================
    
def exib_CURV():
    n1 = 40 #numero de curvas de niveis

    X = np.arange(0, 640, 1)
    Y = np.arange(0, 480, 1)
    X = X[80:]
    Y = Y[10:480]
    X, Y = np.meshgrid(X, Y)


    frame = depth_stream.read_frame()
    frame_data = frame.get_buffer_as_uint16()

    img = np.frombuffer(frame_data, dtype=np.uint16)
    
    
    Z = np.reshape(img, (480, 640))
    Z = Z[10:480, 80:]
    Z = np.rot90(Z, 2) # rotacionar matriz
    
    fig, ax = plt.subplots()
    CS = ax.contour(X, Y, Z, n1) 
    ax.clabel(CS, fontsize=9, inline=True)
    ax.set_title('Curva de nível')
    plt.show()
#==========================================================================================
    #Definindo função para vizualização em 3D
#==========================================================================================

def exib_3D():
    X = np.arange(0, 640, 1)
    Y = np.arange(0, 480, 1)
    X = X[80:]
    Y = Y[10:480]
    X, Y = np.meshgrid(X, Y)

    frame = depth_stream.read_frame()
    frame_data = frame.get_buffer_as_uint16()
    img = np.frombuffer(frame_data, dtype=np.uint16)
    Z = np.reshape(img, (480, 640))
    Z = Z[10:480, 80:]
    Z = np.fliplr(Z) # rotacionar matriz

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=True)                    
    ax.zaxis.set_major_formatter('{x:.02f}')
    fig.colorbar(surf, shrink=0.5, aspect=5)  
    plt.show()

#==========================================================================================
    #Definindo função para vizualização das curvas de nível em tempor real COM MAPA DE CORES
#==========================================================================================   
def exib_TR():
    while(True):
        sleep(0.05)
        frame = depth_stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()
        img = np.frombuffer(frame_data, dtype=np.uint16)

        img.shape = (1, 480, 640)
        img = np.fliplr(img)    
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 0, 1)
        img = img[10:480, 80:]
   
        img = cv2.convertScaleAbs(img, alpha=0.1) # alterando valor de alpha, altera-se o gradiente
        im_color = cv2.applyColorMap(img, cv2.COLORMAP_JET) #APLIC-SE GRADIENTE
        im_color1 = cv2.applyColorMap(img, cv2.COLORMAP_BONE)

        # FILTROS      
        imgray = cv2.cvtColor (im_color1, cv2.COLOR_BGR2GRAY)
        imgray = cv2.medianBlur(img, 43)#melhor
        #imgray = cv2.bilateralFilter(img, 39, 273, 273)

        for i in range(50):     
            ret, thresh = cv2.threshold (imgray, (5*i), 255, cv2.THRESH_BINARY)
            contours, his  = cv2.findContours (thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(im_color, contours, -1, (0,0,0), 2)

        im_color = cv2.rotate(im_color, cv2.ROTATE_180) # rotacionar imagem
        cv2.imshow("Curvas em tempo real com mapa de cores", (im_color))
        cv2.waitKey(34)
        if cv2.getWindowProperty("Curvas em tempo real com mapa de cores", cv2.WND_PROP_VISIBLE) <1:
            break

#==========================================================================================
    #Definindo função para vizualização em tempo real SEM MAPA DE CORES
#==========================================================================================

def exib_TRB():
    while(True):
        sleep(0.05)
        frame = depth_stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()
        img = np.frombuffer(frame_data, dtype=np.uint16)

        img.shape = (1, 480, 640)
        img = np.fliplr(img)    
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 0, 1)
        img = img[10:480, 80:]
    
        img = cv2.convertScaleAbs(img, alpha=0.1) # alterando valor de alpha, altera-se o gradiente
        im_color = cv2.applyColorMap(img, cv2.COLORMAP_JET) #APLICA-SE GRADIENTE
        im_color1 = cv2.applyColorMap(img, cv2.COLORMAP_BONE)

        # FILTROS      
        imgray = cv2.cvtColor (im_color1, cv2.COLOR_BGR2GRAY)
        imgray = cv2.medianBlur(img, 43)#melhor
        #imgray = cv2.bilateralFilter(img, 39, 273, 273)

        tu = (np.ones(im_color.shape))*255
        for i in range(45):     
            ret, thresh = cv2.threshold (imgray, (5*i), 255, cv2.THRESH_BINARY)
            contours, his  = cv2.findContours (thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(tu, contours, -1, (0,0,0), 2)

        tu = cv2.rotate(tu, cv2.ROTATE_180) # rotacionar imagem
        cv2.imshow("Curvas em tempo real", (tu))
        cv2.waitKey(34)
        if cv2.getWindowProperty("Curvas em tempo real", cv2.WND_PROP_VISIBLE) <1:
            break

#==========================================================================================
    #Definindo função para vizualização do MAPA DE CORES
#==========================================================================================

def exib_MAP():
    while(True):
        sleep(0.05)
        frame = depth_stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()
        img = np.frombuffer(frame_data, dtype=np.uint16)

        img.shape = (1, 480, 640)
        img = np.fliplr(img)    
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 0, 1)
        img = img[10:480, 80:]
       
        img = cv2.convertScaleAbs(img, alpha=0.1) # alterando valor de alpha, altera-se o gradiente
        im_color = cv2.applyColorMap(img, cv2.COLORMAP_JET) #APLIC-SE GRADIENTE

        im_color = cv2.rotate(im_color, cv2.ROTATE_180) # rotacionar imagem
        cv2.imshow("Mapa de cores em tempo real", (im_color))
        cv2.waitKey(34)
        if cv2.getWindowProperty("Mapa de cores em tempo real", cv2.WND_PROP_VISIBLE) <1:
            break

#==========================================================================================
    #adicionando thread
#==========================================================================================

def m1():
    x = threading.Thread(target=exib_TR)
    x.start()

def m2():
    x = threading.Thread(target=exib_TRB)
    x.start()

def m3():
    x = threading.Thread(target=exib_MAP)
    x.start()

def m4():
    x = threading.Thread(target= exib_CURV)
    x.start()

def m5():
    x = threading.Thread(target=exib_3D)
    x.start()
#==========================================================================================
    #Criando interface gráfica
#==========================================================================================

janela = Tk()
janela.geometry("300x400")
janela.title("Interface em desenvolvimento")

a = 20
b = 30
c = 10


botao1 = Button(janela, text="Exibir curvas em tempo real com mapa", command= m1 )
botao1.place(height=20, width=220, x=a, y=(c + 2*b))

botao2 = Button(janela, text="Exibir curvas em tempo real sem mapa", command= m2)
botao2.place(height=20, width=220,x=a, y=(c + 3*b))

botao3 = Button(janela, text="Exibir mapa em tempo real", command= m3)
botao3.place(height=20, width=160,x=a, y=(c + 4*b))

texto = Label(janela, text="Escolha modo de exibição do frame capturado:")
texto.place(height=20, width=250, x=a, y=(c + 5*b))

botao4 = Button(janela, text="Exibir curvas", command= m4)
botao4.place(height=20, width=80,x=a, y=(c + 6*b))

botao5 = Button(janela, text="Exibir superficie", command=m5)
botao5.place(height=20, width=100, x=a, y=(c + 7*b))

janela.mainloop()