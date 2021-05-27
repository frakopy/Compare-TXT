import tkinter as tk
from tkinter import font
from tkinter import *
from tkinter import filedialog, messagebox
import os, difflib, time
from concurrent.futures import ThreadPoolExecutor
import win32gui, win32con

#-----------------------------Ocultamos automaticamente la consola de cmd---------------------------------------------
consola = win32gui.GetForegroundWindow()
win32gui.ShowWindow(consola , win32con.SW_HIDE)
#--------------------------------------------------------------------------------------------------------------------


class app_file_comparer():

    def __init__(self):
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font12 = "-family {@Yu Mincho Demibold} -size 12 -weight bold"
        font18 = "-family {@Yu Gothic} -size 14 -weight bold -slant "  \
            "italic"
        
        #Guardamaos en una varibale la ruta donde guardaremos nuestro archivo .html con las diferencias entre los archivos
        self.dir_resultado = 'D:/A_PYTHON/ProgramasPython/Control_NodosCA/File_Comparer/Resultado.html'
        
        #Creamos y cerramos el archivo .html para limpiar su contenido cuando se inicia la aplicacion
        open(self.dir_resultado, 'w').close()

        #Directorio por defecto que se muestra cuando presionamos los botones para seleccionar los archivos
        self.dir_inicial = 'C:/Users/FRANK BOJORQUEZ/Desktop'

        #Iniciamos con valores vacios las varibles donde guardaremos la ruta de los archivos a seleccionar
        #para obligar al usuario a seleccionar los archivos, se controla con condicionales mas adelante
        self.f1 = ''
        self.f2 = ''

        #Creamos nuestra piscina de trheads para llamar a 2 funciones al mismo tiempo, una de ellas creara
        #una etiqueta que mostrarar un mensaje indicando que se estan comparando los archivos mientras que la
        #otra estra ejecutando el proceso de comparacion para encontrar las diferencias
        self.ejecutor = ThreadPoolExecutor(max_workers=2)

        #UTilizaremos esta variable en bucle while para estar pintando en un label el mensaje de que se
        #esta realizando la comparacion y cuando su valor sea False entonces terminaremos el bucle para
        #luego pintar en pantalla el boton que realiza la comparacion de los files.
        self.comp_en_proceso = True

        #Procedemos a crar la ventana con sus widgets
        self.root = Tk()
        self.root.geometry("342x351")
        self.root.resizable(0, 0)
        self.root.iconbitmap('comp.ico')
        self.root.title("FILE COMPARER")
        self.root.configure(background="#7a7a7a")

        #-------------------------  Creacion de la barra de Menu ----------------------------------------------------------------------------
        self.barraMenu = Menu(self.root)
        self.root.config(menu=self.barraMenu)
        
        self.archivo= Menu(self.barraMenu,tearoff=0)
        self.barraMenu.add_cascade(label="Archivo", menu=self.archivo)
        self.archivo.add_command(label="Guardar", command=self.guardar_resultado)
        self.archivo.add_command(label="Salir", command=self.salir)

        self.about= Menu(self.barraMenu,tearoff=0)
        self.barraMenu.add_cascade(label="Información", menu=self.about)
        self.about.add_command(label="Acerca de...", command=self.info)
        

        self.B1 = tk.Button(self.root, command=self.abrir_f1)
        self.B1.place(relx=0.0, rely=0.285, height=56, width=342)
        self.B1.configure(activebackground="#df7000")
        self.B1.configure(activeforeground="#000000")
        self.B1.configure(background="#df7000")
        self.B1.configure(borderwidth="10")
        self.B1.configure(disabledforeground="#a3a3a3")
        self.B1.configure(font=font12)
        self.B1.configure(foreground="#000000")
        self.B1.configure(highlightbackground="#d9d9d9")
        self.B1.configure(highlightcolor="black")
        self.B1.configure(pady="0")
        self.B1.configure(text='''ARCHIVO_1''')

        self.B2 = tk.Button(self.root, command=self.abrir_f2)
        self.B2.place(relx=0.0, rely=0.456, height=56, width=342)
        self.B2.configure(activebackground="#df7000")
        self.B2.configure(activeforeground="#000000")
        self.B2.configure(background="#df7000")
        self.B2.configure(borderwidth="10")
        self.B2.configure(disabledforeground="#a3a3a3")
        self.B2.configure(font=font12)
        self.B2.configure(foreground="#000000")
        self.B2.configure(highlightbackground="#d9d9d9")
        self.B2.configure(highlightcolor="black")
        self.B2.configure(pady="0")
        self.B2.configure(text='''ARCHIVO_2''')

        self.B3 = tk.Button(self.root, command=self.llamar_funciones)
        self.B3.place(relx=0.0, rely=0.627, height=56, width=342)
        self.B3.configure(activebackground="#df7000")
        self.B3.configure(activeforeground="#000000")
        self.B3.configure(background="#df7000")
        self.B3.configure(borderwidth="10")
        self.B3.configure(disabledforeground="#a3a3a3")
        self.B3.configure(font=font12)
        self.B3.configure(foreground="#000000")
        self.B3.configure(highlightbackground="#d9d9d9")
        self.B3.configure(highlightcolor="black")
        self.B3.configure(pady="0")
        self.B3.configure(text='''COMPARAR ARCHIVOS''')

        self.B4 = tk.Button(self.root, command= self.ver_resultado)
        self.B4.place(relx=0.0, rely=0.801, height=56, width=342)
        self.B4.configure(activebackground="#df7000")
        self.B4.configure(activeforeground="#000000")
        self.B4.configure(background="#df7000")
        self.B4.configure(borderwidth="10")
        self.B4.configure(disabledforeground="#a3a3a3")
        self.B4.configure(font=font12)
        self.B4.configure(foreground="#000000")
        self.B4.configure(highlightbackground="#d9d9d9")
        self.B4.configure(highlightcolor="black")
        self.B4.configure(pady="0")
        self.B4.configure(text='''VER RESULTADO''')

        self.E1 = tk.Label(self.root)
        self.E1.place(relx=0.0, rely=0.057, height=59, width=342)
        self.E1.configure(background="#7a7a7a")
        self.E1.configure(borderwidth="5")
        self.E1.configure(disabledforeground="#a3a3a3")
        self.E1.configure(font=font18)
        self.E1.configure(foreground="#ffffff")
        self.E1.configure(relief="sunken")
        self.E1.configure(text='''Selecciona los archivos a comparar''')

        self.root.mainloop()

    def info(self):
        messagebox.showinfo('Creador', 'Desarrollo realizado por el ing. Frank Bojorque')

    def salir(self):
        self.root.destroy()

    def guardar_resultado(self):

        if os.stat(self.dir_resultado).st_size == 0:
            self.msg = 'Aun no se ha realizado la comparacion entre el Archivo_1 y el Archivo_2, por lo tanto el archivo que intentas guardar esta vacio'

            messagebox.showwarning('Advertencia',self.msg)

        else:
            self.nom_archivo = filedialog.asksaveasfilename(initialfile='.html',filetypes=[('Todos los archivos', '*.*')])
            if self.nom_archivo:
                self.a = open(self.nom_archivo, 'w')
                self.a.write(self.diferencias)
                self.a.close()

    #Funciona que abre el archivo html con los resultados de las diferencias encontradas entre ambos files
    def ver_resultado(self):
            
        os.startfile(self.dir_resultado)
            
    #Esta funcion se usa para seleccinar un archivo y obtner la ruta de donde se encuentra
    def abrir_f1(self):

        self.f1 = filedialog.askopenfilename(initialdir=self.dir_inicial, filetypes=[('Archivos', '*.*')])
        
        if self.f1 == '':
            self.B1.config(text='ARCHIVO_1')
            self.B2.config(text='ARCHIVO_2')
            messagebox.showinfo('Aviso','No se selecciono ningún archivo')
        
        else:
            self.nom_f1 = self.f1.split('/')
            self.B1.configure(text=self.nom_f1[-1])


    #Esta funcion se usa para seleccinar un archivo y obtner la ruta de donde se encuentra
    def abrir_f2(self):

        self.f2 = filedialog.askopenfilename(initialdir=self.dir_inicial, filetypes=[('Archivos', '*.*')]) 

        if self.f2 == '':
            self.B1.config(text='ARCHIVO_1')
            self.B2.config(text='ARCHIVO_2')
            messagebox.showinfo('Aviso','No se selecciono ningún archivo')
        
        else:
            self.nom_f2 = self.f2.split('/')
            self.B2.configure(text=self.nom_f2[-1])

    #Esta es la funcion que compara ambos archivos, encuentra su diferencias y las escibe en un archivo .html
    def comparar_archivos(self): 

        #Lectura del archivo 1
        with open(self.f1, 'r') as file1:   
            self.lineas_f1 = file1.readlines()

        #Lectura del archivo 2
        with open(self.f2, 'r') as file2:   
            self.lineas_f2 = file2.readlines()
        
        self.nom_encabezado1 = self.f1.split(('/'))[-1]
        self.nom_encabezado2 = self.f2.split(('/'))[-1]

        #Nota el parametor wrapcolumn sirve para delimitar la cantidad de caracteres que tendran las lineas de cada archivo al momento
        #de presentar la comparacion entre ambos, si no se hace esto entonces las lineas para cada archivo son tan extensas que un 
        #solo archivo ocupa toda la pantalla y no se logra apreciar comodamente la comparacion entre ambos archivos.
        self.diferencias = difflib.HtmlDiff(wrapcolumn=57).make_file(
                                                    self.lineas_f1, 
                                                    self.lineas_f2, 
                                                    self.nom_encabezado1, 
                                                    self.nom_encabezado2
                                                    )


        self.rep_diff = open(self.dir_resultado, 'w')
        self.rep_diff.write(self.diferencias)
        self.rep_diff.close()

        self.comp_en_proceso = False

    #Esta funcion borra el boton que dice comparar y pinta en un label el mensaje que indica que se esta comparando los
    # archivos en un bucle while mientras la variable self.comp_en_proceso se True, al ser False destruye el
    # label y pinta nuevamente el boton de comparar 
    def informar_proceso(self):
        
        font18 = "-family {@Yu Gothic} -size 14 -weight bold -slant "  \
            "italic"
        font12 = "-family {@Yu Mincho Demibold} -size 12 -weight bold"

        self.B3.destroy()
        
        while self.comp_en_proceso == True:
            
            self.E2 = tk.Label(self.root)
            self.E2.place(relx=0.0, rely=0.627, height=59, width=342)
            self.E2.configure(background="#7a7a7a")
            self.E2.configure(disabledforeground="#a3a3a3")
            self.E2.configure(font=font18)
            self.E2.configure(foreground="yellow")
            self.E2.configure(text='''Comparando archivos.''')
            time.sleep(0.5)
            self.E2.configure(text='''Comparando archivos..''')
            time.sleep(0.5)
            self.E2.configure(text='''Comparando archivos...''')
            time.sleep(0.5)
            self.E2.configure(text='''Comparando archivos....''')
            time.sleep(0.5)
            self.E2.configure(text='''Comparando archivos.....''')
            time.sleep(0.5)
            self.E2.configure(text='''Comparando archivos......''')
            time.sleep(0.5)
            self.E2.configure(text='''Comparando archivos.......''')
            time.sleep(0.5)

        self.E2.destroy()
        
        self.B3 = tk.Button(self.root, command=self.llamar_funciones)
        self.B3.place(relx=0.0, rely=0.627, height=56, width=342)
        self.B3.configure(activebackground="#df7000")
        self.B3.configure(activeforeground="#000000")
        self.B3.configure(background="#df7000")
        self.B3.configure(borderwidth="10")
        self.B3.configure(disabledforeground="#a3a3a3")
        self.B3.configure(font=font12)
        self.B3.configure(foreground="#000000")
        self.B3.configure(highlightbackground="#d9d9d9")
        self.B3.configure(highlightcolor="black")
        self.B3.configure(pady="0")
        self.B3.configure(text='''COMPARAR ARCHIVOS''')

        self.texto_informativo = 'Se ha finalizado con la comparacion de los archivos, presiona click en el boton "VER RESULTADO" para ver el resultado de la comparacion'
        messagebox.showinfo('Comparacion Finalizada', self.texto_informativo)

        self.B1.configure(text='''ARCHIVO_1''')
        self.B2.configure(text='''ARCHIVO_2''')

        self.comp_en_proceso = True
        
        #Reinicamos el valor de las varibales para obligar al usuario a seleccionar nuevos archivos
        self.f1 = ''
        self.f2 = ''

    #Esta funcion llama a la funcion informar_proceso y comparar_archivos mediante 2 hilos 
    def llamar_funciones(self):
        
        if self.f1 == '' and self.f2 == '':
            messagebox.showerror('ERROR','El Archivo_1 y el Archivo_2 no han sido seleccionados...')
        
        elif self.f1 == '':
            messagebox.showerror('ERROR','El Archivo_1 no ha sido seleccionado...')
        
        elif self.f2 == '':
            messagebox.showerror('ERROR','El Archivo_2 no ha sido seleccionado...')

        else:
            self.ejecutor.submit(self.informar_proceso)
            self.ejecutor.submit(self.comparar_archivos)

if __name__ == "__main__":
    app_file_comparer()
