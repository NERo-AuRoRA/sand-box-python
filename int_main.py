#                           PLATAFORMA SANDBOX 1/2 2022
#
# Conjunto de abas que permite ao usuario ter acesso às  informações do sistema através da interface gráfica. 
from tkinter import*
import sys
from main_ import*

class myApp(object):
    def __init__(self, **kw):                    
        self.root = Tk()
        self.root.title("SANDBOX")
        self.root.geometry('300x500')
        self.root.configure(bg='white')
        self.create_menu_button()   
        self.image()
        
    def create_menu_button(self):
        avan = Button(self.root, text= "Avançar",command= lambda: win_sand())
        avan.place(height=30, width=100, x=50, y=70)
        avan.configure(bg = "white")

        sobre = Button(self.root, text= "Sobre")
        sobre.place(height=30, width=100, x=150, y=70) 
        sobre.configure(bg = "white")

        sair = Button(self.root, text= "Sair")
        sair.place(height=25, width=75, x=200, y=460)   
        sair.configure(bg = "white")

    def image(self):
        self.imagem = PhotoImage(file="Nero_Preto_SemFundo.PNG")
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