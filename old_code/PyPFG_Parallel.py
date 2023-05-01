from os import cpu_count
from PIL import Image
import time
import colorsys
import cmath
import multiprocessing as mp
import numpy as np
import itertools
import cmath

xmin, xmax = -1, 1
ymin, ymax = -1, 1
Numero_Maximo_Iteracoes = 500

comprimento, largura = 540, 540

cpu_count = 3


#image = Image.new("RGB", (comprimento, largura))

def criar_plano (widthX, heightY, minX, maxX, minY, maxY):
    image = Image.new("RGB", (widthX, heightY))
    xmin = minX
    xmax = maxX
    ymin = minY
    ymax = maxY
    return image
            
def fractal_equation(c):
    z = c
    for i in range(Numero_Maximo_Iteracoes):

        if abs(z*z) > 4:
            return i
        z = cmath.sin(z*z)*cmath.cos(c)

    return Numero_Maximo_Iteracoes-1


    
"""def paralel_fractal():
    complex_dict = dict()
    pool = mp.Pool(cpu_count)
    time_before = time.process_time()
    for y in range(largura):
        cy = y * (ymax - ymin)/(largura - 1) + ymin
        for x in range(comprimento):
            cx = x * (xmax - xmin)/(comprimento - 1) + xmin
            complex_dict[complex(cx, cy)] = (x,y)
    results = pool.map(fractal_equation, [key for key in complex_dict])
    end_time = time.process_time()
    process_time = end_time - time_before
    complex_values = list(complex_dict.values())
    for i in range(len(results)):
        r = int(255 - results[i])%50
        g = int((results[i]*50)%256)%50
        b = results[i]%95
        image.putpixel(complex_values[i], (r,g,b))   
    pool.close()
    return process_time"""

def paint_pixel (image, data):
    for x in data:
        r = x[1]
        g = int((x[1]*50)%256)
        b = int(255 - x[1])
        image.putpixel(x[0], (r,g,b))
        print(list(image.getdata()))

def paralel_fractal_2():
    complex_dict = dict()
    pool = mp.Pool(3)
    for y in range(largura):
        cy = y * (ymax - ymin)/(largura - 1) + ymin
        for x in range(comprimento):
            cx = x * (xmax - xmin)/(comprimento - 1) + xmin
            complex_dict[complex(cx, cy)] = (x,y)
    results = pool.map(fractal_equation, [key for key in complex_dict])
    pool.close()
    complex_values = list(complex_dict.values())
    data = list(zip(complex_values, results))
    print("start painting")
    process = mp.Process(target=paint_pixel, args=[image, data])
    process.start()
    process.join()

       

if __name__ == "__main__":
    image = criar_plano(10, 10, xmin, xmax, ymin, ymax)
    arranjo = list(image.getdata())
    print(arranjo)
    #paralel_fractal_2()
    #image.save("fractal.png", "PNG")

    