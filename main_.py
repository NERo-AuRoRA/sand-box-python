#                           PLATAFORMA SANDBOX 2/3 2022
#
# Conjunto de abas que permite ao usuario ter acesso às  informações do sistema através da interface gráfica. 
import sys
import os
import cv2
import numpy as np
import threading
from tkinter import IntVar, Toplevel, Checkbutton, Entry, Button, StringVar, PhotoImage, Label, ttk, messagebox, DISABLED, NORMAL
from openni import openni2
from matplotlib import pyplot as plt, cm


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class win_sand(object):
    alt_max = 0
    dist = 0
    found_box  = 0
    key_set = []
    list_var = [2, 1, 1, 5, 1, False]
    points_area = []
    closed_cal = False 
    def __init__(self, **kw):
        path = resource_path("nero_icon.ico")
        self.janela = Toplevel()
        self.janela.title("SandBox")
        self.janela.iconbitmap(path)
        self.h = self.janela.winfo_screenheight()
        self.w = self.janela.winfo_screenwidth()
        self.janela.geometry("%dx%d+%d+%d" % (570, 650, ((self.w/2) - (570/2)),((self.h/2) - (680/2))))
        self.janela.resizable(width=0, height=0)
        self.create_menu_button() 
        self.create_sep() 
        self.create_text() 
        self.create_scales()
        self.create_variables()
        self.image()
        
        openni2.initialize()
        self.janela.protocol("WM_DELETE_WINDOW", self.quit_sand)
    def create_variables(self):
        a = 10
        b = 30
        c = 10
        d = 25

        self.var1 = IntVar()
        self.check2 = Checkbutton(self.janela, text='Cores', variable= self.var1)
        self.check2.place(height=20, width=60, x=a, y=(c + 7*b))

        self.var2 = IntVar()
        self.check2 = Checkbutton(self.janela, text='Curvas', variable= self.var2)
        self.check2.place(height=20, width=60, x=6*a + 7, y=(c + 7*b))

        self.selected_gradient = StringVar()
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
        self.gradi = ttk.Combobox(self.janela, values = lt, textvariable= self.selected_gradient)
        self.gradi.set("Estilo de Colormap")
        self.gradi['state'] = 'readonly'
        self.gradi.place(height=20, width=170, x=13*a, y=(c + 7*b))

        self.var3 = IntVar()
        self.list_numbers_curv= [1,3,5,8,10,15,20,30]
        self.numbers_curv = ttk.Combobox(self.janela, values = self.list_numbers_curv, textvariable= self.var3)
        self.numbers_curv.set('Fator de Distância')
        self.numbers_curv['state'] = 'readonly'
        self.numbers_curv.place(height=20, width=125, x=31*a - 8, y=(c + 7*b))

        self.var4 = IntVar()
        list_thickness_curv = [1,2,3,4,5,6,7,8]
        self.thickness_curv = ttk.Combobox(self.janela, values =list_thickness_curv, textvariable= self.var4)
        self.thickness_curv.set('Espessura da Linha')
        self.thickness_curv['state'] = 'readonly'
        self.thickness_curv.place(height=20, width=125, x=42*a + 9 , y=(c + 7*b))

        self.set_heigth = IntVar()
        self.set_entry = Entry(self.janela,textvariable = self.set_heigth)
        self.set_entry.place(height=20, width=50, x=15*a, y=(c + 3*b))

        self.var_a = IntVar()
        self.check_a = Checkbutton(self.janela, text='Exibir Altura', variable= self.var_a)
        self.check_a.place(height=20, width=90, x=a, y=(c + 4*b))

    def create_scales(self):
        a = 10
        b = 30
        c = 10
        d = 25
        self.v1 = IntVar()
        self.s1 = ttk.Scale(self.janela, variable = self.v1, 
                from_ = 1, to = self.w, 
                orient = "horizontal") 
        self.s1.set(self.w/2)
        self.s1.place(height=20, width=400, x=a, y=(c + 11*b))

        self.v2 = IntVar()
        self.s2 = ttk.Scale(self.janela, variable = self.v2, 
                from_ = 1, to = self.h, 
                orient = "horizontal") 
        self.s2.set(self.h/2)
        self.s2.place(height=20, width=400, x=a, y=(c + 12*b))

        self.v4 = IntVar()
        self.s4 = ttk.Scale(self.janela, variable = self.v4, 
                from_ = 0, to = self.w, 
                orient = "horizontal") 
        self.s4.set(self.w/2)
        self.s4.place(height=20, width=400, x=a, y=(c + 13*b))

        self.v5 = IntVar()
        self.s5 = ttk.Scale(self.janela, variable = self.v5, 
                from_ = 0, to = self.h, 
                orient = "horizontal") 
        self.s5.set(self.h/2)
        self.s5.place(height=20, width=400, x=a, y=(c + 14*b))

        self.v3 = IntVar()
        self.s3 = ttk.Scale(self.janela, variable = self.v3, 
                from_ = -180, to = 180, 
                orient = "horizontal") 
        self.s3.set(0)
        self.s3.place(height=20, width=400, x=a, y=(c + 15*b))
        
    def create_menu_button(self):
        a = 10
        b = 30
        c = 10
        d = 25
        self.botao_calibration1 = Button(self.janela, text="Calibrar", command= lambda: threading.Thread(target=self.cal_inicial).start())                                 
        self.botao_calibration1.place(height=25, width=100, x=a, y=(15 + 0*b))

        self.botao_calibration2 = Button(self.janela, text="Calibrar", command= lambda: threading.Thread(target=self.set_f).start())
        self.botao_calibration2.place(height=25, width=100,x=a, y=(15 + 1*b))

        botao_set_top = Button(self.janela, text="Set", command= lambda: self.set_alt())
        botao_set_top .place(height=22, width=75, x=21*a, y=(c + 3*b))

        self.botao_exibTR = Button(self.janela, text="Exibir", command= lambda:[self.fal(), threading.Thread(target=self.exib_TR, args= (self.list_var[0],self.list_var[1],
                        self.list_var[2],self.list_var[3],self.list_var[4], self.h, self.w, self.found_box, self.alt_max)).start()])                             
        self.botao_exibTR.place(height=25, width=100, x=a, y=(c + 8*b))
        self.botao_exibTR["state"] = DISABLED

        self.botao_aplic = Button(self.janela, text="Aplicar", command= lambda: self.maplic())                                 
        self.botao_aplic.place(height=25, width=100, x=11*a, y=(c + 8*b))
        self.botao_aplic["state"] = DISABLED

        self.botao_curv = Button(self.janela, text="Exibir Curvas", command= lambda: self.exibe_curvas_de_nivel())
        self.botao_curv.place(height=25, width=100,x=a, y=(c + 18*b))
        self.botao_curv["state"] = DISABLED

        self.botao_surface = Button(self.janela, text="Exibir Superfície", command= lambda: self.exibe_3d())
        self.botao_surface.place(height=25, width=100, x=11*a, y=(c + 18*b))
        self.botao_surface["state"] = DISABLED

        botao_exit = Button(self.janela, text="Sair", command= lambda: print(self.quit_sand()))
        botao_exit.place(height=25, width=75, x=48*a, y=(10 + 20*b))
   
    def create_sep(self):
        a = 10
        b = 30
        c = 10
        d = 25
        sep1 =ttk.Separator(self.janela, orient='horizontal')
        sep1.place(x=0, y=(d + 2*b), relwidth=1)

        sep2 =ttk.Separator(self.janela, orient='horizontal')
        sep2.place(x=0, y=(d + 5*b), relwidth=1)

        sep3 =ttk.Separator(self.janela, orient='horizontal')
        sep3.place(x=0, y=(d + 9*b), relwidth=1)

        sep4 =ttk.Separator(self.janela, orient='horizontal')
        sep4.place(x=0, y=(d + 16*b), relwidth=1)

        sep5 =ttk.Separator(self.janela, orient='horizontal')
        sep5.place(x=0, y=(d + 19*b), relwidth=1)

    def create_text(self):
        a = 10
        b = 30
        c = 10
        d = 25
        texto_calibration1 = ttk.Label(self.janela, text=" \u27f6   Selecione a Área da Caixa")
        texto_calibration1.place(height=25, width=170, x=12*a, y=(15 + 0*b))

        texto_calibration2 = ttk.Label(self.janela, text=" \u27f6   Selecione Fundo da Caixa")
        texto_calibration2.place(height=25, width=170, x=12*a, y=(15 + 1*b))

        texto_set = ttk.Label(self.janela, text="Altitude Máxima:")
        texto_set.place(height=20, width=100, x=a, y=(c + 3*b))

        texto_param = ttk.Label(self.janela, text="Defina os Parâmetros:")
        texto_param.place(height=20, width=300, x=a, y=(c + 6*b))

        texto_comp = ttk.Label(self.janela, text="Comprimento")
        texto_comp.place(height=20, width=100, x=44*a, y=(c + 11*b))

        texto_larg = ttk.Label(self.janela, text="Largura")
        texto_larg.place(height=20, width=100, x=44*a, y=(c + 12*b))

        texto_moveh = ttk.Label(self.janela, text="Mover (Horizontal)")
        texto_moveh.place(height=20, width=115, x=44*a, y=(c + 13*b))

        texto_movev = ttk.Label(self.janela, text="Mover (Vertical)")
        texto_movev.place(height=20, width=110, x=44*a, y=(c + 14*b))

        texto_girar = ttk.Label(self.janela, text="Girar")
        texto_girar.place(height=20, width=110, x=44*a, y=(c + 15*b))

        texto_proj = ttk.Label(self.janela, text="Projete e Ajuste: (Win + P) \u27f6 (Estender) \u27f6 (Mova a Imagem)")
        texto_proj.place(height=25, width=400, x=a, y=(c + 10*b))

        self.texto_change = ttk.Label(self.janela, text="Parâmetros Alterados, Pressione Exibir.")

        texto_mod = ttk.Label(self.janela, text="Modos de Exibição:")
        texto_mod.place(height=25, width=250, x=a, y=(c + 17*b))

        self.texto_view_alt = ttk.Label(self.janela, text="")
        self.texto_view_alt.place(height=20, width=280, x=10*a, y=(c + 4*b))
      
    def image(self):
        a = 10
        b = 30
        path = resource_path("Nero_Preto_SemFundo.png")
        self.imagem = PhotoImage(file=path)
        self.imagem = self.imagem.subsample(8, 8)
        im = Label(self.janela, image=self.imagem)
        im.place(height=25, width=110, x=a, y=(10 + 20*b))
        # im.configure(bg = "white")
    
    def exibe_curvas_de_nivel(self):
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
            x_label=np.arange((self.points_area[0]), self.points_area[2], 1)
            y_label=np.arange((self.points_area[1]), self.points_area[3], 1)
            x_label, y_label = np.meshgrid(x_label, y_label)
        
            z_label = np.reshape(img, (480, 640))
            z_label = np.rot90(z_label, 2)
            z_label =  z_label[(480 - self.points_area[3]):(480 - self.points_area[1]), (self.points_area[0]):(self.points_area[2])]
            

            if self.alt_max == 0:
                z_label = np.clip(z_label,(self.found_box - 400), (self.found_box))
            else:
                z_label = np.clip(z_label,(self.found_box - self.alt_max), (self.found_box))
            img_d1 = np.ones(np.shape(z_label))*(np.amax(z_label)) 
            z_label = img_d1 - z_label

            initial_cmap = cm.get_cmap('jet')
            fig, ax = plt.subplots()
            CS = ax.contour(x_label, y_label, z_label, n_curvas_de_nivel, cmap= initial_cmap)
            ax.clabel(CS, fontsize=9, inline=True)
            ax.set_title('Curva de nível')
            plt.show()

    def exibe_3d(self):
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
            
            x_label=np.arange((self.points_area[0]), self.points_area[2], 1)
            y_label=np.arange((self.points_area[1]), self.points_area[3], 1)
            x_label, y_label = np.meshgrid(x_label, y_label)

            z_label = np.reshape(img, (480, 640))
            z_label = np.rot90(z_label, 2)
            z_label =  z_label[(480 - self.points_area[3]):(480 - self.points_area[1]), (self.points_area[0]):(self.points_area[2])]
            
            if self.alt_max == 0:
                z_label = np.clip(z_label,(self.found_box - 400), (self.found_box))
            else:
                z_label = np.clip(z_label,(self.found_box - self.alt_max), (self.found_box))
            img_d1 = np.ones(np.shape(z_label))*(np.amax(z_label)) 
            z_label = img_d1 - z_label

            initial_cmap = cm.get_cmap('jet')
            fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
            surf = ax.plot_surface(x_label, y_label, z_label, cmap= initial_cmap, linewidth=0, antialiased=True)
            ax.zaxis.set_major_formatter('{x:.02f}')
            fig.colorbar(surf, shrink=0.5, aspect=5)  
            plt.show()

    def exib_TR(self, mapoption = 2, walloption= 1, curv = 1, n=5, 
                                    thicknesscurv= 1, h= 100, w= 100, pos1= 1700,alt_max= 0 ):                                                         
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

            self.botao_exibTR["state"] = DISABLED
            self.botao_calibration1["state"] = DISABLED
            self.botao_calibration2["state"] = DISABLED

            def onMouse2(event, x, y, flags, param):
                if event == cv2.EVENT_MOUSEMOVE:
                    self.dist = img_d[y, x]            
                    if (type(self.dist) == np.float32) and (np.isnan(self.dist)):
                        self.dist = int(np.nan_to_num(self.dist))
                    elif (type(self.dist) == np.float32):
                        self.dist = int(self.dist)  

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
                img_d = np.fliplr(img_d)[(self.points_area[1]):(self.points_area[3]), (self.points_area[0]):(self.points_area[2])]  

                img = np.fliplr(img)  
                img = np.swapaxes(img, 0, 2)
                img = np.swapaxes(img, 0, 1)  
                img = img[(480 - self.points_area[3]):(480 - self.points_area[1]), (640 - self.points_area[2]):(640 - self.points_area[0])]   

                alpha = 255 / ((np.amax(img) - np.amin(img)))
                beta = -np.amin(img) * alpha
                img = cv2.convertScaleAbs((img), alpha=alpha, beta = beta) 
                img = cv2.medianBlur(img, 19)   
                img = cv2.rotate(img, cv2.ROTATE_180)       
                im_color = cv2.applyColorMap(img, mapoption) 
                im_position = im_color 
                
                x = self.v1.get()
                y = self.v2.get()
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
                
                deslocamento = np.float32([[1, 0, (self.v4.get())], [0, 1,( self.v5.get())]])
                wall = cv2.warpAffine(wall, deslocamento, (w, h))
                ponto = ((self.v4.get() + (x/2)), (self.v5.get() + (y/2))) 
                rotacao = cv2.getRotationMatrix2D(ponto, self.v3.get(), 1.0)
                wall = cv2.warpAffine(wall, rotacao, (w, h))
                
                cv2.imshow("Tempo Real", (wall))            
                if (self.var_a.get() == 1):
                    cv2.imshow("Altitude", im_position)
                    cv2.setMouseCallback("Altitude", onMouse2) 
                    self.texto_view_alt["text"] = "(Mova o Cursor Sobre a Imagem): " + str(self.dist) + " mm"
                cv2.waitKey(34)  
            
                if (cv2.getWindowProperty("Altitude", cv2.WND_PROP_VISIBLE) <1) and (self.var_a.get() == 1):
                    self.var_a.set(0)
                    self.texto_view_alt["text"] = ""
                if (cv2.getWindowProperty("Altitude", cv2.WND_PROP_VISIBLE) >= 1) and (self.var_a.get() == 0):
                    cv2.destroyWindow("Altitude")
                    self.texto_view_alt["text"] = "" 
                if (cv2.getWindowProperty("Tempo Real", cv2.WND_PROP_VISIBLE) <1) or (self.list_var[5] == True):  
                    self.texto_view_alt["text"] = "" 
                    self.botao_exibTR["state"] = NORMAL
                    self.botao_calibration1["state"] = NORMAL
                    self.botao_calibration2["state"] = NORMAL
                    self.list_var[5] = False   
                    break      
            cv2.destroyAllWindows()    
    def cal_inicial(self): 
        try:
            dev = openni2.Device.open_any()
            depth_stream= dev.create_depth_stream()
            depth_stream.start()
        except:
            messagebox.showerror("Erro","Conecte o kinect")
        else:
            messagebox.showinfo("Info", "Clique sobre o vértice superior esquerdo da caixa, depois sobre o vértice inferior direito da caixa.")
            if len(self.points_area) !=  0:
                self.points_area = []
            def onMouse1(event, x, y, flags, param):    
                if event == cv2.EVENT_LBUTTONDOWN:
                    self.points_area.append(x)
                    self.points_area.append(y)
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
                if len(self.points_area) == 4:   
                    if (self.points_area[0] >= self.points_area[2]) or (self.points_area[1] >= self.points_area[3]):
                        messagebox.showinfo("Info", "Clique sobre o vértice superior esquerdo da caixa, depois sobre o vértice inferior direito. Calibre novamente")
                        self.points_area = []
                        self.botao_aplic["state"] = DISABLED
                        self.botao_exibTR["state"] = DISABLED
                        self.botao_curv["state"] = DISABLED
                        self.botao_surface["state"] = DISABLED
                        break
                    else:
                        cframe_data = cframe_data[self.points_area[1]:self.points_area[3], self.points_area[0]: self.points_area[2]]  
                cv2.imshow("Selecionar", cframe_data)
                cv2.waitKey(34)
                if (cv2.getWindowProperty("Selecionar", cv2.WND_PROP_VISIBLE) <1):
                    if (len(self.points_area) != 4):
                        messagebox.showinfo("Info", "Calibre a área da caixa")
                        self.points_area = []
                        self.botao_aplic["state"] = DISABLED
                        self.botao_exibTR["state"] = DISABLED
                        self.botao_curv["state"] = DISABLED
                        self.botao_surface["state"] = DISABLED
                        break  
                    elif (self.found_box  != 0):
                        self.botao_aplic["state"] = NORMAL
                        self.botao_exibTR["state"] = NORMAL
                        self.botao_curv["state"] = NORMAL
                        self.botao_surface["state"] = NORMAL
                        break
                    else:
                        self.botao_aplic["state"] = DISABLED
                        self.botao_exibTR["state"] = DISABLED
                        self.botao_curv["state"] = DISABLED
                        self.botao_surface["state"] = DISABLED
                        break
                if (self.closed_cal == True):
                    self.points_area = []
                    self.botao_aplic["state"] = DISABLED
                    self.botao_exibTR["state"] = DISABLED
                    self.botao_exibTR["state"] = DISABLED
                    self.botao_exibTR["state"] = DISABLED
                    self.botao_exibTR["state"] = DISABLED
                    self.botao_exibTR["state"] = DISABLED
                    self.botao_curv["state"] = DISABLED
                    self.botao_surface["state"] = DISABLED
                    break  
            cv2.destroyAllWindows()

    def set_f(self):      
        try:
            dev = openni2.Device.open_any()
            depth_stream= dev.create_depth_stream()
            depth_stream.start()
        except:
            messagebox.showerror("Erro","Conecte o kinect")
        else:
        
            if len(self.key_set) != 0:
                self.key_set = []                          

            def onMouse2(event, x, y, flags, param):   
                if event == cv2.EVENT_LBUTTONDOWN:
                    self.found_box  = img_d[y, x]   
                    self.key_set.append(x)
                    if (type(self.found_box ) == np.float32) and (np.isnan(self.found_box )):
                        self.found_box  = int(np.nan_to_num(self.found_box ))
                    elif (type(self.found_box ) == np.float32):
                        self.found_box  = int(self.found_box )  

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
                    self.botao_aplic["state"] = DISABLED
                    self.botao_exibTR["state"] = DISABLED
                    self.botao_curv["state"] = DISABLED
                    self.botao_surface["state"] = DISABLED
                    break 
                if  (len(self.key_set)  != 0):
                    if (len(self.points_area) == 4):
                        self.botao_aplic["state"] = NORMAL
                        self.botao_exibTR["state"] = NORMAL
                        self.botao_curv["state"] = NORMAL
                        self.botao_surface["state"] = NORMAL
                        break
                    else:
                        break
                if (self.closed_cal == True):
                    self.botao_aplic["state"] = DISABLED
                    self.botao_exibTR["state"] = DISABLED
                    self.botao_curv["state"] = DISABLED
                    self.botao_surface["state"] = DISABLED
                    break     
            cv2.destroyAllWindows() 

    def maplic(self):
        a = 10
        b = 30
        c = 10
        d = 25
        if ((self.thickness_curv.current() != -1) and (self.numbers_curv.current() != -1) and (self.gradi.current() != -1)):
            self.list_var = [self.gradi.current(),self.var1.get(),self.var2.get(),self.var3.get(),self.var4.get(), True]
            self.botao_exibTR["state"] = NORMAL
            self.texto_change.place(height=25, width=300, x=22*a, y=(c + 8*b))
        else:
            messagebox.showerror("Erro", "Defina todos os paramêtros")

    def fal(self):
        self.texto_change.place_forget()
        self.list_var[5] = False
        if self.list_var == [2, 1, 1, 5, 1, False]:
            messagebox.showinfo("Info", "Parâmetros padrão executados")

    def set_alt(self):  
        try:
            self.list_var[5] = True
            if type(self.alt_max) == int:
                self.alt_max = (self.set_heigth.get())
        except:
            messagebox.showerror("Erro","Digite a distância no formato inteiro, em milímetros")

    def quit_sand(self):
        self.list_var[5] = True
        self.closed_cal = True

        if messagebox.askokcancel("Sair", "Deseja fechar SandBox?"):
            self.janela.destroy()
        else:
            self.list_var[5] = False
            self.closed_cal = False
