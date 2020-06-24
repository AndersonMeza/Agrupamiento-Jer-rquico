import unittest
import random
from bokeh.plotting import figure, output_file,show


def get_distance(punto_1,punto_2):
    sumas=0
    for num in range(len(punto_1)):
        sumas+=(punto_1[num]-punto_2[num])**2
    dist=sumas**0.5
    return dist

def actuales_puntos():
    puntos=[[[0,8],'grupo1'],[[1,5],'grupo1'],[[4,3],'grupo1'],[[2,8],'grupo1'],[[2,10],'grupo1'],[[3,4],'grupo1'],[[4,7],'grupo1'],[[5,9],'grupo1'],[[2,5],'grupo1'],
            [[6,3],'grupo2'],[[7,2],'grupo2'],[[8,4],'grupo2'],[[10,0],'grupo2'],[[9,5],'grupo2'],[[8,7],'grupo2'],[[6,6],'grupo2'],[[5,3],'grupo2'],[[8,2],'grupo2']]
    return puntos

def dibujar_puntos(puntos,p):
    colores={'amarillo':'#ffff00','rojo':'#ff0000','verde':'#00ff00','azul':'#0000ff','morado':'#ff00ff'}
    grupos={}    
    for punto in puntos:
        if punto[1] not in grupos.keys():
            tamano=len(grupos.values())
            valores=list(colores.values())
            grupos[punto[1]]=valores[tamano]
        mscatter(p,punto,grupos[punto[1]])
        mtext(p,punto,grupos[punto[1]])

def mscatter(p, punto,color):
    p.scatter(punto[0][0], punto[0][1], marker='circle', line_color=color, fill_color=color, fill_alpha=0.5, size=12)

def mtext(p, punto,color):
    p.text(punto[0][0], punto[0][1], text=[punto[1]],text_color=color, text_align="center", text_font_size="10pt")

def clasificacionKneigborhud(puntos, coo_punto,k):
    fig=figure() 
    dibujar_puntos(puntos,fig)
    puntos_cercanos=[]
    distancias=[]
    for punto in puntos:
        if len(puntos_cercanos)!=k:                      
            distancias.append(get_distance(coo_punto,punto[0]))
            puntos_cercanos.append(punto)
        else:
            distancia=get_distance(coo_punto,punto[0])
            if distancia<max(distancias):
                index=distancias.index(max(distancias))
                distancias[index]=distancia
                puntos_cercanos[index]=punto

    grupos=[]
    for punto in puntos_cercanos:
        mscatter(fig,punto,'#000000')      
        grupos.append(punto[1])                  

    set_grupos=list(set(grupos))
    cantidades=[]
    for grupo in set_grupos:
        cantidades.append(grupos.count(grupo))

    index=cantidades.index(max(cantidades))
    new_point=[coo_punto,set_grupos[index]]

    puntos.append(new_point)
    mscatter(fig,new_point,'#ffaaaa')
    mtext(fig,new_point,'#ffaaaa')
    show(fig)
    
    print(f'El grupo de este punto es {new_point[1]}')
    

    return puntos

def nuevos_puntos():    
    puntos=[]
    grupos=[]
    num_grupos=int(input('¿Cuantos grupos desea tener?(hasta 5): '))
    if num_grupos>5: num_grupos=5
    for num in range(num_grupos):
        nombre=''
        while True:
            nombre=input(f'Cual es el nombre del grupo {num+1}?: ')
            if nombre not in grupos:
                grupos.append(nombre)
                break
            else:
                print("El nombre de este grupo ya se utilizó para un grupo anterior")
        
        num_puntos=int(input('Cuántos puntos tendrá este grupo?: '))
        for num_p in range(num_puntos):
            punto=[]
            x=int(input(f'valor x pt{num_p+1}: '))
            y=int(input(f'valor y pt{num_p+1}: '))
            punto.append([x,y])
            punto.append(nombre)
            puntos.append(punto)

    return puntos


if __name__ == "__main__":
    output_file('Graficado.html')    
    fig=figure()    
    respuesta=int(input('Con que grupos desea trabajar?\n(1)grupos de ejemplo\n(2)definir mis grupos\n'))
    puntos=[]
    if respuesta!=2:        
        puntos=actuales_puntos()
    else:
        puntos=nuevos_puntos()
    
    while True:                
        dibujar_puntos(puntos,fig)
        show(fig)
    
        x_nuevo_punto=int(input('Valor en x del punto a evaluar: '))                
        y_nuevo_punto=int(input('Valor en y del punto a evaluar: '))
        k=0
        while True :
            k=int(input('Ingrese el valor de k: '))
            if k<=len(puntos):
                break
            else:
                input('No hay suficientes puntos para hacer el análisis')

        coordenadas_nuevo_punto=[x_nuevo_punto,y_nuevo_punto]

        puntos=clasificacionKneigborhud(puntos,coordenadas_nuevo_punto,k)

        respuesta=int(input('Desea ingresar otro punto a evaluar? 1.Si 2.No: '))
        if respuesta !=1: break







