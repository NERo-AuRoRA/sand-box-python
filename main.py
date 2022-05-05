import cv2
import numpy as np
import threading
from tkinter import ttk, Tk, IntVar, StringVar, Entry, Scale, messagebox, PhotoImage, DISABLED, NORMAL
from openni import openni2
from matplotlib import pyplot as plt, cm

#==========================================================================================
    #create interface
janela = Tk()
h = janela.winfo_screenheight()
w = janela.winfo_screenwidth()
janela.geometry("%dx%d+%d+%d" % (570, 650, ((w/2) - (570/2)),((h/2) - (680/2))))
janela.title("Interface em desenvolvimento")
janela.resizable(width=0, height=0)

a = 10
b = 30
c = 10
d = 25
#==========================================================================================
    #variables
var1 = IntVar()
check2 = ttk.Checkbutton(janela, text='Cores', variable= var1)
check2.place(height=20, width=100, x=a, y=(c + 7*b))

var2 = IntVar()
check2 = ttk.Checkbutton(janela, text='Curvas', variable= var2)
check2.place(height=20, width=100, x=6*a + 7, y=(c + 7*b))

selected_gradient = StringVar()
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
gradi.set('Estilo de Colormap')
gradi['state'] = 'readonly'
gradi.place(height=20, width=170, x=13*a, y=(c + 7*b))

var3 = IntVar()
list_numbers_curv= [1,3,5,8,10,15,20,30]
numbers_curv = ttk.Combobox(janela, values = list_numbers_curv, textvariable= var3)
numbers_curv.set('Fator de Distância')
numbers_curv['state'] = 'readonly'
numbers_curv.place(height=20, width=125, x=31*a - 8, y=(c + 7*b))

var4 = IntVar()
list_thickness_curv = [1,2,3,4,5,6,7,8]
thickness_curv = ttk.Combobox(janela, values =list_thickness_curv, textvariable= var4)
thickness_curv.set('Espessura da Linha')
thickness_curv['state'] = 'readonly'
thickness_curv.place(height=20, width=125, x=42*a + 9 , y=(c + 7*b))

set_heigth = IntVar()
set_entry = Entry(janela,textvariable = set_heigth)
set_entry.place(height=20, width=50, x=15*a, y=(c + 3*b))

var_a = IntVar()
check_a = ttk.Checkbutton(janela, text='Exibir Altura', variable= var_a)
check_a.place(height=20, width=150, x=a, y=(c + 4*b))
#==========================================================================================
    #Initializing kinect and variables
#==========================================================================================
alt_max = 0
dist = 0
found_box  = 0
key_set = []
list_var = [2, 1, 1, 5, 1, False]
points_area = []
closed_cal = False

openni2.initialize()
#==========================================================================================
    #curve visualization
#==========================================================================================
def exibe_curvas_de_nivel():
    """
    Função para definir a exibição das curvas de nível na imagem.
    """
    try:
        dev = openni2.Device.open_any()
        depth_stream = dev.create_depth_stream()
        depth_stream.start() 
        frame = depth_stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()
    except:
        messagebox.showerror("Erro","Conecte o kinect")
    else:
        img = np.frombuffer(frame_data, dtype=np.uint16)
        n_curvas_de_nivel=30
        x_label=np.arange((points_area[0]), points_area[2], 1)
        y_label=np.arange((points_area[1]), points_area[3], 1)
        x_label, y_label = np.meshgrid(x_label, y_label)
    
        z_label = np.reshape(img, (480, 640))
        z_label =  z_label[(points_area[1]):(points_area[3]), (points_area[0]):(points_area[2])]
        z_label = np.rot90(z_label, 2)

        if alt_max == 0:
            z_label = np.clip(z_label,(found_box - 400), (found_box))
        else:
            z_label = np.clip(z_label,(found_box - alt_max), (found_box))
        img_d1 = np.ones(np.shape(z_label))*(np.amax(z_label)) 
        z_label = img_d1 - z_label

        initial_cmap = cm.get_cmap('jet')
        fig, ax = plt.subplots()
        CS = ax.contour(x_label, y_label, z_label, n_curvas_de_nivel, cmap= initial_cmap)
        ax.clabel(CS, fontsize=9, inline=True)
        ax.set_title('Curva de nível')
        plt.show()
#==========================================================================================
    #3D visualization
#==========================================================================================
def exibe_3d():
    """
    Função para fazer a exibição da imagem em três dimensões
    """
    try:
        dev = openni2.Device.open_any()
        depth_stream = dev.create_depth_stream()
        depth_stream.start() 
        frame = depth_stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()
    except:
        messagebox.showerror("Erro","Conecte o kinect")
    else:
        img = np.frombuffer(frame_data, dtype=np.uint16)
        
        x_label=np.arange((points_area[0]), points_area[2], 1)
        y_label=np.arange((points_area[1]), points_area[3], 1)
        x_label, y_label = np.meshgrid(x_label, y_label)

        z_label = np.reshape(img, (480, 640))
        z_label =  z_label[(points_area[1]):(points_area[3]), (points_area[0]):(points_area[2])]

        if alt_max == 0:
            z_label = np.clip(z_label,(found_box - 400), (found_box))
        else:
            z_label = np.clip(z_label,(found_box - alt_max), (found_box))
        img_d1 = np.ones(np.shape(z_label))*(np.amax(z_label)) 
        z_label = img_d1 - z_label

        initial_cmap = cm.get_cmap('jet')
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        surf = ax.plot_surface(x_label, y_label, z_label, cmap= initial_cmap, linewidth=0, antialiased=True)
        ax.zaxis.set_major_formatter('{x:.02f}')
        fig.colorbar(surf, shrink=0.5, aspect=5)  
        plt.show()
#==========================================================================================
    #display in real time
#==========================================================================================
def exib_TR(mapoption = list_var[0], walloption= list_var[1], curv = list_var[2], n=list_var[3], 
                                                            thicknesscurv= list_var[4], h= 100, w= 100, pos1= 1700,alt_max= alt_max ):                                                         
    """
    Função para fazer a exibição da imagem em três dimensões
    :param mapoption:
    :param walloption:
    :param curv:
    :param n:
    :param thicknesscurv:
    :param h:
    :param w:
    :param pos:
    :return:
    """
    try:
        dev = openni2.Device.open_any()
        depth_stream = dev.create_depth_stream()
        depth_stream.start()
    except:
        messagebox.showerror("Erro","Conecte o kinect")
    else:

        botao_exibTR["state"] = DISABLED
        botao_calibration1["state"] = DISABLED
        botao_calibration2["state"] = DISABLED

        def onMouse2(event, x, y, flags, param):
            global dist    
            if event == cv2.EVENT_MOUSEMOVE:
                dist = img_d[y, x]            
                if (type(dist) == np.float32) and (np.isnan(dist)):
                    dist = int(np.nan_to_num(dist))
                elif (type(dist) == np.float32):
                    dist = int(dist)  

        while(True):
            frame = depth_stream.read_frame()
            frame_data = frame.get_buffer_as_uint16()
            img = np.frombuffer(frame_data, dtype=np.uint16)
            img.shape = (1, 480, 640)

            if alt_max == 0:
                img = np.clip(img,(pos1 - 400), (pos1))
            else:
                img = np.clip(img,(pos1 - alt_max), (pos1))

            img = (np.ones(np.shape(img))*(np.amax(img))) - img
            
            img_d = np.resize(img, (480, 640))
            img_d = np.fliplr(img_d)[(points_area[1]):(points_area[3]), (points_area[0]):(points_area[2])]  

            img = np.fliplr(img)  
            img = np.swapaxes(img, 0, 2)
            img = np.swapaxes(img, 0, 1)  
            img = img[(480 -points_area[3]):(480 -points_area[1]), (640 - points_area[2]):(640 - points_area[0])]   

            alpha = 255 / ((np.amax(img) - np.amin(img)))
            beta = -np.amin(img) * alpha
            img = cv2.convertScaleAbs((img), alpha=alpha, beta = beta)
            img = cv2.medianBlur(img, 19)
            img = cv2.rotate(img, cv2.ROTATE_180)
            im_color = cv2.applyColorMap(img, mapoption)
            im_position = im_color 
            
            x = v1.get()
            y = v2.get()
            res = [x, y]
            im_color = cv2.resize(im_color, res, interpolation=cv2.INTER_LINEAR)
            imgray = cv2.cvtColor (im_color, cv2.COLOR_BGR2GRAY)
            whitewall = (np.ones(im_color.shape))*255
            if walloption == 0: wall = whitewall
            elif walloption == 1: wall = im_color
            if curv == 1:
                for i in range(255):     
                    ret, thresh = cv2.threshold (imgray, (n*i), 255, cv2.THRESH_BINARY)
                    contours, his  = cv2.findContours (thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                    cv2.drawContours(wall, contours, -1, (0,0,0), thicknesscurv)   
            
            deslocamento = np.float32([[1, 0, (v4.get())], [0, 1,( v5.get())]])
            wall = cv2.warpAffine(wall, deslocamento, (w, h))
            ponto = ((v4.get() + (x/2)), (v5.get() + (y/2))) 
            rotacao = cv2.getRotationMatrix2D(ponto, v3.get(), 1.0)
            wall = cv2.warpAffine(wall, rotacao, (w, h))
            
            cv2.imshow("Tempo Real", (wall))            
            if (var_a.get() == 1):
                cv2.imshow("Altitude", im_position)
                cv2.setMouseCallback("Altitude", onMouse2) 
                texto_view_alt["text"] = "(Mova o Cursor Sobre a Imagem): " + str(dist) + " mm"
            cv2.waitKey(34)  
        
            if (cv2.getWindowProperty("Altitude", cv2.WND_PROP_VISIBLE) <1) and (var_a.get() == 1):
                var_a.set(0)
                texto_view_alt["text"] = ""
            if (cv2.getWindowProperty("Altitude", cv2.WND_PROP_VISIBLE) >= 1) and (var_a.get() == 0):
                cv2.destroyWindow("Altitude")
                texto_view_alt["text"] = "" 
            if (cv2.getWindowProperty("Tempo Real", cv2.WND_PROP_VISIBLE) <1) or (list_var[5] == True):  
                texto_view_alt["text"] = "" 
                botao_exibTR["state"] = NORMAL
                botao_calibration1["state"] = NORMAL
                botao_calibration2["state"] = NORMAL
                list_var[5] = False   
                break      
        cv2.destroyAllWindows()    
#==========================================================================================
    #initial calibration
#==========================================================================================
def cal_inicial(): 
    global points_area
    try:
        dev = openni2.Device.open_any()
        depth_stream= dev.create_depth_stream()
        depth_stream.start()
    except:
        messagebox.showerror("Erro","Conecte o kinect")
    else:
        messagebox.showinfo("Info", "Clique sobre o vértice superior esquerdo da caixa, depois sobre o vértice inferior direito da caixa.")
        if len(points_area) !=  0:
            points_area = []
        def onMouse1(event, x, y, flags, param):    
            if event == cv2.EVENT_LBUTTONDOWN:
                points_area.append(x)
                points_area.append(y)
        cv2.namedWindow("Selecionar", cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback("Selecionar", onMouse1)  
        while (True):
            frame = depth_stream.read_frame()
            frame_data = frame.get_buffer_as_uint16()
            img = np.frombuffer(frame_data, dtype=np.uint16)
            img.shape = (1, 480, 640)

            img = np.fliplr(img)    
            img = np.swapaxes(img, 0, 2)
            img = np.swapaxes(img, 0, 1)
            img = cv2.convertScaleAbs((img), alpha=0.1) 
            img = cv2.medianBlur(img, 23)
            img = cv2.equalizeHist(img)
            img = cv2.bitwise_not(img)
            img = cv2.rotate(img, cv2.ROTATE_180) 
            cframe_data = cv2.applyColorMap(img, cv2.COLORMAP_JET) 
            if len(points_area) == 4:   
                if (points_area[0] >= points_area[2]) or (points_area[1] >= points_area[3]):
                    messagebox.showinfo("Info", "Clique sobre o vértice superior esquerdo da caixa, depois sobre o vértice inferior direito. Calibre novamente")
                    points_area = []
                    botao_aplic["state"] = DISABLED
                    botao_exibTR["state"] = DISABLED
                    botao_curv["state"] = DISABLED
                    botao_surface["state"] = DISABLED
                    break
                else:
                    cframe_data = cframe_data[points_area[1]:points_area[3], points_area[0]: points_area[2]]  
            cv2.imshow("Selecionar", cframe_data)
            cv2.waitKey(34)
            if (cv2.getWindowProperty("Selecionar", cv2.WND_PROP_VISIBLE) <1):
                if (len(points_area) != 4):
                    messagebox.showinfo("Info", "Calibre a área da caixa")
                    points_area = []
                    botao_aplic["state"] = DISABLED
                    botao_exibTR["state"] = DISABLED
                    botao_curv["state"] = DISABLED
                    botao_surface["state"] = DISABLED
                    break  
                elif (found_box  != 0):
                    botao_aplic["state"] = NORMAL
                    botao_exibTR["state"] = NORMAL
                    botao_curv["state"] = NORMAL
                    botao_surface["state"] = NORMAL
                    break
                else:
                    botao_aplic["state"] = DISABLED
                    botao_exibTR["state"] = DISABLED
                    botao_curv["state"] = DISABLED
                    botao_surface["state"] = DISABLED
                    break
            if (closed_cal == True):
                points_area = []
                botao_aplic["state"] = DISABLED
                botao_exibTR["state"] = DISABLED
                botao_curv["state"] = DISABLED
                botao_surface["state"] = DISABLED
                break  
        cv2.destroyAllWindows()
#==========================================================================================
    #set reference
#==========================================================================================
def set_f():      
    global key_set
    try:
        dev = openni2.Device.open_any()
        depth_stream= dev.create_depth_stream()
        depth_stream.start()
    except:
        messagebox.showerror("Erro","Conecte o kinect")
    else:
    
        if len(key_set) != 0:
            key_set = []                          

        def onMouse2(event, x, y, flags, param):
            global found_box   
            if event == cv2.EVENT_LBUTTONDOWN:
                found_box  = img_d[y, x]   
                key_set.append(x)
                if (type(found_box ) == np.float32) and (np.isnan(found_box )):
                    found_box  = int(np.nan_to_num(found_box ))
                elif (type(found_box ) == np.float32):
                    found_box  = int(found_box )  

        while(True):
            frame = depth_stream.read_frame()
            frame_data = frame.get_buffer_as_uint16()

            img = np.frombuffer(frame_data, dtype=np.uint16)
            img.shape = (1, 480, 640)
            img_d = np.resize(img, (480, 640))
            img_d = np.fliplr(img_d)

            img = np.fliplr(img)  
            img = np.swapaxes(img, 0, 2)
            img = np.swapaxes(img, 0, 1)  
            img = cv2.convertScaleAbs((img), alpha=0.1) 
            img = cv2.medianBlur(img, 23)  
            img = cv2.equalizeHist(img)
            img = cv2.bitwise_not(img)
            img = cv2.rotate(img, cv2.ROTATE_180)     
            im_color = cv2.applyColorMap(img, cv2.COLORMAP_JET) 

            cv2.imshow("Alt", (im_color))   
            cv2.setMouseCallback("Alt", onMouse2) 
            cv2.waitKey(34)

            if (cv2.getWindowProperty("Alt", cv2.WND_PROP_VISIBLE) <1):  
                messagebox.showinfo("Info", "Selecione distância")
                botao_aplic["state"] = DISABLED
                botao_exibTR["state"] = DISABLED
                botao_curv["state"] = DISABLED
                botao_surface["state"] = DISABLED
                break 
            if  (len(key_set)  != 0):
                if (len(points_area) == 4):
                    botao_aplic["state"] = NORMAL
                    botao_exibTR["state"] = NORMAL
                    botao_curv["state"] = NORMAL
                    botao_surface["state"] = NORMAL
                    break
                else:
                    break
            if (closed_cal == True):
                botao_aplic["state"] = DISABLED
                botao_exibTR["state"] = DISABLED
                botao_curv["state"] = DISABLED
                botao_surface["state"] = DISABLED
                break     
        cv2.destroyAllWindows()    
#==========================================================================================
    #change parameters
#==========================================================================================
def maplic():
    global list_var
    if ((thickness_curv.current() != -1) and (numbers_curv.current() != -1) and (gradi.current() != -1)):
        list_var = [gradi.current(),var1.get(),var2.get(),var3.get(),var4.get(), True]
        botao_exibTR["state"] = NORMAL
        texto_change.place(height=25, width=300, x=22*a, y=(c + 8*b))
    else:
        messagebox.showerror("Erro", "Defina todos os paramêtros")
#==========================================================================================
    #preview permissions
#==========================================================================================
def fal():
    texto_change.place_forget()
    list_var[5] = False
    if list_var == [2, 1, 1, 5, 1, False]:
        messagebox.showinfo("Info", "Parâmetros padrão executados")
#==========================================================================================
    #set altitude values
#==========================================================================================        
def set_alt():
    global alt_max   
    try:
        list_var[5] = True
        if type(alt_max) == int:
            alt_max = (set_heigth.get())
    except:
        messagebox.showerror("Erro","Digite a distância no formato inteiro, em milímetros")
#==========================================================================================
    #quit
#==========================================================================================
def quit_sand():
    global closed_cal
    list_var[5] = True
    closed_cal = True

    if messagebox.askokcancel("Sair", "Deseja fechar SandBox?"):
        janela.destroy()
    else:
        list_var[5] = False
        closed_cal = False
#==========================================================================================
    #Separators
sep1 =ttk.Separator(janela, orient='horizontal')
sep1.place(x=0, y=(d + 2*b), relwidth=1)

sep2 =ttk.Separator(janela, orient='horizontal')
sep2.place(x=0, y=(d + 5*b), relwidth=1)

sep3 =ttk.Separator(janela, orient='horizontal')
sep3.place(x=0, y=(d + 9*b), relwidth=1)

sep4 =ttk.Separator(janela, orient='horizontal')
sep4.place(x=0, y=(d + 16*b), relwidth=1)

sep5 =ttk.Separator(janela, orient='horizontal')
sep5.place(x=0, y=(d + 19*b), relwidth=1)
#==========================================================================================
    #scales
v1 = IntVar()
s1 = ttk.Scale( janela, variable = v1, 
           from_ = 1, to = w, 
           orient = "horizontal") 
s1.set(w/2)
s1.place(height=20, width=400, x=a, y=(c + 11*b))

v2 = IntVar()
s2 = ttk.Scale( janela, variable = v2, 
           from_ = 1, to = h, 
           orient = "horizontal") 
s2.set(h/2)
s2.place(height=20, width=400, x=a, y=(c + 12*b))

v4 = IntVar()
s4 = ttk.Scale( janela, variable = v4, 
           from_ = 0, to = w, 
           orient = "horizontal") 
s4.set(w/2)
s4.place(height=20, width=400, x=a, y=(c + 13*b))

v5 = IntVar()
s5 = ttk.Scale( janela, variable = v5, 
           from_ = 0, to = h, 
           orient = "horizontal") 
s5.set(h/2)
s5.place(height=20, width=400, x=a, y=(c + 14*b))

v3 = IntVar()
s3 = Scale( janela, variable = v3,
           from_ = -180, to = 180, 
           orient = "horizontal") 
s3.set(0)
s3.place(height=20, width=400, x=a, y=(c + 15*b))

#==========================================================================================
    #text
texto_calibration1 = ttk.Label(janela, text=" \u27f6   Selecione a Área da Caixa")
texto_calibration1.place(height=25, width=170, x=12*a, y=(15 + 0*b))

texto_calibration2 = ttk.Label(janela, text=" \u27f6   Selecione Fundo da Caixa")
texto_calibration2.place(height=25, width=170, x=12*a, y=(15 + 1*b))

texto_set = ttk.Label(janela, text="Altitude Máxima:")
texto_set.place(height=20, width=100, x=a, y=(c + 3*b))

texto_param = ttk.Label(janela, text="Defina os Parâmetros:")
texto_param.place(height=20, width=300, x=a, y=(c + 6*b))

texto_comp = ttk.Label(janela, text="Comprimento")
texto_comp.place(height=20, width=100, x=44*a, y=(c + 11*b))

texto_larg = ttk.Label(janela, text="Largura")
texto_larg.place(height=20, width=100, x=44*a, y=(c + 12*b))

texto_moveh = ttk.Label(janela, text="Mover (Horizontal)")
texto_moveh.place(height=20, width=115, x=44*a, y=(c + 13*b))

texto_movev = ttk.Label(janela, text="Mover (Vertical)")
texto_movev.place(height=20, width=110, x=44*a, y=(c + 14*b))

texto_girar = ttk.Label(janela, text="Girar")
texto_girar.place(height=20, width=110, x=44*a, y=(c + 15*b))

texto_proj = ttk.Label(janela, text="Projete e Ajuste: (Win + P) \u27f6 (Estender) \u27f6 (Mova a Imagem)")
texto_proj.place(height=25, width=400, x=a, y=(c + 10*b))

texto_change = ttk.Label(janela, text="Parâmetros Alterados, Pressione Exibir.")

texto_mod = ttk.Label(janela, text="Modos de Exibição:")
texto_mod.place(height=25, width=250, x=a, y=(c + 17*b))

texto_view_alt = ttk.Label(janela, text="")
texto_view_alt.place(height=20, width=280, x=10*a, y=(c + 4*b))
    
#==========================================================================================
    #button

botao_calibration1 = ttk.Button(janela, text="Calibrar", command= lambda: threading.Thread(target=cal_inicial).start())                                 
botao_calibration1.place(height=25, width=100, x=a, y=(15 + 0*b))

botao_calibration2 = ttk.Button(janela, text="Calibrar", command= lambda: threading.Thread(target=set_f).start())
botao_calibration2.place(height=25, width=100,x=a, y=(15 + 1*b))

botao_set_top = ttk.Button(janela, text="Set", command= lambda: set_alt())
botao_set_top .place(height=22, width=75, x=21*a, y=(c + 3*b))

botao_exibTR = ttk.Button(janela, text="Exibir", command= lambda:[fal(), threading.Thread(target=exib_TR, args= (list_var[0],list_var[1],
                                       list_var[2],list_var[3],list_var[4], h, w, found_box, alt_max)).start()])                             
botao_exibTR.place(height=25, width=100, x=a, y=(c + 8*b))
botao_exibTR["state"] = DISABLED

botao_aplic = ttk.Button(janela, text="Aplicar", command= lambda: maplic())                                 
botao_aplic.place(height=25, width=100, x=11*a, y=(c + 8*b))
botao_aplic["state"] = DISABLED

botao_curv = ttk.Button(janela, text="Exibir Curvas", command= lambda: exibe_curvas_de_nivel())
botao_curv.place(height=25, width=100,x=a, y=(c + 18*b))
botao_curv["state"] = DISABLED

botao_surface = ttk.Button(janela, text="Exibir Superfície", command= lambda: exibe_3d())
botao_surface.place(height=25, width=100, x=11*a, y=(c + 18*b))
botao_surface["state"] = DISABLED

botao_exit = ttk.Button(janela, text="Sair", command= lambda: quit_sand())
botao_exit.place(height=25, width=75, x=48*a, y=(10 + 20*b))
#==========================================================================================
    #image

imagem = PhotoImage(file="Nero_Preto_SemFundo.PNG")
imagem = imagem.subsample(8, 8) 
im = ttk.Label(janela, image=imagem)
im.place(height=25, width=110, x=a, y=(10 + 20*b))

janela.protocol("WM_DELETE_WINDOW", quit_sand)

janela.mainloop()