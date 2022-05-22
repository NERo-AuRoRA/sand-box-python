#                           PLATAFORMA SANDBOX 1/3 2022
#
# Conjunto de abas que permite ao usuario ter acesso às  informações do sistema através da interface gráfica.
import os
import sys
from tkinter import Tk, Button, messagebox, Label, PhotoImage
from main_ import*
from sobre import*


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class myApp(object):
    def __init__(self, **kw):                    
        self.root = Tk()
        self.root.title("SANDBOX")
        self.root.geometry('300x500')
        self.root.configure(bg='white')
        self.root.resizable(width=0, height=0)
        self.create_menu_button()   
        self.image()
        self.root.protocol("WM_DELETE_WINDOW", self.rar)
    def create_menu_button(self):
        avan = Button(self.root, text= "Avançar",command= lambda: win_sand())
        avan.place(height=30, width=100, x=50, y=70)
        avan.configure(bg = "white")

        sobre = Button(self.root, text= "Sobre",command= lambda: sob())
        sobre.place(height=30, width=100, x=150, y=70) 
        sobre.configure(bg = "white")

        sair = Button(self.root, text= "Sair",command= lambda: self.rar())
        sair.place(height=25, width=75, x=200, y=460)   
        sair.configure(bg = "white")
    def rar(self):
        win_sand.list_var[5] = True
        win_sand.closed_cal = True
        if messagebox.askokcancel("Sair", "Deseja fechar SandBox?"):
            self.root.destroy()
        else:
            win_sand.list_var[5] = False
            win_sand.closed_cal = False  
    def image(self):
        path = resource_path("Nero_Preto_SemFundo.png")
        self.imagem = PhotoImage(file=path)
        self.imagem = self.imagem.subsample(5,5)
        im = Label(self.root, image=self.imagem)
        im.place(height=40, width=180, x=70, y=(250))
        im.configure(bg = "white")

    def execute(self):
        self.root.mainloop()


def main(args):
    app_proc = myApp()
    app_proc.execute()

if __name__ == '__main__':
    sys.exit(main(sys.argv))