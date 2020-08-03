import sympy 
from sympy.abc import s,t,x,y,z,a
from sympy.integrals import laplace_transform
from sympy.integrals import inverse_laplace_transform
from tkinter import *

ventana = Tk()
ventana.configure()

ventana.title("Programa para resolver EDO por Laplace, Alumno Ezequiel Ledesma")

lbl = Label(ventana, text="Ingrese los valores en los casilleros para resolver la ecuacion",font=("Arial Bold", 12))
lbl.grid(column=0, row=0)

lbl = Label(ventana, text="Si quiere usar numeros negativos solo agrege el signo delante del numero a ingresar",font=("Arial Bold", 9),fg="gray")
lbl.grid(column=0, row=0)
lbl.place(x=0, y=25)

ventana.geometry('600x200')


entry_var3 = IntVar()

#cuadro de texto
txt1 = Entry(ventana,width=7)
txt1.grid(column=1, row=1)
txt1.place(x=80, y=50)

lbl = Label(ventana, text="X'",font=("Arial Bold", 12))
lbl.grid(column=0, row=0)
lbl.place(x=120, y=48)

lbl = Label(ventana, text="+",font=("Arial Bold", 12))
lbl.grid(column=0, row=0)
lbl.place(x=140, y=48)

txt2 = Entry(ventana,width=7)
txt2.grid(column=2, row=1)
txt2.place(x=160, y=50)

lbl = Label(ventana, text="X",font=("Arial Bold", 12))
lbl.grid(column=0, row=0)
lbl.place(x=200, y=48)

lbl = Label(ventana, text="+",font=("Arial Bold", 12))
lbl.grid(column=0, row=0)
lbl.place(x=220, y=48)

txt3 = Entry(ventana,width=7)
txt3.grid(column=3, row=1)
txt3.place(x=240, y=50)

lbl = Label(ventana, text="=",font=("Arial Bold", 12))
lbl.grid(column=0, row=0)
lbl.place(x=290, y=48)

lbl = Label(ventana, text="0",font=("Arial Bold", 12))
lbl.grid(column=0, row=0)
lbl.place(x=310, y=48)

lbl = Label(ventana, text="Condicion Inicial",font=("Arial Bold", 10))
lbl.grid(column=0, row=0)
lbl.place(x=40, y=80)

lbl = Label(ventana,text="X(0)=" )
lbl.grid(column=0, row=0)
lbl.place(x=150, y=80)

txt4 = Entry(ventana,width=7,textvariable=entry_var3)
txt4.grid(column=1, row=1)
txt4.place(x=190, y=80)

lbl = Label(ventana,text="El resultado es:" ,font=("Arial Bold", 10))
lbl.grid(column=1, row=1)
lbl.place(x=40, y=110)

resultado = Entry(ventana,width=90)
resultado.grid(column=1, row=1)
resultado.place(x=20, y=130)


def calcular(a, b, c, d):
    # Laplace transform (t->s)
    t = sympy.symbols("t", positive=True)
    y = sympy.Function("y")

    edo = a *y(t).diff(t) + b *y(t) + c
    s, Y = sympy.symbols("s, Y", real=True)

  # Calculo la transformada de Laplace 
    L_edo = sympy.laplace_transform(edo, t, s, noconds=True)
  

# Aplicamos la nueva funcion para evaluar las transformadas de Laplace
# de derivadas
    L_edo_2 = laplace_transform_derivatives(L_edo)

# reemplazamos la transfomada de Laplace de y(t) por la incognita Y
# para facilitar la lectura de la ecuación.
    L_edo_3 = L_edo_2.subs(sympy.laplace_transform(y(t), t, s), Y)

# Definimos las condiciones iniciales
#ics = {y(0): 2, y(t).diff(t).subs(t, 0): -3

    ics = {y(0): d}
		
# Aplicamos las condiciones iniciales
    L_edo_4 = L_edo_3.subs(ics)
	
# Resolvemos la ecuación y arribamos a la Transformada de Laplace
# que es equivalente a nuestra ecuación diferencial
    Y_sol = sympy.solve(L_edo_4, Y)
	
# Por último, calculamos al inversa de la Transformada de Laplace que 
# obtuvimos arriba, para obtener la solución de nuestra ecuación diferencial.
    y_sol = sympy.inverse_laplace_transform(Y_sol[0], s, t)
  
    return y_sol

def laplace_transform_derivatives (e):
       
   # Evalua las transformadas de Laplace de derivadas de funciones sin evaluar.
    
    if isinstance(e, sympy.LaplaceTransform):
        if isinstance(e.args[0], sympy.Derivative):
            d, t, s = e.args 
            n = len(d.args) - 1
            return ((s**n) * sympy.LaplaceTransform(d.args[0], t, s) -
                    sum([s**(n-i) * sympy.diff(d.args[0], t, i-1).subs(t, 0)
                         for i in range(1, n+1)]))
        
    if isinstance(e, (sympy.Add, sympy.Mul)):
        t = type(e) 
        return t(*[laplace_transform_derivatives(arg) for arg in e.args])
    
    return e
   

def clicked():
    
    resultado.delete(0,'end')
    a = int(txt1.get()) 
    b = int(txt2.get()) 
    c = int(txt3.get()) 
    d = int(txt4.get()) 

    resultado.insert(0,calcular(a,b,c,d)) 

btn = Button(ventana,text='Resolver', command=lambda: clicked(),fg = "Blue")
btn.grid(column=0,row=2)
btn.place(x=180, y=160)


ventana.mainloop()