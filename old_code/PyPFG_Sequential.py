xmin, xmax = -1, 1
ymin, ymax = -1, 1
Numero_Maximo_Iteracoes = 500

comprimento, largura = 1920, 1080

def iterate_fractal(nIter, equation, canvas):
    result_list = []
    for y in range(largura):
        cy = y * (ymax - ymin)/(largura - 1) + ymin
        for x in range(comprimento):
            cx = x * (xmax - xmin)/(comprimento - 1) + xmin
            c = complex(cx, cy)
            z = c
            for i in range(nIter):
                if abs(z*z) > 4.0:
                    break
                z = (z*z) + c
            r = i
            g = int((i*50)%256)
            b = int(255 - i)
            canvas.putpixel((x, y), (r, g, b))
            result_list.append((x,y,i))
            