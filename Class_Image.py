import numpy as np
from PIL import Image
import cmath
import multiprocessing as mp
from os import cpu_count
import time

class Fractal:
    imagem = []
    comprimento_imagem = 0
    largura_imagem = 0
    coord_min_x = 0.0
    coord_max_x = 0.0
    coord_min_y = 0.0
    coord_max_y = 0.0
    Numero_Maximo_Iteracoes = 0
    Numero_Processos = 4


    #Condicao_de_parada = "abs(z*z) > 4"
    signal = 1
    stop_value = 4
    Equacao = "cmath.sin(c*c)*cmath.cos(c)+cmath.cos(z)"
    color_r = "i"
    color_g = "int((i*50)%256)"
    color_b = "255 - i"

    def __init__(self, comprimento=1024, largura=1024, minX = -1.0, maxX = 1.0, minY = -1.0, maxY = 1.0, max_iter = 500):
        self.comprimento_imagem = comprimento
        self.largura_imagem = largura
        self.coord_min_x = minX
        self.coord_max_x = maxX
        self.coord_min_y = minY
        self.coord_max_y = maxY
        self.Numero_Maximo_Iteracoes = max_iter
        self.imagem = np.full((self.comprimento_imagem, self.largura_imagem, 3), (0,0,0))
        self.Numero_Processos = mp.cpu_count()
        self.signal = 1
        self.stop_value = 4
        #print(self.Numero_Processos)

    """def fractal_equation(self, c):
        z = c
        for i in range(self.Numero_Maximo_Iteracoes):
            if exec(self.Condicao_de_parada):#abs(z*z) > 4:
                return i
            exec("z = cmath.sin(z*z)*cmath.cos(c)")#cmath.sin(z*z)*cmath.cos(c)
        return self.Numero_Maximo_Iteracoes-1"""
    
    ##Compile and Exec() this entire code##Save returns on a file?Parallel might not work
    ##If can save the file in parallel won't be in order. But I can save the coordinates for painting
    def fractal_equation(self, c):
        print(c)
        z = c
        for i in range(self.Numero_Maximo_Iteracoes):
            if self.signal == 0 and abs(z) > self.stop_value:
                return i
            elif abs(z*z) > self.stop_value:
                return i
            z = cmath.sin(z*z)*cmath.cos(c)+cmath.cos(z)
        return self.Numero_Maximo_Iteracoes-1

    def paint_pixel (self, data):
        for x in data:
            r = x[1]%15
            g = int((x[1]*50)%256)%15
            b = int(255 - x[1])
            self.imagem[x[0]] = (r,g,b)


    
    def salvar_imagem(self, nome_arquivo = "teste.png"):
        pil_imagem = Image.fromarray(self.imagem.astype(np.uint8), "RGB")
        pil_imagem.save(nome_arquivo, "PNG")


    def generate_fractal(self):
        time_before = time.time()
        complex_dict = dict()
        results = []
        pool = mp.Pool(self.Numero_Processos)
        for y in range(self.largura_imagem):
            cy = y * (self.coord_max_y - self.coord_min_y)/(self.largura_imagem - 1) + self.coord_min_y
            for x in range(self.comprimento_imagem):
                cx = x * (self.coord_max_x - self.coord_min_x)/(self.comprimento_imagem - 1) + self.coord_min_x
                complex_dict[complex(cx, cy)] = (x,y)
        print("map")
        # Sequential -> for key, value in complex_dict.items():
        #    results.append(self.fractal_equation(key))
        results = pool.map(self.fractal_equation, [key for key in complex_dict])
        print("end")
        complex_values = list(complex_dict.values())
        data = list(zip(complex_values, results))
        paint_time = time.time()
        print("start painting")
        self.paint_pixel(data)

        end_time = time.time()
        process_time = end_time - time_before
        print(process_time)
        print(end_time - paint_time)

if __name__ == "__main__":
    teste = Fractal()
    print("a")
    teste.generate_fractal()
    teste.salvar_imagem("imagem.png")