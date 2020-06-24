import unittest
import random
from bokeh.plotting import figure, output_file,show


def get_distance(punto_1,punto_2):
    sumas=0
    for num in range(len(punto_1)):
        sumas+=(punto_1[num]-punto_2[num])**2
    dist=sumas**0.5
    return dist

def get_point_med(punto_1,punto_2):
    new_point=[]
    for num in range(len(punto_1)):
        new_point.append((punto_1[num]+punto_2[num])/2)    
    return new_point

def creacion_puntos(rango, num_puntos, num_dimensiones):
    puntos=[]
    for _ in range(num_puntos): 
        punto=[]
        for num in range(num_dimensiones):
            dimension=random.randint(rango[num][0],rango[num][1])            
            punto.append(dimension)        
        puntos.append(punto)
    return puntos

def mscatter(p, x, y, typestr):
    p.scatter(x, y, marker=typestr, 
            line_color="#6666ee", fill_color="#ee6666", fill_alpha=0.5, size=12)

def mtext(p, x, y, textstr):
    p.text(x, y, text=[textstr],
         text_color="#449944", text_align="center", text_font_size="10pt")


def agrupamiento(puntos):
    arbol=[puntos,]
    while len(arbol[-1])>1:
        nueva_rama=[]
        indices_usados=[]
        for num_1 in range(len(arbol[-1])-1):
            if indices_usados.count(num_1)== 0:
                indices_usados.append(num_1)
                distancias=[]
                puntos_medios=[]  
                posiciones=[]   
                encontro=False                       
                for num_2 in range(num_1+1,len(arbol[-1])):                    
                    if indices_usados.count(num_2)== 0:
                        distancias.append(get_distance(arbol[-1][num_1],arbol[-1][num_2]))
                        puntos_medios.append(get_point_med(arbol[-1][num_1],arbol[-1][num_2]))    
                        posiciones.append(num_2)         
                        encontro=True           
                    else:
                        if num_2==len(arbol[-1])-1 and encontro==False:
                            distancias.append(0)                                                        
                            puntos_medios.append(arbol[-1][num_1])      
                            posiciones.append(num_1)                                                                              
                        else:
                            continue
                distancia_minima=min(distancias)
                indice=distancias.index(distancia_minima)
                nueva_rama.append(puntos_medios[indice])
                indices_usados.append(posiciones[indice])
            else:
                continue
        arbol.append(nueva_rama)

    return arbol
        


class Pruebas(unittest.TestCase):
    def test_getDistance(self):
        self.assertEqual(get_distance([0,5],[4,2]),5,"no se devulve la distancia correcta")
    
    def test_punto_medio(self):
        self.assertEqual(get_point_med([0,1],[5,1]),[2.5,1],"el punto medio no es el correcto")

if __name__ == "__main__":  
    output_file('Graficado.html')    
    fig=figure()
    print('Especifique su mapa')    
    rango=[]
    num_dimensiones=int(input('Cuantas dimensiones tendrá cada elemento: '))
    for num in range(num_dimensiones):
        i_dim=int(input(f'Inicio de la dimension {num+1}: '))
        f_dim=int(input(f'Fin de la dimension {num+1}: '))
        rango.append([i_dim,f_dim])

    numero_puntos=int(input('Número de puntos: '))    
    puntos=creacion_puntos(rango,numero_puntos,num_dimensiones)        
    arbol=agrupamiento(puntos)
    tipos=["x", "circle_cross","circle","square","asterisk","diamond"]
    jerarquia=0
    for ramas in arbol: 
        tipo=random.sample(tipos,1)     
        jerarquia+=1
        for punto in ramas:      
            mscatter(fig, punto[0], punto[1], tipo)
            mtext(fig,punto[0],punto[1],str(jerarquia))
        print(ramas)

    show(fig)