#                           PLATAFORMA SANDBOX 3/3 2022
#
# Conjunto de abas que permite ao usuario ter acesso às  informações do sistema através da interface gráfica. 
from tkinter import Toplevel, INSERT, WORD, Text
import sys
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class sob(object):
    def __init__(self, **kw):
        path = resource_path("nero_icon.ico")
        self.sob = Toplevel()
        self.sob.iconbitmap(path)
        self.sob.title("SandBox")
        self.sob.geometry('500x450')
        self.sob.configure(bg='white')
        self.sob.resizable(width=0, height=0)
        self.create_text()   
       
        
    def create_text(self):
        atex = Text(self.sob, width=60,
                            height=30,
                            font=("Helvetica", 12),
                            wrap=WORD
                    )

        atex.grid(row=0, column=0)
        atex.pack(pady=20)
        atex.insert(INSERT,
                                    """\
O aplicativo desktop SandBox é uma ferramenta utilizada na criação de práticas e atividades interativas para alunos de Ensino Fundamental e Médio da disciplina de Geografia na criação de relevos e na visualização do mapa de relevo correspondente em tempo real, além de possibilitar interações diversas com as imagens criadas.
                                    """)
        atex.configure(state ='disabled') 
