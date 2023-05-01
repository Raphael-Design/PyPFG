import cmath
import numpy as np


#Operations -> + - * /
#Functions:
#e(x) -> exp(x)
#log(x) -> log(x)
#x^1/2 -> sqrt(x)
#cos(x), sin(x), tan(x), acos(x), asin(x), atan(x)
#pi
#e

equacao = "z = cos(z) + z*z"

def isValue(x):
    print('todo')

#remove "z = "
def translate_value_into_code(x):
    if isValue(x):
        print("0")
    elif "+" in x:
        print("1")
    elif "-" in x:
        print("2")
    elif "*" in x:
        print("3")
    elif "/" in x:
        print("4")
