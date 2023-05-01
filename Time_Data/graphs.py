import matplotlib.pyplot as plt
import pandas as np
import seaborn as sns

tabela = np.DataFrame()

tempo_total_paralelo = open("Tempos_Todos_Paralelos.txt", "rt")
tempo_total_sequencial = open("Tempos_Todos_Sequenciais.txt", "rt")

first_line = tempo_total_paralelo.readline()
first_line_s = tempo_total_sequencial.readline()

n_cpu = []
sizes = []
n_iter = []
time_total = []
time_no_pixel = []
texto = tempo_total_paralelo.readlines()
for line in texto:
    data = line.replace('\n', '').split(",")
    n_cpu.append(data[0]) 
    sizes.append(data[1])
    n_iter.append(data[2])
    time_total.append(data[3])
    time_no_pixel.append(data[4]) 
    
#tabela['Processos'] = n_cpu
tabela['Resolucao'] = sizes
tabela['Iteracoes'] = n_iter
tabela['Tempo Total'] = time_total
#tabela['Tempo Sem Pixel'] = time_no_pixel